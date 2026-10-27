---
id: t-20261027-r27-shadow-run
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
priority: critical
owner: coordinator-lane
depends_on: [t-20261017-release-0-4-27-updates, t-20261022-r27-evidence-contract, t-20261022-r27-evidence-publisher, t-20261022-r27-evidence-verifier, t-20261024-r27-ci-impact-prototype]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1092, mcpdev80/baseharbor#1105, mcpdev80/baseharbor#1107, mcpdev80/baseharbor#1111]
sources: []
blocker: "Owner gaps G1-G6 (OWNER-REVIEW-2026-10-27.md); closure lanes ci1/f3/f4 dispatched on v2 base 38771771; re-qualification through legacy CI required before merge/activation."
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-ci-replacement-2026-10-26/"]
---

- [ ] t-20261027-r27-shadow-run · Prove one automatic contributor receipt chain #task #release/v0-4-27 #status/blocked #view/blocked #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** coordinator-lane · **Priority:** critical  
    **PR:** [baseharbor#1092](https://github.com/mcpdev80/baseharbor/pull/1092), [baseharbor#1105](https://github.com/mcpdev80/baseharbor/pull/1105), [baseharbor#1107](https://github.com/mcpdev80/baseharbor/pull/1107), [baseharbor#1111](https://github.com/mcpdev80/baseharbor/pull/1111)  
    **Blocker:** Owner gaps G1-G6 (OWNER-REVIEW-2026-10-27.md); closure lanes ci1/f3/f4 dispatched on v2 base 38771771; re-qualification through legacy CI required before merge/activation.  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-evidence-publisher](t-20261022-r27-evidence-publisher.md), [t-20261022-r27-evidence-verifier](t-20261022-r27-evidence-verifier.md), [t-20261024-r27-ci-impact-prototype](t-20261024-r27-ci-impact-prototype.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-ci-replacement-2026-10-26/)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-evidence-contract](t-20261022-r27-evidence-contract.md), [t-20261022-r27-evidence-publisher](t-20261022-r27-evidence-publisher.md), [t-20261022-r27-evidence-verifier](t-20261022-r27-evidence-verifier.md), [t-20261024-r27-ci-impact-prototype](t-20261024-r27-ci-impact-prototype.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261022-r27-evidence-acceptance](t-20261022-r27-evidence-acceptance.md), [t-20261027-r27-cutover-pr3](t-20261027-r27-cutover-pr3.md)  
**Owner:** coordinator-lane  
**Priority:** critical  
**PRs:** [baseharbor#1092](https://github.com/mcpdev80/baseharbor/pull/1092), [baseharbor#1105](https://github.com/mcpdev80/baseharbor/pull/1105), [baseharbor#1107](https://github.com/mcpdev80/baseharbor/pull/1107), [baseharbor#1111](https://github.com/mcpdev80/baseharbor/pull/1111)  
**Source:** 
<!-- /generated:links -->

# Prove one automatic contributor receipt chain

**Concrete blockers (2026-10-27):** integrated candidate baseharbor#1111 (SHA `ad4d0f28`) under independent review lane rv1; hosted positive chain additionally requires Owner provisioning of `PLANNING_RECEIPT_WRITE_TOKEN`.

**Superseded input:** rv1 `ACCEPT_WITH_NONBLOCKING` was too optimistic per owner review (see evidence/r27-ci-replacement-2026-10-26/OWNER-REVIEW-2026-10-27.md).

## Reopened acceptance boundary
The earlier z19 record demonstrated a successful producer, actual Owner action and offline-valid receipt with manual assistance. Those events remain real historical evidence. The automatic/no-manual-evidence skeleton is reopened by the current Owner audit: post-run/shadow are dormant and approval publication was manual. No receipt file or old run is erased or relabelled.

## Entry conditions
W1/W2/W3 corrections integrated, existing legacy CI actually runs the relevant suites, trusted workflow registration exists on default main with fixed helper source, Planning credential/publication permissions verified, and pause explicitly lifted. Missing rights/source registration is a blocker, not a patch workaround.

## One sufficient proof
One ordinary contributor PR produces a genuine successful public-contracts run. Actual trusted post-run automatically derives/publishes plan, receipt and task evidence reference. Owner makes only the decision; the approval commit publishes automatically; retained-only shadow consumption succeeds afterwards on exact published inputs with full history. Neither skipped/echoed jobs, manual replay, a local commit nor patch download/git am counts.

## Negative proof and review
Run the production verifier with wrong SHA, genuinely dead run ID and edited controlled receipt/history; require the intended rejection, not an unrelated network/tool failure. Do not alter real approved evidence. The positive retained case succeeds with origin API forbidden. Another worker/coordinator reviews the final integrated SHA and automatic result/link publication.

## Completion
Attach automatically produced exact source/run/commit/task links and actual outcomes. Only then may coordinator mark this card accepted. Keep summary at most checked / validly reused / not required with reason. PR3 remains blocked until the separate final acceptance card is accepted.

## Fixed deadline
T0 remains 2026-10-26T23:35:50Z; deadline 2026-10-29T23:35:50Z. Prior manual success does not satisfy this deadline's automatic criterion. No silent extension.

## Governing order and preserved history

The sole execution order is [CODEMAN-START.md](../evidence/r27-ci-replacement-2026-10-26/CODEMAN-START.md). Codeman remains paused until explicit Owner restart. Existing owner strings/commits are preserved; coordinator reconciles local checkpoints before assigning the three slots. [Pre-reset task, scope and results](https://github.com/mcpdev80/baseharbor-plan/blob/5df54047097107808e92ba4fe1bb2a8197f8772a/tasks/t-20261027-r27-shadow-run.md) remain immutable history, not competing operational instructions.
