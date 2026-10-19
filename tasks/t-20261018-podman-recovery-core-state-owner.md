---
id: t-20261018-podman-recovery-core-state-owner
type: bug
areas: [runtime]
release: v0.4.26
version: ""
parent: v0.4.26
owner: "ChatGPT (bug-994 implementation session)"
priority: high
depends_on: [t-20261017-podman-backup-guided-runtime, t-20261018-podman-recovery-bootstrap-cleanup]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#995]
sources: []
blocker: "Native recovery and owned automatic-cleanup proof at 4ca9881766fc88e850ccdbbc2d837cabb19ebab5, then exact five-file qualification and green Required CI are still missing."
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/commit/36310f08467f6e963f080b22936ffbaf5d763b74","https://github.com/mcpdev80/baseharbor/actions/runs/39219870611","https://github.com/mcpdev80/baseharbor/pull/995#pullrequestreview-5568575016","https://github.com/mcpdev80/baseharbor/pull/995#issuecomment-6262605610"]
---

- [ ] t-20261018-podman-recovery-core-state-owner · Podman recovery: resolve existing Core/OpenBao state without Compose assumptions #task #release/v0-4-26 #status/blocked #view/blocked #area/runtime #kind/bug
    <!-- generated:card -->
    **Owner:** ChatGPT (bug-994 implementation session) · **Priority:** high  
    **PR:** [baseharbor#995](https://github.com/mcpdev80/baseharbor/pull/995)  
    **Blocker:** Native recovery and owned automatic-cleanup proof at 4ca9881766fc88e850ccdbbc2d837cabb19ebab5, then exact five-file qualification and green Required CI are still missing.  
    **Needs:** [t-20261017-podman-backup-guided-runtime](t-20261017-podman-backup-guided-runtime.md), [t-20261018-podman-recovery-bootstrap-cleanup](t-20261018-podman-recovery-bootstrap-cleanup.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/commit/36310f08467f6e963f080b22936ffbaf5d763b74), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/39219870611), [proof 3](https://github.com/mcpdev80/baseharbor/pull/995#pullrequestreview-5568575016), [proof 4](https://github.com/mcpdev80/baseharbor/pull/995#issuecomment-6262605610)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [t-20261017-podman-backup-guided-runtime](t-20261017-podman-backup-guided-runtime.md), [t-20261018-podman-recovery-bootstrap-cleanup](t-20261018-podman-recovery-bootstrap-cleanup.md)  
**Required by:** [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md)  
**Owner:** ChatGPT (bug-994 implementation session)  
**Priority:** high  
**PRs:** [baseharbor#995](https://github.com/mcpdev80/baseharbor/pull/995)  
**Source:** 
<!-- /generated:links -->

## Goal

Correct the Compose-only lookup in the native Podman backup/restore fixture using established selected-Target Core/OpenBao authority.

## Scope

Own TestAppBackupRestoreCLIRealDisasterRecovery and focused tests. Production runtime changes only for a demonstrated product defect. Preserve real native backup/restore verification, secret protection, consent and scoped cleanup.

## Acceptance

- Focused Docker and Podman selection/state regressions, without inventing Compose files.
- Exact-SHA independent review followed by Qwen's real Podman recovery retest proving restored SQL data, secrets, consumer access and regenerated credentials.
- No non-native CI substituted for native recovery evidence.

## Required checks

Focused Go fixture and state-resolution tests, targeted hosted PR CI, planning render/check/tests. No author live/SSH tests.

## Dependencies and file ownership

- Follow-up to [#988](https://github.com/mcpdev80/baseharbor/issues/988) and [PR #990](https://github.com/mcpdev80/baseharbor/pull/990); #990 is not accepted native recovery evidence.
- Required by v0.4.26 release preparation.
- Bounded ownership: existing backup/restore native test and direct tests; shared Core/OpenBao product code only for proven production issue.

## Handoff

### 2026-10-19 — Actual full-path correction published; native assignment updated

- Exact #995 candidate: be972ff39006037a9f06b904c156fe73f7f24ba8. Operations now obtain one current typed acknowledgement from their actual fail-closed authority; restore has separate destructive scope consent. Stale/unknown errors do not cause approval loops. SQL seeding/readback uses the protected current consumer binding with verified TLS, no guessed runtime project/provider role.
- Actual [CI39223771804](https://github.com/mcpdev80/baseharbor/actions/runs/39223771804) Guided/build/vet/source checks pass. The Guided wrapper selects all8 existing fixture/manifest regressions plus new consent/SQL tests; nonverbose logs are not individually enumerated receipts. Full five-file source review [5568897605](https://github.com/mcpdev80/baseharbor/pull/995#pullrequestreview-5568897605) is positive; final remains unresolved on5paths, with valid integration.
- Latest [Qwen exact-SHA native assignment](https://github.com/mcpdev80/baseharbor/pull/995#issuecomment-6263247019) supersedes36310f for final acceptance. The real opt-in native Backup/Destroy/Restore, actual consumer data/secrets, non-replayed identities and owned automatic cleanup have not been executed here. gofmt of these changed fixture files remains an explicit native precheck; no unsupported success claim.
- Keep #990 and the recovery chain unaccepted until that actual result, fresh qualification and green mandatory CI exist. No reset/SSH/native execution by this coordinator.

### 2026-10-18 — Latest native failure supersedes Bootstrap blocker

- Exact #995 eaf86813 now passes the former second-Bootstrap step but fails on obsolete fixture manifest keys before backup. Registered approved cleanup executes yet fails ownership verification and leaves owned runtime resources. See [current canonical correction task](t-20261018-podman-recovery-bootstrap-cleanup.md) for exact evidence and bounded resume instructions.
- Earlier already-initialized diagnosis is historical, not the current blocker. Full native recovery still unproven; no task acceptance or merge. Maintainer paused further writes/testing for Horde/Codex handover; existing ownership retained.


### 2026-10-18 — Native retest failed; acceptance blocked

- Qwen reports exact `560ae9be9c6093a48d1b4b9375286cf4e33fed28` fails 2/2 clean native Podman starts before backup: fixture calls openbao.Bootstrap after runtimeUpGuided has already initialized the real Core. Error: OpenBao is already initialized. Own Core/Identity resources leaked on assertion failure; Qwen removed only owned resources and restored baseline.
- Canonical release-blocking follow-up: [t-20261018-podman-recovery-bootstrap-cleanup](t-20261018-podman-recovery-bootstrap-cleanup.md). Existing selected-Target state fix remains useful, but neither generic green CI nor that partial source review proves full disaster recovery. SQL data, secrets, consumer and token/certificate regeneration remain untested.
- No product recovery defect established, no native rerun by manager, no acceptance or merge. Continue correction on existing #995; Qwen retests only after independently reviewed new candidate. Derived views require executable regeneration on current main.

### 2026-10-18 — Independent #995 source review; ready for native retest
- [Review 5562279087](https://github.com/mcpdev80/baseharbor/pull/995#pullrequestreview-5562279087) inspected exact candidate `560ae9be9c6093a48d1b4b9375286cf4e33fed28`: test now uses existing openBaoRuntime(ctx) for a matched selected-Target runtime/files pair, instead of global ExistingFiles. No production resolver or recovery safety policy changed; no new source blocker found.
- Actual CI 39113728183 selected checks successful; finalcheck still blocked. Generic jobs are not native disaster-recovery evidence.
- Qwen next: exact-SHA real Podman full recovery, SQL data, secrets, consumer access and token/certificate regeneration; retain existing assertions, clean only owned resources, no global/helper reset. Record the exact next failure if any; full recovery remains unproven until this run.
- Formal coverage and bug acceptance remain open; no additional reviewer local/native execution, merge or self-approval.


- 2026-10-18: Complete review handoff, stacked [PR #995](https://github.com/mcpdev80/baseharbor/pull/995), branch `fix/t-20261018-podman-recovery-core-state-owner`, exact product SHA `560ae9be9c6093a48d1b4b9375286cf4e33fed28` (same source tree as tested `7b037b41cd6b071a55a231a5f291cc5de3bc7c25`); parent #990 SHA `bc6bb47a238e4fcd3d18c9ee4a51d7052f98616f`. Root cause: fixture used global `bhruntime.ExistingFiles("")` rather than existing selected-Target Core/OpenBao owner. Replaced test lookup with production `openBaoRuntime(ctx)` (selected runtime + Core-owned source files). The Podman runtime projects valid Core Compose input into Quadlet; no simulated Compose artifact or production code changes.
- New focused tests for Docker and Podman use the real Core source owner (`EnsureFilesForProjectAndResources`), confirm global isolated override is not consulted, selected project and resource identity is exact, and missing owned source fails closed. All old recovery SQL, secrets, identity and actual consumer checks unchanged. Go 1.26.9 isolated targeted tests passed: https://huggingface.co/jobs/ThunderHawk1080/6ad4894d5ccb47ba0f7c2ca5. Hosted CI run [39113728183](https://github.com/mcpdev80/baseharbor/actions/runs/39113728183) evaluated for exact final SHA: workflow policy, Trusted Plan, focused Python, CLI build, CLI vet, CLI guided and source contracts PASS. Mandatory `PR Selected Checks` FAILS closed solely with `coverage-unresolved` on the two modified acceptance fixture files. Native recovery has NOT been executed in this author session; separate independent coverage review and Qwen's real Podman retest are outstanding.  No live/SSH author test; independent review and Qwen native Podman recovery retest needed before release.

- 2026-10-18: Assigned and claimed before product changes. Initial source inspection: ExistingFiles("") resolves global Compose state, not selected Target; Core/OpenBao authority resides in openBaoRuntime(ctx) and existingTargetRuntimeFiles(ctx). Determine Podman-specific artifact resolution before coding.

### 2026-10-19 — Current external dependency, no false acceptance

- Superseding #995 now 2ff6846c3b4d246d1291ae2c90d09d231c4214bc preserves worker d359af83 source in a genuine develop integration. Run 39183081916 confirms integration mismatch repaired and focused validations green; four-file full source qualification and actual native recovery remain missing.
- Historic eaf86813 manifest/cleanup failures are retained as history, not asserted against untested current source. Completion requires independent source re-review and Qwen's authorized exact-SHA full recovery/cleanup result. Paused Codeman owner remains unchanged; no coordinator product implementation or native run.

### 2026-10-19 — Complete independent current-source review

- Full four-file exact-source review of 2ff6846c3b4d246d1291ae2c90d09d231c4214bc is now complete, not deferred: CHANGES REQUIRED, review https://github.com/mcpdev80/baseharbor/pull/995#pullrequestreview-5566018799.
- Confirmed P2: ownershipSubject returns applicationDestructionPlan.Scope.Owner.Subject, which the actual destruction owner fills with DeploymentID; approvedNativeFixtureCleanup logs it. This violates the new coarse-only/no-ID diagnostic contract. Emit fixed categories by actual plan type, never raw Subject/Owner, and add sentinel identity/project/target/path regressions with real machine.Error and plan types. No actual private identifiers are published.
- Manifest/parser, authenticated readiness, early cleanup registration, fresh bounded context, recovery assertions and consent/ownership guards are retained. No further confirmed source blocker. Diagnostic wrapper does not prove successful cleanup; full authorized native recovery and fail-path ownership evidence remain absent.
- Flash/Codeman retains product claim while paused; Qwen/authorized native lane owns retest only after corrected independent source review. Infrastructure coordinator neither overwrites paused source nor grants source/native coverage.

### 2026-10-19 — Final stabilized integration handoff

- Current #995 HEAD02b4cd5f48e449085bc58df625ef6af8fa7bbd73, trusted develop7827e6491a7715e0ffffb1e7938764f6788cc30b. Four worker source blobs unchanged; no product correction or claim transfer by CI coordinator.
- Actual CI39185883757: Trusted Plan, policy, Focused Python, Guided, build, vet and Source Contracts SUCCESS; final117848399067 blocks only qualified native coverage of the four source files, not integration_sha_mismatch. Current trusted plan artifact retained30days. Final PR handoff5566105009.
- Source CHANGES REQUIRED review5566018799 remains applicable: bound diagnostic output to fixed owner categories, exclude raw identities and prove sentinels. Paused Flash/Codeman owns correction after explicit continuation; then independent re-review and authorized Qwen full recovery/owned-cleanup proof. #990 narrow fix remains dependent and unaccepted; existing claims preserved. No source policy waiver, native run or merge of #995/#990. Infrastructure acceptance never resumes Codeman automatically.

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
