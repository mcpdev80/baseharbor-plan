# round-3 — 0428-065 cli2-app-export: golden-record alignment for `baha app export`? premise falsified — BLOCKED (dependency defect, not this candidate)

Task: `t-20261114-r28-cli2-app-export` (card `0428-065`)
Mission: `/tmp/opencode/mission-aexp-r3.md`
Lane/branch: `lane-0428-065-cli2-app-export` (PR #1625, base `cli2-identity-secrets-head`, draft — unchanged)
Candidate: `191367a12df7f0506d321eb578e215a3987e7f5a` (unchanged this round — see "Why no commit")
Session: `d4212c96-16b8-4fe3-a6ef-587d20c0e0d0` · model: worker-flash

Native todowrite tool: not exposed in this session; the plan therefore lives in the
board file (`workers/todos/mission-aexp-r3.md.json`) and in the PLAN list below, per
mission note and AGENTS §4.4.

## PLAN

1. Read mission; verify the authoritative planning repo and remote truth via ls-remote. Done.
2. Attest the mission base (`191367a12`) and the PR #1625 base head (`cli2-identity-secrets-head`). Done.
3. Set up an isolated worktree at exactly `191367a12` and reproduce both unit failures locally. Done.
4. Determine which golden record and which side of the comparison differ. Done.
5. Decide by the mission's rule: source of truth = registry + docs; if a golden/registry
   requirement is not met by `app export`, STOP with the file:line command. Done → rule 5 fired.
6. Would have run build/vet/docs checks and committed a golden-only fix. Done as a verified
   probe (see "Golden-only fix probe") but NOT committed, because it fixes only one of the
   two named failures and the second is not mine to fix.
7. Evidence + END. This file.

## VERDICT

END_BLOCKED. The mission's premise is false for this candidate. Neither failure is caused by
the `baha app export` line or by anything in PR #1625's own commits. Both failures are the
already-merged `secret.reveal` machine-op (card `0428-057`, commit `6f0555c44`) arriving on
this PR's base branch `cli2-identity-secrets-head` without its golden-record regeneration and
without the shared test-invariant update. Fixing them inside candidate #1625 would be a
scope violation (a second candidate for card 057's defect on 065's branch) and would carry
`0428-063`'s in-flight test edit as well.

## REALITY WITNESSES (`git ls-remote origin`, taken 2026-11-16)

```
22e0404c44b81790ab32fff8ca2040d7252cdb98	refs/heads/cli2-identity-secrets-head
191367a12df7f0506d321eb578e215a3987e7f5a	refs/heads/lane-0428-065-cli2-app-export
aff1532c2f6c6782a8c13afad83245d1351815e7	refs/heads/main
191367a12df7f0506d321eb578e215a3987e7f5a	refs/pull/1625/head
```

PR #1625 (`gh pr view 1625`): state `OPEN`, `isDraft: true`, base `cli2-identity-secrets-head`
@ `22e0404c4`, head `191367a12`. Nothing was pushed, merged, closed or re-based by this lane.

Authoritative planning repo (wrong-zone witness, mandated):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote get-url origin
https://github.com/mcpdev80/baseharbor-plan.git
```

## BASE ATTESTATION

This lane created no branch and no commit; it read the existing candidate directly.
- Candidate ref: `refs/heads/lane-0428-065-cli2-app-export` @ `191367a12df7f0506d321eb578e215a3987e7f5a`
  (mission FAST-FORWARD head; the worktree was detached at exactly this SHA).
- PR base ref: `refs/heads/cli2-identity-secrets-head` @ `22e0404c44b81790ab32fff8ca2040d7252cdb98`.
- `git merge-base --is-ancestor 22e0404c 191367a12` → TRUE: the PR base head IS an ancestor of
  the candidate, so the candidate carries its base and is a legitimate fast-forward target.
- `git merge-base --is-ancestor origin/main 191367a12` → TRUE: `main` @ `aff1532c2` is an
  ancestor of the candidate (the stacked base chain reaches the trunk).
- `git merge-base --is-ancestor 191367a12 22e0404c` → FALSE: no reversal, the base does not
  contain the candidate.
- The mission asked to verify `191367a12` beforehand: `ls-remote` above shows the branch still
  exactly at `191367a12`, so a fast-forward push would have been possible. It was not needed.

## REPRODUCTION (both tests, isolated worktree at exactly 191367a12)

Toolchain: `go version go1.26.8 linux/amd64` (from `go.mod`), `GOCACHE` and `GOTMPDIR` under
`/home/marcel/dev/baseharbor-ecosystem/` (never in a foreign zone).

```
$ go test ./contracts/ -run TestMachineControlGoldenRecordsMatchCoreDiscovery -count=1
--- FAIL: TestMachineControlGoldenRecordsMatchCoreDiscovery (0.01s)
    machine_control_test.go:41: public discovery fixture differs from Core operation/binding registry
FAIL	github.com/mcpdev80/baseharbor/contracts	0.020s

$ go test ./cmd/baha/ -run TestAgentDescribeJSON -count=1
--- FAIL: TestAgentDescribeJSON (0.00s)
    agent_mcp_test.go:47: operation missing MCP tool: machine.Operation{ID:"secret.reveal",
      Description:"Human-only authorization seam for managed-secret reveal via a verified operator.
      Workload/runtime identity never satisfies this; the CLI --reveal paths (app env/creds) route
      through it and it is excluded from the MCP tool boundary by design.", Safety:"read_only",
      ConfirmationRequired:false, PolicyRequired:true, ContractVersion:"v1", MCPTool:""}
FAIL	github.com/mcpdev80/baseharbor/cmd/baha	0.009s
```

The hosted CI signature matches the local reproduction exactly (run
[43799450593](https://github.com/mcpdev80/baseharbor/actions/runs/43799450593), job `validate`,
step "Run unit and package tests"): the same two lines, at head `191367a12`, event
`workflow_dispatch`. All other PR jobs were `skipped`, so nothing else failed.

## WHICH GOLDEN RECORD, WHICH SIDE (mission step 1)

- Golden file: `contracts/machine/v1/control.golden.json`, record `"record": "discovery"`,
  sub-object `value.operations` (a list). The comparison is
  `contracts/machine_control_test.go:38-41`:
  `expected := machine.MachineDiscovery(); expected.HTTP = machine.MachineHTTPBindings();
  reflect.DeepEqual(actual, expected)` where `actual` is the golden `discovery` record.
- Side that differs: the golden (stale) side is missing exactly one operation; the registry
  (live) side has it. Machine-checked, not inferred:

```
source ops (internal/machine/contract.go, `ID: "..."`): 95
golden discovery ops (contracts/machine/v1/control.golden.json): 94
missing from golden: ['secret.reveal']
extra in golden:     []
```

- Second failure's side: not a golden record at all. `cmd/baha/agent_mcp_test.go:46-48` asserts
  the invariant "every registered operation carries an MCP tool", and `secret.reveal`
  (`internal/machine/contract.go:202`) deliberately has `MCPTool: ""`.

## DECISION RULE (mission step 2) → STOP + command with file:line

The mission's own rule fires: the requirement behind the failing checks is not carried by
`app export` at all.

1. Cause: `6f0555c44` "fix(0428-057): separate human/runtime secret reveal via secret.reveal op"
   added a machine operation to the shared registry and is already merged into
   `cli2-identity-secrets-head` (PR #1615, whose head IS that branch:
   `refs/pull/1615/head` = `refs/heads/cli2-identity-secrets-head` = `22e0404c4`).
   Its commit touched `internal/machine/contract.go` but NOT
   `contracts/machine/v1/control.golden.json` and NOT `cmd/baha/agent_mcp_test.go`
   (`git show --stat 6f0555c44` → 8 files, neither of those two).
2. Proof this is not caused by `app export`: `git diff 22e0404c 191367a12 --stat` for
   `contracts/machine/v1/control.golden.json`, `internal/machine/contract.go`,
   `contracts/machine_control_test.go` and `cmd/baha/agent_mcp_test.go` is EMPTY.
   My three commits (`fbe703668`, `8d591adbf`, `191367a12`) change only
   `cmd/baha/app_export*.go`, `cmd/baha/commands.go`, `cmd/baha/machine_coverage.go` and the
   four generated EN/DE doc pages.
3. Proof it fails independently of my lane: at the PR #1615 head `6f0555c44` in a fresh
   isolated worktree BOTH named tests fail (`TestMachineControlGoldenRecordsMatchCoreDiscovery`
   → "public discovery fixture differs…", `TestAgentDescribeJSON` → "operation missing MCP tool"),
   and the hosted runs on the base branch itself already failed: 43782856224 (head `6f0555c44`),
   43791086699 (head `5008b991c`), 43795225067 (head `22e0404c4`) — all `failure`, all job
   `validate`, all step "Run unit and package tests".
4. `app export` satisfies its own requirements and needs no golden change: it is classified
   `presentation` with an explicit reason in `cmd/baha/machine_coverage.go:136`, with no
   `cliMachineOperations` mapping, so no operation and no golden entry. The generator
   (`go run ./scripts/tools/machine-control-fixtures`) emits 95 ops whose set differs from the
   committed golden by exactly `secret.reveal` — nothing about export.
5. The fix for failure (b) is already owned elsewhere and is in flight: sibling card
   `0428-063` (PR #1623, branch `lane-0428-063-cli2-app-interact`, commit `78e8257eb`) updates
   the SAME shared assertion to
   `if operation.MCPTool == "" && !strings.Contains(operation.Description, "MCP tool boundary by design")`
   at `cmd/baha/agent_mcp_test.go:49` on that branch. That branch is green for both tests in an
   isolated probe, because its golden regeneration covers all four new ops
   (`app.logs`, `app.exec`, `app.urls`, `secret.reveal`; 98 ops).
   Copying that one-line test change into #1625 would (i) decide card 057's/063's contract
   question from 065's branch, (ii) create a second candidate for the same defect, and (iii)
   make PR #1625 carry 063's in-flight edit — a merge-order conflict on a shared file. Not done.
6. The correct ownership is also the card's own contract: card 065 declares
   `depends_on: [t-20261114-r28-cli2-contract, t-20261114-r28-cli2-identity-secrets]`, and
   `t-20261114-r28-cli2-identity-secrets` is `state: review`, i.e. NOT accepted. Round-1 already
   reported this as a base condition (`evidence/r28-welle1-20261115/cli2-app-export/round-1.md:72`).

COMMAND (what must happen, and where it belongs):
- On the 057 candidate (`cli2-identity-secrets-head`, PR #1615): regenerate the golden discovery
  record, `go run ./scripts/tools/machine-control-fixtures > contracts/machine/v1/control.golden.json`
  — proven to make `TestMachineControlGoldenRecordsMatchCoreDiscovery` and the whole `./contracts`
  package green without any other change (see probe below).
- Plus one shared-test decision, owned by 063's PR #1623 (already implemented at
  `cmd/baha/agent_mcp_test.go:49`) or by the integration owner on the base branch: the
  "every operation has an MCP tool" invariant must exempt operations that document their
  exclusion (`internal/machine/contract.go:202`, and `app.logs`/`app.exec`/`app.urls` from 063).
- Until then PR #1625 cannot go green: its base carries the defect, and per the scope split I
  will not re-base onto 063's unmerged branch (that would stack a second candidate).

## GOLDEN-ONLY FIX PROBE (verified, deliberately NOT committed)

Applied locally in the worktree only, then reverted (`git status --porcelain` → empty):

```diff
--- a/contracts/machine/v1/control.golden.json
+++ b/contracts/machine/v1/control.golden.json
@@ -424,6 +424,14 @@
             "mcp_tool": "baseharbor.secret.tls-set"
           },
           {
+            "id": "secret.reveal",
+            "description": "Human-only authorization seam for managed-secret reveal via a verified operator. Workload/runtime identity never satisfies this; the CLI --reveal paths (app env/creds) route through it and it is excluded from the MCP tool boundary by design.",
+            "safety": "read_only",
+            "confirmation_required": false,
+            "policy_required": true,
+            "contract_version": "v1"
+          },
+          {
             "id": "node.add",
```

Test outcomes with the probe applied at `191367a12`:

```
go test ./contracts -run TestMachineControlGoldenRecordsMatchCoreDiscovery -count=1  → ok
go test ./contracts -count=1                                                        → ok  (whole package, 0.388s)
go test ./internal/machine/... ./contracts/... -count=1                             → all ok
go test ./cmd/baha -run TestAgentDescribeJSON -count=1                              → FAIL (unchanged; needs the test-invariant fix, not a golden)
go test ./cmd/baha -run 'TestAgent|TestMachineDocumentation|TestMachineCoverage|TestMCPRegistrationCI|TestAppExport' → only TestAgentDescribeJSON fails
```

So the golden-only change fixes 1 of the 2 named tests and cannot turn run 43799450593 green.
That is why it was not pushed as a lone commit on this candidate.

## ACTUAL LOCAL RESULTS AT CANDIDATE `191367a12` (unchanged tree)

```
go build ./...                                          exit 0
go vet ./cmd/baha/ ./contracts/ ./internal/machine/      exit 0
go test ./cmd/baha -run TestAppExport -count=1           ok   1.139s   (this card's own tests)
go test ./cmd/baha -run TestMachineDocumentationTracksRegistryAndCommandTree -count=1   ok
go test ./cmd/baha -run TestMCPGenericClientDiscoversCompleteSemanticSurfaceAndExercisesReadOnlyTools  ok
go test ./internal/machine/                             ok
go test ./contracts -run TestMachineControlGoldenRecordsMatchCoreDiscovery   FAIL (see above)
go test ./cmd/baha  -run TestAgentDescribeJSON                               FAIL (see above)
bash scripts/documentation-audit.sh                     all sections PASS, exit 0
python3 scripts/check_de_translation_integrity.py       DE technical integrity: PASS (167 paired pages)
```

This reproduces the CI picture exactly: my card's own surface is green; the two red tests are
base-carried.

## CI ROUTING (no new test added → no CI wiring needed)

No test was created or modified by this lane, so the CI-capture duty (AGENTS §5.3) is not
triggered. For the record, the gate that runs these assertions is the `validate` job of
`.github/workflows/ci.yml` ("Run unit and package tests", `go test ./...` shards); the
selector's own mapping is at `scripts/pr-gate-plan.py:545` and `scripts/pr-gate-plan.py:1483`,
which route `contracts/machine/v1/control.golden.json` and `contracts/**.json` to
`CODE_CHECKS` = `go test ./internal/application/... ./contracts/...`
(`scripts/pr-gate-plan.py:71`) plus `integration/static/public-contracts`. No `.github/**`
file was edited and no rerun or `workflow_dispatch` was triggered by this lane (CI dispatch
stays with the coordinator).

## WHY NO COMMIT

The mission authorizes a commit only if the golden records need to follow this candidate's
command surface. They do not: the delta belongs to card 057's already-merged registry change,
and the second red test needs a shared-file decision owned by PR #1623. Producing a commit here
would either be incomplete (1 of 2 tests) or would import another card's in-flight change —
both are the "one integration candidate per chain" violation AGENTS §3.8 / §4.2 forbid. Zero
commits, zero pushes, PR #1625 head unchanged at `191367a12`, base unchanged, draft unchanged.

## CLEANLINESS

- No container, compose project, podman quadlet, target or state directory was created or
  started by this lane: no `baha` command was run against any runtime, and no SSH test host
  (`baha-docker` / `baha-podman`) was touched. `ps-witness`: `docker ps --format '{{.Names}}'`
  on this session host was listed read-only and shows ONLY ambient `bh-w169-ci-bootstrap-*`
  stacks owned by other lanes — untouched, as required by the owner hygiene directive.
- Own scratch, all confined to `/tmp/opencode` and the ecosystem's own zones: worktree
  `/tmp/opencode/aexp-r3-wt` (detached at `191367a12`, final `git status --porcelain` empty),
  probe worktrees `/home/marcel/dev/baseharbor-ecosystem/worktrees/aexp-r3-probe/*`, scratch
  `/tmp/opencode/golden-before.json`, `/tmp/opencode/golden-after.json`,
  `/tmp/opencode/golden-regen-candidate.json`, `/tmp/opencode/golden-063.json`,
  `/tmp/opencode/gendiff_test.go`, and the temporary diagnosis aid
  `/tmp/opencode/aexp-r3-wt/contracts/zzdebug_diff_test.go` (deleted before the final
  verification runs). Cache/tmp: `GOCACHE=/home/marcel/dev/baseharbor-ecosystem/go-cache`,
  `GOTMPDIR=/home/marcel/dev/baseharbor-ecosystem/work-gotmp`. The first build attempt failed on
  a `/tmp` quota with a private cache dir `/tmp/opencode/gocache-aexp-r3`, which was deleted;
  nothing else under `/tmp` was created or removed.
- This evidence was written in the dedicated planning worktree
  `/home/marcel/dev/baseharbor-ecosystem/worktrees/aexp-r3-plan` (detached at `origin/main`) and
  pushed there, because concurrent lanes reset the shared `baseharbor-plan/main` checkout fast
  enough that a directly-written untracked file was lost twice — a STATE finding worth noting:
  the plan repo's shared main checkout is a race hazard for evidence writes; use a worktree.
  No product-repo commit or push happened at all.
- No subagent was used (AGENTS §4.8): every step ran in this session.

## OPEN DECISIONS FOR THE COORDINATOR

1. Route a round to `t-20261114-r28-cli2-identity-secrets` (PR #1615) to regenerate
   `contracts/machine/v1/control.golden.json` from the registry (the proven generator fix in the
   probe above) so the base branch itself carries golden parity.
2. Decide who owns the `cmd/baha/agent_mcp_test.go` invariant relaxation: accept it as it
   already stands in PR #1623 (`cmd/baha/agent_mcp_test.go:49`), or move it to the base branch /
   integration candidate so every cli2 lane gets it once. Both #1623 and #1625 stay red until
   then.
3. Then re-dispatch this card's CI: `191367a12` needs no new commit — a rerun on a fixed base
   (or a base refresh carrying the 057/063 fixes) should turn the run green. Tell me if you want
   a golden-only commit pushed here instead; that is an explicit scope decision, not mine to make.

## END

END_BLOCKED mission-aexp-r3.md: 0428-065 round-3 — both named red tests are base-carried from
merged `secret.reveal` (`6f0555c44`, card 057): the golden misses `secret.reveal`
(`contracts/machine_control_test.go:41`, fix = regenerate
`contracts/machine/v1/control.golden.json`, verified green in probe) and the shared invariant
`cmd/baha/agent_mcp_test.go:49` is owned by PR #1623; my candidate's own diff for all four
relevant files is EMPTY and its surface is green. No golden change belongs to `app export`, so no
commit was made; PR #1625 head stays `191367a12` (draft, base `cli2-identity-secrets-head` @
`22e0404c4`, witnessed ancestor). Route the fix to 057/063 or authorize a golden-only commit here.
Evidence: `evidence/r28-welle1-20261115/cli2-app-export/round-3.md` on baseharbor-plan `origin/main`
(witness below).

## EVIDENCE-ON-origin/main WITNESS (second-to-last action, as mandated)

```
$ git ls-tree origin/main -- evidence/r28-welle1-20261115/cli2-app-export/
100644 blob ac44bffc08bafeb487c94cf3b8250118a86819c7	evidence/r28-welle1-20261115/cli2-app-export/round-1.md
100644 blob 55782bee48c83bf5ef57a9f5212528917498c1cf	evidence/r28-welle1-20261115/cli2-app-export/round-2.md
100644 blob 58cca78420efeaaf722fc9b921d286fe0967ef7e	evidence/r28-welle1-20261115/cli2-app-export/round-3.md

$ git ls-remote origin refs/heads/main
f36add09b2e39c504714f4be8afa7ec36b08d4bd	refs/heads/main
```

Evidence commit on planning `origin/main`: `f36add09` (this file, 297 lines, blob
`58cca784`). The END line above is inside that blob, i.e. published before this post.

