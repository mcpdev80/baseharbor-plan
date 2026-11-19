---
id: t-20261114-r28-perses-dashboard-messaging
card_number: "0428-079"
card_short_title: "Perses messaging dashboards"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: Codex team (current chat)
kanban_status: closed
kanban_lane: closed
kanban_summary: Deliver RabbitMQ panels conditional on real supported metrics.
kanban_title: 0428-079 · Perses messaging dashboards
priority: normal
depends_on: [t-20261114-r28-perses-dashboard-selection]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1701]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1701", "https://github.com/mcpdev80/baseharbor/commit/f9f02507ba69c178185c54987384cfc0fc6a006f", "https://github.com/mcpdev80/baseharbor/actions/runs/44581190442", "https://github.com/mcpdev80/baseharbor/commit/558dc42d0c8c9d798fcdf5938be2ea14e432b754"]
---

- [x] t-20261114-r28-perses-dashboard-messaging · Perses messaging dashboards #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** Codex team (current chat) · **Priority:** normal  
    **PR:** [baseharbor#1701](https://github.com/mcpdev80/baseharbor/pull/1701)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1701), [proof 2](https://github.com/mcpdev80/baseharbor/commit/f9f02507ba69c178185c54987384cfc0fc6a006f), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44581190442), [proof 4](https://github.com/mcpdev80/baseharbor/commit/558dc42d0c8c9d798fcdf5938be2ea14e432b754)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-perses-dashboard-selection](t-20261114-r28-perses-dashboard-selection.md)  
**Required by:** [t-20261114-r28-perses-native-proof](t-20261114-r28-perses-native-proof.md)  
**Owner:** Codex team (current chat)  
**Priority:** normal  
**PRs:** [baseharbor#1701](https://github.com/mcpdev80/baseharbor/pull/1701)  
**Source:** 
<!-- /generated:links -->

## Goal

Deliver RabbitMQ panels conditional on real supported metrics.

## Scope and file ownership

Own messaging dashboard assets and focused tests. Inspect the current Core source before implementing; use existing provider/capability, ownership, TLS and lifecycle contracts. Coordinate shared registry, CLI, CI and generated docs with their owners. Preserve unrelated work.

## Verified starting points and bounded implementation

All referenced paths exist at Core `cd77e20e`; fetch actual current `develop` and recheck behavior before editing. Do not treat this static reference as a runtime proof.

- [internal/capability/reference.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/capability/reference.go)
- [internal/application/provider_registry.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/application/provider_registry.go)
- [internal/metrics/prometheus_files.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/prometheus_files.go)

Create first messaging dashboard for actual authorized RabbitMQ signals, conditional on measured metrics and labels. Test absent provider, no exporter, tenant isolation and dashboard provisioning.

## Acceptance

- Use a verified, pinned Perses release and native plugin/format where applicable; do not assume Grafana UI APIs or dashboard JSON are Perses-compatible. Verify real provider signals and mark missing/unsupported coverage explicitly.
- Scope all access by actual Target/tenant permissions, fail closed on unknown ownership or missing authorization, and keep secrets out of logs, manifests and audit. Optional visualization must not force new application capabilities or mandatory services.
- Preserve independent Prometheus, Loki and Tempo backend ownership; remove only owned resources. Deliver RabbitMQ panels conditional on real supported metrics.
- For alerting, define the real rule evaluator and notification owner in the approved contract. Do not claim native Perses alerting/routing parity without evidence, nor enable external notifications by default.

## Required checks

Record exact candidate SHA and focused tests by name. Route every changed test through an existing CI check/native gate with trigger and actual execution; no skipped/faked native proof. Require isolated Docker and rootless Podman only when runtime risk requires them; no blanket full matrix. Produce deterministic negative/authorization/ownership tests as appropriate.

## Dependencies and handoff

Prerequisites are encoded in `depends_on`. One worker per card/branch/PR, no concurrent writes to shared files. Codex/Owner-delegated Maintainer reviews and merges only after real checks; no independent-review claim. Archive Console/Node Connector repos are excluded. No implementation or release has occurred.

Supersedes [t-20261113-r28-grafana-dashboard-messaging](t-20261113-r28-grafana-dashboard-messaging.md) under the [Owner decision](../decisions/2026-11-14-perses-replaces-grafana-v0428.md).
## Owner decision note (2026-11-16, coordinator)

1. The RabbitMQ telemetry signal is explicitly UNAVAILABLE in this ecosystem (no native signal source; owner decision 2026-11-15: no exporter is introduced). This card therefore owns only the conditional eligibility layer: panels may appear if and only if a real supported signal is later validated.
2. Board number: this card carries `0428-079` (kanban_title). There is no separate "rabbitmq-source" task; PR #1603 (`draft(0428-079)`) is this card's deliverable. Prior Luna note "RabbitMQ-source task absent in Planning" is resolved by this clarification.

2026-11-19: PR #1701 merged to `develop` at `558dc42d0c8c9d798fcdf5938be2ea14e432b754` after exact-head run `44581190442` succeeded at `f9f02507ba69c178185c54987384cfc0fc6a006f`. The run's Selected Checks, all six Go unit shards, build, vet, source format, workflow policy, and trusted-plan checks passed. Native Docker/Podman and runtime checks were skipped by the accepted native-gate plan because this change adds no runtime resources or lifecycle. Focused tests: `TestPersesMessagingCatalogIsUnavailableWithoutNativeSignal`, `TestPersesMessagingEligibilityFailsClosedForSelectionAndInventories`, `TestPersesMessagingEligibilityFailsClosedWithoutPinnedRelease`, `TestPersesMessagingNativeSignalRequiresBackendVerification`, `TestPersesMessagingUnavailableJSONMatchesGolden`, and `TestPersesMessagingAvailabilityMapIsExplicit`; `go test ./internal/metrics ./internal/capability`, `go build ./...`, `go vet ./...`, and `bash scripts/source-readability-audit.sh` passed. A broader local `go test ./...` was also attempted but cannot serve as clean evidence in this workstation: unrelated command/runtime/database tests require an existing configured Docker target, trusted live-Core CA, protected Docker backend, or `BASEHARBOR_TEST_DATABASE_URL`; the exact isolated CI shards for this candidate all passed. No security, exporter, runtime, CI-workflow, or shared registry files changed.
