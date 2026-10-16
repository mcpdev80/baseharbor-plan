---
id: core-918
areas: [wizard]
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: ""
depends_on: [core-911, core-916]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#918"]
source_updated: "2026-10-15T16:46:17Z"
labels: [area/dx, area/compatibility]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-918 · App edit: apply confirmed changes safely #task #release/v0-4-26 #status/planned #view/ready #area/wizard #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-911](core-911-app-edit-load-existing-selections.md), [core-916](core-916-wizard-back-cancel-eof-no-side-effects.md)  
**Required by:** [core-921](core-921-cli-mcp-register-new-interfaces.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#918](https://github.com/mcpdev80/baseharbor/issues/918)
<!-- /generated:links -->

## Goal

`baha app edit` shows the exact change and executes it through the accepted lifecycle. Lane: wiring Edit.

## Scope

- In scope: new `app_edit` command/apply files and tests.
- Out of scope: CLI root registration (core-921); parallel changes to domain/lifecycle owners; a custom transaction/recovery manager.

## Acceptance

- Loads capability and provider state; unchanged and non-edited manifest parts are preserved; No/Cancel stay write-free.
- Capability and Target preference changes run through the existing owners/consent/reconcile paths.
- Shared/foreign/data/recovery and explicit destructive confirmation rules hold; a stale plan is re-checked; actual partial results/dispositions are reported.

## Required checks

- Edit without change, two Targets, provider switch/removal, real consequences and consent mismatch via contract tests; then the necessary small Docker/Podman change scenarios.

## Dependencies and file ownership

- Depends on core-911 and core-916. Shared v0.4.26 PR/review/runner foundation (#890–#893, #895, #896) must be qualified first.

## Autonomous execution contract — 2026-10-16

- **Owned files:** `cmd/baha/app_edit.go`, `app_edit_test.go`, `app_edit_apply.go` and `app_edit_apply_test.go` only.
- **Delivered interface/result:** Consume accepted hydration and controller APIs; deliver a compiling Edit handler over existing consent/reconcile/apply authorities, with actual execution evidence.
- **Task-specific proof:** `TestAppEditApply*`/`TestAppEditCommand*`: no change, two Targets, provider transition/removal, stale consent, cancel, data/shared preservation and partial results; then the necessary existing Docker/Podman change gates.
- **Boundary:** No New files, component internals, domain mutation owners, recovery framework or central command/MCP registration. Required native gates must already be runnable without another CI owner.
- **Assignment gate:** use only accepted dependencies and APIs already present on develop. Confirm that the trusted plan/executor runs these exact test families on this task's file set and checks their outcomes. A plan that reports unresolved is not execution-ready. The CI-readiness inventory is maintained by [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md); later gaps become an explicit prerequisite before assignment, never an instruction to wait for another running session.
- **End-to-end owner:** the assigned session handles integration, implementation, focused tests, hosted CI observation, demonstrated fixes and its planning handoff. It reads other task states itself from planning main and preserves concurrent updates. No shared CI edits, dependency work-in-progress or manual message relay through Marcel. Normal independent review/Maintainer acceptance remains a boundary, not an implementation dependency.

## Handoff

- Not started.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
