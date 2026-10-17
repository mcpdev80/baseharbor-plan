---
id: t-20261017-inspect-import-ci-coverage
type: task
areas: [ci, inspect]
release: v0.4.x
version: ""
parent: v0.4.x
owner: "mcpdev80 (core-751 trusted import coverage)"
priority: ""
depends_on: [core-893, core-895, core-896]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#983]
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261017-inspect-import-ci-coverage · CI: qualify import detector tests without path exemptions #task #release/v0-4-x #status/review #view/review #area/ci #area/inspect #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (core-751 trusted import coverage)  
    **PR:** [baseharbor#983](https://github.com/mcpdev80/baseharbor/pull/983)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.x](../releases/v0.4.x.md)  
**Depends on:** [core-893](core-893-ci-enforce-selected-pr-checks.md), [core-895](core-895-reviews-require-maintainer-approval.md), [core-896](core-896-runners-isolate-parallel-pr-checks.md)  
**Required by:** [core-751](core-751-inspect-no-false-positives-comments-text.md)  
**Owner:** mcpdev80 (core-751 trusted import coverage)  
**Priority:** not set  
**PRs:** [baseharbor#983](https://github.com/mcpdev80/baseharbor/pull/983)  
**Source:** 
<!-- /generated:links -->

## Goal

Qualify targeted import-detector coverage for core-751 through the existing trusted planner, executor and final check. No authorization for unreviewed product code.

## Scope

- Own only scripts/pr-gate-plan.py and targeted policy regression tests. No ci.yml, CI workflow, runtime, inspector implementation, core-918 or core-894 edits.
- Existing inspect-gofmt, inspect-package-tests, inspect-vet, inspect-consumer-tests and inspect-consumer-build remain mandatory. Prove real executable runner routes and enforced final outcomes.
- Before any future `coverage_status: resolved`, require independent review of the exact product source and immutable source/ancestry binding; path-only approval is prohibited.

## Acceptance

- A bounded import-detector coverage route is identified and validated with the existing runner/checker.
- Absent, skipped and failed required validations, extra changed files, rename/deletion and unreviewed content cannot qualify.
- No release matrix and no self-approval.

## Handoff

- 2026-10-17 independent product review of [#984](https://github.com/mcpdev80/baseharbor/pull/984), exact head `31ea5a733a039499864dcc06db4539065cfe063f`: **CHANGES REQUIRED**; see [review comment 6233499789](https://github.com/mcpdev80/baseharbor/pull/984#issuecomment-6233499789). Demonstrated source-level counterexamples: valid JS/TS regex after `return` incorrectly classified as import; object method `.require('mongodb')` incorrectly classified as CommonJS require; Python `import os, pymongo` misses the second module. Focused Actions [39029788478](https://github.com/mcpdev80/baseharbor/actions/runs/39029788478): inspect package/vet/consumer tests/build success, inspect-gofmt **failed**, final `PR Selected Checks` **failed** (unresolved source coverage and missing required gofmt). No independently qualified source binding is permitted yet. Policy [#983](https://github.com/mcpdev80/baseharbor/pull/983) remains unchanged/fail-closed at `25e5f8e1d71340afff415648374f4dcfa2407aee`; no policy acceptance or merge. This review is not an implementation takeover; preserve the existing product owner and task claim. Regenerate planning views only if metadata changes; this paragraph changes no generated status or ownership.

- Hosted evidence: policy [run 39027850408](https://github.com/mcpdev80/baseharbor/actions/runs/39027850408) SUCCESS for exact commit `25e5f8e1d71340afff415648374f4dcfa2407aee` (Trusted Plan, Workflow policy, Focused Python, pr-planner-tests, CI executor/verifier and authenticated PR Selected Checks). No native/release jobs selected. Planning [run 39028118807](https://github.com/mcpdev80/baseharbor-plan/actions/runs/39028118807) SUCCESS for rendered task/Ready/roadmap, with planning tests. Independent acceptance remains pending; source content binding cannot be claimed before a reviewed core-751 implementation exists.


- Review candidate [PR #983](https://github.com/mcpdev80/baseharbor/pull/983), product SHA `25e5f8e1d71340afff415648374f4dcfa2407aee`, from develop `d54ac358fb6a6b256164ac2689a33e981c013baa`. Changes only `scripts/pr-gate-plan.py` and `scripts/test_pr_gate_plan.py`. The five existing Inspect checks are required for the exact prospective detector path set. The candidate is intentionally fail-closed for unreviewed product content; independently reviewed source binding is a later prerequisite, not something this PR pretends to have done. Real planner and final verifier remain authoritative. No ci.yml or runtime changes.


- Claim published 2026-10-17. The existing planner resolves only the two reviewed reconciliation files; import-detector source is fail-closed even while all five inspect checks are selected. This predecessor must not declare future unreviewed detector changes resolved.
