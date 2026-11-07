---
id: t-20261103-ci-plain-checks
card_number: "0427-099"
card_short_title: "remove evidence verification"
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: ""
owner: "Codex (Owner CI simplification 2026-11-03)"
kanban_lane: closed
kanban_summary: "Owner explicitly authorizes complete removal of gate manifests, CI evidence collection/reverification, receipt approval/shadow…"
kanban_status: closed
kanban_title: "0427-099 · remove evidence verification"
priority: critical
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1345, mcpdev80/baseharbor#1346, mcpdev80/baseharbor-demo#127, mcpdev80/baseharbor-console#16, mcpdev80/baseharbor-node-connector#18]
sources: []
blocker: ""
resolution: accepted
evidence: [https://github.com/mcpdev80/baseharbor/pull/1345, https://github.com/mcpdev80/baseharbor/pull/1346, https://github.com/mcpdev80/baseharbor-demo/pull/127, https://github.com/mcpdev80/baseharbor-console/pull/16, https://github.com/mcpdev80/baseharbor-node-connector/pull/18]
---

- [x] t-20261103-ci-plain-checks · CI: remove evidence verification and keep normal checks plus commit receipts #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** Codex (Owner CI simplification 2026-11-03) · **Priority:** critical  
    **PR:** [baseharbor#1345](https://github.com/mcpdev80/baseharbor/pull/1345), [baseharbor#1346](https://github.com/mcpdev80/baseharbor/pull/1346), [baseharbor-demo#127](https://github.com/mcpdev80/baseharbor-demo/pull/127), [baseharbor-console#16](https://github.com/mcpdev80/baseharbor-console/pull/16), [baseharbor-node-connector#18](https://github.com/mcpdev80/baseharbor-node-connector/pull/18)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1345), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1346), [proof 3](https://github.com/mcpdev80/baseharbor-demo/pull/127), [proof 4](https://github.com/mcpdev80/baseharbor-console/pull/16), [proof 5](https://github.com/mcpdev80/baseharbor-node-connector/pull/18)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Required by:** [core-766](core-766-cleanup-orphaned-owned-runtime-resources.md), [core-815](core-815-tests-greenfield-stacks-native-runtimes.md), [t-20261022-r27-ci-access](t-20261022-r27-ci-access.md), [t-20261022-r27-ci-authority](t-20261022-r27-ci-authority.md), [t-20261022-r27-ci-delivery](t-20261022-r27-ci-delivery.md), [t-20261022-r27-ci-runtime](t-20261022-r27-ci-runtime.md), [t-20261103-ci-routing-audit](t-20261103-ci-routing-audit.md)  
**Owner:** Codex (Owner CI simplification 2026-11-03)  
**Priority:** critical  
**PRs:** [baseharbor#1345](https://github.com/mcpdev80/baseharbor/pull/1345), [baseharbor#1346](https://github.com/mcpdev80/baseharbor/pull/1346), [baseharbor-demo#127](https://github.com/mcpdev80/baseharbor-demo/pull/127), [baseharbor-console#16](https://github.com/mcpdev80/baseharbor-console/pull/16), [baseharbor-node-connector#18](https://github.com/mcpdev80/baseharbor-node-connector/pull/18)  
**Source:** 
<!-- /generated:links -->

## Goal

Owner explicitly authorizes complete removal of gate manifests, CI evidence collection/reverification, receipt approval/shadow chains and evidence reuse from CI, Pre-Release and Release. Normal tests remain mandatory. The only CI receipt is a small Planning file containing merge commit SHA and PR number. Rulesets stay disabled; no release or tag.

## Scope and ownership

- Product branch codex/ci-plain-checks owns CI/release workflows, evidence-only CI scripts/tests and their current documentation.
- Preserve active product claims and the separate unpublished authority-package correction; integrate only the normal package check needed by the current work.
- Coordinator owns ci.yml, planner/executor/final-check integration and minimal writer.
- Parallel release lane owns pre-release.yml, pre-release-runtime-suite.yml, release.yml, supplemental-release-validation.yml and release-only evidence helpers.
- Parallel workflow lane owns other runtime/acceptance workflows and evidence-only upload/collection steps.
- Parallel documentation/planning lane owns current CI documentation and superseding old receipt/evidence planning criteria.
- Historical release records and old receipt data remain unchanged.

## Acceptance

Normal selected CI and release test execution fail on failing/missing required jobs without Actions API or artifact evidence re-verification. No live/retained receipt verifier or separate approval workflow remains active. Commit receipts retain SHA/PR binding and safe publication. Focused regression tests, workflow policy and actionlint pass. Planning render/check pass.

## Handoff

- Owner-authorized acceptance: Core #1345 is merged to develop as 01784c388666cea9d656b5a383bf594c45c86ff7 after every normal selected check, including the final check, passed on source 5fa8d9896f880d0d2bf5a5775c1ee7c8a95bcdce. The default-main CI-only deployment #1346 is merged as 60e198fa04271a5aa6660ffc069a24100fb8c704 after its hosted workflow-policy check and local source-only checks. No product code was promoted from develop to main.
- Demo #127, Console #16 and Connector #18 are merged. Their ordinary tests remain; their CI receipt/manifest publishers and uploads are removed. Console/Connector normal source CI passed; Demo has no PR-triggered workflow and its narrow upload removal passed local workflow validation.
- Normal PR completion uses workflow dependency results, not Actions API job lookup or evidence artifacts. Pre-Release executes selected tests directly; Release executes the full normal Pre-Release workflow for its exact tag. Build inputs and published artifact provenance remain. No full release/native matrix was launched for this CI-only change.
- The normal automatic merge event wrote evidence/receipts/commits/01784c388666cea9d656b5a383bf594c45c86ff7.json containing only commit and pull_request. The writer does not inspect CI. No new credential was needed.
- Local combined regression run: 297 tests passed. Final hosted-runner/shallow-checkout changes passed 34 focused regressions and all-workflow actionlint/policy. EN/DE audit and both hosted MkDocs builds passed. Planning validation has no errors; remaining warnings concern active product dependency states.
- Core drafts #1321/#1325/#1328 are closed as superseded. Historical releases and old receipts remain unchanged. Current task dependencies, release templates and generated CardBoard views use normal checks.
- #1324 documentation was repaired in its own branch at 0db72d3529689a3deaba037cb921ddcebd9db810 and its complete normal CI passed. Product acceptance remains with the assigned contract owner.
- #1333 was replanned after integration via a source-identical commit db5fe1dc3d88ec4831343b749136ac1580df19b8. Its complete normal CI passed, including delivery-package-tests and the final check; no product source was changed.
- Rulesets remain disabled. No release or tag was created. Original unpublished authority-check work remains preserved in its original worktree; no independent review is claimed.
