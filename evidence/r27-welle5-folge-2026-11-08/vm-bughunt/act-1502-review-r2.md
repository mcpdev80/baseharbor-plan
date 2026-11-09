# CODEX-REVIEW 0427-172 r2 — PR #1502

## PLAN

1. Verify the live PR head, develop SHA, ancestry, changed paths, and commit list from GitHub.
2. Trace the inventory context and fail-closed adoption behavior at the exact candidate SHA.
3. Inspect the inventory-failure regressions and confirm their hosted CI selection.
4. Inspect the terminal exact-head PR run and determine whether the native failures are explained by candidate code.
5. Verify the required post-merge develop run and record whether both named tests actually executed.
6. Publish a SHA-specific verdict, correction recipe, and stop criterion in Planning.

## Verdict

**ROLE: REVIEW**  
**VERDICT: KORREKTUR (REQUEST-CHANGES)**  
**PR:** [#1502](https://github.com/mcpdev80/baseharbor/pull/1502)  
**Candidate head:** `e69de123d8f469ea65aa6c29b2a6110814ca8b79`  
**Base develop:** `20902f0a6ab016fd8fe6a501751e1becc5f334dd`  
**Live PR state:** open, mergeable, `mergeStateStatus=UNSTABLE`; current PR run `42536968217` is terminal failure.

### 1. The inventory-context and fail-closed changes work, but the native test setup loses its marker

The requested r1 inventory repair is present at the exact head. `backgroundInventoryCtx()` returns a live bounded context and cancel function at `cmd/baha/runtime_integration_test_support_test.go:389-391`; `destroyOrphanedBootstrapMarkers()` cancels it only after `orphanBootstrapTargetHadFootprint()` returns at `:352-355`. In that helper, only `errors.Is(filesErr, os.ErrNotExist)` establishes absent runtime files (`:421-435`); other runtime-file errors propagate. A nil provider and target-root resolution error also fail closed (`:406-416`). Both engine listing operations propagate errors (`:444-473`).

There is a separate candidate regression behind the reported native red. `runRuntimeIntegrationTestMain()` claims the marker under the initial data root before `m.Run()` at `cmd/baha/runtime_integration_test_support_test.go:99-114`. But `ensureRuntimeIntegrationTrustPlane()` unconditionally creates a new data home and sets `XDG_DATA_HOME` to it at `:538-549`, then calls `ensureBootstrapLeftoverMarker()` at `:575-579`. That check reads the marker path under the new root (`:701-713`), where TestMain did not claim it. Both native jobs fail at `second_target_conflict_native_test.go:31`, before exercising the second-target conflict:

- Docker job `128903364099`, run `42536968217`: `prepare BaseHarbor integration trust plane: bootstrap leftover marker missing (teardown not guaranteed): open /tmp/baseharbor-ci-data-1520143170/baseharbor-bootstrap-cleanup-pending: no such file or directory`
- Podman job `128903364076`, same run: `prepare BaseHarbor integration trust plane: bootstrap leftover marker missing (teardown not guaranteed): open /tmp/baseharbor-ci-data-1138833673/baseharbor-bootstrap-cleanup-pending: no such file or directory`

This evidence does not support classifying these failures as runner-isolation STATE: the candidate's root switch disconnects the marker from the owner that claimed it. `PR Selected Checks` job `128905621982` records `NATIVE_SELECTION: success`, `NATIVE_REQUIRED: true`, `NATIVE_RESULT: failure`, then exits 1. These are failing gates, not skipped or green checks.

**Correction recipe:** In `cmd/baha/runtime_integration_test_support_test.go`, make `ensureRuntimeIntegrationTrustPlane()` use the same data root that `TestMain` claimed; do not unconditionally replace `XDG_DATA_HOME` after marker creation. Preserve per-run isolation within that owned root, or if a new root is essential, create and claim its marker before any operation that relies on it and retain/clean the original claim consistently. Add/retain a native regression that executes `TestSecondSameHostCoreNativeConflictInCI` past `ensureRuntimeIntegrationTrustPlane()` on both runtimes. Stop when the Docker and Podman jobs no longer fail at the marker check and the exact-head selected checks are terminal pass.

### 2. Adoption failure tests are CI-selected; the permission-error regression does not inject that error

`TestBootstrapAdoptionFailsClosedOnEngineInventoryError` and `TestBootstrapAdoptionFailsClosedOnResourceInventoryError` are present in `cmd/baha/runtime_integration_cleanup_coverage_test.go:1152-1195` and `:1201-1244`. They assert a non-nil adoption error and retained marker when container or project-resource inventory fails. The exact-head `PR · Validation · cli-package-tests` job `128903369257` succeeded and reports `matched_tests: ["./cmd/baha"]`; this package-wide selection covers these regression functions on the `pull_request` trigger. The overall run remains failure because of the native jobs above.

The claimed runtime-file permission regression at `runtime_integration_cleanup_coverage_test.go:1252-1294` does not create an inaccessible runtime path or inject an `ExistingFilesForProject` error. It creates only `dir/baseharbor/config.yaml` (`:1271-1276`), leaves the target runtime directory absent, and injects an engine inventory error (`:1278-1286`). Since absence yields `os.ErrNotExist`, the test proceeds into the injected engine error and would still pass if a non-ENOENT runtime-file error were incorrectly treated as absence. There is also no regression that reaches `orphanBootstrapTargetHadFootprint(..., nil, ...)`, despite the nil-provider guard.

**Correction recipe:** In `cmd/baha/runtime_integration_cleanup_coverage_test.go` and its test seam in `runtime_integration_test_support_test.go`, add deterministic injection for `ExistingFilesForProject` returning a permission/I/O error and a nil provider. Assert adoption fails, the marker remains, and engine inventory is not used to convert the file error into absence. Keep these in `cmd/baha`; the existing package-wide `cli-package-tests` group covers them on `pull_request`. Stop when each injected error fails closed independently of the other inventory methods.

### 3. The required develop healing proof is absent

The card requires a hosted full-matrix develop run with no pending PR-side changes, and this review's stop criterion requires both `TestUpNameResumesThroughCommandEntrypoint` and `TestControlPlaneSingleDefaultNativeRuntimeInCI` actually run and pass in native Docker and Podman jobs. PR run `42536968217` is a `pull_request` event: `PR · Native Keycloak/Core · ${{ matrix.runtime }}` (job `128903370298`) is skipped, so it cannot satisfy the healing proof. The latest observed develop-push runs are `42516818029` (Docker Core) and `42516818008` (Podman Core), both on the pre-candidate SHA `20902f0a6ab016fd8fe6a501751e1becc5f334dd`; their `Native single-default` jobs are skipped. The PR remains open, so there is no post-merge develop head/run. No skipped result counts as execution.

**Correction recipe:** After the marker-root regression is fixed and the candidate lands through normal gates, verify a develop-push run on the exact post-merge develop SHA. Both named tests must be shown as executed and passing in native Docker and Podman jobs; provide the terminal run/job IDs and test log evidence. Do not dispatch or rerun workflows from this review. Stop without approval if either test is skipped, absent, or failing.

### 4. Scope and provenance

Live `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1502/head` returned develop `20902f0a6ab016fd8fe6a501751e1becc5f334dd` and PR head `e69de123d8f469ea65aa6c29b2a6110814ca8b79`. `git merge-base --is-ancestor 20902f0a6ab016fd8fe6a501751e1becc5f334dd e69de123d8f469ea65aa6c29b2a6110814ca8b79` returned 0. The base-to-head log contains only `7ea003b8 test(cmd/baha): adopt dead-owner bootstrap marker with no provisioned Core cleanly` and `e69de123 fix(cmd/baha): fail-closed orphan inventory on engine errors (0427-172 r2)`. The changed paths are exactly `cmd/baha/runtime_integration_test_support_test.go` and `cmd/baha/runtime_integration_cleanup_coverage_test.go`; no `.github/**` files changed.

Planning repository witness: `git -C baseharbor-plan remote -v` reports `origin https://github.com/mcpdev80/baseharbor-plan.git` for fetch and push. Planning `origin/main` was `11df4f62d4e90d42beb283da66b3c1af90f8f3e3` before this evidence commit. The product checkout was a fresh clone under `/tmp/opencode/0427-172-review-wt`; no quarantined worker checkout was used. No product files, branches, PR state, or workflows were changed; no tests or containers were run locally.

## repo-rule compliance

This was a read-only product review. Review evidence is stored only in the Planning repository. No local test, Docker, Podman, workflow dispatch, rerun, release, or product mutation was performed.

## Stop criterion

Do not approve until the native marker is resolved to the TestMain-owned data root, the file-error and nil-provider regressions independently prove fail-closed adoption, the exact-head PR required checks are terminal pass, and the required post-merge develop-push run executes and passes both named tests on Docker and Podman. The current PR run is terminal failure; its native destroy-retry failures are not accepted as runner-isolation STATE because the exact logs reproduce the candidate's marker-root mismatch.

## END

END_DONE 0427-172-review-r2 — KORREKTUR required; candidate `e69de123d8f469ea65aa6c29b2a6110814ca8b79`; exact-head run `42536968217` FAILURE; develop healing proof absent.
