# Serial-Chain Prep — Read-Only Evidence (shift w84, card 0428-216)

- Task: `0428-216` — read-only serial-chain prep desk
- Role: READ-ONLY PREPARATION / FINDINGS ONLY. No push/rebase/merge/PR-CI trigger on any PR. No subagents. No other worker sessions.
- Author: worker session (this lane). Model verified at session start.
- Date: 2026-11-24

## REALITY WITNESSES (all via git ls-remote / fresh clone in /tmp/opencode/w84-chain-prep)

- Planning repo path: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (NOT workers/baseharbor-plan). Remote: `origin https://github.com/mcpdev80/baseharbor-plan.git`
- Planning origin/main head: `62754183cb54ee0ae2d5d766696e30adc2e765bb`
- Product develop head: `46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2` (matches mission expectation "expect 46d3dccc after #1825")
- #1819 branch `w54-0428-181-export` head: `17381017be986f0eccb25662ad742ad759296346`
- #1820 branch `fix/broker-build-identity` head: `28803d11027197e7734fb3ec94bef9b34e224b0d`
- #1818 branch `lane-0428-078-cf-fix` head: `20fc1cb7d49602dc7f8aa0004a7562a81311d78c`
- Fresh clone remote: `origin https://github.com/mcpdev80/baseharbor.git` (this is a temp clone in /tmp, NOT the quarantined workers/baseharbor checkout)

## ## PLAN

- Read mission + AGENTS; establish real remotes and planning-repo path
- Reality witnesses: develop HEAD, planning origin/main, three branch heads, fresh clone
- PR #1819: ls-remote, merge-base/behind, write-set diff, RC1+RC2 cross-ref, ghost-catalog
- PR #1820: ls-remote, diff vs base, missing-regression check, base contamination
- PR #1818: ls-remote, clean-head diff, C-retarget seam pins, gate dependency
- Write this evidence file
- Commit + push single evidence file to baseharbor-plan origin/main; verify path on origin/main
- Cleanup clone; post END line

## FINDINGS

### PR #1819 — card 0428-181, branch `w54-0428-181-export`

| Field | Value |
| --- | --- |
| Current head | `17381017be986f0eccb25662ad742ad759296346` (commit: "fix(0428-181): RC1 fail-closed producer-path regression + RC2 byte/hash-stability") |
| Behind base | merge-base with develop = `05ef485369053b732f4b538d7f960275bda48fe9`; develop is NOT an ancestor of head — head is 2 commits behind develop (`git rev-list --count origin/develop..branch` = 2) |
| Write-set (vs merge-base `05ef485`) | 3 files: `internal/application/runtime_postgres.go`, `internal/metrics/perses_dashboard_provision.go`, `internal/metrics/perses_dashboard_provision_test.go` — NO `scripts/**`, NO `.github/**` |
| RC1 (fail-closed witness) | VERIFIED. `perses_dashboard_provision_test.go`:29-44 — `TestPersesDashboardProvisionUnqualifiedWitnessWritesNothing` calls `persesDashboardProvisionForLifecycle` (:40) for selected + probe-verified Perses with unqualified identity witness, seeds stale `keycloak-identity.json`, asserts it is removed (:43). Producer passes witness through `FilterEligibleDashboards`. |
| RC2 (byte/hash stability) | VERIFIED. `perses_dashboard_provision_test.go`:210-289 — `TestPersesDashboardProvisionKeycloakIdentityBytesStable` runs the real producer twice into separate roots, pins SHA-256 to `b964f6eb9b587cceec68c0fad9be44f8937f6e6ec7ff2f07eb0424ad8e627e2e` (:274), asserts Perses envelope (kind/metadata). |
| Ghost-catalog (card 0428-278) | YES — the `perses_dashboard_provision` coverage rows already exist on develop. `scripts/pr-gate-coverage.json` on develop (line ~1529/1534) contains both `source.internal_metrics_perses_dashboard_provision_go` and `source.internal_metrics_perses_dashboard_provision_test_go`, each with surfaces `source.gate.atomic.docker.data.capabilities`, `source.gate.atomic.podman.data.capabilities`. Ghost-state sequence is safe: row exists but file path (`internal/metrics/perses_dashboard_provision.go`) is absent from develop's PR-gate candidate until #1819 merges — the gate-plan skips the absent file, no failure. |
| Prior review state | codex-review-1819.md: RC1 and RC2 were VERIFIED present in source at head `92ce49501` (exact-head CI run `45375290795` terminal green). RC2 card-evidence gate was NOT inspectably met (card evidence array not updated). |

#1819 next-action (coordinator, verbatim):

- Rebase `w54-0428-181-export` onto current develop `46d3dccc` (was rebased onto `05ef485` in the prior review; develop has since advanced by #1824/#1825). Preserve the RC1/RC2 tests.
- Update Planning card `t-20261120-r28-identity-dashboard-catalog-consumer` with the exact-head run URL and the pinned SHA-256 `b964f6eb9b587cceec68c0fad9be44f8937f6e6ec7ff2f07eb0424ad8e627e2e` (RC2 acceptance item 2).
- Rerun required CI on the new head (`gh workflow_dispatch` on the PR's selected checks, or wait for the auto PR-push run); confirm `PR Selected Checks` success on the exact new head.
- Then request a fresh CODEX-REVIEW. STOP before merge until card evidence links the new run + hash.
- NOTE: develop advanced by 2b9a2c6d (card 0428-276, PR #1824, env-destroy OwnerVerified re-check) — unrelated to #1819 content but part of the new base.

### PR #1820 — card 0428-271, branch `fix/broker-build-identity`

| Field | Value |
| --- | --- |
| Current head | `28803d11027197e7734fb3ec94bef9b34e224b0d` (commit: "fix(0428-271): add dev/edge + empty-commit acceptance criterion 2 regression") — ADVANCED beyond prior review head `514084f3` |
| Behind base | merge-base with develop = `05ef485...`; develop advanced beyond it by #1825 (46d3dccc) |
| Diff vs develop (files) | `.github/workflows/pre-release.yml`, `cmd/baha/app_broker.go`, `cmd/baha/app_broker_compat_test.go`, `cmd/baha/env_destroy_integration_test.go`, `internal/deployment/environment_destroy_scope.go`, `internal/deployment/environment_destroy_scope_test.go` |
| Missing regression (RC2 dev/edge+empty) | VERIFIED PRESENT — NEW since prior review. `cmd/baha/app_broker_compat_test.go`:76-81 — `version = "dev"; commit = ""; verifyRuntimeBrokerBuildIdentity("edge", "")` asserts no error. This is the combined dev/edge + empty-commit acceptance case the review demanded. |
| Legit #1820 content | `cmd/baha/app_broker.go`: fail-closed commit comparison `if expectedCommit != "" && actualCommit != "" && expectedCommit != actualCommit` (only when both sides carry a concrete commit). `cmd/baha/app_broker_compat_test.go` commit-mismatch regression. |
| CONTAMINATION (critical) | The branch carries a contaminated tip inherited from the develop base, NOT from its own 4 commits. The branch's own 4 commits (`22ca61bb`, `2f9f2f05`, `514084f3`, `28803d11`) touch ONLY `cmd/baha/app_broker.go` + `cmd/baha/app_broker_compat_test.go` — clean. But develop commit `2b9a2c6d` (card 0428-276, PR #1824, "make env-destroy OwnerVerified a genuine per-deployment owner re-check") is on develop and its content is INVERTED on the current head: `internal/deployment/environment_destroy_scope.go` sets `OwnerVerified: true` (hardcoded) and removes `verifyEnvironmentDestroyDeploymentOwner` + seam hook + `TestOnlyDeploymentOwnerSeamHook`; `environment_destroy_scope_test.go` and `env_destroy_integration_test.go` have those 0428-276 regression tests REMOVED. |
| Contamination witness | `git show 28803d11:internal/deployment/environment_destroy_scope.go` — `OwnerVerified: true` (was real re-check in develop `2b9a2c6d`). `git diff develop..head -- internal/deployment/environment_destroy_scope_test.go` shows ~239 lines removed. |
| Scope conflict | The current head's diff now includes 0428-276 env-destroy scope changes — OUTSIDE card 0428-271's declared write-set (`cmd/baha/app_broker.go` + tests). This is a scope violation that must be resolved before merge. |

#1820 next-action (coordinator, verbatim):

- This branch has been advanced by a second lane that folded card 0428-276 work into it. The legit 0428-271 regression (dev/edge + empty commit, `app_broker_compat_test.go`:76-81) is present and correct.
- The 0428-276 changes on this branch are INVERTED vs develop `2b9a2c6d` (hardcoded `OwnerVerified: true` instead of a genuine per-deployment re-check) — this is a bug introduced by the fold-in, not a fix. Do NOT merge the current head.
- Recommend: the owning lane of card 0428-271 cuts a FRESH branch from current develop `46d3dccc`, cherry-picks ONLY its own 4 commits (`22ca61bb`..`28803d11`) — i.e. `git cherry-pick 22ca61bb 2f9f2f05 514084f3 28803d11` — onto the clean base, then runs exact-head CI on that clean candidate. The 0428-276 env-destroy work belongs on its own card/lane (already implemented correctly on develop via #1824), never on the 0428-271 PR.
- STOP before merge until the #1820 candidate diff contains ONLY `cmd/baha/app_broker.go` + `cmd/baha/app_broker_compat_test.go` and passes required CI on the new head.

### PR #1818 — card 0428-078, branch `lane-0428-078-cf-fix`

| Field | Value |
| --- | --- |
| Current head (remote) | `20fc1cb7d49602dc7f8aa0004a7562a81311d78c` (commit: "fix(0428-078): wire keycloak identity dashboard into develop metrics catalog") |
| Clean intended head | `8e2c50c10a537c00e30d62a47f29638a0f14d5ff` ("fix(0428-078): select real provider-class labels in Keycloak Perses dashboard queries") — still in the branch reflog history |
| Contaminated tip (VOID) | `20fc1cb7` — the mission's noted VOID tip. Diff vs develop = 15 files; it REMOVES the #1819 ghost-catalog rows from `scripts/pr-gate-coverage.json` (regressing #1819's producer) and inherits the 0428-276 env-destroy inversion from develop. |
| Clean-head diff vs develop (`8e2c50c1`) | 14 files; NO `keycloak-identity` catalog row registered in `persesDashboardCatalog()` (the catalog registers prometheus/loki/tempo/postgresql/mongodb only). Touches `.github/workflows/pre-release.yml` + `scripts/pr-gate-coverage.json` (adds the `perses_dashboards_keycloak` row) — see write-set caveat below. |
| (a) keycloak-identity row | ABSENT from `persesDashboardCatalog()` on the clean head — consistent with the mission's "NO catalog keycloak-identity row" for the reset-prep state. |
| (b) C-retarget seam pin | VERIFIED. Source seam: `DashboardBackendIdentity` backend wired via `persesDashboardForBackend`/`backendForKey` in `internal/metrics/perses_dashboards.go` + `perses_dashboards_keycloak.go` (the ONLY dashboard whose backend is `DashboardBackendIdentity`). Witness test `perses_dashboards_test.go:766` `TestPersesKeycloakDashboardQueriesSelectRealProviderLabels` drives real `persesDashboardCatalog()`, asserts `entry.Backend == "keycloak"`, and requires panel queries to key on `http_server_*` metrics + `job="baseharbor-providers"` (provider-class labels), rejecting application-class labels. |
| (c) gate dependency | CONFIRMED #1818 depends on #1819 merge (the #1819 ghost-catalog rows are the producer) AND an owner C-decision (the C-retarget seam pins the Keycloak dashboard to `persesDashboardProvisionForLifecycle`/`FilterEligibleDashboards` — a capability/owner decision). w75's reset-prep evidence `8bbfe9945` referenced in the mission is absent from the live evidence dir; verification is against current source only. |

#1818 next-action (coordinator, verbatim):

- The clean intended head is `8e2c50c1` (not the remote tip `20fc1cb7`, which is contaminated — removes #1819 ghost rows + inherits 0428-276 inversion).
- Cut a fresh branch from current develop `46d3dccc`, cherry-pick ONLY `8e2c50c1` + `888e2193` (the two clean 0428-078 fix commits, BEFORE the `e0a93ce0` hop commits that re-located onto a stale base). Discard the contaminated tip `20fc1cb7`.
- Verify the fresh candidate's diff vs develop contains the Keycloak dashboard wiring + the `perses_dashboards_keycloak` coverage row, NO `keycloak-identity` row registered in `persesDashboardCatalog()` (per reset-prep), and the C-retarget seam test at `perses_dashboards_test.go:766` passes.
- Confirm the #1818 gate depends on #1819 merge AND owner C-decision before running it (per (c) above).
- NOTE: `8e2c50c1` touches `.github/workflows/pre-release.yml` + `scripts/pr-gate-coverage.json` — both outside a worker's write-set. Report the exact needed change as a finding with file:line to the coordinator; do NOT edit them.

## GAPS / MISSED (from prior reviews, carried here)

- #1819 RC2 card-evidence gate (codex-review-1819.md line 50): card `t-20261120-r28-identity-dashboard-catalog-consumer` still does not link the exact-head run + pinned hash. Must be updated before #1819 merge.
- #1820 prior review (codex-review-1820.md): scope conflict was resolved to `app_broker.go` + test, and the dev/edge+empty regression was later added (now present at `app_broker_compat_test.go`:76-81). The NEW blocker is the 0428-276 contamination, not the original scope issue.

## CLEANLINESS

- Clone `/tmp/opencode/w84-chain-prep/baseharbor-clone` created for read-only inspection, removed at end of shift (temp clone, outside the quarantined workers/baseharbor checkout and outside the ecosystem root).
- No containers / compose projects / VM smoke tests started (this is a pure read-only git inspection task).
- No product repo writes, no PR-CI triggers, no rebase/push on any branch.

## repo-rule compliance

- Read-only mission: no product files changed, no edits to `.github/**` or `scripts/**`, no pushes on candidate branches.
- Planning repo verified as `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (remote `origin https://github.com/mcpdev80/baseharbor-plan.git`) before any commit.
- Remote truth measured only via `git ls-remote` / fresh temp clone; the quarantined `workers/baseharbor` checkout and its refs were NOT cited.
- No subagents (§4.8). No other worker sessions contacted.
- HOSTED-ONLY: no local product/unit tests run.

## END

END_LANE w84-0428-216-chainprep DONE — evidence committed to baseharbor-plan origin/main (single file, atomic). Three-column table per PR + verbatim next-action per PR delivered. Critical finding: #1820 branch head is contaminated with an INVERTED card 0428-276 env-destroy change folded in from develop `2b9a2c6d`; the clean 0428-271 regression is present but the head must NOT be merged as-is. #1818 clean head `8e2c50c1` identified; remote tip `20fc1cb7` is the VOID contaminated tip.
