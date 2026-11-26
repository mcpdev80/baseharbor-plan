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
prs: ["mcpdev80/baseharbor#1872", "mcpdev80/baseharbor#1871"]
sources: []
blocker: "BASE ACT DISPOSED by w255 (#1871 comment 7202869676, owner-confirmed): 10 catalog rows land as SEPARATE develop-side catalog-only write-set within existing 0428-359/#136 baseline family (row-before-candidate per #1865 precedent; Trusted Plan reads base catalog, candidate rows cannot self-authorize). Lane w347-0428-344-baseline executes under family assignment against real candidate paths (internal/apierror/pagination*.go, pagination_contract_test.go files, internal/machinehttp/source_transfer.go, docs/spec+docs/de/spec/runtime-list-pagination-v1.md). #1871 stays blocked + catalog-free until baseline act lands AND owner requalifies its exact head. No new card, no merge"
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261128-hunt48-runtime-pagination-contract · 0428 hunt H-V48: runtime API list endpoints have no pagination contract #task #release/v0-4-28 #status/blocked #view/blocked #kind/task
    <!-- generated:card -->
    **Owner:** "" (lane w343 released after END BLOCKED-BASE-CATALOG; re-dispatch after base act lands)  
    **PR:** [baseharbor#1872](https://github.com/mcpdev80/baseharbor/pull/1872), [baseharbor#1871](https://github.com/mcpdev80/baseharbor/pull/1871)  
    **Blocker:** BASE ACT DISPOSED by w255 (\#1871 comment 7202869676, owner-confirmed): 10 catalog rows land as SEPARATE develop-side catalog-only write-set within existing 0428-359/\#136 baseline family (row-before-candidate per \#1865 precedent; Trusted Pl…  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** "" (lane w343 released after END BLOCKED-BASE-CATALOG; re-dispatch after base act lands)  
**Priority:** not set  
**PRs:** [baseharbor#1872](https://github.com/mcpdev80/baseharbor/pull/1872), [baseharbor#1871](https://github.com/mcpdev80/baseharbor/pull/1871)  
**Source:** 
<!-- /generated:links -->

## Owner decision — 2026-11-25

Before v1.0, BaseHarbor may make breaking API-contract changes; no migration or backward-compatibility shim is required. Define an explicit bounded pagination contract for runtime list endpoints and update the specification, EN/DE documentation, and focused contract tests in the same change.