---
id: core-894
areas: [ci]
type: task
release: v0.4.26
version: ""
parent: core-888
owner: "mcpdev80 (core-894 Actions presentation)"
depends_on: [core-893, t-20261016-wizard-task-ci-readiness]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#982]
sources: ["mcpdev80/baseharbor#894"]
source_updated: "2026-10-15T16:48:23Z"
labels: [area/dx]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-894 · Actions: use concise names and clear results #task #release/v0-4-26 #status/review #view/review #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (core-894 Actions presentation)  
    **PR:** [baseharbor#982](https://github.com/mcpdev80/baseharbor/pull/982)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Parent:** [core-888](../epics/core-888-development-and-ci.md)  
**Depends on:** [core-893](core-893-ci-enforce-selected-pr-checks.md), [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md)  
**Required by:** [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md)  
**Owner:** mcpdev80 (core-894 Actions presentation)  
**Priority:** not set  
**PRs:** [baseharbor#982](https://github.com/mcpdev80/baseharbor/pull/982)  
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

- **2026-10-17 — Review handoff, no acceptance or merge.** Product [PR #982](https://github.com/mcpdev80/baseharbor/pull/982) stays unchanged at HEAD `10550e9dcecffdf539f5bf1393807c42e4506add`. The scoped display change provides concise Actions run naming and a non-authoritative Summary separating checked, reused, not required, failed and blocked work, with job duration and links. Existing required context `PR Selected Checks`, authenticated job names, technical evidence IDs, gate selection, trust and concurrency are preserved. GitHub's skipped/support jobs remain visible in the graph; selected runtime/capability cannot be embedded into a static pre-planning run name.
- **Product evidence:** [Actions 39027425378](https://github.com/mcpdev80/baseharbor/actions/runs/39027425378), attempt 1: focused Python **SUCCESS** (nine regressions executing the actual embedded Summary: success, failure, blocked, required/non-required skip, verified reuse, missing API/plan data), plus workflow policy, actionlint, planner and executor/verifier validation **SUCCESS**. Required `PR Selected Checks` **FAILURE**, explicitly `coverage-unresolved` for `.github/workflows/ci.yml` and `scripts/test_pr_actions_summary.py`. Independent trusted-coverage qualification of this exact candidate is the remaining product prerequisite. No self-exemption, runtime-for-display test, merge or acceptance.
- **Planning evidence:** [Plan · validate 39029152951](https://github.com/mcpdev80/baseharbor-plan/actions/runs/39029152951) for own Planning commit `14fb73f36be9616cbe39f9b5a34e6ca8db6958b4`: **SUCCESS**, all 47 planning tests **PASS** and `python3 scripts/plan.py check` executed successfully on GitHub. No local execution claimed; it is not an additional blocker for the verified commit.
- **Separate later failure:** [Planning 39029297275](https://github.com/mcpdev80/baseharbor-plan/actions/runs/39029297275) **FAILURE**, unrelated newer generated drift at `tasks/core-751-inspect-no-false-positives-comments-text.md`, `views/overview.md` and `views/releases/v0.4.x.md`. Ownership and canonical text of core-751 remain untouched; no competing generated correction. Earlier 39027767084 drift diagnosis and claims that core-894 lacked validated Planning CI are **superseded** by the successful own run above.
- **Review boundary:** Hand off the unchanged product candidate for independent coverage qualification; do not accept or merge this task.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
