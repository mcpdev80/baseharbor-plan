---
id: t-20261126-hunt46-recovery-backup-volume-heuristic
card_number: "0428-329"
card_short_title: "tighten recovery/backup volume label match"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: Under the whole-installation full-destroy command — the most destructive command in the tool — the only thing standing between…
kanban_title: 0428-329 · tighten recovery/backup volume label match
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

Under the whole-installation `full-destroy` command — the most destructive command in the tool — the only thing standing between deleting shared/application-owned volumes and deleting recovery/backup data is a provenance heuristic. This card tightens the recovery/backup preservation heuristic in the repository volume inventory to an authoritative match so full-destroy cannot delete recovery/backup data via a mislabeled volume.

## Scope

- In scope:
  - `internal/runtime/repository_volume_inventory.go` recovery/backup detection (lines 73-77): replace the case-insensitive substring search (`strings.Contains(strings.ToLower(key), "recovery")` / `... "backup"` / value substring) with an authoritative, label-keyed match (exact label-key set for the recovery/backup preservation keys), so only volumes carrying a recognized recovery/backup label key are preserved.
  - Positive regression: a volume with a recovery/backup label key is preserved under full-destroy.
  - Negative regression: a volume whose recovery/backup substring appears only in an unrelated label value/key is NOT preserved (would previously have been misclassified as exclusively owned and deleted).
- Out of scope:
  - The `destroy --all` reuse / never-delivered proof leak (0428-326) — different seam.
  - The `control-plane destroy --delete-data` vs `full-destroy` vocabulary gap (0428-330) — related but distinct.

## Acceptance

- Recovery/backup preservation is keyed on authoritative label keys, not a case-insensitive substring of any key or value.
- A mislabeled volume that only embeds "recovery"/"backup" in an unrelated label is no longer misclassified as exclusively owned for full-destroy.
- Positive and negative regression on the inventory heuristic via the existing repository volume inventory test path.
- Every required test is reachable by a real CI check in the same PR; test registered and mapped in the same PR (Gate Rule). Docker/Podman: prove native Docker and rootless Podman/Quadlet separately only if the volume inventory path has a native gate; unit evidence is insufficient for a live runtime gate.
- Exact source SHA -> test ID -> mapped CI gate -> trigger -> actual run recorded in handoff.

## Dependencies and file ownership

- Owned files or areas: `internal/runtime/repository_volume_inventory.go`.
- Shared files: n/a.

## Handoff

- Current state, branch, PR and evidence links. Newest first.

## Task

Cast from hunt H-V46 (akte evidence/r28-welle6-2026-11-27/bughunt-hv46-state-lifecycle/ on origin/main 62de9bb74, anchor develop 2a141387d; re-verified against develop 384d857b5 at intake). BF-46-6 LIVE. `InventoryRepositoryVolumes` returns `RepositoryVolume{Shared bool}`; a volume is `Shared=true` (preserved) when mounted-shared, foreign/conflicting, unlabeled, or carries a recovery/backup label. The recovery/backup preservation (repository_volume_inventory.go:73-77) is a heuristic: `strings.Contains(strings.ToLower(key), "recovery")` plus a value substring check — a case-insensitive substring search, not an authoritative ownership record. A volume whose recovery data is labeled with a non-"recovery"/"backup" substring is classified as exclusively owned and deleted under full-destroy. Fix: tighten to an authoritative label-key match so full-destroy cannot delete recovery/backup data via a mislabeled volume.
