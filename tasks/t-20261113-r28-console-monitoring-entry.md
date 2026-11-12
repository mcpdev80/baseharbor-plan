---
id: t-20261113-r28-console-monitoring-entry
card_number: "0428-014"
card_short_title: "Link Console to Grafana monito"
type: task
areas: [console]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Add one Monitoring navigation entry and contextual drill-down links scoped to the selected Core/Target/application, opening t"
kanban_title: "0428-014 · Link Console to Grafana monitoring"
priority: normal
depends_on: [t-20261017-release-0-4-28-updates, t-20261113-r28-grafana-secure-access, t-20261113-r28-grafana-dashboards]
repos: [mcpdev80/baseharbor-console]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261113-r28-console-monitoring-entry · Link Console to Grafana monitoring #task #release/v0-4-28 #status/planned #area/console #kind/task

## Outcome and scope

Add one Monitoring navigation entry and contextual drill-down links scoped to the selected Core/Target/application, opening the secured Grafana origin. Prefer link/new tab; no cross-origin iframe or duplicated chart engine. If Grafana is disabled, clearly offer enablement information only to authorized operators.

## Acceptance

Console link points to the authenticated installation-owned Grafana instance, never arbitrary URL. Disabled/unavailable state and denied actor are correctly presented.

## Dependencies and file ownership

- Depends on: t-20261017-release-0-4-28-updates, t-20261113-r28-grafana-secure-access, t-20261113-r28-grafana-dashboards.
- Console navigation, monitoring view and its tests only. No shared machine transport/adapter or Core routing writes.
- No worker may modify another worker's reserved file set or invent interfaces while a predecessor is pending. Read current merged heads and old PRs before coding.

## Required checks and CI routing

Console component/browser navigation and origin-negative tests; existing selected quality/browser checks.

## Coordinator / Codex handoff

- Coordinator assigns one independent ready task to one of five workers, claims it in planning before work, and dispatches only after accepted dependencies. Capacity is a ceiling, not a requirement to start five agents.
- Worker delivers one small PR against product repository's normal development branch with exact HEAD, tests -> selected check -> trigger -> execution result, and records a planning handoff; no self-review, merge or release.
- Codex is the independent reviewer and designated merger for approved, green PRs; it checks architecture, changed paths, test routing and exact-source evidence before merging. No merge on skipped/failed mandatory assertions.
- Following merge, coordinator reconciles the planning card and unlocks dependent ready work only after acceptance. No release/tag/promotion by worker or coordinator.

## Handoff

Not started. Claim, PR, checks, evidence and actual blockers will be recorded here.
