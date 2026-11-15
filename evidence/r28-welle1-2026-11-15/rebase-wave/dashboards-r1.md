# Rebase Wave 1, R28 — Dashboards (PR #1597)

Mission: `mission-rebase-1597.md` (fan-rebase-welle schritt 2 — NO feature scope).
Date: 2026-11-15. Agent: ornith lane worker.

## Task summary
Merge the NEW selection-head into the shared branch `perses-dashboard-databases-lane`
(PR #1597 head). No feature changes, only a content merge. Both sides preserved;
minimal conflict-free merge; normal merge-commit push.

## Number list (steps)
- Verified remote heads via git ls-remote (both branches).
- Created dedicated worktree under /tmp/opencode for perses-dashboard-databases-lane; fetched both branches.
- Established base attestation: 2e5f8703 is the base SHA and an ancestor of the branch head.
- Recorded before-state (log/oneline for both heads).
- Dry-run merge confirmed clean; only selection-side files touched.
- Performed merge of selection-head into perses-dashboard-databases-lane (no rebase, no force-push); no conflicts; both sides preserved.
- Ran go build ./... (PASS), go test ./internal/metrics/... -run Perses (10 PASS), go test ./internal/capability/... -run Perses (7 PASS), go vet clean, gofmt clean.
- Readability audit: files >800 lines listed; none in merge-touched files.
- Pushed normal merge-commit to perses-dashboard-databases-lane; PR #1597 stays draft=open; verified pushed head.
- Wrote this evidence dossier in baseharbor-plan.

## Remote witnesses (git ls-remote, before merge)
- `git ls-remote https://github.com/mcpdev80/baseharbor.git perses-dashboard-databases-lane`
  => `2e5f870374ece50f5594def6c73e2f4747090a45  refs/heads/perses-dashboard-databases-lane`
- `git ls-remote https://github.com/mcpdev80/baseharbor.git lane-0428-080-r28-perses-selection`
  => `a270725bdd795a5c944caf96fd1161ec44688a55  refs/heads/lane-0428-080-r28-perses-selection`

## Base attestation
- Base SHA cut from: `2e5f870374ece50f5594def6c73e2f4747090a45` (perses-dashboard-databases-lane head).
- `git merge-base --is-ancestor 2e5f87037 HEAD` => YES (base is ancestor of branch head).
- Merge-base of the two heads: `85b4cbb598272e28944e48b6895ce8935031c9ba`.
- 2e5f87037 has one commit above merge-base; selection-head has four commits above merge-base.

## Before / after
- Before (perses head): `2e5f870374ece50f5594def6c73e2f4747090a45`.
- Selection-head merged in: `a270725bdd795a5c944caf96fd1161ec44688a55`.
- After (new merge head): `7f3a25a0b454adec9fba3beb5b0e3d0e2ba6b89f`.
- Merge commit parents (both verified as ancestors via `git merge-base --is-ancestor`):
  - parent 1: `2e5f870374ece50f5594def6c73e2f4747090a45` (perses base)
  - parent 2: `a270725bdd795a5c944caf96fd1161ec44688a55` (selection-head)

## Merge protocol
- Strategy: `ort`. `git merge --no-ff --no-edit` of selection-head. No rebase, no force-push.
- No conflict markers; automatic merge went well.
- Files changed by the merge (selection side only, perses side unchanged in conflict):
  - `docs/de/spec/management-access-v1.md` (modified)
  - `internal/application/manifest_parse.go` (modified)
  - `internal/application/manifest_parse_services.go` (new)
  - `internal/capability/perses.go` (modified)
  - `internal/capability/perses_test.go` (modified)
  - `internal/metrics/perses_contract_test.go` (modified)

## Verification outputs (verbatim)
- `go build ./...` => BUILD EXIT: 0 (PASS)
- `go vet ./internal/metrics/... ./internal/capability/... ./internal/application/...` => VET EXIT: 0
- `gofmt -l` on touched files => empty (all formatted)
- `go test ./internal/metrics/... -run Perses`:
  - TestPersesReleaseIsPinnedAndCurrent: PASS
  - TestPersesManagementSurfaceFailClosedWhenUnprovisioned: PASS
  - TestPersesReleaseVersionIsRealizationMetadataNotProviderVersion: PASS
  - TestPersesIsNotAnApplicationCapability: PASS
  - TestPersesDashboardCatalogHasRealBackendsOnly: PASS
  - TestPersesRealDashboardPersesNativeJSON: PASS
  - TestPersesDashboardJSONIsDeterministic: PASS
  - TestPersesUnavailableEntryMarshalsReason: PASS
  - TestPersesDashboardKeysMatchSelectionCatalogKeys: PASS
  - TestPersesDashboardGoldenFiles: PASS
  - `ok github.com/mcpdev80/baseharbor/internal/metrics 0.005s`
- `go test ./internal/capability/... -run Perses`:
  - TestDashboardNotEligibleWithoutPersesSelection: PASS
  - TestValidatePersesReleaseFailClosedWithoutPin: PASS
  - TestValidatePersesReleaseRejectsUnknownAuthClass: PASS
  - TestPersesDefaultReleaseValidates: PASS
  - TestPersesIsManagementSurfaceNotApplicationCapability: PASS
  - TestPersesManagementIsAValidIntegrationDescriptor: PASS
  - TestPersesManagementNotRegisteredAsCapabilityProvider: PASS
  - `ok github.com/mcpdev80/baseharbor/internal/capability 0.002s`

## Readability audit
- Files >800 lines in the repo (pre-existing, NOT touched by this merge):
  - internal/runtimeexecutor/client_test.go (2007)
  - internal/openbao/bootstrap_test.go (1727)
  - cmd/baha/runtime_integration_cleanup_coverage_test.go (1386)
  - cmd/baha/runtime_integration_test_support_test.go (1327)
  - cmd/baha/app_edit_apply_test.go (1265)
  - contracts/managementaccess/v1/store.go (1029)
  - cmd/baha/app_new_wizard_test.go (914)
  - cmd/baha/application_artifact_resolution_test.go (912)
  - cmd/baha/app_lifecycle_damaged_state_test.go (883)
  - cmd/baha/app_prune_test.go (883)
  - cmd/baha/onboarding_test.go (868)
  - cmd/baha/app_maintenance_client_test.go (868)
  - cmd/baha/app_apply_result_test.go (849)
  - cmd/baha/node_read_test.go (807)
- None of the merge-touched files exceed 800 lines. No new readability gate breach introduced.

## Push + PR state
- Pushed merge-commit to perses-dashboard-databases-lane (normal push, no force): `2e5f87037..7f3a25a0b`.
- Verified pushed head: `git ls-remote ... perses-dashboard-databases-lane` => `7f3a25a0b454adec9fba3beb5b0e3d0e2ba6b89f`.
- PR #1597 via API: draft=True, state=open, merged=false, base=lane-0428-080-r28-perses-selection.

## Scope compliance
- No merge to develop. No .github/** touched. No ready_for_review. No force-push. No subagent (§4.8). No feature changes — content merge only. PR stays draft.

## origin/main witness (before END)
```
9a47fafc evidence(r28-welle1-2026-11-15): rebase wave step2 dashboards merge PR #1597 (7f3a25a0b)
43705fc7 evidence(0428-080 perses r28): rebase-wave step1 merge a270725b, PRs #1590/#1597 lose manifest_parse inheritance
76a32ad8 plan(coord): fund->karte — bf01 orphan-test removal (zeuge live-verify r4 d3651819)
```

## END
- lane: perses-dashboard-databases-lane (PR #1597)
- result: DONE
- new head SHA: 7f3a25a0b454adec9fba3beb5b0e3d0e2ba6b89f
