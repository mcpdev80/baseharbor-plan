---
id: t-20261128-hunt48-source-transfers-contract
card_number: "0428-346"
card_short_title: "source-transfers routes doc"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: closed
kanban_lane: closed
kanban_summary: ""
kanban_title: 0428-346 · source-transfers routes doc
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: superseded
superseded_by: t-20261128-hunt48-workstation-bootstrap-contract
evidence: ["https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/machinehttp/handler.go#L116-L121","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/machinehttp/source_transfer.go#L48-L130","https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-27/bughunt-hv48-api-surface/hunt-1.md"]
---

- [x] t-20261128-hunt48-source-transfers-contract · 0428 hunt H-V48: source-transfer contract gap #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/machinehttp/handler.go#L116-L121), [proof 2](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/machinehttp/source_transfer.go#L48-L130), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-27/bughunt-hv48-api-surface/hunt-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** superseded  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Disposition

SUPERSEDED by [0428-341](t-20261128-hunt48-workstation-bootstrap-contract.md), which retains all source-transfer route, DTO, authorization, and contract-test requirements while coordinating the shared machine HTTP specification with the workstation-bootstrap contract.
