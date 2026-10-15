---
id: core-911
areas: [wizard]
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: ""
depends_on: [core-910]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#911"]
source_updated: "2026-10-15T16:46:59Z"
labels: [area/dx]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-911 · App edit: load existing selections completely #task #release/v0-4-26 #status/planned #view/waiting #area/wizard #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Needs:** [core-910](core-910-wizard-shared-read-only-editing-state.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-910](core-910-wizard-shared-read-only-editing-state.md)  
**Required by:** [core-918](core-918-app-edit-apply-confirmed-changes.md), [core-920](core-920-machine-adapters-capability-changes-footprint.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#911](https://github.com/mcpdev80/baseharbor/issues/911)
<!-- /generated:links -->

## Goal

An existing app and its selected Target load losslessly into the shared editing state. Lane: data adapter.

## Scope

- In scope: new dedicated `app_edit_load`/guided hydration files and tests, using existing read-only owners.
- Out of scope: TUI renderers, registry, runtime mutations.

## Acceptance

- Hydrates capability selection AND explicit/automatic provider preferences; does not overwrite another Target's choice.
- Preserves rich manifests, instance names, unknown/extended fields and content not edited in the compact form; never asks for a manual UUID.
- Missing, ambiguous or incompatible sources return concrete typed results; reading mutates nothing.

## Required checks

- Fixture round trip and two Targets with different preferences; missing source and ambiguity; package tests only.

## Dependencies and file ownership

- Depends on core-910.

## Handoff

- Not started.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
