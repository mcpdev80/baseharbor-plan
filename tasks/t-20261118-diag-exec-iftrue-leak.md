---
id: t-20261118-diag-exec-iftrue-leak
release: v0.4.28
repos: [mcpdev80/baseharbor]
depends_on: []
kanban_status: closed
owner: w01-0428-118 (codeman d5ecb550)
prs: [mcpdev80/baseharbor#1689]
card_number: 0428-118
card_short_title: fix DIAG_EXEC if-true leak in
kanban_title: 0428-118 · fix DIAG_EXEC if-true leak in
wait_reason: ""
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1689"]

---
# t-20261118-diag-exec-iftrue-leak · DIAG_EXEC if-true leak in app edit apply

- [x] t-20261118-diag-exec-iftrue-leak · fix DIAG_EXEC if-true leak in app_edit_apply.go #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** w01-0428-118 (codeman d5ecb550)  
    **PR:** [baseharbor#1689](https://github.com/mcpdev80/baseharbor/pull/1689)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1689)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.28  
**Depends on:** none  
**Owner:** w01-0428-118 (codeman d5ecb550)  
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

END akzeptiert: head 2d945e963 auf base 9a37b4bc, red c81985c6f -> green, exact-run 44427145360 SUCCESS, akte fix-1.md (463d9d65) mit 9 head-referenzen. GitHub meldet 'behind' — pruefen ob develop erneut zog; merge-fenster wie besprochen. Routing an CODEX-REVIEW

CODEX-REVIEW ACCEPT ohne Befund auf 2d8cef5ef; Exact-head CI 44432398707 SUCCESS (PR Selected Checks von integration 15368), 32.13 runner-min; normaler Squash-Merge de53246585560ddf2c3e6ceae6d0f6eea6b71b68. Evidence: evidence/r28-welle4-2026-11-19/codex-welle3-review/1689.md.

MERGED: develop de5324658 traegt den PR (squash/merge wie am band ausgewiesen); kandidat-kette 2d945e963 -> hopf 2d8cef5ef (Codex-review-lane, normaler develop-merge) -> merge de5324658. Exact-run auf 2d8cef5ef war terminal gruen (#6511). Red c81985c6f -> green belegt, akte fix-1.md 463d9d65
