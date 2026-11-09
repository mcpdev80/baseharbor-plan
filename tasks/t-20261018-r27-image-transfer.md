---
id: t-20261018-r27-image-transfer
card_number: "0427-030"
card_short_title: "reuse native registry and"
areas: [artifacts]
type: task
release: v0.4.27
version: ""
parent: v0.4.27
priority: high
owner: coord-welle5 (w245-codex, entlassen)
kanban_lane: closed
kanban_summary: "Choose registry pull/copy, existing target-native image store, or supported native save/load/OCI layout/archive transfer. Use…"
kanban_status: closed
kanban_title: "0427-030 · reuse native registry and"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-registry-access, t-20261022-r27-ci-delivery]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1402]
sources: []
early: false
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1402", "https://github.com/mcpdev80/baseharbor/commit/5e4fde7177ea020de39b117f6d89cfa8f7c62be2", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-2026-11-06/image-transfer/act-1402f.md"]
---

- [x] t-20261018-r27-image-transfer · Images: reuse native registry and local-store transports #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/artifacts #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle5 (w245-codex, entlassen) · **Priority:** high  
    **PR:** [baseharbor#1402](https://github.com/mcpdev80/baseharbor/pull/1402)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1402), [proof 2](https://github.com/mcpdev80/baseharbor/commit/5e4fde7177ea020de39b117f6d89cfa8f7c62be2), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-2026-11-06/image-transfer/act-1402f.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.27  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-registry-access](t-20261018-r27-registry-access.md), [t-20261022-r27-ci-delivery](t-20261022-r27-ci-delivery.md)  
**Required by:** [t-20261018-r27-artifact-resolution](t-20261018-r27-artifact-resolution.md), [t-20261018-r27-promote](t-20261018-r27-promote.md)  
**Owner:** coord-welle5 (w245-codex, entlassen)  
**Priority:** high  
**PRs:** [baseharbor#1402](https://github.com/mcpdev80/baseharbor/pull/1402)  
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

Merged 2026-11-06: PR #1402 candidate `1c024d11bd6d0c82062902b7066305bf1d582be5` was independently accepted in act-1402f and squash-merged to `develop` as `5e4fde7177ea020de39b117f6d89cfa8f7c62be2`. Run 42226452453 completed successfully; `PR Selected Checks` from integration 15368 passed. Adapter source and test blobs match the accepted candidate. No release or deployment was performed.
