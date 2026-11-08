---
id: t-20261108-bughunt-orphan-process-lock-holder
card_number: "0427-147"
card_short_title: "app init Owner-Naht regression"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Lock-inhaber erkennbar: status/up zeigen pid+zustand des haltenden prozesses und nennen den naechsten schritt; optional…"
kanban_title: 0427-147 · app init Owner-Naht regression
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1458]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd4.md"]
---
- [ ] t-20261108-bughunt-orphan-process-lock-holder · Bug Hunt v0.4.27: Waisen-Prozess haelt Ziel #task #release/v0-4-27 #status/planned #view/ready #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **PR:** [baseharbor#1458](https://github.com/mcpdev80/baseharbor/pull/1458)  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd4.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** [baseharbor#1458](https://github.com/mcpdev80/baseharbor/pull/1458)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
Lock-inhaber erkennbar: status/up zeigen pid+zustand des haltenden prozesses und nennen den naechsten schritt; optional aufraeum-pfad mit ausdruecklicher freigabe; regression (fake-lock-inhaber) im lifecycle-feld.

## Problem (Fund aus Hunt H-D4, datei-/#beleg in der Akte)
SIGKILL: kernel-lock loest sich sauber, resume korrigiert DEGRADED (POSITIV belegt). ABER ein orphanieter baha up (ssh-close, prozess ueberlebt) haelt den lock — up/status melden blockiert bis externer pkill. Quelle Hunt H-D4 BF-hd4-2 (mittel).

## Acceptance
Lock-inhaber erkennbar: status/up zeigen pid+zustand des haltenden prozesses und nennen den naechsten schritt; optional aufraeum-pfad mit ausdruecklicher freigabe; regression (fake-lock-inhaber) im lifecycle-feld.

## Dependencies and file ownership
Keine. Write-set: lifecycle lock anzeige + target status.
