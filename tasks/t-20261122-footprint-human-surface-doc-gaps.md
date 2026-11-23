---
id: t-20261122-footprint-human-surface-doc-gaps
card_number: "0428-246"
card_short_title: "footprint human doc gaps"
type: maintenance
areas: [cli, documentation]
release: v0.4.28
version: ""
parent: v0.4.28
owner: 0847d100 (finalhop 7880a8f6 laeuft) / Coordinator
kanban_status: review
kanban_lane: review
kanban_summary: ""
kanban_title: 0428-246 · footprint human doc gaps
priority: normal
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1773, mcpdev80/baseharbor#1783]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261122-footprint-human-surface-doc-gaps · Document that the human footprint surface is a curated subset and explain the two divergences vs the JSON/MCP contract #task #release/v0-4-28 #status/review #view/review #area/cli #area/documentation #kind/maintenance
    <!-- generated:card -->
    **Owner:** 0847d100 (finalhop 7880a8f6 laeuft) / Coordinator · **Priority:** normal  
    **PR:** [baseharbor#1773](https://github.com/mcpdev80/baseharbor/pull/1773), [baseharbor#1783](https://github.com/mcpdev80/baseharbor/pull/1783)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** 0847d100 (finalhop 7880a8f6 laeuft) / Coordinator  
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

#1773/#1762 = downstream von shared gate #1783(parity)+#1770(pin). #1762 in queue hinter fixture (NICHT unabhaengig, owner-korrektur).

#1773 statuskorrektur (owner): Karte von blocked -> wait. #1770 + #1783 sind GEMERGT, daher KEIN owner-decision mehr noetig. #1773 ist OPEN/BEHIND auf develop 78f75c90 und editiert pr-gate-coverage.json SELBST NICHT -> additive hop uebernimmt develops katalog (keine -144 regression). ffe fuehrt hop+exact-head-pruefung aus. Nur noch auf gruenen exact-head wartend. develop 78f75c90.

abhaengigkeit korrigiert (owner 23:5x): #1773 wartet NICHT nur auf eigenen gruenen exact-head, sondern auf #1753-content (consent/commission-admission von 'baha app footprint show -o json' im managed-workload-set des data-capabilities targets). Der consent-digest ist ok; command-not-in-managed-workload-set ist das admission-defect von 0428-227. Lane arbeitet nicht um.

scope-clean (files==nur presenter); cd9cc-run green aber stale; final-hop auf 7880a8f6 + exact run laeuft, review danach.
