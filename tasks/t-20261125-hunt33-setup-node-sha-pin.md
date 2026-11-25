---
id: t-20261125-hunt33-setup-node-sha-pin
card_number: "0428-297"
card_short_title: "hunt33-setup-node-sha-pin"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: closed
kanban_lane: closed
kanban_summary: ""
kanban_title: 0428-297 · hunt33-setup-node-sha-pin
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: superseded
superseded_by: t-20261125-hunt33-action-pins-audit
evidence: ["https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/pre-release.yml#L1503-L1503","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/pre-release.yml#L1720-L1720","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/pre-release.yml#L1937-L1937","https://github.com/mcpdev80/baseharbor-plan/blob/main/tasks/t-20261125-hunt33-action-pins-audit.md"]
---

- [x] t-20261125-hunt33-setup-node-sha-pin · 0428 hunt H-V33: hunt33-setup-node-sha-pin #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/pre-release.yml#L1503-L1503), [proof 2](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/pre-release.yml#L1720-L1720), [proof 3](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/pre-release.yml#L1937-L1937), [proof 4](https://github.com/mcpdev80/baseharbor-plan/blob/main/tasks/t-20261125-hunt33-action-pins-audit.md)  
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

### Disposition: SUPERSEDED by 0428-298

The three mutable setup-node references are a subset of the broader external-action pinning audit in 0428-298. Keep one task for the complete inventory and the required immutable-ref updates; do not implement a parallel pinning change for these same workflow lines.

### Evidence

- First setup-node@v6 reference: https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/pre-release.yml#L1503-L1503
- Second setup-node@v6 reference: https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/pre-release.yml#L1720-L1720
- Third setup-node@v6 reference: https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/.github/workflows/pre-release.yml#L1937-L1937
- Successor task: https://github.com/mcpdev80/baseharbor-plan/blob/main/tasks/t-20261125-hunt33-action-pins-audit.md
