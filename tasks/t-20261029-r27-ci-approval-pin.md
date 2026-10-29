---
id: t-20261029-r27-ci-approval-pin
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
owner: "f60 (29879f0e, flash)"
early: true
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1200"]
sources: []
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/commit/a3750a8f6a26170fbe3995f0c480e5929948a276", "https://github.com/mcpdev80/baseharbor-plan/blob/HEAD/evidence/r27-ci-replacement-2026-10-29/codex-merge-1200.md"]
---

- [x] t-20261029-r27-ci-approval-pin · CI: repair approval trusted source pins #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** f60 (29879f0e, flash) · **Priority:** high  
    **PR:** [baseharbor#1200](https://github.com/mcpdev80/baseharbor/pull/1200)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/commit/a3750a8f6a26170fbe3995f0c480e5929948a276), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/HEAD/evidence/r27-ci-replacement-2026-10-29/codex-merge-1200.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** none  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md)  
**Owner:** f60 (29879f0e, flash)  
**Priority:** high  
**PRs:** [baseharbor#1200](https://github.com/mcpdev80/baseharbor/pull/1200)  
**Source:** 
<!-- /generated:links -->

## Goal

Repair approval and shadow trusted-source configuration

## Scope

Inspect current registered workflow, source pin and verifier; correct the empty TRUSTED_SOURCE and any proven shadow pin defect using an immutable reviewed commit. Reserve receipt-approval.yml and corresponding focused tests; coordinate any verifier changes with its existing owner.

## Acceptance

Approval loads the intended trusted source and rejects wrong or absent pins; the shadow job is statically wired to a self-consistent reviewed ref (interface + pin correctness). Focused tests and workflow validation pass. Executed shadow evidence belongs to t-20261027-r27-shadow-run (CODEMAN-START proof ordering: registration and hosted execution follow integration; a merged pin cannot be proven by pre-merge hosted runs). Contract clarified by coordinator 2026-10-29 per CODEMAN-START authority in response to codex-merge-1200.md MERGE1200B finding.

## Required checks

Run focused validation for the changed surface; record exact revision and results. Planning-only handoffs require plan render/check.

## Dependencies and file ownership

Exclusive .github/workflows/receipt-approval.yml and its focused tests after coordinator reservation; shared verifier changes require owner coordination.

Lane o201 delivered: branch work/r27-pin-o201 head 5aaa38ec, PR #1200 pins TRUSTED_SOURCE to reviewed b53632aa per evidence approval-pin.md (END o201-DONE, disk-verified by coordinator). Independent review pending per RUNBOOK §5 END rule; merge only via Codex-MERGE after ACCEPT. Evidence: https://github.com/mcpdev80/baseharbor-plan/blob/HEAD/evidence/r27-ci-replacement-2026-10-29/approval-pin.md

