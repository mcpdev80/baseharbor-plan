---
id: t-20261102-ci-backend-env-identity
type: task
areas: []
release: v0.4.x
version: ""
parent: ""
owner: "boardup (ci)"
kanban_status: closed
kanban_title: "fix(application): shared backend environment identity is canonical (owner-dir), not caller-drift"
priority: ""
depends_on: []
repos: ["mcpdev80/baseharbor"]
prs: ["mcpdev80/baseharbor#1271"]
sources: []
blocker: ""
resolution: "accepted"
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1271/merge@640846e1"]
---

- [x] t-20261102-ci-backend-env-identity · fix(application): shared backend environment identity is canonical (owner-dir), not caller-drift #task #release/v0-4-x #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** boardup (ci)  
    **PR:** [baseharbor#1271](https://github.com/mcpdev80/baseharbor/pull/1271)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1271/merge@640846e1)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.x](../releases/v0.4.x.md)  
**Depends on:** none  
**Owner:** boardup (ci)  
**Priority:** not set  
**PRs:** [baseharbor#1271](https://github.com/mcpdev80/baseharbor/pull/1271)  
**Source:** 
<!-- /generated:links -->

## Goal

Make shared backend environment identity canonical (owner-dir) instead of caller-drift, ensuring consistent environment lookup in the application layer.

## Scope

- In scope: canonical backend environment identity.
- Out of scope: caller-side environment management.

## Acceptance

- Backend environment identity resolves from owner-dir canonically.
- PR merged to develop; CI green.
- Merge-SHA: 640846e1d9d8df2b52c726a21cf5ad06206c51d6

## Required checks

- CI green on develop.
