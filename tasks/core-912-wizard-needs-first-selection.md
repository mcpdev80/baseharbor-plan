---
id: core-912
areas: [wizard]
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: "mcpdev80 (core-912 implementation)"
depends_on: [core-910, t-20261016-wizard-task-ci-readiness]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#963]
sources: ["mcpdev80/baseharbor#912"]
source_updated: "2026-10-15T16:46:52Z"
labels: [area/dx]
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/963", "https://github.com/mcpdev80/baseharbor/commit/1d6f1a7982f69622fb1faee6f4b99040c6b6d945", "https://github.com/mcpdev80/baseharbor/actions/runs/38894953755"]
---

- [x] core-912 · Wizard: present a compact needs-first selection #task #release/v0-4-26 #status/closed #view/closed #area/wizard #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (core-912 implementation) · **Priority:** not set  
    **PR:** [baseharbor#963](https://github.com/mcpdev80/baseharbor/pull/963)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/963), [proof 2](https://github.com/mcpdev80/baseharbor/commit/1d6f1a7982f69622fb1faee6f4b99040c6b6d945), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/38894953755)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-910](core-910-wizard-shared-read-only-editing-state.md), [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md)  
**Required by:** [core-913](core-913-wizard-compatible-providers-same-view.md), [core-916](core-916-wizard-back-cancel-eof-no-side-effects.md)  
**Owner:** mcpdev80 (core-912 implementation)  
**Priority:** not set  
**PRs:** [baseharbor#963](https://github.com/mcpdev80/baseharbor/pull/963)  
**Source:** [baseharbor#912](https://github.com/mcpdev80/baseharbor/issues/912)
<!-- /generated:links -->

## Goal

A compact keyboard checklist asks for developer needs instead of product names. Lane: TUI.

## Scope

- In scope: new dedicated `app_capability_selection` view/update files and tests.
- Out of scope: existing New/Init wizard entry points (changed only in the wiring task core-917).

## Acceptance

- One screen with Space/arrow keys; SQL, cache, protected secrets, app login and TLS/HTTPS as examples; further supported capabilities disclosed progressively.
- Zero selection is valid; detected suggestions are visible and deselectable; no implicit SQL/Identity/OpenBao/management bundle requirement.
- App login, operator/team access and service credentials are separated in wording and semantics; existing capability catalogs are used.

## Required checks

- Deterministic TUI update/view tests for selection, zero, preselection, keyboard and extended needs; no runtime.

## Dependencies and file ownership

- Depends on core-910.

## Autonomous execution contract — 2026-10-16

- **Owned files:** `cmd/baha/app_capability_selection.go` and `cmd/baha/app_capability_selection_test.go` only.
- **Delivered interface/result:** Expose a compiling component with explicit input/current-selection state and output capability requirements. Keep provider selection as an extension point owned by the later core-913 integration; no dependency on a future implementation.
- **Task-specific proof:** `TestAppCapabilitySelection*`: key transitions, zero selection, detected suggestions, progressive disclosure and wording separation.
- **Boundary:** No edit to New/Init entry points, hydration, presenters, controller or command registration. Capability facts come from the merged existing catalog/context.
- **Assignment gate:** use only accepted dependencies and APIs already present on develop. Confirm that the trusted plan/executor runs these exact test families on this task's file set and checks their outcomes. A plan that reports unresolved is not execution-ready. The CI-readiness inventory is maintained by [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md); later gaps become an explicit prerequisite before assignment, never an instruction to wait for another running session.
- **End-to-end owner:** the assigned session handles integration, implementation, focused tests, hosted CI observation, demonstrated fixes and its planning handoff. It reads other task states itself from planning main and preserves concurrent updates. No shared CI edits, dependency work-in-progress or manual message relay through Marcel. Normal independent review/Maintainer acceptance remains a boundary, not an implementation dependency.

## Handoff

- 2026-10-16 independent Maintainer re-review and acceptance: **accepted and merged** via [PR #963](https://github.com/mcpdev80/baseharbor/pull/963), squash commit `1d6f1a7982f69622fb1faee6f4b99040c6b6d945` on product `develop`. Reviewed source `3f2e65e0cdf05e46a940c3e758a98aa459c47008` fixes both findings from review #5547162958: named/multiple same-kind requirements retain exact identity and ordering through off/on cycles and detected/current overlap, and Enter/Space share bounded disclosure transitions. Hosted [run 38894953755](https://github.com/mcpdev80/baseharbor/actions/runs/38894953755) checks integration `537d0f0e169d0c7e8fe2f7e94afeb7b85baed246` over trusted base `30d635b827e86d233030746abc65ce9475516ce0`. Logs independently confirm all 13 selection tests executed; format, CLI vet/build, source/contracts, focused Python, workflow policy and PR Selected Checks are SUCCESS. No runtime matrix. #964 was a normal develop-to-task-branch integration, not an earlier acceptance. Only the two owned files changed. Planning main was independently checked, concurrent core-919 work preserved, generated views rendered and validated with 0 errors/0 warnings and all 38 unit tests passing before publication. This accepts the selection component and unblocks core-913; provider choices, controller/wiring and release acceptance remain separately scoped.

- 2026-10-16 review correction handoff for [PR #963](https://github.com/mcpdev80/baseharbor/pull/963), responding to independent review #5547162958. Exact source HEAD `3f2e65e0cdf05e46a940c3e758a98aa459c47008`; trusted develop base `30d635b827e86d233030746abc65ce9475516ce0`; exact PR integration `537d0f0e169d0c7e8fe2f7e94afeb7b85baed246`. Normal develop integration via [PR #964](https://github.com/mcpdev80/baseharbor/pull/964), branch zero commits behind develop; no force push, no author merge to develop.
- Corrected only `cmd/baha/app_capability_selection.go` and `cmd/baha/app_capability_selection_test.go`. Existing named `capability.Requirement` identities, ordering and multiple same-kind instances survive unchanged and off/on cycles. Detected/current overlap retains exact original names; `default` is emitted only for genuinely newly selected kinds. Enter/Space share one disclosure toggle and cursor clamp; regressions cover Enter collapse, alternating keys, valid focus and non-confirmation of footer transitions.
- [Actions run 38894953755](https://github.com/mcpdev80/baseharbor/actions/runs/38894953755) **SUCCESS** at the exact integration: `PR · Trusted Plan`, `Workflow policy`, `PR · Focused Python`, `PR · Validation · wizard-capability-selection-tests` (real `TestAppCapabilitySelection*` execution), `cli-gofmt`, `cli-vet`, `cli-build`, `source-contracts`, and authenticated `PR Selected Checks`. No runtime matrix. Superseded earlier runs documented in PR; first post-review candidate blocked on stale integration, subsequent focused test/format findings corrected before green candidate.
- Review handoff only. Independent Maintainer re-review required; task remains `review`, unaccepted, PR unmerged into develop.


- 2026-10-16 independent Maintainer review of PR #963 at `7ebde0095ad5a7bd1d32b061a77d78a86acdf508`: **changes required, not accepted or merged**. The successful hosted product run `38893037343` is confirmed, but inspection found two missing regressions: current named requirements are reduced to kind flags and emitted as `default` (including loss of multiple same-kind resource identities), and Enter on the expanded disclosure footer collapses the list without clamping its cursor, allowing an invisible focus and accidental next-Enter confirmation. Preserve existing named requirements for selected kinds, synthesize default only for new kinds, and test exact identity preservation plus Enter/Space disclosure transitions. Scope remains the task's two owned files; regular targeted CI must qualify the corrected candidate. Current planning baseline `dc1e881` preserves core-914's concurrent handoff; render produced no changes, check reports 0 errors/0 warnings and all 38 planning tests pass. The previously outstanding planning-validation concern is resolved; product acceptance remains outstanding.

- 2026-10-16 implementation delivered for independent review: [baseharbor PR #963](https://github.com/mcpdev80/baseharbor/pull/963), branch `feature/core-912-needs-first-selection`. Exact source HEAD `7ebde0095ad5a7bd1d32b061a77d78a86acdf508`, trusted develop base `c889ba7f5350e978d6c372cd58f50651d4852e72`, PR integration `f2755262f4c08a9519d4eee413f2b8537f0dfbfd`. Branch is current with develop (0 behind as verified before handoff); no force push.
- Own files only: `cmd/baha/app_capability_selection.go` and `cmd/baha/app_capability_selection_test.go`. Delivered portable catalog-based checklist with arrow/Space/Enter navigation; SQL/cache/secrets/app-login/TLS first, supported extra needs progressive; detected suggestions optional and deselectable, zero selection permitted, no implicit bundles, explicit distinction of app-user login, operator/team access and service credentials. No new/init wiring or shared command changes.
- [Hosted Actions run 38893037343](https://github.com/mcpdev80/baseharbor/actions/runs/38893037343) **SUCCESS**: Trusted Plan, Workflow policy, Focused Python, `wizard-capability-selection-tests` (actual executed `TestAppCapabilitySelection*`), `cli-gofmt`, `cli-vet`, `cli-build`, `source-contracts`, and authenticated **PR Selected Checks**. No runtime gate. Earlier candidate errors were diagnosed, fixed and superseded.
- Status **review**, not accepted; independent Maintainer approval and merge into develop remain outstanding. No further task or self-acceptance.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
