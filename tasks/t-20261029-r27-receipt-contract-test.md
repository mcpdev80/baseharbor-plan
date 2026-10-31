---
id: t-20261029-r27-receipt-contract-test
type: task
areas: []
release: v0.4.27
version: ""
parent: ""
owner: ""
priority: ""
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261029-r27-receipt-contract-test · CI: add required contract test — producer artifact must carry every extract_facts field #task #release/v0-4-27 #status/planned #view/waiting #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Waiting for prerequisites**  
    **Needs:** t-20261017-release-0-4-27-updates  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** t-20261017-release-0-4-27-updates  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

A hosted contract test proves every field receipt_verifier.extract_facts requires is present in the trusted-pr-plan artifact, failing the producer CI instead of the post-run writer.

## Scope

- In scope: Required CI job or step validating the artifact schema against the extractor contract for the same run.
- Out of scope: any product behavior change; this is a CI/contract-coverage card only.

## Acceptance

A plan without attempt/required fields fails the producer gate before publication.

## Required checks

Existing green chain remains; new job listed in required_validation_checks for qualifying paths.

## Dependencies and file ownership

- Owned files or areas: scripts/test_receipt_postrun.py, .github/workflows/ci.yml (gate registration)
- Shared files: coordinate through the owning task.

## Handoff

- Created 2026-10-29 from the R27 night-shift Cause-7..16 findings (evidence/board-2026-10-27/SHADOW-RUN-STATUS.md). Unassigned, planned.
