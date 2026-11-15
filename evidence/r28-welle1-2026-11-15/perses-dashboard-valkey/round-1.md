# round-1.md — 0428-081 Perses Valkey dashboard

Worker: w081 · Shift: r28-welle1-2026-11-15 · Date: 2026-11-16
Model: Ornith-Laptop · Session: 476ffa1d-add0-483f-bd43-a8a318d1b888

## PLAN

1. Read mission + task contract (plan.py show t-20261114-r28-perses-dashboard-valkey)
2. Verify base head via ls-remote; cut wt-0428-081 from a270725bd; confirm ancestor
3. Claim task via plan.py claim; commit+push claim to planning origin/main
4. Investigate source: observability registry, reference.go, perses.go, perses_selection.go, perses_dashboards precedent
5. Determine signal contract: Valkey has NO native metrics signal (RequiresAdapter, no exporter)
6. Scope decision from coordinator: Option A confirmed
7. Write own Valkey dashboard panel file (go structs -> perses-native JSON)
8. Write golden file + golden test
9. go vet + go build ./... + focused local tests
10. Write evidence akte
11. Draft PR (title contains 0428-081), base = lane-0428-080-r28-perses-selection
12. Push evidence to origin/main; END with head-SHA

## Acceptance witnesses

### Base head (regel 8, faecher)
- ls-remote verified base head:
  `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-080-r28-perses-selection`
  => `a270725bdd795a5c944caf96fd1161ec44688a55`
- Branch cut from that exact SHA: `wt-0428-081` at `a270725bdd795a5c944caf96fd1161ec44688a55`.
- Ancestry witness: `git merge-base --is-ancestor a270725bd HEAD` => PASS (base is an ancestor of HEAD).
- First commit will be a direct child of a270725bd; `git log` will list ONLY my own commits.

### Signal-zeugnis (contract)
- Valkey metrics declared `ObservabilityRequiresAdapter` in `internal/capability/reference.go` (ValkeyIntegration, line ~48). No native metrics signal.
- No Valkey metrics exporter exists anywhere in the repo (verified: `internal/` has no valkey metrics/exporter; `internal/providertopology/observation.go` only detects valkey containers, no Prometheus scrape target).
- Perses seam (`internal/capability/perses.go`) forbids false-declaring a metric ("Never false-declare metrics/logs/traces capabilities").
- Precedent: PostgreSQL/MongoDB are explicitly UNAVAILABLE in the #1597 `perses_dashboards.go` (golden files `postgresql-targets.json`, `mongodb-targets.json` report `kind: DashboardUnavailable`, `unavailable: true`).

### Deliverable (Option A, own write-set)
- New file: `internal/metrics/perses_dashboards_valkey.go` (own panel file, own types, own catalog, own helpers).
- Golden file: `internal/metrics/testdata/perses-valkey/valkey-targets.json` (reason doc, not a fabricated panel).
- Golden test: `internal/metrics/perses_dashboards_valkey_test.go` (6 tests).
- reference.go and `capability.DefaultDashboardCatalog()` (perses_selection.go) are UNTOUCHED — no shared-catalog line edited, no fake Valkey signal declared.

### Test results (local, self-run)
- `go test ./internal/metrics/ -run PersesValkey` => PASS (6 tests).
- `go test ./internal/metrics/ ./internal/capability/...` => PASS.
- `go vet ./internal/metrics/` => clean.
- `go build ./...` => BUILD OK.
- gofmt: both new files clean.

### Faechregel (disjoint write-sets)
- Valkey catalog key `valkey-targets` is disjoint from #1597 keys (prometheus-targets, loki-logs, tempo-traces, postgresql-targets, mongodb-targets) and 0428-077 keys (prometheus-host-container, loki-host-container, tempo-host-container, host-node-metrics, container-stats).
- Test `TestPersesValkeyDashboardKeysDistinctFromOtherInventories` pins this. No line of any other lane's inventory is edited.

## Scope notes / conflicts

- The dashboard REALIZATION `perses_dashboards.go` (#1597 inventory) does NOT exist in base a270725bd. Per faechregel it is out of scope; I built my own Valkey file. No conflict — nothing to edit.
- No shared-catalog line edit was required for Option A, so no file:line conflict to hand to the coordinator.

## End state

- Candidate branch: wt-0428-081 (base a270725bd, verified).
- Commit SHA pending first commit + push.
- PR: draft, title contains 0428-081, base = lane-0428-080-r28-perses-selection.
- CI dispatched by coordinator (per mission).
