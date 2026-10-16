---
id: core-916
areas: [wizard]
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: ""
depends_on: [core-912, core-913, core-914, core-915]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#916"]
source_updated: "2026-10-15T16:46:28Z"
labels: [area/dx]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-916 · Wizard: handle back, cancel and EOF without side effects #task #release/v0-4-26 #status/planned #view/waiting #area/wizard #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Waiting for prerequisites**  
    **Needs:** [core-912](core-912-wizard-needs-first-selection.md), [core-913](core-913-wizard-compatible-providers-same-view.md), [core-915](core-915-preview-provider-consequences-partial-results.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-912](core-912-wizard-needs-first-selection.md), [core-913](core-913-wizard-compatible-providers-same-view.md), [core-914](core-914-preview-actual-footprint.md), [core-915](core-915-preview-provider-consequences-partial-results.md)  
**Required by:** [core-917](core-917-app-new-connect-wizard-lifecycle.md), [core-918](core-918-app-edit-apply-confirmed-changes.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#916](https://github.com/mcpdev80/baseharbor/issues/916)
<!-- /generated:links -->

## Goal

No returns to the retained selection as often as needed; cancel writes nothing. Lane: TUI control.

## Scope

- In scope: separate wizard controller/state machine files and tests; components only through agreed interfaces.
- Out of scope: lifecycle or registry wiring.

## Acceptance

- Capability and provider selections and complex original data are retained on every return.
- Cancel/EOF/context cancel and unsuitable non-TTY/`--no-input` use cause no hidden file, profile, Target, credential or runtime writes.
- The preview controller and execution hook are cleanly separated; actual mutation only after existing valid consent.

## Required checks

- Sequence/PTY tests for repeated No, changed selection, abort at every transition and EOF; filesystem/state snapshots with controlled fakes; no runtime.

## Dependencies and file ownership

- Depends on core-912, core-913, core-914 and core-915. Shared v0.4.26 PR/review/runner foundation (#890–#893, #895, #896) must be qualified first.

## Autonomous execution contract — 2026-10-16

- **Owned files:** `cmd/baha/app_wizard_controller.go` and `cmd/baha/app_wizard_controller_test.go` only.
- **Delivered interface/result:** Compose the already accepted selection/provider/presenter components using their exported-to-package APIs. Return a decision and state to the caller; execution remains behind the existing authorized lifecycle hook.
- **Task-specific proof:** `TestAppWizardController*`: repeated back, retained dual selection, cancellation/EOF/context cancellation/non-TTY/no-input at every transition and no-write snapshots.
- **Boundary:** No changes to component internals, shared models or New/Edit registration. If a component contract is missing, repair it before this task is assigned, not while another session implements it.
- **Assignment gate:** use only accepted dependencies and APIs already present on develop. Confirm that the trusted plan/executor runs these exact test families on this task's file set and checks their outcomes. A plan that reports unresolved is not execution-ready. The CI-readiness inventory is maintained by [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md); later gaps become an explicit prerequisite before assignment, never an instruction to wait for another running session.
- **End-to-end owner:** the assigned session handles integration, implementation, focused tests, hosted CI observation, demonstrated fixes and its planning handoff. It reads other task states itself from planning main and preserves concurrent updates. No shared CI edits, dependency work-in-progress or manual message relay through Marcel. Normal independent review/Maintainer acceptance remains a boundary, not an implementation dependency.

## Handoff

- Not started.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
