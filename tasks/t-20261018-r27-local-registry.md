---
id: t-20261018-r27-local-registry
card_number: "0427-033"
card_short_title: "optionally provision an"
areas: [artifacts]
type: task
release: v0.4.27
version: ""
parent: v0.4.27
priority: normal
owner: coord-welle5 (codex-worker, entlassen)
kanban_lane: closed
kanban_summary: "For topologies that actually need a shared endpoint, explicitly opt into one existing OCI Distribution-compatible registry…"
kanban_status: closed
kanban_title: "0427-033 · optionally provision an"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-registry-access, t-20261022-r27-ci-delivery]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1401]
sources: []
early: false
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1401"]
blocker: ""

---

- [x] t-20261018-r27-local-registry · Artifacts: optionally provision an existing OCI registry implementation #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/artifacts #kind/task
    <!-- generated:card -->
    **Owner:** coord-welle5 (codex-worker, entlassen) · **Priority:** normal  
    **PR:** [baseharbor#1401](https://github.com/mcpdev80/baseharbor/pull/1401)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1401)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-registry-access](t-20261018-r27-registry-access.md), [t-20261022-r27-ci-delivery](t-20261022-r27-ci-delivery.md)  
**Required by:** [t-20261018-r27-docs](t-20261018-r27-docs.md), [t-20261018-r27-video-proof](t-20261018-r27-video-proof.md)  
**Owner:** coord-welle5 (codex-worker, entlassen)  
**Priority:** normal  
**PRs:** [baseharbor#1401](https://github.com/mcpdev80/baseharbor/pull/1401)  
**Source:** 
<!-- /generated:links -->

## Outcome and acceptance

For topologies that actually need a shared endpoint, explicitly opt into one existing OCI Distribution-compatible registry implementation with persisted owned storage, supported native TLS/auth and least privilege. Pin tested upstream image/tool versions during implementation. Show footprint/ports/credentials/retention consequences before setup; never install automatically when a native store/transfer suffices. No registry server/protocol, vendor feature parity or public exposure by default. Repeated setup is idempotent; removal preserves registry data by default and never deletes images referenced by deployments or foreign stores. Explicit unavailable secure capability remains unsupported, never TLS bypass.

## Inputs and output

Consume accepted predecessor interfaces and existing native tools. Deliver the callable bounded production adapter and executable positive/negative tests, not a dormant framework. Use [the standards boundary](../decisions/2026-10-18-r27-native-delivery-and-stages.md); runtime support remains limited to qualified providers.

## Dependencies and file ownership

bounded local-registry setup adapter and native Compose/Quadlet assets/tests, separate from runtime workload assets. Reserved paths for this slice only; proposed filenames are fixed in the accepted contract predecessor before assignment. Shared command/HTTP/MCP/help/golden registrations belong to public-surfaces. If another write owner is needed, coordinate and serialize before implementation; no branch-to-branch dependencies or duplicate state.

## Required checks

Rendered native asset/config/consent/ownership tests and one isolated push/pull/restart persistence smoke; reuse registry-access fixtures; no full app journey. Actual trusted discovery/executor/fixtures must be accepted in ci-lanes before assignment. Smallest sufficient checks; independent native gates may run on isolated suitable runners. Existing verifier alone permits green-evidence reuse; missing/skip/fail is not PASS. No self-approved coverage or full pre-release run.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planned/unassigned, 2026-10-18. Maintainer requested native standards, real stage/version operation, existing registries/CI/GitOps and a thin promotion operation. No product implementation or release action started.
