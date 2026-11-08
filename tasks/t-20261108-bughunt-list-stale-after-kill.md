---
id: t-20261108-bughunt-list-stale-after-kill
card_number: "0427-160"
card_short_title: "Stale entries after SIGKILL an"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-w160c-stalelist3
kanban_status: active
kanban_lane: active
kanban_summary: "list/status reconciles against the live provider state (failed unit = not applied, actionable hint); MISSING gains a next-action…"
kanban_title: 0427-160 · Stale entries after SIGKILL an
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1491]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hx2.md"]
superseded_by: t-20261108-bughunt-0427-test-bootstrap-leak
---
- [ ] t-20261108-bughunt-list-stale-after-kill · Bug Hunt v0.4.27: Liste zeigt Leichen #task #release/v0-4-27 #status/active #view/active #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** lane-w160c-stalelist3 · **Priority:** normal  
    **PR:** [baseharbor#1491](https://github.com/mcpdev80/baseharbor/pull/1491)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hx2.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** lane-w160c-stalelist3  
**Priority:** normal  
**PRs:** [baseharbor#1491](https://github.com/mcpdev80/baseharbor/pull/1491)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
list/status reconciles against the live provider state (failed unit = not applied, actionable hint); MISSING gains a next-action line (prune/re-attach) with a regression per case in the cli-surface group.

## Problem (source evidence in the dossier)
After SIGKILL of a Quadlet workload the unit is failed and the container gone, yet app list keeps reporting stale state (BF-04); a destroyed app whose repo was deleted shows a bare MISSING with no next action (BF-05).

## Acceptance
list/status reconciles against the live provider state (failed unit = not applied, actionable hint); MISSING gains a next-action line (prune/re-attach) with a regression per case in the cli-surface group.

## Dependencies and file ownership
None. Write-set: app list/status reconciliation paths.

## COORD CORRECTION 2026-11-08
Coordinator closed this card on a false merge claim (#1491 was never merged; SHA 8f2a90617 does not exist). State restored to review. PR #1491 (head cd9eca82e) is OPEN and needs: rebase onto current develop, terminal hosted run with real native cells.
