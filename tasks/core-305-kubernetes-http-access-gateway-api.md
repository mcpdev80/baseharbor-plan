---
id: core-305
areas: [kubernetes]
type: feature
release: v0.7.x
version: v0.7.2
parent: v0.7.x
owner: ""
depends_on: [core-102, core-304]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#305"]
source_updated: "2026-10-15T16:53:38Z"
labels: [kind/feature, area/kubernetes, area/networking]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-305 · Kubernetes: provide HTTP access through Gateway API #task #release/v0-7-x #status/planned #view/waiting #area/kubernetes #kind/feature
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Waiting for prerequisites**  
    **Needs:** [core-102](core-102-kubernetes-namespace-scoped-runtime-foundation.md), [core-304](core-304-kubernetes-security-identity-networking.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.7.x](../releases/v0.7.x.md) (v0.7.2)  
**Depends on:** [core-102](core-102-kubernetes-namespace-scoped-runtime-foundation.md), [core-304](core-304-kubernetes-security-identity-networking.md)  
**Required by:** [core-309](core-309-tests-kubernetes-restricted-permissions.md), [core-310](core-310-acceptance-compose-to-kubernetes-portability.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#305](https://github.com/mcpdev80/baseharbor/issues/305)
<!-- /generated:links -->

## Goal

Realize portable BaseHarbor HTTP exposure on Kubernetes while allowing namespace-only BaseHarbor users to consume a platform-owned Gateway.

## Scope

Carried over from the source with minimal editing (headings demoted, checkboxes turned into plain bullets).

### Architecture

```text
Platform
  -> GatewayClass
  -> shared Gateway

Application namespace
  -> BaseHarbor-owned HTTPRoute
  -> Service
```

Gateway/GatewayClass are platform-owned by default.

BaseHarbor in namespace-only mode must not need permission to create or mutate them.

### Route realization

Map `exposure.http/v1` to:

- HTTPRoute;
- Service backend;
- portable hostname/path/TLS intent already defined by BaseHarbor.

No vendor/controller annotations in portable application intent.

### Cross-namespace rules

Cross-namespace references are explicit trust relationships.

Where Gateway API requires target-side authorization such as ReferenceGrant:

- BaseHarbor must not create authorization objects in namespaces it does not own;
- platform/provider owner supplies the grant;
- BaseHarbor verifies whether the reference is accepted.

### Verification

Do not treat HTTPRoute creation as success.

Verify relevant status conditions and actual application reachability where feasible.

If platform Gateway policy rejects the route, produce an actionable BaseHarbor error rather than trying to mutate platform-owned Gateway resources.

### Namespace-only requirements

BaseHarbor must operate with only namespaced rights to its own route/service resources.

Cluster-wide GatewayClass listing must not be mandatory if the deployment config identifies the platform Gateway directly.

## Acceptance

- Namespace-only BaseHarbor can bind to a pre-provisioned shared Gateway.
- Gateway/GatewayClass remain platform-owned.
- Cross-namespace authorization is explicit and owner-controlled.
- HTTPRoute acceptance/resolution is verified.
- No vendor-specific exposure details leak into portable intent.
- Missing platform permission blocks only exposure.
- CLI/JSON/MCP expose the same exposure state.
- Validation follows `docs/DEVELOPMENT_GUIDELINES.md`.

## Required checks

- Economical validation per `docs/DEVELOPMENT_GUIDELINES.md`. The [standard pre-release gate](../releases/v0.5.x.md#standard-pre-release-gate) applies to this patch release.

## Dependencies and file ownership

- Depends on core-102, core-304.

## Handoff

- Not started (future release).
