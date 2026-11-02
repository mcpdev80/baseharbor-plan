---
id: t-20261102-rcptlink-task
type: task
areas: []
release: v0.4.x
version: ""
parent: ""
owner: ornith (rcptlink)
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1267","mcpdev80/baseharbor#1268","mcpdev80/baseharbor#1269","mcpdev80/baseharbor#1270","mcpdev80/baseharbor#1271","mcpdev80/baseharbor#1274","mcpdev80/baseharbor#1275"]
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261102-rcptlink-task · Receipt post-run writer: add single `Resolves #<issue>` link to merged PRs so tasklink auto-resolves green #task #release/v0-4-x #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** ornith (rcptlink)  
    **PR:** [baseharbor#1267](https://github.com/mcpdev80/baseharbor/pull/1267), [baseharbor#1268](https://github.com/mcpdev80/baseharbor/pull/1268), [baseharbor#1269](https://github.com/mcpdev80/baseharbor/pull/1269), [baseharbor#1270](https://github.com/mcpdev80/baseharbor/pull/1270), [baseharbor#1271](https://github.com/mcpdev80/baseharbor/pull/1271), [baseharbor#1274](https://github.com/mcpdev80/baseharbor/pull/1274), [baseharbor#1275](https://github.com/mcpdev80/baseharbor/pull/1275)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.x](../releases/v0.4.x.md)  
**Depends on:** none  
**Owner:** ornith (rcptlink)  
**Priority:** not set  
**PRs:** [baseharbor#1267](https://github.com/mcpdev80/baseharbor/pull/1267), [baseharbor#1268](https://github.com/mcpdev80/baseharbor/pull/1268), [baseharbor#1269](https://github.com/mcpdev80/baseharbor/pull/1269), [baseharbor#1270](https://github.com/mcpdev80/baseharbor/pull/1270), [baseharbor#1271](https://github.com/mcpdev80/baseharbor/pull/1271), [baseharbor#1274](https://github.com/mcpdev80/baseharbor/pull/1274), [baseharbor#1275](https://github.com/mcpdev80/baseharbor/pull/1275)  
**Source:** 
<!-- /generated:links -->

## Goal

Make the "Receipt · Post-Run Writer" green again: the merged PRs #1267–#1275 (post #1272/#1273) that were merged without a `Resolves #<issue>` line currently fail `receipt_tasklink.py` with `tasklink blocked: PR #<n> body has no Closes/Fixes/Resolves #NNN`. Each PR gets exactly one `Resolves #<issue>` line pointing to a dedicated `Planning task t-...` Issue, so the trusted PR->task resolver auto-resolves cleanly and the post-run writer publishes the plan fixture and receipt.

## Scope

- In scope: data/planning-side only. One Planning task card per PR family in `baseharbor-plan/tasks`, one GitHub Issue per card (title exactly `Planning task t-...`), and exactly one `Resolves #<issue>` line added to each PR body. `render` + `check` of Planning after card edits.
- Out of scope: no product code, no workflow-code change, no `receipt_tasklink.py` change, no closing other owners' issues, no subagent spawn.

## Acceptance

- Each target PR body contains exactly one `Closes/Fixes/Resolves #<issue>` reference (existing body preserved).
- Each referenced Issue title matches `t-[a-z0-9-]+` (a valid Planning task) so `resolve_task_from_pr` returns a `tasks/<id>.md` reference.
- Plan fixture commit produced per PR by the writer; post-run runs reach a terminal GREEN state.

## Required checks

- `python3 scripts/plan.py render` and `python3 scripts/plan.py check` pass after every card metadata edit; publish refreshed views to main.
- Every red post-run run resolved individually from its log-fundstelle before concluding.

## Dependencies and file ownership

- Owned area: planning-side task links only. No write to `baseharbor` product files or workflows.

## Handoff

- Current state: planning task cards + Issues created; PR bodies patched with single `Resolves #<issue>`; post-run runs watched to terminal. Newest first.
