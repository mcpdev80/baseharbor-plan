---
id: t-20261113-r28-grafana-dashboard-selection
card_number: "0428-034"
card_short_title: "Gate dashboard template activa"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: Implement a small provider/Target-aware dashboard catalog selection that enables only dashboard templates whose required…
kanban_title: 0428-034 · Gate dashboard template activa
priority: high
depends_on: [t-20261017-release-0-4-28-updates, t-20261113-r28-grafana-contract-seam, t-20261113-r28-grafana-signal-inventory]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261113-r28-grafana-dashboard-selection · Gate dashboard template activation #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261113-r28-grafana-contract-seam](t-20261113-r28-grafana-contract-seam.md), [t-20261113-r28-grafana-signal-inventory](t-20261113-r28-grafana-signal-inventory.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261113-r28-grafana-contract-seam](t-20261113-r28-grafana-contract-seam.md), [t-20261113-r28-grafana-signal-inventory](t-20261113-r28-grafana-signal-inventory.md)  
**Required by:** [t-20261113-r28-grafana-dashboard-databases](t-20261113-r28-grafana-dashboard-databases.md), [t-20261113-r28-grafana-dashboard-hosts](t-20261113-r28-grafana-dashboard-hosts.md), [t-20261113-r28-grafana-dashboard-identity](t-20261113-r28-grafana-dashboard-identity.md), [t-20261113-r28-grafana-dashboard-messaging](t-20261113-r28-grafana-dashboard-messaging.md), [t-20261113-r28-grafana-dashboard-valkey](t-20261113-r28-grafana-dashboard-valkey.md), [t-20261113-r28-grafana-dashboards](t-20261113-r28-grafana-dashboards.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Implement a small provider/Target-aware dashboard catalog selection that enables only dashboard templates whose required metrics+labels were verified on the selected Prometheus target. Missing signals never instantiate misleading dashboards. Source of truth is existing provider registry + descriptor/observability status, not guessed container names.

## Acceptance

Unit tests prove eligible vs missing metric/label vs unauthorized provider vs changed Target; return explicit no-data/needs-exporter rather than fake health. Use accepted provider seam.

## Exact source entry points

`internal/capability/integration_contract.go` (provider observability), `internal/capability/reference.go` (per-provider signals), `internal/application/provider_registry.go` (real instances and scope), `internal/metrics/prometheus.go` (Prometheus), `internal/logs/driver.go` (Loki), `internal/traces/tempo.go` (Tempo). Use accepted 0428-033 verified matrix; do not interpret descriptor support as collected live data. Source dashboard revisions/JSON pin/checksum when importing; adapt dashboard queries to actual authenticated labels, not the reverse.

## Exclusive file ownership and minimal worker procedure

New isolated internal/grafana/dashboards/catalog* files and focused tests; no existing provider runtime or shared CLI edits.

Read this card, named exact files, accepted predecessor contracts and relevant tests only. Do NOT load whole repo. Check current source HEAD. One narrow feature change and tests; no new runtime collector, no cross-Target data, no unverified dashboard import. Show positive and negative test, source-change CI route, actual run/check result, PR HEAD. Codex reviews/merges; Coordinator updates accepted Kanban, max five non-overlapping workers.

## Handoff

Not started.

## Binding current-code reference

Read `internal/application/provider_registry.go`, `internal/capability/integration_contract.go`, `internal/capability/reference.go`, and accepted 0428-033 signal matrix. Only real metric names and labels permit template selection, not a declared provider alone.

Worker must verify path and source at current exact commit, not assume any pre-existing proof means live readiness. Codex reviews source-specific tests and CI routing.
