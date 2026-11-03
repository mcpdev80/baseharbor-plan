---
id: t-20261103-ci-receipt-source-recovery
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: ""
owner: "Codex (CI completion 2026-11-03)"
priority: critical
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261103-ci-receipt-source-recovery · CI: deploy receipt authentication on trusted main and recover missing records #task #release/v0-4-27 #status/active #view/active #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** Codex (CI completion 2026-11-03) · **Priority:** critical  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md)  
**Owner:** Codex (CI completion 2026-11-03)  
**Priority:** critical  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Publish minimal commit receipts from the actual trusted default-branch writer and recover missed develop merges without rechecking CI runs or jobs.

## Scope

- Deploy the existing Basic-auth repair to main; retain default-branch execution and commit/PR binding.
- Add a bounded default-branch dispatch for retrying one authenticated merged PR.
- Verify normal hosted CI and productive Planning publication. Keep rulesets disabled; no release or tag.

## Acceptance

- Logs identify the executed writer source without printing credentials.
- Successful productive receipts exist for PRs 1341 and 1342; identical retry is harmless.
- No Actions run/job interpretation or separate approval chain is added to receipts.

## Required checks

- Focused writer/workflow tests, workflow policy and actual hosted publish/readback.
- Planning render/check after every metadata update.

## Dependencies and file ownership

- Own scripts/receipt_writer.py, scripts/test_receipt_writer.py, scripts/test_receipt_postrun.py and .github/workflows/receipt-post-run.yml for this correction.
- Existing publisher implementation is closed. Current active product claims own other files; preserve them. Coordinator cutover card remains blocked and is not taken over as an implementation claim.
- No access to local Codeman processes from this cloud workspace; remote published claims are the available authority.

## Handoff

- Owner assigned CI completion on 2026-11-03. Main 74dd7659996e38cf60c8b39368addb542d40c5a4 still has Bearer auth; develop 8860aa2a6801eba80ceaee45c4c91bee8f1e3344 has Basic auth.
- Run 41551273613 checked out main 74dd7659 and therefore did not execute PR 1342. Existing secret presence is confirmed by masked environment; validity remains unproven.
