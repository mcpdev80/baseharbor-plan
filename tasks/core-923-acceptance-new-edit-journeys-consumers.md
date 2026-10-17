---
id: core-923
areas: [acceptance]
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: ""
depends_on: [core-921, core-922, core-900]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#923"]
source_updated: "2026-10-15T16:45:40Z"
labels: [area/evidence]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-923 · Acceptance: verify New/Edit journeys and ecosystem consumers #task #release/v0-4-26 #status/planned #view/waiting #board/planned #area/acceptance #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Waiting for prerequisites**  
    **Needs:** [core-921](core-921-cli-mcp-register-new-interfaces.md), [core-922](core-922-docs-new-edit-provider-selection.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-921](core-921-cli-mcp-register-new-interfaces.md), [core-922](core-922-docs-new-edit-provider-selection.md), [core-900](core-900-gc-preserve-active-prs-candidates-evidence.md)  
**Required by:** [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#923](https://github.com/mcpdev80/baseharbor/issues/923)
<!-- /generated:links -->

## Goal

The integrated v0.4.26 product surface works for developers and existing consumers on the real candidate. Lane: targeted product acceptance.

## Scope

- In scope: existing Demo/consumer fixtures and release-specific gate/evidence inventories.
- Out of scope: product source changes, except a concrete found bug through its own fix PR. Preparation is not approval for a complete pre-release or promotion.

## Acceptance

- Native Docker and rootless Podman: fresh app without managed capabilities, create with real dependencies, edit/add/remove/provider switch, No/Cancel safety and data/shared preservation covered in a targeted way.
- Qualifies the actual current immutable BaseHarbor/Demo/Console/Connector revisions; CLI/JSON/MCP semantics through the real entry point; no old consumer PASS as a substitute.
- Uses existing gates and the core-888 plan/verifier; reuses green gates, also from failed overall runs, only with proven unchanged inputs.
- Isolates found bugs small; no full journey per fix. Final complete necessary coverage and an independent documented developer path.

## Required checks

- First the predecessors' component/contract evidence, then the necessary real consumer/runtime gates. Source/docs are not run serially before every diagnostic run. Coordinate with #897–#901 for candidate/evidence/pilot.

## Dependencies and file ownership

- Depends on core-921 and core-922; candidate/evidence/GC (#897–#900, already accepted) must be complete before.

## Autonomous execution contract — 2026-10-16

- **Owned files:** Existing release-specific consumer fixtures and evidence inventories in the affected product/consumer repositories; record exact paths and immutable candidate refs before executing.
- **Delivered interface/result:** Own candidate-pin resolution, gate execution, evidence validation and independent developer-path report as one acceptance task; no separate operator session is needed to run its checks.
- **Task-specific proof:** Predecessor component/contract evidence, then only required real New/Edit/runtime/consumer gates. Preserve original evidence and input equality rules; no automatic full release matrix.
- **Boundary:** Source bugs get their own explicit fix assignment. Do not start against missing consumer candidates or unsupported executors: detect those at assignment readiness, before long runs. Pre-release/promotion still requires separate authorization.
- **Assignment gate:** use only accepted dependencies and APIs already present on develop. Confirm that the trusted plan/executor runs these exact test families on this task's file set and checks their outcomes. A plan that reports unresolved is not execution-ready. The CI-readiness inventory is maintained by [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md); later gaps become an explicit prerequisite before assignment, never an instruction to wait for another running session.
- **End-to-end owner:** the assigned session handles integration, implementation, focused tests, hosted CI observation, demonstrated fixes and its planning handoff. It reads other task states itself from planning main and preserves concurrent updates. No shared CI edits, dependency work-in-progress or manual message relay through Marcel. Normal independent review/Maintainer acceptance remains a boundary, not an implementation dependency.

## Handoff

- Not started.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
