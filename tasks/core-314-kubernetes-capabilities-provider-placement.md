---
id: core-314
type: feature
release: v0.8.x
version: v0.8.1
parent: v0.8.x
owner: ""
depends_on: [core-313]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#314"]
source_updated: "2026-10-15T16:52:54Z"
labels: [kind/feature, area/providers, area/kubernetes]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-314 · Kubernetes: add capabilities and provider placement #task #release/v0-8-x #status/planned

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.8.x](../releases/v0.8.x.md) (v0.8.1)  
**Depends on:** [core-313](core-313-kubernetes-complete-app-lifecycle.md)  
**Required by:** [core-315](core-315-kubernetes-backup-disaster-recovery.md), [core-316](core-316-kubernetes-observability-diagnostics-evidence.md), [core-317](core-317-kubernetes-updates-migration-recovery.md), [core-319](core-319-kubernetes-production-hardening-conformance.md), [core-320](core-320-acceptance-complete-kubernetes-support.md)  
**Owner:** unassigned  
**PRs:** none  
**Source:** [baseharbor#314](https://github.com/mcpdev80/baseharbor/issues/314)
<!-- /generated:links -->

## Goal

Make every existing BaseHarbor capability that is applicable to Kubernetes work through the same portable capability/provider model.

This release is about **semantic capability parity**, not installing every possible product into Kubernetes.

## Scope

Carried over from the source with minimal editing (headings demoted, checkboxes turned into plain bullets).

### Required provider placement

For each applicable capability, preserve the generic placement model:

```text
application
shared
external
```

with optional sharing boundary for shared providers.

Runtime topology must not leak into portable application intent.

### Capability coverage

Review the complete current BaseHarbor capability catalog and classify every capability as:

- supported on Kubernetes;
- supported through external/shared provider only;
- not applicable to Kubernetes;
- intentionally deferred with a documented reason.

Applicable existing capability families include, where currently part of BaseHarbor:

- SQL;
- cache;
- object storage;
- secrets;
- metrics;
- logs;
- traces/OTLP;
- HTTP exposure;
- other already-shipped core capabilities.

Do not pull optional post-v0.5 ecosystem capabilities into this release merely to expand scope.

### Binding parity

For each supported capability validate:

```text
request
 -> provider resolution
 -> placement
 -> provision/reference
 -> secure binding
 -> observe
 -> verify
 -> drift/repair
 -> destroy
```

### Namespace-only / platform ownership

Shared or external providers may live outside the application namespace.

BaseHarbor must:

- consume them through explicit provider/binding contracts;
- respect cross-namespace/platform authorization boundaries;
- never require ownership of provider namespaces;
- never assume cluster-admin;
- preserve logical application-owned resources even when backing infrastructure is shared.

### No provider leakage

Portable intent remains product-neutral.

Examples such as CloudNativePG, managed SQL, MinIO-compatible S3, OpenBao, Prometheus or vendor services remain provider realizations, not application contract terms.

### Delivery-provider placement consistency

The canonical placement semantics:

```text
application
shared
external
```

also apply to Delivery Providers.

This does not merge provider responsibilities: Capability Providers and Delivery Providers remain distinct provider families, but they use consistent placement/ownership semantics.

An Argo CD, Flux or other GitOps implementation must not create a new product-specific placement model.

## Acceptance

- Every existing applicable core capability has an explicit Kubernetes support classification.
- Supported capabilities preserve application/shared/external placement semantics.
- Secure binding behavior is equivalent at the BaseHarbor semantic level.
- Shared/external providers do not require cluster-admin or foreign namespace ownership.
- Provider-specific implementation details stay outside portable intent.
- Unsupported/deferred capability paths are explicit rather than silently degraded.
- CLI/JSON/MCP report the same provider/binding state.
- Documentation follows `docs/DEVELOPMENT_GUIDELINES.md`.

## Required checks

- Economical validation per `docs/DEVELOPMENT_GUIDELINES.md`. The [standard pre-release gate](../releases/v0.5.x.md#standard-pre-release-gate) applies to this patch release.

## Dependencies and file ownership

- Depends on core-313.

## Handoff

- Not started (future release).
