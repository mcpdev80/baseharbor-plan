---
id: t-20261022-r27-evidence-verifier
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
priority: critical
owner: w3-lane (W3 verifier package)
depends_on: [t-20261017-release-0-4-27-updates, t-20261022-r27-evidence-publisher, t-20261022-r27-evidence-resolver]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1090, mcpdev80/baseharbor#1048]
sources: []
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-ci-replacement-2026-10-26/ACCEPTANCE-PR1.md"]
---

- [x] t-20261022-r27-evidence-verifier · evidence verifier #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** w3-lane (W3 verifier package) · **Priority:** critical  
    **PR:** [baseharbor#1090](https://github.com/mcpdev80/baseharbor/pull/1090), [baseharbor#1048](https://github.com/mcpdev80/baseharbor/pull/1048)  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-evidence-resolver](t-20261022-r27-evidence-resolver.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-ci-replacement-2026-10-26/ACCEPTANCE-PR1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-evidence-publisher](t-20261022-r27-evidence-publisher.md), [t-20261022-r27-evidence-resolver](t-20261022-r27-evidence-resolver.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261022-r27-evidence-acceptance](t-20261022-r27-evidence-acceptance.md)  
**Owner:** w3-lane (W3 verifier package)  
**Priority:** critical  
**PRs:** [baseharbor#1090](https://github.com/mcpdev80/baseharbor/pull/1090), [baseharbor#1048](https://github.com/mcpdev80/baseharbor/pull/1048)  
**Source:** 
<!-- /generated:links -->

## Binding three-worker execution — Owner instruction, 2026-10-26

Routing: **W3**. Use the [coordinator handoff](../evidence/r27-ci-replacement-2026-10-26/CODEMAN-START.md); it supersedes earlier five-worker or serialized implementation scheduling.

W3: receipt_verifier.py, verifier-specific tests, test_receipt_chain.py and receipt-approval.yml. W2: writer and post-run interface. W1: trusted selection/test discovery and shadow consumption. Do not wait for publisher/resolver acceptance to prepare and test the existing frozen PR1 interface.

Exactly three concurrent worker slots for all v0.4.27 CI work, plus the coordinator; never three additional workers on top of active claims. Existing owners/claims and completed commits are preserved. Coordinator hands over reservations explicitly and balances remaining effort, moving a bounded unfinished subtask or cross-review to a free worker rather than inventing work. No worker edits another worker's scripts, test file or workflow; common-branch pushes, Planning metadata and final integration have one coordinator writer.

Dependencies in frontmatter remain acceptance/readiness requirements, not blanket locks on the explicitly authorized isolated receipt preparation against frozen #1090 interfaces. Parallel preparation does not accept an unmerged dependency, change a shared interface unilaterally, or qualify a new domain. The first one-gate receipt skeleton must be accepted before live domain-gate expansion. Later domain implementation still requires its accepted product contracts, fixtures and release-start inputs; choose another actually ready task or report the concrete blocker if three safe work slices do not exist.

Do not alter active producer behavior or required-check enforcement before the accepted cutover. Preserve the legacy qualification route, use the smallest sufficient checks and batch candidates; no full matrix or duplicate green runs. Cross-review must be by another worker/coordinator and applies to the final integrated SHA.



# Receipt verifier: live approval, retained Git verification

## Goal
Implement scripts/receipt_verifier.py with live, approve and retained modes. No signatures and no API calls after approval.

## Scope and acceptance
- Live: authenticate successful exact run/attempt, repository, workflow/event, successful named gate job, plan and candidate/integration binding; compare exact committed receipt bytes.
- Approve: only an authenticated Owner workflow action, immediately after a new live verification, may add by/at/receipt_commit. Approval refers to the exact original receipt commit; user-controlled names are not authorization.
- Retained: verify protected Git ancestry and the unique permitted approval edit, reject subsequent edits and compare applicable plan/candidate without contacting GitHub.
- Wrong SHA, nonexistent run and edited receipt each fail closed. API unavailability is unverified, never PASS.
- Existing final-check logic consumes receipts only after skeleton acceptance and a separate cutover PR. No circular dependency on the producer workflow completing itself.

## Bootstrap
PR 1 is qualified by existing v0.4.26 legacy checks. Later changes may use only already accepted new components, never their own unaccepted successor. Keep the active legacy pipeline unchanged until the real skeleton is accepted.

Source assignment: <https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-ci-replacement-2026-10-26/CODEMAN-START.md> (three concurrent worker packages; coordinator owns integration).

## Salvage references, not a predecessor implementation
The superseded archive prototype is not an implementation dependency. Read only applicable [run/attempt/job negatives](https://github.com/mcpdev80/baseharbor/blob/cdc905c93005fa2f8edc442e499e98bbea71b611/scripts/tests/test_r27_github_origin.py), [API/strict JSON cases](https://github.com/mcpdev80/baseharbor/blob/cdc905c93005fa2f8edc442e499e98bbea71b611/scripts/tests/test_r27_github_transport.py) and parser-only duplicate-key/NaN/Infinity cases in the historical receipt tests. No HMAC/Ed25519 code or claimed old test totals carry over. Port only cases needed by the small receipt risk surface.
