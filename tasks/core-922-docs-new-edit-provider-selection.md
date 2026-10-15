---
id: core-922
areas: [docs]
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: ""
depends_on: [core-921, core-900]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#922"]
source_updated: "2026-10-15T16:45:47Z"
labels: [area/dx]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-922 · Docs: explain New/Edit and provider selection concisely #task #release/v0-4-26 #status/planned #view/waiting #area/docs #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Waiting for prerequisites**  
    **Needs:** [core-921](core-921-cli-mcp-register-new-interfaces.md), [core-900](core-900-gc-preserve-active-prs-candidates-evidence.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-921](core-921-cli-mcp-register-new-interfaces.md), [core-900](core-900-gc-preserve-active-prs-candidates-evidence.md)  
**Required by:** [core-923](core-923-acceptance-new-edit-journeys-consumers.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#922](https://github.com/mcpdev80/baseharbor/issues/922)
<!-- /generated:links -->

## Goal

Developers find a short, accurate New/Edit guide that needs no prior infrastructure product knowledge. Lane: EN/DE guide.

## Scope

- In scope: EN/DE public guides, navigation, examples, changelog and v0.4.26 release notes.
- Out of scope: generated CLI/MCP references (core-921); process docs (#890, closed).

## Acceptance

- Explains needs-first selection, optional provider, preview, No/Cancel, zero capabilities, footprint and effects with real supported examples.
- Only essential delivered developer changes; Console/Connector consumption described by its actual reach; no anticipation of v0.4.28/platform features.
- EN/DE identical; Pages candidate build/navigation checked; no process rules added to the README and no public Pages deployment before promotion.

## Required checks

- Existing targeted docs/link/EN-DE/candidate build checks; no runtime matrix for text alone.

## Dependencies and file ownership

- Depends on core-921. Final candidate/evidence qualification additionally needs #897–#900 (only core-900 still open); coordinate with pilot core-901.

## Handoff

- Not started.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
