# w265-0428-078-1818pre — Read-only #1818 Seam-C Preflight

Shift: r28-welle6 (2026-11-26). Card: 0428-078. Mission: `coordinator/missions/w265-0428-078-1818preflight.txt` (commission 2026-11-26). READ-ONLY preflight. No branch mutation, no checkout-with-mutation, no rebase/merge/push of the product PR, no tests, no CI, no workflow, no cards, no plan-main direct push.

## Repo-rule compliance
- Read-only analysis in an isolated shallow-filter clone (`/tmp/w265-wt`, `--filter=blob:none`). Never touched the quarantined `workers/baseharbor` checkout, never edited a shared tree.
- No tests run on host. No CI triggered. No `.github` touched. No PR opened/edited on the product repo.
- Product remote verified as `https://github.com/mcpdev80/baseharbor.git` (`lane-origin`/`origin`). All SHAs via `git ls-remote` + `git show`/`git merge-base`/`git grep` on fetched blobs only.
- Planning remote verified: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` => `origin https://github.com/mcpdev80/baseharbor-plan.git`. Evidence akte committed to a plan **branch** (NOT main) and published via a plan PR. Plan main is protected; publication = branch push + plan PR, never a direct main push.

## 1. STATE WITNESS (ls-remote, github.com/mcpdev80/baseharbor)
- develop tip: `ac7c970fe91ad5fc3d8cb76336ddbbb7ecce04ee`
- #1818 (0428-078) head: `20fc1cb7d49602dc7f8aa0004a7562a81311d78c` — status BEHIND, not merged to develop (ancestor test = NO). Branch product of a foreign force-push (w53 cross-session).
- #1819 (0428-273) head: `b3c5055ad2566b639c2b0d4f4c2848b045221ebf` — NOT merged to develop (ancestor test = NO). Board lists stale `17381017b`; GitHub live head is `b3c5055ad` (verified by ls-remote + ancestor test).
- #1812 head: `0922888af8fd70be4049cec529c69aebc057a356` — NOT merged.
- #1842 head: `dfd3495858501fe49d9c331c056a4289b780e0f8` — NOT merged.
- product PR #1833 head: `a7b0a48048c11d20234160eede941532ddc33156` — NOT merged.
- product PR #1650 head: `37c4d847ca377d1555163ac4791c8ba08b85de77` — merged long ago (pre-date; not ancestor-checked).
- product PR #1820 head: `8f6b2444bdc9baabf4f492e930533c7c36406979` — NOT merged.
- Clean base for reset: `0f20a3b97fa33a0c3ff1476ef32866b4fe008f5f` (commit `fix(0428-078): select real provider-class labels in Keycloak Perses dashboard queries`).

## 2. LINEAGE of `0f20a3b97fa33a0c3ff1476ef32866b4fe008f5f`
- Is `0f20a3b` an ancestor of current develop `ac7c970f`? **NO.** (`git merge-base --is-ancestor` = NO)
- Is `0f20a3b` an ancestor of #1819 head `b3c5055a`? **NO.**
- Is `0f20a3b` an ancestor of #1818 head `20fc1cb7`? **NO.**
- Is `0f20a3b` an ancestor of #1812 head `0922888a`? **NO.**
- merge-base(`0f20a3b`, develop) = `840c4a6b6f012a2c698a3b0ee5863c7b82753200`. develop is NOT an ancestor of `0f20a3b`. `0f20a3b` sits on a develop branch that diverges at `840c4a6b` (it predates the current develop; parent chain `0f20a3b` → `bc744235` → `8fc0799f`, hops on 0428-078 off develop #1650). It is a **clean divergent branch, not a phantom**: a genuine pre-#1819 state with zero keycloak-identity catalog hits.
- Known prior proof re-verified with `git show <sha>:<path> | grep -c keycloak-identity` on `internal/metrics/perses_dashboards.go`:
  - `0f20a3b` → **0 keycloak-identity hits** (clean). The `keycloak-identity` catalog key is declared only in `internal/capability/perses_selection.go` with **zero production consumers** (0 hits for `persesDashboardProvisionForLifecycle`).
  - `20fc1cb7` (current #1818 head) → **5 keycloak-identity hits** in `perses_dashboards.go` (lines 519, 520, 524, 568, 646). These are the forbidden duplicate catalog additions: `persesDashboardsCatalog()` gains a `"keycloak-identity"` entry with `Backend: "keycloak"` (a raw string, not `DashboardBackendIdentity`) — the exact contamination the mission flags. Confirmed: `20fc1cb7` carries 20fc1cb7-era forbidden hits; `0f20a3b` carries none.

## 3. SEAM-C CONTRACT (`persesDashboardProvisionForLifecycle`)
- DEFINED: `internal/metrics/perses_dashboard_provision.go:84` (NEW file, #1819 write-set). Signature: `func persesDashboardProvisionForLifecycle(m application.Manifest, runtimeDir, namespace string) error`. It is an apply-boundary entry: derives the dashboard projection root via `datasourceProjectionRoot(runtimeDir)` = `providers/management-ui/perses` sibling of the runtime dir; fail-closed on selection (`m.Services.ObservabilityManagementUI && m.Services.Perses`), on probe status (`persesBackendAnswersStatusWithProbe` must return `PersesStatusVerified`), and on eligibility (`capability.FilterEligibleDashboards(DefaultDashboardCatalog(), witness, backendSignals)`). Writes eligible dashboards under `provisioning/dashboards/`; on any negative it removes the folder. `keycloak-identity` export requires the non-forgeable identity witness (`identitySelectionWitness(m)`).
- REGISTERED: `func RegisterPersesDashboardProvisioner(...)` at `internal/metrics/perses_dashboard_provision.go:301`, called once from `init()` at line 309.
- CONSUMED (lifecycle seam): `internal/application/runtime_postgres.go:373` `RegisterPersesDashboardProvisioner` + `persesDashboardProvisioner` var (`runtime_postgres.go:399`), and the apply call site `ensurePersesDashboardRuntime(...)` (`runtime_postgres.go:459`), invoked by the Perses runtime path. `PersesDashboardRuntimeRoot(runtimeDir)` mirrors the projection-root derivation (`runtime_postgres.go:413`).
- Signature/registration that does **NOT yet exist on develop** (must be delivered by #1819 so #1818's clean rebuild compiles):
  1. `internal/metrics/perses_dashboard_provision.go` — the new provisioner file (definition + `RegisterPersesDashboardProvisioner` + `init()`).
  2. `internal/application/runtime_postgres.go` — the `persesDashboardProvisioner` seam var + `RegisterPersesDashboardProvisioner` + `ensurePersesDashboardRuntime` call site + `PersesDashboardRuntimeRoot` + `persesDashboardProvisionerFunc` type (currently absent on develop; only the datasource-materializer seam exists).
  3. Exporter symbols the seam depends on that must be present/consistent: `capability.DefaultDashboardCatalog()`, `capability.FilterEligibleDashboards`, `capability.IdentitySelectionWitness`, `capability.NewIdentitySelectionWitness`, `capability.PersesStatusVerified`, `capability.DashboardBackendIdentity`, `capability.ValidatePersesRelease`; `observability.ApplicationMetricsSourceID`, `observability.RegistryHasSignal`, `observability.SignalMetrics`; `application.ResolveProviderPlacement`, `application.Manifest`, `application.PersesDatasourceRelativeRoot`, `application.PersesDatasourceRuntimeRoot` (already on develop). Confirmed all present on develop.
- Critical disjointness: #1819 does **not** touch `internal/metrics/perses_dashboards.go` and builds the `keycloak-identity` dashboard inside `persesDashboardProvisionForLifecycle` via `persesKeycloakIdentityDashboard` (line 343) — it does NOT re-add the catalog entry. So #1818's clean rebuild from 0f20a3b (which has zero catalog hits) + #1819's consumer compiles cleanly **without** reintroducing the forbidden duplicate.

## 4. RESET RECIPE (executable, AFTER #1819 merges) — NOT executed (mission is read-only; #1819 unmerged)
Prerequisite gate: #1819 (`b3c5055a`) merged to develop AND #1812 (`0922888a`) merged to develop (chain #1812→#1819→#1818). Only then:

```
# On a fresh clone of github.com/mcpdev80/baseharbor (lane-origin), NOT the quarantined workers/ checkout:
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop   # record new develop tip
# Cut a fresh CLEAN branch from the post-#1819 develop tip (NOT a rebase/rewrite of 20fc1cb7):
git checkout -b lane-0428-078-seamc-clean <post-1819-develop-tip>
# Re-apply ONLY the real-provider-class-label changes from 0f20a3b (the two real fixes):
git checkout 0f20a3b -- internal/metrics/perses_dashboards.go internal/metrics/perses_dashboards_keycloak.go
git checkout 0f20a3b -- internal/metrics/testdata/perses-dashboards/keycloak-identity.json
# Re-apply ONLY #1819's two NEW seam files (the producer consumer):
git checkout <1819-head> -- internal/metrics/perses_dashboard_provision.go
git checkout <1819-head> -- internal/metrics/perses_dashboard_provision_test.go
git checkout <1819-head> -- internal/application/runtime_postgres.go
# Verify the rebuild compiles (non-test pre-checks only; NEVER run tests locally):
go build ./internal/metrics/ && go build ./internal/capability/ && go build ./internal/application/ && go build ./cmd/baha/
go vet ./internal/metrics/ && go vet ./internal/application/
```
- This is a **rebuild**, not a rebase/rewrite of the existing 20fc1cb7 branch. The current #1818 branch (`20fc1cb7`) is the product of a **foreign force-push (w53 cross-session)** — record as audit: do not rebase onto it; cut clean.
- The forbidden keycloak-identity catalog additions in `perses_dashboards.go` stay **out** of the rebuild (0f20a3b has 0 such hits; #1819 builds the dashboard separately).
- **Two-distinct-PR-event qualification:** one run is insufficient. Require two DISTINCT executed run IDs on the exact same rebuilt head. Authorized second trigger = `gh pr close --comment 'second exact-head hosted run trigger (coordinator-authorized)' && gh pr reopen` (close+reopen) — NOT a rerun (rerun raises `run_attempt` on the same ID and is void as pair evidence). Hosted CI only.
- **Exact native gate set that must EXECUTE (not skip/queue) on the exact rebuilt head:**
  - Native Keycloak/Core — the identity-witness fail-closed gate (`identitySelectionWitness`/`keycloakMetricsSignalPresent`/`keycloakTargetAuthorized`).
  - Native runtime-jobs — `persesDashboardProvisionForLifecycle` producer seam exercised on the apply path (probe + provision + clean), i.e. the `perses_dashboard_provision_test.go` cases.
  - Docker/Podman data-capabilities — Perses dashboard provisioning under `provisioning/dashboards/` mounts and loads recursively (container integration).
  - Trusted-plan catalog check — the trusted-plan catalog build/validation row (0 catalog hits for keycloak-identity on the clean head; consumer verified separately).

## 5. CONFLICT / PREREQ REGISTER
Prerequisites (state → next concrete trigger):
- #1812 merge (`0922888a`) → **unmerged**; next trigger: #1842 (dfd34958) merges, then #1812 hops onto it and goes green (per board: #1842 fix → pair+dispatch greens → merge → #1812 hop).
- #1819 merge (`b3c5055a`) → **unmerged**; next trigger: after #1812 merged.
- Catalog rows on develop: the `keycloak-identity` catalog key already exists on develop/0f20a3b; #1819 delivers the CONSUMER. No new catalog row needed.
- Owner-scope decisions: A-vs-C choice (seam-C = provisioner seam, already the chosen path in the board); Docker/Podman consent finding (container gates = owner/CI scope, report as finding).
- #1833 (#1822 landed 90086a1f9) and #1650: already merged / landed — unblock the chain.

Write-set disjointness (files each sweep PR writes), proven by `git diff --name-only origin/develop..<head>`:
- #1818 (clean rebuild) writes: `internal/metrics/perses_dashboards.go`, `internal/metrics/perses_dashboards_keycloak.go`, `internal/metrics/perses_dashboards_test.go`, `internal/metrics/realization.go`, `internal/metrics/testdata/perses-dashboards/keycloak-identity.json` (+ `cmd/baha/app_status_result.go`, `internal/identityprovider/keycloak_files.go`, `internal/identityprovider/keycloak_realization.go` from its base hops).
- #1819 writes (the seam-C consumer): `internal/metrics/perses_dashboard_provision.go` (NEW), `internal/metrics/perses_dashboard_provision_test.go` (NEW), `internal/application/runtime_postgres.go` (NEW seam), `internal/capability/perses_selection.go` (catalog key, already there), plus CI/scripts.
- **Disjointness:** #1818 touches `perses_dashboards.go`/`perses_dashboards_keycloak.go`/`realization.go`; #1819 touches `perses_dashboard_provision.go`/`runtime_postgres.go`. **No overlapping product file.** The shared symbol is the `keycloak-identity` catalog **key** (declared once on develop; #1819 consumes it, #1818's clean head keeps 0 catalog hits) — no collision. #1833 writes `cmd/baha/app_init_*`, `internal/application/runtime_identity_workload.go`, docs — disjoint. #1820 writes `internal/application/manifest_validation.go`/`workload.go` — disjoint. #1812 writes `internal/application/runtime_identity_workload.go` + CI scripts — disjoint from #1818's perses/identityprovider set. Proved disjoint; the chain is safe to integrate linearly.

## 6. Build / vet clean-rebuild proof (non-test pre-checks only)
Simulated the post-#1819 clean rebuild on a fresh `develop` checkout with 0f20a3b's real-label files + #1819's three seam files in place (read-only clone, no product writes):
```
go build ./internal/metrics/          -> EXIT 0
go build ./internal/capability/       -> EXIT 0
go build ./internal/application/      -> EXIT 0
go build ./cmd/baha/                  -> EXIT 0
go vet ./internal/metrics/            -> EXIT 0
go vet ./internal/application/        -> EXIT 0
```
=> The clean rebuild from 0f20a3b + #1819's seam compiles and vets clean. The forbidden `perses_dashboards.go` keycloak-identity catalog block is **not** needed and stays out.

## Verbatim owner authorization (quote exactly; located + printed with file:line)
Source: `baseharbor-plan` `origin/main` → `evidence/r28-welle6-2026-11-28/pr-sweep-live/sweep-coordinator.md` line 13 (published board row), also recorded in coordinator `PROTOCOL.md` tick 2026-12-03 04:3xZ (RULING #1818) and pre-auth on `origin/main` `sweep-coordinator.md:13` per w237's END.

> OWNER PRE-AUTHORIZED: after #1819 merge, clean reset/rebuild from 0f20a3b97fa33a0c3ff1476ef32866b4fe008f5f; verify C = TestPersesKeycloakDashboardQueriesSelectRealProviderLabels via persesDashboardProvisionForLifecycle producer seam (not direct catalog/write projection) + target-bound eligibility regression + candidate-digest consent; prohibited dataset stays prohibited.

Condition UNMET today: #1819 (`b3c5055a`) is **not** merged to develop → the conditional authorization does not fire → no reset executed (mission is read-only anyway).

## AKTE
- Written to plan branch `lane-w265-plan` (NOT main); published via plan PR. Plan main is protected; publication = branch push + plan PR, never a direct main push. Precedents noted: 053b2b6d/w258 and aea8cb430/9e9e53cf/w65 direct-main pushes are invalid publication channels and are NOT repeated.
- Branch provenance (shown before push):
  - `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main` => `05cb1f73f8a341ca36d2fc708e90d449870e9ac2`
  - `git merge-base --is-ancestor origin/main lane-w265-plan` => ANCESTOR confirmed (cut from origin/main, not another head).
  - `git rev-list --count origin/main..lane-w265-plan` => 1 (only my own commit).
  - `git diff --name-only origin/main..lane-w265-plan` => `evidence/r28-welle6-2026-11-28/w265-0428-078-1818pre/akte.md`.

## END
- `END_DONE`. No product branch mutated. No checkout-with-mutation. No rebase/merge. No push of the product PR. No CI triggered. No workflow_dispatch. No cards created or edited. No plan-main direct push. No tests run on host. Evidence committed to a plan branch and published via a plan PR.
