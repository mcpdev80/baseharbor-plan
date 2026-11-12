---
id: t-20261113-r28-grafana-contract-seam
card_number: "0428-032"
card_short_title: "Define Grafana provider seam"
type: architecture
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Choose existing provider management interface or minimal v1-compatible extension; no fake application capability."
kanban_title: "0428-032 · Define Grafana provider seam"
priority: critical
depends_on: [t-20261017-release-0-4-28-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261113-r28-grafana-contract-seam · Define Grafana provider seam #task #release/v0-4-28 #status/planned #area/observability #kind/architecture

## Goal

First implementable architecture gate: integrate optional Grafana OSS into the **existing Provider Contract v1**, provider registry/catalog, management-surface and authorization/lifecycle semantics without making it a mandatory portable application capability. Do not start a Grafana container in this task.

## Exact current-code reading order

1. `docs/spec/provider-contract-v1.md`: three provider axes, management surface and lifecycle ownership, no product identity in portable application intent.
2. `internal/capability/domain.go`: `ProviderKind` is distinct from portable `Kind`; currently no Grafana constant.
3. `internal/capability/integration_contract.go`: `IntegrationDescriptor.Validate()` currently **requires a real capability and a versioned specification**. Do not falsely claim Grafana implements `Metrics`, `Logs`, `Traces` or `TelemetryOTLP`; it only visualizes existing data.
4. `internal/capability/service.go` and `internal/capability/reference.go`: existing `ServiceObservability` and `PrometheusIntegration`, `LokiIntegration`, `TempoIntegration`, and `ProviderInterface` management declarations.
5. `internal/provider/builtin/catalog.go`, `internal/provider/authoring/descriptor.go`, `internal/application/provider_registry.go`: catalog vs installed/owned runtime instances.
6. `internal/metrics/management_ui.go`, `internal/application/management_ui.go`, `internal/providerui/application.go`, `cmd/baha/app_dev_routing.go`: `ObservabilityManagementUI` currently refers to a Prometheus management surface; do NOT silently swap it to Grafana.
7. `docs/spec/provider-management-acceptance-v1.md`, `docs/spec/provider-conformance-v1.md`, `conformance/provider/v1/README.md`.

## Deliverable, exact boundary

- Record a **specific compatible representation**: optional installation/Target-owned management-tool provider through the existing management interface if admissible; otherwise one explicitly reviewed minimal, backwards-compatible administrative-tool descriptor extension to Provider Contract v1.
- Define ID, provider version, product/image digest distinction, service boundary, advertised supported scopes, administration/visualization interface, role mapping, endpoint discovery, source references, ownership, update/destroy and external/unmanaged behavior.
- The catalog must be the installable distribution catalog; the runtime registry must track an **actual owned instance**, not fabricated application bindings. Normal applications must never request `grafana` in portable intent.
- Define concrete Go interface names and exact file paths in an accepted handoff appended to this task; all downstream workers must consume it, not invent a new registry.
- Validate descriptor and management-surface behavior with short positive/negative conformance tests: invalid descriptor, unsupported scope, no-default install, foreign Target, missing protected source, forbidden access.
- If introducing a UI-only provider requires changing established portable semantics or weakening `IntegrationDescriptor.Validate`, stop and hand the Coordinator/Codex one exact design decision. Never silently invent `visualization/v1` as an application capability.

## Exclusive write paths

Only necessary provider-contract/catalog/registry metadata, focused tests, and this handoff. No Grafana runtime assets, dashboards, secrets, gateways, or Console code.

## Worker instructions and Codex handoff

Read only listed paths and direct tests at current Core `develop` SHA; compare existing behavior before editing. One small PR; record exact changed paths, schema, test -> existing CI job -> selection trigger -> actual result. Codex independently reviews and merges on exact green head, then Coordinator marks accepted and releases dependent workers. Five workers max; no shared-file parallel edits or release/tag.
