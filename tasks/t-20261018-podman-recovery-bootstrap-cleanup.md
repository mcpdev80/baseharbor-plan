---
id: t-20261018-podman-recovery-bootstrap-cleanup
type: bug
areas: [runtime]
release: v0.4.26
version: ""
parent: v0.4.26
owner: "Codex (Maintainer-authorized bounded #995 correction; prior Flash claim preserved)"
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#995]
sources: []
blocker: "Full native recovery remains unproved: 39593974584 at 71b66ae fails broker readiness using stale edge runtime image. Exact-source runtime-image correction, real Backup/Destroy/Restore and owned-cleanup proof, current source qualification and required CI remain pending."
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/commit/560ae9be9c6093a48d1b4b9375286cf4e33fed28","https://github.com/mcpdev80/baseharbor/commit/36310f08467f6e963f080b22936ffbaf5d763b74","https://github.com/mcpdev80/baseharbor/actions/runs/39219870611","https://github.com/mcpdev80/baseharbor/pull/995#pullrequestreview-5568575016","https://github.com/mcpdev80/baseharbor/pull/995#issuecomment-6262605610","https://github.com/mcpdev80/baseharbor/commit/4ca9881766fc88e850ccdbbc2d837cabb19ebab5","https://github.com/mcpdev80/baseharbor/actions/runs/39227471936","https://github.com/mcpdev80/baseharbor/pull/995#pullrequestreview-5569225959","https://github.com/mcpdev80/baseharbor/pull/995#issuecomment-6263758673"]
---

- [ ] t-20261018-podman-recovery-bootstrap-cleanup · Podman recovery acceptance: reuse initialized OpenBao and clean owned resources on failure #task #release/v0-4-26 #status/blocked #view/blocked #area/runtime #kind/bug
    <!-- generated:card -->
    **Owner:** Codex (Maintainer-authorized bounded \#995 correction; prior Flash claim preserved) · **Priority:** high  
    **PR:** [baseharbor#995](https://github.com/mcpdev80/baseharbor/pull/995)  
    **Blocker:** Full native recovery remains unproved: 39593974584 at 71b66ae fails broker readiness using stale edge runtime image. Exact-source runtime-image correction, real Backup/Destroy/Restore and owned-cleanup proof, current source qualification a…  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/commit/560ae9be9c6093a48d1b4b9375286cf4e33fed28), [proof 2](https://github.com/mcpdev80/baseharbor/commit/36310f08467f6e963f080b22936ffbaf5d763b74), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/39219870611), [proof 4](https://github.com/mcpdev80/baseharbor/pull/995#pullrequestreview-5568575016), [proof 5](https://github.com/mcpdev80/baseharbor/pull/995#issuecomment-6262605610), [proof 6](https://github.com/mcpdev80/baseharbor/commit/4ca9881766fc88e850ccdbbc2d837cabb19ebab5), [proof 7](https://github.com/mcpdev80/baseharbor/actions/runs/39227471936), [proof 8](https://github.com/mcpdev80/baseharbor/pull/995#pullrequestreview-5569225959), [proof 9](https://github.com/mcpdev80/baseharbor/pull/995#issuecomment-6263758673)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** none  
**Required by:** [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md), [t-20261018-podman-recovery-core-state-owner](t-20261018-podman-recovery-core-state-owner.md)  
**Owner:** Codex (Maintainer-authorized bounded #995 correction; prior Flash claim preserved)  
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

### 2026-10-21 — Actual native failure retained; obsolete source blocker replaced

- Current validation source `71b66ae019b4a1dc3af3b158bbb17b085fca25d8` contains fail-closed cleanup correction, five error-path negatives, real independently owned foreign-volume sentinel and narrow nonduplicated Podman workflow route with Go 1.26.9. Existing #995 published head remains `335477ea96c5992c0ec5e64fc4ce16295cf853e7` until this coherent correction is qualified.
- Actual [39593974584](https://github.com/mcpdev80/baseharbor/actions/runs/39593974584) failed broker readiness before the recovery chain. Rootless setup, exact source/toolchain recording and artifact upload passed; artifact `12344271179` contains real failure receipts. Broker used default edge revision `11a1e76a9a68cf3da7476f2ea811907faef8a233`, not candidate CLI source. Same-source static binary/runtime image verification is now being added before another native attempt.
- Foreign sentinel identity survived cleanup and was separately removed through its own owner. This does not prove whole owned cleanup or Backup/Restore success. Full native recovery, current exact-source qualification, mandatory CI and Owner-authorized acceptance remain open. Earlier Qwen-only restrictions are superseded by the explicit complete-recovery Owner authorization; ownership/resource protections remain binding.


### 2026-10-19 — Actual full-path correction published; native assignment updated

- Exact #995 candidate: be972ff39006037a9f06b904c156fe73f7f24ba8. Operations now obtain one current typed acknowledgement from their actual fail-closed authority; restore has separate destructive scope consent. Stale/unknown errors do not cause approval loops. SQL seeding/readback uses the protected current consumer binding with verified TLS, no guessed runtime project/provider role.
- Actual [CI39223771804](https://github.com/mcpdev80/baseharbor/actions/runs/39223771804) Guided/build/vet/source checks pass. The Guided wrapper selects all8 existing fixture/manifest regressions plus new consent/SQL tests; nonverbose logs are not individually enumerated receipts. Full five-file source review [5568897605](https://github.com/mcpdev80/baseharbor/pull/995#pullrequestreview-5568897605) is positive; final remains unresolved on5paths, with valid integration.
- Latest [Qwen exact-SHA native assignment](https://github.com/mcpdev80/baseharbor/pull/995#issuecomment-6263247019) supersedes36310f for final acceptance. The real opt-in native Backup/Destroy/Restore, actual consumer data/secrets, non-replayed identities and owned automatic cleanup have not been executed here. gofmt of these changed fixture files remains an explicit native precheck; no unsupported success claim.
- Keep #990 and the recovery chain unaccepted until that actual result, fresh qualification and green mandatory CI exist. No reset/SSH/native execution by this coordinator.

### 2026-10-19 — Full-scope audit finds additional fixture blockers; correction authorized

- Marcel explicitly ordered inspection and repair of all v0.4.26 errors. This supersedes the earlier diagnostics-only implementation limit for these demonstrated #995 fixture defects; existing Codex claim/branch and prior Flash history remain intact.
- Independent full-path audit confirms native restore has no fresh destructive scope consent, while apply/retirement also lack operations-bound acknowledgements when required. SQL seed/readback assume an unqualified application project and bootstrap role despite default shared placement. Correct these in this existing PR through actual typed consent and protected service-binding owners; do not weaken product guards or fabricate native PASS.
- Preserve all SQL/secret/identity-regeneration and cleanup assertions. Add executable non-native regressions selected by actual Guided CI. New exact candidate requires independent review and Qwen native retest; prior positive bounded review is not approval for new source.

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

### 2026-10-19 — Final stabilized integration handoff

- Current #995 HEAD02b4cd5f48e449085bc58df625ef6af8fa7bbd73, trusted develop7827e6491a7715e0ffffb1e7938764f6788cc30b. Four worker source blobs unchanged; no product correction or claim transfer by CI coordinator.
- Actual CI39185883757: Trusted Plan, policy, Focused Python, Guided, build, vet and Source Contracts SUCCESS; final117848399067 blocks only qualified native coverage of the four source files, not integration_sha_mismatch. Current trusted plan artifact retained30days. Final PR handoff5566105009.
- Source CHANGES REQUIRED review5566018799 remains applicable: bound diagnostic output to fixed owner categories, exclude raw identities and prove sentinels. Paused Flash/Codeman owns correction after explicit continuation; then independent re-review and authorized Qwen full recovery/owned-cleanup proof. #990 narrow fix remains dependent and unaccepted; existing claims preserved. No source policy waiver, native run or merge of #995/#990. Infrastructure acceptance never resumes Codeman automatically.

### 2026-10-19 — Requested continuation; bounded correction proposal ready

- Marcel requested further progress. Codeman and all existing claims remain paused/protected; this continuation does not silently transfer product ownership or o1's binding work.
- Prepared reviewable **unapplied**, unreferenced proposal commit https://github.com/mcpdev80/baseharbor/commit/36310f08467f6e963f080b22936ffbaf5d763b74, parent exact #995 HEAD02b4cd5f. Only diagnostic source and existing diagnostic-test owner changed in the proposal; no product branch/ref, worktree or claim updated. No competing PR.
- Separate independent static review positive: fixed owner-category/type mapping and fixed failure classifications; no private identity/plan/material/error fields read. Two actual-helper TestGuidedBackupCleanupDiagnostic* tests use real typed errors/real plan types plus private sentinels and wrapped/nil/unknown cases. Existing safety/ownership/consent/cleanup decisions unchanged. This is not executable proof or native acceptance.
- Local executor unavailable; HF Jobs ps endpoint again returns UNAVAILABLE (tool not returned by tools/list). No invented test/format success or additional failed-job rerun. Once explicitly authorized on the existing owned branch, run the two exact unit tests, gofmt/vet/build and current Guided CI before new source qualification; authorized native recovery remains necessary afterward.
- Corrected stale PR descriptions: #995 now distinguishes its actual production diagnostic source and current review failure from older fixture-only claims; #998 identifies the actual published756b22dc and protected unpublished binding. Source heads remain02b4cd5f/756b22dc.
- Required next authorization is narrowly applying the concrete #995 proposal despite the existing product-claim hold. It does not resume Codeman or release/change core-921/o1. Original CI stabilization acceptance and published closures remain valid.

### 2026-10-19 — Explicit bounded continuation authorized and claimed

- Marcel explicitly approved applying and finishing the prepared #995 correction while Codeman and o1 remain paused. Codex claims only this bounded continuation on existing #995, preserving prior Flash/source history; no general worker restart or core-921 ownership change.
- Owned change: cmd/baha/native_fixture_cleanup_diagnostics.go and existing cmd/baha/native_fixture_cleanup_diagnostics_test.go. Prepared candidate36310f08467f6e963f080b22936ffbaf5d763b74 has separate positive static review; no executed test is claimed yet. Existing branch HEAD02b4cd5f, develop7827e649 verified unchanged immediately before application.
- Apply via normal expected-SHA fast-forward, then inspect actual focused Guided/build/vet/source CI before any further candidate. Preserve ownership/consent/destroy behavior. Full recovery, private-data retention and owned cleanup remain real native acceptance requirements; do not turn source-unit success into native success.

### 2026-10-19 — Authorized correction implemented; actual CI and full source review positive

- Marcel explicitly authorized the bounded #995 continuation, recorded before ref update in Planninga631f764. Existing branch advanced normally02b4cd5f→36310f08467f6e963f080b22936ffbaf5d763b74; no force push, new product PR, worker restart or o1/core-921 claim change.
- Fixed P2 diagnostic identity disclosure using fixed owner categories by actual plan type and fixed error classes; never read/output raw Subject/Owner/Reference/Revision/PlanID/message values. Nil/typed-nil/wrapped/unknown errors covered. Added two actual-helper TestGuidedBackupCleanupDiagnostic* tests to existing diagnostic-test owner with real machine.Error/application/runtime plan types and private sentinel fields. Ownership, consent, destruction and cleanup decisions unchanged.
- Actual GitHub CI39219870611: Guided117952464806 runs `go test ./cmd/baha -run '^TestGuided' -count=1` and PASS; both new exact-prefix tests contain no skip. Build, Vet, Source Contracts and Focused Python PASS. No local/HF execution or executed-format check claimed; HF Jobs endpoint still UNAVAILABLE, local executor disconnected.
- Full independent read-only five-file source review POSITIVE, published https://github.com/mcpdev80/baseharbor/pull/995#pullrequestreview-5568575016. This supersedes previous P2 changes-required finding for the bounded source correction, not native acceptance. Current integrationaa53ee44486c58c7e28ccfaff317bce669574f18 is accepted; final117952916212 blocks only unresolved qualification of the five source paths, no integration mismatch.
- Authorized native Qwen/lane handoff published https://github.com/mcpdev80/baseharbor/pull/995#issuecomment-6262605610. Exact candidate36310f; first focused diagnostic unit tests plus gofmt precheck, then actual `BASEHARBOR_APP_BACKUP_ACCEPTANCE=true BASEHARBOR_TEST_RUNTIME=podman go test ./cmd/baha -run '^TestAppBackupRestoreCLIRealDisasterRecovery$' -count=1 -v`, umask0022, exclusive verified isolation. Preserve full SQL recovery_probe/secret/consumer/backup-recovery metadata/fresh-token-certificate assertions. Prove successful automatic owned cleanup separately from any manual fallback; never touch unrelated resources or use global/helper reset.
- Native Recovery/Cleanup is NOT executed or qualified here. No authorized native executor is connected to this session; Qwen retains native test responsibility. Publish sanitized exact-SHA outcomes without private host/access/path/secret/material data. A related lifecycle/control-plane gate does not prove this exact backup fixture; current Podman acceptance/reusable integration command does not select this exact opt-in test. Do not invent that coverage. After real proof, independently bind the complete five-file/status inventory and matching mandatory checks before any merge.
- #990 narrow fixture input remains blocked on this full native result; #998/o1 unchanged and protected. Codeman remains PAUSED; only the explicitly authorized #995 correction proceeded. No source policy exemption, artificially green finalcheck, native execution or merge.

### 2026-10-19 — Current trusted-target integration

- Existing #995 branch now 4ca9881766fc88e850ccdbbc2d837cabb19ebab5, a normal integration of independently reviewed be972ff source with trusted develop19548bf0. All five reviewed fixture/diagnostic source blobs remain unchanged.
- Actual PR CI39226862989: Trusted Plan, workflow policy, Focused Python, Guided, build, vet and Source Contracts PASS. Final117975666636 blocks only native coverage of the five paths; integration_sha_mismatch is absent.
- Full hosted Source Preflight39227471936 completed SUCCESS at that exact head. It is source validation, not the opt-in native recovery test. Earlier Qwen source assignments are historical; use only the latest exact-SHA PR handoff after its source precheck.
- Qwen's authorized isolated Podman lane must still prove the full SQL/Secrets/consumer/identity recovery assertions and actual automatic owned cleanup. No native success, immutable qualification or merge is asserted.

### 2026-10-19 — Exact integration full hosted source validation completed

- Current #9954ca9881766fc88e850ccdbbc2d837cabb19ebab5: actual complete Source Preflight39227471936 SUCCESS, job117977164941; full cmd/baha tests149.350s, formatting/readability, specified races, integration evidence, docs and snapshot/binary steps passed. Protected private-source access was skipped as configured. No native opt-in result or v0.4.26 release readiness is inferred.
- Independent integration review5569225959 positive. Superseding Qwen exact-SHA native assignment6263758673 published; native full recovery/automatic cleanup remains unexecuted here. Final Required PR check still correctly blocks native coverage; no merge or fake qualification.
