---
id: core-916
areas: [wizard]
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: "mcpdev80 (core-916 controller)"
depends_on: [core-912, core-913, core-914, core-915]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#972]
sources: ["mcpdev80/baseharbor#916"]
source_updated: "2026-10-15T16:46:28Z"
labels: [area/dx]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-916 · Wizard: handle back, cancel and EOF without side effects #task #release/v0-4-26 #status/review #view/review #area/wizard #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (core-916 controller) · **Priority:** not set  
    **PR:** [baseharbor#972](https://github.com/mcpdev80/baseharbor/pull/972)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-912](core-912-wizard-needs-first-selection.md), [core-913](core-913-wizard-compatible-providers-same-view.md), [core-914](core-914-preview-actual-footprint.md), [core-915](core-915-preview-provider-consequences-partial-results.md)  
**Required by:** [core-917](core-917-app-new-connect-wizard-lifecycle.md), [core-918](core-918-app-edit-apply-confirmed-changes.md)  
**Owner:** mcpdev80 (core-916 controller)  
**Priority:** not set  
**PRs:** [baseharbor#972](https://github.com/mcpdev80/baseharbor/pull/972)  
**Source:** [baseharbor#916](https://github.com/mcpdev80/baseharbor/issues/916)
<!-- /generated:links -->

## Goal

No returns to the retained selection as often as needed; cancel writes nothing. Lane: TUI control.

## Scope

- In scope: separate wizard controller/state machine files and tests; components only through agreed interfaces.
- Out of scope: lifecycle or registry wiring.

## Acceptance

- Capability and provider selections and complex original data are retained on every return.
- Cancel/EOF/context cancel and unsuitable non-TTY/`--no-input` use cause no hidden file, profile, Target, credential or runtime writes.
- The preview controller and execution hook are cleanly separated; actual mutation only after existing valid consent.

## Required checks

- Sequence/PTY tests for repeated No, changed selection, abort at every transition and EOF; filesystem/state snapshots with controlled fakes; no runtime.

## Dependencies and file ownership

- Depends on core-912, core-913, core-914 and core-915. Shared v0.4.26 PR/review/runner foundation (#890–#893, #895, #896) must be qualified first.

## Autonomous execution contract — 2026-10-16

- **Owned files:** `cmd/baha/app_wizard_controller.go` and `cmd/baha/app_wizard_controller_test.go` only.
- **Delivered interface/result:** Compose the already accepted selection/provider/presenter components using their exported-to-package APIs. Return a decision and state to the caller; execution remains behind the existing authorized lifecycle hook.
- **Task-specific proof:** `TestAppWizardController*`: repeated back, retained dual selection, cancellation/EOF/context cancellation/non-TTY/no-input at every transition and no-write snapshots.
- **Boundary:** No changes to component internals, shared models or New/Edit registration. If a component contract is missing, repair it before this task is assigned, not while another session implements it.
- **Assignment gate:** use only accepted dependencies and APIs already present on develop. Confirm that the trusted plan/executor runs these exact test families on this task's file set and checks their outcomes. A plan that reports unresolved is not execution-ready. The CI-readiness inventory is maintained by [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md); later gaps become an explicit prerequisite before assignment, never an instruction to wait for another running session.
- **End-to-end owner:** the assigned session handles integration, implementation, focused tests, hosted CI observation, demonstrated fixes and its planning handoff. It reads other task states itself from planning main and preserves concurrent updates. No shared CI edits, dependency work-in-progress or manual message relay through Marcel. Normal independent review/Maintainer acceptance remains a boundary, not an implementation dependency.

## Handoff

- 2026-10-16 independent Maintainer review at `8870c311ad4a7b7dc923a5475b441dafd7fbf74b`: **changes required, not accepted or merged**. Pure navigation/no-execution and cancellation/copy boundaries are appropriate, but initial Footprint/Impact pointers are never refreshed or invalidated when needs/provider choices change; confirmation can return new intent after displaying old consequences (or no facts at all). Bind fresh authoritative read-only preview facts to the current full selection/Target, invalidate on changes and reject stale/mismatched required preview before decision. Also remove the unconditional separate provider screen: ordinary zero/all-Automatic flow must go directly from checklist to current preview, and No must return to the retained checklist; provider controls are optional/in-place. Add sequence regressions with non-empty authoritative previews, changed needs/provider, stale/wrong-Target/missing facts, direct No loops and retained optional provider choices, alongside existing abort/no-write tests. Actual PTY detection remains honestly caller-scoped and is not the blocking issue. Hosted run `38915947335` genuinely executed eight controller tests at integration `23ada23c330e3e035bbbf714de544d2aeb4a0504`, with required checks green but these cases missing. Current planning main `e6285b0` independently passes unchanged render/check with 0 errors/0 warnings and all 38 tests; core-920 review updates preserved. Continue only the two owned files, obtain coherent focused CI and publish validated handoff.

- 2026-10-16 review handoff: [baseharbor PR #972](https://github.com/mcpdev80/baseharbor/pull/972), branch `feature/core-916-wizard-controller`. Exact source HEAD `8870c311ad4a7b7dc923a5475b441dafd7fbf74b`, trusted develop base `701d9ac4f6e5b78658a4f429ad406f31087d44d9`, PR integration `23ada23c330e3e035bbbf714de544d2aeb4a0504`; branch 0 commits behind develop, no force-push and no merge into develop.
- Changed only `cmd/baha/app_wizard_controller.go` and `cmd/baha/app_wizard_controller_test.go`. The pure state machine composes accepted needs selection (`newAppCapabilitySelection`/`Requirements`), Target registry-based provider decisions (`appProviderChoices`/`Select`), footprint presenter and provider impact presenter. Repeated Back/No preserves original named multi-instance Requirements and Target-specific provider preferences, including off/on selection cycles. The controller returns a defensive-copy intent decision only; it does not contain or invoke execution, consent, lifecycle, file or registry mutation hooks.
- `TestAppWizardController*` tests exercise repeated No/back sequences, changed capabilities, independent provider preferences, typed initial TTY/no-input refusal, cancel/EOF/context cancellation at each phase, and unchanged on-disk manifest with unchanged input Manifest/Registry/Requirement snapshots. The component accepts an explicit TTY flag supplied by the caller; no real terminal session or lifecycle integration is claimed in this scoped, read-only unit.
- [Hosted Actions 38915947335](https://github.com/mcpdev80/baseharbor/actions/runs/38915947335) **SUCCESS**: trusted PR planner, workflow policy, `wizard-controller-tests` with real matching `TestAppWizardController*`, `cli-gofmt`, `cli-vet`, `cli-build`, `source-contracts`, and binding `PR Selected Checks`; no container/runtime/full release matrix. Early candidate found gofmt discrepancies, then corrected with exact output; final SHA is the qualified candidate.
- **Review only**: no author merge or acceptance. Independent Maintainer review required; no further task begun.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
