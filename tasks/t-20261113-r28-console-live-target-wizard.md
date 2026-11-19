---
id: t-20261113-r28-console-live-target-wizard
card_number: "0428-026"
card_short_title: "Wire live Target wizard"
type: task
areas: [console]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: closed
kanban_lane: closed
kanban_summary: "Connect existing Target create/edit wizard only to allowed Core Target operations; preserve runtime/access selection, ownership…"
kanban_title: "0428-026 · Wire live Target wizard"
priority: normal
depends_on: [t-20261017-release-0-4-28-updates, t-20261113-r28-console-api-contracts]
repos: [mcpdev80/baseharbor-console]
prs: []
sources: []
blocker: ""
resolution: dropped
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/decisions/2026-11-14-public-console-connector-scope.md"]
early: true
---

- [x] t-20261113-r28-console-live-target-wizard · Wire live Target wizard #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/console #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Needs:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261113-r28-console-api-contracts](t-20261113-r28-console-api-contracts.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/decisions/2026-11-14-public-console-connector-scope.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** dropped  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261113-r28-console-api-contracts](t-20261113-r28-console-api-contracts.md)  
**Required by:** [t-20261113-r28-console-native-journey](t-20261113-r28-console-native-journey.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Connect existing Target create/edit wizard only to allowed Core Target operations; preserve runtime/access selection, ownership and dev/test/prod default policy.

## Acceptance

One permitted Target change with policy preview and confirmation, denied/unavailable and stale selection regressions.

## Dependencies and exclusive file ownership

- Only start implementation once dependencies in frontmatter are accepted and an actual interface is available. Do not wait on independent cards.
- **Owned files:** src/app/targets/new/**, edit target route and src/components/wizard/target-* only.
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

## Verified code entry points and no-guess rule (2026-11-13)

Current `src/app/targets/page.tsx` uses `LiveCoreView view="targets"` and links `/targets/new`; retain this exact route and existing Core read model. Access/provider boundaries in Core: `docs/spec/target-access-v1.md`, `internal/machine/contract.go`. Preserve 0.4.27 Target policy presets, no new Target schema.

Before coding, confirm files against exact current develop/main HEAD and actual named CI. If source differs, stop and hand one precise diff to Coordinator; no guessed endpoint or promise of success.
