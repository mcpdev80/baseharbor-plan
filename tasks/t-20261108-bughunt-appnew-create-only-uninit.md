---
id: t-20261108-bughunt-appnew-create-only-uninit
card_number: "0427-140"
card_short_title: "app new ohne Init"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: Entweder dokumentierter zweischritt mit klarer naechster-aktion ODER automatischer init im create-pfad — entscheidung mit…
kanban_title: 0427-140 · app new ohne Init
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
- [ ] t-20261108-bughunt-appnew-create-only-uninit · Bug Hunt v0.4.27: app new nur-anlegen ohne Init #task #release/v0-4-27 #status/planned #view/ready #area/compose #area/lifecycle #kind/bug
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
Entweder dokumentierter zweischritt mit klarer naechster-aktion ODER automatischer init im create-pfad — entscheidung mit begruendung; regression im lifecycle-pfad.

## Problem (Fund aus Hunt H-D3, datei-/#beleg in der Akte)
app-new im create-only-pfad hinterlässt ein repo ohne init-zustand; up/plan/show fordern dann init — flussluecke (mittel, untersuchen). Quelle Hunt H-D3 BF-09.

## Acceptance
Entweder dokumentierter zweischritt mit klarer naechster-aktion ODER automatischer init im create-pfad — entscheidung mit begruendung; regression im lifecycle-pfad.

## Dependencies and file ownership
Keine. Write-set: cmd/baha app new + init seam.
