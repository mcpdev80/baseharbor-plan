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
prs: [mcpdev80/baseharbor#1343, mcpdev80/baseharbor#1344]
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261103-ci-receipt-source-recovery · CI: deploy receipt authentication on trusted main and recover missing records #task #release/v0-4-27 #status/active #view/active #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** Codex (CI completion 2026-11-03) · **Priority:** critical  
    **PR:** [baseharbor#1343](https://github.com/mcpdev80/baseharbor/pull/1343), [baseharbor#1344](https://github.com/mcpdev80/baseharbor/pull/1344)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md)  
**Owner:** Codex (CI completion 2026-11-03)  
**Priority:** critical  
**PRs:** [baseharbor#1343](https://github.com/mcpdev80/baseharbor/pull/1343), [baseharbor#1344](https://github.com/mcpdev80/baseharbor/pull/1344)  
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

- Main fix #1343 merged as 1c20b10bfcdf1fee5eb63d2c9d209fe9955e9a6d after 31 local tests and successful hosted workflow policy (41552223735); main PR does not run develop-only selected checks.
- Productive recovery succeeded with the existing PAT: run 41552421591 published PR 1341 / adfc10bcdaf6dc7d56f78ac600bfc031fd869204 at Planning 796186390f126dcaa1dd8cbca38747675aa785d0; run 41552425121 published PR 1342 / 8860aa2a6801eba80ceaee45c4c91bee8f1e3344 at a606f938843a011a16aedf213e26e389cc4f748c. Both logs identify main writer 1c20b10b and ephemeral Basic auth. No token replacement was needed.
- Develop parity #1344 at ffaaf5374d3a78c958151f6b7ea27482792cbfe7 is in normal hosted CI run 41552430415; do not merge until its actual checks pass. A normal automatic merge-triggered receipt and productive identical retry remain pending.
- GitHub connector cannot dispatch workflows; Owner invoked the two recovery commands. Future missed events: `gh workflow run receipt-post-run.yml -R mcpdev80/baseharbor --ref main -f pr_number=<merged-develop-PR>`.

- Owner assigned CI completion on 2026-11-03. Main 74dd7659996e38cf60c8b39368addb542d40c5a4 still has Bearer auth; develop 8860aa2a6801eba80ceaee45c4c91bee8f1e3344 has Basic auth.
- Run 41551273613 checked out main 74dd7659 and therefore did not execute PR 1342. Existing secret presence is confirmed by masked environment; validity remains unproven.
