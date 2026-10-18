---
id: core-894
areas: [ci]
type: task
release: v0.4.26
version: ""
parent: core-888
owner: "ChatGPT (core-894 implementation correction)"
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
    **Owner:** ChatGPT (core-894 implementation correction)  
    **PR:** [baseharbor#982](https://github.com/mcpdev80/baseharbor/pull/982)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Parent:** [core-888](../epics/core-888-development-and-ci.md)  
**Depends on:** [core-893](core-893-ci-enforce-selected-pr-checks.md), [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md)  
**Required by:** [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md)  
**Owner:** ChatGPT (core-894 implementation correction)  
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

### 2026-10-18 — #982 runtime identity correction accepted at source review
- [Review 5562557813](https://github.com/mcpdev80/baseharbor/pull/982#pullrequestreview-5562557813) inspected exact `0ab44b7edb94618489cb505cf897ff7e6d73da6c`: per-selected-gate actual runtime identities used consistently; prior evidence/missing-data corrections retained. No further source blocker found.
- Actual CI 39117993099 selected checks successful; Focused Python log confirms 17 Summary regressions actually executed successfully. Finalcheck still unresolved for the exact two-file presentation change relative to trusted 980e8db8.
- Prepare a finite separately reviewed trusted-policy binding to this exact source and complete statuses (.github/workflows/ci.yml modified, scripts/test_pr_actions_summary.py added), with existing CI/actionlint checks and mandatory Focused Python preserved. No native work or authoritative gate/trust changes needed for this presentation-only record.
- Formal policy approval, green product finalcheck and final acceptance remain open. No local/native reviewer execution or merge.


- **2026-10-18 — Review 5562473769 implementation handoff.** Existing PR #982, exact SHA `0ab44b7edb94618489cb505cf897ff7e6d73da6c`, normal two-parent integration of current develop `980e8db8b93c09db61ac8a0ea873bc6f43d1dedf` (parent is prior #982 head `0f3fe35ee484ac9e8be4bec43bf1ef2599a7b369`). The embedded Summary now derives one exact Actions reusable-matrix child name per `atomic/docker/<suite>` or `atomic/podman/<suite>` gate using the observed format `PR · Selected Runtime (atomic/podman/lifecycle, podman, lifecycle) / podman · lifecycle`. The same exact name determines presence and whether a skipped job is required; unrelated prefixed names never count and a child cannot satisfy another gate. Actual `PR · Public Contracts` reusable name is checked explicitly. No trusted planner, runner, verifier, gate or security rule changes. All 17 real embedded Python Summary regressions PASS, including the original nine and new actual-name fixtures: https://huggingface.co/jobs/ThunderHawk1080/6ad49a5bc662881452272d22 . GitHub targeted run [39117993099](https://github.com/mcpdev80/baseharbor/actions/runs/39117993099): Trusted Plan, workflow policy, Focused Python, ci-policy, actionlint, pr-planner and executor-verifier validations SUCCESS; required `PR Selected Checks` FAILURE only with `coverage-unresolved` for `.github/workflows/ci.yml` and `scripts/test_pr_actions_summary.py`. The strict native qualification remains open; no runtime or live tests. **Exact SHA handed to Manager for independent review; no self-qualification, coverage exception or merge.**

### 2026-10-18 — Correction review: real runtime-job identity gap
- [Review 5562473769](https://github.com/mcpdev80/baseharbor/pull/982#pullrequestreview-5562473769) inspected exact `0f3fe35ee484ac9e8be4bec43bf1ef2599a7b369`: original evidence/seconds and missing exact-name job findings addressed; new runtime identity correction required.
- Actual native API names include selected-gate matrix and reusable child suffixes, not the synthetic `PR · Selected Runtime` parent. Current exact required-minus-seen check falsely lists missing runtime parent on complete successful native results and treats skipped selected children as not required. Require per-selected-gate actual-job mapping and regressions for complete, one missing, skipped and unrelated children. No authoritative gate/trust behavior change.
- integration_sha_mismatch was independently explained: CI expected old base `d54ac358`, while integration f538356e1e63bc77a39a38e2fcb533fbb2610af2 actually parents trusted `980e8db8` and candidate `0f3fe35e`. Normal current develop integration/fresh CI required; never bypass stale-input rejection.
- No new reviewer Python/native execution, source qualification or merge. Existing implementation claim/status/generated metadata preserved pending validated implementation handoff.


- **2026-10-18 — Implementation correction handoff.** Addressed independent review [5562367686](https://github.com/mcpdev80/baseharbor/pull/982#pullrequestreview-5562367686) in the same [PR #982](https://github.com/mcpdev80/baseharbor/pull/982), exact new candidate `0f3fe35ee484ac9e8be4bec43bf1ef2599a7b369`. Display-only Summary now rejects foreign/malformed/unverified reused evidence URLs and renders invalid durations as `duration unknown`; missing required API jobs are explicitly shown in **Blocked** even if response is nonempty. The currently running `PR Selected Checks` is excluded only from missing-job detection, because its conclusion is not yet available. Twelve real embedded-Summary tests (nine original plus three new) PASS on exact SHA: https://huggingface.co/jobs/ThunderHawk1080/6ad497145ccb47ba0f7c332b . Github CI run [39117096551](https://github.com/mcpdev80/baseharbor/actions/runs/39117096551) is the targeted candidate run; required final/coverage outcome must be interpreted separately. No authoritative runner, policy, trust, gates, product or #983/#991 changes; no self-review, coverage exemption, native tests or merge. **Hand off this exact SHA to Manager for independent review.**

- **2026-10-18 — Role change/claim.** Maintainer assigns this session as core-894 implementer on existing PR #982, addressing independent review [5562367686](https://github.com/mcpdev80/baseharbor/pull/982#pullrequestreview-5562367686). Scope: invalid verified reuse URLs/duration data and missing mandatory API jobs in the embedded display-only summary; preserve all nine existing tests and authoritative runner/finalcheck protections. No self-qualification, merge, or edits to #983/#991.

- **2026-10-17 — Review handoff, no acceptance or merge.** Product [PR #982](https://github.com/mcpdev80/baseharbor/pull/982) stays unchanged at HEAD `10550e9dcecffdf539f5bf1393807c42e4506add`. The scoped display change provides concise Actions run naming and a non-authoritative Summary separating checked, reused, not required, failed and blocked work, with job duration and links. Existing required context `PR Selected Checks`, authenticated job names, technical evidence IDs, gate selection, trust and concurrency are preserved. GitHub's skipped/support jobs remain visible in the graph; selected runtime/capability cannot be embedded into a static pre-planning run name.
- **Product evidence:** [Actions 39027425378](https://github.com/mcpdev80/baseharbor/actions/runs/39027425378), attempt 1: focused Python **SUCCESS** (nine regressions executing the actual embedded Summary: success, failure, blocked, required/non-required skip, verified reuse, missing API/plan data), plus workflow policy, actionlint, planner and executor/verifier validation **SUCCESS**. Required `PR Selected Checks` **FAILURE**, explicitly `coverage-unresolved` for `.github/workflows/ci.yml` and `scripts/test_pr_actions_summary.py`. Independent trusted-coverage qualification of this exact candidate is the remaining product prerequisite. No self-exemption, runtime-for-display test, merge or acceptance.
- **Planning evidence:** [Plan · validate 39029152951](https://github.com/mcpdev80/baseharbor-plan/actions/runs/39029152951) for own Planning commit `14fb73f36be9616cbe39f9b5a34e6ca8db6958b4`: **SUCCESS**, all 47 planning tests **PASS** and `python3 scripts/plan.py check` executed successfully on GitHub. No local execution claimed; it is not an additional blocker for the verified commit.
- **Separate later failure:** [Planning 39029297275](https://github.com/mcpdev80/baseharbor-plan/actions/runs/39029297275) **FAILURE**, unrelated newer generated drift at `tasks/core-751-inspect-no-false-positives-comments-text.md`, `views/overview.md` and `views/releases/v0.4.x.md`. Ownership and canonical text of core-751 remain untouched; no competing generated correction. Earlier 39027767084 drift diagnosis and claims that core-894 lacked validated Planning CI are **superseded** by the successful own run above.
- **Review boundary:** Hand off the unchanged product candidate for independent coverage qualification; do not accept or merge this task.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
