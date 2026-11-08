---
id: t-20261108-bughunt-needs-tui-display-nav
card_number: "0427-143"
card_short_title: "app init Owner-Naht regression"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: Rueckwaertsnavigation sichtbar; umbruchfeste zeilen; fehler bei choicesForSelection显示 statt verschlucken; geschmack konsistent…
kanban_title: 0427-143 · app init Owner-Naht regression
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1458]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp1.md"]
---
- [ ] t-20261108-bughunt-needs-tui-display-nav · Bug Hunt v0.4.27: Needs-TUI Anzeige und Rueckweg #task #release/v0-4-27 #status/planned #view/ready #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **PR:** [baseharbor#1458](https://github.com/mcpdev80/baseharbor/pull/1458)  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp1.md)  
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
Rueckwaertsnavigation sichtbar; umbruchfeste zeilen; fehler bei choicesForSelection显示 statt verschlucken; geschmack konsistent (p vs P); regression je punkt im bestehenden tui-feld.

## Problem (Fund aus Hunt H-P1, datei-/#beleg in der Akte)
needs-TUI: kein sichtbarer Zurueck-Pfad (nur cancel), provider-zeile bricht bei 120 spalten um (appProviderChoice.View), provider-zeilen werden bei choicesForSelection()-fehler still verschluckt (app_wizard_controller.go:329-339), hinweis zeigt grosses P statt kleiner taste. Quelle Hunt H-P1 BF-02/BF-08/BF-09/BF-11.

## Acceptance
Rueckwaertsnavigation sichtbar; umbruchfeste zeilen; fehler bei choicesForSelection显示 statt verschlucken; geschmack konsistent (p vs P); regression je punkt im bestehenden tui-feld.

## Dependencies and file ownership
Keine. Write-set: cmd/baha tui needs-screen + provider choice views.
