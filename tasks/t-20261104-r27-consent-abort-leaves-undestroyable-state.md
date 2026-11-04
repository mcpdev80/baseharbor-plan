---
id: t-20261104-r27-consent-abort-leaves-undestroyable-state
areas: [deployment]
type: bug
release: v0.4.27
version: ""
parent: core-777
priority: critical
owner: coord-welle4 (lane w120)
kanban_lane: active
kanban_summary: An app apply that is refused by the candidate-consent gate (missing or wrong --confirm-candidate digest) must leave NO state…
kanban_status: active
kanban_title: "Deployment: refused candidate apply must leave destroyable state"
depends_on: [t-20261017-release-0-4-27-updates, t-20261018-r27-candidate-contract]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#777"]
aliases: []
early: false
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261104-r27-consent-abort-leaves-undestroyable-state · Deployment: refused candidate apply must leave destroyable state #task #release/v0-4-27 #status/active #view/active #area/deployment #kind/bug
    <!-- generated:card -->
    **Owner:** coord-welle4 (lane w120) · **Priority:** critical  
    <!-- /generated:card -->

<!-- w120 fix (2026-11-04): refused candidate apply now fails closed before any on-disk record write; prior record survives so `destroy` re-resolves and a consented re-apply reaches the choke point and READY. Fix committed `c24a6c7c` on `w120-fix`; draft PR #1375 (base develop). Owner redirect to non-draft for gate run; CODEX-MERGE on owner approval. Evidence: baseharbor-plan/evidence/r27-welle4-2026-11-04/consent-abort/slice-1.md -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Parent:** [core-777](../epics/core-777-developer-access-and-profiles.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261018-r27-candidate-contract](t-20261018-r27-candidate-contract.md)  
**Owner:** coord-welle4 (lane w120)  
**Priority:** critical  
**PRs:** none  
**Source:** [baseharbor#777](https://github.com/mcpdev80/baseharbor/issues/777)
<!-- /generated:links -->

## Outcome and acceptance

An `app apply` that is refused by the candidate-consent gate (missing or wrong `--confirm-candidate` digest) must leave NO state that blocks later operations: `app destroy` on the same environment must succeed, and a follow-up apply with valid consent must reach READY without manual cleanup. Today the refusal leaves an incomplete `deployment.json` (observed identity d9ba7200 in lane evidence) whose network lacks an owner; `destroy --yes` fails and the environment is unrecoverable. Fail-closed means "refuse without trace", not "refuse and corrupt".

## Inputs and output

Input: consent gate in `cmd/baha` apply lifecycle (candidate contract, accepted design: record-before-mutation with consent check). Output: the refusal path either writes nothing or writes a record destroy fully understands, plus executable regression: refused apply -> destroy succeeds -> consented apply reaches READY.

## Dependencies and file ownership

cmd/baha apply/record path and destroy path; internal/deployment store as needed. Same files as the candidate contract branch touched — sequence AFTER t-20261018-r27-candidate-contract merges to avoid write-set collision.

## Required checks

Focused cmd/baha + internal/deployment tests, red-first from the lane reproduction; wizard/lifecycle hosted gates must stay green; no new CI surface.

## Standards boundary

No bypass or weakening of the consent gate; the digest remains bound to the canonical submission fingerprint (candidate contract v1).

## Handoff

Raised 2026-11-04 by coordinator from lane w80 finding (evidence: baseharbor-plan/evidence/r27-welle3-2026-11-03/candidate-contract/harness-consent-1.md + w80 END/QUESTION line with rest-object id). Candidate contract's lifecycle gates are unblocked for CI via harness isolation (throwaway XDG per refused-capture); this card carries the product-side truth.
