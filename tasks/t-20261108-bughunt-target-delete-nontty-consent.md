---
id: t-20261108-bughunt-target-delete-nontty-consent
card_number: "0427-164"
card_short_title: "target delete fails non-TTY ev"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-w164-delconsent
kanban_status: active
kanban_lane: active
kanban_summary: ""
kanban_title: 0427-164 · target delete fails non-TTY ev
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hx3.md"]
superseded_by: t-20261108-bughunt-0427-test-bootstrap-leak
---
- [ ] t-20261108-bughunt-target-delete-nontty-consent · Bug Hunt v0.4.27: Target delete needs TTY #task #release/v0-4-27 #status/active #view/active #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** lane-w164-delconsent · **Priority:** normal  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hx3.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** lane-w164-delconsent  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
--yes honors non-TTY for the config-only delete with the same fail-closed semantics as the interactive flow; a real destructive step (if any remains) keeps its confirmation. Regression with shared cancel-path decision of 138/157.

## Problem (source evidence in the dossier)
target delete demands 2 interactive provider-impact confirmations and fails with impact-confirmation-required on non-TTY even with --yes, although the action is config-only and non-destructive to state (BF-03). Same consent-gate root cause as 0427-157 but on the delete path.

## Acceptance
--yes honors non-TTY for the config-only delete with the same fail-closed semantics as the interactive flow; a real destructive step (if any remains) keeps its confirmation. Regression with shared cancel-path decision of 138/157.

## Dependencies and file ownership
None. Write-set: target delete confirmation path.
