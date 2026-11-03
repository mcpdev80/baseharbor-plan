---
id: t-20261018-r27-state-owner
areas: [state]
type: task
release: v0.4.27
version: ""
parent: core-777
priority: high
owner: w2-state-owner
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-authority-contract, t-20261022-r27-ci-authority]
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1347"]
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261018-r27-state-owner · State: enforce installation-owned deployment storage #task #release/v0-4-27 #status/review #view/review #area/state #kind/task
    <!-- generated:card -->
    **Owner:** w2-state-owner · **Priority:** high  
    **PR:** [baseharbor#1347](https://github.com/mcpdev80/baseharbor/pull/1347)  
    **Needs:** [t-20261018-r27-authority-contract](t-20261018-r27-authority-contract.md), [t-20261022-r27-ci-authority](t-20261022-r27-ci-authority.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-authority-contract](t-20261018-r27-authority-contract.md), [t-20261022-r27-ci-authority](t-20261022-r27-ci-authority.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261018-r27-app-binding](t-20261018-r27-app-binding.md), [t-20261018-r27-management-host](t-20261018-r27-management-host.md), [t-20261018-r27-mutation-lock](t-20261018-r27-mutation-lock.md), [t-20261018-r27-stage-versions](t-20261018-r27-stage-versions.md), [t-20261018-r27-state-recovery](t-20261018-r27-state-recovery.md)  
**Owner:** w2-state-owner  
**Priority:** high  
**PRs:** [baseharbor#1347](https://github.com/mcpdev80/baseharbor/pull/1347)  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Bind existing deployment/provider state to the selected installation and server-owned durable root. Workstation paths are cache/source hints only. Local and server execution resolve the same owner; reject foreign/missing/corrupt installation state and copied caches. Reuse existing state format/owner rather than a second state database.

Preserve the existing deployment identity (application ID + Target + environment), DeploymentSource and applied/observed records. Deliver the accepted owner-scoped read/write seam for later release-selection extensions, including isolation and serialization tests. Environment already exists; do not introduce a second stage identity, new coreinstallation state model or another database. This task owns storage authority, not the downstream version/configuration implementation.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

internal/deployment/deployment_store.go; cmd/baha/app_context.go; cmd/baha/deployment_record.go; matching state-owner tests. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

Focused deployment/context tests using two isolated homes, foreign identity and corrupt-state fixtures; no runtime. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.

### Handoff (2026-11-03, coordinator)

Candidate: PR #1347 head cdfc75bf (branch work/r27-state-owner, base develop, stacked note present);
duplicate #1340 closed with supersession proof. Review pending on windows-compile + production-consumer
points of review-1326b; state-owner content itself delivered by the earlier lane round.

### Coordinator note on installation-ID binding (2026-11-03, s2 round)

Same-target installation identity binding is deferred to the authority contract surfaces
(internal/installauthority plus serviceaccess issuer identity), where the durable installation ID
already lives; this card consumes it at its Load/Save seams once that lands. Recorded per s2 END.

### Coordinator acceptance note (2026-11-03, r1347i)

CODEX-REVIEW verdict on head 33badf7d: **ACCEPT-WITH-DEFERRAL** (evidence/r27-night-2026-11-02/review-1347i.md).
Deferrals as noted on this and the authority card (same-target installation-ID binding lives
on these seams once authority-contract lands). Merge via CODEX-MERGE in flight; closes on proof.
