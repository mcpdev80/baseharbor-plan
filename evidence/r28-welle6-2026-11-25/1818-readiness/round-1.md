# PR #1818 Readiness + Reset Audit (round 1)

Lane: `w106-0428-078-readiness` (worker: ornith). Mission `w106-pr1818-readiness.txt`.
READ-ONLY inventory + reset audit. No rebase, no CI, no merge, no PR edit. No VM run. No subagents (§4.8). Nothing in baseharbor changed.

## PLAN

- Remote witnesses: git ls-remote origin lane-0428-078-cf-fix, ls-remote develop, gh pr view 1818.
- Diff 8e2c50c1 vs develop; enumerate touched files; conflict flags vs chain.
- Verify 3 keycloak rows removed at 8e2c50c1 vs 5 at 20fc1cb7; 0428-057 consumer scope preserved.
- State gated next action (reset to 8e2c50c1, rebase onto develop, Hosted exact-head gates); do NOT execute.
- Write evidence, commit + push atomically with targeted git add; pull --rebase origin main first.

## BASE ATTESTATION

Planning repo remote (verified before first evidence commit):
`git -C baseharbor-plan remote -v` ->
`origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)`
`origin  https://github.com/mcpdev80/baseharbor-plan.git (push)`

Real baseharbor GitHub remote (first git action, resolved to github.com/mcpdev80):
`https://github.com/mcpdev80/baseharbor.git`
(The shared checkout also carries `lane-origin` / `upstream` to the same URL; `origin` on the baseharbor checkout is github.com here, not a local path. All witnesses below use the github.com URL directly.)

Exact base SHA cut from (remote):
`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` -> `f14fb87c8f5afd91168e4f174d620c9f00e6341e refs/heads/develop`
develop = **f14fb87c8f5afd91168e4f174d620c9f00e6341e** (matches the mission's expected ~f14fb87c8).
Branch head (remote):
`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-078-cf-fix` -> `20fc1cb7d49602dc7f8aa0004a7562a81311d78c refs/heads/lane-0428-078-cf-fix`

## 1. REMOTE WITNESSES (PR #1818)

State: OPEN, NOT Draft. base = `develop`, headRefName = `lane-0428-078-cf-fix`, headRefOid = `20fc1cb7`, mergeStateStatus = BEHIND, reviewDecision = (none), changedFiles = 8.
Title: "fix(0428-078): consume real Perses probe for identity dashboard eligibility".

Latest CI run on head `20fc1cb7` (CI · Source & Quality, run 45316544436, 2026-11-24T03:01–03:27Z):
- Required-ish that EXECUTED: `Workflow policy` SUCCESS, `PR · Native gate plan` SUCCESS, `PR · Source format` SUCCESS, `PR · Trusted Plan` SUCCESS, `PR · Runner Interface` SUCCESS, `PR · Demo Pin` SUCCESS, `PR · Exact Candidate` SUCCESS, `PR · Focused Python` SUCCESS, `PR · Go unit · cli-0/1/2/3` SUCCESS, `PR · Go unit · packages` SUCCESS, `PR · Go unit · owner` SUCCESS, `PR · Validation · go-build` SUCCESS, `PR · Validation · go-vet` SUCCESS, `PR · Validation · identity-provider-package-tests` SUCCESS, docker/podman Selected Runtime (identity/observability/data-capabilities) all SUCCESS, aggregate `PR Selected Checks` SUCCESS (2026-11-24T03:25:13Z).
- SKIPPED: `Release Source Preflight`, both Targeted HA gates, `PR · Draft source and routing`, `PR · Draft Go`, `PR · Native` gates, `PR · Consumer Pins`, `PR · Public Contracts`, `PR · Selected Core-less`, `PR · Native Keycloak/Core`.

Note: the EXECUTED required checks here ran against the CURRENT head `20fc1cb7` (the contaminated foreign-candidate head), NOT against the reset target. The pass is real for that SHA; it is NOT evidence that the reset target `8e2c50c1` is gate-clean. Per mission, do NOT re-dispatch.

## 2. 8e2c50c1 EXISTS + ANCESTOR PROOF

`git cat-file -t 8e2c50c1` -> `commit` (real object, full peel):
`8e2c50c10a537c00e30d62a47f29638a0f14d5ff`, parent `888e2193b3f20d1e2af01a86bbb725cd65d370b2`, author `w21-pr1702-0428-246-footprint <246-footprint@baseharbor.local>` 1795478760 +0100.

`git merge-base --is-ancestor 8e2c50c1 20fc1cb7` -> PASS. **8e2c50c1 IS an ancestor of the current head 20fc1cb7.** Reset target exists and is reachable.

git diff 8e2c50c1 vs develop (identity-dashboard/catalog-consumer surface):
`git diff --stat origin/develop...8e2c50c1` is not the right framing here: 8e2c50c1's lineage base is old develop (merge-base with current develop = `3ebfb90da` = #1815, pre #1816/#1817/#1823 hops). So `git diff 8e2c50c1 origin/develop` shows files develop changed AFTER 8e2c50c1's base (e.g. cmd/baha/secret_audit_test.go, cmd/baha/secret_operations.go) — those are normal base divergence, NOT rebase conflicts, because 8e2c50c1's OWN changes are confined to metrics-catalog files.

Touched files AT 8e2c50c1 (the commit's own diff vs its parent 888e2193b):
- `internal/metrics/perses_dashboards_keycloak.go` (new, +70) — provider-class panel queries + PersesDatasourceKeycloak const
- `internal/metrics/perses_dashboards_test.go` (+101) — provider-label assertion + `TestPersesKeycloakDashboardQueriesSelectRealProviderLabels`
- `internal/metrics/testdata/perses-dashboards/keycloak-identity.json` (new, +133) — golden dashboard

These are exactly the metrics/catalog-consumer surface for 0428-078's Keycloak identity dashboard. The 0428-057 consumer files named in the mission (`internal/dashboard/identity_catalog.go`, `internal/dashboard/identity_view.go`, `internal/server.go`, `internal/application/app_catalog.go`, `cmd/baha/catalog.go`, `internal/application/app_dashboard.go`) **DO NOT EXIST** at either 8e2c50c1 or 20fc1cb7 (verified via `git cat-file -e`). The real consumer surface is `internal/capability/perses_selection.go` (single `keycloak-identity` row) + the metrics catalog + the panel JSON. The mission's 0428-057 file list is inaccurate.

## 3. RESET DIFF 20fc1cb7 -> 8e2c50c1 (what is dropped)

`git diff 8e2c50c1 20fc1cb7 --name-only` -> exactly 2 files:
- `internal/metrics/perses_dashboards.go` (drops the stray `keycloak-identity` catalog entry: `Key/Backend=Keycloak/Datasource/DatasourceName/Dashboard` block at line 519, the `backendForKey case "keycloak-identity" -> ProviderKeycloak` at line 568, and the `persesDashboardForBackend case ProviderKeycloak` block at line 640)
- `internal/metrics/testdata/perses-dashboards/keycloak-identity.json` (drops `"duration": "5m"`, restores description + height=12)

CRITICAL CORRECTION to the mission's premise ("head carries 5 keycloak-identity rows, 3 must be dropped"):
- The `keycloak-identity` catalog entry exists in EXACTLY ONE place: `internal/capability/perses_selection.go:220`. Count = 1 at BOTH 8e2c50c1 AND 20fc1cb7 (identical). There is NO 5-row/3-row situation there.
- The head 20fc1cb7 added ONE extra `keycloak-identity` entry in the OTHER catalog, `internal/metrics/perses_dashboards.go:519` (the metrics-package catalog). That is the only real "contamination" added on top of 8e2c50c1.
- The panel queries are byte-identical at 8e2c50c1 and 20fc1cb7 — both key on provider-class `job="baseharbor-providers", baseharbor_provider="keycloak"` with NO application/environment selectors. The queries were already correct at 8e2c50c1; 20fc1cb7 did not touch query bytes, only the catalog wiring + cosmetic JSON (description/height/duration).
- The "3 keycloak-identity rows" wording in the mission does not map to the actual repo. w88's "3 must be dropped" / 0f20a3b9-phantom are not reflected in the current branch; no 0f20a3b9 exists in history. The correct, minimal reset is exactly the 2-file drop above (remove the stray `perses_dashboards.go` entry), which restores the byte-identical state that develop already has in `perses_selection.go`.

## 4. CONFLICT / REBASE FLAGS vs the chain

- #1819 (keycloak EXPORT) / #1820 (broker): neither is merged to develop yet; develop HEAD f14fb87c8 does not carry a keycloak export surface. No overlap with the reset (metrics catalog).
- #1823 secret_* (`fix(0428-277): fail-closed AuthorizationResult`): develop's #1823 touched `cmd/baha/secret_audit_test.go`, `cmd/baha/secret_operations.go`, `internal/authorize/*`. The reset target's own changes touch NONE of those files (metrics catalog only). So the "reverse secret_* content" w96 warned about does not touch 0428-078's surface. The reset-to-8e2c50c1, rebased onto post-#1823 develop, is expected clean of the reverse secret_* conflict because the write-sets are disjoint (perses_dashboards.go / perses_dashboards_keycloak.go / perses_selection.go vs cmd/baha/secret_* and internal/authorize/*).
- Chain base for #1818 is develop (per PR), not another lane head. The branch is NOT under current develop (merge-base = 3ebfb90da = old develop), consistent with BEHIND — this is exactly why the reset+rebase is the next action, not a fast-forward.

## 5. GATED NEXT ACTION (do NOT execute)

After #1819 merges + owner decision C:
1. Reset `lane-0428-078-cf-fix` to `8e2c50c10a537c00e30d62a47f29638a0f14d5ff` (drop the stray 20fc1cb7 foreign commit + the stray `perses_dashboards.go` catalog entry).
2. Rebase onto the then-current `origin/develop` (post #1819). Expect clean because the write-sets are disjoint from #1819/#1820/#1823.
3. Hosted exact-head CI (PR Selected Checks) on the rebased SHA. Keep PR Draft until implementation AND gate are complete; move to review at handoff only.
4. After merge + acceptance, update baseharbor-plan Task-Vertrag (state transitions, Resolution, HTTPS Evidence) and publish.

This lane (w106) prepared ONLY. It did not rebase, re-dispatch CI, edit the PR, or touch baseharbor.

## CLEANLINESS

No containers/compose/projects started. No VM. No git mutation except the evidence commit.

## repo-rule compliance

- Read-only: no baseharbor product files touched, no .github/** edited, no rerun/workflow_dispatch.
- Hosted-only: no local product test / unit suite executed (no go test / python unittest / ci-fast-check).
- Subagents: none (§4.8). Contacted no other session.
- Evidence written into baseharbor-plan ONLY, never a product repo.
