---
id: t-20261022-r27-evidence-resolver
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
priority: high
owner: "w2-lane (post-run + task link, dormant PR2)"
depends_on: [t-20261017-release-0-4-27-updates, t-20261022-r27-evidence-contract]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1090, mcpdev80/baseharbor#1048]
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261022-r27-evidence-resolver · evidence resolver #task #release/v0-4-27 #status/active #view/active #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** w2-lane (post-run + task link, dormant PR2) · **Priority:** high  
    **PR:** [baseharbor#1090](https://github.com/mcpdev80/baseharbor/pull/1090), [baseharbor#1048](https://github.com/mcpdev80/baseharbor/pull/1048)  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-evidence-contract](t-20261022-r27-evidence-contract.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-evidence-contract](t-20261022-r27-evidence-contract.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261022-r27-evidence-verifier](t-20261022-r27-evidence-verifier.md)  
**Owner:** w2-lane (post-run + task link, dormant PR2)  
**Priority:** high  
**PRs:** [baseharbor#1090](https://github.com/mcpdev80/baseharbor/pull/1090), [baseharbor#1048](https://github.com/mcpdev80/baseharbor/pull/1048)  
**Source:** 
<!-- /generated:links -->

## Binding three-worker execution — Owner instruction, 2026-10-26

Routing: **W2**. Use the [coordinator handoff](../evidence/r27-ci-replacement-2026-10-26/CODEMAN-START.md); it supersedes earlier five-worker or serialized implementation scheduling.

W2: post-run task linking and published receipt lookup invocation. W1: receipt-shadow.yml and trusted consumption mapping. W3: retained lookup inside receipt_verifier.py and receipt-approval.yml. No separate resolver service or third production script.

Exactly three concurrent worker slots for all v0.4.27 CI work, plus the coordinator; never three additional workers on top of active claims. Existing owners/claims and completed commits are preserved. Coordinator hands over reservations explicitly and balances remaining effort, moving a bounded unfinished subtask or cross-review to a free worker rather than inventing work. No worker edits another worker's scripts, test file or workflow; common-branch pushes, Planning metadata and final integration have one coordinator writer.

Dependencies in frontmatter remain acceptance/readiness requirements, not blanket locks on the explicitly authorized isolated receipt preparation against frozen #1090 interfaces. Parallel preparation does not accept an unmerged dependency, change a shared interface unilaterally, or qualify a new domain. The first one-gate receipt skeleton must be accepted before live domain-gate expansion. Later domain implementation still requires its accepted product contracts, fixtures and release-start inputs; choose another actually ready task or report the concrete blocker if three safe work slices do not exist.

Do not alter active producer behavior or required-check enforcement before the accepted cutover. Preserve the legacy qualification route, use the smallest sufficient checks and batch candidates; no full matrix or duplicate green runs. Cross-review must be by another worker/coordinator and applies to the final integrated SHA.



# Receipt lookup: read the approved Planning history

## Goal
Resolve evidence/receipts/<gate>/<run>-<attempt>.json from an explicit Planning revision. Lookup is a small part of scripts/receipt_verifier.py, not a separate service or archive framework.

## Scope and acceptance
- Bounded strict JSON read and exact full-SHA plan binding.
- Validate receipt introduction and the sole allowed approval transition through Git objects. Later edits, including edit-and-revert histories, block.
- Missing, ambiguous, unapproved or plan-incompatible receipts block. A successful lookup is not qualification.
- Never query GitHub for already approved evidence. No artifact expiry, recovery or retention subsystem.
- Ship together with the first writer/verifier PR rather than an independently built horizontal platform.

## Historical preparation
Earlier PR #1048 archive resolver work remains historical and unaccepted. Its signed-manifest/retention requirements are superseded by the Owner's 2026-10-26 receipt decision.

Source assignment: <https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-ci-replacement-2026-10-26/CODEMAN-START.md> (three concurrent worker packages; coordinator owns integration).
