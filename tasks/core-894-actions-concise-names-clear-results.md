---
id: core-894
areas: [ci]
type: task
release: v0.4.26
version: ""
parent: core-888
owner: ""
depends_on: [core-893]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#894"]
source_updated: "2026-10-15T16:48:23Z"
labels: [area/dx]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-894 · Actions: use concise names and clear results #task #release/v0-4-26 #status/planned #view/waiting #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Waiting for prerequisites**  
    **Needs:** [core-893](core-893-ci-enforce-selected-pr-checks.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Parent:** [core-888](../epics/core-888-development-and-ci.md)  
**Depends on:** [core-893](core-893-ci-enforce-selected-pr-checks.md)  
**Required by:** [core-901](core-901-pilot-verify-parallel-task-prs-ci-costs.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#894](https://github.com/mcpdev80/baseharbor/issues/894)
<!-- /generated:links -->

## Goal

Titles and summaries explain trigger, result and next action within seconds.

## Scope

- In scope: run-name/job names, run summary, job graph shape, display-name alignment.
- Out of scope: a dedicated full end-to-end run.

## Acceptance

- Short run-name/job names with capability and runtime; SHA and technical gate IDs in details.
- The summary separates checked, reused, not required and failed/blocked, with durations and links.
- The graph is limited to planning, selected checks and the final check; unavoidable platform displays are documented.
- Display names match required checks/verifier; internal evidence IDs are not broken for cosmetics.

## Required checks

- Inspect existing or otherwise necessary small pilot runs in Actions, including a failure case.

## Dependencies and file ownership

- Depends on core-893.

## Handoff

- Not started.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
