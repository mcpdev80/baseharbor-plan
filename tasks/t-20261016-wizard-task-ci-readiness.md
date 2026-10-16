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
prs: [mcpdev80/baseharbor#957]
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261016-wizard-task-ci-readiness · CI: prepare autonomous wizard task verification #task #release/v0-4-26 #status/review #view/review #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (CI readiness session) · **Priority:** not set  
    **PR:** [baseharbor#957](https://github.com/mcpdev80/baseharbor/pull/957)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Parent:** [core-888](../epics/core-888-development-and-ci.md)  
**Depends on:** [core-893](core-893-ci-enforce-selected-pr-checks.md), [core-895](core-895-reviews-require-maintainer-approval.md), [core-896](core-896-runners-isolate-parallel-pr-checks.md), [core-910](core-910-wizard-shared-read-only-editing-state.md)  
**Required by:** [core-894](core-894-actions-concise-names-clear-results.md), [core-911](core-911-app-edit-load-existing-selections.md), [core-912](core-912-wizard-needs-first-selection.md), [core-914](core-914-preview-actual-footprint.md), [core-915](core-915-preview-provider-consequences-partial-results.md)  
**Owner:** mcpdev80 (CI readiness session)  
**Priority:** not set  
**PRs:** [baseharbor#957](https://github.com/mcpdev80/baseharbor/pull/957)  
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

- 2026-10-16 independent review of source `eff029a85a75ad6041d83ecc264c4f521ce02795` / PR #957: **CHANGES REQUESTED; NOT ACCEPTED**. Original [Actions 38886891093](https://github.com/mcpdev80/baseharbor/actions/runs/38886891093) really ran the four temporary Go executor fixtures and the zero-match regression; relevant Python/planner/policy jobs succeeded and the actual final check failed closed. Independently validated planning main with all 38 tests and `plan.py check` (0 errors/warnings); review status, owner, PR and predecessor states are honest.
  - Concrete correctness gap: `wizard-change-presentation-tests` uses a single OR regex and requires only one discovered match. A direct counterexample against the real runner accepts `TestAppChangePreviewOnly` when the entire `TestAppChangeResultPresenter*` family is absent. Require every mandatory family within a combined profile; add positive and missing-each-family regressions. Apply the same rule to the combined Edit/registration profiles that claim multiple required families. Successful process exit must not stand in for actual required test execution.
  - Qualification gap: the successful Go fixtures call the Python executor directly. The actual workflow `wizard-*-tests` case (trusted-base helper loading plus execution) was not selected/exercised in the reported run. Qualify that exact production route with bounded hosted evidence, including a negative missing-family case. Keep temporary fixtures out of develop. The existing always-running final check still has no green reviewed integration for this PR; independent policy bootstrap, integration and final proof remain part of this SAME task, without self-exemption, required-check bypass or a new implementation owner.
  - Refresh normally against current develop after the independent core-901 documentation merge; preserve all source changes and no force push. Do not claim ordinary trusted-target integration from substituted SHA strings alone where actual integration/executor behavior is at issue.
  - Planning follow-through: the noted future core-921 registration-coverage prerequisite is currently prose only. Either provide its qualified lane here or schedule the concrete prerequisite and attach it to core-921 dependencies before that task can become assignable. No hidden later-session dispatch/CI handoff. core-911/912/914/915 remain waiting until this task has actually qualified and been accepted.

- 2026-10-16 review handoff — product PR [baseharbor#957](https://github.com/mcpdev80/baseharbor/pull/957), branch `ci/wizard-task-readiness-20261016`.
  - Exact product source HEAD: `eff029a85a75ad6041d83ecc264c4f521ce02795`; trusted target/base: `9766dcb89dbe0551321b1bf070ab3013d3353c49`; Actions integration: `6a32b31d2e91da888606e120df6677def8b63d68`.
  - Hosted qualification run: [38886891093](https://github.com/mcpdev80/baseharbor/actions/runs/38886891093). SUCCESS: `PR · Trusted Plan`, `Workflow policy`, `PR · Focused Python`, `PR · Validation · pr-planner-tests`, `PR · Validation · ci-executor-verifier-tests`, `PR · Validation · ci-policy`.
  - `PR · Focused Python` executed real temporary Go fixtures for `TestAppEditLoad*`, `TestAppCapabilitySelection*`, `TestAppFootprintPresenter*` and `TestAppChangePreview*`, plus the explicit zero-matching-tests failure case. This is execution evidence, not discovery-only evidence.
  - First-wave inventory: core-911 exact `app_edit_load*.go` -> source/contracts + cmd/baha gofmt/vet/build + `wizard-app-edit-load-tests`; core-912 exact `app_capability_selection*.go` -> same base checks + `wizard-capability-selection-tests`; core-914 exact `app_footprint_presenter*.go` -> same base checks + `wizard-footprint-presenter-tests`; core-915 exact change-preview/result-presenter files -> same base checks + `wizard-change-presentation-tests`. These four profiles select no runtime gate.
  - Later finite profiles are planned for provider choice, controller, footprint command and machine adapters without runtime; New/Edit mutation wiring selects only existing Docker/Podman lifecycle gates. Unknown/nested/helper files and rename/delete/type changes remain fail-closed unresolved.
  - No Runtime, Demo, Public Contracts, full release matrix or Hugging Face lane ran for this qualification.
  - Binding final result: `PR Selected Checks` failed as intended because the currently trusted develop planner classifies this PR's own `.github/workflows/ci.yml` / executor / verifier changes as unresolved CI impact. No self-exemption or immutable-HEAD bootstrap was added. Independent Maintainer review/integration is therefore still required; this task is **review**, not accepted, and core-911/912/914/915 are not yet assignable.
  - Remaining later boundary: shared core-921 command/MCP registration files remain conservative rather than receiving a path-only exemption. A separately scheduled/accepted registration-CI prerequisite is required before core-921 assignment if the eventual shared-file diff cannot be proven by an already trusted executor after this PR is integrated.

