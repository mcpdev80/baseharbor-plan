---
id: t-20261108-bughunt-app-name-identity-cluster
card_number: "0427-149"
card_short_title: "Duplicate names lock all"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-w149b-nameid2
kanban_status: active
kanban_lane: active
kanban_summary: "One name gate in the registry: registration checks collisions and fails closed with a clear message (no silent second uuid);…"
kanban_title: 0427-149 · Duplicate names lock all
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1475]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp3.md"]
---
- [ ] t-20261108-bughunt-app-name-identity-cluster · Bug Hunt v0.4.27: Duplicate names lock all #task #release/v0-4-27 #status/active #view/active #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** lane-w149b-nameid2 · **Priority:** normal  
    **PR:** [baseharbor#1475](https://github.com/mcpdev80/baseharbor/pull/1475)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp3.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** lane-w149b-nameid2  
**Priority:** normal  
**PRs:** [baseharbor#1475](https://github.com/mcpdev80/baseharbor/pull/1475)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
One name gate in the registry: registration checks collisions and fails closed with a clear message (no silent second uuid); name-based commands resolve uniquely or name the concrete way out (uuid path); edit/show/plan/destroy work in all (including already duplicate-loaded) states, with a cleanup path for existing dangling instances; regressions (dup-register, dup-edit, dup-destroy) in the lifecycle group.

## Problem (source evidence in the dossier)
app edit reports application machine: denied as soon as a second app with the same NAME+environment exists; app init silently registers a duplicate under a NEW uuid; app-create openings can no longer be opened or removed by any name-based command; the show/plan NAME hint names a flag that cannot resolve the collision. Source: hunt H-P3 BF-01/02/05/10 (blocker candidate).

## Acceptance
One name gate in the registry: registration checks collisions and fails closed with a clear message (no silent second uuid); name-based commands resolve uniquely or name the concrete way out (uuid path); edit/show/plan/destroy work in all (including already duplicate-loaded) states, with a cleanup path for existing dangling instances; regressions (dup-register, dup-edit, dup-destroy) in the lifecycle group.

## Dependencies and file ownership
None. Write-set: app registry name gate + app edit/init/create/show/plan/destroy.

## Audit note (Karten-Audit 2026-11-08)
Audit 2026-11-08 (mapping): BF-01/02/05 are one name-gate contract; BF-10 hint fix belongs here too; live lane w149 owns it. [Dossier](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/karten-audit-2026-11-08.md)
