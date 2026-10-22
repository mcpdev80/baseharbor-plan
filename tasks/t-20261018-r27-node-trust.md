---
id: t-20261018-r27-node-trust
areas: [connector]
type: task
release: v0.4.27
version: ""
parent: v0.4.27
priority: normal
owner: ""
depends_on: [t-20261017-release-0-4-27-updates, t-20261022-r27-ci-runtime, t-20261018-r27-node-service]
repos: [mcpdev80/baseharbor-node-connector]
prs: []
sources: ["mcpdev80/baseharbor-node-connector#3"]
aliases: []
early: false
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261018-r27-node-trust · Connector: qualify rotation revocation and session recovery #task #release/v0-4-27 #status/planned #view/waiting #board/planned #area/connector #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-ci-lanes](t-20261018-r27-ci-lanes.md), [t-20261018-r27-node-service](t-20261018-r27-node-service.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-ci-lanes](t-20261018-r27-ci-lanes.md), [t-20261018-r27-node-service](t-20261018-r27-node-service.md)  
**Required by:** [nc-3](nc-3-core-enrollment-remote-runtime-acceptance.md), [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261018-r27-node-cli](t-20261018-r27-node-cli.md), [t-20261018-r27-node-streams](t-20261018-r27-node-streams.md), [t-20261018-r27-remote-material](t-20261018-r27-remote-material.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** [baseharbor-node-connector#3](https://github.com/mcpdev80/baseharbor-node-connector/issues/3)
<!-- /generated:links -->

## Outcome and acceptance

Reconcile existing implementation, then close actual token/mTLS/CA overlap/revocation/reconnect gaps against immutable Core contract. Scope/version/capabilities checked after auth; durable admission and no ambiguous mutation replay. Core unavailable preserves target runtime; wrong peer/tenant/runtime and revoked sessions fail closed.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

Connector internal/targetaccess/session*.go enrollment renewal/trust files and internal/connector/outbound*.go; no install.go writes. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

Focused trust/session race tests and bounded real Core/Connector rotation+reconnect gate; not a full app journey. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.
