---
id: t-20261018-r27-video-proof
card_number: "0427-061"
card_short_title: "prove real stage versions"
areas: [demo]
type: acceptance
release: v0.4.28
version: ""
parent: v0.4.28
priority: normal
owner: ""
kanban_lane: closed
kanban_summary: "Qualify real-world operation, not a filmed demonstration: same app has three independent release/component versions and…"
kanban_status: closed
kanban_title: "0427-061 · prove real stage versions"
depends_on: [t-20261017-release-0-4-27-updates, t-20261017-release-0-4-28-updates, t-20261018-r27-access-proof, t-20261018-r27-ci-consumption, t-20261018-r27-delegated-handoff, t-20261018-r27-docs, t-20261018-r27-local-parity-proof, t-20261018-r27-local-registry, t-20261018-r27-promote, t-20261018-r27-team-proof, t-20261018-r27-version-view, t-20261022-r27-ci-runtime]
repos: [mcpdev80/baseharbor-demo]
prs: []
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: true
blocker: ""
resolution: dropped
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/decisions/2026-11-14-drop-standalone-stage-proof.md"]
---

- [x] t-20261018-r27-video-proof · Acceptance: prove real stage versions artifacts and promotion #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/demo #kind/acceptance
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Needs:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261018-r27-ci-consumption](t-20261018-r27-ci-consumption.md), [t-20261018-r27-team-proof](t-20261018-r27-team-proof.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/decisions/2026-11-14-drop-standalone-stage-proof.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** dropped  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261018-r27-access-proof](t-20261018-r27-access-proof.md), [t-20261018-r27-ci-consumption](t-20261018-r27-ci-consumption.md), [t-20261018-r27-delegated-handoff](t-20261018-r27-delegated-handoff.md), [t-20261018-r27-docs](t-20261018-r27-docs.md), [t-20261018-r27-local-parity-proof](t-20261018-r27-local-parity-proof.md), [t-20261018-r27-local-registry](t-20261018-r27-local-registry.md), [t-20261018-r27-promote](t-20261018-r27-promote.md), [t-20261018-r27-team-proof](t-20261018-r27-team-proof.md), [t-20261018-r27-version-view](t-20261018-r27-version-view.md), [t-20261022-r27-ci-runtime](t-20261022-r27-ci-runtime.md)  
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

## Explicit scope transfer to v0.4.28 — 2026-11-13

Deferred from v0.4.27 release: broader three-stage/demo acceptance is assigned to v0.4.28. The earlier Connector dependency was removed under the 2026-11-14 public scope decision; use supported Core-owned paths and keep the actual multi-environment acceptance. Current 0.4.27 single-host Core remote workstation proof remains required.

Preserve original card ID/number, prior PR and test history. This is a release-scope move, not acceptance or implementation completion. The Coordinator must inspect current merged Core code, first-party provider contracts, real selected CI, and the existing task before dispatch; Codex independently reviews/merges. Release v0.4.27 cannot claim the deferred feature as complete.

## Owner scope decision — 2026-11-14

The Owner removed this standalone video/stage-proof card from release scope. It is dropped, not accepted; its historical context remains. This does not remove acceptance requirements independently owned by other active cards.
