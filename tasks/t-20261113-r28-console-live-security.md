---
id: t-20261113-r28-console-live-security
card_number: "0428-017"
card_short_title: "Connect security recovery view"
type: task
areas: [console]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Replace preview-only Security, Recovery and Evidence views only for already-supported protected Core operations. Preserve act"
kanban_title: "0428-017 · Connect security recovery views"
priority: normal
depends_on: [t-20261017-release-0-4-28-updates, t-20261113-r28-console-api-contracts]
repos: [mcpdev80/baseharbor-console]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261113-r28-console-live-security · Connect security recovery views #task #release/v0-4-28 #status/planned #area/console #kind/task

## Outcome and scope

Replace preview-only Security, Recovery and Evidence views only for already-supported protected Core operations. Preserve actor, ownership, safe redaction, destructive confirmation and current provider controls; no browser-managed secret store.

## Acceptance

Read and permitted mutation flow show real Core results, denial and expiry are safe, and unsupported controls are explicitly unavailable rather than acting on fixtures.

## Dependencies and file ownership

- Depends on: t-20261017-release-0-4-28-updates, t-20261113-r28-console-api-contracts.
- Console security/recovery/evidence pages and components only; no shared adapter or other pages.
- No worker may modify another worker's reserved file set or invent interfaces while a predecessor is pending. Read current merged heads and old PRs before coding.

## Required checks and CI routing

Contract/UI tests with negative authorization, redaction and no-replay; selected browser Core journey.

## Coordinator / Codex handoff

- Coordinator assigns one independent ready task to one of five workers, claims it in planning before work, and dispatches only after accepted dependencies. Capacity is a ceiling, not a requirement to start five agents.
- Worker delivers one small PR against product repository's normal development branch with exact HEAD, tests -> selected check -> trigger -> execution result, and records a planning handoff; no self-review, merge or release.
- Codex is the independent reviewer and designated merger for approved, green PRs; it checks architecture, changed paths, test routing and exact-source evidence before merging. No merge on skipped/failed mandatory assertions.
- Following merge, coordinator reconciles the planning card and unlocks dependent ready work only after acceptance. No release/tag/promotion by worker or coordinator.

## Handoff

Not started. Claim, PR, checks, evidence and actual blockers will be recorded here.
