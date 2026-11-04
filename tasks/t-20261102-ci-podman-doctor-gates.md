---
id: t-20261102-ci-podman-doctor-gates
type: task
areas: []
release: v0.4.x
version: ""
parent: ""
owner: "boardup (ci)"
kanban_lane: closed
kanban_summary: Bind podman-doctor CLI paths to lifecycle gates so that podman-target doctor checks are enforced through the existing gate-map…
kanban_status: closed
kanban_title: "ci(gate-map): bind podman-doctor CLI paths to lifecycle gates"
priority: ""
depends_on: []
repos: ["mcpdev80/baseharbor"]
prs: ["mcpdev80/baseharbor#1268"]
sources: []
blocker: ""
resolution: "accepted"
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1268/merge@dbced1af"]
---

- [x] t-20261102-ci-podman-doctor-gates · ci(gate-map): bind podman-doctor CLI paths to lifecycle gates #task #release/v0-4-x #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** boardup (ci)  
    **PR:** [baseharbor#1268](https://github.com/mcpdev80/baseharbor/pull/1268)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1268/merge@dbced1af)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.x](../releases/v0.4.x.md)  
**Depends on:** none  
**Owner:** boardup (ci)  
**Priority:** not set  
**PRs:** [baseharbor#1268](https://github.com/mcpdev80/baseharbor/pull/1268)  
**Source:** 
<!-- /generated:links -->

## Goal

Bind podman-doctor CLI paths to lifecycle gates so that podman-target doctor checks are enforced through the existing gate-map infrastructure.

## Scope

- In scope: gate-map path binding for `podman_doctor_checks.go` CLI paths.
- Out of scope: other doctor checks, docker-engine validation.

## Acceptance

- Gate-map entries for podman-doctor paths are present and enforced.
- PR merged to develop; CI green.
- Merge-SHA: dbced1af86fed12ca5ef2dbceed3d51f85fe05af

## Required checks

- Gate-map validation.
- CI green on develop.
