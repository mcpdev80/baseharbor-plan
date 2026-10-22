---
id: t-20261018-podman-recovery-core-state-owner
type: bug
areas: [runtime]
release: v0.4.26
version: ""
parent: v0.4.26
owner: Flash (codeman w1-baseharbor)
priority: high
depends_on: [t-20261017-podman-backup-guided-runtime, t-20261018-podman-recovery-bootstrap-cleanup]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#995, mcpdev80/baseharbor#1027]
sources: []
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1027", "https://github.com/mcpdev80/baseharbor/commit/213c15e43ac9f3c333ad5eabed202475eefb501f", "https://github.com/mcpdev80/baseharbor/actions/runs/39623691937", "https://github.com/mcpdev80/baseharbor/actions/runs/39605258769"]
---

- [x] t-20261018-podman-recovery-core-state-owner · Podman recovery: resolve existing Core/OpenBao state without Compose assumptions #task #release/v0-4-26 #status/closed #view/closed #board/planned #area/runtime #kind/bug
    <!-- generated:card -->
    **Owner:** Flash (codeman w1-baseharbor) · **Priority:** high  
    **PR:** [baseharbor#995](https://github.com/mcpdev80/baseharbor/pull/995), [baseharbor#1027](https://github.com/mcpdev80/baseharbor/pull/1027)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1027), [proof 2](https://github.com/mcpdev80/baseharbor/commit/213c15e43ac9f3c333ad5eabed202475eefb501f), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/39623691937), [proof 4](https://github.com/mcpdev80/baseharbor/actions/runs/39605258769)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [t-20261017-podman-backup-guided-runtime](t-20261017-podman-backup-guided-runtime.md), [t-20261018-podman-recovery-bootstrap-cleanup](t-20261018-podman-recovery-bootstrap-cleanup.md)  
**Required by:** [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md)  
**Owner:** Flash (codeman w1-baseharbor)  
**Priority:** high  
**PRs:** [baseharbor#995](https://github.com/mcpdev80/baseharbor/pull/995), [baseharbor#1027](https://github.com/mcpdev80/baseharbor/pull/1027)  
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

> CURRENT (2026-10-22): slice accepted via #1027 (native evidence run 39605258769); #995 CLOSED-superseded. Entries below are historical. See evidence/codeman-2026-10-21/HANDOFF.md.


### 2026-10-21 — ACCEPTED: complete rootless recovery integrated

- Owner-authorized Maintainer acceptance: [#1027](https://github.com/mcpdev80/baseharbor/pull/1027) merged as `213c15e43ac9f3c333ad5eabed202475eefb501f`. All nine required validations, Focused Python, Workflow policy and authenticated final verification PASS in [39623691937](https://github.com/mcpdev80/baseharbor/actions/runs/39623691937).
- Independently reviewed exact native source `77eb9a120f46b42281198fcee1de788c9779be18`, seventeen unchanged paths, integrated through a Git-proven clean merge with accepted Core921. Actual rootless Podman [39605258769](https://github.com/mcpdev80/baseharbor/actions/runs/39605258769), job119239688725, proves full Backup/Destroy/Restore in 230.76s, real SQL marker and secret restoration, READY consumer access, regenerated token/client certificate and no secret leakage. No missing runtime or skipped native test is accepted.
- Owned cleanup and foreign-volume ID/CreatedAt/label preservation PASS; the independent sentinel is removed only through its own owner. Artifact12348242787, SHA256 `98db0dd357326383ddf88855748114330e4a5674d21e51d9cb0552db4c763a77`, retains these receipts.
- Canonical Core/OpenBao state and protected service bindings replace fixture guesses; workload stop selects only canonical workload services and preserves backend/sibling/other Target resources. Bounded fresh-context failure recovery retains original and recovery errors. Focused positive/negative source/runtime/cleanup regressions and independent complete source review PASS.
- #995 and #990 are closed as superseded, preserving original descriptions, source ancestry, claims and historical failures. All three shared recovery slices are accepted together; final integrated release/consumer qualification remains open.


### 2026-10-21 — Waiting for the shared recovery integration; no independent active implementation

- The actual Core/OpenBao state-owner correction is included in native-proven source77eb9a12. Full rootless Podman [39605258769](https://github.com/mcpdev80/baseharbor/actions/runs/39605258769) and an independent complete PG17 source re-review PASS. No missing native execution or Qwen-only hold remains.
- Backup/guided and bootstrap/cleanup slices are being integrated together through the same qualified product candidate. This dependent card is PLANNED/WAITING until those actual prerequisites are accepted, rather than a second ACTIVE worker. Existing Flash ownership/history is preserved; there is no separate implementation session or independent additional fix outstanding here.
- Accept this slice with the final merged recovery source/current required CI and its genuine owner/cleanup evidence, not with local tests or the old #995 head alone.


### 2026-10-21 — Current-source cleanup defect requires correction

- Revalidated current #995 source `335477ea96c5992c0ec5e64fc4ce16295cf853e7`; old `4ca98817` acceptance prose does not cover subsequent broker/inventory/workflow changes. [Current CI 39431592234](https://github.com/mcpdev80/baseharbor/actions/runs/39431592234) blocks eight unresolved paths.
- Independent read-only source review found a real P1: `targetDestroyInventoryResourceMissing` converted any project-wide error containing missing-resource text into successful absence, skipping residual volume/resource verification. This is now a source correction task, not a review-ready result. A disjoint local fix removes the shortcut and keeps absence verification with the runtime resource owner. Five negative real-cleanup regressions were red before and green after; focused existing families and vet PASS.
- Actual [native Podman 39413721398](https://github.com/mcpdev80/baseharbor/actions/runs/39413721398) at older `321c138f` failed at unhealthy broker before Backup; current broker timeout changes require a new actual proof. Claimed run `39397436026` returns 404 and is not accepted. Genuine automatic cleanup plus foreign runtime preservation is still required; no merge or native PASS is inferred.


### 2026-10-20 coordinator observation (read-only, no takeover)

- PR #995 head advanced (4ca98817) by its owning session; still OPEN, BEHIND develop, PR Selected Checks failing at last observed run. Native recovery evidence remains with the owner session per 2026-10-19 decision; this lane stays untouched by the coordinator pool.


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

## Handoff

### 2026-10-20 - coordinator correction

- Worker commit 241ac78 set accepted/closed prematurely. Acceptance is a maintainer decision (AGENTS.md). PR #995 is CI-green (run 39397436026, incl. durable native job app_backup_restore_podman on Docker+Podman) and independently review-APPROVED locally (evidence/board-2026-10-20/q18-995-990-review.md pane-confirmed); card is at review pending Codex round 5 and merge.

### 2026-10-20 - Codex podman-pair review round

- codex-verdict-podman-pair.md: CHANGES_REQUESTED 5x P1; correction lane q20 running (P1-1..5); prior q17/q18 acceptance claims corrected.

### 2026-10-20 - carried finding (blocker text moved out of field; card active with fix running)

- Pre-existing product defect: broker readiness 60s window too short for OpenBao PKI bootstrap (fails VM and hosted alike; earlier demo-binary PASS claims did not execute this fixture). Fix attempt 1 (q20, fixture-side knob preferred) running.
