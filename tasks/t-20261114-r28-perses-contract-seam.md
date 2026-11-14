---
id: t-20261114-r28-perses-contract-seam
card_number: "0428-075"
card_short_title: "Define Perses Prov seam"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: Specify optional Perses management/visualization through the existing provider and authorization boundaries; never falsely…
kanban_title: 0428-075 · Define Perses Prov seam
priority: normal
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261114-r28-perses-contract-seam · Define Perses provider seam #task #release/v0-4-28 #status/planned #view/ready #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Required by:** [t-20261114-r28-perses-dashboard-selection](t-20261114-r28-perses-dashboard-selection.md), [t-20261114-r28-perses-datasources](t-20261114-r28-perses-datasources.md), [t-20261114-r28-perses-lifecycle](t-20261114-r28-perses-lifecycle.md), [t-20261114-r28-perses-loki-source](t-20261114-r28-perses-loki-source.md), [t-20261114-r28-perses-runtime](t-20261114-r28-perses-runtime.md), [t-20261114-r28-perses-secure-access](t-20261114-r28-perses-secure-access.md), [t-20261114-r28-perses-tempo-source](t-20261114-r28-perses-tempo-source.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Specify optional Perses management/visualization through the existing provider and authorization boundaries; never falsely declare metrics/logs/traces application capabilities. Pin version, container/plugins and supported provisioning/upgrade/security contract.

## Scope and file ownership

Review Core provider registry, management UI, service-access policies and Perses upstream docs; no container lifecycle implementation. Inspect the current Core source before implementing; use existing provider/capability, ownership, TLS and lifecycle contracts. Coordinate shared registry, CLI, CI and generated docs with their owners. Preserve unrelated work.

## Verified starting points and bounded implementation

All referenced paths exist at Core `cd77e20e`; fetch actual current `develop` and recheck behavior before editing. Do not treat this static reference as a runtime proof.

- [internal/capability/integration_contract.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/capability/integration_contract.go)
- [internal/capability/reference.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/capability/reference.go)
- [internal/application/provider_registry.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/application/provider_registry.go)
- [docs/spec/provider-contract-v1.md](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/docs/spec/provider-contract-v1.md)
- [internal/capability/domain.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/capability/domain.go)
- [internal/capability/service.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/capability/service.go)
- [internal/provider/builtin/catalog.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/provider/builtin/catalog.go)
- [internal/provider/authoring/descriptor.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/provider/authoring/descriptor.go)
- [internal/metrics/management_ui.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/management_ui.go)
- [internal/application/management_ui.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/application/management_ui.go)
- [internal/providerui/application.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/providerui/application.go)
- [cmd/baha/app_dev_routing.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/cmd/baha/app_dev_routing.go)

Decide a concrete provider-owned optional management-tool representation compatible with existing Provider Contract v1 and catalog/registry distinction. `IntegrationDescriptor.Validate` requires a real capability/specification: do not fake metrics/logs/traces implementation or silently replace Prometheus management UI. Name accepted interfaces, scopes, ownership, lifecycle, auth and versioned data source contracts. Any necessary extension needs a reviewed contract before downstream changes.

## Acceptance

- Use a verified, pinned Perses release and native plugin/format where applicable; do not assume Grafana UI APIs or dashboard JSON are Perses-compatible. Verify real provider signals and mark missing/unsupported coverage explicitly.
- Scope all access by actual Target/tenant permissions, fail closed on unknown ownership or missing authorization, and keep secrets out of logs, manifests and audit. Optional visualization must not force new application capabilities or mandatory services.
- Preserve independent Prometheus, Loki and Tempo backend ownership; remove only owned resources. Specify optional Perses management/visualization through the existing provider and authorization boundaries; never falsely declare metrics/logs/traces application capabilities. Pin version, container/plugins and supported provisioning/upgrade/security contract.
- For alerting, define the real rule evaluator and notification owner in the approved contract. Do not claim native Perses alerting/routing parity without evidence, nor enable external notifications by default.

## Required checks

Record exact candidate SHA and focused tests by name. Route every changed test through an existing CI check/native gate with trigger and actual execution; no skipped/faked native proof. Require isolated Docker and rootless Podman only when runtime risk requires them; no blanket full matrix. Produce deterministic negative/authorization/ownership tests as appropriate.

## Dependencies and handoff

Prerequisites are encoded in `depends_on`. One worker per card/branch/PR, no concurrent writes to shared files. Codex/Owner-delegated Maintainer reviews and merges only after real checks; no independent-review claim. Archive Console/Node Connector repos are excluded. No implementation or release has occurred.

Supersedes [t-20261113-r28-grafana-contract-seam](t-20261113-r28-grafana-contract-seam.md) under the [Owner decision](../decisions/2026-11-14-perses-replaces-grafana-v0428.md).
