# round-5 — PR #1578 uid-environment, batch8 REQUEST CHANGES response

- Task: `t-20261114-r28-cli2-uid-environment`
- Candidate (before): `9c5bc09a1f1fb0258100a96f8b3cf91c3743d283` (lane-0428-uid-environment)
- Base: `lane-0428-uid-app` @ `22c545d8242f8cfc2acff2a5152ab5ea4f07d170`
- Candidate (after this lane): `6f07aef2c68ba5eb3c2361d8f0bf1dccc676025c`
- Reviewer: CODEX-REVIEW, recipe `evidence/r28-welle1-2026-11-15/cli2-uid-environment/act-1578-review-r5.md` (VERDICT: REQUEST CHANGES)
- Branch provenance: commit parent is exactly `9c5bc09a` (verified `git rev-parse HEAD^` = `9c5bc09a1f1fb0258100a96f8b3cf91c3743d283`); `9c5bc09a` is an ancestor of the new head (`git merge-base --is-ancestor 9c5bc09a HEAD` = YES); `22c545d` (app-base) is an ancestor of `9c5bc09a` (verified on the blobless clone, `git merge-base --is-ancestor 22c545d 9c5bc09a` = YES). No foreign candidate carried on top.

## Obligations from the recipe and how each was met

1. **Destination-under-lock revalidation (finding #1).** `RenameEnvironment`'s source-still-present path re-read only the source and then installed with `os.Rename(tmpName, newPath)`, which could replace an identity a concurrent `GetEnvironment(target, newName)` created after the pre-lock guard. Fixed in `internal/deployment/environment_identity.go`: under the registry write lock, re-stat and re-read `newPath` on the source-present path; if it now carries a DIFFERENT identity, fail closed with `ErrEnvironmentAlreadyExists`; if it already carries OUR identity, converge on it (idempotent no-op). The change is minimal and contained to the locked install body.

2. **No-replace install.** Same edit: a rename only writes to `newPath` when, under the lock, it is still absent or already holds our identity. A foreign identity is refused rather than clobbered.

3. **Race regression test.** Added `TestRenameDoesNotClobberConcurrentDestinationCreator` to `internal/deployment/environment_identity_test.go`. Two pools of 16 goroutines rename two different sources (`race-a-src`, `race-b-src`) onto one still-absent destination; each successful rename records the dst identity it observed under a mutex. The contract asserted: exactly one dst identity ever exists — a flip across writers is the clobber. Verified as a genuine regression:
   - UNPATCHED `9c5bc09a`: FAILS deterministically (identity flips: e.g. `[170fd3d7-... 90ae48a2-...]`).
   - FIXED head `6f07aef`: PASSES 5/5 runs, exactly one stable valid identity.
   Existing pre-existing foreign-destination (`TestRenameRefusesExistingDestinationUID`) and same-rename convergence (`TestRenameConvergesUnderContention`) tests retained and passing.

4. **Remove orphaned CLI slice.** `cmd/baha/command_target_env.go` is unregistered/orphaned (no production command-tree reference; only referenced by itself) and newly added in this PR's diff, out of the domain-only scope (CLI exposure was reverted in the round-6 evidence; the CLI entry belongs to the separately scoped follow-up). Proven via `git log`/`git grep` (no external symbol reference), removed from the candidate by `git rm`. Did NOT delete it globally from any other branch; it remains on `9c5bc09a`/origin.

## Exact-head diff (base->head), 3 files, 136 insertions / 123 deletions

- `cmd/baha/command_target_env.go` — deleted (123 lines)
- `internal/deployment/environment_identity.go` — +34 (destination re-validation + no-replace comment)
- `internal/deployment/environment_identity_test.go` — +102 (new regression test)

`git diff --check` clean.

## Local verification (all on fixed head `6f07aef`, committed tree)

- `go vet ./internal/deployment/ ./internal/environment/`: clean (exit 0)
- `gofmt -l` on both changed Go files: clean (exit 0)
- `go build ./cmd/baha/`: clean (exit 0) after removing the orphaned CLI file
- `go test ./internal/deployment/ ./internal/environment/ -count=1`: ok (deployment 42.8s, environment 0.003s)
- `go test ./internal/deployment/ -run 'TestRenameDoesNotClobberConcurrentDestinationCreator' -count=3`: PASS on fixed head
- Regression witness (unpatched): `go test ... -run TestRenameDoesNotClobberConcurrentDestinationCreator -count=3` FAILS on `9c5bc09a` with "dst identity flipped across concurrent renames"

## Git / provenance witnesses

- `git ls-remote --heads origin lane-0428-uid-environment` BEFORE push: `9c5bc09a1f1fb0258100a96f8b3cf91c3743d283`
- push `origin HEAD:refs/heads/lane-0428-uid-environment`: `9c5bc09a..6f07aef2` (exit 0)
- `git ls-remote --heads origin lane-0428-uid-environment` AFTER push: `6f07aef2c68ba5eb3c2361d8f0bf1dccc676025c`
- commit parent `git rev-parse HEAD^`: `9c5bc09a1f1fb0258100a96f8b3cf91c3743d283`

## repo-rule compliance

- No `.github/**` touched; no CI rerun / workflow_dispatch; no merge, no force-push, no retarget, no `ready_for_review`.
- No subagents used (all steps executed in this session).
- Evidence written only in baseharbor-plan; no `.evidence/` directory, no product-repo writes.
- Branch provenance shown as ancestor of the fetched base head; no foreign candidate carried.

## Status

- DONE — fix + scope cleanup committed to `lane-0428-uid-environment` @ `6f07aef`, pushed to origin. CI to be dispatched by the coordinator.
- END lane: DONE
