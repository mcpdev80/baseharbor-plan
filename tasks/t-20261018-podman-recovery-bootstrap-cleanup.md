---
id: t-20261018-podman-recovery-bootstrap-cleanup
type: bug
areas: [runtime]
release: v0.4.26
version: ""
parent: v0.4.26
owner: Flash (codeman w1-baseharbor)
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#995]
sources: []
blocker: "Current #995 requires bounded diagnostic-identity correction (review 5566018799), independent re-review and authorized full native recovery/cleanup proof; product owner Codeman Flash remains paused."
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/commit/560ae9be9c6093a48d1b4b9375286cf4e33fed28"]
---

- [ ] t-20261018-podman-recovery-bootstrap-cleanup · Podman recovery acceptance: reuse initialized OpenBao and clean owned resources on failure #task #release/v0-4-26 #status/blocked #view/blocked #area/runtime #kind/bug
    <!-- generated:card -->
    **Owner:** Flash (codeman w1-baseharbor) · **Priority:** high  
    **PR:** [baseharbor#995](https://github.com/mcpdev80/baseharbor/pull/995)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/commit/560ae9be9c6093a48d1b4b9375286cf4e33fed28)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** none  
**Required by:** [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md), [t-20261018-podman-recovery-core-state-owner](t-20261018-podman-recovery-core-state-owner.md)  
**Owner:** Flash (codeman w1-baseharbor)  
**Priority:** high  
**PRs:** [baseharbor#995](https://github.com/mcpdev80/baseharbor/pull/995)  
**Source:** 
<!-- /generated:links -->

## Goal

Make the real native backup/restore acceptance reach and verify its full recovery chain using the existing selected-Target Core/OpenBao initialization authority. Ensure failure paths release only this test's owned resources.

## Scope

- Fix the existing TestAppBackupRestoreCLIRealDisasterRecovery fixture and direct regression tests, continuing existing PR #995.
- Preserve product OpenBao fail-closed behavior and existing initialization/recovery credential owners. Do not rebootstrap initialized Core, accept arbitrary credentials, or treat an initialized response alone as usable authorization.
- Register owned-resource cleanup before side-effectful startup. Cleanup must run on bootstrap failure, startup partial failure and later assertions with a fresh bounded context; preserve useful original failure evidence.
- No global cleanup, ci-runtime-reset.sh, shared-state deletion, production selection redesign or weakened native assertions.

## Acceptance

- Native runtimeUpGuided is not followed by a second unconditional OpenBao Bootstrap against its already initialized selected Core.
- Existing legitimate initialization/credential authority supplies what the test actually needs; protected recovery material remains valid and secret.
- Executable focused tests cover already initialized Core, initialization failure, partial startup and idempotent cleanup, retaining unrelated sentinel resources.
- The real test reaches Backup -> Destroy -> Restore, proving restored SQL data, managed secrets, consumer access and regenerated identity tokens/certificates instead of copied credentials. Preserve authentic per-operation consent and ownership requirements.
- Independent exact-SHA review and Qwen's real native Podman retest succeed before acceptance. No passing fixture unit test or generic CI substitutes for full native recovery evidence.

## Required checks

Focused actual fixture-path regressions, Go build/vet/gofmt, smallest relevant hosted CI and Planning sync/render/check/tests. Native/SSH execution is Qwen-only. No mandatory-CI bypass or self-qualification.

## Dependencies and file ownership

- Bounded ownership: cmd/baha/app_backup_restore_integration_test.go and directly related backup acceptance fixture tests on existing PR #995.
- Follow-up to [Core-state owner task](t-20261018-podman-recovery-core-state-owner.md) and [guided runtime task](t-20261017-podman-backup-guided-runtime.md). Their unmerged partial fixes are implementation inputs on the existing branch, not accepted prerequisites.
- Required before v0.4.26 release preparation. Claim before implementation. Do not edit active shared CI-policy files.

## Reproducer

Exact source: `560ae9be9c6093a48d1b4b9375286cf4e33fed28`.

```sh
BASEHARBOR_APP_BACKUP_ACCEPTANCE=true BASEHARBOR_TEST_RUNTIME=podman go test ./cmd/baha -run '^TestAppBackupRestoreCLIRealDisasterRecovery$' -count=1 -v
```

## Handoff

### 2026-10-19 — PAUSED: BaseHarbor CI stabilization (coordinator hold)

- Controlled development pause ordered by Marcel; infrastructure prerequisite (GC evidence preservation) fixed via merged #999/#1000, but trusted gates still block: `integration_sha_mismatch` (#995/#985 lane) and `coverage-unresolved` needing exact reviewed-bundle qualification (#998/#993/#990/#989). No CI reruns, no correction loops, no merges during the pause.
- New candidate pushed before halt: `d359af833649a16f6b2b121704d5c2a6613f8e36` on the #995 branch (capability-aligned fixture manifest + non-native parser regression + bounded redacted cleanup diagnostics; implementation evidence evidence/board-2026-10-19/o2-995-fix.md). Independent re-review (worker o4) stopped PARTIAL: targeted checks done, one long go-test batch and two source checks open (evidence/board-2026-10-19/o4-995-rereview.md).
- PR gate status: `integration_sha_mismatch` — invalid/unaccepted PR integration; no reruns during pause. Native Qwen retest must not start before a complete independent exact-SHA review.

### 2026-10-19 — Resumed under Codeman lane; implementation boundaries

- Prior owner ChatGPT (PR #995 bootstrap-cleanup correction) dormant since the ended pause; claim transferred to Flash (codeman w1-baseharbor) per the 2026-10-19 board mandate; prior records preserved.
- Verified: #995 open at `eaf86813f789f62b393ecf9ad287ae04b3ff7561`, MERGEABLE; no formal approving reviews recorded (maintainer comment reviews only); latest CI run 39128733229 fails only at the fail-closed enforcement step.
- Implementation scope per resume instructions: replace obsolete postgres/redis fixture manifest keys through the real capability parser without parser exceptions; add real fixture-path regression coverage; emit bounded redacted structured cleanup diagnostics through existing ownership/consent authority without weakening guards. Native Podman retest follows an independently reviewed new exact-SHA candidate.

### 2026-10-18 — Latest Qwen native FAIL; paused, no recovery qualification

- Exact source `eaf86813f789f62b393ecf9ad287ae04b3ff7561`, rootless Podman 5.7.0 / Go 1.26.9. User-supplied Qwen run reports FAIL after 166.76s. Manager has not run this native test or read the private local full report.
- Test reaches app apply (app_backup_restore_integration_test.go:81), then fails with `unsupported service "postgres"`. Legacy postgres/redis manifest keys conflict with the same source's capability-key parser; replace through the actual supported manifest contract, not a parser exception. Qwen reports same mismatch on prior develop; that cross-runtime conclusion is source-based, not an executed Docker run.
- Registered cleanup runs and reports an error, but existing approvedNativeFixtureCleanup -> destroyInstallation refuses unverified Target/deployment ownership before deleting own resources. Qwen observed own containers, volume, networks and Quadlet units left behind. Structured cleanup details were discarded by io.Discard. The exact authority guard/caller is not yet identified; do not weaken it or classify a product destroy bug without isolating the cause.
- Qwen removed only owned resources by identity; unrelated resources preserved, no global/helper reset or code mutation. A source checkout remains on the authorized system. Its private location and access identifiers are intentionally not published. Qwen must checkpoint any useful sanitized logs and remove only that owned checkout if no longer needed; no SSH cleanup by other sessions.
- Backup/Destroy/Restore, restored SQL/secret/consumer checks, identity token/certificate regeneration and successful automatic cleanup remain unverified. Earlier positive source review 5563121341 addresses the bounded prior regression correction only; it is not native acceptance.
- Resume existing PR #995 only after explicit Maintainer assignment. First parse the exact fixture manifest without a runtime, then diagnose cleanup with bounded redacted structured evidence through existing authority. Preserve real recovery assertions, per-operation consent and foreign-resource guards. Add real fixture-path regressions, then independent exact-SHA review, then Qwen native retest. No new GitHub issue or duplicate recovery task.
- Both implementation and testing paused for Horde/Codex handover. Existing claim retained; no automatic takeover. Planning generator/check/tests remain required for this canonical update.


### 2026-10-18 — Qwen native retest: failed before backup, reproduced twice

- User-supplied native evidence reports rootless Podman 5.7.0, clean isolated baseline, exact SHA above, same failure on 2/2 independent clean starts. This entry records Qwen's supplied results; manager did not execute a native test or access the local full report.
- Failure at app_backup_restore_integration_test.go:49: unconditional openbao.Bootstrap after successful runtimeUpGuided returns "OpenBao is already initialized" (internal/openbao/bootstrap.go:129-130). Manager source inspection independently confirms this call sequence at the exact SHA. Qwen's read-only post-up probe confirms initialized Core.
- Classification: acceptance-fixture initialization/ownership defect; no product recovery failure demonstrated. The selected-target lookup correction now reaches the real Core; it does not complete recovery qualification.
- Qwen reports own Core/Identity resources leaked after Fatalf: Core containers, SQL volume and four networks. Existing deferred approvedNativeCoreStop is registered only after successful startup and its error is discarded; exact cleanup cause/coverage requires implementation diagnosis.
- Qwen removed only owned test resources and restored baseline. No global/helper reset, code edit or merge.
- Backup, Destroy, Restore, SQL/secret/consumer checks and identity regeneration were never reached and remain unverified.
- Full local SOP report exists with Qwen; no private host identifiers, SSH aliases, paths, addresses or secrets copied here.
- Canonical intake recorded by Maintainer; executable generator/check/tests and refreshed release/views must be performed by assigned implementation owner on current Planning main before claiming a validated handoff.

### 2026-10-18 — Implementation claim published before code changes

- Existing PR #995, exact baseline `560ae9be9c6093a48d1b4b9375286cf4e33fed28`. Owned files: `cmd/baha/app_backup_restore_integration_test.go`, bounded related fixture regressions only. Reuse production-selected Core/OpenBao credentials; no second bootstrap or permissive initialized fallback.
- Register cleanup before runtimeUpGuided; bounded fresh context and partial-start cleanup, no global reset or unrelated resource deletion. Preserve all backup, restore, SQL, secrets, consumer and regenerated identity checks. Only isolated tests; native Podman retest remains Qwen-owned. No own qualification or merge.

### 2026-10-18 — #995 bounded candidate; independent review pending

- Existing PR #995 corrected from `560ae9be9c6093a48d1b4b9375286cf4e33fed28` to exact candidate `c77307c9bcd7cbcfd33fafb9e75283d4fe688cc2`. No Core/OpenBao product or CI policy code changed. RuntimeUpGuided remains initialization/credential authority; native acceptance checks live manager readiness through existing `inspectManagedOpenBao` rather than calling second `openbao.Bootstrap`.
- Existing consent-checked `approvedNativeFixtureCleanup` is registered via `t.Cleanup` **before** startup. Cleanup gets fresh 3-minute background context even after cancelled startup, retains owned Target boundaries and does not touch unrelated resources; cleanup errors are reported rather than ignored.
- Added direct production-path helper regressions for success, failed partial startup, authenticated-readiness failure, pre-start cleanup registration, bounded fresh cancelled-parent cleanup, and foreign sentinel preservation. All preexisting native full Backup → Destroy → Restore, SQL, secrets, identity regeneration and consent assertions preserved verbatim.
- Isolated Go job [6ad4b086c662881452273729](https://huggingface.co/jobs/ThunderHawk1080/6ad4b086c662881452273729) and CI [39124266211](https://github.com/mcpdev80/baseharbor/actions/runs/39124266211) must be evaluated on exact SHA. No live test or self-qualification. Qwen Native Podman retest remains mandatory after independent review.

### 2026-10-18 — Correction review: one remaining error-propagation regression gap

- Independent review [5563009072](https://github.com/mcpdev80/baseharbor/pull/995#pullrequestreview-5563009072) of exact `1f273cc2e4385882923c6fc3a698d584caac8ca5`: source direction positive (second Bootstrap removed, actual manager readiness checked, bounded approved cleanup registered before startup), no native success claimed.
- Changes required: failure-cause assertion compares against two optional errors with AND. In either failure scenario, unexpected nil passes because the other expected error is nil. Require one explicit expected error per scenario and reject swallowed failures; retain order/context/owned/foreign checks. This is a source-inspected regression flaw, not a new native runtime result.
- Correct on existing #995, publish one focused validated candidate. Independent source acceptance must precede Qwen's full native retest. Formal coverage and release acceptance remain open.

### 2026-10-18 — Review 5563009072 corrected; independent re-review pending

- Exact source before correction `1f273cc2e4385882923c6fc3a698d584caac8ca5`; review [5563009072](https://github.com/mcpdev80/baseharbor/pull/995#pullrequestreview-5563009072) flagged false positive from `errors.Is(nil,nil)`.
- New exact #995 candidate `eaf86813f789f62b393ecf9ad287ae04b3ff7561`: choose one expected error per success/start/readiness scenario; success requires `nil`, failure explicitly requires `err != nil` and `errors.Is(err, expected)`. Test of later abort after readiness confirms registered cleanup, owner cleanup order, bounded uncancelled context and unrelated sentinel unchanged. Existing initialization, authenticated-manager gate, consent and complete native recovery assertions unmodified.
- Isolated first correction [HF 6ad4bf3b5ccb47ba0f7c3edd](https://huggingface.co/jobs/ThunderHawk1080/6ad4bf3b5ccb47ba0f7c3edd) ran focused Go tests, vet and build successfully; formatting was subsequently applied. Final SHA requires exact validation and GitHub CI evidence. No native/SSH tests, own coverage approval or merge. Qwen full recovery retest only after independent Manager re-review.

- Final exact SHA `eaf86813f789f62b393ecf9ad287ae04b3ff7561`: [HF 6ad4bfe75ccb47ba0f7c3f1b](https://huggingface.co/jobs/ThunderHawk1080/6ad4bfe75ccb47ba0f7c3f1b) ran focused Go test fixtures including later-abort cleanup, and native recovery opt-in remained skipped. Go vet/build and gofmt/diff checks included. [GitHub CI 39128733229](https://github.com/mcpdev80/baseharbor/actions/runs/39128733229) Trusted Plan, workflow policy and focused Python pass; PR Selected Checks block due unqualified acceptance-test coverage. [Planning HF 6ad4bff6c662881452273cdf](https://huggingface.co/jobs/ThunderHawk1080/6ad4bff6c662881452273cdf): 299 tasks, 0 errors/warnings, 47 tests pass; render has six unrelated concurrent #991/#921/release view changes not owned here. No own merge; manager re-review, then Qwen Podman retest.

### 2026-10-18 — Regression correction source accepted; native retest next

- Independently reviewed exact #995 `eaf86813f789f62b393ecf9ad287ae04b3ff7561`: one expected error per scenario; explicit nil success/non-nil original failure; actual Goexit-after-readiness test with parent cleanup/order/context/sentinel assertions. No new source blocker in this bounded correction. Helper, manager-authentication and full recovery/consent assertions unchanged.
- Actual GitHub 39128733229 has trusted plan/workflow/Focused Python SUCCESS, Go validation not selected, finalcheck unresolved. Author HF 6ad4bfe75ccb47ba0f7c3f1b reports focused Go/vet/build/gofmt success; manager did not rerun. Never treat generic CI as native recovery evidence.
- Qwen is assigned the authorized isolated native Podman full disaster-recovery test at the exact SHA above, including SQL/secrets/consumer and regenerated token/certificate proof plus owned cleanup. No global/helper reset or code changes. Report precise next failure without suppressing it.
- Task acceptance, formal source coverage and merge remain pending native evidence. This Handoff-only append changes no canonical task status; no new manager executable Planning validation claimed.

### 2026-10-19 — CI stabilization handoff; product claim preserved

- Current remote #995 HEAD 2ff6846c3b4d246d1291ae2c90d09d231c4214bc is a genuine develop integration of worker source d359af833649a16f6b2b121704d5c2a6613f8e36. All four candidate source blobs are unchanged. Actual run 39183081916 accepts integration; build/vet/guided/source validations pass. The previous integration_sha_mismatch is resolved, not hidden by a verifier exception.
- This does not upgrade the prior PARTIAL source review or establish native recovery. The obsolete manifest keys were corrected in worker source, but actual successful Backup→Destroy→Restore with SQL/secrets/consumer access and identity regeneration, plus owned cleanup on failure, is still absent. The last supplied native failure belongs to eaf86813 and is not proof of failure or success of the new candidate.
- Owner remains paused Codeman Flash; no product claim takeover or file change by stabilization coordinator. Before resumption: independent complete four-file re-review (including newly added non-_test cleanup diagnostic source), then Qwen/authorized native lane executes the exact reviewed candidate and proves recovery plus scoped cleanup. No native credentials/executor are available to this coordinator; no unauthorized test or fabricated coverage is provided. Existing ownership/consent guards stay mandatory.

### 2026-10-19 — Complete independent current-source review

- Full four-file exact-source review of 2ff6846c3b4d246d1291ae2c90d09d231c4214bc is now complete, not deferred: CHANGES REQUIRED, review https://github.com/mcpdev80/baseharbor/pull/995#pullrequestreview-5566018799.
- Confirmed P2: ownershipSubject returns applicationDestructionPlan.Scope.Owner.Subject, which the actual destruction owner fills with DeploymentID; approvedNativeFixtureCleanup logs it. This violates the new coarse-only/no-ID diagnostic contract. Emit fixed categories by actual plan type, never raw Subject/Owner, and add sentinel identity/project/target/path regressions with real machine.Error and plan types. No actual private identifiers are published.
- Manifest/parser, authenticated readiness, early cleanup registration, fresh bounded context, recovery assertions and consent/ownership guards are retained. No further confirmed source blocker. Diagnostic wrapper does not prove successful cleanup; full authorized native recovery and fail-path ownership evidence remain absent.
- Flash/Codeman retains product claim while paused; Qwen/authorized native lane owns retest only after corrected independent source review. Infrastructure coordinator neither overwrites paused source nor grants source/native coverage.
