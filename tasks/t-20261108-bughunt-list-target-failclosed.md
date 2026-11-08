---
id: t-20261108-bughunt-list-target-failclosed
card_number: "0427-148"
card_short_title: "app init Owner-Naht regression"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Entscheidung dokumentiert (fail-closed behalten ODER alle-targets-ansicht mit target-spalte); wenn behalten:…"
kanban_title: 0427-148 · app init Owner-Naht regression
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
- [ ] t-20261108-bughunt-list-target-failclosed · Bug Hunt v0.4.27: Liste ohne Zielwahl #task #release/v0-4-27 #status/planned #view/ready #area/compose #area/lifecycle #kind/bug
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
Entscheidung dokumentiert (fail-closed behalten ODER alle-targets-ansicht mit target-spalte); wenn behalten: quickstart-/hilfezeile nennt das verhalten; regression deckt die gewaehlte semantik ab.

## Problem (Fund aus Hunt H-D4, datei-/#beleg in der Akte)
baha list ohne BASEHARBOR_TARGET schliesst bei >1 target fail-closed (text mit auswahl+next ist korrekt, but fluss-bremse fuer quickstart-mehrfach-targets). source: Hunt H-D4 BF-hd4-3 (niedrig).

## Acceptance
Entscheidung dokumentiert (fail-closed behalten ODER alle-targets-ansicht mit target-spalte); wenn behalten: quickstart-/hilfezeile nennt das verhalten; regression deckt die gewaehlte semantik ab.

## Dependencies and file ownership
Keine. Write-set: cmd/baha list + target doku.
