---
id: t-20261108-bughunt-wizard-success-next-lines
card_number: "0427-142"
card_short_title: "app init Owner-Naht regression"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Erfolgs-/Naechste-Texte in allen create-Pfaden konsistent (wizard wie headless, alias wie top-level); Eingabefehler an Prompts…"
kanban_title: 0427-142 · app init Owner-Naht regression
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
- [ ] t-20261108-bughunt-wizard-success-next-lines · Bug Hunt v0.4.27: Erfolg meldet Naechstes nicht #task #release/v0-4-27 #status/planned #view/ready #area/compose #area/lifecycle #kind/bug
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
Erfolgs-/Naechste-Texte in allen create-Pfaden konsistent (wizard wie headless, alias wie top-level); Eingabefehler an Prompts als usageError mit Next-Zeile; regressionen in der cli-surface gruppe.

## Problem (Fund aus Hunt H-P1, datei-/#beleg in der Akte)
Create-only- und headless-Erfolgspfade liefern unterschiedliche, teils fehlende Erfolgs- und Naechste-Schritte-Texte; yes/no-Eingabefehler haerten mit Exit 1 ohne Next-Block (usageError statt fmt.Errorf). Quelle Hunt H-P1 BF-01/BF-03/BF-07.

## Acceptance
Erfolgs-/Naechste-Texte in allen create-Pfaden konsistent (wizard wie headless, alias wie top-level); Eingabefehler an Prompts als usageError mit Next-Zeile; regressionen in der cli-surface gruppe.

## Dependencies and file ownership
Keine. Write-set: cmd/baha app new + wizard meldungswege.
