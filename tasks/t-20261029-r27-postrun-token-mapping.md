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
prs: ["mcpdev80/baseharbor#1201", "mcpdev80/baseharbor#1202", "mcpdev80/baseharbor#1205"]
sources: []
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1201", "https://github.com/mcpdev80/baseharbor/pull/1211", "https://github.com/mcpdev80/baseharbor/actions/runs/41022064363"]
---

- [x] t-20261029-r27-postrun-token-mapping · CI: pass Planning write token to receipt writer publish step #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** o203 (3fba91dd, ornith) · **Priority:** high  
    **PR:** [baseharbor#1201](https://github.com/mcpdev80/baseharbor/pull/1201), [baseharbor#1202](https://github.com/mcpdev80/baseharbor/pull/1202), [baseharbor#1205](https://github.com/mcpdev80/baseharbor/pull/1205)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1201), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1211), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/41022064363)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md)  
**Owner:** o203 (3fba91dd, ornith)  
**Priority:** high  
**PRs:** [baseharbor#1201](https://github.com/mcpdev80/baseharbor/pull/1201), [baseharbor#1202](https://github.com/mcpdev80/baseharbor/pull/1202), [baseharbor#1205](https://github.com/mcpdev80/baseharbor/pull/1205)  
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

Dependency semantics: t-20261017-release-0-4-27-updates is the release-start intake card and is intentionally NOT accepted yet; this slice runs under the r27 CI-replacement order (early: true, CODEMAN-START 2026-10-29), which authorizes CI-infrastructure slices ahead of release intake. This is prerequisite documentation, not an acceptance claim about the intake card.

## Handoff

#1201 merged (80d03122). Codex rv1202b ACCEPT develop-side at de93ff65 (#1202: pins dd8fb61d, GH_TOKEN preserved, write-token kept; checkout semantics verified at actions/checkout v7.0.1 source; hosted execution NOT claimed). #1202 CODEX-MERGE re-dispatched with the early:true dependency semantics documented above. Remaining for this card: main-side registration candidate (adds ONLY PLANNING_RECEIPT_WRITE_TOKEN to main's publish step; preserves main's existing pins/GH_TOKEN/attempt hardening per codex-rv1201 recipe step 1) and one observed automatic publication on a real producer run. Post-cutover follow-up candidate: exercise both SHA-checkout paths hosted; fetch-depth hardening if warranted (rv1202b).
