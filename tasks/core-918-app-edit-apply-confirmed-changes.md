---
id: core-918
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

- [ ] core-918 · App edit: apply confirmed changes safely #task #release/v0-4-26 #status/planned

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-911](core-911-app-edit-load-existing-selections.md), [core-916](core-916-wizard-back-cancel-eof-no-side-effects.md)  
**Required by:** [core-921](core-921-cli-mcp-register-new-interfaces.md)  
**Owner:** unassigned  
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

## Handoff

- Not started.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
