---
id: t-20261018-r27-delegated-handoff
areas: [delivery]
type: task
release: v0.4.27
version: ""
parent: v0.4.27
priority: high
owner: ""
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-delivery-boundary, t-20261018-r27-stage-versions, t-20261022-r27-ci-delivery]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
early: false
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261018-r27-delegated-handoff · GitOps: preserve external desired state and hand off native changes #task #release/v0-4-27 #status/planned #view/waiting #board/planned #area/delivery #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Waiting for prerequisites**  
    **Needs:** t-20261017-release-0-4-27-updates, [t-20261018-r27-delivery-boundary](t-20261018-r27-delivery-boundary.md), [t-20261018-r27-stage-versions](t-20261018-r27-stage-versions.md), [t-20261022-r27-ci-delivery](t-20261022-r27-ci-delivery.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** t-20261017-release-0-4-27-updates, [t-20261018-r27-delivery-boundary](t-20261018-r27-delivery-boundary.md), [t-20261018-r27-stage-versions](t-20261018-r27-stage-versions.md), [t-20261022-r27-ci-delivery](t-20261022-r27-ci-delivery.md)  
**Required by:** [core-325](core-325-delivery-delegated-deployment-gitops.md), [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261018-r27-public-surfaces](t-20261018-r27-public-surfaces.md), [t-20261018-r27-video-proof](t-20261018-r27-video-proof.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Outcome and acceptance

Preserve existing delegated-delivery boundary: Argo CD/GitOps owns its Git/Helm/Kustomize desired resources and reconciliation. Direct up/repair/destroy/promote cannot race it. Produce or validate an explicit native-manifest/ref change preview for the existing Git/CI workflow, with provenance/correlation and authorization; no automatic commit/push/merge or cluster mutation. Display proposed/submitted/synced/healthy only with actual external evidence; no claim deployment succeeded because a file exists or CI is green. No authority over external secrets or grants, no Baha-to-Baha federation. v0.4.27 proves boundary and fixtures/docs only; live Kubernetes/OpenShift/Argo CD consumer implementation remains core-325 and existing v0.7/v0.8 prerequisites.

## Inputs and output

Consume accepted predecessor interfaces and existing native tools. Deliver the callable bounded production adapter and executable positive/negative tests, not a dormant framework. Use [the standards boundary](../decisions/2026-10-18-r27-native-delivery-and-stages.md); runtime support remains limited to qualified providers.

## Dependencies and file ownership

internal/delivery/handoff.go and owner/render fixtures; corresponding bounded machine read-model tests; no Kubernetes runtime/controller implementation. Paths are reservations confirmed by accepted contract predecessor; shared registrations belong only to public-surfaces, not this slice. No overlapping writes or draft-branch consumers.

## Required checks

Actual direct/delegated operation-owner fixtures including promote/apply/repair/destroy, foreign tracking metadata, external drift and no false READY; Git diff/render fixtures; no K3s runner or fake live Argo acceptance. Actual trusted discovery/executor/fixtures must be accepted in ci-lanes before assignment. Smallest sufficient checks; independent native gates may run on isolated suitable runners. Existing verifier alone permits green-evidence reuse; missing/skip/fail is not PASS. No self-approved coverage or full pre-release run.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planned/unassigned, 2026-10-18. Maintainer requested native standards, real stage/version operation, existing registries/CI/GitOps and a thin promotion operation. No product implementation or release action started.
