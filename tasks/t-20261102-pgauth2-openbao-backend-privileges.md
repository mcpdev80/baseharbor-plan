---
id: t-20261102-pgauth2-openbao-backend-privileges
type: task
areas: []
release: v0.4.x
version: ""
parent: ""
owner: ornith (pgauth2)
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1269"]
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261102-pgauth2-openbao-backend-privileges · OpenBao: grant PG backend role legal connect on postgres/template1 #task #release/v0-4-x #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** ornith (pgauth2)  
    **PR:** [baseharbor#1269](https://github.com/mcpdev80/baseharbor/pull/1269)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.x](../releases/v0.4.x.md)  
**Depends on:** none  
**Owner:** ornith (pgauth2)  
**Priority:** not set  
**PRs:** [baseharbor#1269](https://github.com/mcpdev80/baseharbor/pull/1269)  
**Source:** 
<!-- /generated:links -->

## Goal

OpenBao's PostgreSQL storage backend must start legally under the MCP/hosted lifecycle sweep instead of failing with `FATAL: permission denied for database "postgres" / "template1" / "openbao"`.

## Scope

- In scope: `internal/runtime/openbao_runtime_prepare.go` (`openbao-init.sh`), plus a source-level regression test in `internal/runtime/openbao_runtime_prepare_test.go`.
- Out of scope: control-plane superuser wiring, Spilo/pg_hba, CI workflows, app-role isolation.

## Acceptance

- The `openbao` backend role (non-superuser) can connect to its storage database and to the postgres/template1 databases it probes at startup.
- The role remains a restricted login — no Superuser bypass.
- App-role isolation preserved: application roles cannot reach postgres/template1/other consumers.
- `go build ./...`, `go vet ./internal/runtime/`, and runtime/openbao/application test suites green.
- PR on base develop; CI green; before/after reproduction in evidence.

## Required checks

- `go test ./internal/runtime/ ./internal/openbao/ ./internal/application/`
- Local postgres:18 reproduction (before/after) in evidence.

## Dependencies and file ownership

- Owned files or areas: `internal/runtime/openbao_runtime_prepare.go`, `internal/runtime/openbao_runtime_prepare_test.go`.
- Read-only references: `internal/application/shared_backends_runtime.go`, `internal/application/shared_core_sql.go` (isolation guards).
