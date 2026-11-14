---
id: t-20261114-r28-perses-log-trace-dash
card_number: "0428-085"
card_short_title: "Perses log and trace views"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: Provide native Perses log/trace dashboards using validated Loki/Tempo plugin versions and actual telemetry.
kanban_title: 0428-085 · Perses log and trace views
priority: normal
depends_on: [t-20261114-r28-perses-loki-source, t-20261114-r28-perses-tempo-source]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261114-r28-perses-log-trace-dash · Perses log and trace views #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Waiting for prerequisites**  
    **Needs:** [t-20261114-r28-perses-loki-source](t-20261114-r28-perses-loki-source.md), [t-20261114-r28-perses-tempo-source](t-20261114-r28-perses-tempo-source.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-perses-loki-source](t-20261114-r28-perses-loki-source.md), [t-20261114-r28-perses-tempo-source](t-20261114-r28-perses-tempo-source.md)  
**Required by:** [t-20261114-r28-perses-native-proof](t-20261114-r28-perses-native-proof.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Provide native Perses log/trace dashboards using validated Loki/Tempo plugin versions and actual telemetry.

## Scope and file ownership

Own log/trace dashboard assets and focused tests. Inspect the current Core source before implementing; use existing provider/capability, ownership, TLS and lifecycle contracts. Coordinate shared registry, CLI, CI and generated docs with their owners. Preserve unrelated work.

## Verified starting points and bounded implementation

All referenced paths exist at Core `cd77e20e`; fetch actual current `develop` and recheck behavior before editing. Do not treat this static reference as a runtime proof.

- [internal/logs/query.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/logs/query.go)
- [internal/traces/tempo.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/traces/tempo.go)
- [internal/metrics/prometheus_files.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/prometheus_files.go)

Create first actual log/trace views using supported Perses plugins and authorized Loki/Tempo data; include meaningful no-data and verify real query results on fixtures. No placeholder dashboard counted as done.

## Acceptance

- Use a verified, pinned Perses release and native plugin/format where applicable; do not assume Grafana UI APIs or dashboard JSON are Perses-compatible. Verify real provider signals and mark missing/unsupported coverage explicitly.
- Scope all access by actual Target/tenant permissions, fail closed on unknown ownership or missing authorization, and keep secrets out of logs, manifests and audit. Optional visualization must not force new application capabilities or mandatory services.
- Preserve independent Prometheus, Loki and Tempo backend ownership; remove only owned resources. Provide native Perses log/trace dashboards using validated Loki/Tempo plugin versions and actual telemetry.
- For alerting, define the real rule evaluator and notification owner in the approved contract. Do not claim native Perses alerting/routing parity without evidence, nor enable external notifications by default.

## Required checks

Record exact candidate SHA and focused tests by name. Route every changed test through an existing CI check/native gate with trigger and actual execution; no skipped/faked native proof. Require isolated Docker and rootless Podman only when runtime risk requires them; no blanket full matrix. Produce deterministic negative/authorization/ownership tests as appropriate.

## Dependencies and handoff

Prerequisites are encoded in `depends_on`. One worker per card/branch/PR, no concurrent writes to shared files. Codex/Owner-delegated Maintainer reviews and merges only after real checks; no independent-review claim. Archive Console/Node Connector repos are excluded. No implementation or release has occurred.

Supersedes [t-20261113-r28-grafana-log-trace-dash](t-20261113-r28-grafana-log-trace-dash.md) under the [Owner decision](../decisions/2026-11-14-perses-replaces-grafana-v0428.md).
