---
id: core-919
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

- [ ] core-919 · Footprint: serve CLI and JSON from one projection #task #release/v0-4-26 #status/planned

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-910](core-910-wizard-shared-read-only-editing-state.md), [core-914](core-914-preview-actual-footprint.md)  
**Required by:** [core-920](core-920-machine-adapters-capability-changes-footprint.md), [core-921](core-921-cli-mcp-register-new-interfaces.md)  
**Owner:** unassigned  
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

## Handoff

- Not started.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
