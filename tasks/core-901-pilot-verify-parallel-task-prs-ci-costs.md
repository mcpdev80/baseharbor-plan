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
    **Needs:** [core-893](core-893-ci-enforce-selected-pr-checks.md), [core-894](core-894-actions-concise-names-clear-results.md), [core-895](core-895-reviews-require-maintainer-approval.md), [core-896](core-896-runners-isolate-parallel-pr-checks.md), [core-900](core-900-gc-preserve-active-prs-candidates-evidence.md)  
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
- Selected product pilot: core-752 (default-instance reconciliation, target v0.4.26). Reproduce the current defect first; focused package/consumer checks, no full E2E only for this fix. If it is already fixed, do not fabricate one: pick another independently confirmed small defect after an explicit scope check. The second independent PR and the shared-interface case remain separate pilot requirements. This gives #750/#751/#754/#766 no new release target.

## Acceptance

- Two independent small PRs in parallel; one case with a shared interface/pre-contract or conflict resolution without overwriting.
- Selection, fail-closed, review, runners and candidate handoff of the predecessor packages are traced together; an independent final review is documented.
- Run/attempt, SHAs, runner, scope, newly run/reused gates, wall time and runner minutes before/after.
- Real savings demonstrated or remaining costs documented honestly; no invented targets.

## Required checks

- Existing green runs and necessary small regular pilot PRs.

## Dependencies and file ownership

- Satisfied: #890, #891, #892, #897, #898, #899 (closed). Open: as listed.

## Handoff

- Not started.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
