---
id: t-20261113-r28-console-live-wizards
card_number: "0428-016"
card_short_title: "Connect existing management wi"
type: task
areas: [console]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Wire already-built application create/edit, Target and workspace flows to permitted canonical Core operations. Reuse 0.4.26 c"
kanban_title: "0428-016 · Connect existing management wizards"
priority: normal
depends_on: [t-20261017-release-0-4-28-updates, t-20261113-r28-console-api-contracts]
repos: [mcpdev80/baseharbor-console]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261113-r28-console-live-wizards · Connect existing management wizards #task #release/v0-4-28 #status/planned #area/console #kind/task

## Outcome and scope

Wire already-built application create/edit, Target and workspace flows to permitted canonical Core operations. Reuse 0.4.26 capabilities/footprint and 0.4.27 onboarding policies. Only actually supported commands; no speculative backend or new wizard engine.

## Acceptance

One login -> select Target -> inspect/plan/confirm/apply/status or explicit unsupported response. Duplicate mutation, missing consent, denied role and stale session are rejected.

## Dependencies and file ownership

- Depends on: t-20261017-release-0-4-28-updates, t-20261113-r28-console-api-contracts.
- Console wizard and new/detail route files only. No shared adapters, Providers/Observability pages or workflow YAML edits.
- No worker may modify another worker's reserved file set or invent interfaces while a predecessor is pending. Read current merged heads and old PRs before coding.

## Required checks and CI routing

Existing wizard component tests and exact Core-authenticated browser journey on selected runtime.

## Coordinator / Codex handoff

- Coordinator assigns one independent ready task to one of five workers, claims it in planning before work, and dispatches only after accepted dependencies. Capacity is a ceiling, not a requirement to start five agents.
- Worker delivers one small PR against product repository's normal development branch with exact HEAD, tests -> selected check -> trigger -> execution result, and records a planning handoff; no self-review, merge or release.
- Codex is the independent reviewer and designated merger for approved, green PRs; it checks architecture, changed paths, test routing and exact-source evidence before merging. No merge on skipped/failed mandatory assertions.
- Following merge, coordinator reconciles the planning card and unlocks dependent ready work only after acceptance. No release/tag/promotion by worker or coordinator.

## Handoff

Not started. Claim, PR, checks, evidence and actual blockers will be recorded here.
