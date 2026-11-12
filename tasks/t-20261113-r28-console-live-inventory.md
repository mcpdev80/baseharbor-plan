---
id: t-20261113-r28-console-live-inventory
card_number: "0428-015"
card_short_title: "Bind provider monitoring inven"
type: task
areas: [console]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Replace fixture-only Providers and Observability index content with existing protected Core read-model operations. Preserve d"
kanban_title: "0428-015 · Bind provider monitoring inventory"
priority: normal
depends_on: [t-20261017-release-0-4-28-updates, t-20261113-r28-console-api-contracts]
repos: [mcpdev80/baseharbor-console]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261113-r28-console-live-inventory · Bind provider monitoring inventory #task #release/v0-4-28 #status/planned #area/console #kind/task

## Outcome and scope

Replace fixture-only Providers and Observability index content with existing protected Core read-model operations. Preserve dedicated preview mode. Show unknown/unsupported collection and capabilities honestly; no new telemetry service.

## Acceptance

Authenticated operator sees actual authorized providers and signals, tenant-denied objects are absent, logout never displays stale live data, and no preview fallback occurs.

## Dependencies and file ownership

- Depends on: t-20261017-release-0-4-28-updates, t-20261113-r28-console-api-contracts.
- Console provider and observability pages/components only; shared adapter changes only through task 009.
- No worker may modify another worker's reserved file set or invent interfaces while a predecessor is pending. Read current merged heads and old PRs before coding.

## Required checks and CI routing

Focused UI read-model/empty/denied tests and selected Console CI/browser smoke.

## Coordinator / Codex handoff

- Coordinator assigns one independent ready task to one of five workers, claims it in planning before work, and dispatches only after accepted dependencies. Capacity is a ceiling, not a requirement to start five agents.
- Worker delivers one small PR against product repository's normal development branch with exact HEAD, tests -> selected check -> trigger -> execution result, and records a planning handoff; no self-review, merge or release.
- Codex is the independent reviewer and designated merger for approved, green PRs; it checks architecture, changed paths, test routing and exact-source evidence before merging. No merge on skipped/failed mandatory assertions.
- Following merge, coordinator reconciles the planning card and unlocks dependent ready work only after acceptance. No release/tag/promotion by worker or coordinator.

## Handoff

Not started. Claim, PR, checks, evidence and actual blockers will be recorded here.
