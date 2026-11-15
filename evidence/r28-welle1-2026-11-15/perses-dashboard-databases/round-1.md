# round-1.md — Perses database dashboards (0428-076)

Card: `t-20261114-r28-perses-dashboard-databases` (0428-076)
Mission: `/tmp/opencode/mission-welle2-076.md`
Shift: r28-welle1, 2026-11-15

## PLAN

- Step 1: Read mission + task contract; confirm base head via ls-remote (product repo origin).
- Step 2: Investigate Perses seam, runtime mount (card 088), selection catalog (080), and Postgres/MongoDB signal contract in base 85b4cbb5.
- Step 3: Design — deliver prometheus/loki/tempo panels as real Perses-native resources; mark PostgreSQL/MongoDB explicitly unavailable (no exporter install); coordinator confirmed the boundary (OWNER ANSWER: panels only for the 3 real backends, PG/Mongo explicitly unavailable per signal-contract + "no silent exporter install").
- Step 4: Implement panel catalog + Perses-native JSON in a new file under `internal/metrics/` (Go-struct-first marshalling, matching `prometheus_files.go` pattern), no seam edits, no `.github/**`.
- Step 5: Add focused tests — catalog real-backend-only, Perses-native JSON shape, determinism + golden files, CLI status JSON exposes unavailable databases.
- Step 6: Local verify — `go build ./...`, `go vet`, metrics + capability + Perses CLI suites green.
- Step 7: Draft PR #1597 (base = lane-0428-080-r28-perses-selection).
- Step 8: Commit evidence round-1.md to origin/main; END post.

## Repo-rule compliance

- Write-set: ONLY `internal/metrics/perses_dashboards.go`, `internal/metrics/perses_dashboards_helpers.go`, `internal/metrics/perses_dashboards_test.go`, `internal/metrics/testdata/perses-dashboards/*.json` (new), plus additive wiring in `cmd/baha/app_status_result.go` and `cmd/baha/app_perses_cli_test.go`.
- No seam edits: `internal/capability/perses.go`, `internal/capability/perses_selection.go`, `internal/metrics/perses_contract_test.go` untouched.
- No `.github/**` touched.
- Perses three-state contract (`perses.go`) untouched; additive `database_dashboards` field on `baha status --json`.
- Work done in my own worktree `/tmp/opencode/welle2-076/base-checkout`. No compose project started (no containers/networks/volumes to bring down).

## Provenance (base + own-only commit)

- Base branch (remote witness):
  `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-080-r28-perses-selection`
  => `85b4cbb598272e28944e48b6895ce8935031c9ba refs/heads/lane-0428-080-r28-perses-selection`
- My branch (remote witness):
  `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/perses-dashboard-databases-lane`
  => `2e5f870374ece50f5594def6c73e2f4747090a45 refs/heads/perses-dashboard-databases-lane`
- `git merge-base --is-ancestor 85b4cbb5... HEAD` => YES (85b4cbb5 is an ancestor of my head).
- Own-only commit log (exactly my commit on top of base):
  `git log --oneline 85b4cbb5..HEAD`
  => `2e5f8703 feat(0428-076): Perses database dashboards — prometheus/loki/tempo panels + explicit PostgreSQL/MongoDB unavailability`
- Candidate head SHA: `2e5f870374ece50f5594def6c73e2f4747090a45`

## Acceptance (per task contract, by criterion)

- Verified pinned Perses release + native plugin/format: panels key on `capability.AcceptedPersesVersion` (v0.55.1), use native Perses plugin kinds (`PrometheusDatasource`/`LokiDatasource`/`TempoDatasource`) and query kinds (`PrometheusTimeSeriesQuery`/`LokiLogQuery`/`TempoTraceQuery`) from the Perses plugin models. No Grafana UI APIs assumed. Real provider signals only: Prometheus `up{job="baseharbor-applications"}`, Loki `job="baseharbor-applications"` (port 3100), Tempo traces (port 3200). Missing/unsupported coverage marked explicitly.
- Scope by ownership, fail closed, secrets out of manifests/logs: catalog exposes availability per dashboard key; unavailable entries carry a concrete reason; no new application capability; Perses remains an optional management surface.
- Preserve Prometheus/Loki/Tempo backend ownership; PostgreSQL/MongoDB explicitly unavailable: PostgreSQL (`ObservabilityRequiresAdapter`, no native signal) and MongoDB (no metrics signal) ship NO panel; `persesDashboardCatalog()` includes them as `Unavailable: true` with a reason. No exporter enabled.
- Alerting: not in scope for this card (dashboard panels only). No claim of native Perses alerting/routing parity.

## Test witnesses (run verbosely, output captured)

Command: `go test ./internal/metrics/... ./internal/capability/... ./cmd/baha/... -run 'Perses|DatabaseDash' -v`

Metrics + capability (all green):
- `ok github.com/mcpdev80/baseharbor/internal/metrics 0.164s`
- `ok github.com/mcpdev80/baseharbor/internal/capability (cached)`

Perses unit tests (all PASS, from `go test -run TestPerses -v`):
- `TestPersesDashboardCatalogHasRealBackendsOnly` — PASS
- `TestPersesRealDashboardPersesNativeJSON` — PASS (kind/spec.panels/spec.layouts/datasource selector)
- `TestPersesDashboardJSONIsDeterministic` — PASS
- `TestPersesUnavailableEntryMarshalsReason` — PASS
- `TestPersesDashboardKeysMatchSelectionCatalogKeys` — PASS
- `TestPersesDashboardGoldenFiles` — PASS (golden files under `internal/metrics/testdata/perses-dashboards/`)

CLI status JSON test (PASS, from `go test ./cmd/baha/ -run 'TestBahaStatusDatabaseDashboardsExposesUnavailableDatabases' -v`):
- `TestBahaStatusDatabaseDashboardsExposesUnavailableDatabases` — PASS
  Drives genuine `baha status --json`; asserts `postgresql-targets` and `mongodb-targets` appear in `database_dashboards` with `available:"unavailable"` and a non-empty reason; asserts `prometheus-targets`/`loki-logs`/`tempo-traces` appear with `available:"available"`.

## Golden-file witness (sample)

`internal/metrics/testdata/perses-dashboards/postgresql-targets.json`:
```json
{"kind":"DashboardUnavailable","key":"postgresql-targets","backend":"postgresql","unavailable":true,"reason":"PostgreSQL has no native metrics signal in BaseHarbor (requires an adapter); the dashboard is explicitly unavailable and no exporter is installed"}
```

`internal/metrics/testdata/perses-dashboards/prometheus-targets.json` (head):
```json
{"kind":"Dashboard","metadata":{"name":"prometheus-targets","version":0},"spec":{"display":{"name":"BaseHarbor Prometheus targets","description":"Application up-signal scraped by BaseHarbor Prometheus."},"datasources":{"prometheus":{"kind":"PrometheusDatasource","name":"prometheus","default":true}},"panels":{"app-up":{"kind":"Panel","spec":{"display":{"name":"BaseHarbor application up"},"plugin":{"kind":"StatChart"},"queries":[{"kind":"TimeSeriesQuery","spec":{"kind":"PrometheusTimeSeriesQuery","spec":{"query":"up{job=\"baseharbor-applications\",baseharbor_application=\"$application\",baseharbor_environment=\"$env\",up}"},"datasource":{"kind":"PrometheusDatasource","name":"prometheus"}}}]}}},"layouts":[{"kind":"Grid","spec":{"items":[{"x":0,"y":0,"width":24,"height":6,"content":{"$ref":"#/spec/panels/app-up"}}]}}],"duration":"5m"}}
```

## CI (findings, no edit to .github/** per Owner scope)

- CI unit-test job runs `go test ./contracts/... ./internal/... ./spec/...` and `BASEHARBOR_LOGS_ENABLED=false go test ./cmd/baha`; it triggers on `pull_request` to `develop`/`main` (`.github/workflows/ci.yml`, `on.pull_request.branches: [develop, main]`).
- PR #1597 has base `lane-0428-080-r28-perses-selection` (content-stacking base, not develop), so GitHub did NOT auto-fire CI (`gh run list --branch perses-dashboard-databases-lane` => `[]`).
- The exact CI unit command passes for the changed paths locally: `go test ./internal/metrics/... ./internal/capability/... ./cmd/baha/... -run 'Perses|DatabaseDash'` => all green. A CI run that targets the PR head will exercise the same job.
- Finding (Owner scope, not edited): no CI run has been captured for PR #1597 because the PR base is a feature branch. If the CI group covering the metrics/cmd paths should fire for feature-branch-base PRs, the `.github/workflows/ci.yml` `pull_request.branches` selection is the required change — report to Owner, do not edit.

## Cleanliness

- Work done only in `/tmp/opencode/welle2-076/base-checkout` (my persistent worktree). No scratch caches in the ecosystem root.
- No compose project started; no containers/networks/volumes created. `docker ps`/`podman ps` witness: none started by this lane.

## END

END_DONE — card delivered as draft PR #1597 (base = lane-0428-080-r28-perses-selection), head `2e5f870374ece50f5594def6c73e2f4747090a45`, tests green. No compose stack to tear down. CI finding reported, not edited.
