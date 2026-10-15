---
id: core-325
areas: [delivery]
type: architecture
release: v0.7.x
version: v0.7.8
parent: v0.7.x
owner: ""
depends_on: [core-310]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#325"]
source_updated: "2026-10-15T16:52:11Z"
labels: [kind/architecture, area/kubernetes, area/delivery]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-325 · Delivery: support delegated deployment and GitOps #task #release/v0-7-x #status/planned #view/waiting #area/delivery #kind/architecture
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Waiting for prerequisites**  
    **Needs:** [core-310](core-310-acceptance-compose-to-kubernetes-portability.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.7.x](../releases/v0.7.x.md) (v0.7.8)  
**Depends on:** [core-310](core-310-acceptance-compose-to-kubernetes-portability.md)  
**Required by:** [core-313](core-313-kubernetes-complete-app-lifecycle.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#325](https://github.com/mcpdev80/baseharbor/issues/325)
<!-- /generated:links -->

## Goal

Add a runtime-neutral **Delivery Provider** axis so BaseHarbor can support direct mutation and delegated/GitOps reconciliation without making Argo CD, Flux, Git or Kubernetes part of portable application intent.

> **BaseHarbor owns the contract. Runtime, capability and delivery providers choose the mechanism.**
>
> **The developer operates BaseHarbor; BaseHarbor operates or delegates to the underlying tools.**
>
> **Contracts, not tools.**

## Scope

Carried over from the source with minimal editing (headings demoted, checkboxes turned into plain bullets).

### Architecture

Delivery is independent from runtime and capability providers:

```text
                         BaseHarbor Core
                               |
             +-----------------+-----------------+
             |                 |                 |
             v                 v                 v
       Runtime Provider  Capability Provider  Delivery Provider
             |                 |                 |
          Compose           SQL/S3/...        direct
        Kubernetes                          delegated/GitOps
         OpenShift
```

Hard rule:

```text
runtime != capability != delivery
```

The initial Kubernetes implementation may use direct Kubernetes API delivery, but this must not become the only supported reconciliation model.

### Delivery contract

The generic delivery contract must cover only semantics BaseHarbor actually needs, such as:

- delivery mode/capabilities;
- desired-revision identity;
- plan/preflight;
- publish/apply request;
- synchronization/reconciliation observation;
- typed conflict/out-of-sync/denied/unavailable states;
- ownership;
- rollback/recovery capability declaration where supported;
- semantic handoff to BaseHarbor verification/evidence.

Do not leak Argo CD Application, Flux Kustomization, Helm values, Kubernetes resources or Git-provider-specific fields into portable application intent.

### Direct delivery

```text
BaseHarbor
    |
    v
Runtime API
```

BaseHarbor owns mutation/reconciliation for the relevant resource set.

Compose remains the complete first-class reference runtime and normal direct delivery path.

### Delegated / GitOps delivery

```text
BaseHarbor
    |
    v
desired runtime realization
    |
    v
Delivery Provider
    |
    v
Git / GitOps reconciler
    |
    v
Runtime
```

The delivery provider owns publication/integration with the external reconciler.

BaseHarbor continues to own portable semantics, policy, provider selection, placement, lifecycle intent, observation, semantic verification and evidence.

### Single reconciliation owner

For one managed resource set there must be exactly one active mutation/reconciliation owner.

BaseHarbor and an external GitOps controller must never continuously mutate the same owned fields.

- direct: BaseHarbor owns mutation/reconciliation;
- delegated: Delivery Provider / external reconciler owns runtime mutation, BaseHarbor observes and verifies.

Ambiguous or conflicting reconciliation ownership fails closed.

### Placement / ownership

Delivery providers use the same canonical placement semantics as other provider families:

```text
application
shared
external
```

Examples for an Argo CD implementation:

- application: dedicated BaseHarbor-owned Argo CD instance for one app/environment;
- shared: explicitly shared BaseHarbor/platform-managed instance;
- external: existing customer/platform Argo CD, whose lifecycle BaseHarbor must not take over.

The semantics are shared; provider responsibilities remain separate.

### Open provider ecosystem

Argo CD is the first intended reference implementation, not the contract.

The architecture must remain compatible with:

- Argo CD;
- Flux;
- another GitOps reconciler;
- another future delivery implementation.

A Delivery Provider should be independently implementable without BaseHarbor Core changes and may be distributed through the same open provider ecosystem principles used elsewhere: versioned contracts, gRPC/Protocol Buffers where a process boundary is required, OCI distribution, conformance, signatures/provenance.

Providers may internally use mature OSS, standard APIs, controllers, operators, CRDs or SDKs. BaseHarbor Core must not accumulate product-specific integration code.

### Developer experience

Normal users and generic agents operate BaseHarbor:

```text
baha up
baha status
baha doctor
baha update
baha backup
baha restore
baha destroy
```

They must not be required to use `argocd`, `flux`, `kubectl`, Helm or provider-native CLIs for normal BaseHarbor operations.

Native tool UIs/CLIs remain available to platform engineers for drill-down and administration.

### Argo CD reference provider

Prove delegated delivery with one real provider:

- provider-neutral BaseHarbor contract;
- Argo CD adapter/provider outside BaseHarbor Core;
- desired revision publication;
- sync/health observation;
- no double reconciliation;
- BaseHarbor semantic verification after Argo reconciliation;
- Argo CD UI remains fully usable;
- application/shared/external placement behavior;
- no Argo-specific portable application fields.

### Compose protection

This issue must not make Compose depend on Kubernetes, GitOps, Argo CD, Flux, CRDs or cloud tooling.

```text
runtime: compose
delivery: direct
```

remains a complete first-class path.

The delivery abstraction must also not forbid a future non-Kubernetes delegated delivery implementation if a real use case appears.

### Operator boundary

A Kubernetes/OpenShift Operator and a Delivery Provider are different architectural concepts.

- an **Operator** is a possible Kubernetes-native control surface / continuous reconciliation adapter over the shared BaseHarbor core;
- a **Delivery Provider** defines who owns final runtime mutation/reconciliation for a managed resource set;
- the Kubernetes/OpenShift Runtime Provider defines runtime-specific realization and observation.

A future Operator may therefore operate with either delivery model:

```text
Operator -> shared BaseHarbor core -> direct Delivery -> Kubernetes/OpenShift API
```

or:

```text
Operator -> shared BaseHarbor core -> delegated Delivery -> Argo CD / Flux -> Kubernetes/OpenShift
```

The single-reconciliation-owner rule remains authoritative in both cases.

Operator presence must not create a third competing mutation owner, and Operator-specific CRD fields must not leak into portable application intent or the generic Delivery Provider contract.

## Acceptance

- Operator/control-surface concerns remain separate from Runtime and Delivery Provider semantics.
- A future Operator can use direct or delegated delivery without changing portable application intent.
- Operator presence never violates the exactly-one-reconciliation-owner invariant.
- Runtime, Capability and Delivery Provider are documented as separate axes.
- Direct and delegated delivery have stable runtime-neutral semantics.
- Exactly one reconciliation owner exists for each managed resource set.
- Delivery providers support application/shared/external placement semantics.
- Argo CD is implemented/proven as a reference provider, not embedded as a core contract.
- A second implementation such as Flux would not require portable-contract changes.
- Normal users/agents use BaseHarbor surfaces, not underlying tool CLIs.
- Argo CD UI/native platform tooling remains usable for expert drill-down.
- Compose remains complete and first-class with no GitOps dependency.
- Product-specific integration logic does not enter BaseHarbor Core.
- Documentation and conformance follow DEVELOPMENT_GUIDELINES.md.

## Required checks

- Economical validation per `docs/DEVELOPMENT_GUIDELINES.md`. The [standard pre-release gate](../releases/v0.5.x.md#standard-pre-release-gate) applies to this patch release.

## Dependencies and file ownership

- Depends on core-310.

## Handoff

- Not started (future release).
