---
id: t-20261108-bughunt-quickinit-failure-explain
card_number: "0427-141"
card_short_title: "Quick init no reason"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: "chatgpt-r27-cli-diagnostics"
kanban_status: active
kanban_lane: active
kanban_summary: The error names candidates and the missing distinction; docs/help line points to app plan as the dry run; regression for the…
kanban_title: 0427-141 · Quick init no reason
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1466]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd3.md"]
---
- [ ] t-20261108-bughunt-quickinit-failure-explain · Bug Hunt v0.4.27: Quick init names no reason #task #release/v0-4-27 #status/active #view/active #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** chatgpt-r27-cli-diagnostics · **Priority:** normal  
    **PR:** [baseharbor#1466](https://github.com/mcpdev80/baseharbor/pull/1466)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hd3.md)  
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
The error names candidates and the missing distinction; docs/help line points to app plan as the dry run; regression for the message text.

## Problem (source evidence in the dossier)
app init --quick only says no unambiguous requirements without context on which decision failed; docs: up has no dry-run, app plan is the substitute. Source: hunt H-D3 BF-10/BF-11.

## Acceptance
The error names candidates and the missing distinction; docs/help line points to app plan as the dry run; regression for the message text.

## Dependencies and file ownership
None. Write-set: cmd/baha init message + docs.

## Audit note (Karten-Audit 2026-11-08)
Audit 2026-11-08 (zuerklaeren): open owner PR #1466 carries the actionable quick-init diagnosis; card stays claimed by chatgpt-r27-cli-diagnostics until that exact head is green. [Dossier](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/karten-audit-2026-11-08.md)
