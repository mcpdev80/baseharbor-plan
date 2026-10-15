---
id: core-181
areas: [delivery]
type: feature
release: backlog
version: ""
parent: core-209
owner: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#181"]
source_updated: "2026-10-15T16:54:24Z"
labels: [kind/feature, area/security, area/artifacts, status/backlog]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-181 · Distribution: air gap and private OCI registries #task #release/backlog #status/backlog #view/backlog #area/delivery #kind/feature
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** backlog  
**Release:** [backlog](../releases/backlog.md)  
**Parent:** [core-209](../epics/core-209-future-capabilities-integrations.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#181](https://github.com/mcpdev80/baseharbor/issues/181)
<!-- /generated:links -->

## Goal

Make BaseHarbor fully usable in disconnected/air-gapped and enterprise environments where all container images and future provider artifacts must be resolved through operator-controlled private registries such as Nexus Repository, JFrog Artifactory, Harbor, Quay or any standards-compliant OCI registry.

This must be a deployment/distribution concern, not application intent.

## Scope

Carried over from the source with minimal editing (headings demoted, checkboxes turned into plain bullets).

> **Roadmap update (2026-09-20)**
>
> This remains a later enterprise/runtime-distribution track and does not block v0.5. It is listed under the post-v0.5 planning umbrella #209.

### Core principle

> Applications request BaseHarbor capabilities. Operators decide where the required artifacts come from.

The portable application contract must never need to know whether an image/provider artifact is pulled from ghcr.io, Docker Hub, Nexus, Artifactory, Harbor, Quay, an OpenShift mirror or an offline bundle.

### Standards

Prefer public standards and existing runtime mechanisms:

- OCI Distribution Specification / OCI images and artifacts;
- digest-pinned references where practical;
- standard container-runtime registry authentication;
- custom/private CA trust;
- registry mirrors / repository remapping;
- standard OCI artifact transport for future external BaseHarbor providers.

Do not introduce a BaseHarbor-specific proprietary registry protocol.

### Required model

Introduce deployment-owned artifact/registry policy usable by CLI, future API/Web UI and future Operator.

Conceptually:

```text
portable application contract
        |
        v
required logical artifact
        |
        v
BaseHarbor artifact resolution policy
        |
        +--> public registry
        +--> private mirror
        +--> Nexus
        +--> Artifactory
        +--> Harbor / Quay
        +--> offline imported bundle
```

The mapping belongs to deployment/platform policy.

### Scope

##### Private registries

Support operator-defined OCI registries for BaseHarbor-managed artifacts, including at least:

- control-plane images;
- built-in/reference capability provider images;
- runtime broker/helper images;
- future external provider OCI artifacts;
- application images where BaseHarbor is responsible for resolving/pulling them.

Examples must work with generic OCI endpoints rather than vendor-specific integrations.

##### Registry remapping / mirrors

Allow a deployment to remap upstream sources without rewriting application manifests.

Examples:

```text
ghcr.io/mcpdev80/baseharbor-runtime@sha256:...
  -> nexus.example.internal/baseharbor/baseharbor-runtime@sha256:...

docker.io/library/postgres@sha256:...
  -> artifactory.example.internal/docker-remote/library/postgres@sha256:...
```

Policy should support:

- exact registry replacement;
- namespace/repository prefix mapping where needed;
- mirror ordering/fallback only when explicitly allowed;
- strict offline mode with **no public-network fallback**.

##### Authentication

Reuse standard operator/runtime credentials.

Requirements:

- no registry username/password/token in `baseharbor.yaml`;
- support existing Docker/Podman credential mechanisms where possible;
- allow BaseHarbor protected deployment inputs/state for non-interactive environments;
- secrets must never be printed in plan/status/doctor/provider metadata;
- future Kubernetes/OpenShift implementation should map naturally to image pull secrets/service accounts without changing application intent.

##### TLS / private CA

Support enterprise registries using private PKI.

Requirements:

- custom CA trust is deployment-owned;
- no global insecure-TLS switch as the normal solution;
- fail closed on invalid/untrusted registry TLS unless explicitly configured by operator policy;
- do not copy private CA material into portable application contracts.

##### Air-gapped mode

Add an explicit strict disconnected mode.

In strict air-gap mode:

- BaseHarbor must perform no implicit Internet registry access;
- every required artifact must resolve locally before mutation;
- preflight reports every missing artifact before apply;
- there is no silent fallback to Docker Hub/GHCR or another public registry;
- status/doctor can identify unresolved/missing local artifacts without exposing credentials.

##### Offline bundle workflow

Provide a deterministic way to prepare and import all artifacts required by a BaseHarbor deployment.

Target workflow, exact UX TBD:

```bash
# connected staging machine
baha artifacts plan
baha artifacts export --output baseharbor-bundle.tar.zst

# transfer through approved process

# disconnected environment
baha artifacts import baseharbor-bundle.tar.zst
baha up
```

A bundle should include an auditable manifest containing:

- logical artifact identity;
- source reference;
- resolved digest;
- target/mirror reference;
- BaseHarbor/provider version compatibility metadata.

Do not include operator credentials in bundles.

##### Digest-first reproducibility

Prefer immutable digests for BaseHarbor-owned/runtime/provider artifacts.

Tags may remain usable for developer convenience, but air-gapped/enterprise flows should be able to freeze all required artifacts to resolved digests so the same deployment is reproducible after transfer.

##### Provider Integration Contract

This feature must align with #178.

Future third-party providers distributed as OCI artifacts must use the same registry/mirror/offline policy. A vendor publishing a BaseHarbor-compatible provider must not require BaseHarbor Core changes or a proprietary download path.

### Preflight / lifecycle semantics

Artifact resolution is part of:

```text
plan -> preflight -> apply -> verify
```

Before mutation BaseHarbor must know whether every required artifact is resolvable under the active registry policy.

In strict air-gap mode, missing artifacts are a preflight failure.

### Example deployment policy

Illustrative only; final schema belongs in protected deployment/platform configuration, not the portable app contract:

```yaml
artifacts:
  mode: airgapped
  registries:
    default: registry.infra.example
  mirrors:
    ghcr.io: registry.infra.example/github
    docker.io: registry.infra.example/dockerhub
  tls:
    ca: /etc/baseharbor/registry-ca.pem
```

### Non-goals

- implementing a registry server inside BaseHarbor;
- vendor-specific Nexus/Artifactory lifecycle management;
- requiring developers to change application image names solely because the deployment is air-gapped;
- weakening TLS verification as the default enterprise path.

### Architecture constraint

This feature must remain orthogonal to the capability provider registry.

The **provider registry** answers: which provider instance satisfies which logical application capability?

The **artifact registry/distribution policy** answers: where does BaseHarbor obtain the immutable software artifact used to run that implementation?

These are separate domains and must not be conflated.

### Roadmap placement

This issue is deliberately **outside the v0.4.x -> v0.5.0 capability-platform build-up**.

The implementation should align with the runtime-provider roadmap:

- **v0.7 Kubernetes**: introduce/reuse the generic artifact-resolution/private-registry seam required by Kubernetes image/provider deployment.
- **v0.8 Kubernetes Complete**: only the Kubernetes runtime seams needed for first-class operation are in scope (for example pre-provisioned image-pull credentials and runtime-owned artifact references). Full enterprise registry/mirror/private-CA/strict-disconnected/offline-bundle workflows remain deferred.
- **v0.9+ OpenShift / Enterprise**: complete enterprise proxy/mirror/private-CA/strict-disconnected and offline-bundle workflows, including OpenShift-style registry constraints.

Earlier code may preserve compatible seams, but v0.4.x releases must not be blocked by private-registry or air-gap implementation work.

This placement is consistent with #102, where enterprise registry/proxy/offline constraints belong to the OpenShift/enterprise runtime track.

### Cross-cutting provider placement and sharing-boundary rule

BaseHarbor must keep application intent simple and keep infrastructure topology out of the portable application contract.

Canonical model:

```text
Application intent
  -> Capability
  -> Provider resolution
  -> Provider placement
       - application
       - shared
           - optional sharing boundary
       - external
  -> Isolation / deployment boundary
  -> Runtime/provider implementation
```

Rules:

- `shared | application | external` is a generic BaseHarbor provider-placement model, not capability-specific policy.
- `shared` does **not** mean accessible by every application. Access remains explicit and deny-by-default.
- A shared provider may optionally be restricted to a named sharing boundary/group so multiple applications can intentionally share one provider instance without exposing it to unrelated applications.
- A sharing boundary is a property of shared placement, **not a fourth provider scope**.
- Provider placement, sharing boundary, lifecycle ownership and external references are deployment/operator state and must not leak into portable application intent.
- A concrete provider declares which placements it supports. Unsupported requested placement fails closed before mutation; BaseHarbor must not silently fall back to another placement.
- Logical resources remain application-owned even when backed by a shared provider.
- Multiple BaseHarbor installations are reserved for genuine control-plane/trust/administrative boundaries, not merely because a subset of applications needs a shared provider.
- Developer UX stays capability-oriented: the developer states what the application needs; BaseHarbor/platform policy resolves provider, placement, sharing and isolation.
- Current implementation remains Docker/Podman Compose. Kubernetes/OpenShift are **not** implemented by this rule.
- The model must nevertheless avoid Compose-specific coupling so a later runtime can map isolation/deployment boundaries to Kubernetes namespaces/clusters, OpenShift projects/clusters, Helm releases or Operators without changing application intent.
- Operator installation scope is independent from provider placement/resource scope. A future cluster-scoped Operator may still manage application-scoped or sharing-boundary-scoped resources.
- Do not equate provider placement with runtime topology: `shared` is not automatically a shared Docker network, and `application` is not automatically a dedicated host/namespace.

This rule is architecture-wide and must be reused by provider integrations instead of introducing capability-specific placement variables or parallel scope models.

## Acceptance

- BaseHarbor can bootstrap and run with outbound Internet registry access disabled.
- All BaseHarbor control-plane/runtime/provider images can be served from a private standards-compliant OCI registry.
- Nexus and Artifactory require no product-specific BaseHarbor code beyond generic OCI registry support.
- Registry policy can remap upstream image references without modifying `baseharbor.yaml`.
- Strict air-gap mode never silently falls back to public registries.
- Missing artifacts fail during preflight before runtime/application mutation.
- Private registry credentials and CA material stay outside portable application intent.
- Digest-pinned offline bundle export/import is reproducible and auditable.
- Future external provider OCI artifacts use the same mechanism.
- Architecture is reusable by CLI, future Web UI/API and Kubernetes/OpenShift Operator.

## Required checks

- To be defined when scheduled.

## Dependencies and file ownership

- Unscheduled (`status/backlog`). Referenced source issues: none.

## Handoff

- Not scheduled.
