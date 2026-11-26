---
id: t-20261128-hunt48-runtime-pagination-contract
card_number: "0428-344"
card_short_title: "runtime list pagination"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: "" (lane w343 released after END BLOCKED-BASE-CATALOG; re-dispatch after base act lands)
kanban_status: blocked
kanban_lane: blocked
kanban_summary: ""
kanban_title: 0428-344 · runtime list pagination
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1871"]
sources: []
blocker: "exact heads 45884566859/45884719597 FAILURE: pr-gate-plan.py source_unowned (uncataloged pagination sources, Trusted Plan reads catalog from trusted develop -> candidate-side fix impossible). REQUIRED BASE ACT (owner routing, outside lane write-set): component rows on DEVELOP scripts/pr-gate-coverage.json for internal/apierror/pagination.go+pagination_test.go, machine/applicationsecretapi/list_handler.go, machine/applicationruntimeapi/capabilities_handler.go, machinehttp/sourcetransfer.go+store.go, domain/machine/navigation.go, query/machine/machinereadmodels/list.go + both spec markdown paths (NOT data.capabilities example). After base act: lane absorbs develop under lane identity, close+reopen #1871 for fresh exact-head pair" #1871 held ready unmerged"
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261128-hunt48-runtime-pagination-contract · 0428 hunt H-V48: runtime API list endpoints have no pagination contract #task #release/v0-4-28 #status/blocked #view/blocked #kind/task
    <!-- generated:card -->
    **Owner:** "" (lane w343 released after END BLOCKED-BASE-CATALOG; re-dispatch after base act lands)  
    **PR:** [baseharbor#1871](https://github.com/mcpdev80/baseharbor/pull/1871)  
    **Blocker:** exact heads 45884566859/45884719597 FAILURE: pr-gate-plan.py source\_unowned (uncataloged pagination sources, Trusted Plan reads catalog from trusted develop -\> candidate-side fix impossible). REQUIRED BASE ACT (owner routing, outside lane…  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** "" (lane w343 released after END BLOCKED-BASE-CATALOG; re-dispatch after base act lands)  
**Priority:** not set  
**PRs:** [baseharbor#1871](https://github.com/mcpdev80/baseharbor/pull/1871)  
**Source:** 
<!-- /generated:links -->

## Owner decision — 2026-11-25

Before v1.0, BaseHarbor may make breaking API-contract changes; no migration or backward-compatibility shim is required. Define an explicit bounded pagination contract for runtime list endpoints and update the specification, EN/DE documentation, and focused contract tests in the same change.