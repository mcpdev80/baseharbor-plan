---
id: t-20261113-r28-console-api-contracts
card_number: "0428-009"
card_short_title: "Pin Console Core interfaces"
type: task
areas: [console]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Adjust the existing Console adapter and validated wire decoders solely for accepted 0.4.27 Core operations, Target access and"
kanban_title: "0428-009 · Pin Console Core interfaces"
priority: high
depends_on: [t-20261017-release-0-4-28-updates, t-20261113-r28-current-contract-inventory]
repos: [mcpdev80/baseharbor-console, mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261113-r28-console-api-contracts · Pin Console Core interfaces #task #release/v0-4-28 #status/planned #area/console #kind/task

## Outcome and scope

Adjust the existing Console adapter and validated wire decoders solely for accepted 0.4.27 Core operations, Target access and auth/tenant filtering. Determine and carve any truly missing Core HTTP/authorization subtask before changing shared backend. Reuse existing session/transport; no second Core or RBAC.

## Acceptance

Existing live routes pass exact-source read/deny/error contract tests for new Core; unknown or unsupported features remain explicitly unavailable. No fixture fallback.

## Dependencies and file ownership

- Depends on: t-20261017-release-0-4-28-updates, t-20261113-r28-current-contract-inventory.
- Console src/lib/baseharbor/ transport/read-models/contract adapters only; Core shared HTTP changes require a separate later owned task. No page or CI workflow edits.
- No worker may modify another worker's reserved file set or invent interfaces while a predecessor is pending. Read current merged heads and old PRs before coding.

## Required checks and CI routing

Console unit/contract and architecture tests with exact pinned source; identify selected CI check and negative authorization case.

## Coordinator / Codex handoff

- Coordinator assigns one independent ready task to one of five workers, claims it in planning before work, and dispatches only after accepted dependencies. Capacity is a ceiling, not a requirement to start five agents.
- Worker delivers one small PR against product repository's normal development branch with exact HEAD, tests -> selected check -> trigger -> execution result, and records a planning handoff; no self-review, merge or release.
- Codex is the independent reviewer and designated merger for approved, green PRs; it checks architecture, changed paths, test routing and exact-source evidence before merging. No merge on skipped/failed mandatory assertions.
- Following merge, coordinator reconciles the planning card and unlocks dependent ready work only after acceptance. No release/tag/promotion by worker or coordinator.

## Handoff

Not started. Claim, PR, checks, evidence and actual blockers will be recorded here.
