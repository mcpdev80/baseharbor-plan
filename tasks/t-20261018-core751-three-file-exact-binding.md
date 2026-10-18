---
id: t-20261018-core751-three-file-exact-binding
type: task
areas: [ci, inspect]
release: v0.4.x
parent: v0.4.x
owner: "mcpdev80 (independent reviewed source binding)"
priority: high
depends_on: [t-20261018-reviewed-policy-991-982-binding]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#997]
sources: []
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/997#pullrequestreview-5562680081", "https://github.com/mcpdev80/baseharbor/actions/runs/39122188814", "https://github.com/mcpdev80/baseharbor/commit/58efa1a3bc796f93f0ddead7ca0042e37bbd0705"]
---

- [x] t-20261018-core751-three-file-exact-binding · Reviewed #984 three-file immutable Inspect coverage #task #release/v0-4-x #status/closed #view/closed #area/ci #area/inspect #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (independent reviewed source binding) · **Priority:** high  
    **PR:** [baseharbor#997](https://github.com/mcpdev80/baseharbor/pull/997)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.x](../releases/v0.4.x.md)  
**Depends on:** [t-20261018-reviewed-policy-991-982-binding](t-20261018-reviewed-policy-991-982-binding.md)  
**Owner:** mcpdev80 (independent reviewed source binding)  
**Priority:** high  
**PRs:** [baseharbor#997](https://github.com/mcpdev80/baseharbor/pull/997)  
**Source:** 
<!-- /generated:links -->

## Claim and file ownership

- 2026-10-18: exclusive policy follow-up owner of `scripts/pr-gate-plan.py` and `scripts/test_pr_gate_plan.py` on a new draft PR against current develop; no product/other PR changes or GitHub issue.
- Reviewed #984 SHA `cf0a19bc4c8f398d7ee3fc07a635833168081ff5`, independent review 5562635114; exact status set: `internal/repositoryinspect/capability_detection_runtime.go` modified; `capability_detection_js_context.go` added; `capability_import_detection_test.go` added.
- Retain all five Inspect validations, existing independently approved source bindings, genuine clean develop merge-tree proof and fail-closed diff-base changes/status negatives. No reusable path exception, own coverage approval, live test or merge.

## Handoff

- Planning claim published before policy modification; Manager independently reviews exact new SHA after targeted CI.

- 2026-10-18 Manager review handoff: [Draft PR #997](https://github.com/mcpdev80/baseharbor/pull/997) at exact SHA `8ab7f8dc0aca618a6d5e516d91be865f24206f18`; approved source `cf0a19bc4c8f398d7ee3fc07a635833168081ff5` bound to three exact file statuses and five Inspect mandatory checks. [HF 6ad4a76cc6628814522733d6](https://huggingface.co/jobs/ThunderHawk1080/6ad4a76cc6628814522733d6) 45 Planner and 10 Diff-Base regressions PASS, compilation/diff check PASS. CI pending. No merge or self-acceptance.

### 2026-10-18 — Independent Maintainer acceptance and merge

- Policy reviewed at `8ab7f8dc0aca618a6d5e516d91be865f24206f18` (review 5562672390); normal two-parent trusted-develop integration after #982 produced `5595441c6fa444ebc520e736d13f9dffd02dd96b` with unchanged planner/test blobs (review 5562680081).
- Actual fresh [CI 39122188814](https://github.com/mcpdev80/baseharbor/actions/runs/39122188814) fully green including mandatory authenticated PR Selected Checks. Regular squash merge completed to develop `58efa1a3bc796f93f0ddead7ca0042e37bbd0705`; no self-approval or mandatory CI bypass.
- Canonical policy task accepted/closed. Product #984 itself remains pending current-develop integration and actual green mandatory CI before merge. Derived Planning views require executable render/check/tests from current main; manager local environment offline and HF Jobs connector UNAVAILABLE, no new executable Planning validation claimed.
