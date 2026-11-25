---
id: t-20261128-hunt48-workstation-bootstrap-contract
card_number: "0428-341"
card_short_title: "document HTTP routes"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: Complete the existing machine/operator HTTP contract for two live route families that are registered in code but not specified…
kanban_title: 0428-341 · document HTTP routes
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/controlplaneruntime/server_run.go#L332-L359","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/workstationenrollment/http/production_handler.go#L88-L142","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/machinehttp/handler.go#L116-L121","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/machinehttp/source_transfer.go#L48-L130","https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-27/bughunt-hv48-api-surface/hunt-1.md"]
---

- [ ] t-20261128-hunt48-workstation-bootstrap-contract · 0428 hunt H-V48: workstation bootstrap endpoint registered but undocumented as a discrete contract #task #release/v0-4-28 #status/planned #view/ready #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/controlplaneruntime/server_run.go#L332-L359), [proof 2](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/workstationenrollment/http/production_handler.go#L88-L142), [proof 3](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/machinehttp/handler.go#L116-L121), [proof 4](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/machinehttp/source_transfer.go#L48-L130), [proof 5](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-27/bughunt-hv48-api-surface/hunt-1.md)  
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

## Goal

Complete the existing machine/operator HTTP contract for two live route families that are registered in code but not specified as complete wire contracts: operator-authenticated workstation bootstrap and authenticated machine source transfers.

## Scope

- In scope: `docs/spec/machine-http-v1.md`, the relevant operator API documentation in EN/DE, and focused schemas or contract fixtures alongside the existing terminal contracts.
- Document workstation bootstrap's operator/tenant authorization, one-use lifetime, request fields, response fields, status codes, and sensitive token handling.
- Document all four source-transfer routes, per-request authorization scope, bounded chunk upload, commit semantics, request/response fields, and error envelope.
- Out of scope: changing route behavior, weakening authentication, accepting anonymous bootstrap, or adding a new CI pipeline.

## Acceptance

- The contract documents the exact registered methods and paths from the current source and distinguishes operator-authenticated grant creation from the separate one-use enrollment exchange.
- EN and DE operator API docs agree on route names and security boundary; machine-http-v1 includes the source-transfer request/response shapes.
- Examples contain no usable bootstrap token, nonce, certificate, or other credential.
- Existing contract/documentation checks cover changed artifacts; no runtime behavior changes are introduced.

## Related finding

Consolidates H-V48 BF-48-1 (workstation bootstrap contract) and BF-48-7 (source-transfer contract). The former is behind the authenticated operator mux; the public one-use boundary is workstation enrollment, not bootstrap.
