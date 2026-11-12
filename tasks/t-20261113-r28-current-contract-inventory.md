---
id: t-20261113-r28-current-contract-inventory
card_number: "0428-008"
card_short_title: "Audit current Core Console jou"
type: task
areas: [architecture]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Read exact develop/main heads, existing console-2 PR #8, 0.4.24–0.4.27 accepted code and browser evidence; produce a per-rout"
kanban_title: "0428-008 · Audit current Core Console journeys"
priority: high
depends_on: [t-20261017-release-0-4-28-updates]
repos: [mcpdev80/baseharbor-console, mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261113-r28-current-contract-inventory · Audit current Core Console journeys #task #release/v0-4-28 #status/planned #area/architecture #kind/task

## Outcome and scope

Read exact develop/main heads, existing console-2 PR #8, 0.4.24–0.4.27 accepted code and browser evidence; produce a per-route matrix of live/preview/unsupported and an exact Core operation+authorization map. No replacement implementation and no source refactor.

## Acceptance

An evidence-linked gap matrix separates implemented, integrated, qualified and genuinely missing features. Link exact files, commits and tests; reconcile #8 without discarding its work.

## Dependencies and file ownership

- Depends on: t-20261017-release-0-4-28-updates.
- Planning task only: owned audit note in this task; read-only code examination. No shared product writes.
- No worker may modify another worker's reserved file set or invent interfaces while a predecessor is pending. Read current merged heads and old PRs before coding.

## Required checks and CI routing

Existing source/contract test inventory, browser CI selection and negative coverage; record exact paths and gaps without running a full native matrix.

## Coordinator / Codex handoff

- Coordinator assigns one independent ready task to one of five workers, claims it in planning before work, and dispatches only after accepted dependencies. Capacity is a ceiling, not a requirement to start five agents.
- Worker delivers one small PR against product repository's normal development branch with exact HEAD, tests -> selected check -> trigger -> execution result, and records a planning handoff; no self-review, merge or release.
- Codex is the independent reviewer and designated merger for approved, green PRs; it checks architecture, changed paths, test routing and exact-source evidence before merging. No merge on skipped/failed mandatory assertions.
- Following merge, coordinator reconciles the planning card and unlocks dependent ready work only after acceptance. No release/tag/promotion by worker or coordinator.

## Handoff

Not started. Claim, PR, checks, evidence and actual blockers will be recorded here.
