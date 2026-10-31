---
id: t-20261018-r27-candidate-contract
areas: [architecture]
type: architecture
release: v0.4.27
version: ""
parent: core-777
priority: critical
owner: ""
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-authority-contract, t-20261018-r27-delivery-boundary]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261018-r27-candidate-contract · Deployment: define immutable source and image submission #task #release/v0-4-27 #status/planned #view/waiting #board/planned #area/architecture #kind/architecture
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** critical  
    **Waiting for prerequisites**  
    **Needs:** t-20261017-release-0-4-27-updates, [t-20261018-r27-authority-contract](t-20261018-r27-authority-contract.md), [t-20261018-r27-delivery-boundary](t-20261018-r27-delivery-boundary.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** t-20261017-release-0-4-27-updates, [t-20261018-r27-authority-contract](t-20261018-r27-authority-contract.md), [t-20261018-r27-delivery-boundary](t-20261018-r27-delivery-boundary.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261018-r27-app-binding](t-20261018-r27-app-binding.md), [t-20261018-r27-candidate-pack](t-20261018-r27-candidate-pack.md), [t-20261018-r27-registry-access](t-20261018-r27-registry-access.md), [t-20261018-r27-stage-versions](t-20261018-r27-stage-versions.md), [t-20261022-r27-ci-delivery](t-20261022-r27-ci-delivery.md)  
**Owner:** unassigned  
**Priority:** critical  
**PRs:** none  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Define only the minimal Baha app/target/consent binding around existing Git revisions, OCI images/artifacts/layouts and native Compose/Quadlet (later Helm/Kustomize/Kubernetes) release inputs. A candidate is an exact submission, not a proprietary compulsory bundle, catalog, archive protocol or new lifecycle service. Readable release/component versions map to actual artifact references; Git revision may be unknown or absent and OCI annotations alone are not verified provenance. Root/complete environment contracts remain existing intent authority; no stage DSL. Separate local source build from consumption of an existing CI-produced release: release consumption/promote never builds. Adopt native build context/archive/registry APIs and feature-detect versions; bound paths/symlinks/bytes/credentials using existing owners. Builder, runtime, capability and delivery remain separate. Direct versus externally reconciled delivery is explicit; native lifecycle differences/downtime and application-owned schema migrations are stated without false atomicity/rollback guarantees.

Make the migration responsibility boundary normative in the product specification and DE counterpart, with input/negative fixtures: the application or its existing migration tool owns schema changes and compatibility evidence; Baha checks only the applicable declared prerequisites it can actually verify. Missing required evidence blocks that applicable operation; a backup never proves schema compatibility, and an image rollback never implies database rollback. Do not imply automatic compatibility inference, migration execution or a generic migration engine. Define the minimal extension of existing environment-keyed deployment release/configuration records for stage-versions; reuse existing source/applied/observed fields instead of inventing a new stage axis.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

Existing product specifications for application/artifact/delivery boundaries plus DE counterparts; minimal existing internal/delivery/application input records/fixtures as required after accepted standards mapping. Replace the earlier reservation for a standalone contracts/deploymentcandidate/v1 protocol: it is not an authorization to create a mandatory new package format. Shared indexes remain public-surfaces/docs. No generic format/engine without a separately reviewed demonstrated gap.
## Required checks

Record/golden validation; malformed/digest/path/secret-reference fixtures; docs/EN-DE only. Use existing trusted contract/docs/package checks for this prerequisite; acceptance must not wait on downstream ci-lanes. Any genuinely missing contract-check route is resolved explicitly before assignment, without self-exemption. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.
