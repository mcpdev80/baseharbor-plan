---
id: t-20261108-bughunt-quickinit-failure-explain
card_number: "0427-141"
card_short_title: "Schnellstart ohne Grund"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: Fehler nennt kandidaten+fehlende unterscheidung; doku-/hilfezeile verweist auf app plan als trockener lauf; regression fuer…
kanban_title: 0427-141 · Schnellstart ohne Grund
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
- [ ] t-20261108-bughunt-quickinit-failure-explain · Bug Hunt v0.4.27: Schnellstart ohne Grundangabe #task #release/v0-4-27 #status/planned #view/ready #area/compose #area/lifecycle #kind/bug
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
Fehler nennt kandidaten+fehlende unterscheidung; doku-/hilfezeile verweist auf app plan als trockener lauf; regression fuer meldungstext.

## Problem (Fund aus Hunt H-D3, datei-/#beleg in der Akte)
app init --quick sagt nur no unambiguous requirements ohne kontext welche entscheidung fehlt; doku: up hat kein dry-run, app plan ist der ersatz. Quelle Hunt H-D3 BF-10/BF-11.

## Acceptance
Fehler nennt kandidaten+fehlende unterscheidung; doku-/hilfezeile verweist auf app plan als trockener lauf; regression fuer meldungstext.

## Dependencies and file ownership
Keine. Write-set: cmd/baha init meldungstext + docs.
