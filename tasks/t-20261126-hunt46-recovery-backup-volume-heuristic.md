---
id: t-20261126-hunt46-recovery-backup-volume-heuristic
card_number: "0428-329"
card_short_title: "tighten recovery/backup match"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "destroy --all removes every volume in the selected installation's destruction scope, including volumes labeled for recovery or…"
kanban_title: 0428-329 · tighten recovery/backup match
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261126-hunt46-recovery-backup-volume-heuristic · 0428 hunt H-V46: recovery/backup volume preservation uses a case-insensitive substring search (medium) #task #release/v0-4-28 #status/planned #view/ready #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
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

`destroy --all` removes every volume in the selected installation's destruction scope, including volumes labeled for recovery or backup. This is full destruction; retaining installation data would be app deletion rather than destroy. Ownership detection must still keep volumes outside the selected installation scope untouched.

## Acceptance

- Full destroy deletes every installation-owned volume, including recovery/backup volumes; no label-based preservation exception applies within the destruction scope.
- Ownership is determined by authoritative ownership/scope metadata, not substring heuristics. A foreign volume must not become part of the destroy scope because an unrelated label contains “backup” or “recovery”.
- Add focused regressions proving an owned recovery/backup volume is deleted and a foreign volume remains untouched.
- Bind the tests to existing checks and native runtime gates where the inventory path requires them; do not add a parallel CI framework.
- Record exact candidate SHA, tests, selected gates, triggers, and actual results.

## Handoff

- Current state, branch, PR and evidence links. Newest first.

## Owner decision — 2026-11-25

For `baha app destroy`, all resources inside the selected application's destruction scope are deleted, including persistent, recovery-labelled, and backup-labelled volumes. Retaining those volumes would be app deletion, not destroy. Resources outside the selected scope remain untouched. A recovery/backup label is not an ownership boundary and must not override the selected destroy scope.

## Current-source recheck — 2026-11-25

At `mcpdev80/baseharbor/develop`, commit `7bdeae95ccf0ce0d2fe39ae6d4c884402268995d`, `internal/runtime/repository_volume_inventory.go` marks a volume shared/preserved when any label key contains `recovery` or `backup`, or any label value contains `recovery`. This conflicts with the owner decision for volumes otherwise inside the selected application's destroy scope. Keep this card open to remove that label-based preservation exception and verify scope-based deletion. Do not broaden destruction to foreign or out-of-scope volumes.

## Task

- Treat the selected application's authoritative destruction scope as the deletion boundary.
- Delete every volume in that scope, regardless of recovery/backup labels.
- Leave foreign and out-of-scope volumes untouched; labels alone must neither add a volume to the scope nor remove an in-scope volume from it.
- Add focused regressions for an in-scope recovery/backup-labelled volume being deleted and a foreign/out-of-scope volume being retained.
- Use existing mapped unit and native runtime gates; add no parallel CI framework.
- Record exact candidate SHA, tests, selected gates, triggers, and actual results.
