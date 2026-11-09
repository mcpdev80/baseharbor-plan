# CODEX-REVIEW 0427-165 r5 — PR #1500

## PLAN

1. Verify live PR head, exact hosted run, current develop SHA, and ancestry.
2. Trace the new heal-path regression through `removeApplicationState` and check its preconditions and postconditions.
3. Verify the test is selected by hosted CI and inspect native job outcomes and the related #1502 state.
4. Publish a SHA-specific code verdict with explicit landing checks and post END.

## Verdict

**ROLLE: REVIEW — APPROVE the r5 code delta.** The new regression reaches the production app-destroy cleanup method `removeApplicationState` directly, without starting a runtime; it proves the owner-restored record and directory are removed while the Target definition and Core runtime owner remain. It then seeds a new orphan and verifies the refusal still names it and does not advertise the unsupported `--from-recovery` path. The test runs in the exact-head hosted `go-unit-tests` job.

This is a code review approval, not a landing clearance. The two Native Keycloak/Core jobs failed with the same existing-Core same-engine conflict recorded as external STATE 0427-172; #1502 remains open and unmerged. `PR Selected Checks` is consequently failed, not green. Also, current develop `b3a8042d1` is not an ancestor of this head. Treat both as landing checks, as requested: integrate the resolved 0427-172/current develop state, then require a new exact-head run with the native jobs and selected aggregate successful before landing.

### Candidate and ancestry

- PR #1500 is open at exact head `64d621f40e85402b92805d64b65647ca8dc304f1`. The r5 diff from r4 head `0bc028f13272a064c47db1e99d4fbb4da7e74fc3` is one commit touching only `cmd/baha/target_definition_orphan_refusal_test.go`.
- GitHub currently reports PR base `20902f0a6ab016fd8fe6a501751e1becc5f334dd`; live `git ls-remote origin develop` is `b3a8042d18ea60f162a32a51df34a499cad6a237`.
- The r4 head is an ancestor of r5. Current develop `b3a8042d1` is not an ancestor of r5 (merge-base ancestry check exit 1). Per this review assignment, this is a landing/base-refresh check, not a code finding.

### Heal-path regression

`cmd/baha/target_definition_orphan_refusal_test.go:365-465` extends `TestTargetDeleteHealPathReachesRecordWithOwnerRestored`:

- `configureTestTarget` restores the authoritative Core owner; `registerTestDeployment` creates a genuine ownerless orphan record with a matching deployment-directory identity and an available source fixture.
- The test constructs the lifecycle execution and directly calls `e.removeApplicationState()` at line 413. It does not call the runtime-start path and does not start a container or engine.
- `cmd/baha/app_destroy_lifecycle.go:570-599` is the production method exercised: it removes application state, validates that state is gone, releases the application registry entry, and then calls `deployment.DeleteDeploymentRecord`.
- The test asserts the record is absent from `ListDeployments`, the deployment directory is gone, the Target definition still exists, and the Core runtime-owner directory remains (`:417-443`). These match the r4 correction recipe's removal and preservation assertions.
- It then seeds a fresh collectable orphan and calls `buildTargetDefinitionChangePlan`; the refusal must fire, name the new record, and omit `--from-recovery` (`:445-464`). This checks that healing one record did not erase the refusal behavior for a subsequent orphan.

The direct method invocation intentionally isolates the cleanup/removal segment from external runtime effects while exercising the production method that removes the record. No further code correction is requested for this r5 delta.

### Hosted CI and native STATE

Run `42555826490` is terminal `completed/failure` on exact head `64d621f40e85402b92805d64b65647ca8dc304f1` (`pull_request`). The relevant checks were:

- `PR · Validation · go-unit-tests`, job `128961228606`: success. The job runs `scripts/pr-unit-database.sh`, which executes `go test ./... -count=1`; the new `cmd/baha` regression is covered.
- `PR · Validation · deployment-package-tests`, job `128961228650`: success.
- Build, vet, formatting, focused Python, and native destroy-retry Docker/Podman jobs: success.
- `PR · Native Keycloak/Core · docker`, job `128961228741`, and `· podman`, job `128961228590`: failure in `TestControlPlaneSingleDefaultNativeRuntimeInCI`. Both logs report `control_plane_single_native_ci_test.go:38`: Core is already running on the same engine for the `w169-ci-bootstrap-…` target; a second same-host Target cannot silently share it.
- `PR Selected Checks`, job `128964431731`: terminal failure because `pr_owner_node_native` failed. This aggregate is not green.

The native failure is external STATE 0427-172, not caused by this test-only r5 commit. The exact failure class matches the r4 run, and live PR #1502 remains open/unmerged (`merged=false`). No workflow rerun/dispatch or `.github/**` change was made. The native cells failed here; they were not skipped and must not be counted as passes.

### Landing checks

- Keep the 0427-172 native conflict recorded as external STATE while #1502 remains unresolved.
- Refresh the PR onto the current develop tip after the related landing and verify current develop is an ancestor of the resulting candidate.
- Require a new terminal run on that resulting exact head with both Native Keycloak/Core jobs and `PR Selected Checks` successful. Do not merge based on the current run's passing unit/validation jobs alone.

## END

END_DONE 0427-165-r5-review: APPROVE code delta for PR #1500 head `64d621f40e85402b92805d64b65647ca8dc304f1`; real `removeApplicationState` regression and preservation/refusal assertions pass review and are CI-covered. Landing remains gated by external 0427-172 native STATE, failed current `PR Selected Checks`, and refresh onto current develop `b3a8042d1`.
