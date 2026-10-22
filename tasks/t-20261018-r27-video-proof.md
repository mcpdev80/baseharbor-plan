---
id: t-20261018-r27-video-proof
areas: [demo]
type: acceptance
release: v0.4.27
version: ""
parent: v0.4.27
priority: normal
owner: ""
depends_on: [nc-3, t-20261017-release-0-4-27-updates, t-20261018-r27-access-proof, t-20261018-r27-ci-consumption, t-20261018-r27-delegated-handoff, t-20261018-r27-docs, t-20261018-r27-local-parity-proof, t-20261018-r27-local-registry, t-20261018-r27-promote, t-20261018-r27-team-proof, t-20261018-r27-version-view, t-20261022-r27-ci-runtime]
repos: [mcpdev80/baseharbor-demo]
prs: []
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261018-r27-video-proof · Acceptance: prove real stage versions artifacts and promotion #task #release/v0-4-27 #status/planned #view/waiting #board/planned #area/demo #kind/acceptance
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Waiting for prerequisites**  
    **Needs:** [nc-3](nc-3-core-enrollment-remote-runtime-acceptance.md), [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-access-proof](t-20261018-r27-access-proof.md), [t-20261018-r27-ci-consumption](t-20261018-r27-ci-consumption.md), [t-20261018-r27-delegated-handoff](t-20261018-r27-delegated-handoff.md), [t-20261018-r27-docs](t-20261018-r27-docs.md), [t-20261018-r27-local-parity-proof](t-20261018-r27-local-parity-proof.md), [t-20261018-r27-local-registry](t-20261018-r27-local-registry.md), [t-20261018-r27-promote](t-20261018-r27-promote.md), [t-20261018-r27-team-proof](t-20261018-r27-team-proof.md), [t-20261018-r27-version-view](t-20261018-r27-version-view.md), [t-20261022-r27-ci-runtime](t-20261022-r27-ci-runtime.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [nc-3](nc-3-core-enrollment-remote-runtime-acceptance.md), [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-access-proof](t-20261018-r27-access-proof.md), [t-20261018-r27-ci-consumption](t-20261018-r27-ci-consumption.md), [t-20261018-r27-delegated-handoff](t-20261018-r27-delegated-handoff.md), [t-20261018-r27-docs](t-20261018-r27-docs.md), [t-20261018-r27-local-parity-proof](t-20261018-r27-local-parity-proof.md), [t-20261018-r27-local-registry](t-20261018-r27-local-registry.md), [t-20261018-r27-promote](t-20261018-r27-promote.md), [t-20261018-r27-team-proof](t-20261018-r27-team-proof.md), [t-20261018-r27-version-view](t-20261018-r27-version-view.md), [t-20261022-r27-ci-runtime](t-20261022-r27-ci-runtime.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Qualify real-world operation, not a filmed demonstration: same app has three independent release/component versions and configurations across environments, including two environments on one Target and multiple Targets; updating/promoting one preserves the others. Exercise enterprise/private registry auth+CA, no-registry native store/transfer and an explicitly optional local registry. Verify readable version/source/component inventory, exact runtime image identities, destination-only SQL/cache bindings/data, provider ownership and actual reachable HTTPS. Use existing direct native delivery; external GitOps is boundary/fixture evidence only until core-325. CI examples consume a produced release without rebuild; schema-migration limits and rollback implications are explicit. Reuse team/local/remote proofs instead of repeating all journeys. The one-checkout multi-terminal video is an optional presentation of qualified operation; recording/browser choreography never blocks product release and grants no K3s/production support claim.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

Demo bounded stage/artifact/promotion acceptance fixture/scripts and one optional recording runbook, separate from existing Docker/Podman/team gate scripts. No product feature flags or production rollout policy. Preserve this stable ID despite the former video-only title; source-level requirement is now explicitly real operation.
## Required checks

Reuse authenticated unchanged team/local/Docker/Podman/registry receipts only through the existing verifier. Add missing three-version/promotion/data-isolation coverage with deterministic integration first, then the smallest native changed-stage check. No extra full matrix, public recording, K3s job or production deployment. Missing/failed/unknown evidence stays open.
## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.
