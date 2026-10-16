---
id: core-754
areas: [mcp]
type: bug
release: v0.4.x
version: ""
parent: v0.4.x
owner: mcpdev80
depends_on: [core-893, core-895, core-896]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#754"]
source_updated: "2026-10-15T16:51:15Z"
labels: [kind/bug, area/mcp, area/dx, area/compatibility]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-754 · MCP: classify expected preconditions correctly #task #release/v0-4-x #status/planned #view/ready #area/mcp #kind/bug
    <!-- generated:card -->
    **Owner:** mcpdev80 · **Priority:** not set  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.x](../releases/v0.4.x.md)  
**Depends on:** [core-893](core-893-ci-enforce-selected-pr-checks.md), [core-895](core-895-reviews-require-maintainer-approval.md), [core-896](core-896-runners-isolate-parallel-pr-checks.md)  
**Owner:** mcpdev80  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#754](https://github.com/mcpdev80/baseharbor/issues/754)
<!-- /generated:links -->

## Goal

Expected machine/MCP preconditions get stable typed codes instead of being flattened to `internal_error`.

## Scope

- Bug: `machine.Classify` only preserves already-typed `*machine.Error` values, so expected preconditions become `internal_error`: organization configuration not configured; unsupported organization source kind; application without registered deployment; repository manifest not found for workspace operations. CLI output stays actionable but automation cannot distinguish expected state from internal failure.
- Required mapping: missing registered application/deployment → `not_found`; repository manifest/workspace source absent → `source_missing`; organization configuration absent → `validation_failed`; unsupported organization source kind → `unsupported_operation`; real internal/unclassified failures stay `internal_error`.
- Triage (2026-10-15): some classification is now implemented in `cmd/baha/main.go` at `1b1ae323` (workspace/manifest absence, organization configuration errors). Source inspection alone does not prove every case: verify the listed outcomes, cancellation and unexpected-error behavior with bounded CLI/MCP checks and record the actual remaining failures.

## Acceptance

- `baseharbor.organization.inspect` without org config is not `internal_error`.
- Unsupported organization source kind is not `internal_error`.
- `baseharbor.status` / `policy.explain` for an unknown app return `not_found`.
- `baseharbor.workspace.status` outside an app repository returns `source_missing`.
- CLI and MCP use the same underlying typed error semantics.
- Context timeout/cancellation behavior remains unchanged.
- Unknown unexpected errors still classify as `internal_error`.
- The source's "lands directly in active v0.4.21" item is historical.

## Required checks

- Focused machine/MCP tests and `go vet`.

## Dependencies and file ownership

- Product implementation requires the qualified v0.4.26 PR/review/runner foundation (core-893, core-895, core-896; binding 2026-10-15 correction in [core-888](../epics/core-888-development-and-ci.md)).
- No open task dependencies. Related: core-750, core-751, core-752.

## Handoff

- Assigned to mcpdev80; no recent claim. Partial implementation exists (see scope).
