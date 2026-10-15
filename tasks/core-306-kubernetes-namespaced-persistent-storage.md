---
id: core-306
areas: [kubernetes]
type: feature
release: v0.7.x
version: v0.7.3
parent: v0.7.x
owner: ""
depends_on: [core-102, core-304]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#306"]
source_updated: "2026-10-15T16:53:32Z"
labels: [kind/feature, area/kubernetes, area/storage]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-306 · Kubernetes: implement namespaced persistent storage #task #release/v0-7-x #status/planned #view/waiting #area/kubernetes #kind/feature
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Waiting for prerequisites**  
    **Needs:** [core-102](core-102-kubernetes-namespace-scoped-runtime-foundation.md), [core-304](core-304-kubernetes-security-identity-networking.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.7.x](../releases/v0.7.x.md) (v0.7.3)  
**Depends on:** [core-102](core-102-kubernetes-namespace-scoped-runtime-foundation.md), [core-304](core-304-kubernetes-security-identity-networking.md)  
**Required by:** [core-307](core-307-kubernetes-stateful-workloads.md), [core-308](core-308-kubernetes-availability-guarantees.md), [core-309](core-309-tests-kubernetes-restricted-permissions.md), [core-310](core-310-acceptance-compose-to-kubernetes-portability.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#306](https://github.com/mcpdev80/baseharbor/issues/306)
<!-- /generated:links -->

## Goal

Realize BaseHarbor persistent-storage intent using namespaced PVC lifecycle while treating StorageClass/PV infrastructure as platform-owned.

## Scope

Carried over from the source with minimal editing (headings demoted, checkboxes turned into plain bullets).

### Architecture

```text
portable storage requirement
        ↓
deployment/runtime storage policy
        ↓
PVC in application namespace
        ↓
platform provisioner / StorageClass / PV
```

### Namespace-only model

BaseHarbor may create/manage PVCs in its namespace.

It must not require permission to create/manage:

- StorageClasses;
- PersistentVolumes;
- CSI drivers.

StorageClass names and cloud disk products remain deployment/runtime policy.

If no explicit storage policy is supplied, BaseHarbor may rely on platform defaults where safe.

Do not require `list storageclasses` simply to perform a valid default PVC request.

### Lifecycle

Support:

- plan/preflight;
- PVC create/update where safe;
- binding observation;
- mount realization;
- semantic storage verification;
- drift;
- retention/delete behavior;
- restore re-binding;
- ownership-safe destroy.

PVC existence alone is not verification.

### Admission/quota awareness

ResourceQuota, LimitRange and admission policy may reject or mutate workloads/PVCs.

BaseHarbor must surface those as platform-policy outcomes rather than attempting to override them.

## Acceptance

- Namespaced PVC lifecycle works without StorageClass/PV admin permissions.
- Cluster storage infrastructure remains platform-owned.
- Default platform storage can be used without unnecessary cluster-wide discovery.
- Storage bind/mount is semantically verified.
- Retention/delete semantics are explicit and ownership-safe.
- Quota/admission failures are actionable.
- CLI/JSON/MCP expose the same storage state.
- Validation follows `docs/DEVELOPMENT_GUIDELINES.md`.

## Required checks

- Economical validation per `docs/DEVELOPMENT_GUIDELINES.md`. The [standard pre-release gate](../releases/v0.5.x.md#standard-pre-release-gate) applies to this patch release.

## Dependencies and file ownership

- Depends on core-102, core-304.

## Handoff

- Not started (future release).
