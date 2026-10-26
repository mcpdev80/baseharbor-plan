# Codeman start: three parallel receipt workers

## Owner instruction and baseline

Marcel explicitly requests THREE concurrently productive workers with comparable remaining work, not five sequential slots. This scheduling instruction supersedes the earlier five-worker/contract-first implementation schedule. Acceptance dependencies remain; they are not implementation waiting barriers for the isolated preparation authorized here.

v0.4.26 is published: https://github.com/mcpdev80/baseharbor/releases/tag/v0.4.26 . Do not reopen its qualification cycle. Refresh repository heads, AGENTS.md and current claims before mutation.

Continue draft https://github.com/mcpdev80/baseharbor/pull/1090 ; observed head on 2026-10-26: ec82d476126291d372df2c13bd36273767574869. Preserve its two scripts, six focused tests and EN/DE docs. Recheck current source; do not reimplement completed work. The existing legacy coverage mapping/test-discovery gap is not a product-test failure or accepted evidence.

## Start all three now

Coordinator freezes the callable interfaces already in #1090 once, assigns disjoint paths, and dispatches all three together. No worker waits for W1 acceptance to inspect, implement or locally test its assigned slice. Interface changes require a coordinated revision; no worker invents a second contract.

| Worker | Implement concurrently | Exclusive writes |
| --- | --- | --- |
| W1 | Contract/legacy bootstrap, exact path mapping and test discovery; paired documentation; shadow final-check consumption prepared for PR2 | Existing pr-gate-plan.py, pr-check-runner.py, test_pr_gate_plan.py; necessary exact qualification register; docs/development/minimal-ci-receipts.md and DE pair; .github/workflows/receipt-shadow.yml |
| W2 | Writer corrections, safe fast-forward publication, post-run invocation, automatic gate-plan/task reference; focused writer tests | scripts/receipt_writer.py; scripts/test_receipt_writer.py; .github/workflows/receipt-post-run.yml |
| W3 | Verifier corrections, live provenance/integration binding, authenticated approval action, offline history checks and required negatives | scripts/receipt_verifier.py; scripts/test_receipt_verifier.py; scripts/test_receipt_chain.py; .github/workflows/receipt-approval.yml |

W1: legacy registration changes must be exact and independently qualified, never broad exemptions or disabled checks. Do not change producer triggers, runner behavior or replace the active required final-check during preparation.

W2: the existing verifier functions are the shared interface. Keep task linking bounded within the workflow; no extra production script/service, generic flags or archive. Credentials stay in the trusted post-run context, never in fork/PR execution. Check publication before reporting success.

W3: preserve the current live trusted-pr-plan read, needed because Actions head_sha alone does not identify the tested merge. Read only during the live window; retain no artifact. Required negatives: wrong SHA, dead run ID, edited receipt. Reuse existing tests; do not duplicate the old suite or claim self-authored acceptance is independent.

Coordinator owns Planning task metadata, claims, shared views, common branch, PR operations and final integration. Workers use separate worktrees/branches from the frozen baseline and hand off exact commits. They do not concurrently push the shared branch. W1's and W2's workflow definitions and W3's approval definition must agree on the same receipt path and script arguments before combined execution.

## Balance work rather than create waiting workers

Estimate remaining effort against existing code, not historical task size. The packages above distribute bootstrap/docs/shadow, writing/publication/linking, and verification/approval/negatives. Equal completion time is a target, not a claim.

As soon as a worker finishes its primary slice, assign bounded cross-review or one concrete unfinished subtask after explicitly transferring its file reservation. W1 reviews W3, W3 reviews W2, W2 reviews W1. Never generate more gates, speculative features or redundant tests to keep workers busy. Reuse completed f71/o145 work and preserve their commits/results; hand over active assignments cleanly instead of restarting them. Three is the target pool, not three additional workers on top of existing writers.

## Integrate without activating early

Implement all slices concurrently, but keep workflow additions in separate dormant PR2 commits until PR1 is accepted. PR1 remains contract + writer/verifier + focused tests/docs qualified by the legacy path; the exact legacy-mapping prerequisite may need a separately bounded commit/PR. PR2 proves exactly ONE real end-to-end shadow chain: runner -> writer -> receipt commit -> fresh live verification -> Owner approval commit -> automatic task link -> final-check consumption. PR3 alone cuts over the accepted required check.

Preserve genuine technical checks and exact candidate binding. No signatures/PKI, attestation bundles, payload archives, retention/recovery subsystem or second evidence authority. Owner approval remains explicit. Not-required gates have plan reasons, never PASS receipts. No manual run-ID/evidence bookkeeping. Developer summary: at most checked / validly reused / not required with reason.

Batch related changes, run only risk-matched local checks, inspect the current CI result before publishing a replacement candidate. Do not use one-file pushes or repeat green runs as a debugging loop; no full runtime matrix for receipt control-plane work.

## Planning and deadline

Reconcile the existing five evidence cards into these three ownership packages; keep the formal cards as acceptance units, not serialized implementation locks. Do not assume the earlier unpublished five-worker epic is on main. Retire t-20261024-r27-evidence-prototype with resolution superseded and a receipt-task successor; only API verification/parser regression ideas are salvageable. Never resume its HMAC/Ed25519/issuer architecture.

The timer starts at PR1 acceptance, not W1/contract acceptance: record T0 and an absolute UTC deadline T0 + 72 hours in the acceptance record, linked from the contract card. If the one-gate chain is not accepted by then, stop infrastructure expansion, state the concrete blocker, and continue eligible product work through adequate existing trusted legacy checks. No silent extensions, fake passes or waived product prerequisites.

Use GitHub MCP. Keep Planning truthful and render/check changed metadata. If automatic approval blocks publication, report it and request the necessary explicit approval; do not bypass it. This handoff authorizes neither a release nor live cutover before acceptance.
