---
id: t-20261108-bughunt-up-nontty-panic-consent
card_number: "0427-157"
card_short_title: "Up panics and consent gate fai"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "No panic path: missing confirm input = clean usage error that PRINTS the exact --confirm-candidate hash; consent stage honors…"
kanban_title: 0427-157 · Up panics and consent gate fai
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hx2.md"]
superseded_by: t-20261108-bughunt-0427-test-bootstrap-leak
---
- [ ] t-20261108-bughunt-up-nontty-panic-consent · Bug Hunt v0.4.27: Non-TTY up panics #task #release/v0-4-27 #status/planned #view/ready #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hx2.md)  
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
No panic path: missing confirm input = clean usage error that PRINTS the exact --confirm-candidate hash; consent stage honors --yes/non-TTY with the same fail-closed semantics as interactive; regressions both branches in the lifecycle/cli-surface group.

## Problem (source evidence in the dossier)
(a) baha up without --confirm-candidate panics with a Go stack trace and the confirm hash is never surfaced on non-TTY (BF-01, blocker candidate); (b) the two-stage provider-impact consent demands an interactive TTY and auto-fails even with --yes (BF-02). Source: hunt H-X2.

## Acceptance
No panic path: missing confirm input = clean usage error that PRINTS the exact --confirm-candidate hash; consent stage honors --yes/non-TTY with the same fail-closed semantics as interactive; regressions both branches in the lifecycle/cli-surface group.

## Dependencies and file ownership
None. Write-set: up consent/confirm flow cmd/baha.
