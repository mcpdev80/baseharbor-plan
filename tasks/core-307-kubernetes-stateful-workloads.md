---
id: core-307
type: feature
release: v0.7.x
version: v0.7.4
parent: v0.7.x
owner: ""
depends_on: [core-102, core-306]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#307"]
source_updated: "2026-10-15T16:53:26Z"
labels: [kind/feature, area/runtime, area/kubernetes, area/storage]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-307 · Kubernetes: support stateful workloads #task #release/v0-7-x #status/planned #view/waiting
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Needs:** [core-102](core-102-kubernetes-namespace-scoped-runtime-foundation.md), [core-306](core-306-kubernetes-namespaced-persistent-storage.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.7.x](../releases/v0.7.x.md) (v0.7.4)  
**Depends on:** [core-102](core-102-kubernetes-namespace-scoped-runtime-foundation.md), [core-306](core-306-kubernetes-namespaced-persistent-storage.md)  
**Required by:** [core-308](core-308-kubernetes-availability-guarantees.md), [core-309](core-309-tests-kubernetes-restricted-permissions.md), [core-310](core-310-acceptance-compose-to-kubernetes-portability.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#307](https://github.com/mcpdev80/baseharbor/issues/307)
<!-- /generated:links -->

## Goal

Add namespaced Kubernetes stateful workload primitives where a real runtime/capability-provider path requires them, without moving database/product semantics into BaseHarbor Core.

## Scope

Carried over from the source with minimal editing (headings demoted, checkboxes turned into plain bullets).

### Scope

Support, where genuinely needed:

- StatefulSet;
- stable runtime identity;
- namespaced PVC association;
- readiness/recovery observation;
- safe rollout/update behavior;
- ownership/drift/repair;
- lifecycle-safe destroy.

### Namespace-only

Stateful support must work with namespaced permissions when required platform resources are pre-provisioned.

No cluster-admin dependency may be introduced simply because a workload is stateful.

### Capability-provider boundary

Runtime primitives and capability semantics remain separate.

BaseHarbor Runtime must not implement database replication, leader election or product-specific HA.

Valid future providers may use:

- plain StatefulSet;
- external managed service;
- provider/operator CRD;
- another implementation.

Provider-specific CRDs remain provider/runtime implementation details, not portable app fields.

### Finalizers / deletion

Deletion success requires observed completion/retention according to policy.

BaseHarbor must not remove foreign finalizers just to force destroy success.

## Acceptance

- Stateful runtime support remains namespaced where possible.
- Capability-provider semantics remain separate from runtime primitives.
- Stateful identity/storage survive expected reconcile/update flows.
- Foreign finalizers/ownership are respected.
- No product-specific HA logic enters BaseHarbor Core.
- CLI/JSON/MCP expose the same semantic state.
- Validation follows `docs/DEVELOPMENT_GUIDELINES.md`.

## Required checks

- Economical validation per `docs/DEVELOPMENT_GUIDELINES.md`. The [standard pre-release gate](../releases/v0.5.x.md#standard-pre-release-gate) applies to this patch release.

## Dependencies and file ownership

- Depends on core-102, core-306.

## Handoff

- Not started (future release).
