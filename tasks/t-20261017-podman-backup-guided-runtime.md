---
id: t-20261017-podman-backup-guided-runtime
type: bug
areas: [runtime]
release: v0.4.26
version: ""
parent: v0.4.26
owner: "ChatGPT (bug-988 implementation session)"
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#990]
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261017-podman-backup-guided-runtime · Podman backup/restore: resolve isolated guided runtime and prove recovery #task #release/v0-4-26 #status/review #view/review #area/runtime #kind/bug
    <!-- generated:card -->
    **Owner:** ChatGPT (bug-988 implementation session) · **Priority:** high  
    **PR:** [baseharbor#990](https://github.com/mcpdev80/baseharbor/pull/990)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** none  
**Required by:** [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md), [t-20261018-podman-recovery-core-state-owner](t-20261018-podman-recovery-core-state-owner.md)  
**Owner:** ChatGPT (bug-988 implementation session)  
**Priority:** high  
**PRs:** [baseharbor#990](https://github.com/mcpdev80/baseharbor/pull/990)  
**Source:** 
<!-- /generated:links -->

## Goal

Run the existing native Podman disaster-recovery test successfully from isolated state and prove actual backup/restored data and consumer access.

## Scope

Own `TestAppBackupRestoreCLIRealDisasterRecovery` and its existing guided-up/runtime-selection fixture; locate the actual owner before editing. Change production runtime resolution only if reproduction demonstrates a production defect. No new backup/recovery engine, mocked native success or weakened safety checks.

## Acceptance

- Reproduce under the supported native runner configuration and compare runtime/environment/state setup.
- Establish whether the root cause is fixture/integration setup or product runtime selection, and correct that owner.
- Execute the actual disaster-recovery test through backup and restoration; verify restored data and consumer access.
- Missing runtime, skipped tests, mocks or failed recovery are not success evidence.
- Preserve isolation, ownership, consent and cleanup; independently review and have Qwen retest the corrected SHA before release.

## Required checks

Focused Go fixture/runtime-selection tests and existing trusted CI; targeted native `TestAppBackupRestoreCLIRealDisasterRecovery` with explicit Podman selection. No full release matrix.

## Dependencies and file ownership

- No unfinished product-task dependency is established. Before assignment, verify the exact existing CI lane, native fixture and non-overlapping write ownership. A missing trusted lane is an explicit prerequisite, never a self-exemption.
- Implementation belongs to an assigned development session; Qwen performs live testing and retesting only.
- Must be fixed and independently retested before v0.4.26 release (Maintainer instruction, 2026-10-17). Release preparation must depend on this task.

## Handoff

### 2026-10-20 - q18 review (CHANGES_REQUESTED)

- Local independent review: PR #990 head bc6bb47a - no workflow changes; native backup/restore NEVER executed in CI for this PR; coverage-unresolved. The durable native-Podman evidence was created by #995's focused job app_backup_restore_podman instead (run 39397436026, job 118544037959, PASS on Docker+Podman).
- Consequence: this task's remaining need is to bind that durable CI evidence to its acceptance (via #995 merge + evidence links) or extend #990 with the opt-in job; decision at Codex round 5 bundle. Evidence: evidence/board-2026-10-20/q18-995-990-review.md.


### 2026-10-19 — Current external acceptance dependency

- BLOCKED remains intentional: #9954ca9881766fc88e850ccdbbc2d837cabb19ebab5 includes the narrow fixture correction. Independent source/integration review and full hosted Source Preflight39227471936 PASS do not prove native recovery or actual owned automatic cleanup.
- Qwen exact-SHA native assignment6263758673 is current; older36310f/eaf868 source assignments are historical. Await that real result and matching independent qualification before accepting/superseding #990. Codeman source work may proceed independently.

### 2026-10-19 — PAUSED: BaseHarbor CI stabilization (coordinator hold)

- Existing ownership unchanged; no takeover. Candidate SHAs and prior handoffs preserved. Trusted gate reports `coverage-unresolved` (missing independent exact-bundle qualification); CI reruns, correction loops and merges are halted by Maintainer order. Independent local review state recorded in ecosystem `evidence/board-2026-10-19/` where a worker ran one.
- No new activity; partial fixture content remains inside #995 (`d359af83`), supersession logic of the pause decision unchanged.
### 2026-10-18 — Partial fix retained, full recovery remains blocked

- Open #990 `bc6bb47a238e4fcd3d18c9ee4a51d7052f98616f` supplies the selected-runtime fixture input now included in still-unmerged #995. It is not accepted native recovery evidence and is not closed as superseded before its replacement is accepted.
- Current #995 eaf86813 native run fails before backup on legacy manifest keys; automatic cleanup fails ownership verification. See [canonical correction task](t-20261018-podman-recovery-bootstrap-cleanup.md). Full recovery and release acceptance remain blocked.
- No ongoing source writes or native tests during Maintainer handover pause; existing ownership retained.


### 2026-10-18 — Native retest reaches next blocker; recovery not accepted
- Supplied exact-SHA Qwen run at `bc6bb47a238e4fcd3d18c9ee4a51d7052f98616f` confirms actual Podman Core startup after #990. It then fails at test line 52 on the Compose-only ExistingFiles lookup; backup/destroy/restore/verify have not run.
- [Follow-up bug #994](https://github.com/mcpdev80/baseharbor/issues/994) must be corrected/retested before release. Diagnose the real fixture/native Core state owner before declaring a general production defect or changing runtime/backup APIs. [PR evidence summary](https://github.com/mcpdev80/baseharbor/pull/990#issuecomment-6247879647).
- #988 remains open at the full recovery acceptance boundary. Target selection alone is not disaster-recovery success. No helper/global reset used; owned resources cleaned by the tester.


### 2026-10-17 — Independent source review; native retest required
- [Review 5560578165](https://github.com/mcpdev80/baseharbor/pull/990#pullrequestreview-5560578165) inspected exact candidate `bc6bb47a238e4fcd3d18c9ee4a51d7052f98616f`: bounded test-fixture Target setup; no production resolver or recovery assertions changed. No source-review blocker found in the correction.
- Actual [CI 39078042399](https://github.com/mcpdev80/baseharbor/actions/runs/39078042399) selected checks successful; finalcheck reports the two test paths unresolved. Generic jobs do not prove execution of this opt-in native disaster-recovery test.
- Qwen owns the exact-candidate Podman native retest after the current #989 test assignment: actual backup/restore, SQL data, secrets, consumer access and token/certificate regeneration. Any later failure remains an open bug; fixture readiness is not recovery success. Keep authorized isolation, consent and cleanup; no private machine information in public evidence.
- Formal coverage qualification and bug acceptance remain pending actual evidence. No additional reviewer execution (local executor offline/HF Jobs unavailable), no merge or CI exception. Existing claim/status/generated views preserved.


- 2026-10-18: Exact PR CI run [39078042399](https://github.com/mcpdev80/baseharbor/actions/runs/39078042399) evaluated. Workflow policy, Trusted Plan, CLI guided/vet/build, source contracts and focused Python succeeded. The required `PR Selected Checks` stayed fail-closed with `coverage-unresolved` for precisely `cmd/baha/app_backup_restore_integration_test.go` and `cmd/baha/app_backup_runtime_fixture_test.go`; native backup/restore was NOT run, and other skipped gates are not evidence of recovery. Independent mapping/qualification belongs to the Manager, while Qwen must subsequently execute the explicitly selected real Podman disaster-recovery test and prove restored SQL/secret/consumer access before release. No CI policy relaxation or author self-qualification.

- 2026-10-18: Candidate handed off for independent review: product PR [#990](https://github.com/mcpdev80/baseharbor/pull/990), branch `fix/t-20261017-podman-backup-guided-runtime`, exact product source `bc6bb47a238e4fcd3d18c9ee4a51d7052f98616f` against `develop` `d54ac358fb6a6b256164ac2689a33e981c013baa`. Root cause is a test fixture error: isolated state had no configured Podman Target, so the product correctly resolved its implicit Docker default. The fixture now creates a local Target with the explicitly selected native runtime before `runtimeUpGuided`, rejects unsupported runtime names, and verifies effective selection. No production runtime resolver, ownership or consent checks were modified. Real backup, restore, restored SQL data/secret and identity assertions are retained unchanged.
- Focused isolated Go 1.26.9 `TestAppBackupGuidedRuntimeFixture*` Docker/Podman/invalid cases, vet, build, formatting and diff checks PASSED: https://huggingface.co/jobs/ThunderHawk1080/6ad40008c66288145226d095. Trusted exact-SHA PR CI: https://github.com/mcpdev80/baseharbor/actions/runs/39078042399 (results to be evaluated separately). Native `TestAppBackupRestoreCLIRealDisasterRecovery` still requires Qwen's independently reviewed Podman retest; this author's isolated unit tests do NOT establish restored data or consumer access. No SSH/live author test, source qualification, self-acceptance, merge or #978 changes.


- 2026-10-18: Claim published by ChatGPT (bug-988 implementation session) before product changes. Owner scope: the existing backup/restore integration fixture and its guided runtime selection. Production runtime implementation changes require confirmed production defect. No native/SSH retest or #978 changes.

- 2026-10-17: Maintainer-authorized intake from Qwen's supplied pre-freeze audit; this session did not independently reproduce the native failure. The audit reports immediate failure in `runtimeUpGuided`: `runtime up: container runtime orchestration not found` / `ErrRuntimeNotFound`, under isolated state and Podman test selection. Other in-process native Core tests passed. Root cause remains unconfirmed; no successful disaster-recovery evidence exists. Source: `d54ac358fb6a6b256164ac2689a33e981c013baa`.
- Discussion/evidence intake: [baseharbor#988](https://github.com/mcpdev80/baseharbor/issues/988). Unassigned, not implemented or accepted. No private machine identifiers, addresses, local paths or credentials included.

### 2026-10-19 — Narrow fix versus full recovery acceptance

- #990 remains unchanged at bc6bb47a238e4fcd3d18c9ee4a51d7052f98616f. Its target-selection fixture correction is already included in pending #995; accepting it alone would not prove native backup/restore. Do not close this release dependency as successful or duplicate its implementation.
- Current #995 candidate 2ff6846c3b4d246d1291ae2c90d09d231c4214bc has valid integration (39183081916), but full four-file re-review, real native recovery and fail-path owned cleanup evidence remain outstanding. Owner: paused Codeman Flash for source; Qwen/authorized native lane for actual run, after separate source qualification. This coordinator does not have authorized native execution access. Claim retained.

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

### 2026-10-20 - q19 stacked resolution (review)

- PR #990 head 50ad8d72: #995 branch merged in (ancestor 0af3982b confirmed) so the durable native job app_backup_restore_podman executes against this PR too; all 17 mandatory checks pass, MERGEABLE.
- Minimal honest option per q19: reuse #995 gate instead of duplicating a job. Merge order note: merging #990 first makes #995 auto-merge-closable (empty diff). Independent local review record: evidence/board-2026-10-20/q18-995-990-review.md + q19-990-native-job.md. Awaits Codex round 5 bundle.

### 2026-10-20 - Codex podman-pair review round

- Codex stack ruling: no squash auto-close assumption; re-stacking happens AFTER #995 P1 fixes (q20).
