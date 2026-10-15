---
id: core-298
areas: [contracts]
type: architecture
release: v0.5.x
version: v0.5.2
parent: v0.5.x
owner: ""
depends_on: [core-297]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#298"]
source_updated: "2026-10-15T16:54:04Z"
labels: [kind/architecture, area/runtime, area/providers, area/compatibility]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-298 · Contracts: define cross-component compatibility #task #release/v0-5-x #status/planned #view/waiting #area/contracts #kind/architecture
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Waiting for prerequisites**  
    **Needs:** [core-297](core-297-state-versioning-migration-compatibility.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.5.x](../releases/v0.5.x.md) (v0.5.2)  
**Depends on:** [core-297](core-297-state-versioning-migration-compatibility.md)  
**Required by:** [core-299](core-299-lifecycle-upgrades-recovery-deprecation.md), [core-300](core-300-acceptance-portability-compatibility.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#298](https://github.com/mcpdev80/baseharbor/issues/298)
<!-- /generated:links -->

## Goal

Make the public compatibility boundaries explicit so CLI, stored state, capability providers and machine interfaces evolve independently without contaminating portable semantics. Stable contracts, minimal ceremony.

## Scope

- Boundaries to document and verify: CLI/Core ↔ Portable Application Contract; CLI/Core ↔ stored state; Core ↔ Capability Provider Protocol; CLI/JSON/MCP ↔ shared machine result/error contract; Core ↔ Runtime Provider boundary; Deployment/Operator state ↔ Runtime Provider; Runtime Access Reference ↔ Runtime Provider; Platform Resource Ref ↔ Runtime Provider; Runtime Capability Result ↔ shared plan/status/error model; Core ↔ Provider Catalog Descriptor; descriptor ↔ OCI artifact identity; Core ↔ Provider Protocol; Core ↔ Runtime/Capability/Delivery Provider. The public boundary is the documented spec/protocol, not Go package layout.
- Runtime and cloud neutrality (Compose, Kubernetes, OpenShift, future AWS/Azure/GCP): capability provider ≠ runtime provider; cloud vendor ≠ application intent; runtime detail ≠ portable intent; managed cloud services stay replaceable realizations; no portable field added for a future platform.
- Scope: compatibility matrix of supported contract/protocol versions; provider protocol guarantees; machine result/error guarantees; runtime-boundary rules; additive vs breaking evolution; clear unsupported-version diagnostics; tests of supported combinations.
- Target compatibility uses the #408 contract (select runtime and Target, associate deployment identity, access by reference, platform resource references, BaseHarbor-owned vs platform/external) with no runtime-specific portable fields. Runtime access is a secret-safe reference/source resolved by the runtime (kubeconfig/OIDC/cloud auth are implementations, not contract types). Restricted runtimes report supported, unsupported, not authorized, unverifiable, ownership conflict, foreign ownership, degraded; unrelated lifecycle operations stay available.
- Separate checks: capability spec/version compatibility; application-required semantic subset; availability/durability/topology guarantees. Delivery Providers are a third axis and must preserve ownership, policy, verification and result semantics regardless of mechanism.
- Catalog compatibility distinguishes descriptor schema, implementation version, Provider Protocol, service/capability contract, provider family and OCI digest consistency; a catalog match alone never proves usability. Minimal catalog contract is in scope; marketplace breadth is not.
- Runtime-provider axes (#396): Core version, Runtime Provider contract/protocol, implementation version, adopted standards, product/engine version, OCI digest. Product-version equality alone is not compatibility.
- Comments (2026-09-23): also cover CLI/Core ↔ runtime image/API, Core ↔ provider implementation version, Core ↔ persisted artifact/convergence state, application capability ↔ provider semantic support. PostgreSQL is the current default SQL realization, not intent; provider/product/version/digest stay visible facts. Report what matters to the application (contract/API/provider-version changes, deprecations, adaptation needed); image/digest negotiation in verbose/machine diagnostics. Stale or incompatible artifacts are never compatible merely because they run. Include the #390/#391 axes (service contract, provider protocol, implementation, product/engine, artifact digest, standard protocol compatibility such as RESP, S3, OTLP, OIDC); object-storage ≠ S3, cache ≠ RESP; Service Binding 1.1 output and JSON Schema 2020-12 compatibility belong in the matrix.
- Out of scope: implementing Kubernetes/OpenShift/cloud runtimes, HA/topology, catalog expansion, Go ABI stability, enterprise identity/governance. DX: compatibility automatic in the normal path; errors name the incompatible boundary and supported versions; no internal negotiation noise; no unnecessary Go API freeze; no adapters/shims before a demonstrated case.

## Acceptance

- Provider negotiation cannot silently treat partial semantic compatibility as full support.
- Cross-component compatibility documents capability-version, capability-semantic and availability-guarantee compatibility as separate concerns.
- Runtime providers can return permission/capability-aware typed outcomes without collapsing unrelated lifecycle operations.
- Platform-owned resource references are supported without runtime-specific portable fields.
- Runtime access is modeled as a secret-safe deployment reference/source rather than portable credentials.
- Deployment/operator-to-runtime compatibility is documented as a public boundary.
- Supported compatibility boundaries are documented and versioned.
- Capability providers can target the public protocol without BaseHarbor Core changes.
- CLI/JSON/MCP share compatible semantic result/error contracts.
- Runtime provider compatibility does not require portable-contract runtime fields.
- Architecture review confirms AWS/Azure/GCP can later supply runtimes and/or managed capability providers independently.
- Unsupported versions fail with actionable diagnostics.
- Compatibility tests cover supported and intentionally unsupported combinations.
- Internal implementation packages are not accidentally declared public compatibility surfaces.
- Validation follows `docs/DEVELOPMENT_GUIDELINES.md` economically.
- Runtime, Capability and Delivery Provider descriptors use one versioned catalog contract with family-specific semantics.
- Unsupported descriptor/protocol/contract versions fail with an actionable compatibility error before mutation.
- Catalog resolution verifies OCI artifact identity/digest where an artifact is selected.
- Catalog metadata cannot bypass Provider Protocol or capability-semantic compatibility checks.
- Provider Catalog compatibility and Provider Runtime Registry state compatibility are tested as separate boundaries.

## Required checks

- Economical local/repository validation per `docs/DEVELOPMENT_GUIDELINES.md`; no unnecessary GitHub Actions. The [standard pre-release gate](../releases/v0.5.x.md#standard-pre-release-gate) applies to this patch release.

## Dependencies and file ownership

- Depends on the v0.5.0 freeze (#175) and core-297. Consumes core-390.

## Handoff

- Not started (future release).
