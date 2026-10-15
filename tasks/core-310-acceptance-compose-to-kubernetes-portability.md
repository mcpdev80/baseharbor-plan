---
id: core-310
areas: [acceptance]
type: acceptance
release: v0.7.x
version: v0.7.7
parent: v0.7.x
owner: ""
depends_on: [core-102, core-304, core-305, core-306, core-307, core-308, core-309]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#310"]
source_updated: "2026-10-15T16:53:08Z"
labels: [kind/acceptance, area/runtime, area/kubernetes, area/compatibility]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-310 · Acceptance: verify Compose-to-Kubernetes portability #task #release/v0-7-x #status/planned #view/waiting #area/acceptance #kind/acceptance
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Waiting for prerequisites**  
    **Needs:** [core-102](core-102-kubernetes-namespace-scoped-runtime-foundation.md), [core-304](core-304-kubernetes-security-identity-networking.md), [core-305](core-305-kubernetes-http-access-gateway-api.md), [core-306](core-306-kubernetes-namespaced-persistent-storage.md), [core-307](core-307-kubernetes-stateful-workloads.md), [core-308](core-308-kubernetes-availability-guarantees.md), [core-309](core-309-tests-kubernetes-restricted-permissions.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.7.x](../releases/v0.7.x.md) (v0.7.7)  
**Depends on:** [core-102](core-102-kubernetes-namespace-scoped-runtime-foundation.md), [core-304](core-304-kubernetes-security-identity-networking.md), [core-305](core-305-kubernetes-http-access-gateway-api.md), [core-306](core-306-kubernetes-namespaced-persistent-storage.md), [core-307](core-307-kubernetes-stateful-workloads.md), [core-308](core-308-kubernetes-availability-guarantees.md), [core-309](core-309-tests-kubernetes-restricted-permissions.md)  
**Required by:** [core-313](core-313-kubernetes-complete-app-lifecycle.md), [core-325](core-325-delivery-delegated-deployment-gitops.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#310](https://github.com/mcpdev80/baseharbor/issues/310)
<!-- /generated:links -->

## Goal

Close v0.7 by proving that the same portable BaseHarbor application contract runs on Compose and Kubernetes, including a Kubernetes deployment where BaseHarbor has only namespaced permissions.

## Scope

Carried over from the source with minimal editing (headings demoted, checkboxes turned into plain bullets).

### Primary portability test

```text
same repository
same portable baseharbor.yaml
        ↓
Compose
        ↓
verified supported lifecycle

same repository
same portable baseharbor.yaml
        ↓
Kubernetes
        ↓
pre-provisioned namespace
namespace-only credentials
        ↓
verified supported lifecycle
```

Deployment/operator configuration may differ. Portable application intent must not.

### Kubernetes proof constraints

The namespace-only run must not require:

- namespace creation;
- cluster-admin;
- ClusterRole/ClusterRoleBinding creation;
- Node listing;
- StorageClass/GatewayClass mutation;
- CRD installation;
- unrelated namespace access.

Platform-owned dependencies may be pre-provisioned and referenced through deployment/operator state.

### Required lifecycle

Exercise the supported v0.7 surface:

- plan;
- preflight;
- up/apply;
- status;
- doctor;
- drift;
- repair;
- update where supported;
- destroy.

Include where applicable:

- secure bindings;
- network isolation;
- HTTP exposure;
- persistent storage;
- stateful support;
- availability realization.

### Agent proof

A generic coding agent must operate the supported Kubernetes lifecycle through BaseHarbor MCP/JSON without raw `kubectl` fallback for normal BaseHarbor operations.

### Boundary proof

Confirm portable intent contains no Kubernetes-specific:

- namespace;
- Service/Deployment/StatefulSet;
- PVC/StorageClass;
- NetworkPolicy;
- GatewayClass/HTTPRoute;
- ServiceAccount name;
- replica/topology/PDB fields.

### Enterprise target safety proof

The namespace-only portability run must additionally prove:

- the target namespace may contain unrelated non-BaseHarbor resources;
- BaseHarbor networking and destroy operations leave those resources untouched;
- platform-owned namespace labels/policies are not mutated;
- a private image can be used through a pre-provisioned/runtime-owned pull credential path without putting credentials into portable intent;
- Target mismatch is detected before destructive mutation;
- normal operation does not depend on optional broad list/watch/event access.

### Direct Kubernetes implementation constraints

The portability proof uses **direct delivery** as the first Kubernetes realization, but the implementation must remain an adapter over the shared BaseHarbor lifecycle core.

Rules:

- use the official Kubernetes Go API/client libraries for normal mutation, observation and verification;
- do not make `kubectl`, Helm or shell execution part of the normal BaseHarbor lifecycle implementation;
- keep Kubernetes API objects behind the Kubernetes runtime/provider boundary;
- preserve the provider-neutral application contract and runtime-neutral lifecycle/result models;
- direct delivery must implement the same `plan -> preflight -> apply -> verify` and reconciliation invariants as every other BaseHarbor surface;
- do not place CLI-specific lifecycle business logic in the Kubernetes provider;
- the shared core must remain reusable by a future Kubernetes/OpenShift Operator control surface without reimplementing lifecycle semantics.

##### Permanent portability gate

The Compose-to-Kubernetes portability proof is not a one-time release exercise. Add repository/CI coverage that continuously rejects Kubernetes-specific fields leaking into portable application intent or shared provider-neutral contracts.

The gate must cover at least:

- portable contract/schema boundaries;
- runtime/capability/delivery provider-axis separation;
- ownership and target-scope safety;
- same logical application identity across Compose and Kubernetes.

##### Initial Kubernetes support window

Start with a deliberately small, documented Kubernetes API/resource surface and expand only when lifecycle semantics require it.

The first production-capable slice should prefer standard GA Kubernetes APIs and initially focus on the smallest resource set needed by the accepted lifecycle, such as Deployment, Service, ConfigMap, Secret, PVC and ServiceAccount. Additional workload/security primitives are added incrementally behind the same runtime boundary.

### Delivery handoff

This issue proves Compose-to-Kubernetes portability using the direct Kubernetes delivery implementation.

It must not freeze direct Kubernetes API mutation as the only reconciliation model.

The next v0.7 step (#325) proves the independent Delivery Provider boundary with delegated/GitOps reconciliation while keeping the same portable application intent and Kubernetes Runtime semantics.

### Existing target scope semantics

The standard rules for existing platform-named target scopes apply (see [v0.5.x](../releases/v0.5.x.md#rules), "Existing target scope semantics"): the runtime interprets the scope as the existing namespace, BaseHarbor never renames/recreates/deletes a platform-owned namespace, ownership is tracked below namespace level, and destroy removes only BaseHarbor-owned resources.

## Acceptance

- Normal direct Kubernetes lifecycle uses native Go Kubernetes API clients, not kubectl/Helm/shell fallbacks.
- Compose-to-Kubernetes portability boundaries are enforced continuously by repository/CI tests.
- The initial supported Kubernetes API/resource window is explicitly documented and intentionally minimal.
- The shared lifecycle core remains usable by a future Operator control surface without duplicated lifecycle business logic.
- An arbitrary pre-existing target scope such as `r2-4b-dt-test` can be selected without changing portable application intent.
- Destroy never deletes a platform/external target scope itself; it removes only BaseHarbor-owned resources within it.
- Same portable application contract works on Compose and Kubernetes.
- Kubernetes proof includes namespace-only credentials.
- Platform-owned resources remain deployment/runtime state.
- Supported lifecycle completes without cluster-admin.
- Missing optional cluster visibility does not break unrelated lifecycle operations.
- CLI/JSON/MCP expose the same semantic truth.
- Generic agent works without raw `kubectl` fallback.
- Remaining gaps are explicitly deferred to v0.8 Kubernetes Complete.
- Exact-head acceptance is captured economically.

## Required checks

- Economical validation per `docs/DEVELOPMENT_GUIDELINES.md`. The [standard pre-release gate](../releases/v0.5.x.md#standard-pre-release-gate) applies to this patch release.

## Dependencies and file ownership

- Depends on core-102, core-304, core-305, core-306, core-307, core-308, core-309.

## Handoff

- Not started (future release).
