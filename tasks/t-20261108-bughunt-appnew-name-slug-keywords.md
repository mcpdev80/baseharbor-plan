---
id: t-20261108-bughunt-appnew-name-slug-keywords
card_number: "0427-139"
card_short_title: "Name reshaped silently"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: "chatgpt-r27-appnew"
kanban_status: active
kanban_lane: active
kanban_summary: "Visible normalization (note when input != result) + reject reserved keywords at the name prompt; regressions in the existing…"
kanban_title: 0427-139 · Name reshaped silently
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1465]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd3.md"]
---
- [ ] t-20261108-bughunt-appnew-name-slug-keywords · Bug Hunt v0.4.27: Name silently reshaped #task #release/v0-4-27 #status/planned #view/ready #area/compose #area/lifecycle #kind/bug
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
Visible normalization (note when input != result) + reject reserved keywords at the name prompt; regressions in the existing field.

## Problem (source evidence in the dossier)
app new silently slugifies input (My App!! -> my-app) and accepts reserved words like cancel as a name. Source: hunt H-D3 BF-03/BF-04.

## Acceptance
Visible normalization (note when input != result) + reject reserved keywords at the name prompt; regressions in the existing field.

## Dependencies and file ownership
None. Write-set: cmd/baha app new name validation.
