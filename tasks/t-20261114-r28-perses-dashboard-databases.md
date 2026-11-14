---
id: t-20261114-r28-perses-dashboard-databases
card_number: "0428-076"
card_short_title: "Perses database dashboards"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: Deliver PostgreSQL/MongoDB panels only when verified compatible metrics and permissions exist.
kanban_title: 0428-076 · Perses database dashboards
priority: normal
depends_on: [t-20261114-r28-perses-dashboard-selection]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261114-r28-perses-dashboard-databases · Perses database dashboards #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Waiting for prerequisites**  
    **Needs:** [t-20261114-r28-perses-dashboard-selection](t-20261114-r28-perses-dashboard-selection.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-perses-dashboard-selection](t-20261114-r28-perses-dashboard-selection.md)  
**Required by:** [t-20261114-r28-perses-native-proof](t-20261114-r28-perses-native-proof.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Deliver PostgreSQL/MongoDB panels only when verified compatible metrics and permissions exist.

## Scope and file ownership

Own database dashboard assets and focused tests. Inspect the current Core source before implementing; use existing provider/capability, ownership, TLS and lifecycle contracts. Coordinate shared registry, CLI, CI and generated docs with their owners. Preserve unrelated work.

## Verified starting points and bounded implementation

All referenced paths exist at Core `cd77e20e`; fetch actual current `develop` and recheck behavior before editing. Do not treat this static reference as a runtime proof.

- [internal/capability/reference.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/capability/reference.go)
- [internal/application/provider_registry.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/application/provider_registry.go)
- [internal/metrics/prometheus_files.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/prometheus_files.go)

Create first PostgreSQL/MongoDB panels using only verified actual exporters/labels. Each unsupported database must remain explicitly unavailable; no silent exporter install. Validate real data/no-data per supported fixture.

## Acceptance

- Use a verified, pinned Perses release and native plugin/format where applicable; do not assume Grafana UI APIs or dashboard JSON are Perses-compatible. Verify real provider signals and mark missing/unsupported coverage explicitly.
- Scope all access by actual Target/tenant permissions, fail closed on unknown ownership or missing authorization, and keep secrets out of logs, manifests and audit. Optional visualization must not force new application capabilities or mandatory services.
- Preserve independent Prometheus, Loki and Tempo backend ownership; remove only owned resources. Deliver PostgreSQL/MongoDB panels only when verified compatible metrics and permissions exist.
- For alerting, define the real rule evaluator and notification owner in the approved contract. Do not claim native Perses alerting/routing parity without evidence, nor enable external notifications by default.

## Required checks

Record exact candidate SHA and focused tests by name. Route every changed test through an existing CI check/native gate with trigger and actual execution; no skipped/faked native proof. Require isolated Docker and rootless Podman only when runtime risk requires them; no blanket full matrix. Produce deterministic negative/authorization/ownership tests as appropriate.

## Dependencies and handoff

Prerequisites are encoded in `depends_on`. One worker per card/branch/PR, no concurrent writes to shared files. Codex/Owner-delegated Maintainer reviews and merges only after real checks; no independent-review claim. Archive Console/Node Connector repos are excluded. No implementation or release has occurred.

Supersedes [t-20261113-r28-grafana-dashboard-databases](t-20261113-r28-grafana-dashboard-databases.md) under the [Owner decision](../decisions/2026-11-14-perses-replaces-grafana-v0428.md).
