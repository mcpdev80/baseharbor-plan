---
id: t-20261108-bughunt-appnew-create-only-uninit
card_number: "0427-140"
card_short_title: "app new left uninit"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Either a documented two-step with a clear next action, or automatic init in the create path - decision with rationale;…"
kanban_title: 0427-140 · app new left uninit
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd3.md"]
---
- [ ] t-20261108-bughunt-appnew-create-only-uninit · Bug Hunt v0.4.27: app new left uninit #task #release/v0-4-27 #status/planned #view/ready #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd3.md)  
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
Either a documented two-step with a clear next action, or automatic init in the create path - decision with rationale; regression in the lifecycle path.

## Problem (source evidence in the dossier)
The create-only path of app new leaves a repository without init state; up/plan/show then demand init - a flow gap (medium, investigate). Source: hunt H-D3 BF-09; reinforced by hunt H-P1 BF-04 (create-only on an ownerless target reports project created but ... with no recovery path).

## Acceptance
Either a documented two-step with a clear next action, or automatic init in the create path - decision with rationale; regression in the lifecycle path.

## Dependencies and file ownership
None. Write-set: cmd/baha app new + init seam.
