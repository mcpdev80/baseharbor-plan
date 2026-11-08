---
id: t-20261108-bughunt-wizard-foreign-records
card_number: "0427-144"
card_short_title: "app init Owner-Naht regression"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: Provider resolution toleriert fremde records sauber oder meldet den konkreten konflikt loesbar; regression mit zwei apps auf…
kanban_title: 0427-144 · app init Owner-Naht regression
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
- [ ] t-20261108-bughunt-wizard-foreign-records · Bug Hunt v0.4.27: Fremde Records storen Wizard #task #release/v0-4-27 #status/planned #view/ready #area/compose #area/lifecycle #kind/bug
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
Provider resolution toleriert fremde records sauber oder meldet den konkreten konflikt loesbar; regression mit zwei apps auf einem target in der lifecycle gruppe.

## Problem (Fund aus Hunt H-P1, datei-/#beleg in der Akte)
Wizardlaeufe auf einem target mit fremden/anhaengigen deployment-records koennen bei provider resolution an missing-dependency scheitern (nach sql+http app scheiterten folgende http-only-zellen auf echtem host-target). Quelle Hunt H-P1 BF-06.

## Acceptance
Provider resolution toleriert fremde records sauber oder meldet den konkreten konflikt loesbar; regression mit zwei apps auf einem target in der lifecycle gruppe.

## Dependencies and file ownership
Keine. Write-set: internal provider resolution + deployment records.
