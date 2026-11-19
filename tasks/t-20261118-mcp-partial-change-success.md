---
id: t-20261118-mcp-partial-change-success
release: v0.4.28
repos: [mcpdev80/baseharbor]
depends_on: []
owner: w1-lane-5584d84a (0428-120)
kanban_status: closed
card_number: 0428-120
card_short_title: MCP/HTTP edit path must fail
kanban_title: 0428-120 · MCP/HTTP edit path must fail
prs: [mcpdev80/baseharbor#1688]
wait_reason: ""
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1688"]

---
# t-20261118-mcp-partial-change-success · MCP/HTTP edit path reports partial provider-change as success

- [x] t-20261118-mcp-partial-change-success · MCP/HTTP edit path must fail loud on partial provider-change result #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** w1-lane-5584d84a (0428-120)  
    **PR:** [baseharbor#1688](https://github.com/mcpdev80/baseharbor/pull/1688)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1688)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w1-lane-5584d84a (0428-120)  
**Priority:** not set  
**PRs:** [baseharbor#1688](https://github.com/mcpdev80/baseharbor/pull/1688)  
**Source:** 
<!-- /generated:links -->

## Goal
Hunt 917 Befund 1 (MEDIUM): through `appMachineChangeDesired` an incomplete provider-change result can return with nil error; the CLI edit path catches `partial`, but the MCP/HTTP edit path returns success without checking `result.Status`. Make the MCP/HTTP path honor result.Status (fail loud on partial, same contract as CLI), with a regression that drives the MCP/HTTP handler directly (unit-only repro exists in the hunt akte).

## Scope
- MCP/HTTP edit-path files ONLY. Explicitly NOT cmd/baha machine-edit internals owned by 0428-118 in flight, and NOT the i18n/catalog files of 0428-093. If a shared helper must change: STOP with file:line, coord arbitrates ordering.

## Required checks
- go build/vet; MCP/HTTP + application unit tests on exact head.

## Dependencies and file ownership
- Source: hunt 917 befund-1.md, evidence/r28-welle4-2026-11-18/hunt-silentsuccess/befund-1.md (band 1cf56980 snapshot, END_DONE by lane ae414bfe).

END akzeptiert: head 23837dcc5 (rebase auf 9a37b4bc, base clean), exact-run 44426400958 SUCCESS, regression core921PendingPartialMCPReportsFailure red-without/green-with-fix, akte 7f622590 am band. Routing an CODEX-REVIEW

CODEX-REVIEW ACCEPT ohne Befund auf 75f67a526; Exact-head CI 44436020492 SUCCESS (PR Selected Checks von integration 15368), 21.20 runner-min; normaler Squash-Merge 7d343836447f976ec613fa4ae1cb09afcabbbbe0. Evidence: evidence/r28-welle4-2026-11-19/codex-welle3-review/1688.md.

MERGED: merge commit 7d3438364traegt #1688 (head 23837dcca5, review accepted mit merge-window-hopf wie verabredet). develop damit 7d3438364
