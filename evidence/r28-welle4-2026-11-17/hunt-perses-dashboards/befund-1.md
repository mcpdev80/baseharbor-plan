# Befund 1 — Perses dashboard selection catalog on develop is dead code (no production consumer, catalog keys never realized)

- file:line: `internal/capability/perses_selection.go` (whole file, `DefaultDashboardCatalog`/`EligibleFor`/`FilterEligibleDashboards`/`Templates()`), `internal/metrics/perses_dashboards_valkey.go` (whole file)
- Type: dead code + catalog/datasource drift (consumer-visible contract gap)
- SHA base: `62eaea2c8c5b29f73db03ae9b3e7efaf772e4458` (develop HEAD, verified `git ls-remote origin develop`)
- Repo: `https://github.com/mcpdev80/baseharbor.git`
- Slice: (a) dashboard-JSON against perses-contract, (c) error paths

## Statement

The merged develop tree (62eaea2c8) declares a Perses-native **dashboard selection catalog** (`perses_selection.go`) with four catalog keys — `prometheus-targets`, `loki-logs`, `tempo-traces`, `keycloak-identity` — each carrying a datasource kind (`prometheus`/`loki`/`tempo`/`keycloak`) and a supported version (`v0.55.1`). **Every one of these functions has zero production consumers on develop.** The catalog exists only in its own test file (`perses_selection_test.go`). No `cmd/baha` command, no status collector, no render/apply path calls it. The only live dashboard realization on develop is the Valkey face (`perses_dashboards_valkey.go`), which is explicitly UNAVAILABLE and ships no JSON resource.

Evidence (all verified against 62eaea2c8):

- `git grep` for `DefaultDashboardCatalog|EligibleFor|FilterEligibleDashboards|Templates()|HasTemplate` in non-`*_test.go` Go files returns nothing except the definitions themselves.
- `git ls-tree -r develop --name-only | grep -i dashboard` returns only the two Go files; **no dashboard JSON resource is committed on develop.**
- The selection catalog's datasource kinds (`prometheus`/`loki`/`tempo`/`keycloak`) do **not** resolve to any emitted dashboard: the catalog returns eligibility verdicts only, never a Perses `Dashboard` resource, never a JSON document. There is no apply/read-back path from the catalog to a Perses resource on develop.

## Consequence

- The four catalog keys are declared but **never realized**: a consumer that asks "which Perses dashboards are eligible?" gets a verdict, but no dashboard is produced, applied, or surfaced. The catalog reads as a stub whose production wiring is missing, not a finished selection layer.
- Datasource drift risk: `keycloak-identity` declares `Datasource: "keycloak"` in the catalog (`perses_selection.go:223`), while the separate 0428-082 infra-dashboard face (NOT merged to develop) pins `PrometheusTimeSeriesQuery` over a `prometheus` datasource. If the two faces ever reconcile, the catalog's `keycloak` datasource kind and the infra dashboard's `prometheus` datasource selector must line up; they currently live in disjoint trees with no cross-check.
- The Valkey catalog key is `valkey-targets` (`perses_dashboards_valkey.go:55`), a name that mirrors the (non-existent on develop) database-dashboard key `postgresql-targets`/`mongodb-targets` referenced only in the 082/077 lane code. On develop the `valkey-targets` key names a dashboard that is explicitly unavailable; a future consumer wiring the key to a real datasource must not assume a `valkey` datasource exists (Valkey has no native Perses signal; RequiresAdapter).

## Repro (reproducible, read-only, no containers)

```
$ git ls-tree -r develop --name-only | grep -i dashboard
internal/metrics/perses_dashboards_valkey.go
internal/metrics/perses_dashboards_valkey_test.go
# (no dashboard JSON resource committed)

$ git grep -n "DefaultDashboardCatalog\|EligibleFor\|FilterEligibleDashboards\|Templates()" -- '*.go' | grep -v '_test.go'
# (nothing: catalog is test-only)

$ go test ./internal/capability/ ./internal/metrics/ ./cmd/baha/ ./...   # all green
```

The status CLI round-trip was observed end-to-end (built `cmd/baha`, ran `baha status --json` over a temp root with `services.perses=true`): `state=not_applied`, `perses=configured_unverified`, `metrics/application.support=SUPPORTED` — the Perses **seam** (`perses.go`) is live, but the **dashboard catalog** behind it produces nothing. The dashboard face that would realize `prometheus-targets` (0428-082 `perses_infra_dashboards.go`) lives only on `origin/lane-0428-082-perses-dashboards`, not on develop.

## Severity

MEDIUM. No runtime failure and no false dashboard ships — the fail-closed seam and the Valkey-unavailable witness both work. The defect is that a whole selection layer is committed without its consumer, so the catalog/datasource contract is unexercised and the catalog-vs-realized-dashboard drift (esp. `keycloak` vs `prometheus` datasource) is unguarded. Recommend either wiring the catalog into the status/render path (owner scope) or removing the dead catalog so the dashboard contract is not half-implemented.

## Notes

- Pure finding, no product change. Build/vet/test all green on 62eaea2c8.
- Compose note: no test compose project started by this lane; `bh-local-shared` (running, 4 services) belongs to a different lane (`hunt-uid-he`) and was left untouched.
