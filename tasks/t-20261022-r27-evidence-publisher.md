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
prs: [mcpdev80/baseharbor#1090, mcpdev80/baseharbor#1048]
sources: []
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/v0.4.27-2026-10-23/o68-publisher.md"]
---

- [x] t-20261022-r27-evidence-publisher · evidence publisher #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** w2-lane (W2 writer package) · **Priority:** critical  
    **PR:** [baseharbor#1090](https://github.com/mcpdev80/baseharbor/pull/1090), [baseharbor#1048](https://github.com/mcpdev80/baseharbor/pull/1048)  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/v0.4.27-2026-10-23/o68-publisher.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-evidence-contract](t-20261022-r27-evidence-contract.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261022-r27-evidence-verifier](t-20261022-r27-evidence-verifier.md)  
**Owner:** w2-lane (W2 writer package)  
**Priority:** critical  
**PRs:** [baseharbor#1090](https://github.com/mcpdev80/baseharbor/pull/1090), [baseharbor#1048](https://github.com/mcpdev80/baseharbor/pull/1048)  
**Source:** 
<!-- /generated:links -->

## Binding three-worker execution — Owner instruction, 2026-10-26

Routing: **W2**. Use the [coordinator handoff](../evidence/r27-ci-replacement-2026-10-26/CODEMAN-START.md); it supersedes earlier five-worker or serialized implementation scheduling.

W2: receipt_writer.py, writer-specific tests and receipt-post-run.yml, including bounded publication/task linking. W1: exact mapping/discovery and shared docs only. W3: receipt_verifier.py and verifier-specific tests; review producer binding without writing W2 files.

Exactly three concurrent worker slots for all v0.4.27 CI work, plus the coordinator; never three additional workers on top of active claims. Existing owners/claims and completed commits are preserved. Coordinator hands over reservations explicitly and balances remaining effort, moving a bounded unfinished subtask or cross-review to a free worker rather than inventing work. No worker edits another worker's scripts, test file or workflow; common-branch pushes, Planning metadata and final integration have one coordinator writer.

Dependencies in frontmatter remain acceptance/readiness requirements, not blanket locks on the explicitly authorized isolated receipt preparation against frozen #1090 interfaces. Parallel preparation does not accept an unmerged dependency, change a shared interface unilaterally, or qualify a new domain. The first one-gate receipt skeleton must be accepted before live domain-gate expansion. Later domain implementation still requires its accepted product contracts, fixtures and release-start inputs; choose another actually ready task or report the concrete blocker if three safe work slices do not exist.

Do not alter active producer behavior or required-check enforcement before the accepted cutover. Preserve the legacy qualification route, use the smallest sufficient checks and batch candidates; no full matrix or duplicate green runs. Cross-review must be by another worker/coordinator and applies to the final integrated SHA.



# Receipt writer: one bounded result, one Planning commit

## Goal
Implement scripts/receipt_writer.py, approximately 100 lines excluding shared validation, invoked only by a trusted post-run workflow. PR jobs, including forks, never receive Planning write credentials.

## Scope and acceptance
- Read authenticated GitHub run/attempt/job facts through the live verifier and a protected, immutable gate plan. Persist references/IDs only, below 500 bytes.
- Create evidence/receipts/<gate>/<run>-<attempt>.json with approved:null. Identical retry is idempotent; conflicting content blocks.
- Publish ordinary fast-forward commits, preserve concurrent Planning edits and report failed publication. No force pushes or secret/log payloads.
- Publish an automatic task reference as part of the walking skeleton, with no manually copied run numbers or evidence URLs.
- Start workflow integration only after PR 1 contract/scripts acceptance. Exactly one gate first; no parallel gate expansion.
- No signature key, issuer service, payload archive, redaction pipeline or retention/recovery subsystem.

## Historical preparation
PR #1048 is retained as historical isolated archive work, not an implementation dependency or current qualification. The Owner's 2026-10-26 receipt decision supersedes its archive/signature requirements.

Source assignment: <https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-ci-replacement-2026-10-26/CODEMAN-START.md> (three concurrent worker packages; coordinator owns integration).
