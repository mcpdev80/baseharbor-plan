---
id: core-309
areas: [testing]
type: acceptance
release: v0.7.x
version: v0.7.6
parent: v0.7.x
owner: ""
depends_on: [core-102, core-304, core-305, core-306, core-307, core-308]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#309"]
source_updated: "2026-10-15T16:53:14Z"
labels: [kind/acceptance, area/runtime, area/security, area/kubernetes]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-309 · Tests: verify Kubernetes with restricted permissions #task #release/v0-7-x #status/planned #view/waiting #board/planned #area/testing #kind/acceptance
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Waiting for prerequisites**  
    **Needs:** [core-102](core-102-kubernetes-namespace-scoped-runtime-foundation.md), [core-304](core-304-kubernetes-security-identity-networking.md), [core-305](core-305-kubernetes-http-access-gateway-api.md), [core-306](core-306-kubernetes-namespaced-persistent-storage.md), [core-307](core-307-kubernetes-stateful-workloads.md), [core-308](core-308-kubernetes-availability-guarantees.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.7.x](../releases/v0.7.x.md) (v0.7.6)  
**Depends on:** [core-102](core-102-kubernetes-namespace-scoped-runtime-foundation.md), [core-304](core-304-kubernetes-security-identity-networking.md), [core-305](core-305-kubernetes-http-access-gateway-api.md), [core-306](core-306-kubernetes-namespaced-persistent-storage.md), [core-307](core-307-kubernetes-stateful-workloads.md), [core-308](core-308-kubernetes-availability-guarantees.md)  
**Required by:** [core-310](core-310-acceptance-compose-to-kubernetes-portability.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#309](https://github.com/mcpdev80/baseharbor/issues/309)
<!-- /generated:links -->

## Goal

Define Kubernetes Runtime conformance around real BaseHarbor lifecycle semantics and multiple realistic authorization profiles.

Namespace-only is a mandatory conformance profile.

## Scope

Carried over from the source with minimal editing (headings demoted, checkboxes turned into plain bullets).

### Conformance profiles

At minimum test:

##### A. Namespace-only

- pre-provisioned namespace;
- Role/RoleBinding only;
- no namespace creation;
- no ClusterRoleBinding;
- no Node read;
- no StorageClass write;
- no GatewayClass write;
- no CRD installation.

This profile must pass the normal supported app lifecycle.

##### B. Admin-capable local/dev context

Proves optional bootstrap/discovery behavior without becoming the assumed runtime model.

##### C. Platform-managed dependencies

Pre-provisioned:

- namespace;
- shared Gateway;
- storage policy;
- CRDs where required;
- admission/security controls.

BaseHarbor consumes them without ownership.

##### D. Insufficient permissions

Verify precise preflight failure for one missing required permission while unrelated operations remain possible.

##### E. Admission-mutated cluster

Verify reconciliation against server-observed semantic state instead of naive YAML equality.

##### F. Workload identity isolation

Application ServiceAccount has zero/minimal Kubernetes API privileges and is distinct from the BaseHarbor operator identity.

### Conformance surface

Validate:

- auth/access preflight;
- plan/apply;
- observe/verify;
- idempotency;
- SSA ownership/conflict handling;
- admission-aware reconciliation;
- security;
- networking;
- exposure;
- storage;
- stateful lifecycle;
- availability;
- finalizer-safe destroy.

### Additional negative conformance cases

Conformance must also cover:

- same namespace name on a different runtime target/context must not permit an unsafe destructive operation;
- platform-owned namespace metadata remains untouched;
- shared namespace with unrelated workloads is not affected by BaseHarbor default-deny networking;
- private-image pull reference works without exposing credential contents;
- missing optional Event/list/watch permissions do not break the normal lifecycle;
- FQDN-only external egress is not falsely reported as enforced by standard NetworkPolicy;
- PDB/replicas alone are not accepted as proof of host/failure-domain availability.

### Kubernetes version and API compatibility

Runtime conformance must define the supported Kubernetes version/API range for the release.

Rules:

- use stable Kubernetes APIs where available;
- do not depend on deprecated/removed API versions when a supported stable API exists;
- capability/API discovery must fail with actionable diagnostics when a required API is unavailable;
- the support matrix must stay intentionally small and evidence-based rather than testing every Kubernetes version;
- Gateway API or provider CRDs are capability dependencies and must be detected separately from the core Kubernetes version.

## Acceptance

- Supported Kubernetes/API range is documented and exercised by conformance.
- Required APIs are discovered explicitly and unavailable/deprecated APIs fail with actionable diagnostics.
- Namespace-only profile passes as a required conformance gate.
- Normal app lifecycle does not require cluster-admin.
- Normal app lifecycle does not require mandatory cluster-wide read.
- Missing optional cluster permissions affect only dependent features.
- Admission mutation does not create false drift where semantics remain valid.
- Foreign field ownership is never force-overwritten by default.
- Finalizers are respected.
- Workload identities remain isolated.
- Results are human- and machine-readable from one model.
- Validation is economical and follows `docs/DEVELOPMENT_GUIDELINES.md`.

## Required checks

- Economical validation per `docs/DEVELOPMENT_GUIDELINES.md`. The [standard pre-release gate](../releases/v0.5.x.md#standard-pre-release-gate) applies to this patch release.

## Dependencies and file ownership

- Depends on core-102, core-304, core-305, core-306, core-307, core-308.

## Handoff

- Not started (future release).
