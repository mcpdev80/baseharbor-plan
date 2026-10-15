---
id: core-921
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: ""
depends_on: [core-917, core-918, core-919, core-920]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#921"]
source_updated: "2026-10-15T16:45:53Z"
labels: [area/dx, area/compatibility]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-921 · CLI and MCP: register new interfaces consistently #task #release/v0-4-26 #status/planned #view/waiting
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Needs:** [core-917](core-917-app-new-connect-wizard-lifecycle.md), [core-918](core-918-app-edit-apply-confirmed-changes.md), [core-919](core-919-footprint-cli-json-one-projection.md), [core-920](core-920-machine-adapters-capability-changes-footprint.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-917](core-917-app-new-connect-wizard-lifecycle.md), [core-918](core-918-app-edit-apply-confirmed-changes.md), [core-919](core-919-footprint-cli-json-one-projection.md), [core-920](core-920-machine-adapters-capability-changes-footprint.md)  
**Required by:** [core-922](core-922-docs-new-edit-provider-selection.md), [core-923](core-923-acceptance-new-edit-journeys-consumers.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#921](https://github.com/mcpdev80/baseharbor/issues/921)
<!-- /generated:links -->

## Goal

The finished separate handlers are reachable consistently through the real CLI/JSON/MCP entry points. Lane: single shared integration.

## Scope

- In scope: **sole owner** of the `cmd/baha` command tree/registration, `human_new` routing, `machine_coverage`, the MCP tool registry, help/discovery/coverage goldens and generated CLI/MCP references.
- Out of scope: reinventing legacy aliases.

## Acceptance

- `app new`, `app edit` and `app footprint show` are discovered and routed correctly; existing verbs/approval/machine classification stay consistent.
- Discovery/help show only actually available operations; generated references come from real registrations.
- Shared files change in this one small integration PR; predecessor tasks deliver compiling constructors/adapters, no parallel registry patches.

## Required checks

- Command tree/help/discovery/generated drift checks and a generic in-process MCP client; small CLI smokes, no full journey.

## Dependencies and file ownership

- Depends on core-917, core-918, core-919 and core-920. Shared v0.4.26 PR/review/runner foundation (#890–#893, #895, #896) must be qualified first.

## Handoff

- Not started.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
