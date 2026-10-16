---
id: t-20261016-wizard-task-ci-readiness
type: task
areas: [ci]
release: v0.4.26
version: ""
parent: core-888
owner: "mcpdev80 (CI readiness session)"
priority: ""
depends_on: [core-893, core-895, core-896, core-910]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261016-wizard-task-ci-readiness · CI: prepare autonomous wizard task verification #task #release/v0-4-26 #status/planned #view/ready #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (CI readiness session) · **Priority:** not set  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Parent:** [core-888](../epics/core-888-development-and-ci.md)  
**Depends on:** [core-893](core-893-ci-enforce-selected-pr-checks.md), [core-895](core-895-reviews-require-maintainer-approval.md), [core-896](core-896-runners-isolate-parallel-pr-checks.md), [core-910](core-910-wizard-shared-read-only-editing-state.md)  
**Required by:** [core-894](core-894-actions-concise-names-clear-results.md), [core-911](core-911-app-edit-load-existing-selections.md), [core-912](core-912-wizard-needs-first-selection.md), [core-914](core-914-preview-actual-footprint.md), [core-915](core-915-preview-provider-consequences-partial-results.md)  
**Owner:** mcpdev80 (CI readiness session)  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Before another product component is assigned, the trusted develop pipeline can execute and enforce the focused checks for its agreed files. A component session owns implementation through exact-integration CI and planning handoff without another session operating its test lane.

## Scope

- Own the bounded additions to `scripts/pr-gate-plan.py`, `scripts/pr-check-runner.py`, their existing tests and `.github/workflows/ci.yml`; use existing validation/executor/final-check infrastructure. No second planner, verifier or general change-impact framework.
- Read the explicit file/check inventories in core-911 through core-921. Prepare reusable check profiles for hydration, selection, provider choice, footprint/consequence presenters, controller, command adapters and command registration. Prepare the required source/format/vet/build/contract checks, plus selection of existing targeted native gates where mutation actually requires them. Later tasks must not need concurrent CI edits.
- Qualify the first four independent lanes (core-911/912/914/915) end to end on GitHub-hosted runners. Plan the remaining named lanes against their stated risk; if an existing native executor cannot provide a required later-task check, record a separately scheduled prerequisite before that task is assigned, not a mid-task handoff.
- No wizard/product implementation, stubs committed to develop to fake coverage, changes to product main/AGENTS/rulesets, provider catalog matrix or release qualification.

## Acceptance

- Finite reviewed file/profile mapping, not blanket `cmd/baha/**`, filename-only runtime exemption, label override or per-feature immutable-HEAD bootstrap. Unlisted/shared/lifecycle/provider/security changes remain unresolved unless their actual targeted risk is qualified.
- Every required check is executed and authenticated by the existing final check; actual component tests must run. The old `^TestGuided` filter alone is not coverage for new tests. Test-discovery assertions prevent zero matching tests from producing a misleading PASS.
- Positive fixtures cover every named first-wave file, test and ordinary trusted-target integration. Negative cases cover unknown/nested files, mutations outside declared boundaries, missing tests, missing/failed/cancelled results and stale input SHAs. Rename/delete handling stays conservative.
- A single bounded hosted qualification demonstrates the first-wave profiles and actual executor cases, with no runtime for pure hydration/presentation. The final required check is green on the reviewed integration. Establish the trusted-policy bootstrap within this same task if needed; do not create a new task or ask another implementation session to operate the lane. Independent Maintainer review is still required; no self-exemption.
- The task records exact run/job/source/integration evidence and a compact file-to-check inventory. Only after policy/executor changes are reviewed, merged and this task is accepted do core-911/912/914/915 become assignable. A planning change alone does NOT mean the product CI is ready.

## Required checks

- Existing planner/diff/check-runner/executor/final-verifier regression suites; workflow policy and actionlint; positive/negative profile tests and real hosted first-wave execution. One coherent candidate, inspect failures before a justified corrective push. No full release matrix or broad legacy validation job.

## Dependencies and file ownership

- All declared dependencies are already accepted. This task is the sole CI-file writer during preparation; core-894 follows it, and product component tasks never patch these shared files on the side.
- The session handles checkout, publishing, CI observation and evidence itself using its available connector/CLI. Read prerequisites and ownership directly from planning main. Marcel is not a message relay. An unavailable tool must be identified before accepting the assignment.
- Interface changes needed for another task are integrated here first. Do not publish a speculative promise that a future session will fill in an executor later.

## Handoff

- 2026-10-16 planning audit: newly scheduled prerequisite, not implemented/claimed/accepted. Product develop currently recognizes only the existing Guided read adapter and reviewed Inspect files; the new wizard files would otherwise be unresolved. This task closes that concrete execution-readiness gap before feature assignment.
