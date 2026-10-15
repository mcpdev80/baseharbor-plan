---
id: core-915
areas: [wizard]
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: ""
depends_on: [core-910]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#915"]
source_updated: "2026-10-15T16:46:34Z"
labels: [area/dx]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-915 · Preview: explain provider consequences and partial results #task #release/v0-4-26 #status/planned #view/waiting #area/wizard #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Waiting for prerequisites**  
    **Needs:** [core-910](core-910-wizard-shared-read-only-editing-state.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-910](core-910-wizard-shared-read-only-editing-state.md)  
**Required by:** [core-916](core-916-wizard-back-cancel-eof-no-side-effects.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#915](https://github.com/mcpdev80/baseharbor/issues/915)
<!-- /generated:links -->

## Goal

Before confirmation and after execution, the actual consequences for every supported provider are understandable. Lane: read-only presentation.

## Scope

- In scope: separate `app_change_preview`/`result_presenter` files and tests, consuming existing ProviderChange plan/result types.
- Out of scope: UI-local impact engines or special blockers.

## Acceptance

- Distinguishes add, stop, remove, replace and capability deselection; affected apps/functions/data locations, PKI/token renewal and required actions come from the real plan.
- Intended destructive decisions are possible through the existing explicit/double confirmation; no UI-specific blocker and no ownership/security bypass.
- After success or partial failure, shows actual dispositions/remaining state and the next step; no generic warning lists or invented substitute locations.

## Required checks

- Typed fixtures across all relevant existing consequence classes, safe continuation, destructive alternative, partial execution and secret redaction; no runtime.

## Dependencies and file ownership

- Depends on core-910. Shared v0.4.26 PR/review/runner foundation (#890–#893, #895, #896) must be qualified first.

## Handoff

- Not started.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
