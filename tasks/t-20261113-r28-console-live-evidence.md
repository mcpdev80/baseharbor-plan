---
id: t-20261113-r28-console-live-evidence
card_number: "0428-029"
card_short_title: "Bind Console Evidence view"
type: task
areas: [console]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Connect ONLY existing Evidence view to canonical Core execution/status/event results. Do not rebuild CI receipt chain."
kanban_title: "0428-029 · Bind Console Evidence view"
priority: normal
depends_on: [t-20261017-release-0-4-28-updates, t-20261113-r28-console-api-contracts]
repos: [mcpdev80/baseharbor-console]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261113-r28-console-live-evidence · Bind Console Evidence view #task #release/v0-4-28 #status/planned #area/console #kind/task

## Goal

Connect ONLY existing Evidence view to canonical Core execution/status/event results. Do not rebuild CI receipt chain.

## Acceptance

Correlated Core execution records appear accurately; denied/empty/expired states; no fake CI approvals.

## Dependencies and exclusive file ownership

- Only start implementation once dependencies in frontmatter are accepted and an actual interface is available. Do not wait on independent cards.
- **Owned files:** src/app/evidence/** and src/components/evidence/** only.
- No other worker may change these files concurrently. File overlap requires explicit Coordinator serialization before coding.

## Worker instructions (local 256k LLM)

1. Fetch the current exact product head and this task's accepted predecessors. Read only named source paths and their direct tests, not the entire repository or all backlog.
2. Check current behavior before editing. If already delivered, present exact code/test SHA and ask Coordinator to mark the card superseded; do not duplicate.
3. Implement ONLY the Goal in owned files, using the existing Core authority/transport and native provider patterns; do not add a new API, database, custom monitoring engine or provider capability.
4. Add one executable positive and one negative test for the Acceptance, identify exact test -> existing CI check -> path/trigger -> real result. If missing CI routing, hand off to assigned shared CI owner rather than silently skipping.
5. Run the smallest relevant checks and selected native proof where required. Open one limited PR to the product's normal integration branch; hand off head SHA, files, observed test output, exact gate run and unresolved issues.
6. **Worker never reviews/merges. Codex is reviewer and merger** after required green exact-HEAD checks and real negative tests. Coordinator updates task state and schedules up to 5 ready non-overlapping workers; no release/tag authorization.

## Handoff

Unassigned. No code or acceptance evidence yet.
