---
id: t-20261108-bughunt-damaged-state-misleading-error
card_number: "0427-159"
card_short_title: "Corrupted deployment state rep"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-0427-159-r7
kanban_status: wait
kanban_lane: wait
kanban_summary: "Damaged-state detection precedes generic limits: error names the missing record/network and the concrete recovery (re-up from…"
kanban_title: 0427-159 · Corrupted deployment state rep
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1499]
sources: []
blocker: ""
wait_reason: "APPROVED exact-head green d69d3c0b9 (run 42619991654, act-1499-review-r10) — wartet auf merge-griff"
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hx2.md"]
superseded_by: t-20261108-bughunt-0427-test-bootstrap-leak
---
- [ ] t-20261108-bughunt-damaged-state-misleading-error · Bug Hunt v0.4.27: Damaged state lies #task #release/v0-4-27 #status/wait #view/wait #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** lane-0427-159-r7 · **Priority:** normal  
    **PR:** [baseharbor#1499](https://github.com/mcpdev80/baseharbor/pull/1499)  
    **Waiting:** APPROVED exact-head green d69d3c0b9 (run 42619991654, act-1499-review-r10) — wartet auf merge-griff  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hx2.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** lane-0427-159-r7  
**Priority:** normal  
**PRs:** [baseharbor#1499](https://github.com/mcpdev80/baseharbor/pull/1499)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
Damaged-state detection precedes generic limits: error names the missing record/network and the concrete recovery (re-up from source or destroy-and-recreate); regression with a deliberately damaged fixture in the lifecycle group.

## Problem (source evidence in the dossier)
With deployment.json deleted and the network removed, up answers "repository inspection file limit exceeded" - misleading, hides the real damaged-state condition (BF-03, blocker candidate per hunt dossier).

## Acceptance
Damaged-state detection precedes generic limits: error names the missing record/network and the concrete recovery (re-up from source or destroy-and-recreate); regression with a deliberately damaged fixture in the lifecycle group.

## Dependencies and file ownership
None. Write-set: state reader / damaged-record paths.
