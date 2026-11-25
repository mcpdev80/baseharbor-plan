---
id: t-20261128-hunt48-metrics-endpoint-docs
card_number: "0428-342"
card_short_title: "document operator metrics"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Document the GET /metrics endpoint in the operator/Core runtime reference, including when it is registered, its…"
kanban_title: 0428-342 · document operator metrics
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/controlplaneruntime/server_run.go#L132-L142","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/runtimeobservability/observer.go#L180-L218","https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-27/bughunt-hv48-api-surface/hunt-1.md"]
---

- [ ] t-20261128-hunt48-metrics-endpoint-docs · 0428 hunt H-V48: metrics endpoint registered but undocumented in any spec #task #release/v0-4-28 #status/planned #view/ready #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/controlplaneruntime/server_run.go#L132-L142), [proof 2](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/runtimeobservability/observer.go#L180-L218), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-27/bughunt-hv48-api-surface/hunt-1.md)  
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

Document the `GET /metrics` endpoint in the operator/Core runtime reference, including when it is registered, its authentication/exposure boundary, and representative BaseHarbor series.

## Scope

- In scope: the existing runtime/control-plane observability reference that owns `/healthz` and `/readyz`, with matching EN/DE content where that reference is bilingual.
- Out of scope: adding metrics, changing endpoint registration or authentication, and documenting archived Console surfaces as current product behavior.

## Acceptance

- Documentation states that `/metrics` is present only when the bound runtime observability component is enabled and describes the actual middleware/exposure path.
- Documented sample names come from current emitted metrics; no inferred series are presented as guaranteed.
- EN/DE docs agree and the existing documentation audit covers the updated pages.
