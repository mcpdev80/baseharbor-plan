---
id: core-300
type: acceptance
release: v0.5.x
version: v0.5.4
parent: v0.5.x
owner: ""
depends_on: [core-297, core-298, core-299]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#300"]
source_updated: "2026-10-15T16:53:51Z"
labels: [kind/acceptance, area/runtime, area/providers, area/compatibility]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-300 · Acceptance: verify portability and compatibility #task #release/v0-5-x #status/planned #view/waiting
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Needs:** [core-297](core-297-state-versioning-migration-compatibility.md), [core-298](core-298-contracts-cross-component-compatibility.md), [core-299](core-299-lifecycle-upgrades-recovery-deprecation.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.5.x](../releases/v0.5.x.md) (v0.5.4)  
**Depends on:** [core-297](core-297-state-versioning-migration-compatibility.md), [core-298](core-298-contracts-cross-component-compatibility.md), [core-299](core-299-lifecycle-upgrades-recovery-deprecation.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#300](https://github.com/mcpdev80/baseharbor/issues/300)
<!-- /generated:links -->

## Goal

Close v0.5 by proving the frozen contracts are stable, portable and ready for later availability/topology semantics and new runtimes without changing portable intent. An acceptance/hardening release, not a feature expansion. No new knob without a demonstrated need.

## Scope

- Portability questions (must all be yes without implementing the future platform): same contract by Compose today and Kubernetes/OpenShift later; capability provider can move to an AWS/Azure/GCP managed service without rewriting intent; runtime, provider, identity, networking, storage and distribution stay independent; no monolithic `aws`/`azure`/`gcp` mode; later availability/topology requirements negotiated without Kubernetes concepts in the contract.
- Kubernetes contract-readiness (paper/design acceptance for a namespace-restricted runtime): portable intent + deployment/operator state (runtime target, environment, access reference, platform resource references) → restricted runtime provider → plan/preflight/apply/observe/verify. Cover a pre-provisioned scope, credentials outside intent, platform-owned shared infrastructure, BaseHarbor-owned app resources, a missing permission affecting one feature, an unavailable platform fact yielding `unverifiable`, foreign ownership/conflict, and no runtime field in the contract.
- Target portability (#408): arbitrary existing scopes referenceable; scope interpretation behind the Runtime Provider; platform/external scope ownership preserved; destroy removes only BaseHarbor-owned resources; no new Target semantics or Kubernetes fields in `baseharbor.yaml`.
- Capability substitution: one negative test — the application needs capability X plus semantic Y; provider A implements both (supported); provider B only X (unsupported before mutation); use an existing family and a realistic requirement.
- Executable matrix (Compose reference): fresh app → init → plan → up → status → doctor; existing supported contract; supported old state migration; provider protocol compatibility; full agent-native Compose lifecycle through MCP/JSON; drift → repair; backup → restore → real verification; update/upgrade → verification/recovery; ownership-safe destroy; shared/application/external placement where supported; secret-safe diagnostics/evidence.
- Portability review: classify important public/state fields as portable intent, environment/operator policy, capability-provider state, runtime state or protected/generated state; flag anything tied to Compose/Docker/Podman, Kubernetes/OpenShift, AWS/Azure/GCP, a managed service or a storage/network/identity product (blocking only when the frozen public contract or portability is affected).
- DX: five-minute onboarding works; sparse configuration; low-friction upgrades; actionable compatibility errors; implementation details out of normal output; CLI/JSON/MCP agree; no speculative framework.
- Delivery portability (contract/fixture): direct delivery stays the Compose reference; a delegated delivery fixture represents desired revision, sync state and reconciliation ownership without GitOps product fields; conflicting reconciliation ownership fails closed.
- Provider Catalog portability (contract/fixture): one catalog contract for all three families with separate responsibilities; discovery metadata ≠ instance/binding state; selection by immutable OCI digest; unsupported protocol/contract versions rejected before mutation; capability substitution only when the semantic subset is satisfied; Delivery and Runtime Provider substitution keep intent unchanged; artifact/version changes observable in status/plan/evidence.
- Third-party runtime proof (#396): a fake/reference conforming runtime implements the frozen boundary without intent changes or product-specific Core branches; unsupported semantics fail before mutation; Docker/Podman are reference implementations, not privileged paths; document adopted standards vs minimal extensions.
- Comments (2026-09-23): include the real developer journey and artifact truth — pristine repo → guided `baha app init` → `baha up`; deterministic CI path separately; repository Compose/source read-only; intent vs provider resolution visibly distinct; default provider observable without leaking into intent; stale runtime image detection; changed vs unchanged `build:` convergence; Docker/Podman parity; CLI/verbose/JSON/MCP agree on desired/realized/verified truth; update reports application-facing, provider/runtime and recovery implications; no false READY. Reuse #372 and #367–#379 work. Prove #390/#391: same service intent with different conforming providers; stable Service Binding names; protocol requirements do not become product selection; catalog metadata stays out of intent; adopted standards used; extensions isolated/versioned; no provider product fields in service schemas; legacy env projections not canonical; RESP without Redis identity; S3 without AWS identity; OTLP for observability; OIDC/OAuth for identity; AsyncAPI/CloudEvents for messaging; vector a small extension.
- Out of scope: HA/topology, Kubernetes/OpenShift/cloud implementations, Operator/CRDs, OIDC/RBAC/JIT, air-gap/private registry, ecosystem expansion.

## Acceptance

- The test does not rely on provider product names in portable application intent.
- A negative provider-substitution scenario proves semantic incompatibility is rejected before mutation.
- An arbitrary pre-existing target scope such as `r2-4b-dt-test` can be selected without changing portable application intent.
- Destroy never deletes a platform/external target scope itself; it removes only BaseHarbor-owned resources within it.
- `unsupported`, `unverifiable`, authorization denial, conflict and foreign ownership remain distinct machine-readable states.
- Missing permission/capability can block one feature without unnecessarily blocking unrelated lifecycle operations.
- Future runtime target, access source and platform-resource references require no portable-contract Kubernetes fields.
- A namespace-restricted Kubernetes thought experiment fits entirely within the frozen deployment/runtime boundaries.
- Full Compose reference lifecycle passes on the exact release head.
- Supported state migrations pass end to end.
- Public compatibility contracts are versioned/documented.
- Capability-provider compatibility is demonstrated.
- CLI/JSON/MCP expose the same underlying semantics.
- A generic coding agent completes the supported Compose lifecycle end to end without raw shell/Docker/Compose fallback.
- MCP covers the necessary semantic lifecycle without becoming a 1:1 CLI mirror.
- Portable application intent contains no runtime/cloud-vendor realization details.
- Architecture review confirms Kubernetes/OpenShift/AWS/Azure/GCP remain implementable without fundamental contract rewrite.
- Backup/restore, repair and destroy remain ownership-safe.
- Documentation matches current behavior and clearly marks future behavior.
- Validation is truthful and economical; unnecessary GitHub Actions are not used.
- Remaining blockers for the next phase are explicit and limited to genuine missing platform primitives.
- Provider Catalog and Provider Runtime Registry boundaries are proven separately.
- Runtime, Capability and Delivery provider descriptors validate against the frozen catalog schema.
- OCI artifact reference/digest consistency is verified.
- Unsupported descriptor/protocol/contract combinations fail before mutation.
- Provider replacement preserves portable application intent when compatibility requirements are satisfied.

## Required checks

- Economical local/repository validation per `docs/DEVELOPMENT_GUIDELINES.md`; no unnecessary GitHub Actions. The [standard pre-release gate](../releases/v0.5.x.md#standard-pre-release-gate) applies to this patch release.

## Dependencies and file ownership

- Depends on the v0.5.0 freeze (#175), core-297, core-298 and core-299.

## Handoff

- Not started (future release).
