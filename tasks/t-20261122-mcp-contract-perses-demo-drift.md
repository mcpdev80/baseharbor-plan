---
id: t-20261122-mcp-contract-perses-demo-drift
card_number: "0428-232"
card_short_title: "perses MCP contract demo drift"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: ""
kanban_title: 0428-232 · perses MCP contract demo drift
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261122-mcp-contract-perses-demo-drift · perses MCP contract demo drift #task #release/v0-4-28 #status/planned #view/ready #kind/task
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


## Why

`Static · mcp` job 137080600598 at head `fec44963` fails with the emitted line

`RuntimeError: MCP contract mismatch: missing=[] unexpected=['baseharbor.app.perses.disable', 'baseharbor.app.perses.enable', 'baseharbor.app.perses.remove', 'baseharbor.app.perses.status']`

The four tools are registered on the product side in `internal/machine/contract.go:205-208`, and the product test
expectation was already extended by merged PR #1751 (`cmd/baha/agent_mcp_test.go:146-149`, card
`t-20261121-mcp-release-gate-perses-tool-drift`, closed/accepted). The gate still compares against the expected list
carried by the pinned Demo reference `5d1cf312e18d06915db35c340bebe4e3d4f39d45`, so the drift is on the contract
fixture side, not in #1746's diff.

## Acceptance

- The machine contract golden (`contracts/machine/v1/control.golden.json`) and the Demo-side expected tool list agree on
  the four `app.perses.*` tools, or the Demo pin is moved to a reference that already agrees.
- `Static · mcp` is green at one exact head of #1746; `missing=[]` alone is not enough - the unexpected list must be
  empty.
