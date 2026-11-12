---
id: t-20261113-r28-grafana-dashboard-valkey
card_number: "0428-038"
card_short_title: "Qualify Valkey dashboard"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Selectively adapt Grafana Redis exporter dashboard 763 (https://grafana.com/grafana/dashboards/763-redis-dashb"
kanban_title: "0428-038 · Qualify Valkey dashboard"
priority: normal
depends_on: [t-20261017-release-0-4-28-updates, t-20261113-r28-grafana-dashboard-selection]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261113-r28-grafana-dashboard-valkey · Qualify Valkey dashboard #task #release/v0-4-28 #status/planned #area/observability #kind/task

## Goal

Selectively adapt Grafana Redis exporter dashboard 763 (https://grafana.com/grafana/dashboards/763-redis-dashboard-for-prometheus-redis-exporter-1-x/) for Valkey only when actual compatible Redis/Valkey exporter metrics, selected instance labels and authorized Target are present. Do not start redis_exporter or relax network privileges automatically.

## Acceptance

Selected Valkey with real compatible metrics yields real memory/client/command graphs; absent exporter or unsupported labels hides template with reason. Validate metric query and negative authorization.

## Exclusive ownership, current source and worker instructions

Only `internal/grafana/dashboards/valkey*` assets and tests. Read `internal/capability/reference.go`, `internal/application/provider_registry.go`, accepted 0428-033 signals; no provider backend changes.

Worker reads only named paths at exact current Core SHA, accepted predecessors and direct tests. One narrow PR; report test name -> selected CI job -> source trigger -> exact successful assertion, and denial/no-data case. Missing exporter is a legitimate unsupported state, not a license to expand scope. Coordinator assigns at most five disjoint workers; Codex independently reviews and merges.

## Handoff

Not started.
