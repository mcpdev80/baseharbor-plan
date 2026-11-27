# PR #1884 / card 0428-292 — exact-head content review

ROLE=REVIEW
Reviewer lane: `w267-0428-284-pridentity`
Task owner from current Plan main: `w399-0428-289-providers`.
Plan main reviewed: `2f40ca1630f5919ec7c129a038ff6e2185130966`.
Task: https://github.com/mcpdev80/baseharbor-plan/blob/2f40ca1630f5919ec7c129a038ff6e2185130966/tasks/t-20261116-r28-bug-apply-consent-ux.md
Evidence on Plan main: https://github.com/mcpdev80/baseharbor-plan/blob/2f40ca1630f5919ec7c129a038ff6e2185130966/evidence/2026-11-27/0428-292/korrektur-1884-fix.md
Evidence blob: `9a41e563bd19a2ffa90c3e993ab668fc7a147e85`.

## Exact candidate and diff

Repo `mcpdev80/baseharbor`, PR #1884, branch `lane-0428-292-consent-ux`, exact head `4e499b3cf67ad86cb022640589dba05bfa26922d`, current `develop` `6944e8761af6f07b801f55e39bb9a5409226c10b`. PR state OPEN. Current develop is an ancestor of the candidate.

The exact diff contains nine paths: `cmd/baha/app_apply.go`, `cmd/baha/app_candidate_consent.go`, `cmd/baha/app_candidate_consent_interactive.go`, `cmd/baha/app_candidate_consent_test.go`, `cmd/baha/app_edit_apply_result.go`, `cmd/baha/app_remote_lifecycle.go`, `cmd/baha/core_installation.go`, `cmd/baha/deployment_record.go`, and `scripts/pr-gate-coverage.json`; diff stat 820 insertions, 41 deletions. `git diff --check` is clean. The correction aligns the prompt reader with the terminal decision and preserves the candidate digest revalidation at the write boundary.

## Review verdict: CHANGES

Finding — the interactive consent is stored in a process-global singleton and can survive the invocation that created it. `cmd/baha/app_candidate_consent_interactive.go:22-35` stores only application/target/digest globally. At `:45-50`, a write attempt for a different identity returns without consuming or clearing the saved binding. At `:72-76`, an explicit `--confirm-candidate` value also wins without consuming the binding. The normal lifecycle clears it only through `recordFailedDeployment` (`cmd/baha/app_apply.go:268-272`); a successful lifecycle has no corresponding unconditional cleanup. The next invocation for the original application and target can therefore consume a prior invocation's `y`, even if the current prompt was refused or never answered. The identity/digest recheck prevents a changed candidate from matching, but it does not prevent stale consent for the same unchanged candidate from crossing invocation boundaries.

Correction recipe: scope the interactive confirmation to the apply invocation itself, preferably as an invocation-local/context-carried token consumed only by that call's `recordDeploymentBeforeMutation`. If the existing singleton remains, clear it at every lifecycle entry/exit and consume or retire it on explicit-flag use and identity mismatch; do not leave it available for a later same-identity invocation. Add sequential-call regressions: bind A then make an unrelated B attempt and verify a later A without a new affirmative answer fails closed; also bind A while an explicit flag is supplied and verify a later A refusal cannot reuse that binding. Preserve current-source digest recomputation and constant-time comparison.

## Required checks and current state

The task requires positive and negative consent regressions, red-first reproduction, path-to-test mapping, actual exact-SHA hosted test execution, and separate Docker/rootless Podman evidence where the lifecycle behavior is shared. The akte lists `TestInteractiveCandidateConsentCarriesToWriteWithoutSecondFlag`, `TestInteractiveCandidateConsentRefusalKeepsFailClosed`, `TestNonInteractiveCandidateConsentKeepsFlagContract`, `TestQueuedNonTerminalReaderNeverGrantsBindConsent`, `TestWithApplicationInputPreservesTerminalIdentity`, and `TestRemoteApplyRouteInlineBindContractIsTruthful` on the existing CLI/package route.

Runs `46046111688` and `46046309439` are distinct pull_request events on the exact head and correct branch. Both terminal results are FAILURE: Trusted Plan is red under the known class-A freeze; `PR Selected Checks` then reports `UNIT_SCOPE` empty and `UNIT_RESULT=skipped` with `REJECT: Go test selection missing or invalid`. Thus the new tests and the required native runtime gates were not qualified on this exact head. The run pair is valid as two pull_request-context witnesses, but it is not a passing test receipt.

No local tests were run. No PR mutation or merge was performed; Freeze #136 remains active.

END_DONE w267-0428-284-pridentity: #1884 content review completed as CHANGES at 4e499b3cf67ad86cb022640589dba05bfa26922d; no merge.
