# children-baseheal — round-1

Mission: /tmp/opencode/mission-children-baseheal.md (base-heal, two paths).
Lane: mission-children-baseheal (Flash worker). Date: 2026-11-16.

## PLAN

1. Done — Reality check: remotes fetched, heads verified (ls-remote below).
2. Done — Worktree set up at /var/tmp/children-baseheal-wt (tmpfs /tmp at 80%, mission line 6).
3. Done — Path A (#1623): merge of origin/cli2-identity-secrets-head into lane-0428-063-cli2-app-interact; no conflicts, golden taken from base; FF push.
4. Done — Path A: build + both tests GREEN (outputs below).
5. Done — Path B (#1625): merge of base into lane-0428-065-cli2-app-export.
6. Done — Path B: first merge candidate RED at TestAgentDescribeJSON (diagnosis below); fixed inside mission rules (063's agent_mcp_test.go:49 invariant applied — this file is owned by the fix per mission line 2, and the 063 lineage owns it); GREEN after fix.
7. Done — Path B: FF-only push (witness below).
8. Done — This evidence file committed and pushed to baseharbor-plan origin/main.
9. Done — No containers/compose started by this lane; END post.

## Base attestation

- Base ref cut/merged from: origin/cli2-identity-secrets-head = 35292a670aa69ac9a737d542c3befa1f232ccc56
  (`git ls-remote origin refs/heads/cli2-identity-secrets-head` output witnessed below).
- Ancestry proofs (both shown in transcripts):
  - Path A: `git merge-base --is-ancestor 1004ecd5f HEAD && git merge-base --is-ancestor 35292a670 HEAD` → "both ancestors OK"
  - Path B: same test on final tip → "both ancestors OK" (fix commit is on top of the merge commit).

## Planning-repo verification (wrong-zone check)

    git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-remote --get-url origin
    https://github.com/mcpdev80/baseharbor-plan.git

## ls-remote witnesses (alt/neu per path)

Before (all three refs, single call):

    35292a670aa69ac9a737d542c3befa1f232ccc56	refs/heads/cli2-identity-secrets-head
    1004ecd5f15519f1bb895c97f51205042ad45bbe	refs/heads/lane-0428-063-cli2-app-interact
    191367a12df7f0506d321eb578e215a3987e7f5a	refs/heads/lane-0428-065-cli2-app-export

After Path A push (FF line: `1004ecd5f..7ee9c8808`):

    7ee9c88088614e02081c784924f7a859c6a78d5a	refs/heads/lane-0428-063-cli2-app-interact

After Path B push (FF line: `191367a12..5e175d36a`), final state of both:

    7ee9c88088614e02081c784924f7a859c6a78d5a	refs/heads/lane-0428-063-cli2-app-interact
    5e175d36a09207064a85d1b2fa22c3cf4bf2f332	refs/heads/lane-0428-065-cli2-app-export

No force-push used: both remote push outputs show `..` fast-forward ranges; pre-push remote tip equals the old head in each case.

## Path A — lane-0428-063-cli2-app-interact (#1623)

Merge: `git merge origin/cli2-identity-secrets-head` → clean, ort strategy, auto-merged contracts/machine/v1/control.golden.json (golden from base taken; no conflict).
Resulting head: 7ee9c88088614e02081c784924f7a859c6a78d5a ("Merge remote-tracking branch 'origin/cli2-identity-secrets-head' into heal-063"; heal-063 was a local branch name, pushed FF to the named candidate branch — no second remote branch created, see cleanup).

    $ go build ./...
    BUILD_EXIT=0
    $ go test ./cmd/baha -run 'TestAgentDescribeJSON' -v
    === RUN   TestAgentDescribeJSON
    --- PASS: TestAgentDescribeJSON (0.00s)
    PASS
    ok  	github.com/mcpdev80/baseharbor/cmd/baha	0.012s
    $ go test ./contracts -run 'TestMachineControlGoldenRecordsMatchCoreDiscovery' -v
    === RUN   TestMachineControlGoldenRecordsMatchCoreDiscovery
    --- PASS: TestMachineControlGoldenRecordsMatchCoreDiscovery (0.01s)
    PASS
    ok  	github.com/mcpdev80/baseharbor/contracts	0.019s

## Path B — lane-0428-065-cli2-app-export (#1625)

First merge candidate b2839b7ce was RED:

    $ go test ./cmd/baha -run 'TestAgentDescribeJSON' -v
    === RUN   TestAgentDescribeJSON
        agent_mcp_test.go:47: operation missing MCP tool: machine.Operation{ID:"secret.reveal", ... excluded from the MCP tool boundary by design.", Safety:"read_only", ConfirmationRequired:false, PolicyRequired:true, ContractVersion:"v1", MCPTool:""}
    --- FAIL: TestAgentDescribeJSON (0.00s)

Diagnosis (root cause, not a product issue): the base (contract.go:202) adds secret.reveal with MCPTool:"" and the by-design phrasing. The 063 lineage fixed agent_mcp_test.go:49 to accept exactly that (#1623 owns the fix). The 065 lineage still carried the pre-fix assertion `if operation.MCPTool == ""` — the base-side old version, because 065 branched before the fix and the mission's conflict case (line 2: "eure agent_mcp_test.go:49-invariant hat VORRANG vor base-version — ihr besitzt den fix") applies to both children of the 057 line.

Fix applied strictly per mission rule 2: took the 063 version of cmd/baha/agent_mcp_test.go (`git checkout 1004ecd5f -- cmd/baha/agent_mcp_test.go`) — no other product change, no file outside the sanctioned invariant touched. Commit 5e175d36a "test: carry the 063 agent_mcp_test.go invariant through base merge (mission rule: lane fix wins)".

After fix (GOFLAGS/GOCACHE as in Path A):

    $ go build ./...
    BUILD OK
    $ go test ./cmd/baha -run 'TestAgentDescribeJSON' -v
    === RUN   TestAgentDescribeJSON
    --- PASS: TestAgentDescribeJSON (0.00s)
    PASS
    ok  	github.com/mcpdev80/baseharbor/cmd/baha	0.011s
    $ go test ./contracts -run 'TestMachineControlGoldenRecordsMatchCoreDiscovery' -v
    === RUN   TestMachineControlGoldenRecordsMatchCoreDiscovery
    --- PASS: TestMachineControlGoldenRecordsMatchCoreDiscovery (0.01s)  [cached]
    PASS
    ok  	github.com/mcpdev80/baseharbor/contracts

## Branch-provenance / log-line check

Path A (`git log --oneline 1004ecd5f..lane-0428-063-cli2-app-interact`):

    7ee9c8808 Merge remote-tracking branch 'origin/cli2-identity-secrets-head' into heal-063
    35292a670 contracts: regenerate machine-control golden fixtures for secret.reveal
    22e0404c4 Merge remote-tracking branch 'origin/develop' into cli2-identity-secrets-head

Path B (`git log --oneline 191367a12..lane-0428-065-cli2-app-export`):

    5e175d36a test: carry the 063 agent_mcp_test.go invariant through base merge (mission rule: lane fix wins)
    b2839b7ce Merge remote-tracking branch 'origin/cli2-identity-secrets-head' into lane-0428-065-cli2-app-export
    35292a670 contracts: regenerate machine-control golden fixtures for secret.reveal
    (+ base-side commits 22e0404c4 and below, common to the sanctioned base 35292a670)

Each list shows only this lane's own merge/fix commit plus the sanctioned base head 35292a670 and base-side commits reachable from it. No foreign candidate lineage: both chains run strictly old-head + origin/cli2-identity-secrets-head.

## Branch cleanup (one candidate per chain)

Local working branches heal-063/heal-065 existed only inside this lane's worktree and were never pushed to origin; remote shows no such refs (final ls-remote above lists only the two named candidate branches). No second branch for either card exists on the remote.

## Container/compose hygiene

This lane started no containers or compose projects. Pre-existing `bh-w169-*` docker containers on this host belong to another lane/owner and were left untouched (ambient rule).

## Findings for coordinator

- TestAgentDescribeJSON on the 065 lineage carried the pre-fix assertion; resolved per mission rule 2 (063 invariant wins). If the coord dispatches further children of the 057 line, they need the same rule.
- CI dispatch is coord's job (mission line 5); this lane triggered nothing hosted and touched no .github/**.

END_DONE mission-children-baseheal.md: both children healed — 063 head 7ee9c8808, 065 head 5e175d36a (FF pushes, build+2 tests green both paths)
