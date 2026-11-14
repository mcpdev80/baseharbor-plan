---
id: t-20261113-r28-grafana-dashboards
card_number: "0428-012"
card_short_title: "Grafana infrastructure dashboa"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: closed
kanban_lane: closed
kanban_summary: Deliver ONE Grafana OSS dashboard for real Target/application infrastructure metrics present in Prometheus. Inspect label names…
kanban_title: 0428-012 · Grafana infrastructure dashboa
priority: normal
depends_on: [t-20261017-release-0-4-28-updates, t-20261113-r28-grafana-dashboard-selection, t-20261113-r28-grafana-datasources]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: superseded
superseded_by: t-20261114-r28-perses-dashboards
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/decisions/2026-11-14-perses-replaces-grafana-v0428.md"]
early: true
---

- [x] t-20261113-r28-grafana-dashboards · Grafana infrastructure dashboard #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Needs:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261113-r28-grafana-dashboard-selection](t-20261113-r28-grafana-dashboard-selection.md), [t-20261113-r28-grafana-datasources](t-20261113-r28-grafana-datasources.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/decisions/2026-11-14-perses-replaces-grafana-v0428.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** superseded  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261113-r28-grafana-dashboard-selection](t-20261113-r28-grafana-dashboard-selection.md), [t-20261113-r28-grafana-datasources](t-20261113-r28-grafana-datasources.md)  
**Required by:** [t-20261113-r28-grafana-native-proof](t-20261113-r28-grafana-native-proof.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Deliver ONE Grafana OSS dashboard for real Target/application infrastructure metrics present in Prometheus. Inspect label names and queries first. Don't invent CPU, memory, readiness or deployment metrics where absent.

## Acceptance

One useful provisioned dashboard with working current metric series and explicit no-data state for unavailable collectors.

## Dependencies and file ownership

- Hard prerequisites (not mere priority): t-20261017-release-0-4-28-updates, t-20261113-r28-grafana-datasources.
- **Exclusive write ownership:** internal/grafana/dashboards/infrastructure*.json and test fixtures ONLY; no runtime/provider code.
- A referenced task must be accepted/merged before implementation if an actual interface is needed; read-only inspection and isolated schema fixtures may start earlier. Never base work on another worker's unmerged branch.

## Worker instructions (256k context budget)

1. Read this card and only the directly named source files, predecessor interface/commit and existing tests. Do not load the whole ecosystem into context.
2. Identify the exact existing implementation, change only the specified behavior and reserved files. If a missing dependency or conflicting owner appears, stop and hand the Coordinator one concrete missing contract/path; do not self-expand the scope.
3. Add/adjust the smallest executable positive and negative regressions described here. **Test -> existing CI check -> file-change trigger -> actual result** is mandatory; no skipped assertion may count as pass.
4. Run targeted source checks; native Docker/Podman/browser only where this card uniquely requires them. Reuse existing selected CI jobs and fixture owners; no shadow approval/evidence system.
5. Open one limited product PR against the normal development branch and hand off exact commit SHA, changed files, commands/check IDs, actual passed assertions, gaps and rollback. No worker self-merges.
6. **Codex reviews independently and merges** only after required tests on the exact PR HEAD. Coordinator updates this plan note/Obsidian state after acceptance; max five non-overlapping workers concurrently.

## Required checks and CI routing

JSON schema/provisioning validation, expected panel queries, test data/no-data states; one real panel query on native fixture.

## Handoff

Not claimed. Do not mark accepted from plan creation or a draft PR.

## Binding current-source implementation note (2026-11-13)

Own only one native BaseHarbor infrastructure dashboard. Read `docs/spec/provider-contract-v1.md`, `internal/capability/integration_contract.go`, `internal/application/runtime_telemetry.go` and accepted signal matrix 0428-033. Only use tested real PromQL names/labels and real available signals. Community host/container and product-specific dashboards belong to 0428-035..037, NOT this card.

Worker must quote current exact Core/Console commit, confirm entry points still exist, and stop with explicit blocker if changed. Codex checks exact source and CI selected gate before merge.

## Superseded by Owner decision (2026-11-14)

Closed as superseded by [t-20261114-r28-perses-dashboards](t-20261114-r28-perses-dashboards.md). The Owner chose Perses in place of Grafana visualization; historical planning is retained. Alert rule evaluation and contact routing are re-specified rather than presumed to be Perses features. No implementation is asserted.
