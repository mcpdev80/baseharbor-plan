---
id: t-20261114-r28-perses-native-proof
card_number: "0428-087"
card_short_title: "Prove Perses native monitoring"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Qualify exact integrated Perses candidate using real verified metric/log/trace signals, secured access and approved alert…"
kanban_title: 0428-087 · Prove Perses native monitoring
priority: normal
depends_on: [t-20261017-release-0-4-28-updates, t-20261114-r28-perses-alerts, t-20261114-r28-perses-contact-routing, t-20261114-r28-perses-dashboard-databases, t-20261114-r28-perses-dashboard-hosts, t-20261114-r28-perses-dashboard-identity, t-20261114-r28-perses-dashboard-messaging, t-20261114-r28-perses-dashboard-valkey, t-20261114-r28-perses-dashboards, t-20261114-r28-perses-lifecycle, t-20261114-r28-perses-log-trace-dash, t-20261114-r28-perses-loki-source, t-20261114-r28-perses-secure-access, t-20261114-r28-perses-tempo-source]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261114-r28-perses-native-proof · Prove Perses native monitoring #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261114-r28-perses-alerts](t-20261114-r28-perses-alerts.md), [t-20261114-r28-perses-contact-routing](t-20261114-r28-perses-contact-routing.md), [t-20261114-r28-perses-dashboard-databases](t-20261114-r28-perses-dashboard-databases.md), [t-20261114-r28-perses-dashboard-hosts](t-20261114-r28-perses-dashboard-hosts.md), [t-20261114-r28-perses-dashboard-identity](t-20261114-r28-perses-dashboard-identity.md), [t-20261114-r28-perses-dashboard-messaging](t-20261114-r28-perses-dashboard-messaging.md), [t-20261114-r28-perses-dashboard-valkey](t-20261114-r28-perses-dashboard-valkey.md), [t-20261114-r28-perses-dashboards](t-20261114-r28-perses-dashboards.md), [t-20261114-r28-perses-lifecycle](t-20261114-r28-perses-lifecycle.md), [t-20261114-r28-perses-log-trace-dash](t-20261114-r28-perses-log-trace-dash.md), [t-20261114-r28-perses-loki-source](t-20261114-r28-perses-loki-source.md), [t-20261114-r28-perses-secure-access](t-20261114-r28-perses-secure-access.md), [t-20261114-r28-perses-tempo-source](t-20261114-r28-perses-tempo-source.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261114-r28-perses-alerts](t-20261114-r28-perses-alerts.md), [t-20261114-r28-perses-contact-routing](t-20261114-r28-perses-contact-routing.md), [t-20261114-r28-perses-dashboard-databases](t-20261114-r28-perses-dashboard-databases.md), [t-20261114-r28-perses-dashboard-hosts](t-20261114-r28-perses-dashboard-hosts.md), [t-20261114-r28-perses-dashboard-identity](t-20261114-r28-perses-dashboard-identity.md), [t-20261114-r28-perses-dashboard-messaging](t-20261114-r28-perses-dashboard-messaging.md), [t-20261114-r28-perses-dashboard-valkey](t-20261114-r28-perses-dashboard-valkey.md), [t-20261114-r28-perses-dashboards](t-20261114-r28-perses-dashboards.md), [t-20261114-r28-perses-lifecycle](t-20261114-r28-perses-lifecycle.md), [t-20261114-r28-perses-log-trace-dash](t-20261114-r28-perses-log-trace-dash.md), [t-20261114-r28-perses-loki-source](t-20261114-r28-perses-loki-source.md), [t-20261114-r28-perses-secure-access](t-20261114-r28-perses-secure-access.md), [t-20261114-r28-perses-tempo-source](t-20261114-r28-perses-tempo-source.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Qualify exact integrated Perses candidate using real verified metric/log/trace signals, secured access and approved alert architecture on isolated supported Docker and rootless Podman.

## Scope and file ownership

Independent integration evidence, no fake data claimed as production, no archived external repos. Inspect the current Core source before implementing; use existing provider/capability, ownership, TLS and lifecycle contracts. Coordinate shared registry, CLI, CI and generated docs with their owners. Preserve unrelated work.

## Verified starting points and bounded implementation

All referenced paths exist at Core `cd77e20e`; fetch actual current `develop` and recheck behavior before editing. Do not treat this static reference as a runtime proof.

- [.github/workflows/observability-acceptance.yml](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/.github/workflows/observability-acceptance.yml)
- [internal/metrics/prometheus_test.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/prometheus_test.go)
- [internal/logs/loki_integration_test.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/logs/loki_integration_test.go)
- [internal/traces/tempo_integration_test.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/traces/tempo_integration_test.go)

After all predecessors, run exact-SHA isolated native Docker and rootless Podman tests: opt-in/install readiness, auth denial, real Prometheus/Loki/Tempo data for enabled sources, first dashboards, approved alert path, removal and retention. Skips are not passes; archived public Connector is not a prerequisite.

## Acceptance

- Use a verified, pinned Perses release and native plugin/format where applicable; do not assume Grafana UI APIs or dashboard JSON are Perses-compatible. Verify real provider signals and mark missing/unsupported coverage explicitly.
- Scope all access by actual Target/tenant permissions, fail closed on unknown ownership or missing authorization, and keep secrets out of logs, manifests and audit. Optional visualization must not force new application capabilities or mandatory services.
- Preserve independent Prometheus, Loki and Tempo backend ownership; remove only owned resources. Qualify exact integrated Perses candidate using real verified metric/log/trace signals, secured access and approved alert architecture on isolated supported Docker and rootless Podman.
- For alerting, define the real rule evaluator and notification owner in the approved contract. Do not claim native Perses alerting/routing parity without evidence, nor enable external notifications by default.

## Required checks

Record exact candidate SHA and focused tests by name. Route every changed test through an existing CI check/native gate with trigger and actual execution; no skipped/faked native proof. Require isolated Docker and rootless Podman only when runtime risk requires them; no blanket full matrix. Produce deterministic negative/authorization/ownership tests as appropriate.

## Dependencies and handoff

Prerequisites are encoded in `depends_on`. One worker per card/branch/PR, no concurrent writes to shared files. Codex/Owner-delegated Maintainer reviews and merges only after real checks; no independent-review claim. Archive Console/Node Connector repos are excluded. No implementation or release has occurred.

Supersedes [t-20261113-r28-grafana-native-proof](t-20261113-r28-grafana-native-proof.md) under the [Owner decision](../decisions/2026-11-14-perses-replaces-grafana-v0428.md).
