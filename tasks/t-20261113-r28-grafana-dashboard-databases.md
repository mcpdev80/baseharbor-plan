---
id: t-20261113-r28-grafana-dashboard-databases
card_number: "0428-036"
card_short_title: "Qualify database dashboard pan"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Evaluate PostgreSQL Dashboard 9628 (https://grafana.com/grafana/dashboards/9628-postgresql-database/) and MongoDB Dashboard…"
kanban_title: 0428-036 · Qualify database dashboard pan
priority: high
depends_on: [t-20261017-release-0-4-28-updates, t-20261113-r28-grafana-dashboard-selection]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261113-r28-grafana-dashboard-databases · Qualify database dashboard panels #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261113-r28-grafana-dashboard-selection](t-20261113-r28-grafana-dashboard-selection.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261113-r28-grafana-dashboard-selection](t-20261113-r28-grafana-dashboard-selection.md)  
**Required by:** [t-20261113-r28-grafana-native-proof](t-20261113-r28-grafana-native-proof.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Evaluate PostgreSQL Dashboard 9628 (https://grafana.com/grafana/dashboards/9628-postgresql-database/) and MongoDB Dashboard 25802 (https://grafana.com/grafana/dashboards/25802-mongodb-replica-set-full-overview/). Both depend on specific exporters. Import/pin only if deployed provider exposes actual compatible metric names/labels and selected scope is authorized. Never provision exporters silently.

## Acceptance

For each supported exporter, one live metric graph and no-data proof; provider absent or exporter missing leaves dashboard unavailable, with precise prerequisite rather than fabricated values.

## Exact source entry points

`internal/capability/integration_contract.go` (provider observability), `internal/capability/reference.go` (per-provider signals), `internal/application/provider_registry.go` (real instances and scope), `internal/metrics/prometheus.go` (Prometheus), `internal/logs/driver.go` (Loki), `internal/traces/tempo.go` (Tempo). Use accepted 0428-033 verified matrix; do not interpret descriptor support as collected live data. Source dashboard revisions/JSON pin/checksum when importing; adapt dashboard queries to actual authenticated labels, not the reverse.

## Exclusive file ownership and minimal worker procedure

New internal/grafana/dashboards/databases* assets/tests only.

Read this card, named exact files, accepted predecessor contracts and relevant tests only. Do NOT load whole repo. Check current source HEAD. One narrow feature change and tests; no new runtime collector, no cross-Target data, no unverified dashboard import. Show positive and negative test, source-change CI route, actual run/check result, PR HEAD. Codex reviews/merges; Coordinator updates accepted Kanban, max five non-overlapping workers.

## Handoff

Not started.
