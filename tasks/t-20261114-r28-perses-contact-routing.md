---
id: t-20261114-r28-perses-contact-routing
card_number: "0428-074"
card_short_title: "Define alert notification"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: coord
kanban_status: wait
kanban_lane: wait
kanban_summary: Implement opt-in alert notification routing. No route configured means no external notification leaves the system. First…
kanban_title: 0428-074 · Define alert notification
priority: normal
depends_on: [t-20261114-r28-perses-alerts, t-20261114-r28-perses-secure-access]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: "Owner-Entscheidung queue-124 umgesetzt und geschlossen: opt-in-Routing ohne externe Benachrichtigung per Default. Begonnener Entwurf wartet auf die Abnahme von 0428-073; die Kompatibilitätsprüfung des vorhandenen Alertmanager kann parallel erfolgen."
resolution: ""
evidence: []
---

- [ ] t-20261114-r28-perses-contact-routing · Define alert notification routing #task #release/v0-4-28 #status/wait #view/wait #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** coord · **Priority:** normal  
    **Waiting:** Owner-Entscheidung queue-124 umgesetzt und geschlossen: opt-in-Routing ohne externe Benachrichtigung per Default. Begonnener Entwurf wartet auf die Abnahme von 0428-073; die Kompatibilitätsprüfung des vorhandenen Alertmanager kann parallel…  
    **Needs:** [t-20261114-r28-perses-alerts](t-20261114-r28-perses-alerts.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-perses-alerts](t-20261114-r28-perses-alerts.md), [t-20261114-r28-perses-secure-access](t-20261114-r28-perses-secure-access.md)  
**Required by:** [t-20261114-r28-perses-native-proof](t-20261114-r28-perses-native-proof.md)  
**Owner:** coord  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Implement opt-in alert notification routing. No route configured means no external notification leaves the system. First evaluate whether the existing Alertmanager integration is compatible; do not assume Alertmanager is present or add infrastructure by default. The routing contract is independent of operator access.

## Scope and file ownership

Own routing integration/tests; do not assume Alertmanager exists or default external notification. Inspect the current Core source before implementing; use existing provider/capability, ownership, TLS and lifecycle contracts. Coordinate shared registry, CLI, CI and generated docs with their owners. Preserve unrelated work.

## Verified starting points and bounded implementation

All referenced paths exist at Core `cd77e20e`; fetch actual current `develop` and recheck behavior before editing. Do not treat this static reference as a runtime proof.

- [internal/serviceaccess/policy.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/serviceaccess/policy.go)
- [internal/openbao/application_scope.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/openbao/application_scope.go)
- [internal/metrics/prometheus_render.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/prometheus_render.go)

Inspect the current Core and Prometheus integration for an existing compatible Alertmanager. If present, use it with explicit opt-in routing and existing authorization, secret-reference, TLS and lifecycle rules. If absent or incompatible, do not add a service: keep outbound delivery disabled and report the precise missing contract. Verify configured delivery with a bounded test receiver; never configure an external route by default.

## Acceptance

- Use a verified, pinned Perses release and native plugin/format where applicable; do not assume Grafana UI APIs or dashboard JSON are Perses-compatible. Verify real provider signals and mark missing/unsupported coverage explicitly.
- Scope all access by actual Target/tenant permissions, fail closed on unknown ownership or missing authorization, and keep secrets out of logs, manifests and audit. Optional visualization must not force new application capabilities or mandatory services.
- Preserve independent Prometheus, Loki and Tempo backend ownership; remove only owned resources. Design opt-in notification routing, evaluate existing compatible Alertmanager integration first; preserve authorization and secret-safe configuration.
- For alerting, define the real rule evaluator and notification owner in the approved contract. Do not claim native Perses alerting/routing parity without evidence, nor enable external notifications by default.

## Required checks

Record exact candidate SHA and focused tests by name. Route every changed test through an existing CI check/native gate with trigger and actual execution; no skipped/faked native proof. Require isolated Docker and rootless Podman only when runtime risk requires them; no blanket full matrix. Produce deterministic negative/authorization/ownership tests as appropriate.

## Owner decision — queue-124 (2026-11-20)

Resolved: routing is opt-in; no configured route means nothing leaves the system. First inspect the existing Alertmanager integration for compatibility; do not assume it exists or introduce it as new infrastructure. Design may proceed in parallel, while implementation waits for 0428-073.

## Dependencies and handoff

Prerequisites are encoded in `depends_on`. One worker per card/branch/PR, no concurrent writes to shared files. Codex/Owner-delegated Maintainer reviews and merges only after real checks; no independent-review claim. Archive Console/Node Connector repos are excluded. No implementation or release has occurred.

Supersedes [t-20261113-r28-grafana-contact-routing](t-20261113-r28-grafana-contact-routing.md) under the [Owner decision](../decisions/2026-11-14-perses-replaces-grafana-v0428.md).
