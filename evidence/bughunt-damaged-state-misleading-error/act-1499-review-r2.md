# CODEX-REVIEW 0427-159 r2 — PR #1499

## PLAN

1. Refresh PR #1499, develop, candidate, and hosted run state from GitHub.
2. Compare the exact candidate source with the task acceptance and prior act-1499 correction recipe.
3. Trace the production damaged-state command path, directory identity checks, foreign-orphan handling, recovery output, and regression coverage.
4. Inspect exact-head job results and logs, distinguishing the 0427-172 bootstrap marker failure from the 0427-159 CLI regression.
5. Record verdict and actionable correction recipe in this Planning evidence, validate, publish to origin/main, and post END.

## Urteil

**ROLLE: REVIEW — KORREKTUR; approval withheld.** The candidate adds a network state and recovery text, but the production scan can attribute an arbitrary orphan to the app currently being resolved, the damaged-directory scanner does not validate the folder name or establish owner identity, and the app-scoped network scan is sequenced after a resolver path that can return the damaged-state error first. The new tests do not close those gaps. The exact-head hosted run is also terminal failure because the external native 0427-172 test fails; that is classified as STATE, not as a 0427-159 product regression, but it leaves the required selected result red.

## Exact candidate and remote state

- Repository: `mcpdev80/baseharbor`; PR #1499 is open, head `b68092b22ffe6585f631ddea796867ec28161f34`, current API base `20902f0a6ab016fd8fe6a501751e1becc5f334dd`.
- The candidate commit's parent is `3187cea15728143146905c7238ad6e280ca11b3e`, matching the lane's stated historical base. Current develop `20902f0a6ab016fd8fe6a501751e1becc5f334dd` is not an ancestor of the candidate (`git merge-base --is-ancestor` returned 1); GitHub reports `mergeable=true`, `mergeable_state=unstable`. The only commit in `develop..head` is the named r2 commit. After code corrections, integrate current develop and obtain checks on the resulting exact head.
- `git ls-remote` reports `20902f0a6ab016fd8fe6a501751e1becc5f334dd refs/heads/develop` and `b68092b22ffe6585f631ddea796867ec28161f34` for both the candidate branch and `refs/pull/1499/head`.
- The requested `evidence/bughunt-damaged-state-misleading-error/round-2.md` was absent from fetched Planning `origin/main` (`5fb42689e5f2bebab5503916a5fd8b93363b18e1`). The available `round-3.md` still describes prior head `452be76cec7122f27b3468850d780e232960d2f2`, not this candidate. I reviewed the live source and hosted run directly; the absent round-2 dossier remains an evidence gap.
- The candidate source diff is the single r2 commit, 13 files, under `cmd/baha/`, `internal/application/`, `internal/deployment/`, and `internal/runtime/`; no workflow edits were made by this review.

## Findings against the acceptance and prior recipe

### F1 — The code names the missing network, but the production error path can return before the network inspection

The message construction in `internal/deployment/damaged_state.go:45-62` includes `deployment.json`, the path and application identity it was given, and—when state is absent—the network name. `NextAction()` at lines 68-73 includes both source re-up and destroy/recreate. The intended network name is derived in `workloadNetworkNameForIdentity` at lines 20-30; `internal/application/network.go:31-36` confirms the corresponding canonical development workload network prefix.

However, `cmd/baha/app_context.go:199-211` calls `deployment.FindDeployment` and immediately returns any error. `FindDeployment` uses `ListDeployments` (`internal/deployment/deployment_store.go:622-667`), whose `listDeploymentRecords` branch returns a `DamagedDeploymentError` as soon as `DamagedDirectoryState` matches (`internal/deployment/deployment_list.go:71-94`). The new app-scoped `damagedScanRuntimeForTarget` / `DamagedDeploymentNamespaceScoped` call is later in `app_context.go:245-268`, so this earlier error path does not reach the network inspector. The candidate therefore has not established from source that the actual `up` path reports both halves for the exact damaged-directory condition.

`TestUpFailsClosedNamingRecordAndNetworkAbsent` calls the real `newApplicationUpExecution` path, but the assertion only searches for the generic substring `network` (`cmd/baha/app_lifecycle_damaged_state_test.go:226-238, 312-326`) rather than the exact derived name or the explicit absent-state wording. This passing CI test report does not reconcile the early-return source path with the test's claimed network assertion. Demonstrate the executed call path and exact message before claiming F1 is closed.

### F2 — Damaged directory identity is not checked against its directory name

`internal/deployment/damaged_state.go:156-178` scans every directory entry and accepts its artifacts as a damaged deployment without calling `ValidateDeploymentID` or verifying a deployment identity. The helper tests themselves use names such as `damaged-net`, `damaged-present`, and `damaged-nil` (`internal/deployment/damaged_namespace_network_test.go:34-45, 73-84, 113-122`), so the regression fixtures do not prove canonical UUID directory handling.

More importantly, `internal/deployment/deployment_list.go:71-89` calls `DamagedDirectoryState` before the existing owner/path and record validation path. The regular `loadDeploymentRecordFile` verifies record identity against its storage path at `internal/deployment/deployment_store.go:540-580`, but the new damaged-state short circuit bypasses that check. A malformed or mismatched record path can therefore enter the damage classification without the identity check required by the prior recipe and the 0427-165 lesson.

### F3 — A foreign orphan can be returned as damage for the selected app

`DamagedDeploymentNamespace` returns the first damaged directory in the target namespace without establishing which app owns it (`internal/deployment/damaged_state.go:144-180`). `DamagedDeploymentNamespaceScoped` then inspects the network derived from the currently selected manifest (`lines 210-239`). `cmd/baha/app_context.go:256-268` constructs the returned `DamagedDeploymentError.Identity` from that selected manifest regardless of which directory `damagedDir` named. Thus a foreign app's orphan can be reported as the selected app's damaged record; if the selected app's own network is absent, the message can attribute both facts to the selected app even though the returned orphan path belongs to another app.

`TestDamagedDeploymentNamespaceScopedNoFalseAttributionToForeignApp` does not prove the CLI contract: it expects the foreign orphan to be flagged, supplies a `Present` inspector, and only checks that the helper's returned state is not `Absent` (`internal/deployment/damaged_namespace_network_test.go:134-176`). The helper does not return an owner identity, and the test does not inspect a production command error. This is contrary to the acceptance's requirement that a foreign orphan never be attributed to this app.

### F4 — CI runs the added tests, but missing identity and fallback cases are not proven

The exact-head run's `PR · Validation · go-unit-tests` job (`128882101499`) ran `scripts/pr-unit-database.sh`, whose command is `go test ./... -count=1`; `PR · Validation · deployment-package-tests` (`128882101450`) also passed. These include the new `cmd/baha` and `internal/deployment` test packages on the PR event. The pure network-state tests therefore have CI execution coverage.

That coverage does not prove the missing cases: no fixture checks a canonical UUID directory plus a stored UUID/path mismatch; the foreign-orphan CLI test does not assert no false attribution; and the nil-inspector test exercises `DamagedDeploymentNamespaceScoped` directly rather than the `app_context.go` runtime-factory-error fallback. Add regressions at those production seams. Keep them in the existing `go-unit-tests` / `deployment-package-tests` coverage; do not edit `.github/**` from this review.

### F5 — Exact-head run is terminal failure; the native failure is the 0427-172 marker test, not another CLI entrypoint regression

Run [42530058011](https://github.com/mcpdev80/baseharbor/actions/runs/42530058011) has `head_sha=b68092b22ffe6585f631ddea796867ec28161f34`, `status=completed`, `conclusion=failure`.

- `PR · Native Keycloak/Core · docker`, job `128882101537`, and `PR · Native Keycloak/Core · podman`, job `128882101469`, both fail only at `TestControlPlaneSingleDefaultNativeRuntimeInCI` (`control_plane_single_native_ci_test.go:31`) with `bootstrap leftover marker missing (teardown not guaranteed)`. Both logs show `TestKeycloakSingleNativeSQLInCI` passed before that failure. The failing native test is the reported 0427-172 bootstrap-marker case; the logs do not show a failure in the 0427-159 damaged-state entrypoint tests.
- `PR Selected Checks`, job `128884532599`, is failed. Its result artifact identifies `pr_owner_node_native` as `failure`; therefore the exact-head run and required selected checks are red. Other applicable non-native checks and both native destroy-retry jobs passed. Skipped checks are not passes.

Classify the native marker failure as external **STATE / 0427-172**, as requested. It is not a 0427-159 source finding, but it still blocks acceptance until the owner-scoped 172 issue is resolved or explicitly waived and the selected result is green on the final exact head. No workflow rerun or modification was made.

## Correction recipe

- In `internal/deployment/damaged_state.go:144-180` and `internal/deployment/deployment_list.go:67-94`, validate canonical deployment-directory IDs before classifying damage, and do not infer application ownership from an arbitrary orphan path. Preserve the verified storage-path identity checks from `deployment_store.go:540-580` rather than bypassing them for damaged entries.
- In `cmd/baha/app_context.go:199-211,232-268`, route a verified damaged record through the network inspection before returning, while keeping unknown-owner or foreign orphans unattributed. Only add the selected app's network name/state when a trusted identity binds that damaged directory to the selected app. If owner identity cannot be recovered, return an explicit unknown-owner damaged-path conflict and do not claim that the selected app's network is absent.
- In `cmd/baha/app_lifecycle_damaged_state_test.go` and `internal/deployment/damaged_namespace_network_test.go`, add production-path regressions for: canonical UUID plus correct identity; mismatched/malformed directory identity; foreign orphan while the selected app's network is absent; runtime factory error/nil fallback; and a valid-record repository that exceeds the generic inspection limit while an unrelated orphan exists. Assert the exact network name, missing record, owner attribution (or explicitly unknown owner), and both concrete recovery paths.
- Run the tests through existing `go-unit-tests` (`go test ./... -count=1`) and `deployment-package-tests`, each on the corrected exact candidate. The final acceptance also requires current-develop ancestry and a terminal green `PR Selected Checks`; the 0427-172 native marker failure must first have its owner-scoped resolution/waiver. No skipped job substitutes for an executed required gate.

**Stop criterion:** a real `baha app up` resolution reports the missing record and the exact absent workload network only when ownership is verified; foreign/malformed orphans are never attributed to another app; the generic limit remains for a valid over-limit repository; CI proves those regressions; and the final exact-head selected result is green after the external 172 state is cleared or waived.

## Evidence and repository rules

- Prior review recipe: `evidence/bughunt-damaged-state-misleading-error/act-1499-review.md`.
- Available candidate dossier: `evidence/bughunt-damaged-state-misleading-error/round-3.md` (documents earlier head `452be76...`); the requested `round-2.md` was not present on Planning origin/main at review time.
- Exact hosted run: `https://github.com/mcpdev80/baseharbor/actions/runs/42530058011`.
- Planning repository remote: `origin https://github.com/mcpdev80/baseharbor-plan.git`.
- Planning `origin/main` before this review publication: `5fb42689e5f2bebab5503916a5fd8b93363b18e1`.
- Product candidate and hosted CI were inspected read-only; no product files, workflows, PR state, VMs, or containers were changed by this review.

END 0427-159 r2 REVIEW — KORREKTUR for `b68092b22ffe6585f631ddea796867ec28161f34`; hosted 0427-172 marker failure recorded as external STATE.

## Planning validation

`git diff --check` passed for this evidence, and `python3 scripts/plan.py check` passed with 434 tasks, 7 epics, 13 releases, 16 decisions, zero errors, and four pre-existing dependency warnings. This act contains no Markdown checkbox lines.
