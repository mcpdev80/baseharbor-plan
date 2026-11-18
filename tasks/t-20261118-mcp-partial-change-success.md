---
id: t-20261118-mcp-partial-change-success
release: v0.4.28
repos: [mcpdev80/baseharbor]
depends_on: []
kanban_status: active
card_number: 0428-120
card_short_title: MCP/HTTP edit path must fail
kanban_title: 0428-120 · MCP/HTTP edit path must fail
---
# t-20261118-mcp-partial-change-success · MCP/HTTP edit path reports partial provider-change as success

- [ ] t-20261118-mcp-partial-change-success · MCP/HTTP edit path must fail loud on partial provider-change result #task #release/v0-4-28 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
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
