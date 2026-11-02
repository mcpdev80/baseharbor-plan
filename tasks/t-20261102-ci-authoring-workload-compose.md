---
id: t-20261102-ci-authoring-workload-compose
type: task
areas: []
release: v0.4.x
version: ""
parent: ""
owner: "boardup (ci)"
priority: ""
depends_on: []
repos: ["mcpdev80/baseharbor"]
prs: ["mcpdev80/baseharbor#1272"]
sources: []
blocker: ""
resolution: "accepted"
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1272/merge@9a93865a"]
---

- [x] t-20261102-ci-authoring-workload-compose · fix(authoring): Workload.Compose optional in MCP intent schema #task #release/v0-4-x #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** boardup (ci)  
    **PR:** [baseharbor#1272](https://github.com/mcpdev80/baseharbor/pull/1272)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1272/merge@9a93865a)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.x](../releases/v0.4.x.md)  
**Depends on:** none  
**Owner:** boardup (ci)  
**Priority:** not set  
**PRs:** [baseharbor#1272](https://github.com/mcpdev80/baseharbor/pull/1272)  
**Source:** 
<!-- /generated:links -->

## Goal

Make Workload.Compose optional in the MCP intent schema, relaxing a required field constraint that was too strict for some runtime configurations.

## Scope

- In scope: MCP intent schema Workload.Compose field optionality.
- Out of scope: other schema fields, runtime behavior changes.

## Acceptance

- Workload.Compose is optional in MCP intent schema.
- PR merged to develop; CI green.
- Merge-SHA: 9a93865a935624045e96a503da0a3a1c2f7d1559

## Required checks

- CI green on develop.
