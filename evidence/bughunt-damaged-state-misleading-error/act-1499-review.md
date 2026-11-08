# CODEX-REVIEW 0427-159 — PR #1499

## PLAN

1. Resolve the exact live PR head and compare it with PR #1498 and the current develop base.
2. Review the damaged-state path, recovery guidance, and the relevant command tree at the candidate and develop refs.
3. Verify the four regressions are in the CI-selected packages and inspect terminal hosted results on the exact candidate SHA.
4. Record the verdict and actionable corrections in this Planning evidence file.
5. Validate and publish this file to baseharbor-plan origin/main, then post END.

## Verdict

**KORREKTUR — approval withheld.** The early damaged-state detection and the listed recovery commands are present, but the candidate does not fully represent the reported BF-03 condition (both the record and runtime network were removed), and the exact-head hosted required result is red. The native failures are recorded as external STATE per the 0427-172 attribution supplied for this review; they are not assigned as a 0427-159 implementation defect.

## Exact candidate and ancestry

- Repository: `mcpdev80/baseharbor`
- PR: #1499, open, base `develop`, live base SHA `20902f0a6ab016fd8fe6a501751e1becc5f334dd`
- Exact head: `452be76cec7122f27b3468850d780e232960d2f2`, branch `0427-159-damagedstate`
- The PR is mergeable according to GitHub, but its commit parent is `3187cea15728143146905c7238ad6e280ca11b3e`; current develop is ahead of that base.
- Closed predecessor PR #1498 head `934775f6ad4a46cd2a229d6308c216801661fc12` is **not an ancestor** of #1499 (merge-base ancestor test returns false). Both candidate commits share parent `3187cea15728143146905c7238ad6e280ca11b3e`; the range-diff shows a replacement/amendment, not a descendant chain. This is recorded as lineage fact; #1498 is closed and contributes no separate candidate to accept.
- The #1499 product diff contains only `cmd/baha/app_context.go`, `cmd/baha/app_lifecycle_damaged_state_test.go`, `internal/deployment/damaged_namespace_test.go`, `internal/deployment/damaged_state.go`, and `internal/deployment/deployment_list.go`; no workflow or unrelated paths.

## Findings

### F1 — BF-03 reproduction's missing network is not represented or checked

At candidate `internal/deployment/damaged_state.go:27-38`, the diagnostic correctly states that `deployment.json` is missing and protected deploy-directory state remains. `DamagedDirectoryState` at lines 80-107 checks filesystem artifacts only. It does not inspect or report the runtime network. The documented BF-03 reproducer in `evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hx2.md:63-69` deletes both `deployment.json` and `baseharbor-dev-workload-w0427-owner-missing-hx3app-dev`, then encounters the inspection-limit error. The new CLI regression at `cmd/baha/app_lifecycle_damaged_state_test.go:131-200` removes only `deployment.json` and retains `application.env`; it does not reproduce the absent network or assert that the diagnostic names that part of the observed damage. The package tests in `internal/deployment/damaged_namespace_test.go:13-95` likewise cover orphaned state and empty/never-delivered controls, not the absent network.

The implementation does establish that damaged state is checked before the generic repository inspection path: `cmd/baha/app_context.go:219-240` calls `DamagedDeploymentNamespace` before returning a resolved repository application. Its damaged predicate requires a retained deploy directory plus missing `deployment.json` and protected artifacts. Healthy records and empty/incomplete directories do not match that predicate, so the normal path still proceeds to the existing repository inspection budget. However, the new tests do not include a paired genuine over-limit control case.

There is also an identity ambiguity in this scan: `DamagedDeploymentNamespace` at `internal/deployment/damaged_state.go:120-155` returns the first damaged directory anywhere under the target namespace, while `app_context.go:231-239` labels it with the currently selected repository manifest's identity. If an unrelated app's orphaned directory is found, the diagnostic can name the wrong app. The error should report the actual identity only when it can be proved; otherwise it should say the orphan's identity is unknown and identify the retained path.

**Required change:** in `internal/deployment/damaged_state.go` and the production-resolution seam in `cmd/baha/app_context.go`, make the error accurately describe the specific damage that can be established. For BF-03, either include a verified missing-network condition in the damaged-state payload/message, or make the message explicit that the network state is unverified while naming the missing record and retained state. Do not claim the network is absent without observing it. Do not attribute an unidentifiable orphan to the current repository app. Extend `cmd/baha/app_lifecycle_damaged_state_test.go` with the exact record-plus-network-missing fixture and assert the user-facing diagnostic/recovery; add a second-app orphan fixture to prevent false attribution. Add a valid-record repository fixture that genuinely exceeds the inspection budget and assert the existing generic limit remains the result. **Stop criterion:** the exact BF-03 condition is reported without misattribution, the recovery is actionable, and the undamaged over-limit control still returns the existing limit error.

### F2 — Recovery commands exist; no correction required for command spelling

The emitted recovery text at `internal/deployment/damaged_state.go:34-36, 48` names `baha destroy --yes` then `baha app up`. Those commands are present on current develop: root `baha up` is registered in `cmd/baha/commands.go:76-80`; root `baha destroy` in `commands.go:94-102`; and `baha app up [NAME]` is appended by `configuredApplicationCommand` at `commands.go:252-273`, implemented by `cmd/baha/app_up.go:39-56`. Thus the action names are valid; `baha app up` is not a phantom command. The source-repository re-up option is valid through the registered root `baha up` command, though the error text could make that invocation explicit.

### F3 — Four regressions are covered by hosted Go package checks

- `cmd/baha`: `TestDetectDamagedDeploymentState` and `TestUpFailsClosedOnDamagedDeploymentState` in `cmd/baha/app_lifecycle_damaged_state_test.go`.
- `internal/deployment`: `TestDamagedDeploymentNamespaceDetectsOrphanedState` and `TestDamagedDeploymentNamespaceIgnoresEmptyAndNeverDelivered` in `internal/deployment/damaged_namespace_test.go`.
- On exact head `452be76...`, run `42518412175` executed `PR · Validation · go-unit-tests` (log reports `ok github.com/mcpdev80/baseharbor/cmd/baha`) and `PR · Validation · deployment-package-tests` (the deployment package check matched `./internal/deployment`; log reports `ok github.com/mcpdev80/baseharbor/internal/deployment`). These checks ran on the PR event. The tests are in the discovered Go packages and are not skip-gated. Other targeted checks must not be inferred from these package results.

### F4 — Exact-head hosted run is terminal but not green

Run `42518412175` on exact head `452be76cec7122f27b3468850d780e232960d2f2` is `completed / failure`. Non-native required checks including source format, trusted plan, focused Python, go-vet, go-build, go-unit-tests, deployment-package-tests, cli-gofmt, and native destroy-retry Docker/Podman succeeded. Some other jobs were skipped and are not passes.

Both `PR · Native Keycloak/Core · podman` (job `128846435593`) and `PR · Native Keycloak/Core · docker` (job `128846435771`) failed. Both executed `TestKeycloakSingleNativeSQLInCI` successfully, then failed immediately in `TestControlPlaneSingleDefaultNativeRuntimeInCI`:

- Podman log: `control_plane_single_native_ci_test.go:31: prepare BaseHarbor integration trust plane: bootstrap leftover marker missing (teardown not guaranteed): open /tmp/baseharbor-ci-data-4139119002/baseharbor-bootstrap-cleanup-pending: no such file or directory`
- Docker log: `control_plane_single_native_ci_test.go:31: prepare BaseHarbor integration trust plane: bootstrap leftover marker missing (teardown not guaranteed): open /tmp/baseharbor-ci-data-891421899/baseharbor-bootstrap-cleanup-pending: no such file or directory`
- `PR Selected Checks` also failed because selected required results were not all successful.

Per the supplied ownership attribution, these two native failures are **STATE: 0427-172 successor / external native-gate failure**, not a 0427-159 code failure. They still make the exact-head hosted result red; no skipped check is counted as green and no local/package report replaces that red result. Do not rerun or edit workflow files from this review. Acceptance requires the owner-scoped 0427-172 explanation/resolution (or explicit waiver) and a terminal green required selected result on the exact accepted head.

## repo-rule compliance

- Read-only review of product candidate `452be76...`; product refs and worktree were not modified.
- Evidence is written only to the Planning repository.
- No workflow edits, reruns, VM tests, merges, tags, or releases were performed.
- #1498 ancestry was checked against the fetched PR head; it is not an ancestor of #1499.
- Planning pre-push remote witness: `1402376c0f327dae4676fdfed06a34849c21de30	refs/heads/main`

## END

END 0427-159-review: KORREKTUR — functional coverage gap for the observed record-plus-network damage; exact-head required hosted result remains blocked by external native STATE in run 42518412175.
