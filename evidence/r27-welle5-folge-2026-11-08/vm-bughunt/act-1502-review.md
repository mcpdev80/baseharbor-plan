# CODEX-REVIEW 0427-172 — PR #1502

## PLAN

1. Verify the live PR head, base develop SHA, ancestry, changed paths, and commit list from GitHub.
2. Trace orphan marker adoption and both safety counterexamples at the exact candidate SHA.
3. Verify which tests the hosted CLI package job executes and inspect the terminal PR run, including native runtime results.
4. Check whether the required post-merge develop run exists and assess the exact tests and native job outcomes.
5. Record the verdict, actionable correction recipe, tests, and stop condition in this Planning evidence file.

## Verdict

**ROLE: REVIEW**
**VERDICT: KORREKTUR (REQUEST-CHANGES)**
**PR:** #1502
**Candidate head:** `7ea003b87d343b4685b306ac9c5db84520044f08`
**Base develop:** `20902f0a6ab016fd8fe6a501751e1becc5f334dd`

### 1. Orphan-marker adoption can mistake failed inventory for no Core

The new branch correctly tries to distinguish a dead-owner marker left before `up` from a real provisioned Core. In `cmd/baha/runtime_integration_test_support_test.go:344-354`, it consumes the marker when `orphanBootstrapTargetHadFootprint` returns `(false, nil)`; `adoptBootstrapLeftoverMarkerFromDeadProcess` removes that marker at `:283-285` only after the aggregate destroy path reports no error.

The footprint check does not reliably establish absence. `backgroundInventoryCtx` at `:375-378` defers `cancel()` before returning the context, so the context is already canceled when the caller uses it. Then `ownedFootprintOnEngine` at `:422-441` silently ignores errors from both `ListRuntimeContainers` (`:424-430`) and `ListOwnedProjectResources` (`:436-440`), and returns `(false, nil)` if inspection failed. In addition, `orphanBootstrapTargetHadFootprint` at `:406-413` treats every `ExistingFilesForProject` error as if project files were absent; it does not distinguish `os.ErrNotExist` from permission or I/O errors. A real Core resource can therefore become indistinguishable from the no-Core phantom case and its only retry marker can be consumed.

**Correction recipe:** In `cmd/baha/runtime_integration_test_support_test.go`, keep the inventory context alive through the complete inventory call (return a cancel function or create/cancel the context in the caller after inventory finishes). Treat only the documented not-found result for runtime files as absence. Return all other file and engine-inventory errors so adoption retains the marker and fails closed. A nil provider must also be an unverifiable error, not `(false, nil)`. Add injected regressions for runtime-file permission/I/O failure, `ListRuntimeContainers` failure, `ListOwnedProjectResources` failure, and nil provider; each must prove the marker remains and the adoption caller fails closed. The stop condition is that no unavailable inventory can produce the “no provisioned Core” result.

### 2. The requested counterexamples are CI-covered, with one distinction

The new `TestBootstrapAdoptionConsumesOrphanWithNoProvisionedCore` at `cmd/baha/runtime_integration_cleanup_coverage_test.go:1057-1095` uses a reaped child PID, persisted bootstrap target, and no runtime files/resources; it checks successful adoption and marker removal. The new `TestBootstrapAdoptionKeepsMarkerWhenCoreExists` at `:1100-1145` checks that a dead owner with a persisted Core footprint fails closed and keeps the marker.

The live-owner case is covered by `TestBootstrapAdoptionIgnoresLiveOwners` at `cmd/baha/runtime_integration_cleanup_coverage_test.go:682-710`. It exercises the adopter with the current PID and PID 2 and verifies the marker still exists. It is a pre-existing regression rather than a newly added test in this diff. It proves the sequential live-PID guard; it does not cover the canceled-inventory/failure case above.

All these tests are in the `cmd/baha` package. On exact candidate run `42528188447`, hosted job `PR · Validation · cli-package-tests` (job `128876402959`) passed. Its logged runner implementation is `go test ./cmd/baha -count=1 -json` (`scripts/pr-check-runner.py` at base `20902f0a6`, `go_package_tests` lines 116-119), which executes the full package and therefore selects these test functions. This establishes CI routing under the PR trigger, not a green native Docker/Podman acceptance run.

### 3. Hosted PR run is terminal failure; native tests do not establish the requested healing

Run `42528188447` is terminal `completed/failure` on the exact head. Both `PR · Native destroy retry · docker` (job `128876390162`) and `PR · Native destroy retry · podman` (job `128876390266`) failed in `TestSecondSameHostCoreNativeConflictInCI` at `second_target_conflict_native_test.go:31`. The exact log line in each job is:

`prepare BaseHarbor integration trust plane: bootstrap leftover marker missing (teardown not guaranteed): open /tmp/baseharbor-ci-data-<id>/baseharbor-bootstrap-cleanup-pending: no such file or directory`

The preceding `TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry` passed in each job. I record the requested runner-isolation classification as **STATE**, but the two checks remain failed and `PR Selected Checks` (job `128878564549`) is also terminal failure. They are not green evidence.

The PR-context `PR · Native Keycloak/Core · ${{ matrix.runtime }}` job (job `128876404232`) is `skipped`. Thus neither `TestUpNameResumesThroughCommandEntrypoint` (`cmd/baha/runtime_ports_test.go:316`) nor `TestControlPlaneSingleDefaultNativeRuntimeInCI` (`cmd/baha/control_plane_single_native_ci_test.go:18`) has a passing native result in this PR run. The latter requires `BASEHARBOR_SINGLE_DEFAULT_NATIVE_ACCEPTANCE=1` and a Docker or Podman runtime (`:19-24`).

The decisive post-merge develop proof is absent: live `gh pr view` reports PR #1502 `OPEN`, `mergedAt=null`; `git ls-remote` reports develop still at `20902f0a6ab016fd8fe6a501751e1becc5f334dd`. Latest develop Docker/Podman Core runs observed were `42516818029` and `42516818008`, both successful on that base SHA at 19:47Z, before this PR run at 22:02Z. They are not post-merge evidence for #1502.

**Correction recipe:** After the code correction and normal landing, verify a develop push run on the exact post-merge develop head. The Docker and Podman native jobs must actually execute and pass both `TestUpNameResumesThroughCommandEntrypoint` and `TestControlPlaneSingleDefaultNativeRuntimeInCI`; provide terminal job/run IDs and logs naming both tests. A skipped PR native job or pre-merge develop run does not satisfy this stop condition. Do not rerun or dispatch workflows from this review.

### 4. Scope and ancestry

The exact PR diff against develop changes only `cmd/baha/runtime_integration_cleanup_coverage_test.go` and `cmd/baha/runtime_integration_test_support_test.go`; no `.github/**` path is changed. `git merge-base --is-ancestor 20902f0a6ab016fd8fe6a501751e1becc5f334dd 7ea003b87d343b4685b306ac9c5db84520044f08` returned 0. The base-to-head log contains only `7ea003b8 test(cmd/baha): adopt dead-owner bootstrap marker with no provisioned Core cleanly`. `git diff --check` passed.

## repo-rule compliance

This was a read-only product review. No product file, workflow, branch, or PR state was changed, and no local or VM tests were run. The only write is this review evidence in the Planning repository.

## Stop criterion

Do not approve until inventory completion is required to classify a target as absent, all injected inventory failures retain the marker and fail closed, and the exact post-merge develop run completes with both required native tests passing on Docker and Podman. The present PR run is terminal failure; its runner-isolation STATE is recorded as requested and is not counted as green.

## END

END_DONE 0427-172-review — KORREKTUR required; candidate `7ea003b87d343b4685b306ac9c5db84520044f08`.
