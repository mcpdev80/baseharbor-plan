---
id: t-20261122-mcp-contract-perses-demo-drift
card_number: "0428-232"
card_short_title: "perses MCP contract demo drift"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: coord (befund) / external demo owner (aktion)
kanban_status: blocked
kanban_lane: blocked
kanban_summary: ""
kanban_title: 0428-232 · perses MCP contract demo drift
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: "der gepinnte Demo-Vertrag (baseharbor-demo) ist NICHT im lane-zugriff - externe Demo-owner aktion: die vier tools baseharbor.app.perses.{disable,enable,remove,status} in den Demo-expected-tool-list aufnehmen, damit static-mcp sie nicht mehr als unexpected zaehlt. Kein Codeman-produkt/aenderung moeglich, repo ist extern."
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/mcp-contract-0428-232/round-1.md"]
---

- [ ] t-20261122-mcp-contract-perses-demo-drift · perses MCP contract demo drift #task #release/v0-4-28 #status/blocked #view/blocked #kind/task
    <!-- generated:card -->
    **Owner:** coord (befund) / external demo owner (aktion)  
    **Blocker:** der gepinnte Demo-Vertrag (baseharbor-demo) ist NICHT im lane-zugriff - externe Demo-owner aktion: die vier tools baseharbor.app.perses.{disable,enable,remove,status} in den Demo-expected-tool-list aufnehmen, damit static-mcp sie nicht meh…  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/mcp-contract-0428-232/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** coord (befund) / external demo owner (aktion)  
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

Der drift ist nicht mehr nur behauptet, sondern von einem gehosteten statischen gate gemessen: job 137102052168 aus run 44987381250 meldet 'MCP contract mismatch: missing=[] unexpected=[baseharbor.app.perses.disable/enable/remove/status]'. Der eine freie sitz arbeitet daran (mission sha 04ab43ff7e73); falls contracts/** Owner-scope bleibt, liefert die lane das rezept mit datei:zeile und ich melde denbedarf.

Ursache ist NICHT der produktcontract: die vier perses-methoden sind legitima exponiert (cmd/baha/mcp_lifecycle_extra.go:61-75, internal/machine/contract.go:205-208, Operations meldet sie und MCPTools bei zeile 270 liefert jedes nicht-leere MCPTool) und stehen bereits im produkt-internen golden. Die abweichende liste liegt im DEMO-REPO: baseharbor-demo/tests/mcp/run.sh, das expected-set bei zeile 31 (ein Python set-literal), die bracket-zeilen 72-73 fuer baseharbor.app.perses.*, und der comparer bei 127-128; aufgerufen wird die position aus baseharbor-demo/.github/workflows/pre-release-runtime-suite.yml:267 (mcp-branch). Die lane hat korrekt STOP gemeldet: die korrektur ist ein ADDITIVER golden-eintrag im demo-repo, also Owner-scope. Rezept mit exakten zeilen liegt in der akte mcp-contract-0428-232/round-1.md. Diese karte bleibt blocked auf diesen einen demo-edit; nach dem edit melde ich den statischen mcp-gate-nachweis neu an.

VON active zurueck auf blocked: 0847d100 wurde losgeschickt, aber sie ist im gepinnten DEMO-repo extern, nicht lane-aenderbar. static-mcp 137190621450 braucht die vier perses tools im demo-expected-list. Befund liegt vor, aktion = externer demo owner. Kein blocked-heben ohne deren zugriff.
