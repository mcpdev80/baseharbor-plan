---
id: core-297
areas: [contracts]
type: architecture
release: v0.5.x
version: v0.5.1
parent: v0.5.x
owner: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#297"]
source_updated: "2026-10-15T16:54:11Z"
labels: [kind/architecture, area/compatibility]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-297 · State: define versioning and migration compatibility #task #release/v0-5-x #status/planned #view/queued #area/contracts #kind/architecture
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** not set  
    **Later release** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** queued  
**Release:** [v0.5.x](../releases/v0.5.x.md) (v0.5.1)  
**Depends on:** none  
**Required by:** [core-298](core-298-contracts-cross-component-compatibility.md), [core-299](core-299-lifecycle-upgrades-recovery-deprecation.md), [core-300](core-300-acceptance-portability-compatibility.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#297](https://github.com/mcpdev80/baseharbor/issues/297)
<!-- /generated:links -->

## Goal

Make BaseHarbor state safely evolvable after the v0.5.0 freeze without migration ceremony for normal users. A supported upgrade normally stays `baha up → detect state version → preflight migration → migrate if safe → verify → continue`.

## Scope

- Target semantics are owned by #408; this item versions/migrates those persisted structures as an existing compatibility surface.
- Version/compatibility handling for BaseHarbor-owned state: deployment/operator, runtime, capability-provider, secure bindings and ownership metadata, generated/protected, backup/restore metadata, durable audit/evidence.
- Requirements: explicit state/schema version ownership; deterministic migrations; non-mutating preflight; safe handling of partially failed migrations; unknown incompatible future state fails closed; ownership/isolation invariants preserved; no runtime/provider detail promoted into portable intent.
- Migration rules: migrate only owned state; prefer additive; never silently discard unknown or security-relevant state; verify invariants after migration; failure leaves an actionable recovery path; rollback only where safe and meaningful (recovery may use the last verified state/backup).
- DX: normal supported upgrades automatic; warnings explain what needs migration and why; no manual migration file editing; no global migration framework unless state requires it; small explicit testable migrations.
- Deployment/runtime state: define version ownership where persisted for deployment target identity, selected runtime/provider identity, access-source reference metadata (no credentials), platform-resource reference metadata, ownership classification of external/platform resources, capability/permission observations affecting planning, typed unsupported/unverifiable/authorization/conflict state. Never migrate credentials into portable state; never convert platform-owned resources into BaseHarbor-owned implicitly; keep runtime realization behind the runtime boundary.
- Provider Catalog selection: version ownership for selected provider family, stable provider ID, resolved implementation version, Provider Protocol metadata, resolved OCI reference and digest, selected service/capability contract version, selected Delivery Provider and reconciliation ownership. Catalog metadata never enters portable intent; catalog entries are not runtime instances; `provider-registry.json` instance/binding/ownership semantics stay runtime state; old identifiers migrate deterministically; digest is used when available; missing/incompatible identity fails preflight.
- Comment (2026-09-23): where artifact/convergence metadata is persisted, cover desired/resolved/realized artifact identity, immutable digest metadata, repository build fingerprints, selected provider/runtime identity and interpretation metadata; no secret values in fingerprints or migration state; supported old state migrates deterministically or fails before mutation; output concise for humans, inspectable via verbose/JSON/MCP; no manual edits of migration files or runtime metadata.
- Out of scope: Kubernetes/OpenShift/cloud state, HA/topology, distributed control-plane migrations, rolling multi-node upgrades.

## Acceptance

- Migrations preserve external/platform ownership and never import credential material into portable application state.
- Deployment target/access/platform-reference state has explicit ownership/versioning where persisted.
- Supported v0.4/v0.5 state has explicit version ownership.
- Supported old state can be migrated deterministically.
- Migration preflight is non-mutating.
- Failed/incompatible migration does not continue into unsafe apply.
- Ownership, isolation and secret-safety invariants survive migration.
- Post-migration verification checks the authoritative behavior/state.
- Normal supported migration is low-friction for developers.
- Tests cover success, invalid state, interrupted/failed migration and unsupported future state.
- Documentation follows `docs/DEVELOPMENT_GUIDELINES.md`.
- No unnecessary GitHub Actions are introduced or triggered.
- Persisted provider resolution has explicit state ownership and versioning where needed.
- Provider Catalog identity and Provider Runtime Registry instance identity remain distinct after migration.
- OCI artifact digest identity survives supported migrations without silent substitution.
- Runtime, Capability and Delivery Provider selections can evolve independently without entering portable application intent.

## Required checks

- Economical local/repository validation per `docs/DEVELOPMENT_GUIDELINES.md`; no unnecessary GitHub Actions. The [standard pre-release gate](../releases/v0.5.x.md#standard-pre-release-gate) applies to this patch release.

## Dependencies and file ownership

- Depends on the v0.5.0 freeze (#175, in [v0.5.x](../releases/v0.5.x.md)); no task-level dependency.

## Handoff

- Not started (future release).
