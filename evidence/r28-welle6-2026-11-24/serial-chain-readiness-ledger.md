# Serial-chain readiness ledger — #1812 → #1819 → #1820 / #1818

Lane: w79-0428-249-chainledger (read-only Befund/planning, §3.3.3 hunt fill). No rebase, no push to baseharbor, no merge, no CI trigger. All data measured read-only via `git ls-remote`, `git diff` on a blob:none clone, and the `gh` API against `https://github.com/mcpdev80/baseharbor.git`.

## PLAN
- Read mission, verify workspace + planning-repo remote, set up read-only clone under /tmp.
- Fetch fresh develop + all four lane branches; record develop HEAD.
- Analyze #1812 diff, reload survival, artifact-gate, corruption, gate count.
- Analyze #1819 base-vs-develop, rebase target, ghost-catalog rows.
- Analyze #1820 missing regression quote, void run, base freshness.
- Analyze #1818 gate dependency + strict-serial ordering + go/no-go.
- Write this ledger, commit atomically to baseharbor-plan, verify origin/main.
- Post END_DONE.

## Base attestation
- Real planning repo (verified BEFORE first evidence commit): `origin https://github.com/mcpdev80/baseharbor-plan.git`
- Fresh develop HEAD (measured via `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`): `46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2`
- Blob:none read-only clone under /tmp/baha-readonly; remote = `origin https://github.com/mcpdev80/baseharbor.git`.

## Current remote heads (git ls-remote, read-only)
- develop: `46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2`
- lane-0428-249-runtime-image-fix (#1812): `f2433d7fd0fc969d9ce01033a59b0d424c9739da`
- w54-0428-181-export (#1819): `17381017be986f0eccb25662ad742ad759296346`
- fix/broker-build-identity (#1820): `28803d11027197e7734fb3ec94bef9b34e224b0d`
- lane-0428-078-cf-fix (#1818): `20fc1cb7d49602dc7f8aa0004a7562a81311d78c`

All four lane heads are NOT ancestors of develop (all need rebase onto current develop).

## #1825 (the tag-artifact blocker)
- PR #1825 `fix(0428-249): build baha-ci-operator-testonly artifact with its build tag`, branch `lane-0428-249-tagfix`, head `844987ded88b1c365f5b660e3f700af69e52bb5a`.
- State: MERGED (mergedAt 2026-11-24T12:43:08Z). Squash-merged, so the PR head SHA is not a direct ancestor of develop, but its CONTENT is on develop.
- Confirmed on fresh develop (sha `46d3dccc`): pre-release.yml line 505 builds `baha-ci-operator-testonly` with `-tags=baseharbor_ci_operator_testonly`, and lines 512-514 run the `go version -m` build-tag proof (`grep -q -- '-tags=baseharbor_ci_operator_testonly'`). This is exactly the operator-auth denial that #1825 clears. **The operator-auth denial is now cleared on develop.**
- Consequence for #1812: the runtime image is now exported from develop's pre-release.yml (`docker save ... baseharbor-runtime-pre-release.tar`, line 621) and uploaded as the `pre-release-runtime-candidate` artifact. #1812's +20 reload restores that tar in the runtime-suite when it is missing.

## #1812 (card 0428-249, branch lane-0428-249-runtime-image-fix, head f2433d7f)
- Diff vs develop: exactly the intended `+20` in `.github/workflows/pre-release-runtime-suite.yml` (two runtime-image-tar reload blocks added at the backup-restore path ~line 341 and the lifecycle path ~line 372), PLUS a stray `-334` revert.
- Stray revert (CORRUPTION / scope violation): the same single commit `f2433d7f` also deletes the now-canonical 0428-276 owner-re-check tests that #1824 merged into develop — `cmd/baha/env_destroy_integration_test.go` (-56), `internal/deployment/environment_destroy_scope.go` (-48), `internal/deployment/environment_destroy_scope_test.go` (-234). The branch's merge-base is the OLD base `05ef485369053b732f4b538d7f960275bda48fe9` (pre-#1824); develop HEAD is `46d3dccc`, and develop HEAD `fix(0428-276): make env-destroy OwnerVerified a genuine per-deployment owner re-check (#1824)` MERGED.
- Reload survival: #1825's fix is live on develop, so on the rebase onto current develop the +20 reload still applies cleanly (the two guard sites exist at the same lines) and the tag from #1825 clears the operator-auth denial. The +20 must be verified after rebase — it currently survives only against the stale base, not against `46d3dccc`.
- Artifact-gate dependency: #1812's gate is the `pre-release-runtime-suite` Light runtime gates. The `load_image` step fails closed at `test -s "$archive"` (line 189) if the `pre-release-runtime-candidate` tar is absent — which is exactly what #1825 fixed. **Go/no-go for #1812: #1825 must be merged first (done), then #1812 rebased onto current develop and the +20 reload re-verified; the stray -334 revert must be removed.**
- 14 Light gates that must go green before merge: the `runtime_light_gates_docker` + `runtime_light_gates_podman` matrices — 7 docker + 7 podman Light gates (`Light · <runtime> · <gate>`), gated on `needs.source.result == success` and `needs.runtime_candidate.result != failure`. Selection of which of the 14 fire is decided by the source-selection script; a workflow-only change (the +20) selects the runtime lifecycles that the coverage resolver maps.
- CI state for head f2433d7f: NO CI RUNS. Branch is stale + corrupted.

## #1819 (card 0428-181, branch w54-0428-181-export, head 17381017, RC1+RC2 done)
- Commits on branch vs develop: `9f84f47a` (wire) + `17381017` (RC1 fail-closed producer-path regression + RC2 byte/hash-stability).
- Diff vs develop: `internal/metrics/perses_dashboard_provision.go` (+388), `internal/metrics/perses_dashboard_provision_test.go` (+327), plus product wiring; AND the same stray `-334` 0428-276 revert (merge-base `05ef4853`, pre-#1824).
- Ghost-catalog dependency: the catalog rows `source.internal_metrics_perses_dashboard_provision_go` and `source.internal_metrics_perses_dashboard_provision_test_go` (paths `internal/metrics/perses_dashboard_provision.go` / `..._test.go`, surfaces `source.gate.atomic.docker.data.capabilities` + `source.gate.atomic.podman.data.capabilities`) ARE present on fresh develop in `scripts/pr-gate-coverage.json`. **The catalog rows are already live on develop, so #1819's CI will select these rows when the new source files land.**
- Base vs develop: branch merge-base `05ef4853` ≠ develop `46d3dccc`; needs rebase onto current develop.
- Run id to expect: the `pre-release` workflow `Light · …` gates after merge (no run id exists yet for head 17381017).
- CI state for head 17381017: NO CI RUNS. Stale base (same -334 revert).

## #1820 (card 0428-271, branch fix/broker-build-identity, head 28803d11)
- Missing regression (the one the mission asks to quote): `cmd/baha/app_broker_compat_test.go`, `TestVerifyRuntimeBrokerBuildIdentity`, the added acceptance-criterion-2 case in commit `28803d11`:
  - version = "dev" / commit = "" / `verifyRuntimeBrokerBuildIdentity("edge", "")` must return nil (empty dev CLI commit + empty edge runtime commit stays green).
  - The regression it covers lives in `cmd/baha/app_broker.go`, `verifyRuntimeBrokerBuildIdentity` (line 652): commit provenance check at line 672 (`if expectedCommit != "" && actualCommit != "" && expectedCommit != actualCommit`), with the dev/edge leniency at line 661 (`developmentPair := expectedVersion == "dev" && actualVersion == "edge"`). The regression asserts the `dev`/`edge` development pair with an EMPTY CLI commit AND an EMPTY runtime commit stays green — the combined dev/edge + empty-commit pair not covered by the earlier "none" sentinel case.
- Void run: CI run 45382404741 (`PR #1820`, event pull_request, head 28803d11) is CANCELLED (void), confirmed via `gh api .../actions/runs/45382404741`.
- Base freshness: branch merge-base `05ef4853` ≠ develop `46d3dccc`; needs rebase onto current develop.
- CI state for head 28803d11: NO CI RUNS. Stale base (same -334 revert).

## #1818 (card 0428-078, branch lane-0428-078-cf-fix, head 20fc1cb7)
- Commits vs develop: `20fc1cb7` (wire keycloak identity dashboard) + `8e2c50c1` (real provider-class labels in Keycloak Perses queries) + `888e2193` (resolve app_status identity-field conflict on f3d847874) + `e0a93ce0` (re-locate perses identity-witness onto latest develop, references #1650).
- Diff vs develop (15 files, +970/-391): product wiring (`app_status_result.go +82`, `keycloak_files.go +15`, `keycloak_realization.go +11`, `perses_dashboards.go +26`, `perses_dashboards_keycloak.go +70`, `realization.go +155`, `internal/metrics/perses-dashboards/keycloak-identity.json +134`, `internal/operatorauth/*`); AND a `.github/workflows/pre-release.yml -9` line removal and `scripts/pr-gate-coverage.json -30` row removal; AND the same stray `-334` 0428-276 revert.
- Operator-auth seam: `internal/operatorauth/authorization.go` (in develop it is fail-closed with no trusted-local arm; #1818 reintroduces a `!ManagedEnvironment(...) && !ok` trusted-local open arm) — a behavioral change to the operator-auth decision, owned by the product/contract, not a lane-only edit.
- Base vs develop: branch merge-base `3ebfb90d` ≠ develop `46d3dccc`; needs rebase onto current develop.
- CI state for head 20fc1cb7: NO CI RUNS. Stale base.

## Strict-serial dependency (§1825 merge is the gate)
- #1812 merge is the GATE for #1819 (per plan). #1819 merge is the GATE for #1820. #1819 merge is one of #1818's gates. Chain order: #1812 → #1819 → #1820, and #1819→#1818.
- GO/NO-GO per PR (all currently NO-GO; none can advance without disturbing the others' exact-head CI):
  - #1812: NO-GO. Head f2433d7f is stale AND carries a -334 revert of merged #1824. Go only after: rebase onto develop `46d3dccc`, DELETE the stray revert (restore the #1824 owner-re-check tests), re-verify the +20 reload applies and survives, then run the 14 Light gates to green.
  - #1819: NO-GO. Stale base + stray -334 revert. Go only after #1812 merged + rebased onto current develop.
  - #1820: NO-GO. Void run; stale base + stray -334 revert. Go only after #1819 merged + rebased.
  - #1818: NO-GO. Stale base + stray -334 revert + touches `.github/**` (Owner scope) + reintroduces an operator-auth trusted-local open arm (contract change). Go only after #1819 merged + rebased.
- They must NOT be advanced in parallel: each PR's exact-head CI must run against the base produced by the previous merge; rebasing a lower PR onto a changed develop changes the higher PRs' tested heads, invalidating their exact-head CI.

## Artifact-gate dependency for #1812
- #1812's runtime-suite gates consume the `pre-release-runtime-candidate` artifact tar `baseharbor-runtime-pre-release.tar`. develop's pre-release.yml now builds+bakes that tar (line 621) after #1825's operator-auth fix is live. The runtime-suite `load_image` step fails closed (`test -s "$archive"`, line 189) if the tar is absent — the operator-auth denial #1825 fixed.
- GO/NO-GO: #1825 must be merged before #1812's gate can pass (done on develop). #1812 then must be rebased onto current develop with the +20 reload re-verified and the stray -334 revert removed; only then are the 14 Light gates eligible to run green.

## Read-only witnesses (pasted outputs)
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` → `46d3dccc1f6fc65c027f5c2a28e9d17b29c5fed2`
- #1825: `gh api .../pulls/1825` → base `2b9a2c6d...`, head `844987d...`, merged `2026-11-24T12:43:08Z`. develop contains #1825's `-tags=baseharbor_ci_operator_testonly` + `go version -m` proof (pre-release.yml:505,512-514).
- #1820 void run: `gh api .../actions/runs/45382404741` → status `completed`, conclusion `cancelled`, head `28803d11`.
- Catalog rows present on develop: `git show origin/develop:scripts/pr-gate-coverage.json` → `source.internal_metrics_perses_dashboard_provision_go` / `_test_go` with docker+podman data.capabilities surfaces.
- No CI runs for any of the four stale heads (all `NO CI RUNS`).
- #1818 operator-auth revert (develop has the fail-closed seam; #1818 reintroduces the trusted-local open arm): `git diff origin/develop..origin/lane-0428-078-cf-fix -- internal/operatorauth/authorization.go internal/operatorauth/config.go`.

## cleanliness
- Blob:none read-only clone under /tmp/baha-readonly only; no product-repo writes, no worktree created, no containers/compose started. No docker/podman state touched. No CI triggered. No rebase/push/merge.
- /tmp/baha-readonly created by me this lane; no orphans.
