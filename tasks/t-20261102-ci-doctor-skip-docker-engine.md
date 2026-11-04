---
id: t-20261102-ci-doctor-skip-docker-engine
type: task
areas: []
release: v0.4.x
version: ""
parent: ""
owner: "boardup (ci)"
kanban_status: closed
kanban_title: "fix(doctor): skip Docker-engine check for non-Docker runtime providers"
priority: ""
depends_on: []
repos: ["mcpdev80/baseharbor"]
prs: ["mcpdev80/baseharbor#1274"]
sources: []
blocker: ""
resolution: "accepted"
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1274/merge@9f61c162"]
---

- [x] t-20261102-ci-doctor-skip-docker-engine · fix(doctor): skip Docker-engine check for non-Docker runtime providers #task #release/v0-4-x #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** boardup (ci)  
    **PR:** [baseharbor#1274](https://github.com/mcpdev80/baseharbor/pull/1274)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1274/merge@9f61c162)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.x](../releases/v0.4.x.md)  
**Depends on:** none  
**Owner:** boardup (ci)  
**Priority:** not set  
**PRs:** [baseharbor#1274](https://github.com/mcpdev80/baseharbor/pull/1274)  
**Source:** 
<!-- /generated:links -->

## Goal

Skip Docker-engine checks in the doctor for non-Docker runtime providers, preventing false-positive failures when the Docker engine is not available.

## Scope

- In scope: Docker-engine check skip logic for non-Docker providers.
- Out of scope: Docker-engine check for Docker-target providers.

## Acceptance

- Doctor skips Docker-engine checks when the runtime is non-Docker.
- PR merged to develop; CI green.
- Merge-SHA: 9f61c16210865c6f8c151e96ab659ecf216f7a7f

## Required checks

- CI green on develop.
