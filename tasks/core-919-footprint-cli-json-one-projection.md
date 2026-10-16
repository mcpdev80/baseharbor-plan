---
id: core-919
areas: [cli]
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: ""
depends_on: [core-910, core-914]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#919"]
source_updated: "2026-10-15T16:46:11Z"
labels: [area/dx, area/compatibility]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-919 · Footprint: serve CLI and JSON from one projection #task #release/v0-4-26 #status/planned #view/waiting #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Waiting for prerequisites**  
    **Needs:** [core-914](core-914-preview-actual-footprint.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-910](core-910-wizard-shared-read-only-editing-state.md), [core-914](core-914-preview-actual-footprint.md)  
**Required by:** [core-920](core-920-machine-adapters-capability-changes-footprint.md), [core-921](core-921-cli-mcp-register-new-interfaces.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#919](https://github.com/mcpdev80/baseharbor/issues/919)
<!-- /generated:links -->

## Goal

`baha app footprint show` delivers the existing authoritative projection for humans and as JSON. Lane: CLI/JSON read-only.

## Scope

- In scope: dedicated footprint command/output files and tests.
- Out of scope: central command/MCP registry, footprint schema, registry golden changes.

## Acceptance

- Uses the existing footprint version/resolver and current Target/consumer/provider facts; no second footprint or state calculator.
- Reports real completeness, measured/estimated/unknown and denied/unverifiable/source_missing truthfully.
- Read-only even with missing/partial installations; safe errors/exit codes; no credential or internal path leaks.

## Required checks

- Golden/contract tests for the same facts in human/JSON output, empty/partial/wrong Target; no containers.

## Dependencies and file ownership

- Depends on core-910 and core-914. Shared v0.4.26 PR/review/runner foundation (#890–#893, #895, #896) must be qualified first.

## Autonomous execution contract — 2026-10-16

- **Owned files:** `cmd/baha/app_footprint_show.go` and `cmd/baha/app_footprint_show_test.go` only; dedicated testdata beneath `cmd/baha/testdata/app_footprint_show/` if needed.
- **Delivered interface/result:** Deliver callable human/JSON handlers consuming accepted footprint presentation and the existing authoritative footprint schema; the controller does not become a new calculation owner.
- **Task-specific proof:** `TestAppFootprintShow*`: same authoritative facts in human/JSON, empty/incomplete/wrong Target, denial and secret-free error/exit behavior.
- **Boundary:** No footprint-domain/schema changes, presenter edits, machine registry/goldens or command routing. Registration is delivered by core-921.
- **Assignment gate:** use only accepted dependencies and APIs already present on develop. Confirm that the trusted plan/executor runs these exact test families on this task's file set and checks their outcomes. A plan that reports unresolved is not execution-ready. The CI-readiness inventory is maintained by [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md); later gaps become an explicit prerequisite before assignment, never an instruction to wait for another running session.
- **End-to-end owner:** the assigned session handles integration, implementation, focused tests, hosted CI observation, demonstrated fixes and its planning handoff. It reads other task states itself from planning main and preserves concurrent updates. No shared CI edits, dependency work-in-progress or manual message relay through Marcel. Normal independent review/Maintainer acceptance remains a boundary, not an implementation dependency.

## Handoff

- Not started.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
