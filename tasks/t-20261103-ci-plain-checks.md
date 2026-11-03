---
id: t-20261103-ci-plain-checks
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: ""
owner: "Codex (Owner CI simplification 2026-11-03)"
priority: critical
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1345, mcpdev80/baseharbor-demo#127, mcpdev80/baseharbor-console#16, mcpdev80/baseharbor-node-connector#18]
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261103-ci-plain-checks · CI: remove evidence verification and keep normal checks plus commit receipts #task #release/v0-4-27 #status/active #view/active #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** Codex (Owner CI simplification 2026-11-03) · **Priority:** critical  
    **PR:** [baseharbor#1345](https://github.com/mcpdev80/baseharbor/pull/1345), [baseharbor-demo#127](https://github.com/mcpdev80/baseharbor-demo/pull/127), [baseharbor-console#16](https://github.com/mcpdev80/baseharbor-console/pull/16), [baseharbor-node-connector#18](https://github.com/mcpdev80/baseharbor-node-connector/pull/18)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Required by:** [core-766](core-766-cleanup-orphaned-owned-runtime-resources.md), [core-815](core-815-tests-greenfield-stacks-native-runtimes.md), [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261022-r27-ci-access](t-20261022-r27-ci-access.md), [t-20261022-r27-ci-authority](t-20261022-r27-ci-authority.md), [t-20261022-r27-ci-delivery](t-20261022-r27-ci-delivery.md), [t-20261022-r27-ci-runtime](t-20261022-r27-ci-runtime.md)  
**Owner:** Codex (Owner CI simplification 2026-11-03)  
**Priority:** critical  
**PRs:** [baseharbor#1345](https://github.com/mcpdev80/baseharbor/pull/1345), [baseharbor-demo#127](https://github.com/mcpdev80/baseharbor-demo/pull/127), [baseharbor-console#16](https://github.com/mcpdev80/baseharbor-console/pull/16), [baseharbor-node-connector#18](https://github.com/mcpdev80/baseharbor-node-connector/pull/18)  
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

- Implementation published as Core #1345 (b52c97744f5cd2db4d600cd7047ebfa018569bbd), Demo #127, Console #16 and Connector #18. Normal hosted checks are running; no merge acceptance is claimed yet.
- The normal Delivery package route also fixes current PR #1333's sole final-check failure (unknown impact for internal/delivery/contract_test.go); its documentation checks are already green.
- Local planner (143) and runner (23) regressions, receipt/source/frozen-source checks, all-workflow actionlint and EN/DE documentation audit passed. Combined final regression run is pending completion. Planning checks: zero errors; remaining warnings are product dependency states.
- Existing unpublished authority-check work is preserved in its original worktree; equivalent normal package routing is included here. The earlier authority-coverage task is superseded by this integrated change.
- Rulesets remain disabled. No release, tag or full runtime dispatch was performed.
