# CODEX-REVIEW 0427-128 r5 — PR #1452

## PLAN

1. Verify the exact PR head, develop head, r4 ancestry, file delta, and hosted run.
2. Recheck the four r4 stop points: renderer panic safety, production identity checks, cross-project pinned coverage, and selected-stop postcondition plus hosted execution.
3. Record the verdict and actionable correction recipe in the planning evidence.
4. Render and validate the planning repository, publish to origin/main, and verify the remote evidence path and candidate SHA.

## Verdict

**ROLLE: REVIEW**  
**URTEIL: KORREKTUR (REQUEST-CHANGES)**  
**PR #1452 head:** `01f6325d660aa4723a9106d84dbca49faf6e392f`  
**Develop base:** `07ae6c3e91b081a189266ca4b162ba705d4aa78f`  
**R4 head:** `48814ecc5e8603f16f4849249fffc9b0c8abd7ab`  
**Hosted run:** `42461735463`, terminal success on the exact r5 head.

### 1. R4 renderer panic: corrected

The r5 delta adds `plannedNamesForService` and `nilCheckedRenderer` in `internal/runtime/service_retirement.go`. It avoids calling an absent or nil-promoted renderer, catches a renderer panic as an unavailable model, and retains the canonical-only fallback. `TestRetireOwnedServicesStaysPanicFreeWithoutCallableRender` covers an embedded nil provider, a provider without render capability, and a panicking renderer. `internal/runtime/container_identity.go` also rejects a nil provider explicitly.

The r4 hosted `go-unit-tests` panic root cause is addressed in the candidate. In run `42461735463`, `PR · Validation · go-unit-tests` completed successfully. This resolves r4 finding 1.

### 2. Production identity paths: improved, with a remaining control-plane regression gap

The production retirement path still derives rendered names and filters runtime inventory by project and service. The new `TestRetireOwnedServicesRejectsForeignPinnedReplica` invokes `RetireOwnedServices` with both an owned pinned container and a foreign-project row carrying the exact same name/service. It asserts that the foreign row is not selected or mutated; a foreign-only inventory does not satisfy retirement of the owned container. This closes the retirement-side production-path gap from r4.

The r5 write set changes `cmd/baha/control_plane_stop_observation.go` to make its optional renderer nil/panic-safe, but adds no regression that calls `observeControlPlaneStopRuntime` with the exact same pinned name under a foreign project. The r4 recipe explicitly required a production Control-Plane-Observation test as well as the retirement test. The existing runtime matcher test is not a substitute for exercising that production observer.

**Correction recipe:** add a focused test alongside the control-plane stop-observation tests (or the existing `cmd/baha` test file that owns this seam). Invoke `observeControlPlaneStopRuntime` with an owned planned pinned container and a foreign-project row sharing the native name and service; prove the foreign row is not accepted as an owned replica or included in the selected/mutated set. Include the foreign-only case and preserve the valid owned pinned case. The exact test must run in the existing `go-unit-tests` package discovery.

### 3. Cross-project pinned production regression: retirement covered; observer coverage incomplete

The new retirement regression is a meaningful production-call test rather than only a direct matcher check. Its foreign-only case confirms that the foreign row cannot hide the still-running owned resource. However, the paired control-plane-observation production regression required by r4 remains absent, so the overall cross-project acceptance point is only partially satisfied.

**Stop condition for this point:** both production paths must have a regression that supplies the same pinned native name in a foreign project and proves the foreign row cannot satisfy, alter, or enter the owner’s planned set.

### 4. Selected-stop postcondition and hosted execution: source regression remains, required native run is still missing

The final candidate retains `StopOwnedProjectServices` postcondition checks: observations are bounded by the rendered planned names plus canonical name, and an unexpected or still-running selected process fails verification. `TestSelectedStopAcceptsPinnedContainerName` and `TestSelectedStopRejectsUnplannedPinnedReplica` remain present in `internal/runtime/service_stop_test.go`. No r5 change regresses that code or those unit regressions.

The native pinned lifecycle test `TestRepositoryComposePinnedWorkloadLifecycleInCI` is still absent from the runtime integration selector in `.github/workflows/ci.yml:349`. On this exact hosted PR run, the native runtime job was skipped; the passing Go unit and `PR Selected Checks` jobs do not prove that native Docker/Podman lifecycle path. The round-5 evidence also records the selector gap. Workflow ownership belongs to the Owner, so this review makes no workflow edit and triggers no rerun.

**Correction recipe:** the Owner must add `TestRepositoryComposePinnedWorkloadLifecycleInCI` to the existing runtime-integration selector in `.github/workflows/ci.yml:349`, preserving its `BASEHARBOR_CI_RUNTIME_INTEGRATION=1` gate. Then an ordinary hosted PR run must execute that test and report success on the exact candidate head. The new control-plane test above must also be selected by `go-unit-tests` and pass on that same head.

## SHA, scope, and CI witnesses

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1452/head` returned `07ae6c3e91b081a189266ca4b162ba705d4aa78f` for develop and `01f6325d660aa4723a9106d84dbca49faf6e392f` for PR #1452.
- `git merge-base --is-ancestor 48814ecc5e8603f16f4849249fffc9b0c8abd7ab 01f6325d660aa4723a9106d84dbca49faf6e392f` exited 0. The develop base ancestry check also exited 0.
- The r4-to-r5 product delta is limited to `cmd/baha/control_plane_stop_observation.go`, `internal/runtime/container_identity.go`, `internal/runtime/service_retirement.go`, `internal/runtime/service_retirement_render_safety_test.go`, and `internal/runtime/service_retirement_test.go`. No workflow file changed.
- `gh run view 42461735463 --repo mcpdev80/baseharbor`: `headSha=01f6325d660aa4723a9106d84dbca49faf6e392f`, `status=completed`, `conclusion=success`. `PR · Validation · go-unit-tests`, `PR · Source format`, and `PR Selected Checks` succeeded. The native runtime job was skipped; the required pinned lifecycle test did not run.
- No product file was modified, no local test was run, no workflow was changed, and no rerun/dispatch or container operation was performed.

## Stop criterion

Do not approve until the control-plane observation production-path cross-project regression is present and selected `TestRepositoryComposePinnedWorkloadLifecycleInCI` actually executes and passes on a hosted run for the exact candidate head. The passing r5 unit run resolves the r4 panic finding but does not waive these remaining requirements. No approval based only on a skipped native job.

## END

END_BLOCKED 0427-128-r5-review — KORREKTUR; PR #1452 head `01f6325d660aa4723a9106d84dbca49faf6e392f`, hosted run `42461735463` terminal success; control-plane cross-project regression and hosted pinned lifecycle execution remain open.
