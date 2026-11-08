---
id: t-20261108-bughunt-destroy-data-root-residual
card_number: "0427-152"
card_short_title: "Destroy finds own core"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Destroy resolves owned core targets from the data root (never discards foreign targets, fail-closed per the card-127 doctrine);…"
kanban_title: 0427-152 · Destroy finds own core
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/bughunt-ca-pkce/act-1455-fate.md"]
---
- [ ] t-20261108-bughunt-destroy-data-root-residual · Bug Hunt v0.4.27: Destroy finds own core #task #release/v0-4-27 #status/planned #view/ready #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/bughunt-ca-pkce/act-1455-fate.md)  
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
Destroy resolves owned core targets from the data root (never discards foreign targets, fail-closed per the card-127 doctrine); use the two commits as a base or deliberately re-slice with rationale; regression destroy+core in the lifecycle field.

## Problem (source evidence in the dossier)
The destroy change from PR #1455 (resolve owned core targets from the data root) landed in NO ancestry of develop or #1457 - the review confirms residual commits a2761413 + 9a963000. PR #1455 is closed; this card is its contract. Source: act-1455-fate.md.

## Acceptance
Destroy resolves owned core targets from the data root (never discards foreign targets, fail-closed per the card-127 doctrine); use the two commits as a base or deliberately re-slice with rationale; regression destroy+core in the lifecycle field.

## Dependencies and file ownership
None. Write-set: internal destroy + data-root resolution.
