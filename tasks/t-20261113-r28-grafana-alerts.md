---
id: t-20261113-r28-grafana-alerts
card_number: "0428-020"
card_short_title: "Provision Grafana alert rules"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: Provision Grafana OSS rules on real Prometheus metrics only; notification contact points and routing belong to a different card.
kanban_title: "0428-020 · Provision Grafana alert rules"
priority: high
depends_on: [t-20261017-release-0-4-28-updates, t-20261113-r28-grafana-datasources]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261113-r28-grafana-alerts · Grafana: deliver managed OSS alerting and scoped routing #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261113-r28-grafana-datasources](t-20261113-r28-grafana-datasources.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261113-r28-grafana-datasources](t-20261113-r28-grafana-datasources.md)  
**Required by:** [t-20261113-r28-grafana-contact-routing](t-20261113-r28-grafana-contact-routing.md), [t-20261113-r28-grafana-native-proof](t-20261113-r28-grafana-native-proof.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Provision Grafana OSS rules on real Prometheus metrics only; notification contact points and routing belong to a different card.

## Acceptance

One threshold crosses firing/resolved; no-data/error fail safely; native evaluation.

## Dependencies and file ownership

- Exclusive product writes: internal/grafana/alerting/rules* only.
- Dependencies are the frontmatter depends_on values. Do not wait for unrelated Grafana/Console cards.
- Before implementation read current exact-source contract and named files only. If an API is missing, report one concrete blocker to Coordinator; do not invent a second API.

## Required checks and CI routing

- Small positive/negative tests for the listed acceptance; bind exact tests to existing selected CI triggers, native tests only for covered runtime behavior.
- Worker supplies exact PR HEAD, affected files, commands/checks, results and cleanup; no skipped test counted as passing.

## Coordinator / Codex handoff

- Worker claims one task, opens one small PR to the normal product development branch and hands off exact verified results.
- Codex independently reviews and merges only after relevant real checks pass. No worker or Coordinator merges or publishes.
- Coordinator updates planning state after acceptance and dispatches newly unblocked tasks.

## Handoff

Not started. Actual branch, PR, exact checks and test evidence will be attached here.
