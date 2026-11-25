---
id: t-20261126-hunt46-recovery-backup-volume-heuristic
card_number: "0428-329"
card_short_title: "delete owned app volumes"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "baha app destroy deletes all resources and volumes proven to belong to the selected application, including volumes with recovery…"
kanban_title: 0428-329 · delete owned app volumes
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/runtime/repository_volume_inventory.go#L50-L80","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/cmd/baha/app_destroy_lifecycle.go#L264-L278","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/cmd/baha/app_destroy_volumes.go#L11-L40","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/cmd/baha/app_volume_observation.go#L70-L91"]
---

- [ ] t-20261126-hunt46-recovery-backup-volume-heuristic · 0428 hunt H-V46: recovery/backup volume preservation uses a case-insensitive substring search (medium) #task #release/v0-4-28 #status/planned #view/ready #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/runtime/repository_volume_inventory.go#L50-L80), [proof 2](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/cmd/baha/app_destroy_lifecycle.go#L264-L278), [proof 3](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/cmd/baha/app_destroy_volumes.go#L11-L40), [proof 4](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/cmd/baha/app_volume_observation.go#L70-L91)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

`baha app destroy` deletes all resources and volumes proven to belong to the selected application, including volumes with recovery or backup labels. This is full application destruction; retaining app-owned volumes would be app deletion rather than destroy. Foreign, shared, or ownership-uncertain volumes remain outside the deletion scope.

## Acceptance

- `baha app destroy` deletes every volume proven to belong to the selected application, including recovery/backup-labelled volumes; no label-based preservation exception applies within that app scope.
- Ownership is determined by authoritative ownership/scope metadata, not substring heuristics. A foreign or shared volume must not enter the deletion scope because a label contains “backup” or “recovery”.
- Add focused regressions proving an app-owned recovery/backup-labelled volume is deleted and foreign/shared or ownership-uncertain volumes remain untouched.
- Bind the tests to existing checks and native runtime gates where the inventory path requires them; do not add a parallel CI framework.
- Record exact candidate SHA, tests, selected gates, triggers, and actual results.

## Handoff

- Current state, branch, PR and evidence links. Newest first.

## Owner decision — 2026-11-25

For `baha app destroy`, all resources inside the selected application's destruction scope are deleted, including persistent, recovery-labelled, and backup-labelled volumes. Retaining those volumes would be app deletion, not destroy. Resources outside the selected scope remain untouched. A recovery/backup label is not an ownership boundary and must not override the selected destroy scope.

## Current-source recheck — 2026-11-25

At `mcpdev80/baseharbor/develop`, commit `3a2ae6b1139570c98b8924e3b19975c56a289400`, `internal/runtime/repository_volume_inventory.go` marks a volume shared/preserved when any label key contains `recovery` or `backup`, or any label value contains `recovery`. `app_destroy_volumes.go` then excludes every volume marked shared from deletion. This conflicts with the owner decision for volumes otherwise proven inside the selected application's destroy scope. Remove that label-based preservation exception and verify scope-based deletion; do not broaden destruction to foreign or out-of-scope volumes.

## Task

- Treat the selected application's authoritative destruction scope as the deletion boundary for `baha app destroy`.
- Delete every volume in that scope, regardless of recovery/backup labels.
- Leave foreign and out-of-scope volumes untouched; labels alone must neither add a volume to the scope nor remove an in-scope volume from it.
- Add focused regressions for an in-scope recovery/backup-labelled volume being deleted and a foreign/out-of-scope volume being retained.
- Use existing mapped unit and native runtime gates; add no parallel CI framework.
- Record exact candidate SHA, tests, selected gates, triggers, and actual results.
