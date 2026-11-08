---
id: t-20261108-bughunt-appnew-name-slug-keywords
card_number: "0427-139"
card_short_title: "Name ohne Warnung verbogen"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Sichtbare normalisierung (hinweis wenn eingabe != Ergebnis) + reservierte keywords am name-prompt ablehnen; regressionen im…"
kanban_title: 0427-139 · Name ohne Warnung verbogen
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1458]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd3.md"]
---
- [ ] t-20261108-bughunt-appnew-name-slug-keywords · Bug Hunt v0.4.27: Namens.slugify und Keywordwall #task #release/v0-4-27 #status/planned #view/ready #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **PR:** [baseharbor#1458](https://github.com/mcpdev80/baseharbor/pull/1458)  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd3.md)  
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
Sichtbare normalisierung (hinweis wenn eingabe != Ergebnis) + reservierte keywords am name-prompt ablehnen; regressionen im bestehenden feld.

## Problem (Fund aus Hunt H-D3, datei-/#beleg in der Akte)
app new slugifyt still (My App!! -> my-app) und akzeptiert reservierte wortlike "cancel" als namen. Quelle Hunt H-D3 BF-03/BF-04.

## Acceptance
Sichtbare normalisierung (hinweis wenn eingabe != Ergebnis) + reservierte keywords am name-prompt ablehnen; regressionen im bestehenden feld.

## Dependencies and file ownership
Keine. Write-set: cmd/baha app new name validation.
