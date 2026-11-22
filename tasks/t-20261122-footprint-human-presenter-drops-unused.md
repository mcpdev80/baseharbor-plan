---
id: t-20261122-footprint-human-presenter-drops-unused
card_number: "0428-245"
card_short_title: "footprint Unused gap"
type: bug
areas: [cli, testing]
release: v0.4.28
version: ""
parent: v0.4.28
owner: 0847d100
kanban_status: active
kanban_lane: active
kanban_summary: ""
kanban_title: 0428-245 · footprint Unused gap
priority: normal
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261122-footprint-human-presenter-drops-unused · Human footprint presenter drops the Unused field present in JSON contract #task #release/v0-4-28 #status/active #view/active #area/cli #area/testing #kind/bug
    <!-- generated:card -->
    **Owner:** 0847d100 · **Priority:** normal  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** 0847d100  
**Priority:** normal  
**PRs:** none  
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
