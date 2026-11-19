---
id: t-20261118-diag-exec-iftrue-leak
release: v0.4.28
repos: [mcpdev80/baseharbor]
depends_on: []
kanban_status: review
owner: "Flash (codeman d5ecb550 / 0428-118)"
prs: [mcpdev80/baseharbor#1689]
card_number: 0428-118
card_short_title: fix DIAG_EXEC if-true leak in
kanban_title: 0428-118 · fix DIAG_EXEC if-true leak in
wait_reason: ""
blocker: ""

---
# t-20261118-diag-exec-iftrue-leak · DIAG_EXEC if-true leak in app edit apply

- [ ] t-20261118-diag-exec-iftrue-leak · fix DIAG_EXEC if-true leak in app_edit_apply.go #task #release/v0-4-28 #status/review #view/review #kind/task
    <!-- generated:card -->
    **Owner:** Flash (codeman d5ecb550 / 0428-118)  
    **PR:** [baseharbor#1689](https://github.com/mcpdev80/baseharbor/pull/1689)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** Flash (codeman d5ecb550 / 0428-118)  
**Priority:** not set  
**PRs:** [baseharbor#1689](https://github.com/mcpdev80/baseharbor/pull/1689)  
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

candidate 2d945e963; CI 44427145360 completed success; red c81985c6f -> green; evidence r28-welle4-2026-11-18/diag-exec-leak/fix-1.md
