---
id: core-912
areas: [wizard]
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: "mcpdev80 (core-912 implementation)"
depends_on: [core-910, t-20261016-wizard-task-ci-readiness]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#912"]
source_updated: "2026-10-15T16:46:52Z"
labels: [area/dx]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-912 · Wizard: present a compact needs-first selection #task #release/v0-4-26 #status/active #view/active #area/wizard #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (core-912 implementation) · **Priority:** not set  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-910](core-910-wizard-shared-read-only-editing-state.md), [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md)  
**Required by:** [core-913](core-913-wizard-compatible-providers-same-view.md), [core-916](core-916-wizard-back-cancel-eof-no-side-effects.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#912](https://github.com/mcpdev80/baseharbor/issues/912)
<!-- /generated:links -->

## Goal

A compact keyboard checklist asks for developer needs instead of product names. Lane: TUI.

## Scope

- In scope: new dedicated `app_capability_selection` view/update files and tests.
- Out of scope: existing New/Init wizard entry points (changed only in the wiring task core-917).

## Acceptance

- One screen with Space/arrow keys; SQL, cache, protected secrets, app login and TLS/HTTPS as examples; further supported capabilities disclosed progressively.
- Zero selection is valid; detected suggestions are visible and deselectable; no implicit SQL/Identity/OpenBao/management bundle requirement.
- App login, operator/team access and service credentials are separated in wording and semantics; existing capability catalogs are used.

## Required checks

- Deterministic TUI update/view tests for selection, zero, preselection, keyboard and extended needs; no runtime.

## Dependencies and file ownership

- Depends on core-910.

## Autonomous execution contract — 2026-10-16

- **Owned files:** `cmd/baha/app_capability_selection.go` and `cmd/baha/app_capability_selection_test.go` only.
- **Delivered interface/result:** Expose a compiling component with explicit input/current-selection state and output capability requirements. Keep provider selection as an extension point owned by the later core-913 integration; no dependency on a future implementation.
- **Task-specific proof:** `TestAppCapabilitySelection*`: key transitions, zero selection, detected suggestions, progressive disclosure and wording separation.
- **Boundary:** No edit to New/Init entry points, hydration, presenters, controller or command registration. Capability facts come from the merged existing catalog/context.
- **Assignment gate:** use only accepted dependencies and APIs already present on develop. Confirm that the trusted plan/executor runs these exact test families on this task's file set and checks their outcomes. A plan that reports unresolved is not execution-ready. The CI-readiness inventory is maintained by [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md); later gaps become an explicit prerequisite before assignment, never an instruction to wait for another running session.
- **End-to-end owner:** the assigned session handles integration, implementation, focused tests, hosted CI observation, demonstrated fixes and its planning handoff. It reads other task states itself from planning main and preserves concurrent updates. No shared CI edits, dependency work-in-progress or manual message relay through Marcel. Normal independent review/Maintainer acceptance remains a boundary, not an implementation dependency.

## Handoff

- Not started.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
