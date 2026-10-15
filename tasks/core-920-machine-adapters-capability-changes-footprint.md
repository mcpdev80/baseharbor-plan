---
id: core-920
areas: [cli]
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: ""
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

- [ ] core-920 · Machine adapters: reuse capability changes and footprint #task #release/v0-4-26 #status/planned #view/waiting #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Needs:** [core-910](core-910-wizard-shared-read-only-editing-state.md), [core-911](core-911-app-edit-load-existing-selections.md), [core-919](core-919-footprint-cli-json-one-projection.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-910](core-910-wizard-shared-read-only-editing-state.md), [core-911](core-911-app-edit-load-existing-selections.md), [core-919](core-919-footprint-cli-json-one-projection.md)  
**Required by:** [core-921](core-921-cli-mcp-register-new-interfaces.md)  
**Owner:** unassigned  
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

## Handoff

- Not started.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
