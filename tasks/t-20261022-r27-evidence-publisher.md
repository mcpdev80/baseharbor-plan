---
id: t-20261022-r27-evidence-publisher
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
priority: critical
owner: w2-lane (W2 writer package)
depends_on: [t-20261017-release-0-4-27-updates, t-20261022-r27-evidence-contract]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1092, mcpdev80/baseharbor#1105, mcpdev80/baseharbor#1108, mcpdev80/baseharbor#1116, mcpdev80/baseharbor#1125]
sources: []
blocker: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/v0.4.27-2026-10-23/o68-publisher.md", "https://github.com/mcpdev80/baseharbor/pull/1108", "https://github.com/mcpdev80/baseharbor/pull/1109", "https://github.com/mcpdev80/baseharbor/pull/1110", "https://github.com/mcpdev80/baseharbor/pull/1121", "https://github.com/mcpdev80/baseharbor/pull/1122", "https://github.com/mcpdev80/baseharbor/commit/839e5cc9fa9b3da3908ee65f26596c2b3dfaaca7", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/board-2026-10-27/CODEX-REVIEW-c7936e8bd838.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/board-2026-10-27/CODEX-REVIEW-804383ed3364.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/board-2026-10-27/b2-board.md"]
---

- [ ] t-20261022-r27-evidence-publisher · W2: automatic receipt, plan and task publication #task #release/v0-4-27 #status/review #view/review #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** w2-lane (W2 writer package) · **Priority:** critical  
    **PR:** [baseharbor#1092](https://github.com/mcpdev80/baseharbor/pull/1092), [baseharbor#1105](https://github.com/mcpdev80/baseharbor/pull/1105), [baseharbor#1108](https://github.com/mcpdev80/baseharbor/pull/1108), [baseharbor#1116](https://github.com/mcpdev80/baseharbor/pull/1116), [baseharbor#1125](https://github.com/mcpdev80/baseharbor/pull/1125)  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/v0.4.27-2026-10-23/o68-publisher.md), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1108), [proof 3](https://github.com/mcpdev80/baseharbor/pull/1109), [proof 4](https://github.com/mcpdev80/baseharbor/pull/1110), [proof 5](https://github.com/mcpdev80/baseharbor/pull/1121), [proof 6](https://github.com/mcpdev80/baseharbor/pull/1122), [proof 7](https://github.com/mcpdev80/baseharbor/commit/839e5cc9fa9b3da3908ee65f26596c2b3dfaaca7), [proof 8](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/board-2026-10-27/CODEX-REVIEW-c7936e8bd838.md), [proof 9](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/board-2026-10-27/CODEX-REVIEW-804383ed3364.md), [proof 10](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/board-2026-10-27/b2-board.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-evidence-contract](t-20261022-r27-evidence-contract.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261022-r27-evidence-acceptance](t-20261022-r27-evidence-acceptance.md), [t-20261027-r27-shadow-run](t-20261027-r27-shadow-run.md)  
**Owner:** w2-lane (W2 writer package)  
**Priority:** critical  
**PRs:** [baseharbor#1092](https://github.com/mcpdev80/baseharbor/pull/1092), [baseharbor#1105](https://github.com/mcpdev80/baseharbor/pull/1105), [baseharbor#1108](https://github.com/mcpdev80/baseharbor/pull/1108), [baseharbor#1116](https://github.com/mcpdev80/baseharbor/pull/1116), [baseharbor#1125](https://github.com/mcpdev80/baseharbor/pull/1125)  
**Source:** 
<!-- /generated:links -->

# W2: automatic receipt, plan and task publication

## Observable result
An ordinary eligible completed PR run automatically produces and publishes a bounded plan, unapproved receipt and visible task evidence reference. W3 can reuse the same small publication helper for the sole approval edit; no patch export or human evidence push.

## Owned files
scripts/receipt_writer.py, scripts/receipt_tasklink.py; scripts/test_receipt_writer.py, scripts/test_receipt_tasklink.py; .github/workflows/receipt-post-run.yml. Reuse these helpers, no third production publisher. W1 owns policy/discovery/docs; W3 owns verifier and approval workflow. Coordinator owns shared Planning source/metadata.

## Inputs and interfaces
Existing six-field schema, attempt 1 and live verifier; corrected controller pin from the common integrated candidate; PLANNING_RECEIPT_WRITE_TOKEN availability is unverified. Prepare/test with temporary bare-Git remotes while coordinator resolves the real credential. Do not label configuration ready or substitute the Core GITHUB_TOKEN.

## Ordered subtasks
1. Replace the echo-only post-run template with actual bounded trusted-code execution and Planning checkout. Never check out PR head for privileged Python. Gate on eligible run/producer identity and success.
2. Obtain workflow_id from authenticated run.workflow_id and head/base/integration from authenticated producer data; never run.id or a branch-name fallback. Validate the real primary task association. Caller-supplied refs alone are not authenticated facts.
3. Produce the plan and receipt, then publish by ordinary fast-forward/expected-head update with bounded re-read/reapply on unrelated concurrent edits. Require clean worktree; propagate Git/API failures, preserve other writers, make identical retry idempotent and conflicting receipt fail closed. Define exact return values for introduction/path/published commits so W3/W1 do not guess HEAD.
4. Publish a task-to-receipt evidence reference and summary automatically; plan.task alone is not task evidence publication. Keep receipt bytes immutable except W3's single approval edit. Test actual implementation calls, not fixture arithmetic.

## Acceptance
Temporary Git tests prove successful durable publication, rejected push is not success, unrelated-writer preservation, idempotency, introduction-commit return and conflict failure. Workflow has no manual run/SHA/patch step and no candidate-code credential exposure. Actual cross-repository permission is separately proven before hosted pilot. Coordinator reviews combined candidate; hosted chain proof belongs to shadow-run.

## Exclusions
No secrets/log payloads in receipts or summaries, force push, archive/retention mechanism, new service or live dispatch during pause.

## Governing order and preserved history

The sole execution order is [CODEMAN-START.md](../evidence/r27-ci-replacement-2026-10-26/CODEMAN-START.md). Codeman remains paused until explicit Owner restart. Existing owner strings/commits are preserved; coordinator reconciles local checkpoints before assigning the three slots. [Pre-reset task, scope and results](https://github.com/mcpdev80/baseharbor-plan/blob/5df54047097107808e92ba4fe1bb2a8197f8772a/tasks/t-20261022-r27-evidence-publisher.md) remain immutable history, not competing operational instructions.

## Candidate status 2026-10-27 (b2 board sync)
Integrated candidate: baseharbor#1125 (branch `work/r27-correction-v34`, head `839e5cc9fa9b3da3908ee65f26596c2b3dfaaca7`). Package PRs: #1108, #1109, #1110, #1121, #1122. Codex REVIEW verdicts [CODEX-REVIEW-c7936e8bd838.md](../evidence/board-2026-10-27/CODEX-REVIEW-c7936e8bd838.md) and [CODEX-REVIEW-804383ed3364.md](../evidence/board-2026-10-27/CODEX-REVIEW-804383ed3364.md): both BLOCKED; F7 closed at source/test level, F1-F6 partially open and F8 open; no green required hosted CI on either reviewed candidate. Status stays review. Resolution text is not set here because the validator only allows `resolution` on a checked card.
