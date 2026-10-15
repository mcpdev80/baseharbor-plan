---
id: core-102
type: feature
release: v0.7.x
version: v0.7.0
parent: v0.7.x
owner: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#102"]
source_updated: "2026-10-15T16:54:50Z"
labels: [kind/feature, area/runtime, area/kubernetes, area/compatibility]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-102 · Kubernetes: establish a namespace-scoped runtime foundation #task #release/v0-7-x #status/planned #view/queued
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Later release** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** queued  
**Release:** [v0.7.x](../releases/v0.7.x.md) (v0.7.0)  
**Depends on:** none  
**Required by:** [core-304](core-304-kubernetes-security-identity-networking.md), [core-305](core-305-kubernetes-http-access-gateway-api.md), [core-306](core-306-kubernetes-namespaced-persistent-storage.md), [core-307](core-307-kubernetes-stateful-workloads.md), [core-308](core-308-kubernetes-availability-guarantees.md), [core-309](core-309-tests-kubernetes-restricted-permissions.md), [core-310](core-310-acceptance-compose-to-kubernetes-portability.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#102](https://github.com/mcpdev80/baseharbor/issues/102)
<!-- /generated:links -->

## Goal

Implement Kubernetes as a real BaseHarbor Runtime Provider while keeping the normal application lifecycle fully usable with **namespace-only permissions**.

> **Developer experience first.**
>
> **Namespace-only is the primary enterprise-compatible mode.**
>
> **Kubernetes realizes BaseHarbor semantics; it does not redefine them.**
>
> **As little as possible, as much as necessary.**

## Scope

Carried over from the source with minimal editing (headings demoted, checkboxes turned into plain bullets).

### Status correction — Kubernetes implementation remains planned

Parent: #430; milestone: **v0.7.x**. Reopened because this issue's current scope requires an actual Kubernetes Runtime Provider and namespace-only lifecycle acceptance. The historical closure followed the v0.4 runtime-selection/guard foundations (#135–#148); it does not prove the expanded Kubernetes implementation below. The current v0.4.25 runtime provider tree contains Docker and Podman, and the master roadmap #155 still schedules Kubernetes implementation in v0.7.x.

Preserve the accepted architectural foundation. Complete the runtime implementation and required native namespace-only evidence here before marking this v0.7.0 scope done. Contradictory historical v0.4.0/v0.7.0/v0.8.0 labels are replaced by the v0.7.x milestone and canonical kind/area labels.

---

### Core architecture

```text
Portable Application Contract
        ↓
Environment / Policy
        ↓
Availability / Guarantees
        ↓
BaseHarbor Core
        ↓
Kubernetes Runtime Provider
        ↓
Kubernetes API
```

Capability providers remain separate from the runtime provider.

### Primary access model

The default design target is:

```text
Platform Admin
  -> pre-provisions namespace and cluster-scoped dependencies

BaseHarbor operator/user
  -> namespaced credentials only
  -> manages application-scoped resources

Application workload
  -> separate ServiceAccount
  -> minimal or zero Kubernetes API permissions
```

BaseHarbor must not require cluster-admin or cluster-wide read access for the normal namespaced lifecycle.

### Supported access modes

##### 1. Namespace-only mode — primary

Given a pre-provisioned namespace, BaseHarbor must support the normal application lifecycle using only namespaced permissions required by the selected plan.

Typical managed resources may include:

- Deployments;
- Services;
- ConfigMaps;
- Secrets owned by BaseHarbor where required;
- ServiceAccounts;
- Roles/RoleBindings owned by the application scope where needed;
- NetworkPolicies;
- PVCs;
- HTTPRoutes;
- PDBs;
- StatefulSets in later 0.7.x releases.

BaseHarbor must not require permission to:

- create/delete namespaces;
- create ClusterRoles/ClusterRoleBindings;
- create StorageClasses;
- create GatewayClasses;
- install CRDs;
- read Nodes;
- enumerate unrelated namespaces;
- mutate cluster-scoped policy.

##### 2. Broader admin-capable context — optional

Useful for local/dev/bootstrap scenarios.

BaseHarbor may use broader permissions when available, but must not build normal lifecycle assumptions around them.

##### 3. Platform-managed/bootstrap mode — optional

Platform admins may pre-provision:

- namespace;
- Gateway/GatewayClass;
- StorageClass;
- required CRDs;
- admission/security policy;
- shared infrastructure;
- other cluster-scoped dependencies.

BaseHarbor consumes these as external/platform-owned resources.

### Credentials

Support standard Kubernetes client credential sources rather than inventing BaseHarbor Kubernetes credentials:

- kubeconfig/current context;
- client certificate;
- OIDC;
- exec credential plugins;
- in-cluster/service-account credentials where appropriate.

Credentials and kubeconfig content must never enter portable application intent.

BaseHarbor must not persist privileged credentials unless a demonstrated deployment model requires it.

### Authorization preflight

Before mutation:

```text
plan
  ↓
derive exact Kubernetes operations
  ↓
SelfSubjectAccessReview per required action
  ↓
preflight result
  ↓
apply
```

Do not depend on broad permission enumeration as the authorization source of truth.

Missing permissions must identify:

- verb;
- API group/resource;
- namespace/scope;
- BaseHarbor feature requiring it;
- safe remediation.

Optional cluster permissions must block only the dependent feature, not unrelated namespaced lifecycle operations.

### Cluster-scoped dependencies

Treat cluster-scoped resources as platform-owned by default.

BaseHarbor may reference/use them when configured or discoverable, but must not require ownership.

Examples:

- StorageClass;
- GatewayClass/shared Gateway;
- CRDs;
- cluster admission/security policy;
- cluster-wide identity/integration resources.

### Namespace model

Namespace selection is deployment/operator state.

BaseHarbor must support:

- pre-provisioned namespace;
- optional BaseHarbor-created namespace only when explicit permissions exist.

No Kubernetes namespace field is required in portable application intent.

### Minimal workload realization

Initial runtime proof includes:

- Deployment;
- internal Service where required;
- application ServiceAccount;
- workload configuration/bindings;
- readiness observation;
- BaseHarbor semantic verification.

A Running/Available Kubernetes workload is not automatically BaseHarbor READY.

### Apply / ownership

Use Kubernetes API directly, not `kubectl`.

Prefer Server-Side Apply for BaseHarbor-owned fields.

Rules:

- explicit BaseHarbor field manager;
- no blind force ownership;
- own only fields BaseHarbor semantically controls;
- foreign ownership/conflict becomes typed state;
- admission-mutated legitimate fields do not automatically become drift;
- ownership metadata uses stable BaseHarbor identities.

Do not rely on cross-namespace OwnerReferences for BaseHarbor ownership.

### Security baseline

Initial workloads must be compatible with hardened/restricted environments:

- run as non-root;
- no unnecessary privilege escalation;
- drop unnecessary capabilities;
- seccomp where supported;
- no host PID/IPC/network by default;
- avoid fixed UID assumptions unless genuinely required;
- no workload API token unless required.

### Explicitly out of scope

- Gateway API realization;
- persistent storage realization;
- stateful support;
- topology/PDB realization;
- Operator/CRDs as BaseHarbor control model;
- OpenShift-specific behavior;
- cloud-specific runtime behavior.

### Target safety and restricted observation

A deployment target must be protected against accidental context/cluster switches.

Before mutating or destroying resources, BaseHarbor must verify that the resolved runtime access source still points at the intended deployment target as far as can be established without requiring cluster-wide privileges.

Rules:

- target scope name alone is not sufficient protection against accidentally selecting another cluster with the same namespace name;
- persist only secret-safe target identity/fingerprint metadata;
- do not require reading `kube-system`, Nodes or other unrelated cluster-scoped objects just to identify the target;
- destructive operations fail closed when target identity is ambiguous or changed unexpectedly;
- normal observation should prefer known BaseHarbor resource identities/names over broad namespace-wide list/watch permissions where practical;
- richer diagnostics such as Events are optional permissions and must not become normal lifecycle requirements.

### Platform-owned namespace protection

For a platform/external target scope BaseHarbor must not mutate namespace-level metadata or policy as part of the normal application lifecycle.

This includes, unless explicitly platform-authorized:

- namespace labels/annotations;
- Pod Security admission labels;
- quota/limit policy;
- platform network/security labels.

### Image pull access

A real Kubernetes runtime must support private application images without turning private-registry administration into v0.7 scope.

Minimum requirement:

- support a pre-provisioned namespaced image-pull credential/reference or other runtime-supported image identity mechanism;
- keep registry credentials outside portable application intent;
- treat platform-managed pull credentials as external/platform-owned;
- never read or expose credential contents merely to verify that a reference exists;
- image-pull failure must surface as a typed runtime verification failure.

Full private-registry lifecycle, mirrors and air-gapped distribution remain later work.

### Delivery-provider boundary

Direct Kubernetes API application is the initial/reference Kubernetes delivery implementation for v0.7.0, not a permanent requirement that all Kubernetes deployments be mutated directly by BaseHarbor.

The runtime implementation must preserve the frozen Delivery Provider boundary so later work can support delegated/GitOps delivery without changing portable application intent.

For the direct path:

```text
BaseHarbor
  ↓
Kubernetes API
```

BaseHarbor owns mutation/reconciliation for its managed resource set.

A later delegated path is implemented in #325. v0.7.0 must not introduce assumptions that make such delegation impossible.

### Existing target scope semantics

The standard rules for existing platform-named target scopes apply (see [v0.5.x](../releases/v0.5.x.md#rules), "Existing target scope semantics"): the runtime interprets the scope as the existing namespace, BaseHarbor never renames/recreates/deletes a platform-owned namespace, ownership is tracked below namespace level, and destroy removes only BaseHarbor-owned resources.

### Source comments

*mcpdev80, 2026-09-10* ([link](https://github.com/mcpdev80/baseharbor/issues/102#issuecomment-5622385284)):

Architecture rule accepted for future provider work: application contracts describe portable **capabilities, not infrastructure products**. Concrete products are selected by environment/platform-owned providers. Every default BaseHarbor component must have a provider boundary plus a documented replacement path, and unsupported guarantees must fail explicitly rather than silently degrade. Implementation guidance is being documented in ADR `docs/decisions/0005-capabilities-not-products.md` and `docs/capability-provider-model.md`. This does not expand v0.2.0 scope; Compose remains the current implementation focus.

## Acceptance

- An arbitrary pre-existing target scope such as `r2-4b-dt-test` can be selected without changing portable application intent.
- Destroy never deletes a platform/external target scope itself; it removes only BaseHarbor-owned resources within it.
- A representative stateless application runs with pre-provisioned namespace + namespace-only credentials.
- Cluster-admin is not required for normal lifecycle.
- Cluster-wide read is not required unless a selected feature genuinely needs it.
- Authorization preflight is derived from the actual plan.
- Missing optional cluster permissions affect only dependent features.
- Standard Kubernetes credential mechanisms are supported.
- Kubernetes API is used directly; no `kubectl` shell dependency.
- Namespace remains deployment/operator state.
- Deployment/Service/ServiceAccount lifecycle is idempotent.
- BaseHarbor verification follows Kubernetes readiness.
- Ownership/conflict/drift are typed and fail closed where required.
- CLI/JSON/MCP expose the same runtime-neutral semantics.
- Validation follows `docs/DEVELOPMENT_GUIDELINES.md`.

## Required checks

- Economical validation per `docs/DEVELOPMENT_GUIDELINES.md`. 

## Dependencies and file ownership

- Depends on the v0.5 freeze and compatibility acceptance; no open task dependency. Depends on the v0.5 contract freeze/compatibility acceptance; v0.6.x is not an unconditional prerequisite.

## Handoff

- Not started (future release).
