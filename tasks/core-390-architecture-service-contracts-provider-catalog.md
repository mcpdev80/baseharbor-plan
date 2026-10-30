---
id: core-390
areas: [architecture]
type: architecture
release: v0.4.x
version: ""
parent: v0.4.x
owner: marcel
depends_on: [core-893, core-895, core-896, t-20261027-r27-cutover-pr3]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#390"]
source_updated: "2026-10-15T16:52:05Z"
labels: [kind/architecture, area/providers, area/compatibility]
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/board-2026-10-30/w390.md","https://github.com/mcpdev80/baseharbor/commit/dd1923dc","https://github.com/mcpdev80/baseharbor/blob/develop/docs/decisions/0013-standards-first-service-provider-contracts.md"]
---

- [x] core-390 · Architecture: align service contracts and provider catalog #task #release/v0-4-x #status/closed #view/closed #board/planned #area/architecture #kind/architecture
    <!-- generated:card -->
    **Owner:** marcel  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/board-2026-10-30/w390.md), [proof 2](https://github.com/mcpdev80/baseharbor/commit/dd1923dc), [proof 3](https://github.com/mcpdev80/baseharbor/blob/develop/docs/decisions/0013-standards-first-service-provider-contracts.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.x](../releases/v0.4.x.md)  
**Depends on:** [core-893](core-893-ci-enforce-selected-pr-checks.md), [core-895](core-895-reviews-require-maintainer-approval.md), [core-896](core-896-runners-isolate-parallel-pr-checks.md), [t-20261027-r27-cutover-pr3](t-20261027-r27-cutover-pr3.md)  
**Owner:** marcel  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#390](https://github.com/mcpdev80/baseharbor/issues/390)
<!-- /generated:links -->

## Goal

Complete standards-first service/provider contract alignment before the v0.5 freeze without discarding the working v0.4 capability/provider architecture. The single architecture/freeze prerequisite for standards alignment; feature issues stay responsible for their implementations. Ordering: current v0.4.x correctness/DX → this task → v0.4.31 semantic acceptance → v0.5 freeze. Blocks #175/#298/#300 contract freeze work.

## Scope

- Rule — Standards First: prefer established open standards over proprietary contracts; use de-facto standards where no formal one exists; BaseHarbor-specific contracts define only semantics no standard reasonably covers; extensions are separated, versioned and provider-neutral. Every new service kind/provider documents Existing Standards, Adopted Standards, Deviations, BaseHarbor Extensions and Compatibility Impact before implementation.
- Baseline: JSON Schema 2020-12 (config schemas); Service Binding 1.1 (well-known connection outputs); Crossplane (provider/resource/reconciliation pattern only); Open Service Broker concepts where useful; OCI Image/Distribution (digest-first artifacts); OpenTelemetry/OTLP; OIDC/OAuth; AsyncAPI + CloudEvents; RESP; S3 API (protocol capability, not service identity).
- Model: application intent → service contract → protocol/semantic requirements → provider resolution → provider implementation → product/engine realization. Independent version axes: service contract, provider protocol, provider implementation, product/engine, artifact digest.
- Scope items: freeze provider-neutral service families (sql, key-value database, document database, cache, object-storage, secrets, messaging, vector, observability, identity); keep v0.4 capability IDs compatible until an explicit migration is tested; classify existing capability specs as service contract, protocol/semantic capability or compatibility alias; JSON Schema 2020-12 as canonical schema layer; Service Binding 1.1 outputs `type`, `provider`, `host`, `port`, `uri`, `username`, `password`, `certificates`, `private-key`; BaseHarbor security/lifecycle extensions separate and versioned; Runtime Provider Registry ≠ Provider Catalog; freeze Provider Catalog descriptor metadata (provider id/version, service kinds, contracts/capabilities, product support, platforms, OCI artifact/digest, schema, signature/provenance refs); OCI distribution registry-neutral and digest-first; observability via OTLP; identity via OIDC/OAuth; messaging adopts AsyncAPI/CloudEvents before implementation (#516); `database.key-value/v1` distinct from `cache.key-value/v1` (Valkey reference); `database.document/v1` provider-neutral (MongoDB reference); vector defines only demonstrated common semantics; document compatibility/migration for `object-storage.s3/v1`, `telemetry.otlp/v1`, metrics/logs/traces and other affected specs; conformance/provider SDK checks standards adoption and extension boundaries.
- Runtime/platform extension (implemented via #396, closed): audit OCI Image/Distribution/Runtime, Compose, Kubernetes API, CRI, CNI, CSI, Gateway API, Service Binding and Crossplane patterns with the same five fields.
- Keep: provider-neutral intent; capability → provider → placement; desired/observed/reconcile/verify; Provider Integration Contract; gRPC/Protobuf process boundary; OCI distribution; provider conformance; runtime provider registry ownership/placement; independent provider implementation version; OTLP workload integration.
- Non-goals: no provider marketplace/server; no one-repo-per-provider split before freeze; no dynamic loader for this issue; no Kubernetes-specific application fields; no mass capability-ID rename without compatibility evidence; no product versions in generic service contracts.

## Acceptance

- Development Guidelines contain the permanent Standards First rule.
- Canonical service/provider/binding schemas are JSON Schema 2020-12.
- Service Binding well-known output names are enforced/documented.
- Existing contract migrations are explicit and backwards-compatible where promised.
- Provider Catalog and Runtime Provider Registry are not conflated.
- #210, #363, #516, #170 and the v0.5 freeze/compatibility items reference this architecture.
- Exact-head unit/spec/document validation is green before merge.
- Docker/Podman acceptance only runs if executable runtime behavior changed.
- Compatibility/migration behavior stays intact in executable acceptance.
- A final pre-v0.5 contract review confirms no product-specific service fields leaked into portable intent.

## Required checks

- Exact-head source/spec/docs tests; runtime acceptance only for executable changes.

## Dependencies and file ownership

- Product implementation requires the qualified v0.4.26 PR/review/runner foundation (core-893, core-895, core-896; binding 2026-10-15 correction in [core-888](../epics/core-888-development-and-ci.md)).
- No open task dependencies. Consumed by v0.4.31 and the v0.5.x freeze (core-298, core-300).

## Handoff

- 2026-09-23 progress (branch `fix/runtime-artifact-convergence`): Standards First rule in the guidelines; JSON Schema 2020-12 layout under `contracts/`; provider-neutral service schemas; Service Binding-aligned binding schema with output-name validation; `secure-binding/v1` reduced to security/lifecycle extension semantics; provider descriptor schema with `builtin | oci` distribution; registry vs catalog documented; capability specs classified; ADR 0013 and a standards/gap matrix; pre-release audit requires standards review. Still to prove: exact-head tests, executable compatibility behavior, final pre-v0.5 contract review.
