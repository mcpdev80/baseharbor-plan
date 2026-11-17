---
id: t-20261114-r28-perses-dashboard-selection
card_number: "0428-080"
card_short_title: "Select compatible Perses"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: coord
kanban_status: closed
kanban_lane: closed
kanban_summary: Define eligibility and provisioning for Perses-native dashboards based on real signal/label inventory and authorized providers.
kanban_title: 0428-080 · Select compatible Perses
priority: normal
depends_on: [t-20261114-r28-perses-contract-seam, t-20261114-r28-perses-signal-inventory]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1590]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/perses-dashboard-selection/merge-1.md", "https://github.com/mcpdev80/baseharbor/pull/1590", "https://github.com/mcpdev80/baseharbor/actions/runs/44040693658", "https://github.com/mcpdev80/baseharbor/commit/4094448543359a13ba312119304f1f70d3bc40a9"]
---

- [x] t-20261114-r28-perses-dashboard-selection · Select compatible Perses dashboards #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** coord · **Priority:** normal  
    **PR:** [baseharbor#1590](https://github.com/mcpdev80/baseharbor/pull/1590)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/perses-dashboard-selection/merge-1.md), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1590), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44040693658), [proof 4](https://github.com/mcpdev80/baseharbor/commit/4094448543359a13ba312119304f1f70d3bc40a9)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-perses-contract-seam](t-20261114-r28-perses-contract-seam.md), [t-20261114-r28-perses-signal-inventory](t-20261114-r28-perses-signal-inventory.md)  
**Required by:** [t-20261114-r28-perses-dashboard-databases](t-20261114-r28-perses-dashboard-databases.md), [t-20261114-r28-perses-dashboard-hosts](t-20261114-r28-perses-dashboard-hosts.md), [t-20261114-r28-perses-dashboard-identity](t-20261114-r28-perses-dashboard-identity.md), [t-20261114-r28-perses-dashboard-messaging](t-20261114-r28-perses-dashboard-messaging.md), [t-20261114-r28-perses-dashboard-valkey](t-20261114-r28-perses-dashboard-valkey.md), [t-20261114-r28-perses-dashboards](t-20261114-r28-perses-dashboards.md)  
**Owner:** coord  
**Priority:** normal  
**PRs:** [baseharbor#1590](https://github.com/mcpdev80/baseharbor/pull/1590)  
**Source:** 
<!-- /generated:links -->

## Goal

Define eligibility and provisioning for Perses-native dashboards based on real signal/label inventory and authorized providers.

## Scope and file ownership

Dedicated selection code, versioned templates and tests; no implicit exporter enablement. Inspect the current Core source before implementing; use existing provider/capability, ownership, TLS and lifecycle contracts. Coordinate shared registry, CLI, CI and generated docs with their owners. Preserve unrelated work.

## Verified starting points and bounded implementation

All referenced paths exist at Core `cd77e20e`; fetch actual current `develop` and recheck behavior before editing. Do not treat this static reference as a runtime proof.

- [internal/capability/integration_contract.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/capability/integration_contract.go)
- [internal/capability/reference.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/capability/reference.go)
- [internal/application/provider_registry.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/application/provider_registry.go)
- [internal/metrics/prometheus_verify.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/prometheus_verify.go)
- [internal/metrics/prometheus_files.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/prometheus_files.go)

Define small dashboard selection catalog keyed by accepted Perses version and real provider/label/permission requirements. Test matching and missing metrics, unauthorized providers, other Targets and stale registry. Do not imply all exporter types exist.

## Acceptance

- Use a verified, pinned Perses release and native plugin/format where applicable; do not assume Grafana UI APIs or dashboard JSON are Perses-compatible. Verify real provider signals and mark missing/unsupported coverage explicitly.
- Scope all access by actual Target/tenant permissions, fail closed on unknown ownership or missing authorization, and keep secrets out of logs, manifests and audit. Optional visualization must not force new application capabilities or mandatory services.
- Preserve independent Prometheus, Loki and Tempo backend ownership; remove only owned resources. Define eligibility and provisioning for Perses-native dashboards based on real signal/label inventory and authorized providers.
- For alerting, define the real rule evaluator and notification owner in the approved contract. Do not claim native Perses alerting/routing parity without evidence, nor enable external notifications by default.

## Required checks

Record exact candidate SHA and focused tests by name. Route every changed test through an existing CI check/native gate with trigger and actual execution; no skipped/faked native proof. Require isolated Docker and rootless Podman only when runtime risk requires them; no blanket full matrix. Produce deterministic negative/authorization/ownership tests as appropriate.

## Dependencies and handoff

Prerequisites are encoded in `depends_on`. One worker per card/branch/PR, no concurrent writes to shared files. Codex/Owner-delegated Maintainer reviews and merges only after real checks; no independent-review claim. Archive Console/Node Connector repos are excluded. No implementation or release has occurred.

Supersedes [t-20261113-r28-grafana-dashboard-selection](t-20261113-r28-grafana-dashboard-selection.md) under the [Owner decision](../decisions/2026-11-14-perses-replaces-grafana-v0428.md).
