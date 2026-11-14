---
id: t-20261114-r28-perses-runtime
card_number: "0428-088"
card_short_title: "Launch optional Perses"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Implement explicitly enabled optional Perses runtime, pinned reviewed image/plugin versions, lifecycle and safe storage using…"
kanban_title: 0428-088 · Launch optional Perses
priority: normal
depends_on: [t-20261114-r28-perses-contract-seam]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261114-r28-perses-runtime · Launch optional Perses #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Waiting for prerequisites**  
    **Needs:** [t-20261114-r28-perses-contract-seam](t-20261114-r28-perses-contract-seam.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-perses-contract-seam](t-20261114-r28-perses-contract-seam.md)  
**Required by:** [t-20261114-r28-perses-datasources](t-20261114-r28-perses-datasources.md), [t-20261114-r28-perses-lifecycle](t-20261114-r28-perses-lifecycle.md), [t-20261114-r28-perses-loki-source](t-20261114-r28-perses-loki-source.md), [t-20261114-r28-perses-secure-access](t-20261114-r28-perses-secure-access.md), [t-20261114-r28-perses-tempo-source](t-20261114-r28-perses-tempo-source.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Implement explicitly enabled optional Perses runtime, pinned reviewed image/plugin versions, lifecycle and safe storage using the existing runtime/provider seam.

## Scope and file ownership

Own dedicated Perses runtime assets and tests; do not provision unrelated telemetry backends. Inspect the current Core source before implementing; use existing provider/capability, ownership, TLS and lifecycle contracts. Coordinate shared registry, CLI, CI and generated docs with their owners. Preserve unrelated work.

## Verified starting points and bounded implementation

All referenced paths exist at Core `cd77e20e`; fetch actual current `develop` and recheck behavior before editing. Do not treat this static reference as a runtime proof.

- [internal/providerui/application.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/providerui/application.go)
- [internal/metrics/prometheus_render.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/prometheus_render.go)
- [internal/metrics/prometheus_files.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/prometheus_files.go)
- [internal/deployment/runtime_provider.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/deployment/runtime_provider.go)

Use the accepted seam to implement an opt-in owned Perses runtime with verified immutable image and required plugin availability, protected persistent/config state and real readiness. Normal applications must not create Perses. Missing image/security policy must fail closed. Add removal/restart/foreign-owner tests.

## Acceptance

- Use a verified, pinned Perses release and native plugin/format where applicable; do not assume Grafana UI APIs or dashboard JSON are Perses-compatible. Verify real provider signals and mark missing/unsupported coverage explicitly.
- Scope all access by actual Target/tenant permissions, fail closed on unknown ownership or missing authorization, and keep secrets out of logs, manifests and audit. Optional visualization must not force new application capabilities or mandatory services.
- Preserve independent Prometheus, Loki and Tempo backend ownership; remove only owned resources. Implement explicitly enabled optional Perses runtime, pinned reviewed image/plugin versions, lifecycle and safe storage using the existing runtime/provider seam.
- For alerting, define the real rule evaluator and notification owner in the approved contract. Do not claim native Perses alerting/routing parity without evidence, nor enable external notifications by default.

## Required checks

Record exact candidate SHA and focused tests by name. Route every changed test through an existing CI check/native gate with trigger and actual execution; no skipped/faked native proof. Require isolated Docker and rootless Podman only when runtime risk requires them; no blanket full matrix. Produce deterministic negative/authorization/ownership tests as appropriate.

## Dependencies and handoff

Prerequisites are encoded in `depends_on`. One worker per card/branch/PR, no concurrent writes to shared files. Codex/Owner-delegated Maintainer reviews and merges only after real checks; no independent-review claim. Archive Console/Node Connector repos are excluded. No implementation or release has occurred.

Supersedes [t-20261113-r28-grafana-runtime](t-20261113-r28-grafana-runtime.md) under the [Owner decision](../decisions/2026-11-14-perses-replaces-grafana-v0428.md).
