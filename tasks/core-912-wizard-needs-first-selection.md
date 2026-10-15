---
id: core-912
areas: [wizard]
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: ""
depends_on: [core-910]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#912"]
source_updated: "2026-10-15T16:46:52Z"
labels: [area/dx]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-912 · Wizard: present a compact needs-first selection #task #release/v0-4-26 #status/planned #view/waiting #area/wizard #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Waiting for prerequisites**  
    **Needs:** [core-910](core-910-wizard-shared-read-only-editing-state.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-910](core-910-wizard-shared-read-only-editing-state.md)  
**Required by:** [core-913](core-913-wizard-compatible-providers-same-view.md), [core-916](core-916-wizard-back-cancel-eof-no-side-effects.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#912](https://github.com/mcpdev80/baseharbor/issues/912)
<!-- /generated:links -->

## Goal

A compact keyboard checklist asks for developer needs instead of product names. Lane: TUI.

## Scope

- In scope: new dedicated `app_capability_selection` view/update files and tests.
- Out of scope: existing New/Init wizard entry points (changed only in the wiring task core-917).

## Acceptance

- One screen with Space/arrow keys; SQL, cache, protected secrets, app login and TLS/HTTPS as examples; further supported capabilities disclosed progressively.
- Zero selection is valid; detected suggestions are visible and deselectable; no implicit SQL/Identity/OpenBao/management bundle requirement.
- App login, operator/team access and service credentials are separated in wording and semantics; existing capability catalogs are used.

## Required checks

- Deterministic TUI update/view tests for selection, zero, preselection, keyboard and extended needs; no runtime.

## Dependencies and file ownership

- Depends on core-910.

## Handoff

- Not started.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
