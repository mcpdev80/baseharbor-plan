---
id: core-913
areas: [wizard]
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: ""
depends_on: [core-910, core-912]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#913"]
source_updated: "2026-10-15T16:46:46Z"
labels: [area/dx]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-913 · Wizard: offer compatible providers in the same view #task #release/v0-4-26 #status/planned #view/waiting #area/wizard #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Waiting for prerequisites**  
    **Needs:** [core-912](core-912-wizard-needs-first-selection.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-910](core-910-wizard-shared-read-only-editing-state.md), [core-912](core-912-wizard-needs-first-selection.md)  
**Required by:** [core-916](core-916-wizard-back-cancel-eof-no-side-effects.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#913](https://github.com/mcpdev80/baseharbor/issues/913)
<!-- /generated:links -->

## Goal

For a need, a compatible provider preference can be set in place; Automatic stays the default. Lane: provider view.

## Scope

- In scope: separate `app_provider_choice` files and tests, using only the agreed selection-component interface.
- Out of scope: checklist core files, central registry, resolver; persistence (not in this task).

## Acceptance

- Shows the current compatible providers/instances from the Target/registry/resolver result instead of a fixed product catalog.
- No additional mandatory screen; shows the proposed actual provider and reason; errors are concrete with no silent substitute.
- The preference stays Target/deployment intent, never a portable manifest field.

## Required checks

- Automatic/explicit, available/incompatible/ambiguous, no provider, Target switch; component/contract tests only.

## Dependencies and file ownership

- Depends on core-910 and core-912.

## Handoff

- Not started.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
