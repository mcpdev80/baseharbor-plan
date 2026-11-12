---
id: t-20261113-r28-console-live-inventory
card_number: "0428-015"
card_short_title: "Bind live Providers view"
type: task
areas: [console]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Connect ONLY Providers list to existing protected Core read operations; Observability is a different task."
kanban_title: "0428-015 · Bind live Providers view"
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

## Goal

Connect ONLY Providers list to existing protected Core read operations; Observability is a different task.

## Acceptance

Authorized provider list, empty/denied, no fixture fallback.

## Dependencies and file ownership

- Exclusive product writes: src/app/providers/** and src/components/providers/**; no shared adapters.
- Dependencies are the frontmatter depends_on values. Do not wait for unrelated Grafana/Console cards.
- Before implementation read current exact-source contract and named files only. If an API is missing, report one concrete blocker to Coordinator; do not invent a second API.

## Required checks and CI routing

- Small positive/negative tests for the listed acceptance; bind exact tests to existing selected CI triggers, native tests only for covered runtime behavior.
- Worker supplies exact PR HEAD, affected files, commands/checks, results and cleanup; no skipped test counted as passing.

## Coordinator / Codex handoff

- Coordinator assigns one independent ready task to one of five workers, claims it in planning before work, and dispatches only after accepted dependencies. Capacity is a ceiling, not a requirement to start five agents.
- Worker delivers one small PR against product repository's normal development branch with exact HEAD, tests -> selected check -> trigger -> execution result, and records a planning handoff; no self-review, merge or release.
- Codex is the independent reviewer and designated merger for approved, green PRs; it checks architecture, changed paths, test routing and exact-source evidence before merging. No merge on skipped/failed mandatory assertions.
- Following merge, coordinator reconciles the planning card and unlocks dependent ready work only after acceptance. No release/tag/promotion by worker or coordinator.

## Handoff

Not started. Claim, PR, checks, evidence and actual blockers will be recorded here.
