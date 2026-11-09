---
id: t-20261103-ci-receipt-source-recovery
card_number: "0427-100"
card_short_title: "deploy receipt Auth on trusted"
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: ""
owner: "Codex (CI completion 2026-11-03)"
kanban_lane: closed
kanban_summary: Publish minimal commit receipts from the actual trusted default-branch writer and recover missed develop merges without…
kanban_status: closed
kanban_title: "0427-100 · deploy receipt Auth on trusted"
priority: critical
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1343, mcpdev80/baseharbor#1344]
sources: []
blocker: ""
resolution: accepted
evidence: [https://github.com/mcpdev80/baseharbor/pull/1343, https://github.com/mcpdev80/baseharbor/pull/1344, https://github.com/mcpdev80/baseharbor/actions/runs/41552421591, https://github.com/mcpdev80/baseharbor/actions/runs/41552425121, https://github.com/mcpdev80/baseharbor/actions/runs/41552839185]
---

- [x] t-20261103-ci-receipt-source-recovery · CI: deploy receipt authentication on trusted main and recover missing records #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** Codex (CI completion 2026-11-03) · **Priority:** critical  
    **PR:** [baseharbor#1343](https://github.com/mcpdev80/baseharbor/pull/1343), [baseharbor#1344](https://github.com/mcpdev80/baseharbor/pull/1344)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1343), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1344), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/41552421591), [proof 4](https://github.com/mcpdev80/baseharbor/actions/runs/41552425121), [proof 5](https://github.com/mcpdev80/baseharbor/actions/runs/41552839185)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.27  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Required by:** [t-20261103-ci-authority-package-coverage](t-20261103-ci-authority-package-coverage.md)  
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

- Owner-authorized Maintainer acceptance: #1344 passed all normal selected CI including final PR Selected Checks (41552430415), merged to develop as 470642acbb87e89c10d90f1f622cdd8c81b8705c, and automatically published its commit receipt in pull_request_target run 41552839185 (success). This proves normal event publication in addition to both recovery dispatches. Existing local bare-remote tests prove identical retry and concurrency preservation; no extra live retry was launched. No independent review is claimed.

- Main fix #1343 merged as 1c20b10bfcdf1fee5eb63d2c9d209fe9955e9a6d after 31 local tests and successful hosted workflow policy (41552223735); main PR does not run develop-only selected checks.
- Productive recovery succeeded with the existing PAT: run 41552421591 published PR 1341 / adfc10bcdaf6dc7d56f78ac600bfc031fd869204 at Planning 796186390f126dcaa1dd8cbca38747675aa785d0; run 41552425121 published PR 1342 / 8860aa2a6801eba80ceaee45c4c91bee8f1e3344 at a606f938843a011a16aedf213e26e389cc4f748c. Both logs identify main writer 1c20b10b and ephemeral Basic auth. No token replacement was needed.
- Develop parity #1344 at ffaaf5374d3a78c958151f6b7ea27482792cbfe7 is in normal hosted CI run 41552430415; do not merge until its actual checks pass. The normal automatic merge-triggered receipt subsequently passed as recorded above.
- GitHub connector cannot dispatch workflows; Owner invoked the two recovery commands. Future missed events: `gh workflow run receipt-post-run.yml -R mcpdev80/baseharbor --ref main -f pr_number=<merged-develop-PR>`.

- Owner assigned CI completion on 2026-11-03. Main 74dd7659996e38cf60c8b39368addb542d40c5a4 still has ***; develop 8860aa2a6801eba80ceaee45c4c91bee8f1e3344 has Basic auth.
- Run 41551273613 checked out main 74dd7659 and therefore did not execute PR 1342. Existing secret presence is confirmed by masked environment; validity remains unproven.
