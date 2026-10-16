---
id: core-920
areas: [cli]
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: "mcpdev80 (core-920)"
depends_on: [core-910, core-911, core-919]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#920"]
source_updated: "2026-10-15T16:46:05Z"
labels: [area/dx, area/compatibility]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-920 · Machine adapters: reuse capability changes and footprint #task #release/v0-4-26 #status/active #view/active #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (core-920) · **Priority:** not set  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-910](core-910-wizard-shared-read-only-editing-state.md), [core-911](core-911-app-edit-load-existing-selections.md), [core-919](core-919-footprint-cli-json-one-projection.md)  
**Required by:** [core-921](core-921-cli-mcp-register-new-interfaces.md)  
**Owner:** mcpdev80 (core-920)  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#920](https://github.com/mcpdev80/baseharbor/issues/920)
<!-- /generated:links -->

## Goal

Agents can use the same useful needs/provider operations without the TUI or a CLI subprocess. Lane: JSON/MCP.

## Scope

- In scope: dedicated machine/MCP adapters and tests over existing domain operations.
- Out of scope: registration, discovery/coverage goldens and generated references (core-921 only).

## Acceptance

- Reuses existing domain/provider-change/footprint APIs; classifies useful operations instead of mirroring every UI step as a tool.
- Explicit provider preference can be discovered and expressed; Target binding, authorization, valid plan/consent and required double destructive confirmation are represented equivalently.
- Typed denied/unsupported/conflict/cancel/partial results, secret-free; no false machine capability advertised, no TTY requirement or shell escape.

## Required checks

- In-process adapter/parity/negative contract tests with the same domain fixtures, including footprint, consent/revision change and partial failure. No real provider needed for the transport contract.

## Dependencies and file ownership

- Depends on core-910, core-911 and core-919. Shared v0.4.26 PR/review/runner foundation (#890–#893, #895, #896) must be qualified first.

## Autonomous execution contract — 2026-10-16

- **Owned files:** `cmd/baha/app_machine_adapters.go` and `cmd/baha/app_machine_adapters_test.go` only; dedicated adapter fixture files if needed, listed before editing.
- **Delivered interface/result:** Deliver compiling callable JSON/MCP adapters over existing authoritative operations and accepted read/hydration/footprint APIs; describe registration inputs for core-921.
- **Task-specific proof:** `TestAppMachineAdapters*`: in-process capability/provider/footprint parity, typed denial/conflict/cancel/partial results, stale plan/consent and destructive confirmation; no TTY, shell or runtime dependency.
- **Boundary:** No registry/discovery/machine-coverage golden edits and no dependency on unfinished New/Edit CLI wiring. Runtime mutations remain inside existing authorized domain operations.
- **Assignment gate:** use only accepted dependencies and APIs already present on develop. Confirm that the trusted plan/executor runs these exact test families on this task's file set and checks their outcomes. A plan that reports unresolved is not execution-ready. The CI-readiness inventory is maintained by [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md); later gaps become an explicit prerequisite before assignment, never an instruction to wait for another running session.
- **End-to-end owner:** the assigned session handles integration, implementation, focused tests, hosted CI observation, demonstrated fixes and its planning handoff. It reads other task states itself from planning main and preserves concurrent updates. No shared CI edits, dependency work-in-progress or manual message relay through Marcel. Normal independent review/Maintainer acceptance remains a boundary, not an implementation dependency.

## Handoff

- Not started.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
