---
id: t-20261118-diag-exec-iftrue-leak
release: v0.4.28
repos: [mcpdev80/baseharbor]
depends_on: []
kanban_status: planned
card_number: 0428-118
card_short_title: fix DIAG_EXEC if-true leak in
kanban_title: 0428-118 · fix DIAG_EXEC if-true leak in
---
# t-20261118-diag-exec-iftrue-leak · DIAG_EXEC if-true leak in app edit apply

- [ ] t-20261118-diag-exec-iftrue-leak · fix DIAG_EXEC if-true leak in app_edit_apply.go #task #release/v0-4-28 #status/planned #view/ready #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal
Hunt 916 defect I1: `cmd`? no — `internal/application/app_edit_apply.go:372-376` contains an if-true leak gated by the DIAG_EXEC environment signal: a diagnostic execution path is reachable where the guard never blocks. Fix the guard so DIAG_EXEC cannot alter production behavior; add a regression asserting identical behavior with DIAG_EXEC unset vs set (in the affected CI group).

## Scope
- app_edit_apply.go guard + one regression test. No behavior change otherwise.

## Required checks
- go build/vet, internal/application unit tests on exact head.

## Dependencies and file ownership
- Source: hunt 916 befund-1.md defect I1, evidence/r28-welle4-2026-11-18/hunt-ownership/befund-1.md (origin/main 20ddd05e).
