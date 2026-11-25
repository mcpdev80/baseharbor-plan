---
id: t-20261128-hunt48-unify-runtime-error-envelope
card_number: "0428-343"
card_short_title: "canonical runtime errors"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Use one intentional runtime HTTP error contract across the runtime-resource, application-runtime, and application-secret APIs.…"
kanban_title: 0428-343 · canonical runtime errors
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/runtimeresourceapi/handler.go#L260-L280","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/apierror/error.go#L24-L66","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/applicationruntimeapi/handler.go#L250-L275","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/applicationsecretapi/handler.go#L160-L180","https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-27/bughunt-hv48-api-surface/hunt-1.md"]
---

- [ ] t-20261128-hunt48-unify-runtime-error-envelope · 0428 hunt H-V48: unify runtime HTTP error envelope (runtimeresourceapi writeProblem vs apierror.Error) #task #release/v0-4-28 #status/planned #view/ready #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/runtimeresourceapi/handler.go#L260-L280), [proof 2](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/apierror/error.go#L24-L66), [proof 3](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/applicationruntimeapi/handler.go#L250-L275), [proof 4](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/applicationsecretapi/handler.go#L160-L180), [proof 5](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-27/bughunt-hv48-api-surface/hunt-1.md)  
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

Before v1.0, BaseHarbor may make breaking API-contract changes; no migration or backward-compatibility shim is required. If implementation unifies the error envelopes, define one intentional canonical shape and update the specification, EN/DE documentation, and focused contract tests in the same change.

## Goal

Use one intentional runtime HTTP error contract across the runtime-resource, application-runtime, and application-secret APIs. The current resource API writes an RFC-7807-style object while the other APIs serialize the stable `apierror.Error` `{code,message}` envelope.

## Scope

- In scope: runtime-resource error serialization, shared contract/specification, EN/DE API docs, and focused contract tests for representative validation, authorization, not-found, and internal failures.
- Out of scope: changing successful response DTOs, weakening HTTP authorization, or adding a migration/backward-compatibility shim.

## Acceptance

- All listed runtime HTTP APIs return the chosen canonical JSON fields and preserve their appropriate HTTP status codes.
- Error details do not expose wrapped causes or secret material; tests cover serialization and representative status/code pairs.
- The runtime API specification and EN/DE docs describe the same shape; existing affected contract tests are updated in the same implementation.
- Intentional breaking changes are permitted before v1.0; no compatibility shim or migration is required.
