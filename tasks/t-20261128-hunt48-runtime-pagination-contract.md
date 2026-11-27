---
id: t-20261128-hunt48-runtime-pagination-contract
card_number: "0428-344"
card_short_title: "runtime list pagination"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: ""
kanban_title: 0428-344 · runtime list pagination
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1872", "mcpdev80/baseharbor#1871", "mcpdev80/baseharbor-plan#156"]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/2026-11-27/planpr-backlog-disposition.md", "https://github.com/mcpdev80/baseharbor/pull/1871", "https://github.com/mcpdev80/baseharbor/pull/1872"]
---

- [ ] t-20261128-hunt48-runtime-pagination-contract · 0428 hunt H-V48: runtime API list endpoints have no pagination contract #task #release/v0-4-28 #status/planned #view/ready #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **PR:** [baseharbor#1872](https://github.com/mcpdev80/baseharbor/pull/1872), [baseharbor#1871](https://github.com/mcpdev80/baseharbor/pull/1871), [baseharbor-plan#156](https://github.com/mcpdev80/baseharbor-plan/pull/156)  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/2026-11-27/planpr-backlog-disposition.md), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1871), [proof 3](https://github.com/mcpdev80/baseharbor/pull/1872)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** [baseharbor#1872](https://github.com/mcpdev80/baseharbor/pull/1872), [baseharbor#1871](https://github.com/mcpdev80/baseharbor/pull/1871), [baseharbor-plan#156](https://github.com/mcpdev80/baseharbor-plan/pull/156)  
**Source:** 
<!-- /generated:links -->

## Owner decision — 2026-11-25

Before v1.0, BaseHarbor may make breaking API-contract changes; no migration or backward-compatibility shim is required. Define an explicit bounded pagination contract for runtime list endpoints and update the specification, EN/DE documentation, and focused contract tests in the same change.

## Claim-gap receipt (2026-11-27)

- Plan PR #156 remains OPEN at head 607e98e8aebd72b6f1d3cce8b19b2cdc51d3769d; it contributes the baseline Akte file only. The task’s prior blocked reason referred to an earlier failed #1872 run; #1871 and #1872 are now merged, but this card is not being marked accepted from those merges alone. This receipt does not close #156.
