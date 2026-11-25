---
id: t-20261128-hunt48-runtime-pagination-contract
card_number: "0428-344"
card_short_title: "bounded runtime lists"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Define and implement one explicit bounded-pagination contract for runtime API list responses, so clients can detect the page…"
kanban_title: 0428-344 · bounded runtime lists
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/applicationsecretapi/handler.go#L48-L82","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/applicationruntimeapi/handler.go#L110-L140","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/spec/runtime-api/v1/openapi.yaml","https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-27/bughunt-hv48-api-surface/hunt-1.md"]
---

- [ ] t-20261128-hunt48-runtime-pagination-contract · 0428 hunt H-V48: runtime API list endpoints have no pagination contract #task #release/v0-4-28 #status/planned #view/ready #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/applicationsecretapi/handler.go#L48-L82), [proof 2](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/applicationruntimeapi/handler.go#L110-L140), [proof 3](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/spec/runtime-api/v1/openapi.yaml), [proof 4](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-27/bughunt-hv48-api-surface/hunt-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Owner decision — 2026-11-25

Before v1.0, BaseHarbor may make breaking API-contract changes; no migration or backward-compatibility shim is required. Define an explicit bounded pagination contract for runtime list endpoints and update the specification, EN/DE documentation, and focused contract tests in the same change.

## Goal

Define and implement one explicit bounded-pagination contract for runtime API list responses, so clients can detect the page limit and continue without silent truncation.

## Scope

- In scope: enumerate current list-shaped runtime responses, choose a bounded request/response shape and maximum page size, implement it consistently for dynamic collections, then update OpenAPI/specification, EN/DE docs, and focused contract tests.
- Out of scope: pagination for non-list endpoints, unrelated response DTO normalization, and compatibility shims or data migrations.

## Acceptance

- Every dynamic list endpoint has a documented maximum and deterministic continuation contract; responses cannot silently truncate beyond the bound.
- The same query parameters, response metadata, validation rules, and maximum are used across applicable runtime list endpoints.
- OpenAPI, runtime API specification, EN/DE docs, and contract tests agree on defaults, limits, ordering, and continuation behavior.
- Breaking API-contract changes are allowed before v1.0; no migration or backward-compatibility shim is required.
