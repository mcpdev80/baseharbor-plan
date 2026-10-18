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
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/983", "https://github.com/mcpdev80/baseharbor/commit/980e8db8b93c09db61ac8a0ea873bc6f43d1dedf", "https://github.com/mcpdev80/baseharbor/actions/runs/39115837200"]
---

- [x] t-20261017-inspect-import-ci-coverage · CI: qualify import detector tests without path exemptions #task #release/v0-4-x #status/closed #view/closed #board/planned #area/ci #area/inspect #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (core-751 trusted import coverage)  
    **PR:** [baseharbor#983](https://github.com/mcpdev80/baseharbor/pull/983)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/983), [proof 2](https://github.com/mcpdev80/baseharbor/commit/980e8db8b93c09db61ac8a0ea873bc6f43d1dedf), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/39115837200)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
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

### 2026-10-18 — Maintainer policy accepted and merged
- [Independent review 5562448322](https://github.com/mcpdev80/baseharbor/pull/983#pullrequestreview-5562448322) accepted exact policy `a23adb72f4e004beab01ec2f605c28ddd8ff6bbe`. Actual CI 39115837200 was fully green, with strict required PR Selected Checks.
- PR #983 was regularly squash-merged to develop at `980e8db8b93c09db61ac8a0ea873bc6f43d1dedf`, following the live allowed squash-only Maintainer PR path. No GitHub self-approval or CI bypass. The merged branch is no longer available via the repository branch endpoint.
- Product #984 was updated by a normal two-parent develop merge at `8c2ce09975fe3ed6722cd06a2b19848969c8f9a1`, preserving its two reviewed source blobs and applying only trusted target changes. Await actual new CI before product merge.
- #991 now has a real conflict in shared planner/test files with integrated #983. Any conflict resolution requires independent inspection and, where the clean-tree proof no longer applies, a new immutable qualification. Never silently extend the old source approval.
- Canonical accepted/closed transition and generated views still need validated render/check/tests by the executable Planning owner; this append records the actual acceptance/merge without claiming those pending runs. No release acceptance.


- 2026-10-17 independent re-review of revised [#984](https://github.com/mcpdev80/baseharbor/pull/984), exact product HEAD `4b7a0371dc6dada7eb283290d4ad9bac62efc018`: **CHANGES REQUIRED**, [review comment 6233783222](https://github.com/mcpdev80/baseharbor/pull/984#issuecomment-6233783222). Earlier three findings (regex after return, member require, Python comma imports) appear corrected in actual source and fixture changes. All five targeted Inspect jobs in [39030351947](https://github.com/mcpdev80/baseharbor/actions/runs/39030351947) SUCCESS. New adjacent valid JS control-statement regex `if (ready) /import 'mongodb'/.test(text);` is mis-tokenized after `)` and falsely produces `EvidenceImport`; add direct and integrated negative regressions for control-condition contexts. `PR Selected Checks` remains FAILURE due unresolved source coverage, as designed. Do not bind reviewed source into [#983](https://github.com/mcpdev80/baseharbor/pull/983) before independent positive content review. Product and policy branches untouched; independent review remains pending, no acceptance or merge.

- 2026-10-17 independent product review of [#984](https://github.com/mcpdev80/baseharbor/pull/984), exact head `31ea5a733a039499864dcc06db4539065cfe063f`: **CHANGES REQUIRED**; see [review comment 6233499789](https://github.com/mcpdev80/baseharbor/pull/984#issuecomment-6233499789). Demonstrated source-level counterexamples: valid JS/TS regex after `return` incorrectly classified as import; object method `.require('mongodb')` incorrectly classified as CommonJS require; Python `import os, pymongo` misses the second module. Focused Actions [39029788478](https://github.com/mcpdev80/baseharbor/actions/runs/39029788478): inspect package/vet/consumer tests/build success, inspect-gofmt **failed**, final `PR Selected Checks` **failed** (unresolved source coverage and missing required gofmt). No independently qualified source binding is permitted yet. Policy [#983](https://github.com/mcpdev80/baseharbor/pull/983) remains unchanged/fail-closed at `25e5f8e1d71340afff415648374f4dcfa2407aee`; no policy acceptance or merge. This review is not an implementation takeover; preserve the existing product owner and task claim. Regenerate planning views only if metadata changes; this paragraph changes no generated status or ownership.

- Hosted evidence: policy [run 39027850408](https://github.com/mcpdev80/baseharbor/actions/runs/39027850408) SUCCESS for exact commit `25e5f8e1d71340afff415648374f4dcfa2407aee` (Trusted Plan, Workflow policy, Focused Python, pr-planner-tests, CI executor/verifier and authenticated PR Selected Checks). No native/release jobs selected. Planning [run 39028118807](https://github.com/mcpdev80/baseharbor-plan/actions/runs/39028118807) SUCCESS for rendered task/Ready/roadmap, with planning tests. Independent acceptance remains pending; source content binding cannot be claimed before a reviewed core-751 implementation exists.


- Review candidate [PR #983](https://github.com/mcpdev80/baseharbor/pull/983), product SHA `25e5f8e1d71340afff415648374f4dcfa2407aee`, from develop `d54ac358fb6a6b256164ac2689a33e981c013baa`. Changes only `scripts/pr-gate-plan.py` and `scripts/test_pr_gate_plan.py`. The five existing Inspect checks are required for the exact prospective detector path set. The candidate is intentionally fail-closed for unreviewed product content; independently reviewed source binding is a later prerequisite, not something this PR pretends to have done. Real planner and final verifier remain authoritative. No ci.yml or runtime changes.


- Claim published 2026-10-17. The existing planner resolves only the two reviewed reconciliation files; import-detector source is fail-closed even while all five inspect checks are selected. This predecessor must not declare future unreviewed detector changes resolved.

- 2026-10-18 assigned #983 writer claim: exclusively `scripts/pr-gate-plan.py` and `scripts/test_pr_gate_plan.py`. Add immutable exact-SHA/status qualification for positively reviewed #984 (`9fcc77cd1feb0bf02e7647aa64bc02a2ebb47ae2`, review 5560608936) and integrated #991 (`ba577f0384b291ad01f8e4530ffe80119aa34c06`, review 5562278686). Keep source qualification separate from check execution; no change to #991/product PRs. Before publishing verify genuine `pr-diff-base.py` Git resolution, clean trusted develop merge and rejection of descendants/unavailable checks. No merge or self-acceptance.

- 2026-10-18 immutable coverage policy candidate for independent Manager review: [#983](https://github.com/mcpdev80/baseharbor/pull/983) exact SHA `a23adb72f4e004beab01ec2f605c28ddd8ff6bbe`. Binds positive reviews 5560608936 (#984 `9fcc77cd1feb0bf02e7647aa64bc02a2ebb47ae2`, exact 2-file changed status, all five Inspect validations) and 5562278686 (#991 `ba577f0384b291ad01f8e4530ffe80119aa34c06`, exact 4-file changed status and CI planner/executor validation checks). Real `pr-diff-base.py` Git integration fixture tests both unchanged reviewed source and normal trusted-develop merge, rejects unreviewed descendant, missing/extra/renamed/deleted/status-changed paths and unverified inputs. Existing strict final verifier still blocks missing/skip/fail checks; no path-wide allowlist. Exact-SHA isolated [HF job 6ad492905ccb47ba0f7c316a](https://huggingface.co/jobs/ThunderHawk1080/6ad492905ccb47ba0f7c316a): 44 planner tests PASS, Python compile and diff check PASS. [Product CI 39115837200](https://github.com/mcpdev80/baseharbor/actions/runs/39115837200) must be read for final status. No acceptance, merge, #991 or product modifications.

- 2026-10-18 accepted/merged: Maintainer review [5562448322](https://github.com/mcpdev80/baseharbor/pull/983#pullrequestreview-5562448322), exact policy candidate `a23adb72f4e004beab01ec2f605c28ddd8ff6bbe`, [CI 39115837200](https://github.com/mcpdev80/baseharbor/actions/runs/39115837200) including required `PR Selected Checks` SUCCESS; merged into develop at exact `980e8db8b93c09db61ac8a0ea873bc6f43d1dedf`. This accepts only immutable reviewed #984/#991 bindings; subsequent conflict resolution and altered SHA still demand independent review, not inherited qualification.
