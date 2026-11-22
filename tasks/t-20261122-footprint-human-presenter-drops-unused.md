---
id: t-20261122-footprint-human-presenter-drops-unused
card_number: "0428-245"
card_short_title: "footprint Unused gap"
type: bug
areas: [cli, testing]
release: v0.4.28
version: ""
parent: v0.4.28
owner: owner (0847d100 fix + owner-patch) / coord
kanban_status: closed
kanban_lane: closed
kanban_summary: ""
kanban_title: 0428-245 · footprint Unused gap
priority: normal
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1772]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/commit/62784eff"]
---

- [x] t-20261122-footprint-human-presenter-drops-unused · Human footprint presenter drops the Unused field present in JSON contract #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/cli #area/testing #kind/bug
    <!-- generated:card -->
    **Owner:** owner (0847d100 fix + owner-patch) / coord · **Priority:** normal  
    **PR:** [baseharbor#1772](https://github.com/mcpdev80/baseharbor/pull/1772)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/commit/62784eff)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** owner (0847d100 fix + owner-patch) / coord  
**Priority:** normal  
**PRs:** [baseharbor#1772](https://github.com/mcpdev80/baseharbor/pull/1772)  
**Source:** 
<!-- /generated:links -->

## Found by bug-hunt H-V22 (0847d100) on develop 64eab13e

Befund B3: the human-readable footprint presenter omits the `Unused` field that the JSON/MCP footprint contract reports, so the two
output surfaces disagree for the same footprint. Recipe lives in evidence/r28-welle5-2026-11-22/footprint-desk round-1.

## Acceptance

1. Make the human presenter render the `Unused` field (or explicitly mark N/A) consistently with the JSON/MCP contract for the same data.
2. Regression asserting human and JSON footprint surfaces agree on the Unused field; native/CI picks it up per existing gate mapping.

## Boundaries

cmd/baha footprint presenter (human path) + its test only. NOT the consent guard (0428-236/227), NOT app_broker/237, NOT .github/scripts catalog (0428-242).

Kandidat #1772 head ef11a301 run 45025176987 GREEN aber NICHT vollstndig: acceptance-luecke (owner-befund) = renderAppFootprint kehrt fuer Details VOR der per-instance Unused-schleife zurck, default human mode zeigt nur die Zahl, nicht die Unused-IDs. Karte bleibt ACTIVE (nicht review). OWNER patcht den branch selbst (per-instance rows vor den early-return + regression im default mode), ein schreiber pro branch; 0847d100 stand-down. Nach owner-push: exact-hosted neu + dann review/merge. Display-only, kein contract/model/.github.

Owner-patch auf head 232ded2 (per-instance Unused-rows vor Details early-return, default human mode zeigt Unused-IDs wie JSON/MCP). 0847d100 stand-down (ein writer). EXAKTER run 45025731965 completed SUCCESS -> review/merge geroutet an fecbada9.

GEMERGED (squash) bei develop 62784eff, exact run 45025731965 SUCCESS. Human footprint presenter rendert Unused pro instanz VOR dem Details early-return, damit default mode die Unused-IDs wie JSON/MCP zeigt. Fund->Karte (H-V22 B3) erfuellt. Display-only, kein contract/model/.github.
