---
id: t-20261113-r28-grafana-dashboard-identity
card_number: "0428-039"
card_short_title: "Qualify Keycloak dashboard"
type: task
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Inspect Keycloak's native metrics from the actual pinned provider code; use Grafana dashboard 10441…"
kanban_title: "0428-039 · Qualify Keycloak dashboard"
priority: normal
depends_on: [t-20261017-release-0-4-28-updates, t-20261113-r28-grafana-dashboard-selection]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261113-r28-grafana-dashboard-identity · Qualify Keycloak dashboard #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/observability #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261113-r28-grafana-dashboard-selection](t-20261113-r28-grafana-dashboard-selection.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261113-r28-grafana-dashboard-selection](t-20261113-r28-grafana-dashboard-selection.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Inspect Keycloak's native metrics from the actual pinned provider code; use Grafana dashboard 10441 (https://grafana.com/grafana/dashboards/10441-keycloak-metrics-dashboard/) only as reference because it requires the separate legacy Keycloak Metrics SPI. Prefer a small template built from native current Keycloak metrics if available. Do not install obsolete SPI blindly.

## Acceptance

If native metrics are actually scraped, show real request/login metrics that exist; if absent, mark unavailable; no claimed SPI compatibility, no secret leakage.

## Exclusive ownership, current source and worker instructions

Only `internal/grafana/dashboards/keycloak*` assets/tests. Read `internal/identityprovider/`, `internal/capability/reference.go` and 0428-033 signal matrix; no Keycloak provider changes.

Worker reads only named paths at exact current Core SHA, accepted predecessors and direct tests. One narrow PR; report test name -> selected CI job -> source trigger -> exact successful assertion, and denial/no-data case. Missing exporter is a legitimate unsupported state, not a license to expand scope. Coordinator assigns at most five disjoint workers; Codex independently reviews and merges.

## Handoff

Not started.
