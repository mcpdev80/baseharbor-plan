# driftfix-r1 — PR #1580 uid-target drift diagnosis (correction round, card t-20261114-r28-cli2-uid-target)

- Card: t-20261114-r28-cli2-uid-target (0428-052)
- Mission: /tmp/opencode/mission-target-driftfix.md
- Shift worker session: worker-ornith1.5-laptop (verified at spawn via `codeman agent list`)
- Date: 2026-11-15

## PLAN

- Reality attested: product remote verified via fresh clone in my own zone (/tmp/mtdf-fetch, `git clone --origin origin https://github.com/mcpdev80/baseharbor.git`). The checkout at /home/marcel/dev/baseharbor-ecosystem/baseharbor is QUARANTINED (stale-ref, force-push incident 2026-11-06) and NOT cited.
- Base SHA / origin/main (planning repo): 06816348f260badb4de3e1bc3ccc41bb2b12ac6c (local = origin/main)
- Base ref for the drift: #1578/uid-env head = 756d21b7839a05c83435e6a39fc0daeb8b0580be
- Work done purely by reading remote refs + diffing in fetch zone. No branch cut, no push, no reopen, no merge (mission scope).
- Local build/vet/test on the restored head — BLOCKED on Owner decision (see below: PR #1580 is CLOSED, no PR head to push to).
- Post QUESTION to Owner: cannot restore PR #1580 head by push because the PR is closed; mission forbids reopen/merge.

## REALITY WITNESSES

Fresh clone `git clone --origin origin https://github.com/mcpdev80/baseharbor.git /tmp/mtdf-fetch`. `git ls-remote origin`:

```
3a91e2a8362bc8028c8f4a7ef278f8c9d96df823	refs/heads/lane-0428-uid-target
756d21b7839a05c83435e6a39fc0daeb8b0580be	refs/pull/1578/head
756d21b7839a05c83435e6a39fc0daeb8b0580be	refs/pull/1580/head
```

gh PR #1580 state (`gh pr view 1580 --repo mcpdev80/baseharbor --json`):

```
"baseRefName":"lane-0428-uid-environment","headRefName":"lane-0428-uid-target",
"headRefOid":"756d21b7839a05c83435e6a39fc0daeb8b0580be",
"isDraft":true,"state":"CLOSED","closedAt":"2026-11-15T11:41:50Z","updatedAt":"2026-11-15T11:41:51Z"
```

## DRIFT DIAGNOSIS

- Branch `lane-0428-uid-target` remote head = 3a91e2a8362bc8028c8f4a7ef278f8c9d96df823.
- PR #1580 head = 756d21b7839a05c83435e6a39fc0daeb8b0580be = IDENTICAL to #1578 uid-env (the drift from round-3 MEDIUM-01).
- The branch head 3a91e2a8 = 756d21b7 + exactly 3 target-UID commits (git log):
  - 3a91e2a8 target: fix CLI cmd/baha unit tests for read-triggered UID migration
  - 2247832b target: idempotent legacy-target UID migration + real-CLI tests
  - b60411bd feat(r28): stable target UID without runtime-ownership change (0428-052)
- Ancestry: 756d21b7 IS an ancestor of the branch (git merge-base --is-ancestor 756d21b7 origin/lane-0428-uid-target -> exit 0). Only my 3 commits on top; no foreign commit.
- Diff name-only between PR #1580 head (756d21b7) and branch (3a91e2a8) — exactly the 12 target-UID files the branch carries that the PR head lacks:
  - cmd/baha/application_core_authority_test.go
  - cmd/baha/application_runtime_retirement_preferences_test.go
  - cmd/baha/target.go
  - cmd/baha/target_mutation.go
  - cmd/baha/target_test_helpers_test.go
  - cmd/baha/target_uid_cli_test.go
  - internal/deployment/config_mutation_test.go
  - internal/deployment/config_target_recovery.go
  - internal/deployment/target.go
  - internal/deployment/target_id.go
  - internal/deployment/target_id_test.go
  - internal/deployment/target_migration_test.go
- Consequence: the target-eigene Inhalt (the `targetListItem.UID` field in target.go, internal/deployment/target_id.go +179 lines, etc.) that round-5 restored is present in the branch but ABSENT from the drifted PR #1580 head.

## HOW THE DRIFT AROSE (from round-5 evidence + this round)

- round-5 (mission-052-rebase) rebased lane-0428-uid-target onto 756d21b7 and force-pushed to 3a91e2a8 (target content restored on top of the delivered ENV-BASIS).
- round-5's own INTEGRITY NOTE recorded a transient base-refresh rebased the uid-target chain, so the remote head briefly returned to bare 756d21b7 after the first force-push; an explicit-refspec force-push re-landed 3a91e2a8.
- The live-verify round-3 akte (MEDIUM-01) shows the drift is recurring: the uid-target chain is repeatedly retargeted/reset onto the uid-env head 756d21b7 by base-refresh. This round confirms the branch head has since settled back at 3a91e2a8, but the PR #1580 head itself is STILL bare 756d21b7.

## RESOLUTION (Owner release 2026-11-15, option 2, EXACTLY these two actions)

- Owner (coord) explicit release for exactly: (1) `gh pr reopen 1580`; (2) verify `gh pr view 1580 headRefOid == 3a91e2a8` (branch-sync after reopen; if divergent: document as finding, DO NOT `gh pr edit`). No ready_for_review, no merge, no .github/**.
- `gh pr reopen 1580 --repo mcpdev80/baseharbor` -> Reopened #1580 (0428-052: stable target UID -- DRAFT); REOPEN_EXIT=0.
- Post-reopen `gh pr view 1580 --json`:
  ```
  "baseRefName":"lane-0428-uid-environment","headRefName":"lane-0428-uid-target",
  "headRefOid":"3a91e2a8362bc8028c8f4a7ef278f8c9d96df823",
  "isDraft":true,"state":"OPEN","updatedAt":"2026-11-15T20:18:57Z"
  ```
  headRefOid == 3a91e2a8 == branch head. Branch-synced automatically on reopen. No `gh pr edit` issued.
- PR #1580 now OPEN and its head carries the target content that round-5 restored (3a91e2a8 = 756d21b7 + my 3 target-UID commits).

## LOCAL VERIFICATION (on restored head 3a91e2a8)

Toolchain go1.26.8 linux/amd64, clean tmpfs GOCACHE/GOPATH/HOME to avoid host /tmp disk-quota bleed.

- Build: `go build -o /tmp/mtdf-baha ./cmd/baha` -> BUILD_EXIT=0; version line "BaseHarbor dev".
- Vet: `go vet ./internal/deployment/ ./internal/environment/ ./cmd/baha/` -> VET_EXIT=0.
- `go test ./internal/deployment/ ./internal/environment/` -> ok 0.713s / ok 0.003s.
- `go test ./cmd/baha/ -run 'Target|UID|Migration'` -> ok 19.928s (target-UID CLI subset: migration idempotency, collision fail-closed, explicit UID preservation, legacy migration, config validate/recovery, env-identity rename isolation).
- No regressions; pre-existing env-gated FAILs (internal/database Postgres, internal/controlplaneruntime Docker) are environmental on base-develop too, not touched by this slice.

## CI COVERAGE (read-only, no .github/** edit)

- Re-opened PR #1580 triggers the GitHub-hosted CI. ci.yml `on:` = workflow_dispatch / push to develop + runtime-validation/** / pull_request to develop+main (lines 5-20).
- Job `go-test` (ci.yml ~lines 117-130) runs on every pull_request: `go test ./contracts/... ./internal/... ./spec/...`, `go test ./cmd/baha`, `go vet ./...`. This job covers the target-UID path (cmd/baha, internal/deployment) and runs on the re-opened PR #1580 under the `pull_request` trigger.
- Hosted-run ownership (Eigenes-Run-Pflicht): the exact-head CI run on lane-0428-uid-target is dispatched by the coordinator (per END note in mission step 4). Worker recorded only the trigger/coverage; no run launched by worker (Owner scope).

## BLOCKER (resolved)

- Previously: PR #1580 was a CLOSED draft (closedAt 2026-11-15T11:41:50Z); GitHub does not run CI on closed PRs and a pushed branch does not re-point a closed PR head; mission forbade reopen/merge. This required an Owner decision — posted as a QUESTION (no interactive dialog). Owner granted explicit release for reopen + verify only.

## EVIDENCE PROVENANCE

- Planning repo origin/main confirmed before END:
  - b58da568d56c1b46747581a0788f897c8873cbe7 (my evidence commit `evidence(r28): driftfix-r1 ...`), local = origin/main = b58da568

## repo-rule compliance

- Reading-only this round: no product files edited, no branch cut, no push, no reopen, no merge. No .github/** touched. No reruns/workflow_dispatch.
- Evidence written ONLY in planning repo baseharbor-plan (path evidence/r28-welle1-2026-11-15/cli2-uid-target/driftfix-r1.md). No .evidence/ dir. No main-branch writes to product repos.
- One candidate per chain: only lane-0428-uid-target considered; nothing new cut.
- No subagents used (§4.8). Every command run in own session.

## CLEANLINESS

- No docker/podman compose project started this lane. Cleanliness witness:
  - `docker ps -q | wc -l` -> 0
  - `podman ps -q | wc -l` -> 0

## END
END_DONE lane worker-ornith1.5-laptop: PR #1580 uid-target drift (MEDIUM-01) RESOLVED. Owner (coord) granted explicit release (option 2) for exactly: (1) `gh pr reopen 1580` -> reopens #1580 (draft), EXIT 0; (2) verify head == 3a91e2a8 -> confirmed headRefOid 3a91e2a8 == branch head, branch-synced on reopen; no `gh pr edit`, no ready_for_review, no merge, no .github/**. PR #1580 now OPEN with head 3a91e2a8 = 756d21b7 + my 3 target-UID commits (ancestry-verified, only my commits above base). Local verification on restored head: build EXIT 0, vet EXIT 0, internal/deployment+internal/environment ok, cmd/baha target-UID subset ok (19.9s). CI coverage: ci.yml `go-test` job (pull_request trigger, ~lines 117-130) runs go test ./contracts ./internal ./spec, go test ./cmd/baha, go vet ./... — covers target-UID path on the re-opened PR; exact-head CI run dispatched by coordinator (Owner scope). Branch lane-0428-uid-target already carried correct content (3a91e2a8); only the PR-lifecycle (reopen) was the remaining action. Cleanliness: 0 docker/podman containers. Evidence in planning repo baseharbor-plan.
