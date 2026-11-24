---
id: t-20261124-0428-279-mcp-contract-app-pull-unexpected
card_number: "0428-279"
card_short_title: "MCP contract drift: app.pull"
type: bug
areas: [cli]
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "v0.4.28 static/mcp runtime gate reports MCP contract mismatch unexpected=['baseharbor.app.pull'] (missing=[]): the MCP server exposes baseharbor.app.pull but the contract's expected method set does not include it (or app.pull must not be exposed). Independent of #1825."
kanban_title: 0428-279 · MCP contract drift: app.pull
priority: medium
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence:
  - hosted v0.4.28 static/mcp gate job 138450101757 on Pre-Release run 45394505629 (head 844987ded88b1c365f5b660e3f700af69e52bb5a): RuntimeError: MCP contract mismatch: missing=[] unexpected=['baseharbor.app.pull']
---

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
