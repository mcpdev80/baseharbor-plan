---
id: t-20261022-r27-evidence-contract
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
priority: critical
owner: flash-f71 (worker-1 contract+legacy-bootstrap)
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1090, mcpdev80/baseharbor#1091, mcpdev80/baseharbor#1092]
sources: []
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-ci-replacement-2026-10-26/ACCEPTANCE-PR1.md"]
---

- [x] t-20261022-r27-evidence-contract · Receipt schema and interface contract (PR1 scope) #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** flash-f71 (worker-1 contract+legacy-bootstrap) · **Priority:** critical  
    **PR:** [baseharbor#1090](https://github.com/mcpdev80/baseharbor/pull/1090), [baseharbor#1091](https://github.com/mcpdev80/baseharbor/pull/1091), [baseharbor#1092](https://github.com/mcpdev80/baseharbor/pull/1092)  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-ci-replacement-2026-10-26/ACCEPTANCE-PR1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261022-r27-evidence-acceptance](t-20261022-r27-evidence-acceptance.md), [t-20261022-r27-evidence-publisher](t-20261022-r27-evidence-publisher.md), [t-20261022-r27-evidence-resolver](t-20261022-r27-evidence-resolver.md), [t-20261022-r27-evidence-verifier](t-20261022-r27-evidence-verifier.md), [t-20261024-r27-ci-impact-prototype](t-20261024-r27-ci-impact-prototype.md), [t-20261026-r27-receipt-pilot](t-20261026-r27-receipt-pilot.md), [t-20261027-r27-shadow-run](t-20261027-r27-shadow-run.md)  
**Owner:** flash-f71 (worker-1 contract+legacy-bootstrap)  
**Priority:** critical  
**PRs:** [baseharbor#1090](https://github.com/mcpdev80/baseharbor/pull/1090), [baseharbor#1091](https://github.com/mcpdev80/baseharbor/pull/1091), [baseharbor#1092](https://github.com/mcpdev80/baseharbor/pull/1092)  
**Source:** 
<!-- /generated:links -->

# Receipt schema and interface contract (PR1 scope)

## Accepted scope, not complete operational qualification
Retain the six-field/<500-byte receipt contract and original PR1 source/schema acceptance. One gate is public-contracts; the receipt identifies full tested integration SHA and immutable Planning plan. Only one approved:null -> by/at/receipt_commit transition is permitted. No signatures, payload archive, retention service or extra authority.

## Actual baseline and qualification limit
PR #1092 incorporated #1090; #1090 is closed without separate merge. The audit found that current trusted CI does not discover receipt suites, contrary to earlier docs/PR1 wording. Do not treat old CI success as complete test execution or automatic publication. W1/W2/W3 own those corrections; this contract card owns no parallel source writes.

## Interface ownership
W1 owns trusted execution/discovery and docs; W2 owns publication/plan/task-link interfaces in existing helpers; W3 owns live/approve/retained validation. Freeze shared call signatures once before parallel edits. Receipt fields/modes remain stable; no unilateral branch/API invention.

## Timebox
T0 2026-10-26T23:35:50Z and deadline 2026-10-29T23:35:50Z remain unchanged. Read the code audit and current order; do not start new contract implementation or restart old archive stories.

## Governing order and preserved history

The sole execution order is [CODEMAN-START.md](../evidence/r27-ci-replacement-2026-10-26/CODEMAN-START.md). Codeman remains paused until explicit Owner restart. Existing owner strings/commits are preserved; coordinator reconciles local checkpoints before assigning the three slots. [Pre-reset task, scope and results](https://github.com/mcpdev80/baseharbor-plan/blob/5df54047097107808e92ba4fe1bb2a8197f8772a/tasks/t-20261022-r27-evidence-contract.md) remain immutable history, not competing operational instructions.
