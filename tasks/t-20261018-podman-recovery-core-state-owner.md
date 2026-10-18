---
id: t-20261018-podman-recovery-core-state-owner
type: bug
areas: [runtime]
release: v0.4.26
version: ""
parent: v0.4.26
owner: "ChatGPT (bug-994 implementation session)"
priority: high
depends_on: [t-20261017-podman-backup-guided-runtime]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#995]
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261018-podman-recovery-core-state-owner · Podman recovery: resolve existing Core/OpenBao state without Compose assumptions #task #release/v0-4-26 #status/review #view/review #area/runtime #kind/bug
    <!-- generated:card -->
    **Owner:** ChatGPT (bug-994 implementation session) · **Priority:** high  
    **PR:** [baseharbor#995](https://github.com/mcpdev80/baseharbor/pull/995)  
    **Needs:** [t-20261017-podman-backup-guided-runtime](t-20261017-podman-backup-guided-runtime.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [t-20261017-podman-backup-guided-runtime](t-20261017-podman-backup-guided-runtime.md)  
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

- 2026-10-18: Complete review handoff, stacked [PR #995](https://github.com/mcpdev80/baseharbor/pull/995), branch `fix/t-20261018-podman-recovery-core-state-owner`, exact product SHA `560ae9be9c6093a48d1b4b9375286cf4e33fed28` (same source tree as tested `7b037b41cd6b071a55a231a5f291cc5de3bc7c25`); parent #990 SHA `bc6bb47a238e4fcd3d18c9ee4a51d7052f98616f`. Root cause: fixture used global `bhruntime.ExistingFiles("")` rather than existing selected-Target Core/OpenBao owner. Replaced test lookup with production `openBaoRuntime(ctx)` (selected runtime + Core-owned source files). The Podman runtime projects valid Core Compose input into Quadlet; no simulated Compose artifact or production code changes.
- New focused tests for Docker and Podman use the real Core source owner (`EnsureFilesForProjectAndResources`), confirm global isolated override is not consulted, selected project and resource identity is exact, and missing owned source fails closed. All old recovery SQL, secrets, identity and actual consumer checks unchanged. Go 1.26.9 isolated targeted tests passed: https://huggingface.co/jobs/ThunderHawk1080/6ad4894d5ccb47ba0f7c2ca5. Hosted CI run [39113728183](https://github.com/mcpdev80/baseharbor/actions/runs/39113728183) evaluated for exact final SHA: workflow policy, Trusted Plan, focused Python, CLI build, CLI vet, CLI guided and source contracts PASS. Mandatory `PR Selected Checks` FAILS closed solely with `coverage-unresolved` on the two modified acceptance fixture files. Native recovery has NOT been executed in this author session; separate independent coverage review and Qwen's real Podman retest are outstanding.  No live/SSH author test; independent review and Qwen native Podman recovery retest needed before release.

- 2026-10-18: Assigned and claimed before product changes. Initial source inspection: ExistingFiles("") resolves global Compose state, not selected Target; Core/OpenBao authority resides in openBaoRuntime(ctx) and existingTargetRuntimeFiles(ctx). Determine Podman-specific artifact resolution before coding.
