# CODEX-REVIEW 0427-129 — verified-no-change

## PLAN

1. Verify PR #1439's fix commit against the exact remote develop head and prove ancestry with `merge-base`.
2. Inspect the focused test on develop and identify its selected hosted CI group, trigger, and observed execution.
3. Compare the round-1 evidence against the card's acceptance text and record the verdict.
4. Publish this verification in baseharbor-plan and verify the remote evidence path.

## Verdict

**ROLLE: REVIEW**  
**URTEIL: ANNEHME-VERMERK**  
**0427-129 state:** VERIFIED-NO-CHANGE  
**Develop:** `07ae6c3e91b081a189266ca4b162ba705d4aa78f`  
**PR #1439 fix commit:** `449f107ffc11993952182a8889460dab88047f71`

### 1. Fix ancestry

Remote `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` returned `07ae6c3e91b081a189266ca4b162ba705d4aa78f`. In a fresh clone, `git merge-base --is-ancestor 449f107ffc11993952182a8889460dab88047f71 origin/develop` exited `0`. The computed merge base of the fix and develop is the fix commit itself, confirming PR #1439's debug-stack removal is in develop.

### 2. Focused regression and CI coverage

`TestMissingCandidateConsentDoesNotDumpRuntimeStack` exists on develop at `cmd/baha/app_candidate_consent_test.go:257`. It creates the repository-candidate fixture, calls the production `recordDeploymentBeforeMutation` path without candidate consent, asserts `errConsentRequiredForCandidateSubmission`, and fails if captured stderr contains `goroutine` or `runtime.Stack`.

The current CI group is `PR · Validation · go-unit-tests`. On develop, `.github/workflows/ci.yml` maps that validation to `scripts/pr-unit-database.sh`, which executes `go test ./... -count=1`; the test is in an ordinary `_test.go` file and is included in package discovery. The workflow is triggered for pull requests targeting `develop`. Hosted run `42462640598` on PR #1459 head `b69c096242a8940f5365b683532313a4fb89e5bc` completed successfully; its `go-unit-tests` job passed while this develop test was present in the tested tree. No workflow change or owner routing finding is needed.

### 3. Acceptance line

The round-1 evidence satisfies the acceptance condition for this verified-no-change card. The focused test covers the exact missing-consent branch that previously emitted the stack, verifies the required fail-closed consent error, and checks that stderr has no goroutine/stack text. On develop, `cmd/baha/app_apply.go:160-168` prints the candidate confirmation block, calls `recordDeploymentBeforeMutation`, and propagates that function's error; `cmd/baha/deployment_record.go:517-523` returns the consent error without a stack write. This is the unchanged production command path with the fixed function-level regression.

The regression is seam-level rather than a full CLI transcript: it does not assert the complete combined stdout/stderr byte stream or process exit code. That is a coverage limitation, not a blocker for the acceptance clause verified here, whose regression target is the stack leak in the production consent-refusal function. No consent semantics or exit-code change is proposed.

## Evidence source and repository witnesses

- The round-1 file is present in the supplied planning commit `16edc59a6e14a7348604a6d27a7549c540af85ca`; its tree entry is `100644 blob 03a4f3c975d17c1270640fb858d87a941785eabd evidence/r27-welle5-folge-2026-11-08/bughunt-regression-dbgdump/round-1.md`.
- The verified planning clone's `origin` is `https://github.com/mcpdev80/baseharbor-plan.git`; no product repository was modified.
- Product remote truth was checked with `git ls-remote`, not the quarantined workers/baseharbor checkout.
- No local test, rerun, dispatch, or container operation was performed for this review.

## Close recommendation

Close 0427-129 as VERIFIED-NO-CHANGE. Keep `TestMissingCandidateConsentDoesNotDumpRuntimeStack` in the package-wide `go-unit-tests` selection. Reopen only if that test is removed/skipped or if the consent-refusal path again emits a goroutine stack.

## END

END_DONE 0427-129-verify — ANNEHME-VERMERK; fix commit `449f107ffc11993952182a8889460dab88047f71` is an ancestor of develop `07ae6c3e91b081a189266ca4b162ba705d4aa78f`; focused regression is CI-selected and passing.

## Publication witnesses

Pre-publication remote output:

```text
55d1c6e37eb64d3ff815cebe3ab299da55b00345\trefs/heads/main
07ae6c3e91b081a189266ca4b162ba705d4aa78f\trefs/heads/develop
```
