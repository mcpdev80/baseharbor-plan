---
id: core-304
areas: [kubernetes]
type: feature
release: v0.7.x
version: v0.7.1
parent: v0.7.x
owner: ""
depends_on: [core-102]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#304"]
source_updated: "2026-10-15T16:53:45Z"
labels: [kind/feature, area/security, area/identity, area/kubernetes, area/networking]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-304 · Kubernetes: implement security, identity and networking #task #release/v0-7-x #status/planned #view/waiting #area/kubernetes #kind/feature
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Needs:** [core-102](core-102-kubernetes-namespace-scoped-runtime-foundation.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.7.x](../releases/v0.7.x.md) (v0.7.1)  
**Depends on:** [core-102](core-102-kubernetes-namespace-scoped-runtime-foundation.md)  
**Required by:** [core-305](core-305-kubernetes-http-access-gateway-api.md), [core-306](core-306-kubernetes-namespaced-persistent-storage.md), [core-308](core-308-kubernetes-availability-guarantees.md), [core-309](core-309-tests-kubernetes-restricted-permissions.md), [core-310](core-310-acceptance-compose-to-kubernetes-portability.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#304](https://github.com/mcpdev80/baseharbor/issues/304)
<!-- /generated:links -->

## Goal

Realize BaseHarbor security, workload identity and network-isolation semantics on Kubernetes while preserving namespace-only operation.

## Scope

Carried over from the source with minimal editing (headings demoted, checkboxes turned into plain bullets).

### Identity separation

Three identities remain distinct:

```text
Platform/bootstrap identity
BaseHarbor operator identity
Application workload identity
```

The BaseHarbor operator identity must never be reused as the application ServiceAccount.

### Namespaced RBAC

The normal application lifecycle must work with Role/RoleBinding permissions inside the target namespace.

BaseHarbor must avoid requiring:

- ClusterRoleBinding;
- impersonate;
- escalate;
- bind;
- arbitrary service-account token minting;
- cluster-admin.

Any stronger permission requires an explicit demonstrated feature.

### Workload ServiceAccounts

Application ServiceAccounts are namespaced, app-scoped and least privilege.

Rules:

- workload SA != BaseHarbor operator identity;
- disable token automount where Kubernetes API access is not needed;
- do not expose arbitrary ServiceAccount selection in portable app intent;
- workload API access must be an explicit capability/need.

### Secret handling

Avoid broad secret privileges where possible.

BaseHarbor must not assume wildcard `get/list/watch secrets` is harmless.

Use the narrowest practical ownership/access path and preserve external secret-provider options.

Secret values never appear in:

- labels/annotations;
- events/evidence;
- status;
- logs;
- JSON/MCP output.

### Namespace as trust boundary

BaseHarbor must not claim strong tenant isolation between mutually untrusted workloads sharing one namespace.

Default architecture should prefer application/environment isolation by namespace when the platform permits it.

If a platform forces multiple applications into one namespace, BaseHarbor must describe reduced isolation honestly and avoid false guarantees.

### Network isolation

Normal model:

```text
deny by default
      ↓
allow only explicit capability/provider connectivity
```

Use namespaced NetworkPolicy where available.

Connectivity derives from BaseHarbor bindings, not developer-authored Kubernetes rules.

### Platform limitations

If required network isolation cannot be enforced because the cluster/CNI lacks the capability:

- fail only the affected security guarantee;
- do not silently claim isolation;
- do not require cluster-admin to "fix" it automatically.

### Shared-namespace network safety

A platform/external namespace may contain workloads not owned by the current BaseHarbor application.

Therefore BaseHarbor must never install a namespace-wide default-deny policy in a shared/platform-owned namespace unless it explicitly owns that policy boundary.

Normal shared-namespace realization must scope NetworkPolicies to BaseHarbor-owned application pods using stable selectors/identity.

Destroy/repair must not modify network policy for unrelated workloads.

### External endpoint limitation

Standard Kubernetes NetworkPolicy cannot generically express every hostname/FQDN-based external-provider egress requirement.

Therefore BaseHarbor must not claim that a portable external capability binding can always be enforced through standard NetworkPolicy.

For external/provider endpoints:

- use standard Kubernetes policy when the endpoint can be represented safely;
- use an explicitly declared platform/network capability when available;
- otherwise report the requested egress-isolation guarantee as unsupported or unverifiable;
- never resolve a hostname once and persist dynamic service IPs as if they were a stable security policy.

### RBAC creation boundary

Having namespaced application permissions does not imply BaseHarbor may create or change Role/RoleBinding objects.

Platform-provisioned operator RBAC is the normal model.

BaseHarbor creates application Roles/RoleBindings only when a demonstrated workload API-access requirement exists and the current identity is explicitly authorized to do so.

Failure to create optional workload RBAC must affect only that workload capability.

## Acceptance

- Namespace-only Role/RoleBinding is sufficient for normal app lifecycle.
- BaseHarbor operator identity and workload ServiceAccount are distinct.
- Workloads without Kubernetes API needs receive no unnecessary token.
- No normal-path dependency on `bind`, `escalate`, or `impersonate`.
- Secret handling avoids unnecessary broad namespace-secret access.
- Namespace isolation limits are documented honestly.
- Default-deny + explicit binding connectivity works where supported.
- Unsupported isolation fails clearly without broadening privileges.
- CLI/JSON/MCP report the same security state.
- Validation follows `docs/DEVELOPMENT_GUIDELINES.md`.

## Required checks

- Economical validation per `docs/DEVELOPMENT_GUIDELINES.md`. The [standard pre-release gate](../releases/v0.5.x.md#standard-pre-release-gate) applies to this patch release.

## Dependencies and file ownership

- Depends on core-102.

## Handoff

- Not started (future release).
