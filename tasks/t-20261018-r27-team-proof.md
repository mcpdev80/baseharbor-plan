---
id: t-20261018-r27-team-proof
card_number: "0427-059"
card_short_title: "prove two workstations share"
areas: [acceptance]
type: acceptance
release: v0.4.28
version: ""
parent: v0.4.28
priority: normal
owner: worker-059-teamproof
kanban_lane: active
wait_reason: ""
kanban_summary: "Two isolated homes/checkouts attach one app on Docker VM; A changes, B sees same IDs and current revision. Race same…"
kanban_status: active
kanban_title: "0427-059 · prove two workstations share"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-maintenance-client, t-20261018-r27-public-surfaces, t-20261018-r27-stage-versions, t-20261018-r27-state-recovery, t-20261022-r27-ci-access]
repos: [mcpdev80/baseharbor-demo]
prs: []
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: true
blocker: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-15/team-proof/round-1.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-15/mission-rev-relay/act-059-review-r1.md"]
---

- [ ] t-20261018-r27-team-proof · Acceptance: prove two workstations share one authoritative deployment #task #release/v0-4-28 #status/active #view/active #area/acceptance #kind/acceptance
    <!-- generated:card -->
    **Owner:** worker-059-teamproof · **Priority:** normal  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-15/team-proof/round-1.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-15/mission-rev-relay/act-059-review-r1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-maintenance-client](t-20261018-r27-maintenance-client.md), [t-20261018-r27-public-surfaces](t-20261018-r27-public-surfaces.md), [t-20261018-r27-stage-versions](t-20261018-r27-stage-versions.md), [t-20261018-r27-state-recovery](t-20261018-r27-state-recovery.md), [t-20261022-r27-ci-access](t-20261022-r27-ci-access.md)  
**Required by:** [console-2](console-2-live-core-adapter-workflow-proofs.md), [t-20261018-r27-video-proof](t-20261018-r27-video-proof.md)  
**Owner:** worker-059-teamproof  
**Priority:** normal  
**PRs:** none  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

Two isolated homes/checkouts attach one app on Docker VM; A changes, B sees same IDs and current revision. Race same deployment/shared provider; stale approval rejected. Lost response and management restart preserve operation/result without duplicate mutation. Revoking A preserves B; private target secrets stay off clients. Different installation/equal aliases deny cross-boundary access.

## Inputs and output

Use only accepted predecessor interfaces and the existing authorities identified in [the release plan](../releases/v0.4.27.md). Output: the callable production path described above plus executable positive/negative regressions; a standalone unused adapter is not complete. Refresh actual remote SHAs before implementation.

## Dependencies and file ownership

Demo tests/team-authority/ independent two-client fixture and scripts only. These are bounded write reservations, not assertions that proposed files already exist. New interface/type paths are fixed by the contract predecessor before assignment. Never edit another slice's files or use its draft branch. Shared indexes/registrations belong only to `t-20261018-r27-public-surfaces` (documentation navigation belongs to the docs task). If an additional shared write is necessary, update dependencies/ownership before work; do not reconcile competing copies later.

## Required checks

One bounded two-client Docker integration; API/filesystem negatives elsewhere reused only with exact compatible inputs. Predecessor CI readiness must identify actual selected test commands, discovery and native fixtures before assignment. Owner implements, runs sufficient selected checks, diagnoses real failures and hands off exact-SHA evidence; no self-qualification or automatic full matrix. Reuse green evidence only through the existing verifier; failed/skipped/missing requirements remain open.

## Standards boundary

[Native delivery and stages](../decisions/2026-10-18-r27-native-delivery-and-stages.md) constrains this slice: reuse native tools/owners, no private release/registry/build/pipeline/controller framework; no default CI or GitOps prerequisite for local work. Runtime-specific unsupported behavior remains explicit.

## Handoff

Planning only, 2026-10-18. Unassigned; no product changes, acceptance, native run, merge or release authorized by this note. Product implementation starts after release startup prerequisites and Maintainer assignment. Preserve current v0.4.26 work and historical consumer PR commits.

## Reopened for acceptance gap — 2026-11-21

The prior review accepted the two-home evidence, but the stated acceptance requires both homes to attach the same application and observe its current revision after a change. The current `TestClientCommandsTwoHomesSameDeploymentPrecedence` calls `app init` independently and explicitly only asserts that each home receives a server-assigned ID; it does not assert equal IDs or revision visibility. The Docker witness also records two distinct IDs and says there is no ID sharing. Therefore the old evidence does not establish this acceptance, and the prior closure is withdrawn pending a real shared-app attachment test and exact gate evidence.

## Release boundary decision — 2026-11-13

Two concurrent independent workstation sessions, revocation isolation and multi-user authority stress acceptance move to v0.4.28. v0.4.27 still requires real single-workstation authenticated management, ownership and denial proof.

No implementation/acceptance is inferred; original stable card_number remains unchanged. Complete this through the normal v0.4.28 Coordinator/Worker/Codex merge process and current native tests.
