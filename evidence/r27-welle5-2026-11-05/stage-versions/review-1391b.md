# CODEX-REVIEW — stage versions, PR #1391 round 2

- Review timestamp: 2026-11-06 00:43 UTC.
- Reviewer: Codex, GPT-6-Luna channel, review pane `codeman-ab08e19f`.
- Verdict: **REJECT current PR head** `ab8f3036b1ed3980311023f0fc5da2037b992cc0` because it contains an out-of-scope `.gitignore` replacement.
- Mission-requested candidate: `60d5896c9c4aec9018786e40aa63e626916e5b01`. It is an ancestor of the current PR head, but is no longer the PR/remote branch HEAD. The PR and `git ls-remote origin refs/heads/work/r27-stage-versions` both point to `ab8f3036b1ed3980311023f0fc5da2037b992cc0`.
- PR #1391 is OPEN, base `develop`; `develop` is `21d8d05cf1acf04729077e05eb350fcd3bb018ed` and is an ancestor of the current head (rc=0).
- The requested run [42131821530](https://github.com/mcpdev80/baseharbor/actions/runs/42131821530) is terminal success at the requested `60d5896…` head. Current-head run [42135376590](https://github.com/mcpdev80/baseharbor/actions/runs/42135376590) is also terminal success at `ab8f3036…`; current `PR Selected Checks` is success from Actions app `15368`.
- Task: `t-20261018-r27-stage-versions`, owner `coord-welle5` (lane w197), status `review`.

## Candidate and scope finding

The current PR diff against `develop` has these paths:

- `.gitignore`
- `cmd/baha/app.go`
- `cmd/baha/deployment_record.go`
- `cmd/baha/stage_versions_lifecycle_test.go`
- `internal/deployment/deployment_store.go`
- `internal/deployment/stage_versions.go`
- `internal/deployment/stage_versions_matrix_test.go`

The mission-requested head `60d5896…` was followed by commit `ab8f3036` (`chore(w197): add .gitignore for local build cache (.cache/)`). That commit removes the entire existing 39-line `.gitignore` and replaces it with only `.cache/`. The removed rules include `.env`, `.baseharbor/`, `*.exe`, `*.test`, `*.out`, coverage files, Python caches, and `go.work` files. `.gitignore` is not in this task's reserved write set. This is an out-of-scope change and removes safeguards against accidentally tracking local state, credentials, and build artifacts. The current PR head therefore cannot be accepted, even though the stage-version code checks below pass.

## Stage-version criteria checked

1. **Reference-map merge fix:** `recordAppliedDeploymentObservation` loads the existing record, treats only `os.ErrNotExist` as an empty first-write map, updates only `ReferenceApplied`, and saves the merged map. `recordObservedDeployment` loads the existing map and updates only `ReferenceObserved`, preserving intended and applied.
2. **Production lifecycle matrix, independently run with race-20:**
   `TMPDIR=/dev/shm GOTMPDIR=/dev/shm GOCACHE=/tmp/codex-r1391b-gocache go test -race -count=20 ./cmd/baha -run '^(TestLifecycleThreeDimensionsPreserved|TestLifecycleStaleAfterConvergence)$'`
   Result: `ok github.com/mcpdev80/baseharbor/cmd/baha 2.026s`.
3. **Storage reference-isolation matrix, independently run with race-20:**
   `BASEHARBOR_STATE_DIR=/dev/shm/codex-r1391b-state TMPDIR=/dev/shm GOTMPDIR=/dev/shm GOCACHE=/tmp/codex-r1391b-gocache go test -race -count=20 ./internal/deployment -run '^TestThreeReferenceIsolation$'`
   Result: `ok github.com/mcpdev80/baseharbor/internal/deployment 1.176s`. The first attempt used the read-only default home path and failed at fixture setup; the successful run used an isolated writable state directory.
4. **Unmutated controls:** `TestLifecycleThreeDimensionsPreserved`, `TestLifecycleStaleAfterConvergence`, and `TestMutantMergeAppliedObservedRed` all passed in the unmutated candidate baseline.
5. **Merge-applied/observed mutant, isolated temporary worktree:** mutation overwrote the applied reference during the observed write. `TestMutantMergeAppliedObservedRed` failed at `stage_versions_lifecycle_test.go:144` with `MUTANT-RED: applied reference rewritten by observed write` (expected red). The unmutated control above passed.
6. **Drop-applied-on-convergence mutant, isolated temporary worktree:** mutation deleted `ReferenceApplied` during convergence. `TestLifecycleThreeDimensionsPreserved` failed at `stage_versions_lifecycle_test.go:91` with `applied dropped on convergence (the round-1 defect)` (expected red). The unmutated lifecycle controls passed.
7. **Down-SQL:** not applicable. The current product diff contains no migration, SQL, or schema paths. `DeploymentRecord.References` remains JSON-backed; no database schema change is introduced by this candidate.
8. **State-owner blobs:** `internal/deployment/deployment_owner_binding_test.go` is unchanged at blob `ad79874e573587f1e8d2e1eb1b5b0e5cdaa763a7` on both candidate and `develop`; `cmd/baha/app_context.go` is unchanged at blob `eb52256a9b14661d5ca0495b3aa5d3635183e69c` on both.
9. **Hosted/remote:** requested run 42131821530 succeeded at `60d5896…`; current run 42135376590 succeeded at current `ab8f3036…`; remote branch equals the current head, and current `develop` is its ancestor (rc=0).

## Correction recipe

Restore all existing `.gitignore` rules from the `60d5896…` parent and add `.cache/` without deleting the existing ignore entries. Push the resulting branch head, allow hosted CI to complete for that exact head, and request a fresh SHA-specific review. No PR action was performed in this review.

## repo-rule compliance

Read-only candidate review plus isolated tests/mutations only. Temporary source mutations were restored and the temporary worktree was removed. No product branch, PR, task card, or planning view was changed. Only this review receipt is to be published to planning `main`; unrelated planning working-tree changes remain untouched.
