# 0428-078 reset preparation desk (READ-ONLY PREP)

Card **0428-078** / PR **#1818** `lane-0428-078-cf-fix` / owner-authorized **#1819 reset**.
Shift `r28-welle6-2026-11-24`. Lane `w75-0428-078-resetprep`. Coordinator desk,
§3.3.5 hunt fill. **Befund/prep only — no push, no force-push, no product edits,
no merge, no subagent.**

Prepared 2026-11-24 by coordinator-side read-only verification against the live
remote via `git ls-remote`, `git fetch <sha>` + `git show`, and `gh pr view` /
`gh api`. All witnesses below are real-remote measurements, not memory.

## PLAN

- [ ] Reality witness: planning repo = `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`, origin = `https://github.com/mcpdev80/baseharbor-plan.git`; `workers/baseharbor-plan` is the quarantined bookkeeping checkout (NEVER commit there).
- [ ] Verify branch/PR #1818 clean vs contaminated head + voided runs.
- [ ] Compute exact `origin/develop..0f20a3b9` diff; consumer-file map; catalog-row question.
- [ ] C-retarget plan: `TestPersesKeycloakDashboardQueriesSelectRealProviderLabels` + `persesDashboardProvisionForLifecycle` seam + target-bound eligibility regression.
- [ ] Precondition checklist for the reset.
- [ ] Write + atomically commit + push the single evidence file to `origin/main`.

Reality witnesses (remote truth, via `git ls-remote` / `git fetch` / `gh`):

- Planning repo remote: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` -> `origin https://github.com/mcpdev80/baseharbor-plan.git` (fetch/push).
- `workers/baseharbor-plan` remote: `origin`/`lane-origin` -> `ssh://git@github.com/mcpdev80/baseharbor.git` (product repo, NOT planning; never commit here).
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` -> `2b9a2c6d1611ea85e11bf81e9650c28165c8293a`.
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-078-cf-fix` -> `20fc1cb7d49602dc7f8aa0004a7562a81311d78c` (the CONTAMINATED tip).
- PR #1818 via `gh pr view 1818`: state=OPEN, base=develop, head=`lane-0428-078-cf-fix`, headOid=`20fc1cb7...`, `mergeStateStatus=BEHIND`, isDraft=false, updatedAt=2026-11-24T03:01:19Z.

## 1. Branch / PR #1818 — CLEAN vs CONTAMINATED head + voided runs

Clean commit (the one the reset targets):
`0f20a3b97fa33a0c3ff1476ef32866b4fe008f5f`
`fix(0428-078): select real provider-class labels in Keycloak Perses dashboard queries`
Verified present on GitHub via `gh api repos/mcpdev80/baseharbor/commits/0f20a3b9...`.

**Item 1a — clean head has 0 keycloak-identity entries:**
`git show 0f20a3b9:internal/metrics/perses_dashboards.go | grep -c "keycloak-identity"` -> `0`
(grep found no match, exit 1). The provider-class query fix lives in the orphaned
`perses_dashboards_keycloak.go`; `perses_dashboards.go` at the clean head carries
no `keycloak-identity` catalog entry.

**Item 1b — contaminated tip 20fc1cb7 reintroduces the forbidden catalog entry (2 hits):**
`git show 20fc1cb7:internal/metrics/perses_dashboards.go | grep -n "keycloak-identity"`:
```
519:		"keycloak-identity": {
520:			Key:            "keycloak-identity",
524:			Dashboard:      persesDashboardForBackend(resolved, "keycloak-identity"),
568:	case "keycloak-identity":
646:			Metadata: PersesDashboardMetadata{Name: "keycloak-identity", Version: 0},
```
The two forbidden catalog-key hits (the re-introduced catalog entry that must be
removed by the reset) are:
- line 519: `"keycloak-identity": {` (map key)
- line 520: `Key: "keycloak-identity"` (catalog entry Key field)
Commit `20fc1cb7` message: `fix(0428-078): wire keycloak identity dashboard into
develop metrics catalog` (author w53-0428-152-alertfix, committer Codex) — a
force-push that re-added `persesDashboardCatalog()` + `backendForKey` +
`persesDashboardForBackend` for keycloak-identity, re-contaminating the branch.

**0f20a3b9 is NOT an ancestor of 20fc1cb7** (`git merge-base --is-ancestor
0f20a3b9 20fc1cb7` -> NO). The clean head was force-pushed away by w53.

**Voided runs (passed, but run against contaminated/foreign heads):**
- Run **45316544436**: `head_sha=20fc1cb7` (contaminated), branch `lane-0428-078-cf-fix`, status=completed, conclusion=success, workflow_id=352609139. VOID — contaminated head.
- Run **45313048505**: `head_sha=306a2b1ea55e9849ae0fa8fce52a9b7d7a037d75`, branch `lane-0428-078-cf-fix`, status=completed, conclusion=success, workflow_id=352609139. VOID — foreign head.
Both run against w53's contaminated commits, so their green conclusion is evidence of nothing for the clean candidate.

### File-evidence table (clean vs contaminated)

| Object | SHA | `perses_dashboards.go` keycloak-identity count | Catalog-key hits | Status |
| --- | --- | --- | --- | --- |
| Clean (reset target) | `0f20a3b97fa33a0c3ff1476ef32866b4fe008f5f` | **0** | none | reset target |
| Contaminated tip | `20fc1cb7d49602dc7f8aa0004a7562a81311d78c` | 5 total | 2 catalog-key (L519 map key, L520 Key field) | branch head now; voided CI |
| Foreign head | `306a2b1ea55e9849ae0fa8fce52a9b7d7a037d75` | (w53 contaminated) | (w53 contaminated) | voided CI |

## 2. Exact diff `origin/develop..0f20a3b9` + consumer-file map + catalog question

`git diff --name-only origin/develop 0f20a3b9` (develop head `2b9a2c6d1611ea85e11bf81e9650c28165c8293a`):
```
.github/workflows/pre-release.yml
cmd/baha/app_status_collect.go
cmd/baha/app_status_perses_alert_evaluator_0428_152_test.go
cmd/baha/app_status_result.go
cmd/baha/ci_integration_operator_enabled.go
cmd/baha/ci_integration_operator_enabled_test.go
cmd/baha/env_destroy_integration_test.go
cmd/baha/perses_lifecycle.go
internal/deployment/environment_destroy_scope.go
internal/deployment/environment_destroy_scope_test.go
internal/identityprovider/keycloak_files.go
internal/identityprovider/keycloak_realization.go
internal/metrics/perses_dashboards_keycloak.go
internal/metrics/perses_dashboards_test.go
internal/metrics/realization.go
internal/metrics/testdata/perses-dashboards/keycloak-identity.json
internal/operatorauth/authorization.go
internal/operatorauth/config.go
scripts/pr-gate-coverage.json
```
19 files, +944 / -1307. This is the full PR #1818 content against develop (a broad
card), not a single-file change.

**Catalog-row question (Item 2):** `0f20a3b9` does NOT add a new
observability-catalog catalog row beyond develop. The only catalog-level changes
are: regenerated `internal/metrics/testdata/perses-dashboards/keycloak-identity.json`
golden + `perses_dashboards_keycloak.go` (realizes the provider-class Keycloak
panel queries against `prometheus_files.go`'s production contract). The
`scripts/pr-gate-coverage.json` hunk is the reverse — it **removes** coverage rows
for `internal/application/runtime_postgres.go`,
`internal/metrics/perses_dashboard_provision.go`,
`internal/metrics/perses_dashboard_provision_test.go`,
`cmd/baha/app_broker_compat_test.go`, `internal/operatorauth/authorization.go`,
`internal/operatorauth/config.go` — files that belong to PR #1819, not #1818. So
#1818's clean diff carries no new observability-catalog row; the catalog surface
it touches is the `keycloak-identity` golden only.

**Consumer files in `cmd/baha/app_status_*` that reference the identity dashboard:**
- `cmd/baha/app_status_result.go` — adds field `IdentityDashboardEligible bool
  (json:"identity_dashboard_eligible,omitempty")` to `applicationStatusResult`;
  derives eligibility via `identityDashboardBackendEligible(persesStatus, manifest,
  targetStateRoot, targetName)`; exposes it on BOTH the local-return and the
  remote-target early-return through `withIdentityDashboardStatus(...)`. Verified in
  the diff (adds 30 lines around the `withIdentityDashboardStatus` +
  `identityDashboardBackendEligible` helpers). This is the single validated
  entrance to the flag on the status JSON.
- `cmd/baha/app_status_collect.go` — removes the old
  `collectPersesAlertEvaluatorObservation()` eager call inside
  `collectManagedServiceChecks()` (alert-evaluator surface, not the identity
  dashboard per se); identity-dashboard availability is now produced from the
  resolved status via the result.go seam.
- `cmd/baha/app_status_perses_alert_evaluator_0428_152_test.go` — 443 lines
  removed (alert-evaluator contract consolidation, part of the card's broader
  reorg).

## 3. C-retarget plan (exact file:line + correct call target)

**Test to retarget:**
`func TestPersesKeycloakDashboardQueriesSelectRealProviderLabels` at
`internal/metrics/perses_dashboards_test.go:766` (clean head).

Current test body (clean head) drives the **catalog** directly:
`catalog := persesDashboardCatalog()` then asserts the keycloak-identity entry's
queries key on `job="baseharbor-providers"` + `baseharbor_provider="keycloak"` and
reject `job="keycloak"`, `baseharbor_application=`, `baseharbor_environment=`.
This is a catalog-level unit test — it does NOT exercise the apply/lifecycle path
the reset must keep correct once #1819 moves realization out of the catalog.

**Correct call target — #1819 seam (verified in `gh pr diff 1819`):**
```
internal/metrics/perses_dashboard_provision.go:
+func persesDashboardProvisionForLifecycle(m application.Manifest, runtimeDir, namespace string) error {
```
This is the apply-boundary producer the lifecycle seam registers
(`RegisterPersesDashboardProvisioner(persesDashboardProvisionForLifecycle)`).
It is byte-stable across calls (comment in #1819). The retarget test must drive
`persesDashboardProvisionForLifecycle(m, runtimeDir, "")` — the runtime-dir root
is `datasourceProjectionRoot(runtimeDir)` = the `providers/management-ui/perses`
sibling of the `RuntimeFiles.Dir` — NOT `persesDashboardCatalog()` and NOT
`writePersesDashboardProjection()` and NOT the observability catalog. Quote: the
test drives the producer seam, decodes the emitted keycloak dashboard, and asserts
the same provider-class label contract as now.

**Target-bound eligibility regression (must be added in the retarget):**
Eligibility is the verified-only, non-forgeable path:
`IdentitySelectionWitnessAt(m, placement, targetStateRoot, targetName).NonForgeableAvailable()`
- `IdentitySelectionWitnessAt` signature (clean head `internal/metrics/realization.go:55`):
  `func IdentitySelectionWitnessAt(m application.Manifest, placement capability.ProviderPlacement, dataDir, namespace string) capability.IdentitySelectionWitness`
- `NonForgeableAvailable()` (clean head `internal/capability/perses_selection.go:109`):
  `return w.SelectionConfirmed && w.MetricPresent && w.MetricCurrent && w.TargetAuthorized`
- An **unqualified target** (no real manifest identity selection, or placement
  `Validate()` fails, or `Scope == external`, or no `MetricPresent`/`MetricCurrent`
  signal for that target) fails closed: `NonForgeableAvailable() == false` => the
  identity-dashboard status is NOT emitted (no dashboard for that Target).
- The retarget regression asserts: a manifest with a valid, authorized,
  keycloak-identity-bearing Target that carries a current real metric => eligible;
  the same manifest on an unqualified target (or `persesStatus != verified`) =>
  `IdentityDashboardEligible == false`.

**Note / scope flag:** `persesDashboardProvisionForLifecycle` does NOT exist at
`0f20a3b9` (verified: `git grep persesDashboardProvisionForLifecycle 0f20a3b9 --
*.go` -> empty; callers in `cmd/baha` -> empty). It is introduced by PR #1819. So
the C-retarget test cannot be compiled/verified against the clean #1818 head
alone — it requires #1819's seam. This is exactly why the precondition checklist
requires #1819 merged first. The seam signature/line above is quoted from #1819's
live diff (`gh pr diff 1819`), which is the authoritative source for the call
target.

## 4. Reset precondition checklist

The reset of PR #1818 / `lane-0428-078-cf-fix` back to clean `0f20a3b9` is
**precondition-gated**. None of the below is done by this desk. Order:

1. **[ ] #1819 merged to develop.** Verify `git ls-remote
   https://github.com/mcpdev80/baseharbor.git refs/heads/develop` advances past
   the merge and `persesDashboardProvisionForLifecycle` is live at the new develop
   head. (This is what makes the C-retarget test in item 3 compilable.)
2. **[ ] Branch reset to `0f20a3b9` by a #1818-owning lane.** A lane that owns
   #1818 performs the reset (not this read-only desk). Baseline attestation before
   the reset: `git ls-remote https://github.com/mcpdev80/baseharbor.git
   refs/heads/develop` = `2b9a2c6d1611ea85e11bf81e9650c28165c8293a` (the SHA the
   clean head was originally cut toward); confirm `0f20a3b9`'s merge-base with
   develop is an ancestor of that develop head.
3. **[ ] C-retarget applied + rebased onto then-develop.** Apply the test change
   from item 3 (drive `persesDashboardProvisionForLifecycle`, add the
   target-bound eligibility regression), then rebase onto the then-current
   develop. Show `git log --oneline origin/develop..HEAD` lists ONLY the lane's
   own commits; `git diff origin/develop...HEAD --name-only` captured in evidence.
4. **[ ] Fresh exact-hosted green CI.** One hosted CI run on the exact reset head
   (not the voided 45316544436 / 45313048505). Terminal exact-head "PR Selected
   Checks" aggregate must be green (SKIPPED/queued is not a pass).
5. **[ ] Consent `--confirm-candidate` with a RESOLVED candidate digest + owner
   authz.** The reset is an owner-authorized action (#1819 reset); the candidate
   digest must be RESOLVED and the reset run under owner authorization, not
   auto-triggered.

## repo-rule compliance

- Read-only desk: only `git ls-remote`, `git fetch <sha>`, `git show`, `gh pr
  view`, `gh api` against the live GitHub remote. No product edits, no force-push,
  no merge, no subagent.
- Working clone at `/tmp/bh-fetch-clean` (outside the ecosystem root, per the
  fixed-workspace-layout rule). Not committed to anywhere under
  `/home/marcel/dev/baseharbor-ecosystem`.
- Evidence authored into the planning repo only (`baseharbor-plan/evidence/...`),
  never into a product repo. No `.evidence/` directory.

## cleanliness

- No containers / compose projects / volumes started by this lane.
- No stray files under `/home/marcel/dev/baseharbor-ecosystem` (clone lives in
  `/tmp/bh-fetch-clean`).

## status

Read-only preparation desk complete. All four findings documented. The actual
reset runs later once #1819 merges; this desk does NOT touch PR #1818 or its
branch beyond reading. END lane DONE.

## handoff / END post

END w75-0428-078-resetprep: read-only prep done; findings in evidence; #1818 untouched.
