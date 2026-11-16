---
id: mission-secrets-r3-golden
title: "t-20261114-r28-cli2-identity-secrets r3: golden fixtures for secret.reveal (PR #1615)"
status: done
lane: secrets-r3-golden
date: 2026-11-16
---

# Round 3 – machine-control golden regeneration (secret.reveal)

Task: t-20261114-r28-cli2-identity-secrets, PR #1615 (draft, base
`cli2-env-policy-head`). The `secret.reveal` operation added on this branch
(`6f0555c4`) was never pulled into the golden record
`contracts/machine/v1/control.golden.json`.

## PLAN

1. Verify remote refs: `cli2-identity-secrets-head` = 22e0404c (sync-head
   confirmed), base `cli2-env-policy-head` = e5ad8a68, PR #1615 head = 22e0404c. DONE
2. Fresh clone of `cli2-identity-secrets-head` (mission-named branch);
   witness `6f0555c44` is ancestor of head. DONE
3. Run `go run ./scripts/tools/machine-control-fixtures`, check diff: only
   the `secret.reveal` discovery record added, no other record moved. DONE
4. `TestMachineControlGoldenRecordsMatchCoreDiscovery` + `go build ./...` +
   `go vet`. DONE
5. One commit on `cli2-identity-secrets-head`, fast-forward push, ls-remote
   witness after push. DONE
6. Evidence committed and pushed to baseharbor-plan origin/main. DONE
7. END post with head SHA. DONE

## Reality witnesses (all via git ls-remote / fresh clone)

- Before work:
  - `22e0404c44b81790ab32fff8ca2040d7252cdb98  refs/heads/cli2-identity-secrets-head`
  - `e5ad8a6882550168ea262b18dfbdf8c2e4518c1d  refs/heads/cli2-env-policy-head`
  - `22e0404c44b81790ab32fff8ca2040d7252cdb98  refs/pull/1615/head`
- Base attestation: branch cut from remote head `22e0404c44b81790ab32fff8ca2040d7252cdb98`
  of `cli2-identity-secrets-head` (the mission-named candidate branch,
  fast-forward). `git merge-base --is-ancestor 6f0555c44 HEAD` → true
  (the secret.reveal commit is in the candidate history).
- After push:
  - `35292a670aa69ac9a737d542c3befa1f232ccc56  refs/heads/cli2-identity-secrets-head`
  - `35292a670aa69ac9a737d542c3befa1f232ccc56  refs/pull/1615/head`
- Candidate commit: `35292a670aa69ac9a737d542c3befa1f232ccc56`
- Provenance: `git log --oneline lane-origin/cli2-env-policy-head..HEAD` lists
  only this chain's own commits:
  - `35292a67` contracts: regenerate machine-control golden fixtures for secret.reveal (mine)
  - `22e0404c` Merge remote-tracking branch 'origin/develop' into cli2-identity-secrets-head (pre-existing branch history)
  - `5008b991` style: gofmt internal/operatorauth/authorization.go (pre-existing branch history)
  - `6f0555c4` fix(0428-057): separate human/runtime secret reveal via secret.reveal op (pre-existing branch history)

  No foreign candidate carried on top; `22e0404c` is ancestor of `35292a67`
  (merge-base witness printed in transcript). Push was fast-forward
  (`22e0404c..35292a67`).

## Golden diff (whole candidate change)

`git diff 22e0404c 35292a67 -- contracts/machine/v1/control.golden.json` →
8 added lines, nothing removed or modified: the `secret.reveal` entry
(`safety: read_only`, `policy_required: true`, `confirmation_required: false`,
no `mcp_tool`) inserted in the discovery `operations` list between
`secret.tls-set` and `node.add`.

Semantic verification before committing (per step-2 instruction "diff
PRUEFEN"): compared every generated record against the committed golden with a
structural diff. Result: added operation ids = `['secret.reveal']`, removed =
`[]`, changed existing operations = `[]`, records 1..16 byte-identical. So the
regeneration moved exactly the expected secret.reveal addition and nothing
else. No stop condition triggered.

## Checks run (own session, self-run duty)

- Environment: go1.26.8 (toolchain from go.mod), linux/amd64.
- `go test ./contracts/ -run TestMachineControlGoldenRecordsMatchCoreDiscovery -v`
  → PASS (and the whole `./contracts/` package → ok).
- Before regeneration the same test FAILED on head 22e0404c with
  `public discovery fixture differs from Core operation/binding registry`
  (reproduced in /tmp/opencode worktree before the quota issue), confirming
  the 065-r3-lane probe witness.
- `go build ./...` → OK.
- `go vet ./contracts/... ./internal/machine/... ./scripts/tools/machine-control-fixtures/` → OK.
- CI: the golden test lives in `./contracts/` and is executed by the standard
  Go unit-test job of the PR workflow (no new test added; no `.github/**`
  change needed). CI dispatch for this push belongs to the coordinator
  ("CI dispatcht coord").

## Follow-up note (for coordinator, not executed here)

After this push the child PRs #1623 (app-interact) and #1625 (app-export)
need to re-merge their base. Coordination is the coordinator's job.

## Deviation / environment notes

- One candidate only: work happened on the mission-named branch
  `cli2-identity-secrets-head`; no second branch was created; PR left draft,
  no merge, no force-push, no `.github/**` edit, no subagents (mission limits).
- The host's `/tmp` tmpfs hit its user quota mid-mission
  ("unable to write loose object file: Disk quota exceeded"), so the working
  clone was rebuilt at `/var/tmp/secrets-r3-golden-wt` with a private Go build
  cache at `/var/tmp/secrets-r3-gocache`. `/tmp/opencode/secrets-r3-golden-wt`
  is a leftover incomplete clone from before the quota hit — safe to remove;
  no content of value lives there (the commit was re-made in the new clone).
  Pre-existing test scratch dirs under /tmp (not created by this lane) caused
  the pressure and were left untouched.
- No containers/compose projects were started by this lane (nothing to tear
  down; cleanliness: host-state unchanged by this lane beyond /var/tmp caches).
- Planning repo verified: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel`
  → `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (correct zone, not workers/).

END_DONE mission-secrets-r3-golden.md: golden regenerated for secret.reveal, candidate 35292a670aa69ac9a737d542c3befa1f232ccc56 pushed fast-forward to cli2-identity-secrets-head (PR #1615), test+build+vet green.
