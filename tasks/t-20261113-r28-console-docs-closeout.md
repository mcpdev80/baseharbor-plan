---
id: t-20261113-r28-console-docs-closeout
card_number: "0428-019"
card_short_title: "Finish monitoring Console docs"
type: task
areas: [documentation]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Update concise English/German operator/developer docs for optional Grafana, enabled data sources, supported Console journeys,"
kanban_title: "0428-019 · Finish monitoring Console docs"
priority: normal
depends_on: [t-20261017-release-0-4-28-updates, t-20261113-r28-console-native-journey]
repos: [mcpdev80/baseharbor-console, mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261113-r28-console-docs-closeout · Finish monitoring Console docs #task #release/v0-4-28 #status/planned #area/documentation #kind/task

## Outcome and scope

Update concise English/German operator/developer docs for optional Grafana, enabled data sources, supported Console journeys, access restrictions, no-data behavior and actual commands. Keep release notes human-oriented, not implementation diaries. Refresh stale Console readiness wording based on accepted evidence.

## Acceptance

Commands match the shipped CLI/API; EN/DE navigation and build pass. Do not claim Grafana mandatory, public by default, or unqualified native functionality.

## Dependencies and file ownership

- Depends on: t-20261017-release-0-4-28-updates, t-20261113-r28-console-native-journey.
- Documentation and release-facing examples only. Coordinate shared release notes with release maintainer; no product or CI files.
- No worker may modify another worker's reserved file set or invent interfaces while a predecessor is pending. Read current merged heads and old PRs before coding.

## Required checks and CI routing

EN/DE docs build, link/check and command reference verification against current source.

## Coordinator / Codex handoff

- Coordinator assigns one independent ready task to one of five workers, claims it in planning before work, and dispatches only after accepted dependencies. Capacity is a ceiling, not a requirement to start five agents.
- Worker delivers one small PR against product repository's normal development branch with exact HEAD, tests -> selected check -> trigger -> execution result, and records a planning handoff; no self-review, merge or release.
- Codex is the independent reviewer and designated merger for approved, green PRs; it checks architecture, changed paths, test routing and exact-source evidence before merging. No merge on skipped/failed mandatory assertions.
- Following merge, coordinator reconciles the planning card and unlocks dependent ready work only after acceptance. No release/tag/promotion by worker or coordinator.

## Handoff

Not started. Claim, PR, checks, evidence and actual blockers will be recorded here.
