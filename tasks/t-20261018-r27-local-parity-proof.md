---
id: t-20261018-r27-local-parity-proof
card_number: "0427-032"
card_short_title: "prove unchanged no-login local"
areas: [acceptance]
type: acceptance
release: v0.4.27
version: ""
parent: v0.4.27
priority: normal
owner: cg-s3
kanban_lane: blocked
kanban_summary: Same init/up/status semantics on local Docker and Podman without login/server/bundle; no compulsory services beyond…
kanban_status: blocked
kanban_title: "0427-032 · prove unchanged no-login local"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-public-surfaces, t-20261022-r27-ci-authority]
repos: [mcpdev80/baseharbor-demo]
prs: []
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: "Canonical local acceptance test contradicts its own fixture and current local-owner/consent semantics; local API/direct-owner same-state race proof is missing."
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/v0.4.27-local-parity-0427-032-2026-11-13.md"]
---

- [ ] t-20261018-r27-local-parity-proof · Acceptance: prove unchanged no-login local operation #task #release/v0-4-27 #status/blocked #view/blocked #area/acceptance #kind/acceptance
    <!-- generated:card -->
    **Owner:** cg-s3 · **Priority:** normal  
    **Blocker:** Canonical local acceptance test contradicts its own fixture and current local-owner/consent semantics; local API/direct-owner same-state race proof is missing.  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/v0.4.27-local-parity-0427-032-2026-11-13.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-public-surfaces](t-20261018-r27-public-surfaces.md), [t-20261022-r27-ci-authority](t-20261022-r27-ci-authority.md)  
**Required by:** [t-20261018-r27-video-proof](t-20261018-r27-video-proof.md)  
**Owner:** cg-s3  
**Priority:** normal  
**PRs:** none  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Same init/up/status semantics on local Docker and Podman without login/server/bundle; no compulsory services beyond requirements. Existing Git auth/checkouts unchanged. Prove local API/direct owner cannot race over same state; collect actual IDs, consumers and cleanup evidence.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

Demo tests/local-authority-parity/ bounded fixture and test scripts only. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

Reuse unaffected verifier-valid local gates; run only changed owner/dispatch cases plus bounded Docker/Podman local smokes. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.

2026-11-13: Claimed as `cg-s3` on Maintainer instruction and tested Core develop `1cbfaefe24e19ed6110a0cc68eb8b9b869880e52` on the supplied rootless Docker and Podman VMs. The unchanged `TestCorelessFreshWorkloadRuntimeLifecycle` fails on both before runtime use because `configureTestTarget` registers an installation and the next assertion requires it absent. Temporary test-only diagnostics passed local `app init/plan/up/status/doctor` on both runtimes without a running Core server, but this does not qualify the unchanged test or prove the required local API/direct-owner race. Full commands, outcomes, and verified cleanup are in [the native VM report](../evidence/v0.4.27-local-parity-0427-032-2026-11-13.md). Blocked pending a canonical test that matches the card's local-authority boundary, current consent behavior, cleanup assertions, and same-state concurrency proof. No product checkout was edited.
