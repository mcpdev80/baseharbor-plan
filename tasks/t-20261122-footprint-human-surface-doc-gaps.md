---
id: t-20261122-footprint-human-surface-doc-gaps
card_number: "0428-246"
card_short_title: "footprint human doc gaps"
type: maintenance
areas: [cli, documentation]
release: v0.4.28
version: ""
parent: v0.4.28
owner: Coordinator (parity defect intake) / Owner-Core (canonical-output ruling) / a lane (product fix)
kanban_status: blocked
kanban_lane: blocked
kanban_summary: ""
kanban_title: 0428-246 · footprint human doc gaps
priority: normal
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1773, mcpdev80/baseharbor#1783]
sources: []
blocker: "NEUER BESTAETIGTER PRODUKT-DEFECT (critical path): tests/guided/new_edit.py:63 footprint_parity assertiert native CLI footprint JSON == MCP footprint JSON, beide selected data-caps jobs zeigen DIVERGENZ. Product code: cmd/baha/mcp.go:248 registerMCPFootprintShowTool vs cmd/baha/app_footprint_presenter.go. OWNER-CORE-ENTSCHEID noetig: welche output-form ist kanonisch (presenter oder mcp), dann product fix + regression. DIES blockiert ALLE selected data-caps zellen (#1783/#1780/#1770/#1773/#1738-A) - NICHT das operator fixture. (Y) runtime:edge broker = 0428-237 separat. develop b27b2ebe."
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261122-footprint-human-surface-doc-gaps · Document that the human footprint surface is a curated subset and explain the two divergences vs the JSON/MCP contract #task #release/v0-4-28 #status/blocked #view/blocked #area/cli #area/documentation #kind/maintenance
    <!-- generated:card -->
    **Owner:** Coordinator (parity defect intake) / Owner-Core (canonical-output ruling) / a lane (product fix) · **Priority:** normal  
    **PR:** [baseharbor#1773](https://github.com/mcpdev80/baseharbor/pull/1773), [baseharbor#1783](https://github.com/mcpdev80/baseharbor/pull/1783)  
    **Blocker:** NEUER BESTAETIGTER PRODUKT-DEFECT (critical path): tests/guided/new\_edit.py:63 footprint\_parity assertiert native CLI footprint JSON == MCP footprint JSON, beide selected data-caps jobs zeigen DIVERGENZ. Product code: cmd/baha/mcp.go:248 r…  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** Coordinator (parity defect intake) / Owner-Core (canonical-output ruling) / a lane (product fix)  
**Priority:** normal  
**PRs:** [baseharbor#1773](https://github.com/mcpdev80/baseharbor/pull/1773), [baseharbor#1783](https://github.com/mcpdev80/baseharbor/pull/1783)  
**Source:** 
<!-- /generated:links -->

## Found by bug-hunt H-V25 (0847d100) on develop 62784eff

Read-only audit confirmed the JSON and MCP footprint outputs are byte-identical (no data defect). The human-readable presenter is by
design a curated subset, but two divergences are undocumented and read like defects to an operator:

- B3: a status value is rendered with a switched/reworded human label vs the machine status token, without noting the mapping.
- B4: scope/ownership fields that the JSON contract carries are absent from the human view with no explanatory line.

## Acceptance

1. Document the human-vs-machine status label mapping (one line near the presenter or in the footprint help) so the switch is intentional and traceable.
2. Add a short human-view note that scope/ownership are available via JSON/MCP (or render them), so the curated subset does not read as a missing field.
3. No behavioral change to the JSON/MCP contract; no native/CI change. Regression only if a help/annotation string is asserted somewhere.

## Boundaries

cmd/baha footprint human presenter comments/help only (and its existing test if a string is asserted). Not the consent guard (236/227), not app_broker/237, not operatorauth (231), not 242 catalog, not .github/scripts.

UNBLOCKT: C-mapping (app_footprint_presenter.go) via #1777 auf develop 68b26bd7 GEMERGT. Owner hoppte #1773 additiv auf head 3ec2eba9 base 68b26bd; exact run 45036009904 laeuft (selected docker+podman native+runtime heavy gates). Review + merge bei terminal green. Kein content-aenderung (presenter-docs only).
