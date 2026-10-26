---
id: t-20261026-r27-receipt-pilot
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: ""
owner: ""
priority: critical
depends_on: [t-20261017-release-0-4-27-updates, t-20261022-r27-evidence-contract]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261026-r27-receipt-pilot · CI: single receipt shadow-chain pilot (PR2) #task #release/v0-4-27 #status/planned #view/waiting #board/planned #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** critical  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-evidence-contract](t-20261022-r27-evidence-contract.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md)  
**Owner:** unassigned  
**Priority:** critical  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Reconstruct the PR2 receipt shadow chain end-to-end on paper against the frozen baseharbor interfaces: runner (writer) -> receipt-commit -> fresh live verification -> Owner approval -> automatic task link -> retained final-check consumption, so PR2 has a verified, non-activated runbook before the dormant workflows are wired.

## Scope

- In scope: paper reconstruction of the six shadow steps (§Step 0-5 of p2-shadow-runbook.md) against the pinned frozen scripts (baseharbor work/r27-minimal-receipt @ ec82d476), the single Owner step, the missing task-link building block, the three yml activation points, and the abort/rollback criteria.
- Out of scope: activating any workflow, running any real GitHub gate, product code change, Planning write on the product side, or any commit/push of product state.

## Acceptance

- All four shadow steps share one `--planning`, one plan-fixture commit, one candidate SHA, and the receipt path `evidence/receipts/public-contracts/<run>-1.json`.
- The single manual Owner step is `receipt_verifier.py approve` (receipt_verifier.py:234-252), signed only by Owner `mcpdev80` via `GITHUB_ACTOR` + `GITHUB_TRIGGERING_ACTOR` on `workflow_dispatch` on protected main.
- The task link is produced by the existing trusted planner in the post-run workflow, never by a new producer/service (KLARER FEHLBAUSTEIN per p2-shadow-runbook §3).
- The three yml activation points are mapped line-precise to the pinned verifier/writer guards and remain DORMANT until PR2 commits activate them.
- Abort/rollback criteria documented; failed live/approve never leaves a partial write, and a rejected push is not success.

## Required checks

- Paper-only: no product file changed, no Planning write, no commit, no push.
- Cross-check the reconstruction against the pinned frozen scripts and the r3-reviews-pr2.md readiness note.

## Dependencies and file ownership

- Owned files or areas: this pilot card and the PR2 shadow-prep evidence under evidence/r27-ci-replacement-2026-10-26/.
- Shared files: the frozen baseharbor interfaces (receipt_writer.py:48-63, receipt_verifier.py:101-112, :127-203, :217-231, :234-252) and the receipt_tasklink producer bound to the existing trusted planner.
- Depends on the accepted PR1 one-gate skeleton (t-20261022-r27-evidence-contract) and the accepted positive PR2 shadow run before PR3 cutover (p3-cutover-checklist.md §4).

## Handoff

- Current state: PLANNED. This card authorizes the PR2 shadow-prep planning work only; it does not activate any workflow.
- Evidence: evidence/r27-ci-replacement-2026-10-26/PR2-SHADOW-PREP.md.
- Open before PR2 activation: the three yml dormant-activation commits, the trusted-planner task-link wiring, and the allowlist update on PR land.
