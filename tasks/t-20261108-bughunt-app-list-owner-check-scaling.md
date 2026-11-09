---
id: t-20261108-bughunt-app-list-owner-check-scaling
card_number: "0427-178"
card_short_title: "App list scales with every rec"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: none
kanban_status: closed
kanban_lane: closed
kanban_summary: "batch or cache owner verification so list cost is not linear per-record re-verification through the engine, while fail-closed…"
kanban_title: 0427-178 · App list scales with every rec
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1508, mcpdev80/baseharbor#1509, mcpdev80/baseharbor#1511]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp4.md", "https://github.com/mcpdev80/baseharbor/commit/8a2912c62"]
superseded_by: t-20261108-bughunt-0427-test-bootstrap-leak
---
- [x] t-20261108-bughunt-app-list-owner-check-scaling · Bug Hunt v0.4.27: App list scales with every record #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** none · **Priority:** normal  
    **PR:** [baseharbor#1508](https://github.com/mcpdev80/baseharbor/pull/1508), [baseharbor#1509](https://github.com/mcpdev80/baseharbor/pull/1509), [baseharbor#1511](https://github.com/mcpdev80/baseharbor/pull/1511)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/vm-bughunt/hp4.md), [proof 2](https://github.com/mcpdev80/baseharbor/commit/8a2912c62)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** none  
**Priority:** normal  
**PRs:** [baseharbor#1508](https://github.com/mcpdev80/baseharbor/pull/1508), [baseharbor#1509](https://github.com/mcpdev80/baseharbor/pull/1509), [baseharbor#1511](https://github.com/mcpdev80/baseharbor/pull/1511)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
 batch or cache owner verification so list cost is not linear per-record re-verification through the engine, while fail-closed semantics of card 174 stay intact; benchmark-style regression (bounded engine calls for N records) in CI-covered group.

## Problem (source evidence in the dossier)
BF-08 (damm): app list performs O(n) owner verification — every added record slows every list. Acceptance: batch or cache owner verification so list cost is not linear per-record re-verification through the engine, while fail-closed semantics of card 174 stay intact; benchmark-style regression (bounded engine calls for N records) in CI-covered group.

## Dependencies and file ownership
None blocking. Write-set: internal/deployment list path.
