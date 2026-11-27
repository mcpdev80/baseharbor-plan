---
id: t-20261124-0428-279-mcp-contract-app-pull-unexpected
card_number: "0428-279"
card_short_title: "MCP contract drift: app.pull"
type: bug
areas: [cli]
release: v0.4.28
version: ""
parent: ""
owner: w80-0428-279-mcpcontract
kanban_status: wait
kanban_lane: wait
kanban_summary: ""
kanban_title: 0428-279 · MCP contract drift: app.pull
priority: normal
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1826]
sources: []
blocker: ""
wait_reason: "parked for v0.5.x per owner disposition 2026-11-27, resolution-akte #1826 merged"
resolution: ""
evidence:
  - https://github.com/mcpdev80/baseharbor/actions/runs/45394505629
  - https://github.com/mcpdev80/baseharbor/pull/1826
---

- [ ] t-20261124-0428-279-mcp-contract-app-pull-unexpected · MCP contract drift: app.pull #task #release/v0-4-28 #status/wait #view/wait #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** w80-0428-279-mcpcontract · **Priority:** normal  
    **PR:** [baseharbor#1826](https://github.com/mcpdev80/baseharbor/pull/1826)  
    **Waiting:** parked for v0.5.x per owner disposition 2026-11-27, resolution-akte \#1826 merged  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/45394505629), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1826)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w80-0428-279-mcpcontract  
**Priority:** normal  
**PRs:** [baseharbor#1826](https://github.com/mcpdev80/baseharbor/pull/1826)  
**Source:** 
<!-- /generated:links -->

## Problem

- Where: the static/mcp contract gate (v0.4.28). Source of truth for the expected MCP tool/method set vs the live MCP server surface. Find the contract definition (grep for `baseharbor.app.` method names + the contract assertion that emits 'MCP contract mismatch') in cmd/baha/mcp.go (or the contract test/fixture it compares against).
- Expected: the exposed MCP method set and the contract's expected set agree — either baseharbor.app.pull is a sanctioned method and is IN the expected contract, or it must not be exposed.
- Actual: the gate sees baseharbor.app.pull as UNEXPECTED (missing=[] so nothing is absent; one extra method is present). A prior change added/exposed app.pull without reconciling the contract list, OR a stale contract still rejects it.

## Regression

- Reconcile the MCP contract for baseharbor.app.pull: add it to the expected contract method set (if app.pull is intended, which matches the app pull/runtime-fetch capability) AND assert the live server tool list equals the contract (no unexpected/missing) so future drift fails loud. If app.pull is NOT intended, remove it from the server surface instead — decide by reading the contract's purpose + any related card (#1599/#1693 CLI2 family, mcp.go).

## Acceptance

- The v0.4.28 static/mcp gate passes on the exact candidate with zero unexpected/missing methods.
- A test asserts the MCP server's exposed method set == the contract expected set (fail-loud on drift), and explicitly covers baseharbor.app.pull.
- New test discovered by the static/mcp selected check; no scripts/** or .github/** change (if the contract list lives in a CI file, STOP + report file:line for the owner).
