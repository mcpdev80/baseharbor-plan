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
kanban_summary: Under the whole-installation full-destroy command — the most destructive command in the tool — the only thing standing between…
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

## Task

Cast from hunt H-V46 (akte evidence/r28-welle6-2026-11-27/bughunt-hv46-state-lifecycle/ on origin/main 62de9bb74, anchor develop 2a141387d; re-verified against develop 384d857b5 at intake). BF-46-6 LIVE. `InventoryRepositoryVolumes` returns `RepositoryVolume{Shared bool}`; a volume is `Shared=true` (preserved) when mounted-shared, foreign/conflicting, unlabeled, or carries a recovery/backup label. The recovery/backup preservation (repository_volume_inventory.go:73-77) is a heuristic: `strings.Contains(strings.ToLower(key), "recovery")` plus a value substring check — a case-insensitive substring search, not an authoritative ownership record. A volume whose recovery data is labeled with a non-"recovery"/"backup" substring is classified as exclusively owned and deleted under full-destroy. Fix: tighten to an authoritative label-key match so full-destroy cannot delete recovery/backup data via a mislabeled volume.
