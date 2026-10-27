---
id: t-20261022-r27-evidence-verifier
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
priority: critical
owner: w3-lane (W3 verifier package)
depends_on: [t-20261017-release-0-4-27-updates, t-20261022-r27-evidence-contract]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1092, mcpdev80/baseharbor#1107]
sources: []
blocker: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-ci-replacement-2026-10-26/ACCEPTANCE-PR1.md"]
---

- [ ] t-20261022-r27-evidence-verifier · W3: genuine Owner approval and live/offline verification #task #release/v0-4-27 #status/active #view/active #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** w3-lane (W3 verifier package) · **Priority:** critical  
    **PR:** [baseharbor#1092](https://github.com/mcpdev80/baseharbor/pull/1092), [baseharbor#1107](https://github.com/mcpdev80/baseharbor/pull/1107)  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-ci-replacement-2026-10-26/ACCEPTANCE-PR1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-evidence-contract](t-20261022-r27-evidence-contract.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261022-r27-evidence-acceptance](t-20261022-r27-evidence-acceptance.md), [t-20261027-r27-shadow-run](t-20261027-r27-shadow-run.md)  
**Owner:** w3-lane (W3 verifier package)  
**Priority:** critical  
**PRs:** [baseharbor#1092](https://github.com/mcpdev80/baseharbor/pull/1092), [baseharbor#1107](https://github.com/mcpdev80/baseharbor/pull/1107)  
**Source:** 
<!-- /generated:links -->

# W3: genuine Owner approval and live/offline verification

## Observable result
Trusted code verifies an eligible producer and exact source tuple, authenticates the actual Owner action on real main, publishes the sole approval edit through W2's helper and exposes exact durable references for W1. Retained verification requires no origin API call.

## Owned files
scripts/receipt_verifier.py; scripts/test_receipt_verifier.py, scripts/test_receipt_chain.py; .github/workflows/receipt-approval.yml. Preserve useful #1107 test changes at b83e4faa; integrate them into this correction, do not merge them alone as evidence the chain is fixed. W2 alone edits writer/tasklink/publication; W1 alone edits CI/policy/docs/shadow.

## Inputs and parallel boundary
Use existing live/approve/retained API and six-field receipt; prepare/test alongside W1/W2 after restart. Reuse W2's agreed publication interface rather than changing W2 files. Keep the actual historical approved receipt unchanged.

## Ordered subtasks
1. Remove GITHUB_REF/identity overrides. Run from genuine main through reviewed default-branch registration and immutable helper pin. Validate real actor, triggering actor, event, repository and ref; the user approves a PR, not hand-entered receipt/hash/run fields.
2. Resolve the current exact receipt introduction/plan/candidate from trusted PR/task association and published Git history. Re-run the live witness before the approval edit; reject stale/ambiguous bindings and noneligible attempts. Do not mistake latest task-link HEAD for receipt introduction.
3. Bind producer trust beyond job names/workflow_id: initially reject a producer whose ci.yml differs from the reviewed protected base, and independently bind authenticated source inputs. PR code/artifacts cannot issue trust through matching labels.
4. Use W2's idempotent publication helper and least-privilege Planning credential, read back durable approval before success. Never export a patch as completion, create a second approval edit after retry or accept unapproved evidence through live fallback.
5. Repair test_approve_reverifies_live_before_edit by injecting the failing API; its current patch misses live(api=github)'s captured default and calls real gh. Tests must be hermetic. Retain meaningful existing coverage and #1107 cases without duplicating the old suite.

## Acceptance
Production verifier rejects wrong SHA, a genuinely nonexistent run and edited fixture/history. Wrong actor/ref/repository/event, forged producer workflow and ambiguous reference are bounded local negatives. Real approved receipt still verifies offline with origin API unavailable. W1 cross-reviews final integrated W3 code; complete hosted-chain acceptance is separate.

## Exclusions
No PKI, signatures, artifact archive, fabricated env/source assertions, real-receipt tampering or product/native test matrix.

## Governing order and preserved history

The sole execution order is [CODEMAN-START.md](../evidence/r27-ci-replacement-2026-10-26/CODEMAN-START.md). Codeman remains paused until explicit Owner restart. Existing owner strings/commits are preserved; coordinator reconciles local checkpoints before assigning the three slots. [Pre-reset task, scope and results](https://github.com/mcpdev80/baseharbor-plan/blob/5df54047097107808e92ba4fe1bb2a8197f8772a/tasks/t-20261022-r27-evidence-verifier.md) remain immutable history, not competing operational instructions.
