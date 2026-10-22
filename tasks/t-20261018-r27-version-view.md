---
id: t-20261018-r27-version-view
areas: [cli]
type: task
release: v0.4.27
version: ""
parent: v0.4.27
priority: normal
owner: ""
depends_on: [t-20261017-release-0-4-27-updates, t-20261022-r27-ci-delivery, t-20261018-r27-registry-access, t-20261018-r27-stage-versions]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
early: false
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261018-r27-version-view · Versions: show release components source and running state #task #release/v0-4-27 #status/planned #view/waiting #board/planned #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-ci-delivery](t-20261022-r27-ci-delivery.md), [t-20261018-r27-registry-access](t-20261018-r27-registry-access.md), [t-20261018-r27-stage-versions](t-20261018-r27-stage-versions.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-ci-delivery](t-20261022-r27-ci-delivery.md), [t-20261018-r27-registry-access](t-20261018-r27-registry-access.md), [t-20261018-r27-stage-versions](t-20261018-r27-stage-versions.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261018-r27-public-surfaces](t-20261018-r27-public-surfaces.md), [t-20261018-r27-video-proof](t-20261018-r27-video-proof.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Outcome and acceptance

Readable release names/tags and component versions are the primary UI. Show each app/service image repository/tag, resolved digest (detail/JSON), index/platform identity, app contract revision, per-component Git source/revision when evidenced, build/CI link when supplied, intended/applied/observed versions and actual container/unit/resource identities with observation freshness. Prefer OCI image.version/source/revision/title annotations and existing release manifests/Compose/Helm metadata; no invented mandatory release index or assuming matching component tags define a release. Metadata is a claim, not verified provenance: distinguish verified/unverified/unknown and never infer Git commit from tag. Query configured authorized sources only; version listing is not an unrestricted registry catalog. No per-stage state sharing or mutating inspection.

## Inputs and output

Consume accepted predecessor interfaces and existing native tools. Deliver the callable bounded production adapter and executable positive/negative tests, not a dormant framework. Use [the standards boundary](../decisions/2026-10-18-r27-native-delivery-and-stages.md); runtime support remains limited to qualified providers.

## Dependencies and file ownership

cmd/baha/app_release_show.go and internal/machinereadmodels/release.go with matching tests; no app_context.go writes. Paths are reservations confirmed by accepted contract predecessor; shared registrations belong only to public-surfaces, not this slice. No overlapping writes or draft-branch consumers.

## Required checks

Read-only API/collector/CLI presentation fixtures for multi-image releases, image-only/dirty/missing Git, tag drift, stale/offline observations, misleading annotations, platform indexes and bounded denied listings. Actual trusted discovery/executor/fixtures must be accepted in ci-lanes before assignment. Smallest sufficient checks; independent native gates may run on isolated suitable runners. Existing verifier alone permits green-evidence reuse; missing/skip/fail is not PASS. No self-approved coverage or full pre-release run.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planned/unassigned, 2026-10-18. Maintainer requested native standards, real stage/version operation, existing registries/CI/GitOps and a thin promotion operation. No product implementation or release action started.
