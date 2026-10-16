---
id: core-320
areas: [acceptance]
type: acceptance
release: v0.8.x
version: v0.8.7
parent: v0.8.x
owner: ""
depends_on: [core-313, core-314, core-315, core-316, core-317, core-318, core-319]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#320"]
source_updated: "2026-10-15T16:52:17Z"
labels: [kind/acceptance, area/runtime, area/kubernetes, area/compatibility]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-320 · Acceptance: verify complete Kubernetes support #task #release/v0-8-x #status/planned #view/waiting #board/planned #area/acceptance #kind/acceptance
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Waiting for prerequisites**  
    **Needs:** [core-313](core-313-kubernetes-complete-app-lifecycle.md), [core-314](core-314-kubernetes-capabilities-provider-placement.md), [core-315](core-315-kubernetes-backup-disaster-recovery.md), [core-316](core-316-kubernetes-observability-diagnostics-evidence.md), [core-317](core-317-kubernetes-updates-migration-recovery.md), [core-318](core-318-kubernetes-cli-agent-developer-parity.md), [core-319](core-319-kubernetes-production-hardening-conformance.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.8.x](../releases/v0.8.x.md) (v0.8.7)  
**Depends on:** [core-313](core-313-kubernetes-complete-app-lifecycle.md), [core-314](core-314-kubernetes-capabilities-provider-placement.md), [core-315](core-315-kubernetes-backup-disaster-recovery.md), [core-316](core-316-kubernetes-observability-diagnostics-evidence.md), [core-317](core-317-kubernetes-updates-migration-recovery.md), [core-318](core-318-kubernetes-cli-agent-developer-parity.md), [core-319](core-319-kubernetes-production-hardening-conformance.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#320](https://github.com/mcpdev80/baseharbor/issues/320)
<!-- /generated:links -->

## Goal

Close the Kubernetes roadmap phase and establish Kubernetes as a fully first-class BaseHarbor production runtime before OpenShift/Enterprise work begins.

This is an acceptance/release-closeout issue, not a new feature bucket.

## Scope

Carried over from the source with minimal editing (headings demoted, checkboxes turned into plain bullets).

### Definition of Kubernetes Complete

For everything already supported by the BaseHarbor core and applicable to Kubernetes:

```text
portable application intent
        ↓
deployment/operator state
        ↓
Kubernetes Runtime
        ↓
full supported lifecycle
        ↓
verified semantic result
```

No Kubernetes-specific rewrite of the portable application contract is required.

### End-to-end reference acceptance

Use at least one representative real application with meaningful capabilities and persistent state.

Run from a clean supported Kubernetes target:

```text
target/access preflight
 -> init/inspect
 -> plan
 -> up
 -> status/doctor
 -> capability bindings
 -> exposure
 -> observability
 -> availability
 -> backup
 -> destructive recovery test
 -> restore
 -> drift
 -> repair
 -> update
 -> verification
 -> destroy
```

Run the core acceptance in the namespace-only profile with a pre-provisioned platform-owned target scope.

### Runtime parity review

Inventory every existing BaseHarbor user-facing feature and classify it:

- works on Kubernetes;
- not applicable by design;
- explicitly belongs to a provider/platform outside the runtime;
- deferred only if the BaseHarbor core itself does not yet support it.

There must be no hidden "use kubectl for this BaseHarbor feature" gaps.

### Agent acceptance

A generic coding agent must complete the same supported lifecycle through BaseHarbor MCP/JSON.

No generic Kubernetes shell escape is required.

### Ownership/safety acceptance

Prove:

### Documentation / release

Before completion:

- reconcile architecture/application/runtime/provider/CLI/MCP documentation;
- document supported Kubernetes/API range;
- document namespace-only RBAC expectations;
- document platform prerequisites without turning them into app intent;
- produce human-friendly release notes;
- validate exact final head;
- ensure changelog/tag/release metadata agree.

### Explicitly not required for Kubernetes Complete

Unless independently part of the BaseHarbor core before this release:

- OpenShift-specific SCC/Route/OAuth/OLM behavior;
- air-gapped/disconnected enterprise distribution;
- human OIDC/JIT production-access platform;
- every optional ecosystem provider;
- a Kubernetes Operator;
- vendor/cloud-specific managed-service integrations.

Those belong to later tracks.

### Kubernetes Complete architecture freeze

"Kubernetes Complete" does not require shipping a Kubernetes Operator, but it **does require an Operator-compatible architecture**.

Before this phase is closed:

- the normal Kubernetes implementation uses native Go Kubernetes API clients rather than requiring kubectl/Helm/shell execution;
- the portable application contract remains free of Kubernetes-specific resource fields;
- Compose-to-Kubernetes portability boundaries are enforced by permanent CI/conformance tests;
- the supported Kubernetes API/version/resource window is explicitly documented and tested;
- Runtime, Capability and Delivery Provider responsibilities remain separate;
- lifecycle semantics remain in the shared BaseHarbor core so a later Kubernetes/OpenShift Operator can reuse them without reimplementation;
- direct and delegated/GitOps delivery both preserve semantic BaseHarbor verification;
- Argo/Flux synchronization or health never substitutes for BaseHarbor semantic verification;
- exactly one active mutation/reconciliation owner exists for each managed resource set.

A later Operator/CRD track is therefore an additional Kubernetes-native control surface and packaging/reconciliation option, not a prerequisite for first-class Kubernetes runtime support and not a new portable application contract.

### Delivery acceptance

Kubernetes Complete must prove both supported delivery models without changing portable application intent:

```text
Path A:
  Kubernetes Runtime
  + direct Delivery Provider

Path B:
  Kubernetes Runtime
  + delegated/GitOps Delivery Provider
  + Argo CD as the reference implementation
```

The delegated path must prove:


Argo CD is reference evidence, not a BaseHarbor contract dependency. A conforming Flux/other provider must remain architecturally possible.

## Acceptance

- platform-owned namespace survives destroy;
- unrelated shared-namespace resources remain untouched;
- shared/external providers retain correct ownership;
- secrets are not leaked;
- target mismatch fails closed;
- required guarantees are not falsely claimed;
- restore/update success is semantically verified.
- Kubernetes Complete has permanent portability/conformance gates preventing Kubernetes details from leaking into portable intent.
- Supported Kubernetes API/version/resource ranges are documented and exercised by acceptance.
- The shipped lifecycle core is demonstrably reusable by a future Operator without duplicated lifecycle semantics.
- Direct and delegated delivery both preserve the exactly-one-reconciliation-owner rule and BaseHarbor semantic verification.
- Full applicable BaseHarbor feature inventory has no unexplained Kubernetes gaps.
- Representative end-to-end lifecycle passes with namespace-only access.
- Capability/provider-placement parity is demonstrated.
- Backup/restore is verified end to end.
- Observability/diagnostics/evidence parity is demonstrated.
- Update/migration/recovery behavior is verified.
- Generic agent completes the supported lifecycle without raw Kubernetes fallback.
- Platform/foreign ownership and shared-namespace safety are proven.
- Same portable application intent remains valid across Compose and Kubernetes.
- Supported Kubernetes/API matrix passes.
- Canonical docs and human-friendly release notes are complete.
- Exact final implementation head is validated economically.
- Kubernetes can truthfully be documented as a first-class production runtime.
- normal lifecycle remains `baha`/JSON/MCP-first;
- Argo CD UI remains fully usable;
- BaseHarbor does not directly fight the external reconciler;
- semantic verification can fail even when GitOps reports synchronized;
- provider-specific GitOps fields remain outside portable application intent.

## Required checks

- Economical validation per `docs/DEVELOPMENT_GUIDELINES.md`. The [standard pre-release gate](../releases/v0.5.x.md#standard-pre-release-gate) applies to this patch release.

## Dependencies and file ownership

- Depends on core-313, core-314, core-315, core-316, core-317, core-318, core-319.

## Handoff

- Not started (future release).
