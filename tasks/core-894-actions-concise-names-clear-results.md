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

- [ ] core-894 · Actions: use concise names and clear results #task #release/v0-4-26 #status/active #view/active #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (core-894 Actions presentation)  
    **PR:** [baseharbor#982](https://github.com/mcpdev80/baseharbor/pull/982)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
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

- 2026-10-17 continuation — **ACTIVE, not a complete review handoff**. PR #982 now includes an executable regression `scripts/test_pr_actions_summary.py` which extracts and executes the actual inline Summary Python from `ci.yml`. Cases include success, failure, blocked/missing conclusion, mandatory/nonmandatory skips, plan-marked verified reuse, missing/incomplete plan, missing/empty API, runtime required skip, elapsed times and links. The unchanged required-check context and machine evidence IDs remain authoritative. Hosted source `fa353d6095761a33ce321d8d13458e3520df40e7` [run 39027000092](https://github.com/mcpdev80/baseharbor/actions/runs/39027000092) had focused tests PASS and required final COVERAGE-UNRESOLVED; source `9d832eda6d1ad629ebc26fa8a5e26a521251d6ab` [run 39027171441](https://github.com/mcpdev80/baseharbor/actions/runs/39027171441) exposed a test fixture error (empty API response rightly classified as blocked while the reuse fixture expected a populated job list). That regression fixture is fixed at `1376c733a9d88287c5fb6df7fc20df985c27f85c` and [run 39027285412](https://github.com/mcpdev80/baseharbor/actions/runs/39027285412) is under evaluation. No runtime-for-display tests, merge, coverage bypass or acceptance. GitHub platform/contract boundary: matrix job names are kept exact for the authenticated verifier, PR run names cannot know dynamically computed selected gates before the planner runs, and skipped/helper jobs may remain visible in the job graph; changing trust/executor/job graph is out of this scope.
- Planning render/check/tests remain **NOT EXECUTED** in this environment: `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git HEAD` fails with `Could not resolve host: github.com`; GitHub MCP can read and update individual files, but exposes no repository checkout/archive or workflow dispatch. Searching for an existing alternative yielded only file-level operations and push-triggered CI that cannot be invoked/inspected as a local render/check run here. Derived CardBoard/Ready views are updated by exact file operations, NOT a substitute for generated `plan.py render/check`. The independent CI coverage qualification for `.github/workflows/ci.yml` plus the new test file remains a separate prerequisite to review acceptance.

- 2026-10-17 independent coverage qualification required — **REVIEW / NOT ACCEPTED**. The exact product candidate is [PR #982](https://github.com/mcpdev80/baseharbor/pull/982), head `46ff7af132a7fe07868f3bf2101771cf2d50b87b`, based on develop `d54ac358fb6a6b256164ac2689a33e981c013baa`. Single-file diff `.github/workflows/ci.yml`: one run-name change and an always-run, presentation-only summary step; no touched trusted selectors, executor, verifier or required check name. Hosted [Actions run 39026546388](https://github.com/mcpdev80/baseharbor/actions/runs/39026546388), attempt 1: Workflow policy, PR Trusted Plan, PR Focused Python, ci-actionlint, ci-policy, ci-executor-verifier-tests and pr-planner-tests all **SUCCESS**; final `PR Selected Checks` **FAILURE** on `coverage-unresolved: workflow execution/cleanup/evidence impact requires native qualification: .github/workflows/ci.yml`. The summary step itself ran successfully after that failure. This fail-closed outcome is not an implementation/test pass or a self-exemption. Independent qualification of the exact diff is needed; do not initiate native runtime just for display, waive protection or merge. Existing success [38891345247](https://github.com/mcpdev80/baseharbor/actions/runs/38891345247) and intentional error [38891065971](https://github.com/mcpdev80/baseharbor/actions/runs/38891065971) were inspected. Planning views were updated via GitHub file operations, but repository-local `plan.py render/check`, planning tests and Obsidian GUI were not executed from the connector-only environment. No acceptance or merge.

- 2026-10-17 candidate: [PR #982](https://github.com/mcpdev80/baseharbor/pull/982), source `46ff7af132a7fe07868f3bf2101771cf2d50b87b`, branch `feature/core-894-actions-presentation`, based on develop `d54ac358fb6a6b256164ac2689a33e981c013baa`. Scope: `.github/workflows/ci.yml` presentation-only. Required context `PR Selected Checks`, authenticated job names, gate IDs and selected execution remain unchanged. PR CI [39026546388](https://github.com/mcpdev80/baseharbor/actions/runs/39026546388) started; not yet asserted green or accepted. Existing positive [38891345247](https://github.com/mcpdev80/baseharbor/actions/runs/38891345247) and negative [38891065971](https://github.com/mcpdev80/baseharbor/actions/runs/38891065971) inspected. Runtime checks not launched for display. Planning render/check and Obsidian verification are pending; do not mark task reviewed or accepted.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
