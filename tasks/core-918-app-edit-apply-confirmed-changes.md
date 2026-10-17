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
prs: [mcpdev80/baseharbor#978]
sources: ["mcpdev80/baseharbor#918"]
source_updated: "2026-10-17T01:55:00Z"
labels: [area/dx, area/compatibility]
blocker: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/pull/978", "https://github.com/mcpdev80/baseharbor/actions/runs/38993072829", "https://github.com/mcpdev80/baseharbor/commit/5d62816f5a90a45836f8fcc49e1add42e12350bf", "https://github.com/mcpdev80/baseharbor/commit/e0421d97246062abd45a6966fcefb4a1f6049cc4", "https://github.com/mcpdev80/baseharbor/actions/runs/38999275799"]
---

- [ ] core-918 · App edit: apply confirmed changes safely #task #release/v0-4-26 #status/review #view/review #area/wizard #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (core-918 Edit wiring)  
    **PR:** [baseharbor#978](https://github.com/mcpdev80/baseharbor/pull/978)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/978), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/38993072829), [proof 3](https://github.com/mcpdev80/baseharbor/commit/5d62816f5a90a45836f8fcc49e1add42e12350bf), [proof 4](https://github.com/mcpdev80/baseharbor/commit/e0421d97246062abd45a6966fcefb4a1f6049cc4), [proof 5](https://github.com/mcpdev80/baseharbor/actions/runs/38999275799)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-911](core-911-app-edit-load-existing-selections.md), [core-916](core-916-wizard-back-cancel-eof-no-side-effects.md)  
**Required by:** [core-921](core-921-cli-mcp-register-new-interfaces.md), [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md)  
**Owner:** mcpdev80 (core-918 Edit wiring)  
**Priority:** not set  
**PRs:** [baseharbor#978](https://github.com/mcpdev80/baseharbor/pull/978)  
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

### 2026-10-17 — Review #5555553577 resolved; candidate e0421d97 qualified for re-review

Continued the same claim on PR #978 (no new branch/PR). All four review findings are fixed in one candidate; published once as `e0421d97` (base develop `beca492d`).

- **Finding 1 (callable handler):** `runAppEdit` in `cmd/baha/app_edit.go` is now the end-to-end Edit command handler: it resolves the application, reads the exact repository/store source, assembles the production authorities via `defaultAppEditAuthorities` (real guided read, accepted choice projection, existing impact planning, read-only footprint preview, ownership-bound authorize) and drives the accepted controller over real input — EOF/No/Cancel remain write-free (core-916 contract). `appEditRuntimeExecuteAuthority` is referenced from this production assembly, no longer only from tests. Core-921 can bind central registration directly to this function.
- **Finding 2 (in-lock boundary):** fresh read→propose→plan-equality→consent revalidation and the confirmed source persist now execute inside the existing Target lifecycle lock through the authorized minimal `applicationApplyLifecycleHooks.Mutate` slot, immediately before the first deployment-state write; the lifecycle then re-reads the mutated source under the same lock and converges it. Repository writes recheck the exact original bytes immediately before the atomic replace; the store path recompares the internal copy before `Sync`. All six error-only Apply callers keep their signatures and behavior; no nested locking.
- **Finding 3 (invocation-bound receipts):** retirement requires a measured-present before fact and a measured-zero after fact — map-key presence and measured-zero/measured-zero pairs can no longer mint applied receipts (review reproduction `TestReview918AlreadyAbsentCannotBecomeApplied` covered by `TestAppApplyObservedOutcomesNeverFabricatesApplied`). add/stop/replace emit applied only for genuine measured transitions; impacts whose material/function/effect/access/location evidence the observation cannot attest stay pending/partial per the domain contract, with the exact missing producers documented in the PR body (runtime-inspector material delivery, OpenBao access verification, recovery-registry receipts inside the existing recorder pattern). No proposed `After` values are copied into receipts.
- **Finding 4 (cancellation):** post-run observation runs on an independent bounded read-only context (`context.WithoutCancel` plus timeout) so partial effects survive cancellation while the original run error is preserved (`TestObserveApplyLifecycleAfterSurvivesCancellation`).

Local qualification (Go 1.26.9, umask 0022): full `go test ./cmd/baha` green, focused Edit/Apply/receipt matrices green, `go vet`/`gofmt -l cmd internal spec contracts`/`source-readability-audit.sh` clean. Environment note: the three `TestExternalProviderRemoval*` failures seen earlier in this workspace reproduce only under a nonstandard `umask 0002` shell (registry ownership checks demand non-group-writable modes); they are pre-existing and pass under the standard CI umask — no product change required.

Hosted PR-CI on `e0421d97` (run 38999275799): `Workflow policy`, `PR · Exact Candidate`, `PR · Trusted Plan`, `cli-build/vet/gofmt/guided-tests/source-contracts`, `wizard-app-edit-tests`, and both native `docker · lifecycle` and `podman · lifecycle` gates pass. Remaining honest boundary (not suppressed, no policy exception): `PR Selected Checks` is FAILURE with `coverage-unresolved` for `cmd/baha/app_apply.go; app_apply_lifecycle.go; app_apply_result.go; app_apply_result_test.go; app_edit_apply_result.go` — the trusted planner has no resolved coverage mapping for these lifecycle-hook paths, so independent review must qualify them (scope grant is not CI qualification). Status moves active→review; Maintainer acceptance and merge remain open.

### 2026-10-17 — Independent review: functional changes required (PR #978)



- Reviewed exact source `5d62816f5a90a45836f8fcc49e1add42e12350bf`; independent [review #5555553577](https://github.com/mcpdev80/baseharbor/pull/978#pullrequestreview-5555553577). Keep the existing claim and PR, return the task to active implementation. No acceptance, merge, policy exception or additional CI run.
- The hosted results in run `38993072829` are confirmed: selected lifecycle and focused validations pass, but the final required check fails. The boundary is not merely a missing trusted coverage mapping: functional implementation gaps remain.
- The production Edit executor factory has no non-test caller; the current handler requires an already-confirmed controller and injected authorities. Supply a runnable interactive handler assembled with the real source/lifecycle connection (registration still belongs to core-921), and exercise that default connection end-to-end.
- Source persistence occurs before the existing Apply Target lock; before/after observations bracket a separately resolving, separately locked lifecycle. Move fresh identity/plan/consent validation, first source mutation and actual invocation-bound result capture into the authorized existing lifecycle boundary, preserving error-only callers and avoiding a second executor or nested lock. The read/compare/later-rename sequence is not an atomic source CAS; concurrent external edits and stale store-managed source need explicit protection.
- An additional reviewer regression demonstrates that measured-zero before and measured-zero after currently fabricate a verified applied retirement receipt: BEFORE map-key existence is not runtime presence or proof of an effect by this invocation. Genuine add/change results must also be supported where authoritative facts exist, rather than omitting all After/material/function/effect outcomes permanently.
- A second reviewer regression demonstrates canceled-context reuse for the post-execution observation. Preserve the original error and collect bounded read-only partial evidence independently of the canceled mutation context; observation failure never means success.
- Existing focused Edit/receipt suites were checked locally with Go 1.26.9; both additional reviewer regressions fail as described. Temporary reviewer tests were removed from the product worktree after recording the evidence. No product source change or push was made by this review.
- Continuation is already authorized within the bounded receipt scope, including minimal `app_apply.go` / `app_apply_lifecycle.go` hooks. Batch implementation, tests and formatting; qualify one coherent candidate, then update this handoff and rendered views. Seek independent trusted coverage qualification only after these functional findings are addressed. The prior handoff below remains historical evidence, not acceptance.

### 2026-10-17 — Execution-environment blocker; local continuation required

- The current implementation session reports repeated GitHub DNS failure and only Go 1.23.2, without an executable project checkout. The local draft is incomplete and has no qualified product PR or project/native test evidence. Mark blocked honestly; no acceptance or claim that the receipt bridge is implemented.
- Maintainer's separate environment successfully executed `git ls-remote https://github.com/mcpdev80/baseharbor.git HEAD`; that does not repair this session's environment. Computer-use access is not an established requirement: a working CLI checkout, repository Go toolchain and existing isolated CI/native execution are sufficient. Connector file reads/writes alone do not prove those prerequisites.
- A local continuation (for example Qwen with the user's local gh/checkout) should validate repository identity, current branch/dirty state, current claim, project toolchain and available targeted tests before adopting the task. Reuse/preserve existing draft files if accessible; do not claim an inaccessible download has been recovered. No ownership transfer or local recovery has been performed by this note.
- Preserve the existing claim until a continuation is explicitly adopted; no competing implementation. Existing bounded Apply/receipt scope remains authorized. Do not touch core-917's preference-owner paths. Read the current core-917 note before consuming persistent preferences; its new owner implementation is not yet accepted and must not be assumed present.
- The native receipt connection and full Edit command remain real implementation work even after tooling is restored. Cancellation observation must stay read-only under correct Target identity/locking, with actual partial evidence and original errors. No extra wrapper-only progress report or untested success claim.

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

### 2026-10-17 — Qualified local continuation on existing PR #978 (review handoff)

Adopted the existing claim `mcpdev80 (core-918 Edit wiring)` on a qualified local workspace (git checkout, GitHub access and the required Go 1.26.9 toolchain from `go.mod` verified). Reused the existing product branch `feature/core-918-app-edit-safe-apply` and PR #978; current `develop` (`beca492d`, incl. #979) was merged in, preserving #917/#975 history. No competing branch was started.

- Verified the prior PR candidate (`b292ef3b`) and reproduced its two red gates locally: `cli-gofmt` (one unformatted test file) and `wizard-app-edit-tests` (`TestAppEditApplyProviderSwitchUsesConfirmedTargetPreference` returned `application machine: unsupported`). Root cause of the test failure was a fixture bug: the confirmed switch targeted a fabricated `provider-sql-primary` id that the accepted `app_provider_choice` candidate projection never produces; corrected to the genuine candidate id (`provider-` + `capability.SQL` + `-` + name). Formatting fixed.
- Closed the confirmed interface gap with the bounded result integration: `cmd/baha/app_apply_result.go` adds `executeApplicationApplyLifecycleResults`, which drives the existing Apply lifecycle exactly once (all six error-only callers via the unchanged `executeApplicationApplyLifecycle` wrapper; `applicationApplyLifecycleRun`/`resolveApplicationFunc`/`observeApplicationProviderFactsFunc` default to the real functions), brackets the single run with read-only `observeApplicationProviderFacts`, and binds actual native observations to the approved plan. Only a genuinely retired provider runtime (measured zero containers on the correct Target, present before the run, and an impact that the observation can attest without material/function/After evidence) is reported `applied`; every other impact stays pending through `application.RecordProviderChangeResult`. Proposed `After`/material/effect values are never copied and a nil aggregate error never implies complete per-provider effects.
- `cmd/baha/app_edit_apply_result.go` adds the production Edit executor: confirmed-consent/Target validation, a single source persist (repository path uses an exact-byte compare-and-swap against the hydrated original so a concurrent or foreign edit aborts before any lifecycle run; store path uses the accepted `Store.Sync`), then one lifecycle run returning the bound outcomes; the original execution error is preserved alongside genuine partial effects.
- New focused tests in `cmd/baha/app_apply_result_test.go` exercise the concrete lifecycle connection (single execution, error preservation with partial effects, no fabrication of applied receipts, no write on target/consent/source mismatch) and the repository CAS, in addition to the accepted injected-fixture Edit suites. Existing app-edit suites stay green.

Executed locally with the required toolchain (`go 1.26.9`): `go build ./...`, `go vet ./cmd/baha`, `gofmt -l cmd internal spec contracts` (clean), `go test ./cmd/baha -run 'TestAppEdit…|TestAppApplyObservedOutcomes|TestExecuteApplicationApplyLifecycleResults|TestAppEditRuntimeExecuteAuthority|TestDefaultAppEdit'` (all pass), and `bash scripts/source-readability-audit.sh` (pass). `go test ./cmd/baha` (full package) shows only three `TestExternalProviderRemoval*` failures (`provider-registry-ownership-unverifiable`) which reproduce identically on a clean `origin/develop` checkout in this sandbox; they are pre-existing, environment-dependent and not introduced by this task.

Candidate published once as `5d62816f` (base `beca492d`, CI integration `57c03064`, run `38993072829`, demo pin `a9234790`). CI outcomes: `cli-gofmt`, `wizard-app-edit-tests`, `cli-vet`, `cli-build`, `source-contracts`, `cli-guided-tests`, `PR · Exact Candidate`, `PR · Trusted Plan`, `PR · Focused Python`, `PR · Demo Pin`, and the native `Selected Runtime · docker · lifecycle` + `podman · lifecycle` gates are all SUCCESS. The prior two failures are resolved.

Boundary for independent qualification (not a policy exception, not suppressed): `PR Selected Checks` remains FAILURE with the honest `coverage-unresolved: CLI runtime impact needs qualified targeted native coverage: cmd/baha/app_apply_result.go; app_apply_result_test.go; app_edit_apply_result.go`. The trusted planner has no resolved→coverage mapping for these three new Apply/receipt source paths, so it blocks even though the docker/podman lifecycle native gates passed. Independent review must qualify these exact paths; scope authorization is not CI qualification.

- Central `baha app edit` command/MCP registration stays with core-921 (this task does not register it). Durable provider-preference persistence stays core-917-owned (PR #975, not yet accepted) and is not assumed or duplicated here; this Edit connection uses only accepted, integrated APIs. No product merge, tag, release or self-acceptance performed.
