---
id: t-20261108-bughunt-docker-netpool-exhaustion
card_number: "0427-146"
card_short_title: "app init Owner-Naht regression"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: Die netz-anlege-fehlerstelle faengt den pool-exhaustion-fehler und meldet konkreten naechsten schritt (freigebene netze nennen /…
kanban_title: 0427-146 · app init Owner-Naht regression
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
- [ ] t-20261108-bughunt-docker-netpool-exhaustion · Bug Hunt v0.4.27: Netzpool-Erschoepfung ohne Rat #task #release/v0-4-27 #status/planned #view/ready #area/compose #area/lifecycle #kind/bug
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
Die netz-anlege-fehlerstelle faengt den pool-exhaustion-fehler und meldet konkreten naechsten schritt (freigebene netze nennen / docker network prune hinweis mit target-bezug); regression mit erzeugbarem fehlerpfad (mock/invalid netz-name) in der lifecycle gruppe; host-seitige erschoepfung selbst ist owner-scope, nicht produkt-fix.

## Problem (Fund aus Hunt H-D4, datei-/#beleg in der Akte)
Auf gesaettigtem docker-host bricht baha up (Core wie workload) an "all predefined address pools have been fully subnetted" ohne jeden recovery-hinweis; user sieht nur die daemon-zeile. Quelle Hunt H-D4 BF-hd4-1 (HOCH).

## Acceptance
Die netz-anlege-fehlerstelle faengt den pool-exhaustion-fehler und meldet konkreten naechsten schritt (freigebene netze nennen / docker network prune hinweis mit target-bezug); regression mit erzeugbarem fehlerpfad (mock/invalid netz-name) in der lifecycle gruppe; host-seitige erschoepfung selbst ist owner-scope, nicht produkt-fix.

## Dependencies and file ownership
Keine. Write-set: compose netz-anlage fehlerpfad in core/workload up.
