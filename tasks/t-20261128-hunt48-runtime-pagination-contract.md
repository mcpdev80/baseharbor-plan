---
id: t-20261128-hunt48-runtime-pagination-contract
card_number: "0428-344"
card_short_title: "runtime list pagination"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: "w356-0428-288-1870hop"
kanban_status: active
kanban_lane: active
kanban_summary: ""
kanban_title: 0428-344 · runtime list pagination
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1871"]
sources: []
blocker: "parked pending w255 scope decision (a in-card route fix / b own tracking / c refute) for TestCapabilitiesPaginationContract 404; head c21b4fde pushed, Go packages red only via that pre-existing gap; w356 holds worktree, no autonomous continuation"
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261128-hunt48-runtime-pagination-contract · 0428 hunt H-V48: runtime API list endpoints have no pagination contract #task #release/v0-4-28 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** w356-0428-288-1870hop  
    **PR:** [baseharbor#1871](https://github.com/mcpdev80/baseharbor/pull/1871)  
    **Blocker:** parked pending w255 scope decision (a in-card route fix / b own tracking / c refute) for TestCapabilitiesPaginationContract 404; head c21b4fde pushed, Go packages red only via that pre-existing gap; w356 holds worktree, no autonomous conti…  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w356-0428-288-1870hop  
**Priority:** not set  
**PRs:** [baseharbor#1871](https://github.com/mcpdev80/baseharbor/pull/1871)  
**Source:** 
<!-- /generated:links -->

## Owner decision — 2026-11-25

Before v1.0, BaseHarbor may make breaking API-contract changes; no migration or backward-compatibility shim is required. Define an explicit bounded pagination contract for runtime list endpoints and update the specification, EN/DE documentation, and focused contract tests in the same change.