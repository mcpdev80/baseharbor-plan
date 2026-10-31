---
id: t-20261029-r27-writer-selftest-job
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

- [ ] t-20261029-r27-writer-selftest-job · CI: writer selftest job — validate plan.zip against extract_facts before any publication #task #release/v0-4-27 #status/planned #view/waiting #board/planned #kind/task
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

The receipt post-run writer validates the downloaded artifact against extract_facts in an isolated selftest step before any planning publication, so transport/binding errors surface as one precise gate failure.

## Scope

- In scope: A dry-run selftest step (no publish) running extract_facts against the real plan.zip.
- Out of scope: any product behavior change; this is a CI/contract-coverage card only.

## Acceptance

The selftest step reports the exact missing/bad field; no publication occurs on its failure.

## Required checks

receipt-postrun tests stay green; selftest failure blocks the publish step fail-closed.

## Dependencies and file ownership

- Owned files or areas: .github/workflows/receipt-post-run.yml (selftest step), scripts/test_receipt_postrun.py
- Shared files: coordinate through the owning task.

## Handoff

- Created 2026-10-29 from the R27 night-shift Cause-7..16 findings (evidence/board-2026-10-27/SHADOW-RUN-STATUS.md). Unassigned, planned.
