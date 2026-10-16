---
id: core-913
areas: [wizard]
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: "mcpdev80 (core-913 implementation)"
depends_on: [core-910, core-912]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#913"]
source_updated: "2026-10-15T16:46:46Z"
labels: [area/dx]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-913 · Wizard: offer compatible providers in the same view #task #release/v0-4-26 #status/active #view/active #area/wizard #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (core-913 implementation) · **Priority:** not set  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-910](core-910-wizard-shared-read-only-editing-state.md), [core-912](core-912-wizard-needs-first-selection.md)  
**Required by:** [core-916](core-916-wizard-back-cancel-eof-no-side-effects.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#913](https://github.com/mcpdev80/baseharbor/issues/913)
<!-- /generated:links -->

## Goal

For a need, a compatible provider preference can be set in place; Automatic stays the default. Lane: provider view.

## Scope

- In scope: separate `app_provider_choice` files and tests, using only the agreed selection-component interface.
- Out of scope: checklist core files, central registry, resolver; persistence (not in this task).

## Acceptance

- Shows the current compatible providers/instances from the Target/registry/resolver result instead of a fixed product catalog.
- No additional mandatory screen; shows the proposed actual provider and reason; errors are concrete with no silent substitute.
- The preference stays Target/deployment intent, never a portable manifest field.

## Required checks

- Automatic/explicit, available/incompatible/ambiguous, no provider, Target switch; component/contract tests only.

## Dependencies and file ownership

- Depends on core-910 and core-912.

## Autonomous execution contract — 2026-10-16

- **Owned files:** `cmd/baha/app_provider_choice.go` and `cmd/baha/app_provider_choice_test.go` only.
- **Delivered interface/result:** Consume the accepted core-912 component API and existing Target/provider facts. Return Target-scoped preference selections without writing them. All APIs must be present on develop before assignment.
- **Task-specific proof:** `TestAppProviderChoice*`: automatic/explicit, compatibility/ambiguity, missing candidate and Target switch.
- **Boundary:** No changes to selection-component source, resolver/registry, persistence or portable manifest schema. If the predecessor API is insufficient, correct and integrate it before assigning this task.
- **Assignment gate:** use only accepted dependencies and APIs already present on develop. Confirm that the trusted plan/executor runs these exact test families on this task's file set and checks their outcomes. A plan that reports unresolved is not execution-ready. The CI-readiness inventory is maintained by [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md); later gaps become an explicit prerequisite before assignment, never an instruction to wait for another running session.
- **End-to-end owner:** the assigned session handles integration, implementation, focused tests, hosted CI observation, demonstrated fixes and its planning handoff. It reads other task states itself from planning main and preserves concurrent updates. No shared CI edits, dependency work-in-progress or manual message relay through Marcel. Normal independent review/Maintainer acceptance remains a boundary, not an implementation dependency.

## Handoff

- Not started.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
