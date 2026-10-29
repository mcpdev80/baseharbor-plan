---
id: t-20261029-r27-ci-approval-pin
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
owner: "o201 (350b6e73, ornith)"
early: true
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261029-r27-ci-approval-pin · CI: repair approval trusted source pins #task #release/v0-4-27 #status/active #view/active #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** o201 (350b6e73, ornith) · **Priority:** high  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** none  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md)  
**Owner:** o201 (350b6e73, ornith)  
**Priority:** high  
**PRs:** none  
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

## Handoff

Lane o201 session 350b6e73; product writes: .github/workflows/receipt-approval.yml + focused tests only, own new worktree/branch work/r27-pin-o201.

