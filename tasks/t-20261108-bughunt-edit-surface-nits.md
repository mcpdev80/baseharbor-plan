---
id: t-20261108-bughunt-edit-surface-nits
card_number: "0427-151"
card_short_title: "app init Owner-Naht regression"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Jeder der vier punkte: dokumentierte entscheidung + passende regression ODER fix im bestehenden feld; meldungs-loop endet…"
kanban_title: 0427-151 · app init Owner-Naht regression
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp3.md"]
---
- [ ] t-20261108-bughunt-edit-surface-nits · Bug Hunt v0.4.27: Edit-Oberflaeche Klebe-Funde #task #release/v0-4-27 #status/planned #view/ready #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp3.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
Jeder der vier punkte: dokumentierte entscheidung + passende regression ODER fix im bestehenden feld; meldungs-loop endet spaetestens nach einem durchlauf.

## Problem (Fund H-P3, datei-/#beleg in der Akte)
Interaktive hilfe widerspricht sich (pipe funktioniert, hilfe/--no-input sagen terminal noetig, BF-04); app new --directory erzeugt fehlende eltern still (BF-07); status/doctor zeigen docker-block auf podman-only target (BF-08); init auf vorhandenem manifest laeuft in meldungs-loop (BF-14). Quelle Hunt H-P3.

## Acceptance
Jeder der vier punkte: dokumentierte entscheidung + passende regression ODER fix im bestehenden feld; meldungs-loop endet spaetestens nach einem durchlauf.

## Dependencies and file ownership
Keine. Write-set: cmd/baha edit-flaeche (hilfe-text, directory-pruefung, target-blockanzeige, init-manifest-pfad).
