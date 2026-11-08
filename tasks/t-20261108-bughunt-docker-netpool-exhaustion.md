---
id: t-20261108-bughunt-docker-netpool-exhaustion
card_number: "0427-146"
card_short_title: "No advice on pool error"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: The network-create error site catches pool exhaustion and reports a concrete next step (name released nets / docker network…
kanban_title: 0427-146 · No advice on pool error
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd4.md"]
---
- [ ] t-20261108-bughunt-docker-netpool-exhaustion · Bug Hunt v0.4.27: No advice on pool error #task #release/v0-4-27 #status/planned #view/ready #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd4.md)  
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
The network-create error site catches pool exhaustion and reports a concrete next step (name released nets / docker network prune hint with target context); regression with a producible error path (mock/invalid network name) in the lifecycle group; host-side exhaustion itself is owner-scope, not a product fix.

## Problem (source evidence in the dossier)
On a saturated docker host, baha up (core and workload) dies on all predefined address pools have been fully subnetted without any recovery hint; the user only sees the daemon line. Source: hunt H-D4 BF-hd4-1 (HIGH).

## Acceptance
The network-create error site catches pool exhaustion and reports a concrete next step (name released nets / docker network prune hint with target context); regression with a producible error path (mock/invalid network name) in the lifecycle group; host-side exhaustion itself is owner-scope, not a product fix.

## Dependencies and file ownership
None. Write-set: compose network creation error paths in core/workload up.
