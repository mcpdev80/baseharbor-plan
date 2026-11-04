---
id: t-20261102-ci-baha-test-gate-bind
type: task
areas: []
release: v0.4.x
version: ""
parent: ""
owner: "boardup (ci)"
kanban_lane: closed
kanban_summary: Bind cmd/baha/test.go files to the existing cli-gofmt gate so baha test files receive the same formatting enforcement.
kanban_status: closed
kanban_title: "ci(pr-gate-plan): bind cmd/baha/*_test.go to existing cli-gofmt gate"
priority: ""
depends_on: []
repos: ["mcpdev80/baseharbor"]
prs: ["mcpdev80/baseharbor#1276"]
sources: []
blocker: ""
resolution: "accepted"
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1276/merge@55db9035"]
---

- [x] t-20261102-ci-baha-test-gate-bind · ci(pr-gate-plan): bind cmd/baha/*_test.go to existing cli-gofmt gate #task #release/v0-4-x #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** boardup (ci)  
    **PR:** [baseharbor#1276](https://github.com/mcpdev80/baseharbor/pull/1276)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1276/merge@55db9035)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.x](../releases/v0.4.x.md)  
**Depends on:** none  
**Owner:** boardup (ci)  
**Priority:** not set  
**PRs:** [baseharbor#1276](https://github.com/mcpdev80/baseharbor/pull/1276)  
**Source:** 
<!-- /generated:links -->

## Goal

Bind `cmd/baha/*_test.go` files to the existing cli-gofmt gate so baha test files receive the same formatting enforcement.

## Scope

- In scope: gate binding for cmd/baha/*_test.go files.
- Out of scope: other test files, non-cli tests.

## Acceptance

- cli-gofmt gate covers cmd/baha/*_test.go.
- PR merged to develop; CI green.
- Merge-SHA: 55db9035535779d2e761a9ede82dba548578ce93

## Required checks

- CI green on develop.
