---
id: core-918
areas: [wizard]
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: "mcpdev80 (core-918 Edit wiring)"
depends_on: [core-911, core-916]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#918"]
source_updated: "2026-10-15T16:46:17Z"
labels: [area/dx, area/compatibility]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-918 · App edit: apply confirmed changes safely #task #release/v0-4-26 #status/active #view/active #area/wizard #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (core-918 Edit wiring)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-911](core-911-app-edit-load-existing-selections.md), [core-916](core-916-wizard-back-cancel-eof-no-side-effects.md)  
**Required by:** [core-921](core-921-cli-mcp-register-new-interfaces.md), [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md)  
**Owner:** mcpdev80 (core-918 Edit wiring)  
**Priority:** not set  
**PRs:** none  
**Source:** [baseharbor#918](https://github.com/mcpdev80/baseharbor/issues/918)
<!-- /generated:links -->

## Goal

`baha app edit` shows the exact change and executes it through the accepted lifecycle. Lane: wiring Edit.

## Scope

- In scope: new `app_edit` command/apply files and tests, plus the bounded existing-lifecycle receipt integration authorized below.
- Out of scope: CLI root registration (core-921); unrelated changes to domain/lifecycle owners; a custom transaction/recovery manager. The existing Apply lifecycle may receive only the result integration explicitly authorized below.

## Acceptance

- Loads capability and provider state; unchanged and non-edited manifest parts are preserved; No/Cancel stay write-free.
- Capability and Target preference changes run through the existing owners/consent/reconcile paths.
- Shared/foreign/data/recovery and explicit destructive confirmation rules hold; a stale plan is re-checked; actual partial results/dispositions are reported.

## Required checks

- Edit without change, two Targets, provider switch/removal, real consequences and consent mismatch via contract tests; then the necessary small Docker/Podman change scenarios.

## Dependencies and file ownership

- Depends on core-911 and core-916. Shared v0.4.26 PR/review/runner foundation (#890–#893, #895, #896) must be qualified first.

## Autonomous execution contract — 2026-10-16

- **Owned files:** `cmd/baha/app_edit.go`, `app_edit_test.go`, `app_edit_apply.go` and `app_edit_apply_test.go`. The bounded receipt extension below additionally owns `cmd/baha/app_apply_result.go`, `app_apply_result_test.go`, and minimal result-propagation hooks in existing `app_apply.go` / `app_apply_lifecycle.go`. Existing public/error-only Apply callers must remain compatible.
- **Delivered interface/result:** Consume accepted hydration and controller APIs; deliver a compiling Edit handler over existing consent/reconcile/apply authorities, with actual execution evidence.
- **Task-specific proof:** `TestAppEditApply*`/`TestAppEditCommand*`: no change, two Targets, provider transition/removal, stale consent, cancel, data/shared preservation and partial results; then the necessary existing Docker/Podman change gates.
- **Boundary:** No New files, selection/controller internals, domain mutation owners, recovery framework or central command/MCP registration. Existing lifecycle result propagation is allowed only as specified below; do not create a second executor. Required native gates must already be runnable without another CI owner. Additional source paths or unresolved trusted CI coverage require independent review, not a self-exemption.
- **Assignment gate:** use only accepted dependencies and APIs already present on develop. Confirm that the trusted plan/executor runs these exact test families on this task's file set and checks their outcomes. A plan that reports unresolved is not execution-ready. The CI-readiness inventory is maintained by [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md); later gaps become an explicit prerequisite before assignment, never an instruction to wait for another running session.
- **End-to-end owner:** the assigned session handles integration, implementation, focused tests, hosted CI observation, demonstrated fixes and its planning handoff. It reads other task states itself from planning main and preserves concurrent updates. No shared CI edits, dependency work-in-progress or manual message relay through Marcel. Normal independent review/Maintainer acceptance remains a boundary, not an implementation dependency.

## Bounded execution-receipt integration — Maintainer scope correction, 2026-10-17

The assignment incorrectly assumed that the accepted machine adapter already had a concrete runtime receipt producer. It does not: `appMachineApply` is an injected callback returning `[]application.ProviderExecutionOutcome`, whereas `executeApplicationApplyLifecycle` returns only `error`. The existing retirement receipt recorder also accepts missing outcomes and honestly leaves the result partial. A deployment success flag or the plan's proposed `After` values cannot supply the missing receipts.

- The current core-918 owner is authorized to complete this missing connection in the same task and product PR. Keep the published claim; no new task assignment or manual handoff through Marcel is needed.
- Reuse the existing Apply lifecycle exactly once. Add a result-bearing entry point and preserve the existing error-only wrapper/callers. Keep existing Target lock, authorization, consent, preflight, ownership and verify behavior; do not weaken or duplicate them. Revalidate the exact desired plan before the first source/state mutation.
- Capture only actual native execution results and authoritative observations from that invocation, bound to the requested Target, application, provider instance and approved plan. Preserve real partial effects together with the original execution error. A failure/cancellation or an observation failure must never become success; do not infer per-provider effects from a nil aggregate error or parse terminal output as receipts.
- Report unobserved functions, access, recovery and material dispositions as pending/unknown/partial through the existing domain contracts. Never copy proposed effects or material dispositions into actual outcomes, invent evidence, mark an unverified outcome applied, or claim all providers failed merely because one stage failed. Do not silently make the command a permanent pending-only stub.
- Use existing runtime inspectors/material inventories where they establish the required facts. Any missing provider-native receipt that cannot be obtained within the named hooks must be reported with the exact function and needed minimal output, rather than widening into a new runtime or recovery framework.
- Add focused tests for success, a failure after a real earlier effect, verification/observation failure, cancellation, mismatched Target/plan, no duplicate lifecycle execution and compatibility of existing Apply callers. Exercise the Edit command through this concrete connection as well as injected unit fixtures. Test source preservation and zero writes on No/Cancel/stale consent. Run only the necessary isolated Docker/Podman change cases after the coherent implementation is ready.
- The extra Apply source paths can exceed current trusted CI coverage. Publish their actual diff and tests for independent policy review if unresolved; never treat the scope grant as CI qualification or suppress the final check. No temporary workflow or full release matrix is authorized by this correction.

## Handoff

### 2026-10-17 — Confirmed integration gap and corrected task scope

- Session 2 reports a local, formatted Edit-Apply safety adapter and initial negative tests. No product PR or executed test evidence has been supplied; the complete Edit command, source persistence and concrete lifecycle connection remain unfinished.
- Maintainer source inspection confirmed the callback/result mismatch in `app_machine_adapters.go` and `app_apply.go`, and that existing retirement records do not provide the missing complete execution receipts. The original four-file scope was insufficient; the bounded result connection above is now part of this task.
- Local DNS/toolchain limits are reported environment constraints, not test passes. Use the required repository toolchain and existing supported hosted execution; do not publish incomplete candidates in a per-file CI debugging loop.
- Status remains active under the existing owner. No implementation acceptance, product merge or claim of an already implemented receipt bridge. core-921 continues to wait for the complete accepted Edit implementation.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.

### 2026-10-17 — Local safety guard, execution limitation (not review-ready)

- Claim remains with mcpdev80 (core-918 Edit wiring); no product commit, PR, acceptance or merge is asserted.
- Prepared the six-file local draft (`app_edit.go`, `app_edit_test.go`, `app_edit_apply.go`, `app_edit_apply_test.go`, `app_apply_result.go`, `app_apply_result_test.go`), including exact-source comparison, cancellation checks, same-directory source staging and a result projector. This is NOT yet a wired Edit command or native lifecycle receipt bridge.
- Isolated source persistence test `GO111MODULE=off go test -count=1 -v` passed for `TestAppEditCommandSourcePreservationAndApproval`; not a BaseHarbor package/integration or required Docker/Podman gate. Other drafted tests are unexecuted.
- Concrete execution-environment limitation: container `git ls-remote https://github.com/mcpdev80/baseharbor.git HEAD` returns `Could not resolve host: github.com`; local Go is `go1.23.2`, while project toolchain is newer. GitHub connector provides file-level API only, not an executable checkout. Product PR/CI was deliberately not attempted with unfinished code.
- Core remaining implementation: source/ownership/consent authority binding before source write, actual `app_apply.go`/`app_apply_lifecycle.go` native outcomes under Target lock, real interactive command and end-to-end tests; no invented receipts or completed review handoff.
- Obsidian and planning render/check were not executed in this environment; do not interpret this note as acceptance.
