---
id: core-911
areas: [wizard]
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: ""
depends_on: [core-910, t-20261016-wizard-task-ci-readiness]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#911"]
source_updated: "2026-10-15T16:46:59Z"
labels: [area/dx]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-911 · App edit: load existing selections completely #task #release/v0-4-26 #status/planned #view/waiting #area/wizard #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Waiting for prerequisites**  
    **Needs:** [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-910](core-910-wizard-shared-read-only-editing-state.md), [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md)  
**Required by:** [core-918](core-918-app-edit-apply-confirmed-changes.md), [core-920](core-920-machine-adapters-capability-changes-footprint.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#911](https://github.com/mcpdev80/baseharbor/issues/911)
<!-- /generated:links -->

## Goal

An existing app and its selected Target load losslessly into the shared editing state. Lane: data adapter.

## Scope

- In scope: new dedicated `app_edit_load`/guided hydration files and tests, using existing read-only owners.
- Out of scope: TUI renderers, registry, runtime mutations.

## Acceptance

- Hydrates capability selection AND explicit/automatic provider preferences; does not overwrite another Target's choice.
- Preserves rich manifests, instance names, unknown/extended fields and content not edited in the compact form; never asks for a manual UUID.
- Missing, ambiguous or incompatible sources return concrete typed results; reading mutates nothing.

## Required checks

- Fixture round trip and two Targets with different preferences; missing source and ambiguity; package tests only.

## Dependencies and file ownership

- Depends on core-910.

## Autonomous execution contract — 2026-10-16

- **Owned files:** `cmd/baha/app_edit_load.go` and `cmd/baha/app_edit_load_test.go` only.
- **Delivered interface/result:** Expose a compiling hydration adapter using the merged `GuidedReadContext` and existing authorities. Its result carries the untouched source representation plus editable selections; own any new hydration-specific types in this file.
- **Task-specific proof:** `TestAppEditLoad*`: rich intent, automatic/explicit preferences, two Targets, incomplete/ambiguous sources and no-write snapshots.
- **Boundary:** No edits to `guided_application_read_context*`, checklist/provider/presenter/controller files, lifecycle owners, shared fixtures or registration. Reading/hydration does not apply changes.
- **Assignment gate:** use only accepted dependencies and APIs already present on develop. Confirm that the trusted plan/executor runs these exact test families on this task's file set and checks their outcomes. A plan that reports unresolved is not execution-ready. The CI-readiness inventory is maintained by [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md); later gaps become an explicit prerequisite before assignment, never an instruction to wait for another running session.
- **End-to-end owner:** the assigned session handles integration, implementation, focused tests, hosted CI observation, demonstrated fixes and its planning handoff. It reads other task states itself from planning main and preserves concurrent updates. No shared CI edits, dependency work-in-progress or manual message relay through Marcel. Normal independent review/Maintainer acceptance remains a boundary, not an implementation dependency.

## Handoff

- Not started.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
