---
id: t-20261113-r28-grafana-signal-inventory
card_number: "0428-033"
card_short_title: "Audit real dashboard signals"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Inspect real current Core source and provider descriptors to build a signal inventory for Prometheus, Loki and Tempo. Determine…"
kanban_title: "0428-033 · Audit real dashboard signals"
priority: high
depends_on: [t-20261017-release-0-4-28-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261113-r28-grafana-signal-inventory · Audit real dashboard signals #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md)  
**Required by:** [t-20261113-r28-grafana-dashboard-selection](t-20261113-r28-grafana-dashboard-selection.md), [t-20261113-r28-grafana-datasources](t-20261113-r28-grafana-datasources.md), [t-20261113-r28-grafana-loki-source](t-20261113-r28-grafana-loki-source.md), [t-20261113-r28-grafana-tempo-source](t-20261113-r28-grafana-tempo-source.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Inspect real current Core source and provider descriptors to build a signal inventory for Prometheus, Loki and Tempo. Determine exporter/scrape/labels exactly; Node Exporter, cAdvisor, postgres_exporter, RabbitMQ, MongoDB and Valkey exporters are NOT assumed present.

## Acceptance

Deliver matrix provider -> signal family -> metric names/labels -> actual producer -> currently discovered? -> scrape/retention -> eligibility -> test/CI. Mark missing signals unsupported, no invented exporter; no code changes.

## Exact source entry points

`internal/capability/integration_contract.go` (provider observability), `internal/capability/reference.go` (per-provider signals), `internal/application/provider_registry.go` (real instances and scope), `internal/metrics/prometheus.go` (Prometheus), `internal/logs/driver.go` (Loki), `internal/traces/tempo.go` (Tempo). Use accepted 0428-033 verified matrix; do not interpret descriptor support as collected live data. Source dashboard revisions/JSON pin/checksum when importing; adapt dashboard queries to actual authenticated labels, not the reverse.

## Exclusive file ownership and minimal worker procedure

docs/internal/v0.4.28-grafana-signal-matrix.md (new) and this card only; read internal/metrics/, internal/logs/, internal/traces/, internal/capability/reference.go, internal/application/runtime_telemetry.go and current tests.

Read this card, named exact files, accepted predecessor contracts and relevant tests only. Do NOT load whole repo. Check current source HEAD. One narrow feature change and tests; no new runtime collector, no cross-Target data, no unverified dashboard import. Show positive and negative test, source-change CI route, actual run/check result, PR HEAD. Codex reviews/merges; Coordinator updates accepted Kanban, max five non-overlapping workers.

## Handoff

Not started.
