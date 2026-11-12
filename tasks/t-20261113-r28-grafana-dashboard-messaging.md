---
id: t-20261113-r28-grafana-dashboard-messaging
card_number: "0428-037"
card_short_title: "Qualify RabbitMQ dashboard"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Evaluate Grafana dashboard RabbitMQ-Overview 10991 (https://grafana.com/grafana/dashboards/10991-rabbitmq-overview/"
kanban_title: "0428-037 · Qualify RabbitMQ dashboard"
priority: high
depends_on: [t-20261113-r28-grafana-dashboard-selection]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261113-r28-grafana-dashboard-messaging · Qualify RabbitMQ dashboard #task #release/v0-4-28 #status/planned #area/observability #kind/task

## Goal

Evaluate Grafana dashboard RabbitMQ-Overview 10991 (https://grafana.com/grafana/dashboards/10991-rabbitmq-overview/) against real RabbitMQ management Prometheus plugin output, current labels and target scope; do not assume any plugin/exporter enabled.

## Acceptance

If enabled and compatible, show real queues/message rates; absent/unsupported metric produces explicit unavailable panel/template; no unauthenticated RabbitMQ metrics port.

## Exact source entry points

`internal/capability/integration_contract.go` (provider observability), `internal/capability/reference.go` (per-provider signals), `internal/application/provider_registry.go` (real instances and scope), `internal/metrics/prometheus.go` (Prometheus), `internal/logs/driver.go` (Loki), `internal/traces/tempo.go` (Tempo). Use accepted 0428-033 verified matrix; do not interpret descriptor support as collected live data. Source dashboard revisions/JSON pin/checksum when importing; adapt dashboard queries to actual authenticated labels, not the reverse.

## Exclusive file ownership and minimal worker procedure

New internal/grafana/dashboards/rabbitmq* assets/tests only.

Read this card, named exact files, accepted predecessor contracts and relevant tests only. Do NOT load whole repo. Check current source HEAD. One narrow feature change and tests; no new runtime collector, no cross-Target data, no unverified dashboard import. Show positive and negative test, source-change CI route, actual run/check result, PR HEAD. Codex reviews/merges; Coordinator updates accepted Kanban, max five non-overlapping workers.

## Handoff

Not started.
