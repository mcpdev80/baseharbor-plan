---
id: core-315
areas: [kubernetes]
type: feature
release: v0.8.x
version: v0.8.2
parent: v0.8.x
owner: ""
depends_on: [core-313, core-314]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#315"]
source_updated: "2026-10-15T16:52:48Z"
labels: [kind/feature, area/recovery, area/kubernetes]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-315 · Kubernetes: verify backup and disaster recovery #task #release/v0-8-x #status/planned #view/waiting #area/kubernetes #kind/feature
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Waiting for prerequisites**  
    **Needs:** [core-313](core-313-kubernetes-complete-app-lifecycle.md), [core-314](core-314-kubernetes-capabilities-provider-placement.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.8.x](../releases/v0.8.x.md) (v0.8.2)  
**Depends on:** [core-313](core-313-kubernetes-complete-app-lifecycle.md), [core-314](core-314-kubernetes-capabilities-provider-placement.md)  
**Required by:** [core-317](core-317-kubernetes-updates-migration-recovery.md), [core-318](core-318-kubernetes-cli-agent-developer-parity.md), [core-319](core-319-kubernetes-production-hardening-conformance.md), [core-320](core-320-acceptance-complete-kubernetes-support.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#315](https://github.com/mcpdev80/baseharbor/issues/315)
<!-- /generated:links -->

## Goal

Bring BaseHarbor backup/restore semantics to Kubernetes with real recovery verification.

A snapshot/object existing is not a successful BaseHarbor backup or restore.

## Scope

Carried over from the source with minimal editing (headings demoted, checkboxes turned into plain bullets).

### Lifecycle

```text
plan backup
 -> preflight
 -> capture required state/data
 -> record ownership/compatibility metadata
 -> verify backup

restore
 -> preflight compatibility/target
 -> restore data/state
 -> rebind
 -> reconcile workload/provider state
 -> restart/recover where required
 -> semantic verification
```

### Scope

Apply the existing BaseHarbor backup/restore model to Kubernetes-owned state and supported capability providers.

Cover where applicable:

- application state required for reconstruction;
- persistent storage/provider data;
- binding metadata;
- provider/version compatibility metadata;
- target/runtime ownership metadata;
- retained platform-owned resources;
- restore into the same or another valid Kubernetes deployment target where supported.

### Provider boundary

Backup implementation belongs to the capability/provider that owns the data semantics.

The Kubernetes Runtime must not pretend that copying Kubernetes manifests is equivalent to database/object-storage backup.

Potential mechanisms such as CSI snapshots are runtime/provider mechanisms only when they satisfy the BaseHarbor backup contract.

### Namespace-only

Backup/restore must work with namespace-only rights where the selected provider/platform mechanism allows it.

If a platform snapshot API or provider requires additional rights, preflight reports only that feature as unavailable.

### Safety

- restore never overwrites foreign-owned resources silently;
- target mismatch fails closed;
- platform-owned namespaces/Gateways/StorageClasses are not captured as BaseHarbor-owned application state;
- secrets remain secret-safe;
- restore success requires post-restore semantic verification.

### Reuse mature recovery mechanisms

BaseHarbor owns backup/restore orchestration, compatibility, ownership and semantic verification, but should not reimplement mature runtime data-movement or snapshot mechanisms merely to keep the implementation BaseHarbor-specific.

A provider/runtime implementation may use mechanisms such as provider-native backup, CSI snapshots, Velero, VolSync or other conforming tools when they satisfy the BaseHarbor backup contract.

Those products remain implementation details. Backup success is still defined by BaseHarbor recovery semantics and real restore verification.

### PKI / issuer parity requirement

Kubernetes backup/restore and runtime parity MUST consume the same provider-neutral issuer/trust lifecycle established before v0.5.

Kubernetes/OpenShift deployments must not depend on PKI material stored on the machine running `baha`.

Target model:

```text
baha CLI
  ↓
Kubernetes/OpenShift runtime adapter
  ↓
issuer provider in/for the cluster
  ├─ OpenBao PKI
  ├─ cert-manager-compatible issuer
  ├─ platform-native issuer
  └─ external enterprise PKI adapter
```

Certificate issuance, renewal, revocation, rotation and trust distribution must be realizable fully inside the cluster/platform boundary. Portable application intent and workload-facing bindings remain identical to the Compose/OpenBao path.

## Acceptance

- Supported Kubernetes workloads/providers have real backup verification.
- Restore performs rebind/reconcile and semantic verification.
- Manifests/PVC existence alone are not accepted as backup/restore success.
- Provider-specific data backup remains provider-owned.
- Namespace-only operation remains possible where the chosen mechanism allows it.
- Foreign/platform ownership remains protected.
- CLI/JSON/MCP expose the same backup/restore state.
- Documentation follows `docs/DEVELOPMENT_GUIDELINES.md`.

## Required checks

- Economical validation per `docs/DEVELOPMENT_GUIDELINES.md`. The [standard pre-release gate](../releases/v0.5.x.md#standard-pre-release-gate) applies to this patch release.

## Dependencies and file ownership

- Depends on core-313, core-314.

## Handoff

- Not started (future release).
