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
resolution: ""
evidence: []
---

- [ ] t-20261029-r27-ci-approval-pin · CI: repair approval trusted source pins #task #release/v0-4-27 #status/review #view/review #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** f60 (correction round, flash H3) · **Priority:** high  
    **PR:** [baseharbor#1200](https://github.com/mcpdev80/baseharbor/pull/1200)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** none  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md)  
**Owner:** f60 (correction round, flash H3)  
**Priority:** high  
**PRs:** [baseharbor#1200](https://github.com/mcpdev80/baseharbor/pull/1200)  
**Source:** 
<!-- /generated:links -->

## Goal

Repair approval and shadow trusted-source configuration

## Scope

Inspect current registered workflow, source pin and verifier; correct the empty TRUSTED_SOURCE and any proven shadow pin defect using an immutable reviewed commit. Reserve receipt-approval.yml and corresponding focused tests; coordinate any verifier changes with its existing owner.

## Acceptance

Approval loads the intended trusted source and rejects wrong or absent pins; shadow executes reviewed source. Focused tests and workflow validation pass; hosted end-to-end remains a separate proof.

## Required checks

Run focused validation for the changed surface; record exact revision and results. Planning-only handoffs require plan render/check.

## Dependencies and file ownership

Exclusive .github/workflows/receipt-approval.yml and its focused tests after coordinator reservation; shared verifier changes require owner coordination.

Lane o201 delivered: branch work/r27-pin-o201 head 5aaa38ec, PR #1200 pins TRUSTED_SOURCE to reviewed b53632aa per evidence approval-pin.md (END o201-DONE, disk-verified by coordinator). Independent review pending per RUNBOOK §5 END rule; merge only via Codex-MERGE after ACCEPT. Evidence: https://github.com/mcpdev80/baseharbor-plan/blob/{sha}/evidence/r27-ci-replacement-2026-10-29/approval-pin.md

