---
id: core-313
type: feature
release: v0.8.x
version: v0.8.0
parent: v0.8.x
owner: ""
depends_on: [core-310, core-325]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#313"]
source_updated: "2026-10-15T16:53:00Z"
labels: [kind/feature, area/runtime, area/kubernetes]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-313 · Kubernetes: implement the complete app lifecycle #task #release/v0-8-x #status/planned #view/waiting
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Needs:** [core-310](core-310-acceptance-compose-to-kubernetes-portability.md), [core-325](core-325-delivery-delegated-deployment-gitops.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.8.x](../releases/v0.8.x.md) (v0.8.0)  
**Depends on:** [core-310](core-310-acceptance-compose-to-kubernetes-portability.md), [core-325](core-325-delivery-delegated-deployment-gitops.md)  
**Required by:** [core-314](core-314-kubernetes-capabilities-provider-placement.md), [core-315](core-315-kubernetes-backup-disaster-recovery.md), [core-316](core-316-kubernetes-observability-diagnostics-evidence.md), [core-317](core-317-kubernetes-updates-migration-recovery.md), [core-318](core-318-kubernetes-cli-agent-developer-parity.md), [core-319](core-319-kubernetes-production-hardening-conformance.md), [core-320](core-320-acceptance-complete-kubernetes-support.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#313](https://github.com/mcpdev80/baseharbor/issues/313)
<!-- /generated:links -->

## Goal

Start the Kubernetes Complete phase by making the full BaseHarbor application lifecycle available on Kubernetes wherever the corresponding BaseHarbor lifecycle operation already exists.

v0.7 proves the Runtime Provider and Kubernetes primitives.

v0.8.0 starts closing the remaining product-level parity gap.

> **Kubernetes is now a first-class BaseHarbor runtime, not a special deployment mode.**

## Scope

Carried over from the source with minimal editing (headings demoted, checkboxes turned into plain bullets).

### Required lifecycle

For Kubernetes, support the same semantic application lifecycle as the BaseHarbor core where applicable:

```text
discover
inspect
init / adopt where supported
plan
preflight
apply / up
status
doctor
observe diagnostics
update
drift
repair
destroy
```

Later v0.8 releases complete backup/restore, capability breadth, observability and upgrade/recovery depth.

### Rules

- CLI/JSON/MCP use the same shared core/domain logic;
- no Kubernetes-only lifecycle vocabulary for the normal path;
- no raw `kubectl`/Helm/shell fallback for normal BaseHarbor operations;
- namespace-only remains the primary authorization profile;
- platform-owned target scopes remain protected;
- unsupported operations fail explicitly and narrowly;
- destructive operations preserve ownership/target-safety rules from v0.7.

### Init / adoption boundary

Where BaseHarbor supports initialization/adoption of an existing application/runtime state:

- do not claim ownership of foreign resources implicitly;
- distinguish discovered, adoptable and BaseHarbor-owned state;
- adoption must be explicit and preflighted;
- platform-owned namespace/Gateway/storage resources remain external/platform-owned.

### Developer experience

The same commands should remain meaningful across Compose and Kubernetes.

The user should not need a second Kubernetes-specific workflow just because the runtime changed.

### Operator-ready shared lifecycle boundary

Kubernetes lifecycle parity must be implemented in the shared BaseHarbor domain/lifecycle core, not in CLI handlers and not in a future Operator-specific implementation.

The architecture must support these control surfaces over the same semantics:

```text
baha CLI / JSON / MCP / HTTP API / future Operator
                    |
                    v
             shared lifecycle core
                    |
                    v
          Runtime + Delivery Providers
```

A future Kubernetes/OpenShift Operator is **not required for v0.8.0**, but this release must avoid architecture that would force lifecycle logic to be rewritten when one is added.

In particular:

- plan/preflight/apply/verify/status/doctor/drift/repair/update/destroy semantics live below presentation/control surfaces;
- lifecycle results and diagnostics remain typed and machine-readable;
- Kubernetes-native status/conditions may later map from the same shared result model;
- a future Operator must be able to reconcile through the same core rather than shelling out to `baha`;
- CRDs, if introduced later, are Kubernetes-facing adapters to BaseHarbor desired state, not a replacement portable application contract or a second domain authority.

### Delivery-mode lifecycle parity

Full lifecycle parity must work through the BaseHarbor lifecycle model regardless of who performs final runtime reconciliation.

After #325, Kubernetes lifecycle coverage includes:

- direct delivery through the Kubernetes Runtime;
- delegated delivery through a conforming Delivery Provider.

The user-facing lifecycle remains BaseHarbor-first in both cases. Delivery-provider-specific commands must not become required normal lifecycle steps.

## Acceptance

- Applicable Kubernetes lifecycle semantics live in reusable shared core services rather than CLI-specific code.
- Adding a future Kubernetes/OpenShift Operator would not require a second lifecycle implementation.
- Any future CRD can remain an adapter to the BaseHarbor core rather than becoming a competing application contract.
- Kubernetes supports the complete applicable application lifecycle listed above.
- Namespace-only credentials are sufficient for the normal lifecycle.
- Existing platform-owned target scopes remain protected.
- Init/adopt never silently steals ownership.
- Unsupported lifecycle operations are typed and actionable.
- CLI/JSON/MCP use the same underlying lifecycle behavior.
- No normal lifecycle requires raw kubectl/Helm/shell fallback.
- Documentation follows `docs/DEVELOPMENT_GUIDELINES.md`.

## Required checks

- Economical validation per `docs/DEVELOPMENT_GUIDELINES.md`. The [standard pre-release gate](../releases/v0.5.x.md#standard-pre-release-gate) applies to this patch release.

## Dependencies and file ownership

- Depends on core-310, core-325.

## Handoff

- Not started (future release).
