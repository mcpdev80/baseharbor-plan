# PR #1750 exact-head review follow-up — 17f471cd3fe9a41fbe5b4e2d3d2748f1e1bf9c99

## PLAN

1. Read the updated #1750 review contract and record its two specific questions and restrictions. DONE.
2. Reconfirm the exact PR head, base, and terminal selected-check result. DONE.
3. Inspect the exact source and diagnosis evidence for temporary-directory cleanup and selection-state isolation. DONE.
4. Classify both points and record any fix recipe without running tests or changing product/PR state. DONE.
5. Validate and publish this evidence, verify its remote path, update the board, and post END.

## Review target and provenance

- Role: CODEX-REVIEW, read-only. PR #1750, card 0428-223 / `t-20261121-develop-full-suite-red`.
- Exact head: `17f471cd3fe9a41fbe5b4e2d3d2748f1e1bf9c99`; exact base `develop` at `82825e95a6f6083702d0ba5401d97f356085c722`.
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1750/head` returned `82825e95a6f6083702d0ba5401d97f356085c722 refs/heads/develop` and `17f471cd3fe9a41fbe5b4e2d3d2748f1e1bf9c99 refs/pull/1750/head`.
- PR remains open, ready (not draft), mergeable/clean. No branch, PR, review, or workflow state was changed.

## Point 1 — host config isolation directory cleanup

Finding: `cmd/baha/test_operator_context_test.go:112-121` has a real cleanup omission. `hostConfigIsolationDir` creates the directory with `os.MkdirTemp("", ...)`, which places it under the process temporary directory; it is not beneath a testing temporary root and this helper does not register cleanup. Thus the comment at lines 113-115 that the directory is discarded with the test temporary root is inaccurate. A test that observes the host organization-selection file leaves a `baseharbor-0428-223-cfg-*` directory after completion.

Classification: non-blocking P3 test-hygiene issue for this PR, not a functional or security blocker. The required checks use GitHub-hosted runners, whose job environment is disposable; repeated local invocations can still leave these small directories behind. This is a real leak, not the documented consequence implied by the comment.

Fix recipe: change the helper to accept `*testing.T` and return `t.TempDir()` (or register `t.Cleanup` for `os.MkdirTemp`). Add or adapt a focused test to exercise the host-selection isolation path and ensure cleanup is owned by the test. Stop when the helper no longer creates an unowned system-temp directory and the regression remains green in the existing Go CI shard.

## Point 2 — early return in selection isolation

Finding assessment: the early return at `cmd/baha/test_operator_context_test.go:75-84` could preserve a leaked `BASEHARBOR_TARGET` or `BASEHARBOR_STATE_DIR` in a future test that calls this helper without owning that selection. It relies on the caller knowing whether those values are fixture-owned; it cannot distinguish fixture state from stale process state. That is a latent hardening concern.

It does not conceal the diagnosed 14-test failure source. The published `develop-full-suite-red/diagnose-1.md` classifies groups A-C as the host-persisted organization selection (`organization/active.json`, resolving `company-dev`) read through the host config root; when that file is visible and neither selection variable is present, this helper redirects `XDG_CONFIG_HOME` to a private directory. Group D is a self-executed child inheriting selection environment; the candidate filters `BASEHARBOR_TARGET`, `BASEHARBOR_STATE_DIR`, and `BASEHARBOR_ENV` through `envWithoutLeakedTargetSelection` before launching it. The cited `application_lifecycle_lock_test.go:171-172` and `:528-529` raw `os.Setenv` calls are inside child-only branches, so they mutate the child process, not the parent test process. The bootstrap `BASEHARBOR_TARGET` setter in `runtime_integration_test_support_test.go:868-880` registers a deferred `os.Unsetenv` immediately after setting it. The package-wide XDG `os.Setenv` calls create the intended private package roots and are not `company-dev` selection leaks.

Classification: not a blocker for the reported 14 failures; the exact root cause is covered by disk-selection isolation and child-environment filtering. The guard remains a latent test-order risk if a future parent-process test uses raw `os.Setenv` for those selection variables.

Fix recipe: as follow-up hardening, make fixture ownership explicit (for example, pass an explicit preserve-selection option only to fixtures that need it), and otherwise clear stale selection state before the test resolves a Target. Add a regression that seeds a process-level selection, invokes the unconfigured-test isolation path, and verifies the stale selection cannot win. Stop when fixture-owned selection remains intact while an unowned stale selection is neutralized, with the case selected by the existing Go CI shard.

## Hosted checks

- Exact-head run `44982566548` is terminal `completed/success` on `17f471cd3fe9a41fbe5b4e2d3d2748f1e1bf9c99`.
- `gh pr checks 1750 --required` reports `PR Selected Checks pass`, job `137087212830`. The aggregate completed the selected native-acceptance, complete selected Go-shard-coverage, and normal selected-job-result checks.
- The run skipped `PR · Selected Runtime` and `validate`; the Targeted HA Docker and Podman jobs were also skipped. These skips are not presented as successful receipts. The code changes under review are test-only, and the current required aggregate is green.

## Verdict

VERDICT: APPROVE

The temporary directory leak is a non-blocking P3 cleanup issue, and the early return does not conceal the reported 14-test root cause. The identified latent guard risk has a concrete follow-up recipe above; no current same-process raw selection setter was found in the cited path. No test was run locally.

## repo-rule compliance

- Read-only exact-head source and hosted-run review. No local tests, product edits, GitHub review/comment, PR-state change, merge/close, workflow dispatch, or subagents.
- Planning remote verified as `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and push URL is the same.
- Evidence lives only in the true `baseharbor-plan` repository. No product checkout or quarantined worker checkout was used.
- Prior exact-head evidence is preserved; this file resolves its two follow-up classifications.

## cleanliness

- Before review: PID 2142367; `docker ps -a` showed no containers.
- After review: PID 2170152; `docker ps -a` showed no containers.
- No container or compose project was started.

END codex-rev-1747 DONE — #1750 exact head 17f471cd3fe9a41fbe5b4e2d3d2748f1e1bf9c99 APPROVE; temp-dir leak is non-blocking; early return does not mask the diagnosed 14 failures.

Planning evidence commit SHA: pending.
