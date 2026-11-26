---
id: t-20261126-hunt46-never-delivered-proof-leak
card_number: "0428-326"
card_short_title: "consume never-delivered proof"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: w329-0428-326-hunt46-proofleak
kanban_status: review
kanban_lane: review
kanban_summary: "The never-delivered proof at never-delivered/<applicationID>/<environment>.json is created by guided adoption…"
kanban_title: 0428-326 · consume never-delivered proof
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor-plan#133"]
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261126-hunt46-never-delivered-proof-leak · 0428 hunt H-V46: the never-delivered destroy/retire path verifies but never consumes the one-shot proof (medium) #task #release/v0-4-28 #status/review #view/review #kind/task
    <!-- generated:card -->
    **Owner:** w329-0428-326-hunt46-proofleak  
    **PR:** [baseharbor-plan#133](https://github.com/mcpdev80/baseharbor-plan/pull/133)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w329-0428-326-hunt46-proofleak  
**Priority:** not set  
**PRs:** [baseharbor-plan#133](https://github.com/mcpdev80/baseharbor-plan/pull/133)  
**Source:** 
<!-- /generated:links -->

## Goal

The never-delivered proof at `never-delivered/<applicationID>/<environment>.json` is created by guided adoption (`CreateNeverDeliveredProof`, O_EXCL) and consumed by the first successful deployment (`ConsumeNeverDeliveredProof`, `deployment_store.go:562`). On the never-delivered destroy/retire path (`app_runtime_retirement.go:57-86`, `verifyOwnershipWhenNoDeploymentRecord`) the proof is verified but never consumed. An app initialized but destroyed/downed before ever being delivered leaves a stale one-shot witness. This card makes that path consume the proof (and remove a now-empty `never-delivered/<applicationID>` dir) so the O_EXCL collision between the guided adoption flow and the lifecycle destroy flow cannot occur.

## Scope

- In scope:
  - `cmd/baha/app_runtime_retirement.go`: on the never-delivered retire branch, call `deployment.ConsumeNeverDeliveredProof(e.resolved.DeploymentIdentity)` after successful retirement (parallel to the existing `ReleaseApplicationProviderRegistryAt` + `recordApplicationAudit`), and remove a now-empty `never-delivered/<applicationID>` directory.
  - Regression test via the existing `runWithIO` deployment test harness (positive: proof file gone after never-delivered retire; negative: a pre-existing foreign proof keeps the path fail-closed on the verify gate, unchanged).
- Out of scope:
  - The `destroy --all` full-destroy gate: it reuses the app-destroy lifecycle path this card fixes; no separate change (see Dependencies, derivative card 0428-329).
  - The reserved-namespace structural guards (0428-327, 0428-328) — different seams.

## Acceptance

- The never-delivered retire branch consumes the one-shot proof (`ConsumeNeverDeliveredProof` called on the retire path) and removes a now-empty `never-delivered/<applicationID>` directory.
- The existing verify gate (`VerifyNeverDeliveredProof`) still fails closed on an existing runtime / mismatched / corrupt proof; consumption only removes a proof that this lane actually verified as consumed by the same identity.
- Positive regression (proof file absent after never-delivered retire) and negative (foreign proof keeps fail-closed) via the existing `runWithIO` deployment harness.
- Every required test is reachable by a real CI check in the same PR; test registered and mapped in the same PR (Gate Rule). Docker/Podman: n/a (no containers; pure state-file seam).
- Exact source SHA -> test ID -> mapped CI gate -> trigger -> actual run recorded in handoff.

## Dependencies and file ownership

- Owned files or areas: `cmd/baha/app_runtime_retirement.go`, the never-delivered proof harness in `internal/deployment/`.
- Derivative card 0428-329 (BF-46-5) shares this root cause; the `destroy --all` gate is clean by reuse once 0428-326 lands — do not double-fix.
- Shared files: n/a (single-repo seam).

## Handoff

- Current state, branch, PR and evidence links. Newest first.

## Task

Cast from hunt H-V46 (akte evidence/r28-welle6-2026-11-27/bughunt-hv46-state-lifecycle/ on origin/main 62de9bb74, anchor develop 2a141387d; re-verified against develop 384d857b5 at intake). BF-46-2 LIVE. `VerifyNeverDeliveredProof` (internal/deployment/never_delivered_proof.go:72) confirms the never-delivered state before clean retire; on the never-delivered branch of `verifyOwnershipWhenNoDeploymentRecord` (cmd/baha/app_runtime_retirement.go:57-86) the code releases provider registry state and records audit but never calls `deployment.ConsumeNeverDeliveredProof`. `ConsumeNeverDeliveredProof` is only called from `internal/deployment/deployment_store.go:562` (SaveDeploymentRecord) and the test. The proof path (`never_deliveredProofPath`, never_delivered_proof.go:21) is `never-delivered/<applicationID>/<environment>.json`. Consequence: an app initialized but destroyed/downed before delivery leaves a stale one-shot proof; the next adoption with the same identity uses O_EXCL and fails "already exists" — a concrete state-dir race between guided adoption and lifecycle destroy. Fix once in `app_runtime_retirement.go`; the `destroy --all` gate (BF-46-5, 0428-329) is clean by reuse.
