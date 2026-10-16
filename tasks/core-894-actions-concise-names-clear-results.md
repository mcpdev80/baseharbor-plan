---
id: core-894
areas: [ci]
type: task
release: v0.4.26
version: ""
parent: core-888
owner: ""
depends_on: [core-893, t-20261016-wizard-task-ci-readiness]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#894"]
source_updated: "2026-10-15T16:48:23Z"
labels: [area/dx]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-894 · Actions: use concise names and clear results #task #release/v0-4-26 #status/planned #view/ready #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Parent:** [core-888](../epics/core-888-development-and-ci.md)  
**Depends on:** [core-893](core-893-ci-enforce-selected-pr-checks.md), [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md)  
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

## Autonomous execution contract — 2026-10-16

- **Owned files:** `.github/workflows/ci.yml` display/summary expressions; display strings in existing selected-check helpers only when necessary, named explicitly in the PR.
- **Delivered interface/result:** An independently reviewable display/summary change; no execution, trust, concurrency, admission or gate-selection redesign.
- **Task-specific proof:** Existing workflow-policy/actionlint and summary fixtures; inspect existing success/failure runs. Keep required context `PR Selected Checks` and evidence IDs unchanged.
- **Boundary:** Do not overlap the CI-readiness task. Never launch a runtime merely to obtain a prettier screenshot.
- **Assignment gate:** use only accepted dependencies and APIs already present on develop. Confirm that the trusted plan/executor runs these exact test families on this task's file set and checks their outcomes. A plan that reports unresolved is not execution-ready. The CI-readiness inventory is maintained by [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md); later gaps become an explicit prerequisite before assignment, never an instruction to wait for another running session.
- **End-to-end owner:** the assigned session handles integration, implementation, focused tests, hosted CI observation, demonstrated fixes and its planning handoff. It reads other task states itself from planning main and preserves concurrent updates. No shared CI edits, dependency work-in-progress or manual message relay through Marcel. Normal independent review/Maintainer acceptance remains a boundary, not an implementation dependency.

## Handoff

- Not started.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
