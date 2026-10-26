---
id: t-20261022-r27-evidence-publisher
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
priority: critical
owner: ""
depends_on: [t-20261017-release-0-4-27-updates, t-20261022-r27-evidence-contract]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1048]
sources: []
blocker: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/v0.4.27-2026-10-23/o68-publisher.md"]
---

- [ ] t-20261022-r27-evidence-publisher · evidence publisher #task #release/v0-4-27 #status/planned #view/waiting #board/planned #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** critical  
    **PR:** [baseharbor#1048](https://github.com/mcpdev80/baseharbor/pull/1048)  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-evidence-contract](t-20261022-r27-evidence-contract.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/v0.4.27-2026-10-23/o68-publisher.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-evidence-contract](t-20261022-r27-evidence-contract.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261022-r27-evidence-verifier](t-20261022-r27-evidence-verifier.md)  
**Owner:** unassigned  
**Priority:** critical  
**PRs:** [baseharbor#1048](https://github.com/mcpdev80/baseharbor/pull/1048)  
**Source:** 
<!-- /generated:links -->


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
