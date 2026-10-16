---
id: core-911
areas: [wizard]
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: "mcpdev80 (core-911)"
depends_on: [core-910, t-20261016-wizard-task-ci-readiness]
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#967"]
sources: ["mcpdev80/baseharbor#911"]
source_updated: "2026-10-15T16:46:59Z"
labels: [area/dx]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-911 · App edit: load existing selections completely #task #release/v0-4-26 #status/review #view/review #area/wizard #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (core-911) · **Priority:** not set  
    **PR:** [baseharbor#967](https://github.com/mcpdev80/baseharbor/pull/967)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-910](core-910-wizard-shared-read-only-editing-state.md), [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md)  
**Required by:** [core-918](core-918-app-edit-apply-confirmed-changes.md), [core-920](core-920-machine-adapters-capability-changes-footprint.md)  
**Owner:** mcpdev80 (core-911)  
**Priority:** not set  
**PRs:** [baseharbor#967](https://github.com/mcpdev80/baseharbor/pull/967)  
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

- 2026-10-16 core-911 independent-review handoff: Product [PR #967](https://github.com/mcpdev80/baseharbor/pull/967) on `task/core-911-edit-hydration`, exact product HEAD `b1d976d210e4d0954dbb9ab007adb21b99c0e0ac`, trusted `develop` SHA `a1e58f1f3600bf95d0318662bbec447c6e8ed74a` (unchanged since branch creation; no develop merge necessary). Scope is exactly `cmd/baha/app_edit_load.go` and `cmd/baha/app_edit_load_test.go`. Read-only `appEditLoad` adapter uses `GuidedReadContext` authority per Target, preserves exact original supplied source bytes including named instances, extension fields and all noncompact intent, and copies capability selections plus explicit/automatic Target-local provider preferences. Typed safe errors for missing, ambiguous, incompatible, unverifiable and wrong Target; no manual ID, command registration, mutation, or persistence. `TestAppEditLoad*` tests cover rich source byte-for-byte roundtrip, target preference separation, error taxonomy and source/authority nonmutation. Existing targeted [GitHub Actions run 38899265776](https://github.com/mcpdev80/baseharbor/actions/runs/38899265776), attempt 1, **SUCCESS**: Trusted Plan, Workflow policy, Focused Python, source/contracts, `wizard-app-edit-load-tests`, cli-gofmt, cli-vet, cli-build and final `PR Selected Checks`. Unneeded runtime, release, public-contract, candidate and legacy broad validate jobs skipped. Earlier gofmt failures are historical red evidence, not accepted. No containers or runtime matrix. **Await independent review; do not merge or self-accept.**

- Not started.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
