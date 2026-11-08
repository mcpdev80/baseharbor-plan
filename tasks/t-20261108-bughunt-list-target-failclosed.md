---
id: t-20261108-bughunt-list-target-failclosed
card_number: "0427-148"
card_short_title: "List needs target choice"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: "chatgpt-r27-cli-diagnostics"
kanban_status: active
kanban_lane: active
kanban_summary: "Decision documented (keep fail-closed OR add an all-targets view with a target column); if kept: quickstart/help line mentions…"
kanban_title: 0427-148 · List needs target choice
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1466]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd4.md"]
---
- [ ] t-20261108-bughunt-list-target-failclosed · Bug Hunt v0.4.27: List needs target choice #task #release/v0-4-27 #status/active #view/active #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** chatgpt-r27-cli-diagnostics · **Priority:** normal  
    **PR:** [baseharbor#1466](https://github.com/mcpdev80/baseharbor/pull/1466)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd4.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** chatgpt-r27-cli-diagnostics  
**Priority:** normal  
**PRs:** [baseharbor#1466](https://github.com/mcpdev80/baseharbor/pull/1466)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
Decision documented (keep fail-closed OR add an all-targets view with a target column); if kept: quickstart/help line mentions the behavior; regression covers the chosen semantics.

## Problem (source evidence in the dossier)
baha list without BASEHARBOR_TARGET fails closed when more than one target is configured (the error text with choices+Next is correct, but it stalls quickstart flows on multi-target setups). Source: hunt H-D4 BF-hd4-3 (low).

## Acceptance
Decision documented (keep fail-closed OR add an all-targets view with a target column); if kept: quickstart/help line mentions the behavior; regression covers the chosen semantics.

## Dependencies and file ownership
None. Write-set: cmd/baha list + target docs.
