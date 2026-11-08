# CODEX-REVIEW 0427-127 r3 — PR #1454

## PLAN

1. Fetch and verify the exact PR head, develop base, ancestry, delta, and hosted run.
2. Compare the r3 changes with the r2 stop criterion for teardown failures and marker preservation.
3. Verify whether the adoption failure reaches TestMain as a non-zero exit and whether the injected test actually proves that behavior.
4. Verify the new injected-failure test is selected by hosted PR CI and preserve the exact owner-only workflow routing finding.
5. Publish the delta-only verdict, fix recipe, tests, and stop criterion in this planning evidence file.

## Verdict

**ROLE: REVIEW**  
**VERDICT: KORREKTUR (REQUEST-CHANGES)**  
**PR #1454 head:** `709067e01a7ac62e92486b406d83ed7bda5081db`  
**develop base:** `07ae6c3e91b081a189266ca4b162ba705d4aa78f`  
**Prior review:** `act-1454-review-r2.md`, blocking on fail-closed teardown/adoption, marker retention, and runtime-integration CI routing.

### 1. Package teardown now fails the process, but still deletes the marker after cleanup reports failure

`cmd/baha/runtime_integration_test_support_test.go:102-106` now propagates a package-teardown error into the named `code`, so `TestMain` exits non-zero after a teardown error. However, `destroyBootstrapTrustPlane` at `:352-367` removes the marker after any destroy error except errors classified as “unbeginning” at `:361-363`. A destroy that ran but found residual resources therefore returns an error, makes the package exit non-zero, and still removes the marker. The r2 recipe required removing the marker only after destruction succeeds; r3's own comments and test at `runtime_integration_cleanup_coverage_test.go:915-917` explicitly treat a failed-but-run teardown as marker-consuming. This does not meet the r2 stop criterion that the marker never be lost after unsuccessful cleanup.

**Fix recipe:** In `cmd/baha/runtime_integration_test_support_test.go`, retain the marker on every non-nil cleanup result, including a destroy that ran but reported residuals. Return the cleanup error without reaching `os.Remove(marker)`; consume the marker only after the destroy and residual watcher both establish success. Keep the TestMain non-zero exit behavior. Add a regression where the destroy runs and reports a residual, then assert both a non-zero subprocess exit and that the marker still exists. The stop condition is that no cleanup failure removes the only durable retry claim.

### 2. Orphan adoption does not fail the production TestMain path closed

`runRuntimeIntegrationTestMain` at `cmd/baha/runtime_integration_test_support_test.go:91-92` ignores the result of `adoptBootstrapLeftoverMarkerFromDeadProcess`. The adoption function returns an empty string when orphan destruction fails (`:237-241`), logs the error, and keeps the marker, but the caller proceeds to `setupBootstrapLeftoverMarker` and then `m.Run()`. There is no adoption error propagated into the named TestMain exit code. Thus the marker may remain on disk while the current test invocation reports success; retaining the file alone does not make this invocation fail closed.

The injected regression does not currently prove the claimed TestMain behavior. `TestBootstrapFailedAdoptionSubprocess` at `cmd/baha/runtime_integration_cleanup_coverage_test.go:949-971` calls the adoption helper from the selected test body and then calls `t.Fatalf`; its non-zero status comes from that deliberate test failure, not from TestMain reacting to an adoption error. The production `runRuntimeIntegrationTestMain` path in the child ignores the adoption failure.

**Fix recipe:** Make adoption return an error distinct from “no stale marker” and propagate it from `runRuntimeIntegrationTestMain` before `m.Run()` (set a non-zero exit code and do not proceed to provisioning). Preserve the orphan marker on that path. Rewrite the injected regression to launch the normal TestMain path with a harmless test that would pass if executed; assert the child exits non-zero due to the adoption error, assert the pass-test sentinel was not reached, and assert the marker still exists. The stop condition is a demonstrated non-zero TestMain exit caused by adoption itself, not by `t.Fatalf` in the child test.

### 3. The new marker-preservation assertion is inverted

In `cmd/baha/runtime_integration_cleanup_coverage_test.go:939-940`, the parent regression says it is checking that a failed adoption keeps the marker, but fails unless `os.Stat(marker)` returns `os.ErrNotExist`. That condition requires the marker to be absent, opposite to the contract and opposite to the direct helper-level assertion in `TestBootstrapFailedAdoptionSubprocess` at `:966-968`. As written, the injected regression rejects the correct retained-marker behavior.

**Fix recipe:** Change the parent assertion to fail only when `os.Stat` returns `os.ErrNotExist`, and fail on any other stat error as an inconclusive result. Keep the direct helper test and the production-TestMain subprocess proof. The stop condition is that both tests pass only when a failed adoption leaves the marker present and the TestMain subprocess exits non-zero for that reason.

### 4. CI coverage and owner routing

The new pure-Go injected-failure test is selected by the hosted `PR · Validation · cli-package-tests` job: `scripts/pr-check-runner.py:184-200` invokes `go_package_tests(repository, ['./cmd/baha'], ...)`, and `go_package_tests` runs `go test ./cmd/baha -count=1 -json` at `:116-119`. This is the package-wide PR selector, so the test is CI-covered under the pull-request trigger. Run `42459947615` completed successfully on the exact candidate SHA; `PR · Validation · cli-package-tests` passed in 7m54s and `PR Selected Checks` passed. This green package run does not cure the assertions and TestMain-path gaps above: the subprocess test can be red because its own test body calls `t.Fatalf`, and its parent checks for the marker's absence.

The r2 owner-only blocker remains for the heavyweight runtime-integration suite that consumes the fixture. The exact needed owner change is in `.github/workflows/ci.yml:255-256` (the `validate` job excludes `pull_request`) and `.github/workflows/ci.yml:342-349` (the runtime-integration step has a narrow test pattern that omits these bootstrap lifecycle proofs and is skipped on PRs). The run's `validate` job is skipped. No workflow file was edited, and no rerun or dispatch was triggered.

**Fix recipe:** The Owner must route the runtime-integration fixture through an appropriate PR-triggered job at those exact workflow locations, with skips rejected as evidence. The ordinary injected failure test remains selected by `cli-package-tests`; that does not replace the native/runtime suite for real fixture consumers. Stop until the corrected package regression passes on the exact candidate and the owner-routed runtime integration test actually executes successfully on a required trigger.

## SHA, diff, and hosted run witnesses

- `git ls-remote origin refs/heads/develop refs/heads/work/0427-127-test-bootstrap-leak refs/pull/1454/head` returned `07ae6c3e91b081a189266ca4b162ba705d4aa78f` for develop and `709067e01a7ac62e92486b406d83ed7bda5081db` for both the named candidate branch and PR head.
- `git merge-base --is-ancestor 07ae6c3e91b081a189266ca4b162ba705d4aa78f 709067e01a7ac62e92486b406d83ed7bda5081db` returned exit 0.
- `git log --oneline origin/develop..709067e01a7ac62e92486b406d83ed7bda5081db` contains only the single card chain: the r1 candidate, its drift merge, r2 commits, and r3 commit `709067e0`; no foreign candidate is carried.
- The PR diff against develop changes only `cmd/baha/runtime_integration_cleanup_coverage_test.go` and `cmd/baha/runtime_integration_test_support_test.go`; no product or `.github/**` workflow file is changed by this candidate.
- `gh run view 42459947615 --repo mcpdev80/baseharbor --json headSha,status,conclusion` returned `headSha=709067e01a7ac62e92486b406d83ed7bda5081db`, `status=completed`, `conclusion=success`. `gh pr checks 1454` showed `PR · Validation · cli-package-tests` pass (7m54s) and `PR Selected Checks` pass. The other non-skipped checks were successful. `validate`, Targeted HA Docker/Podman, and native runtime jobs were skipped, so no hosted execution of the heavier runtime-integration suite is evidenced.

## Stop criterion

Do not approve until every cleanup failure preserves the marker and makes TestMain exit non-zero; adoption errors stop the production TestMain path before `m.Run()`; the injected test proves that exit independently of `t.Fatalf`; the inverted marker assertion is fixed; the exact-candidate `cli-package-tests` run succeeds; and the Owner's runtime-integration routing change at `.github/workflows/ci.yml:255-256` and `:342-349` results in an actual passing run of the fixture. No local test, skipped job, or helper-only subprocess test substitutes for these conditions.

## END

END_BLOCKED 0427-127-r3-review — KORREKTUR required; candidate `709067e01a7ac62e92486b406d83ed7bda5081db`.
