---
id: core-915
areas: [wizard]
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: "mcpdev80 (core-915)"
depends_on: [core-910, t-20261016-wizard-task-ci-readiness]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#969]
sources: ["mcpdev80/baseharbor#915"]
source_updated: "2026-10-15T16:46:34Z"
labels: [area/dx]
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/969", "https://github.com/mcpdev80/baseharbor/commit/701d9ac4f6e5b78658a4f429ad406f31087d44d9", "https://github.com/mcpdev80/baseharbor/actions/runs/38911659557"]
---

- [x] core-915 · Preview: explain provider consequences and partial results #task #release/v0-4-26 #status/closed #view/closed #board/planned #area/wizard #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (core-915) · **Priority:** not set  
    **PR:** [baseharbor#969](https://github.com/mcpdev80/baseharbor/pull/969)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/969), [proof 2](https://github.com/mcpdev80/baseharbor/commit/701d9ac4f6e5b78658a4f429ad406f31087d44d9), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/38911659557)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-910](core-910-wizard-shared-read-only-editing-state.md), [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md)  
**Required by:** [core-916](core-916-wizard-back-cancel-eof-no-side-effects.md)  
**Owner:** mcpdev80 (core-915)  
**Priority:** not set  
**PRs:** [baseharbor#969](https://github.com/mcpdev80/baseharbor/pull/969)  
**Source:** [baseharbor#915](https://github.com/mcpdev80/baseharbor/issues/915)
<!-- /generated:links -->

## Goal

Before confirmation and after execution, the actual consequences for every supported provider are understandable. Lane: read-only presentation.

## Scope

- In scope: separate `app_change_preview`/`result_presenter` files and tests, consuming existing ProviderChange plan/result types.
- Out of scope: UI-local impact engines or special blockers.

## Acceptance

- Distinguishes add, stop, remove, replace and capability deselection; affected apps/functions/data locations, PKI/token renewal and required actions come from the real plan.
- Intended destructive decisions are possible through the existing explicit/double confirmation; no UI-specific blocker and no ownership/security bypass.
- After success or partial failure, shows actual dispositions/remaining state and the next step; no generic warning lists or invented substitute locations.

## Required checks

- Typed fixtures across all relevant existing consequence classes, safe continuation, destructive alternative, partial execution and secret redaction; no runtime.

## Dependencies and file ownership

- Depends on core-910. Shared v0.4.26 PR/review/runner foundation (#890–#893, #895, #896) must be qualified first.

## Autonomous execution contract — 2026-10-16

- **Owned files:** `cmd/baha/app_change_preview.go`, `app_change_preview_test.go`, `app_change_result_presenter.go` and `app_change_result_presenter_test.go` only.
- **Delivered interface/result:** Consume existing authoritative ProviderChange plan/result types; deliver pure before/after and partial-result presentation. Use the already merged domain types directly; do not define a competing consequence model.
- **Task-specific proof:** `TestAppChangePreview*` and `TestAppChangeResultPresenter*`: existing typed consequence classes, locations/access/renewal, destructive alternatives, partial execution and redaction.
- **Boundary:** No changes to footprint presenter, hydration, controller, domain/lifecycle/consent authorities or shared printing/registration helpers. This component never authorizes or executes a mutation.
- **Assignment gate:** use only accepted dependencies and APIs already present on develop. Confirm that the trusted plan/executor runs these exact test families on this task's file set and checks their outcomes. A plan that reports unresolved is not execution-ready. The CI-readiness inventory is maintained by [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md); later gaps become an explicit prerequisite before assignment, never an instruction to wait for another running session.
- **End-to-end owner:** the assigned session handles integration, implementation, focused tests, hosted CI observation, demonstrated fixes and its planning handoff. It reads other task states itself from planning main and preserves concurrent updates. No shared CI edits, dependency work-in-progress or manual message relay through Marcel. Normal independent review/Maintainer acceptance remains a boundary, not an implementation dependency.

## Handoff

- 2026-10-16 independent Maintainer acceptance: **accepted and merged** via [PR #969](https://github.com/mcpdev80/baseharbor/pull/969), squash commit `701d9ac4f6e5b78658a4f429ad406f31087d44d9` on product `develop`. Source `fbcb544ddad22e27e44b0218437a7ec62abb6569` now projects authoritative material meaning/validity, function behavior, prerequisite consequences and safe structural access/security facts; raw endpoints, identifiers and evidence remain excluded. Proposed and executed states stay separate; canonical result/pending owners remain in use. [Run 38911659557](https://github.com/mcpdev80/baseharbor/actions/runs/38911659557), attempt 1, SUCCESS at integration `ff620752a8f8973c2473e3ac13e2c4999eec7f08` over trusted base `1c78c509ffc2846e76ed1b27bc39f478948b1cb0`; logs confirm ten tests across both mandatory families and all source/format/vet/build/Python/policy/final checks green. Current develop is already integrated; only the four owned files changed. No runtime matrix. Planning and concurrent core-920 handoff preserved, generated views rendered and validated with 0 errors/0 warnings and all 38 tests before publication. This closes presentation and makes core-916 ready; controller/wiring/mutation and release acceptance remain separate.

- 2026-10-16 correction for independent review #5548584406, [product PR #969](https://github.com/mcpdev80/baseharbor/pull/969): exact source HEAD `fbcb544ddad22e27e44b0218437a7ec62abb6569`, trusted develop base `1c78c509ffc2846e76ed1b27bc39f478948b1cb0`, PR integration SHA `ff620752a8f8973c2473e3ac13e2c4999eec7f08`. Current develop integrated normally through [PR #971](https://github.com/mcpdev80/baseharbor/pull/971); 0 commits behind and only four owned presenter/test files changed. No force push.
- The read-only preview now surfaces existing `MaterialConsequence.Meaning`, material validity dates and remaining validity, `FunctionConsequence.Behavior` and remaining function validity, and `ProviderPrerequisite.Consequence`. Before/proposed provider and material accesses expose only structural secure-binding properties (identity present, reference counts, lifecycle renewable/rotatable/revocable); absent access is explicitly unknown. Proposed access is labelled unverified, not claimed actual. The after-execution presenter similarly displays only actual receipt access structure and `ProviderFunctionOutcome.Behavior`, with verified flags; pending/failed operations remain controlled by `RecordProviderChangeResult` and `PendingProviderChanges`.
- Typed `TestAppChangePreview*` and `TestAppChangeResultPresenter*` regressions assert exact authoritative PKI certificate-retention/renewal limitation, token/lease validity behavior, prerequisite consequence, secure access before/proposed/actual, supported rebind and destructive alternative explanations, observed partial outcomes, and withheld methods/endpoints/credentials/secret references/evidence. No derived consequence, impact engine, mutation, domain/consent/controller/workflow change.
- [Exact GitHub-hosted run 38911659557](https://github.com/mcpdev80/baseharbor/actions/runs/38911659557) **SUCCESS**: Trusted Plan, Workflow policy, Focused Python, `wizard-change-presentation-tests` (both mandatory families executed), `cli-gofmt`, `cli-vet`, `cli-build`, `source-contracts`, and binding `PR Selected Checks`. No runtime/container/full release matrix. Earlier candidates exposed formatting and invalid typed fixtures and were corrected before the final green integration.
- Remains **review**. Independent Maintainer re-review required; no author merge or acceptance. No other task started.


- 2026-10-16 independent Maintainer review at `666e542949d37e19e44f995c0018ff4207923469`: **changes required, not accepted or merged**. Read-only plan/result separation and canonical result/pending authorities are appropriate, but the presenter omits required explanation classes: `MaterialConsequence.Meaning` (including retention versus future renewal/recoverability), function `Behavior`, prerequisite `Consequence` and material validity details. It also hides all access/security data rather than projecting non-secret before/proposed/actual consequences; actual function behavior is omitted. Show existing authoritative explanation and safe structural access/security facts without dumping endpoints, credentials or evidence, and preserve unknown/unverified distinctions. Add authority-backed typed fixtures for retained certificate/lease/token renewal limits, prerequisite explanations, safe access/security changes, supported continuation/destructive alternatives and observed partial results; no UI-local inference. Hosted run `38908808009` genuinely executed both required families (seven tests) at integration `ca3161e05804017382b14158c0a529b48e59d872`; the omitted semantics remain unproven despite green required CI. Planning main `3170bef` independently passes render/check unchanged, 0 errors/0 warnings and all 38 tests. Continue only the four owned files, integrate latest develop normally (core-911 merged), obtain focused CI and publish a validated handoff.

- 2026-10-16 independent review handoff for [product PR #969](https://github.com/mcpdev80/baseharbor/pull/969), branch `feature/core-915-change-consequence-presenters`. Source HEAD `666e542949d37e19e44f995c0018ff4207923469`; trusted develop base `b3428843bc8f04156339a7b7f6d1e0ed6fa955d6`; GitHub PR integration SHA `ca3161e05804017382b14158c0a529b48e59d872`. Branch is 0 behind develop; normal history without force push or merge into develop.
- Implemented strictly four owned files: `cmd/baha/app_change_preview.go`, `app_change_preview_test.go`, `app_change_result_presenter.go`, `app_change_result_presenter_test.go`. Present `ProviderImpactPlan` and `ProviderChangeResult` as pure read-only views; operation/scenario including add/stop/remove/replace/deselection, observed functions/consumers, material dispositions, observed data/recovery locations, operation effects and required prerequisites. After execution `RecordProviderChangeResult` and `PendingProviderChanges` remain the authoritative basis for applied/failed/pending results, remaining work and fresh-consent/replan guidance; proposals never masquerade as verified execution. No UI blocker, mutation, consent change or invented destination. Evidence, provider access, endpoints and credential material deliberately never printed; redaction tested.
- [Hosted targeted run 38908808009](https://github.com/mcpdev80/baseharbor/actions/runs/38908808009): **SUCCESS** Trusted Plan, Workflow policy, Focused Python, `wizard-change-presentation-tests` executing both required `TestAppChangePreview*` and `TestAppChangeResultPresenter*` families, `cli-gofmt`, `cli-vet`, `cli-build`, `source-contracts`, and authenticated **PR Selected Checks**. No container/runtime/release matrix.
- Review boundary: not accepted; independent Maintainer approval/merge required. No further task started.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
