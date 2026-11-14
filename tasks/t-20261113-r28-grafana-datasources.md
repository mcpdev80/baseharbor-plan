---
id: t-20261113-r28-grafana-datasources
card_number: "0428-011"
card_short_title: "Connect Grafana Prometheus"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: closed
kanban_lane: closed
kanban_summary: "Provision exactly an existing, authorized managed Prometheus as Grafana datasource via native provisioning. Reuse provider…"
kanban_title: "0428-011 · Connect Grafana Prometheus"
priority: normal
depends_on: [t-20261017-release-0-4-28-updates, t-20261113-r28-grafana-contract-seam, t-20261113-r28-grafana-runtime, t-20261113-r28-grafana-signal-inventory]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: superseded
superseded_by: t-20261114-r28-perses-datasources
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/decisions/2026-11-14-perses-replaces-grafana-v0428.md"]
early: true
---

- [x] t-20261113-r28-grafana-datasources · Connect Grafana Prometheus #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Needs:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261113-r28-grafana-contract-seam](t-20261113-r28-grafana-contract-seam.md), [t-20261113-r28-grafana-runtime](t-20261113-r28-grafana-runtime.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/decisions/2026-11-14-perses-replaces-grafana-v0428.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** superseded  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261113-r28-grafana-contract-seam](t-20261113-r28-grafana-contract-seam.md), [t-20261113-r28-grafana-runtime](t-20261113-r28-grafana-runtime.md), [t-20261113-r28-grafana-signal-inventory](t-20261113-r28-grafana-signal-inventory.md)  
**Required by:** [t-20261113-r28-grafana-alerts](t-20261113-r28-grafana-alerts.md), [t-20261113-r28-grafana-dashboards](t-20261113-r28-grafana-dashboards.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Provision exactly an existing, authorized managed Prometheus as Grafana datasource via native provisioning. Reuse provider endpoint/CA/secret-safe credentials; do not invent metrics or provision Prometheus.

## Acceptance

One deterministic datasource UID; authorized Prometheus query succeeds, missing/prometheus-disabled does not invent green state; no credentials logged.

## Dependencies and file ownership

- Hard prerequisites (not mere priority): t-20261017-release-0-4-28-updates, t-20261113-r28-grafana-runtime.
- **Exclusive write ownership:** New internal/grafana/provisioning/prometheus* and its tests only; coordination with 022/023 on immutable datasource UID namespace. No shared renderer edits.
- A referenced task must be accepted/merged before implementation if an actual interface is needed; read-only inspection and isolated schema fixtures may start earlier. Never base work on another worker's unmerged branch.

## Worker instructions (256k context budget)

1. Read this card and only the directly named source files, predecessor interface/commit and existing tests. Do not load the whole ecosystem into context.
2. Identify the exact existing implementation, change only the specified behavior and reserved files. If a missing dependency or conflicting owner appears, stop and hand the Coordinator one concrete missing contract/path; do not self-expand the scope.
3. Add/adjust the smallest executable positive and negative regressions described here. **Test -> existing CI check -> file-change trigger -> actual result** is mandatory; no skipped assertion may count as pass.
4. Run targeted source checks; native Docker/Podman/browser only where this card uniquely requires them. Reuse existing selected CI jobs and fixture owners; no shadow approval/evidence system.
5. Open one limited product PR against the normal development branch and hand off exact commit SHA, changed files, commands/check IDs, actual passed assertions, gaps and rollback. No worker self-merges.
6. **Codex reviews independently and merges** only after required tests on the exact PR HEAD. Coordinator updates this plan note/Obsidian state after acceptance; max five non-overlapping workers concurrently.

## Required checks and CI routing

Provisioning JSON/YAML, invalid URL/CA, missing backend and isolated real Prometheus query.

## Handoff

Not claimed. Do not mark accepted from plan creation or a draft PR.

## Binding current-source implementation note (2026-11-13)

Exact sources: `internal/metrics/prometheus.go`, `internal/metrics/prometheus_files.go`, `internal/metrics/management_ui.go`, `internal/capability/reference.go`, `internal/application/provider_registry.go`. Provision only existing authorized provider instance; use accepted Provider Contract seam and protected endpoint/CA. Never hardcode localhost, claim cross-Target read or invent scrape jobs. This card owns Prometheus only.

Worker must quote current exact Core/Console commit, confirm entry points still exist, and stop with explicit blocker if changed. Codex checks exact source and CI selected gate before merge.

## Superseded by Owner decision (2026-11-14)

Closed as superseded by [t-20261114-r28-perses-datasources](t-20261114-r28-perses-datasources.md). The Owner chose Perses in place of Grafana visualization; historical planning is retained. Alert rule evaluation and contact routing are re-specified rather than presumed to be Perses features. No implementation is asserted.
