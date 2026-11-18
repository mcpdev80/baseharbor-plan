---
id: t-20261114-r28-perses-datasources
card_number: "0428-083"
card_short_title: "Connect Perses Prometheus"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: worker-ornith1.5
kanban_status: active
kanban_lane: active
kanban_summary: Provision authorized existing Prometheus datasource in Perses using supported pinned native plugin and proxy/TLS contract.
kanban_title: 0428-083 · Connect Perses Prometheus
priority: normal
depends_on: [t-20261114-r28-perses-contract-seam, t-20261114-r28-perses-runtime, t-20261114-r28-perses-signal-inventory]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1608]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

## Owner decision — 2026-11-17

Owner decision (2026-11-17): Unblock. Reopen PR #1608 if it remains suitable, otherwise create a superseding PR on develop. Restore the Prometheus datasource integration and rebase PR #1665 onto an actively CI-covered base. Run the applicable exact-head CI and security/authorization checks before review and merge. No merge is authorized solely by this decision.

- [ ] t-20261114-r28-perses-datasources · Connect Perses Prometheus #task #release/v0-4-28 #status/active #view/active #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** worker-ornith1.5 · **Priority:** normal  
    **PR:** [baseharbor#1608](https://github.com/mcpdev80/baseharbor/pull/1608)  
    **Needs:** [t-20261114-r28-perses-runtime](t-20261114-r28-perses-runtime.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-perses-contract-seam](t-20261114-r28-perses-contract-seam.md), [t-20261114-r28-perses-runtime](t-20261114-r28-perses-runtime.md), [t-20261114-r28-perses-signal-inventory](t-20261114-r28-perses-signal-inventory.md)  
**Required by:** [t-20261114-r28-perses-alerts](t-20261114-r28-perses-alerts.md), [t-20261114-r28-perses-dashboards](t-20261114-r28-perses-dashboards.md)  
**Owner:** worker-ornith1.5  
**Priority:** normal  
**PRs:** [baseharbor#1608](https://github.com/mcpdev80/baseharbor/pull/1608)  
**Source:** 
<!-- /generated:links -->

## Goal

Provision authorized existing Prometheus datasource in Perses using supported pinned native plugin and proxy/TLS contract.

## Scope and file ownership

Dedicated Prometheus datasource adapter/tests; no new Prometheus instance or invented metrics. Inspect the current Core source before implementing; use existing provider/capability, ownership, TLS and lifecycle contracts. Coordinate shared registry, CLI, CI and generated docs with their owners. Preserve unrelated work.

## Verified starting points and bounded implementation

All referenced paths exist at Core `cd77e20e`; fetch actual current `develop` and recheck behavior before editing. Do not treat this static reference as a runtime proof.

- [internal/metrics/prometheus.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/prometheus.go)
- [internal/metrics/prometheus_files.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/prometheus_files.go)
- [internal/metrics/prometheus_verify.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/metrics/prometheus_verify.go)
- [internal/serviceaccess/policy.go](https://github.com/mcpdev80/baseharbor/blob/cd77e20e107d7f29020c167ae143eaf1e6598b40/internal/serviceaccess/policy.go)

Use Perses PrometheusDatasource native versioned spec with existing authorized metrics endpoint, CA and credentials via proxy as supported; test actual query plus unauthorized/cross-target denial and no secret in descriptors.

## Acceptance

- Use a verified, pinned Perses release and native plugin/format where applicable; do not assume Grafana UI APIs or dashboard JSON are Perses-compatible. Verify real provider signals and mark missing/unsupported coverage explicitly.
- Scope all access by actual Target/tenant permissions, fail closed on unknown ownership or missing authorization, and keep secrets out of logs, manifests and audit. Optional visualization must not force new application capabilities or mandatory services.
- Preserve independent Prometheus, Loki and Tempo backend ownership; remove only owned resources. Provision authorized existing Prometheus datasource in Perses using supported pinned native plugin and proxy/TLS contract.
- For alerting, define the real rule evaluator and notification owner in the approved contract. Do not claim native Perses alerting/routing parity without evidence, nor enable external notifications by default.

## Required checks

Record exact candidate SHA and focused tests by name. Route every changed test through an existing CI check/native gate with trigger and actual execution; no skipped/faked native proof. Require isolated Docker and rootless Podman only when runtime risk requires them; no blanket full matrix. Produce deterministic negative/authorization/ownership tests as appropriate.

## Dependencies and handoff

Prerequisites are encoded in `depends_on`. One worker per card/branch/PR, no concurrent writes to shared files. Codex/Owner-delegated Maintainer reviews and merges only after real checks; no independent-review claim. Archive Console/Node Connector repos are excluded. No implementation or release has occurred.

Supersedes [t-20261113-r28-grafana-datasources](t-20261113-r28-grafana-datasources.md) under the [Owner decision](../decisions/2026-11-14-perses-replaces-grafana-v0428.md).

## Owner decision — 2026-11-18 (takeover)
Card is ready to work after the 2026-11-17 unblock. Precondition per owner: 083 AND 080 must land on develop before #1665 continues (080 already merged via #1590). Deliver 083 on a fresh branch + one PR per card rule (#1608 stays closed).
