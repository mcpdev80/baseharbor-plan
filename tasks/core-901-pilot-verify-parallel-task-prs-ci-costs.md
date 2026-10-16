---
id: core-901
areas: [ci]
type: task
release: v0.4.26
version: ""
parent: core-888
owner: ""
depends_on: [core-893, core-894, core-895, core-896, core-900]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#901"]
source_updated: "2026-10-15T16:47:38Z"
labels: [area/evidence]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-901 · Pilot: verify parallel task PRs and CI costs #task #release/v0-4-26 #status/planned #view/waiting #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Waiting for prerequisites**  
    **Needs:** [core-894](core-894-actions-concise-names-clear-results.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Parent:** [core-888](../epics/core-888-development-and-ci.md)  
**Depends on:** [core-893](core-893-ci-enforce-selected-pr-checks.md), [core-894](core-894-actions-concise-names-clear-results.md), [core-895](core-895-reviews-require-maintainer-approval.md), [core-896](core-896-runners-isolate-parallel-pr-checks.md), [core-900](core-900-gc-preserve-active-prs-candidates-evidence.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#901](https://github.com/mcpdev80/baseharbor/issues/901)
<!-- /generated:links -->

## Goal

Qualify the new workflow with necessary regular work and own the before/after documentation.

## Scope

- In scope: two independent small PRs in parallel, one shared-interface or conflict case, cost record.
- Out of scope: extra full matrix for benchmarking; final release evidence (a separately authorized step). This task does not block early independent product work after a qualified PR/review/runner foundation.
- The accepted core-752/#935 and core-910/#934 histories are existing pilot evidence. Analyze them rather than implementing/reproducing an already fixed defect. Establish actual overlap and the shared-interface case from timestamps and supporting PRs; do not assume that two completed PRs prove parallel execution. This gives #750/#751/#754/#766 no new release target.

## Acceptance

- Two independent small PRs in parallel; one case with a shared interface/pre-contract or conflict resolution without overwriting.
- Selection, fail-closed, review, runners and candidate handoff of the predecessor packages are traced together; an independent final review is documented.
- Run/attempt, SHAs, runner, scope, newly run/reused gates, wall time and runner minutes before/after.
- Real savings demonstrated or remaining costs documented honestly; no invented targets.

## Required checks

- Existing green runs and necessary small regular pilot PRs.

## Dependencies and file ownership

- Satisfied: #890, #891, #892, #897, #898, #899 (closed). Open: as listed.

## Autonomous execution contract — 2026-10-16

- **Owned files:** New `docs/internal/v0.4.26-parallel-pr-pilot.md` and dedicated evidence fixtures only; no CI/product implementation edits.
- **Delivered interface/result:** One evidence-backed comparison and explicit limitations, accepted independently of the remaining feature implementations.
- **Task-specific proof:** Use existing runs for #934/#935 and their supporting CI PRs first; collect run/job/attempt, duration and concurrency facts. No extra benchmark run.
- **Boundary:** Do not wait for sessions to send measurements. Fetch logs directly. If history does not establish a criterion, state the gap and use only the next already-required regular run; no synthetic savings.
- **Assignment gate:** use only accepted dependencies and APIs already present on develop. Confirm that the trusted plan/executor runs these exact test families on this task's file set and checks their outcomes. A plan that reports unresolved is not execution-ready. The CI-readiness inventory is maintained by [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md); later gaps become an explicit prerequisite before assignment, never an instruction to wait for another running session.
- **End-to-end owner:** the assigned session handles integration, implementation, focused tests, hosted CI observation, demonstrated fixes and its planning handoff. It reads other task states itself from planning main and preserves concurrent updates. No shared CI edits, dependency work-in-progress or manual message relay through Marcel. Normal independent review/Maintainer acceptance remains a boundary, not an implementation dependency.

## Handoff

- Not started.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
