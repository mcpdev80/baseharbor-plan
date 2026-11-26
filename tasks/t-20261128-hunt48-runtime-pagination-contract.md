---
id: t-20261128-hunt48-runtime-pagination-contract
card_number: "0428-344"
card_short_title: "runtime list pagination"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: w343-0428-344-pagination (LIVE; awaiting Plan PR #155 trusted rows for the 11 uncatalogued pagination sources)
kanban_status: blocked
kanban_lane: blocked
kanban_summary: ""
kanban_title: 0428-344 · runtime list pagination
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1871"]
sources: []
blocker: "exact-head Hosted run 45888715532 = TERMINAL FAILURE: Trusted Plan reports 11 uncatalogued pagination sources (same trusted-develop bootstrap class as 0428-321/#1866). Acceptance of #1871 blocked until the same task/PR lands the required trusted rows AND a fresh exact-head run passes (owner directive 03:2xZ). Lane currently waits 240s on Plan PR #155. No new card, no merge."
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261128-hunt48-runtime-pagination-contract · 0428 hunt H-V48: runtime API list endpoints have no pagination contract #task #release/v0-4-28 #status/blocked #view/blocked #kind/task
    <!-- generated:card -->
    **Owner:** w343-0428-344-pagination (LIVE; awaiting Plan PR \#155 trusted rows for the 11 uncatalogued pagination sources)  
    **PR:** [baseharbor#1871](https://github.com/mcpdev80/baseharbor/pull/1871)  
    **Blocker:** exact-head Hosted run 45888715532 = TERMINAL FAILURE: Trusted Plan reports 11 uncatalogued pagination sources (same trusted-develop bootstrap class as 0428-321/\#1866). Acceptance of \#1871 blocked until the same task/PR lands the required t…  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w343-0428-344-pagination (LIVE; awaiting Plan PR #155 trusted rows for the 11 uncatalogued pagination sources)  
**Priority:** not set  
**PRs:** [baseharbor#1871](https://github.com/mcpdev80/baseharbor/pull/1871)  
**Source:** 
<!-- /generated:links -->

## Owner decision — 2026-11-25

Before v1.0, BaseHarbor may make breaking API-contract changes; no migration or backward-compatibility shim is required. Define an explicit bounded pagination contract for runtime list endpoints and update the specification, EN/DE documentation, and focused contract tests in the same change.