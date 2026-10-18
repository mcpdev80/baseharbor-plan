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
prs: []
sources: ["mcpdev80/baseharbor#994", "mcpdev80/baseharbor#988", "mcpdev80/baseharbor#990"]
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261018-podman-recovery-core-state-owner · Podman recovery: resolve existing Core/OpenBao state without Compose assumptions #task #release/v0-4-26 #status/active #area/runtime #kind/bug

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

- 2026-10-18: Assigned and claimed before product changes. Initial source inspection: ExistingFiles("") resolves global Compose state, not selected Target; Core/OpenBao authority resides in openBaoRuntime(ctx) and existingTargetRuntimeFiles(ctx). Determine Podman-specific artifact resolution before coding.
