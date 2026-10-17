---
id: core-914
areas: [wizard]
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: "mcpdev80 (core-914)"
depends_on: [core-910, t-20261016-wizard-task-ci-readiness]
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#962"]
sources: ["mcpdev80/baseharbor#914"]
source_updated: "2026-10-15T16:46:40Z"
labels: [area/dx]
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/962", "https://github.com/mcpdev80/baseharbor/commit/30d635b827e86d233030746abc65ce9475516ce0", "https://github.com/mcpdev80/baseharbor/actions/runs/38892885506"]
---

- [x] core-914 · Preview: present the actual footprint concisely #task #release/v0-4-26 #status/closed #view/closed #board/planned #area/wizard #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (core-914)  
    **PR:** [baseharbor#962](https://github.com/mcpdev80/baseharbor/pull/962)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/962), [proof 2](https://github.com/mcpdev80/baseharbor/commit/30d635b827e86d233030746abc65ce9475516ce0), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/38892885506)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-910](core-910-wizard-shared-read-only-editing-state.md), [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md)  
**Required by:** [core-916](core-916-wizard-back-cancel-eof-no-side-effects.md), [core-919](core-919-footprint-cli-json-one-projection.md), [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md)  
**Owner:** mcpdev80 (core-914)  
**Priority:** not set  
**PRs:** [baseharbor#962](https://github.com/mcpdev80/baseharbor/pull/962)  
**Source:** [baseharbor#914](https://github.com/mcpdev80/baseharbor/issues/914)
<!-- /generated:links -->

## Goal

The New/Edit preview explains required services and incremental resource needs in a few lines. Lane: read-only presentation.

## Scope

- In scope: separate footprint presenter files and tests in the existing presentation area.
- Out of scope: resolver changes; `internal/application/footprint.go` is consumed only.

## Acceptance

- Shows new/reused/stopped/unverified realizations correctly; running/additional containers are not guessed from capability names.
- RAM/container values distinguish measured, estimated and unknown; no invented zeros or seemingly exact sums.
- Explains zero-core and genuine dependencies, details optional; output is secret-free.

## Required checks

- Fixtures for empty, reuse/new, unknown capacity, real transitive dependencies and incomplete facts; no runtime.

## Dependencies and file ownership

- Depends on core-910. Shared v0.4.26 PR/review/runner foundation (#890–#893, #895, #896) must be qualified first.

## Autonomous execution contract — 2026-10-16

- **Owned files:** `cmd/baha/app_footprint_presenter.go` and `cmd/baha/app_footprint_presenter_test.go` only.
- **Delivered interface/result:** Consume the existing `application.Footprint` from `GuidedReadContext`; deliver a pure human-readable projection with optional details. New presentation-specific options/types stay in this file.
- **Task-specific proof:** `TestAppFootprintPresenter*`: empty/coreless, reused/new/stopped/unverified, measured/estimated/unknown, transitive/incomplete facts and secret-free output.
- **Boundary:** No changes to `internal/application/footprint.go`, footprint authority, CLI command/JSON schema, consequence presenter or shared rendering helpers.
- **Assignment gate:** use only accepted dependencies and APIs already present on develop. Confirm that the trusted plan/executor runs these exact test families on this task's file set and checks their outcomes. A plan that reports unresolved is not execution-ready. The CI-readiness inventory is maintained by [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md); later gaps become an explicit prerequisite before assignment, never an instruction to wait for another running session.
- **End-to-end owner:** the assigned session handles integration, implementation, focused tests, hosted CI observation, demonstrated fixes and its planning handoff. It reads other task states itself from planning main and preserves concurrent updates. No shared CI edits, dependency work-in-progress or manual message relay through Marcel. Normal independent review/Maintainer acceptance remains a boundary, not an implementation dependency.

## Handoff

- 2026-10-16 independent Maintainer acceptance: **accepted and merged**, [product PR #962](https://github.com/mcpdev80/baseharbor/pull/962), squash commit `30d635b827e86d233030746abc65ce9475516ce0` on product `develop`. Reviewed source `a779e45b435324d1b2f522698f8dffe599353dca` against the existing `application.Footprint` and `GuidedReadContext` authorities; only the two owned presenter/test files changed. Original [Actions run 38892885506](https://github.com/mcpdev80/baseharbor/actions/runs/38892885506), attempt 1, is SUCCESS and checks integration `b3177d5a94a50858e5d6a3dd54275237e0d8d1db` over trusted base `c889ba7f5350e978d6c372cd58f50651d4852e72`. Logs independently confirm all five presenter tests and the green mandatory final check; format, source/contracts, CLI vet/build, focused Python and workflow policy are green. Unneeded native/runtime/HA/release jobs were skipped. No second resolver, guessed totals or writes were added. Current planning and the concurrent core-912 review were preserved; generated views are rendered and planning checks plus all 38 unit tests pass before publication. This closes the presenter component and unblocks core-919; later handlers, wiring and release qualification remain separately scoped.

- 2026-10-16 core-914 implementation handoff: [product PR #962](https://github.com/mcpdev80/baseharbor/pull/962), branch `task/core-914-footprint-presenter`, exact head `a779e45b435324d1b2f522698f8dffe599353dca`, base `c889ba7f5350e978d6c372cd58f50651d4852e72`. Diff owns only `cmd/baha/app_footprint_presenter.go` and `cmd/baha/app_footprint_presenter_test.go`. Implements a pure projection of `application.Footprint` consumed via `GuidedReadContext`: separate new/reused-running/stopped-owned/unverifiable counts, explicit authoritative Core requirement, unknown/incomplete state, optional per-provider measured/estimated/unknown RAM and container evidence, verified/transitive/unknown dependencies, no inferred totals or mutations. `TestAppFootprintPresenter*` tests cover empty/core-free, mixed state, evidence classification, transitive dependency and incomplete snapshot, and no exposure of context revisions. Existing regular targeted [Actions run 38892885506](https://github.com/mcpdev80/baseharbor/actions/runs/38892885506) covers exact PR integration and is the authoritative check; previously [38892653643](https://github.com/mcpdev80/baseharbor/actions/runs/38892653643) confirmed wizard tests, source/contracts, vet/build and focused Python green, but formatting failed; later formatting corrections are included in current head. `PR Selected Checks` SUCCESS in [Actions 38892885506](https://github.com/mcpdev80/baseharbor/actions/runs/38892885506), together with Trusted Plan, Workflow policy, Focused Python, `wizard-footprint-presenter-tests`, `source-contracts`, `cli-gofmt`, `cli-vet` and `cli-build`. The native/HA/release/candidate and legacy broad validate jobs were correctly skipped. Exact current `develop` is the tested target `c889ba7f5350e978d6c372cd58f50651d4852e72`, so no additional develop merge was needed. No container or release matrix. **Independent review required**; do not self-merge or self-accept.


The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
