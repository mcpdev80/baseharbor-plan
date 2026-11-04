---
id: t-20261102-ci-pgauth-openbao-privileges
type: task
areas: []
release: v0.4.x
version: ""
parent: ""
owner: "boardup (ci)"
kanban_status: closed
kanban_title: "fix(secrets): grant OpenBao postgres backend the right privileges"
priority: ""
depends_on: []
repos: ["mcpdev80/baseharbor"]
prs: ["mcpdev80/baseharbor#1269"]
sources: []
blocker: ""
resolution: "accepted"
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1269/merge@d4715f79"]
---

- [x] t-20261102-ci-pgauth-openbao-privileges · fix(secrets): grant OpenBao postgres backend the right privileges #task #release/v0-4-x #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** boardup (ci)  
    **PR:** [baseharbor#1269](https://github.com/mcpdev80/baseharbor/pull/1269)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1269/merge@d4715f79)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.x](../releases/v0.4.x.md)  
**Depends on:** none  
**Owner:** boardup (ci)  
**Priority:** not set  
**PRs:** [baseharbor#1269](https://github.com/mcpdev80/baseharbor/pull/1269)  
**Source:** 
<!-- /generated:links -->

## Goal

Grant OpenBao postgres backend the right privileges so it can connect to its storage database and postgres/template1 at startup.

## Scope

- In scope: privilege granting for OpenBao postgres backend.
- Out of scope: control-plane superuser wiring, Spilo/pg_hba.

## Acceptance

- OpenBao postgres backend can connect to postgres and template1 databases.
- PR merged to develop; CI green.
- Merge-SHA: d4715f798c500f33c1a2411a711f8c7055135a52

## Required checks

- CI green on develop.
