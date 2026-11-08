---
id: t-20261108-bughunt-stale-provider-edit-block
card_number: "0427-150"
card_short_title: "Stale instance blocks edit"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: Provider-instance check on edit refresh (stale = re-resolve or report clearly); regression with a state-only app in the same…
kanban_title: 0427-150 · Stale instance blocks edit
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
- [ ] t-20261108-bughunt-stale-provider-edit-block · Bug Hunt v0.4.27: Stale instance blocks edit #task #release/v0-4-27 #status/planned #view/ready #area/compose #area/lifecycle #kind/bug
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
Provider-instance check on edit refresh (stale = re-resolve or report clearly); regression with a state-only app in the same target in the lifecycle group.

## Problem (source evidence in the dossier)
app edit cannot change a need when an unapplied state-only app exists: a stale provider instance in the target registry leads to broken references. Source: hunt H-P3 BF-03 (blocker candidate).

## Acceptance
Provider-instance check on edit refresh (stale = re-resolve or report clearly); regression with a state-only app in the same target in the lifecycle group.

## Dependencies and file ownership
None. Write-set: target registry provider-instance refresh on the edit path.

## Audit note (Karten-Audit 2026-11-08)
Audit 2026-11-08 (mapping): same registry surface as #149 - sequence after the name gate lands. [Dossier](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/karten-audit-2026-11-08.md)
