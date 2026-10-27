---
id: t-20261024-r27-ci-impact-prototype
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
priority: high
owner: "ChatGPT (isolated v0.4.27 prototype)"
depends_on: [t-20261017-release-0-4-27-updates, t-20261022-r27-evidence-contract]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1091, mcpdev80/baseharbor#1092, mcpdev80/baseharbor#1109]
sources: []
early: false
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261024-r27-ci-impact-prototype · W1: trusted receipt execution, discovery and shadow consumption #task #release/v0-4-27 #status/review #view/review #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** ChatGPT (isolated v0.4.27 prototype) · **Priority:** high  
    **PR:** [baseharbor#1091](https://github.com/mcpdev80/baseharbor/pull/1091), [baseharbor#1092](https://github.com/mcpdev80/baseharbor/pull/1092), [baseharbor#1109](https://github.com/mcpdev80/baseharbor/pull/1109)  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-evidence-contract](t-20261022-r27-evidence-contract.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261022-r27-evidence-acceptance](t-20261022-r27-evidence-acceptance.md), [t-20261027-r27-shadow-run](t-20261027-r27-shadow-run.md)  
**Owner:** ChatGPT (isolated v0.4.27 prototype)  
**Priority:** high  
**PRs:** [baseharbor#1091](https://github.com/mcpdev80/baseharbor/pull/1091), [baseharbor#1092](https://github.com/mcpdev80/baseharbor/pull/1092), [baseharbor#1109](https://github.com/mcpdev80/baseharbor/pull/1109)  
**Source:** 
<!-- /generated:links -->

# W1: trusted receipt execution, discovery and shadow consumption

## Observable result
Existing selected CI actually executes the receipt/policy suites. The trusted shadow consumer accepts only a published approved receipt after approval; a reviewed default-main workflow registration can use a fixed corrected helper SHA without pretending develop is main.

## Owned files
.github/workflows/ci.yml; .github/workflows/receipt-shadow.yml; scripts/pr-gate-plan.py, scripts/pr-check-runner.py, scripts/ci-workflow-policy.sh; their existing test files including test_ci_workflow_policy_receipts.py; paired docs/development/minimal-ci-receipts.md and docs/de/development/minimal-ci-receipts.md. No writer/verifier/post-run/approval source edits. Coordinator alone updates final literal pins and publishes main registration.

## Inputs and parallel boundary
Consume frozen merged develop 3431b22c and existing writer/verifier interfaces; prepare concurrently with W2/W3 after Owner resume, not after their acceptance. Use explicit publication outputs agreed with W2. Give changes to another package's files to its owner.

## Ordered subtasks
1. Repair actual receipt-suite discovery/required-result wiring in the existing selected lane; keep exact path mapping fail-closed. Current CI_CHECKS alone runs unrelated legacy suites. Prove real execution and failure propagation, not only that a path resolves.
2. Define the actual controller context as main, using reviewed workflow files on default main and immutable corrected develop helper pin. Remove diagnostic/stale policy assumptions, not protections. Prepare the smallest CI-only main registration diff through normal gates; no product promotion, tag or default-branch change.
3. Replace PR-open/live-fallback shadow logic with retained-only full-history verification after W3 reports durable approval publication. Pass the exact published receipt/plan/candidate; do not globally scan for any apparently green candidate. No final-check/producer cycle.
4. Fix EN/DE statements that falsely claim receipt discovery or automatic flow already exists. Cross-review W3 once own package is ready.

## Acceptance and handoff
Actual selected command runs receipt and policy tests, rejects a relevant injected fixture failure, and reports zero skips as qualification. Policy/actionlint/local binding tests pass. A wrong producer ref cannot receive trusted privileges; an unapproved receipt cannot pass shadow. Handoff exact source, commands/results and prepared main-registration diff to coordinator. Real automatic skeleton is accepted only on the shadow-run card; W1 cannot self-qualify the complete chain.

## Exclusions
No native/full matrix, blanket map, disabled required check, invented source flag or added production framework.

## Governing order and preserved history

The sole execution order is [CODEMAN-START.md](../evidence/r27-ci-replacement-2026-10-26/CODEMAN-START.md). Codeman remains paused until explicit Owner restart. Existing owner strings/commits are preserved; coordinator reconciles local checkpoints before assigning the three slots. [Pre-reset task, scope and results](https://github.com/mcpdev80/baseharbor-plan/blob/5df54047097107808e92ba4fe1bb2a8197f8772a/tasks/t-20261024-r27-ci-impact-prototype.md) remain immutable history, not competing operational instructions.

## Coordinator reservation 2026-10-27 (restart)
Slot W1 executes via fresh lane `w1` (ornith), branch `work/r27-w1-discovery` from frozen develop `3431b22c`; historical owner string preserved per governing order. Lane WIP checkpoint `worktrees/pr3a` (ci.yml change = reusable input; scripts/pr-required-final.py + scripts/test_pr_required_final_receipt.py are outside the reserved write set and enter only by owner-of-file review).

