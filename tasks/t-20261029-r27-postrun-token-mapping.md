---
id: t-20261029-r27-postrun-token-mapping
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
owner: "o203 (3fba91dd, ornith)"
early: true
priority: high
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261029-r27-postrun-token-mapping · CI: pass Planning write token to receipt writer publish step #task #release/v0-4-27 #status/active #view/active #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** o203 (3fba91dd, ornith) · **Priority:** high  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md)  
**Owner:** o203 (3fba91dd, ornith)  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Close the fail-closed publication gap found on run 40834168626

## Scope

In receipt-post-run.yml the publish job's "Publish receipt to Planning" step env supplies GH_TOKEN, PLANNING_ROOT, RUN_ID, PLAN_REVISION only; scripts/receipt_writer.py requires the PLANNING_RECEIPT_WRITE_TOKEN environment (require at receipt_writer.py:108-110) and therefore fails closed although the repository secret exists. Reproduce from the failed run log, add the token to the step env of the workflow copy registered on the product default branch (and the develop source copy), keeping all other credential handling unchanged, and extend the focused workflow test that asserts publish-step env keys. Verify the controller checkout already maps the token for the Planning checkout step.

## Acceptance

Focused tests pass; the diff touches only .github/workflows/receipt-post-run.yml plus its focused test; publication path can receive the token without logging it; exact candidate PR available for the chain requalification run.

## Required checks

Run focused validation for the changed surface; record exact revision and results. Planning-only handoffs require plan render/check.

## Dependencies and file ownership

Exclusive: .github/workflows/receipt-post-run.yml + its focused test files. No overlap with receipt-approval.yml (#1200 owner) or verifier scripts.

## Handoff

Unassigned. Coordinator checks current claims and source heads before assignment.
