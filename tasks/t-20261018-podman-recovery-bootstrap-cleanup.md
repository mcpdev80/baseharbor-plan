---
id: t-20261018-podman-recovery-bootstrap-cleanup
type: bug
areas: [runtime]
release: v0.4.26
version: ""
parent: v0.4.26
owner: "ChatGPT (PR #995 bootstrap-cleanup correction)"
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#995]
sources: []
blocker: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/commit/560ae9be9c6093a48d1b4b9375286cf4e33fed28"]
---

- [ ] t-20261018-podman-recovery-bootstrap-cleanup · Podman recovery acceptance: reuse initialized OpenBao and clean owned resources on failure #task #release/v0-4-26 #status/active #view/active #area/runtime #kind/bug
    <!-- generated:card -->
    **Owner:** ChatGPT (PR \#995 bootstrap-cleanup correction) · **Priority:** high  
    **PR:** [baseharbor#995](https://github.com/mcpdev80/baseharbor/pull/995)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/commit/560ae9be9c6093a48d1b4b9375286cf4e33fed28)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** none  
**Required by:** [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md), [t-20261018-podman-recovery-core-state-owner](t-20261018-podman-recovery-core-state-owner.md)  
**Owner:** ChatGPT (PR #995 bootstrap-cleanup correction)  
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
