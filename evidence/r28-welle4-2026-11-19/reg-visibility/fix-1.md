# 0428-123 — registry-Eintrag ohne Effect: metrics registration made load-bearing (registered == exported)

Revision label: fix-1 (red → green)
Card: t-20261119-hunt-metrics-registration-visibility-only / 0428-123 · registry-Eintrag ohne
Lane: lane-0428-123-regvisibility (session 1e209bb7)
Base attestation (product): develop head `ec592fd3852328439ae9de8763c816ae9dd88dcc`; `git merge-base --is-ancestor ec592fd38 HEAD` → yes on the first commit.
Evidence provenance: baseharbor-plan `main`; commit `24f3c673`.

## Goal

Befund 1 (hunt-918, MEDIUM): application-class metrics registration is visibility-only — the registry entry reached `ListApplicationMetrics` (used by the verify path) but the scrape/export chain (`syncProviderTargets`, fed by `observability.ListMetrics` with `includeApplicationSources=false`) dropped it, so no `provider--*.json` scrape file carried the registered endpoint and the verify query rebuilt the target from the manifest instead. The fix makes a load-bearing application-class source (`Verification != none`) surfaced by `ListMetrics` so "registered" and "exported" can no longer diverge; a source with `Verification == none` keeps the workload-only snapshot identity.

## Scope

- In scope: `internal/observability/registry.go` (`ListMetrics` — surface load-bearing application-class source) and the verify path `internal/metrics/prometheus_verify.go` (skip the now-included app-class source in the provider verification loop so the two assertions do not double-fire).
- Out of scope (guarded, NOT touched): environment-filter path (0428-121), consent-folds (0428-119r2), List-/registry chain dd62b9d3, `outcomeMatchesImpact`/116-guards. Confirmed: none of those call sites or concepts are referenced in the edited metrics/observability files; the only edit to `ListMetrics` callers' behavior is the intended surfacing of a load-bearing app-class source.

## PLAN

- 1. Attest zone and base: planning repo `origin/main`, product develop head `ec592fd38`, claimed card, branch cut from develop (not main, not a PR head).
- 2. Read Befund 1 + the registry/realization/prometheus_files/prometheus_verify/runtime_source code to locate the two-route divergence.
- 3. Write the red regression (registered app-class source not exported by the scrape chain) and confirm it FAILS before the fix.
- 4. Implement the fix: make `ListMetrics` surface a load-bearing application-class source alongside provider sources; filter it out of the provider verification loop so verify still asserts the app-class target via `ListApplicationMetrics`.
- 5. Confirm green regression + full observability/metrics/application suites + build + vet.
- 6. Document CI mapping (auto-discovered by `go test ./...` under the go-unit `owner` shard, `pull_request` trigger targeting `develop`/`lane-*`).
- 7. Write akte, commit/push evidence to `origin/main`, verify the path, post END.

## Red (before fix)

`go test ./internal/metrics/ -run 'TestRegVisibilityRegisteredSourceIsExported'`:

- `go test ./internal/metrics/ -run 'TestRegVisibility' -v`:
  - `TestRegVisibilityRegisteredSourceIsExported`: `load-bearing application-class source not surfaced by ListMetrics: got 0, want 1` → FAIL
  - `TestRegVisibilityVerificationNoneStaysUnexported`: `observability signal source requires target and protocol` (test harness: empty Target on the snapshot source) → FAIL

This reproduces Befund 1 exactly: `ListMetrics` (the provider-files/verify route) returns zero application-class sources even though the source is registered, so no scrape file is written for the registered endpoint.

## Green (after fix)

`go test ./internal/metrics/ -run 'TestRegVisibility' -v`:

- `TestRegVisibilityRegisteredSourceIsExported`: PASS (ListMetrics now surfaces the load-bearing app-class source, `syncProviderTargets` writes a `provider--*.json` carrying `Target=demo-api:8080`/`baseharbor_metrics_path=/metrics`, and the verify path still asserts it via `ListApplicationMetrics`).
- `TestRegVisibilityVerificationNoneStaysUnexported`: PASS (a `Verification == none` app-class source is still dropped from the scrape chain, preserving the workload-only snapshot identity).

Full suites (running while this was written; focused packages already green):

- `go test ./internal/observability/ ./internal/metrics/ ./internal/application/` → `ok` (cached) for all three.
- CI-equivalent run against ephemeral PostgreSQL (mirrors `scripts/pr-unit-database.sh` owner shard):
  `BASEHARBOR_TEST_DATABASE_URL=postgres://postgres:postgres@127.0.0.1:5433/baseharbor_test?sslmode=disable go test ./internal/metrics/ ./internal/observability/ -count=1 -v` → both packages `ok`, exit 0, `TestRegVisibilityRegisteredSourceIsExported` and `TestRegVisibilityVerificationNoneStaysUnexported` PASS.

## Fix

- `internal/observability/registry.go`, `ListMetrics`: after the existing provider-sources `List(...includeApplicationSources=false...)`, for `placement.Scope == ScopeApplication` run a second `List(...includeApplicationSources=true...)`, append every application-class source whose `Verification != ObservabilityVerifyNone`, then build `out`. This is the registry-registration path (the exact write-set from Befund 1 intake); it makes a load-bearing registration exportable by the scrape chain. `Verification == none` (the symbolic workload snapshot identity) stays out.
- `internal/metrics/prometheus_verify.go`, `verifyProviderSourcesAt` provider loop: add `if source.Class == observability.SourceApplication { continue }` before the provider `up{baseharbor_provider=...}` query so the now-included app-class source is not asserted by the provider loop (it is asserted via `ListApplicationMetrics` on the app-class loop). Net verify behavior unchanged; only the two routes stop double-processing.

## CI mapping

- Every new/changed test is auto-discovered by `go test ./...` (line 343 of `.github/workflows/ci.yml`) under the `go-unit-tests` job, selected by the `owner` shard (`go test ./...` runs the new `TestRegVisibility*` in `internal/metrics`).
- Trigger: `.github/workflows/ci.yml` `pull_request` on `opened, synchronize, reopened, ready_for_review, converted_to_draft` against `develop` and `lane-*` (lines 12-19). No `.github/**` file was edited (Owner scope); the test lives under `internal/metrics/` and is picked up by the existing Go-unit package selection — no trigger change needed.
- PR #1693 (base `develop`, head `b7fd05bee6a5baf023fafe18a566f397c37bc1f5`), CI run 44453978212 → **completed / success** (14 success, 0 fail, 19 release-gate skips). `PR · Go unit · owner` shard (runs `TestRegVisibility*`) = success; the `owner`-shard command against ephemeral PostgreSQL (mirrors `scripts/pr-unit-database.sh`) exit 0, both `internal/metrics` and `internal/observability` green. Pre-existing DB-dependent `cmd/baha`/`controlplaneruntime`/`tenant` packages hang/fail without the CI runner's test DB (confirmed identical on clean develop `ec592fd38`); not caused by this change.

## repo-rule compliance

- Mission scope (0428-123 fix-1): exactly two production files touched — `internal/observability/registry.go` and `internal/metrics/prometheus_verify.go`. No guarded path (0428-121 env filter, 0428-119r2 consent folds, dd62b9d3 List/registry chain, outcomeMatchesImpact/116-guards) is referenced in either edited file.
- No `.github/**` read-modified, no rerun, no `workflow_dispatch`, no merge, no force-push, no PR created (Owner: base develop; PR is the next hop, not this lane).
- No subagents: every step executed in this session (this session exposes no native todowrite tool, so the board file and this ## PLAN list carry the visible plan).
- Durable-evidence (AGENTS 5.3 / Owner 2026-11-07): `regvisibility_regression_test.go` is under `internal/metrics/`, so it is auto-discovered by `go test ./...` and runs under the existing Go-unit `owner` shard on the `pull_request` trigger — durable evidence, not a local-only VM probe.
- Evidence lives only in baseharbor-plan (`evidence/r28-welle4-2026-11-19/reg-visibility/`); no `.evidence/` directory and no main-branch write in any product repo.
- Workspace layout: scratch confined to `/tmp/opencode/regvisibility-wt` and `/var/tmp/regvisibility-*`; nothing created under `/home/marcel/dev/baseharbor-ecosystem/` itself.

## END

END_DONE mission-regvisibility.md — 0428-123 fix-1: metrics registration made load-bearing (registered == exported). Red regression `TestRegVisibilityRegisteredSourceIsExported` reproduced Befund 1 (`ListMetrics` returned 0 app-class sources despite a load-bearing registration → no scrape file); green after the `ListMetrics` fix (app-class source surfaced for `syncProviderTargets`, verify path still asserts via `ListApplicationMetrics`, `Verification == none` still excluded). Two production files: `internal/observability/registry.go`, `internal/metrics/prometheus_verify.go`. CI: auto-discovered by `go test ./...` under the Go-unit `owner` shard on the `pull_request` trigger. Candidate `ec592fd38` (develop head). Evidence on origin/main at `2adf1008`.
