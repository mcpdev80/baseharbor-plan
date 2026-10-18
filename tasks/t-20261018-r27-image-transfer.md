---
id: t-20261018-r27-image-transfer
areas: [artifacts]
type: task
release: v0.4.27
version: ""
parent: v0.4.27
priority: normal
owner: ""
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-ci-lanes, t-20261018-r27-registry-access]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
early: false
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261018-r27-image-transfer · Images: reuse native registry and local-store transports #task #release/v0-4-27 #status/planned #view/waiting #board/planned #area/artifacts #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-ci-lanes](t-20261018-r27-ci-lanes.md), [t-20261018-r27-registry-access](t-20261018-r27-registry-access.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-ci-lanes](t-20261018-r27-ci-lanes.md), [t-20261018-r27-registry-access](t-20261018-r27-registry-access.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261018-r27-artifact-resolution](t-20261018-r27-artifact-resolution.md), [t-20261018-r27-promote](t-20261018-r27-promote.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Outcome and acceptance

Choose registry pull/copy, existing target-native image store, or supported native save/load/OCI layout/archive transfer. Use Docker/Podman/Skopeo or an established OCI library; implement no layer-transfer protocol or private container format. Never assume Docker image ID/config digest equals a registry manifest digest. Record index and selected platform-manifest identity where relevant; verify runtime availability/architecture, digest-preserving copy and supported signatures/referrers policy. Reject silent conversion/rebuild/substitution. No registry required for one-host local use; images on a developer machine are not automatically present on the VM. Bound archives/unpack, interruption cleanup and foreign-image retention. Full disconnected mirror/air-gap products remain core-181.

## Inputs and output

Consume accepted predecessor interfaces and existing native tools. Deliver the callable bounded production adapter and executable positive/negative tests, not a dormant framework. Use [the standards boundary](../decisions/2026-10-18-r27-native-delivery-and-stages.md); runtime support remains limited to qualified providers.

## Dependencies and file ownership

cmd/baha/application_image_transfer.go and matching tests; native transport wrappers only. Paths are reservations confirmed by accepted contract predecessor; shared registrations belong only to public-surfaces, not this slice. No overlapping writes or draft-branch consumers.

## Required checks

Transport selection, hostile/truncated archive, wrong digest/architecture, tag drift, cancellation and non-owned-image fixtures; isolated Docker and Podman load/pull smokes only as affected. Actual trusted discovery/executor/fixtures must be accepted in ci-lanes before assignment. Smallest sufficient checks; independent native gates may run on isolated suitable runners. Existing verifier alone permits green-evidence reuse; missing/skip/fail is not PASS. No self-approved coverage or full pre-release run.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planned/unassigned, 2026-10-18. Maintainer requested native standards, real stage/version operation, existing registries/CI/GitOps and a thin promotion operation. No product implementation or release action started.
