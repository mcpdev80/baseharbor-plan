ROLLE: REVIEW
**Verdict: REQUEST CHANGES**

# PR #1737 — card 0428-213 trust-uninstall EOF

## PLAN

1. Read the mission and record this numbered plan in the live board and review evidence.
2. Verify the exact PR head, current stacked base, merge ref, ancestry, and review freeze.
3. Inspect the test correction and trace it to the production command and EOF behavior.
4. Inspect the exact hosted run, its archive and job logs, and classify each first-level failure by exact message and card.
5. Check write-set exclusions, CI selection, red-first evidence, and the recorded cleanliness witness.
6. Publish only this review file, verify it on baseharbor-plan origin/main, and recheck the PR head.

## Candidate and session

- Card: t-20261121-trust-uninstall-false-green (0428-213).
- PR: mcpdev80/baseharbor#1737, branch lane-0428-213-trust-uninstall-false-green.
- PR head before review: 5be4f003aa1be5ff732e149a1c4a179d3abda047.
- PR head after review: 5be4f003aa1be5ff732e149a1c4a179d3abda047.
- PR is open, non-draft; PR API base SHA is 80dc4987993b6855314c0112ad2c8645c15a4562 and mergeable_state is unstable.
- GitHub remote witnesses:
  - refs/heads/lane-0428-213-trust-uninstall-false-green = refs/pull/1737/head = 5be4f003aa1be5ff732e149a1c4a179d3abda047
  - refs/heads/lane-0428-198-cli-shard-operator-env = e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4
  - refs/pull/1737/merge = 48b7ccdfa2424d8a24a29d967a0c81a80bb2c487
- Candidate commit parent is c2f9f2f32fd6bd27c0c0b4e269ad02fde6d643b5. GitHub compare current base e45430f2f1b7...candidate reports diverged, ahead_by 1, behind_by 3; current base is not an ancestor.
- Run 44867291850 checked synthetic merge 48b7ccdfa2424d8a24a29d967a0c81a80bb2c487, with parents 80dc4987993b6855314c0112ad2c8645c15a4562 and the candidate head. It did not test the candidate atop current base e45430f2f1b7.
- Planning remote first-action witness: origin https://github.com/mcpdev80/baseharbor-plan.git (fetch).
- Session ID is not exposed by this review interface. Model/backend: GPT-6.2, Codex API session. Review time: 2026-11-21 06:02 UTC.

## P1 — real production prompt path and substantive assertions

The PR diff changes only cmd/baha/trust_status_regression_test.go and cmd/baha/trust_uninstall_test.go. The three EOF regressions call trustUninstallCommand().Run directly with the real production command implementation: TestTrustUninstallPromptUnterminatedAffirmativeEOFRejects at trust_uninstall_test.go:138-159, TestTrustUninstallPromptEOFRejects at :164-185, and TestTrustUninstallPromptEOFAbortsCleanly at :224-245. Each now requires nil error, the exact "Host trust unchanged." output, and the ownership record to remain present. The production path authorizes before reading at cmd/baha/trust.go:180, reads the prompt at :203-204, treats io.EOF as a clean cancel at :205-212, and returns non-EOF read errors at :213-214. Thus the checks now observe the prompt's real behavior rather than accepting a helper result.

The trust-status tests were also routed through the same fixture at trust_status_regression_test.go:31-36 and :105-114; their state/output and no-mutation assertions remain enabled.

The cited pre-fix evidence is RED for the unreachable prompt path: at base 7db142852d22 the tests used a bare context and failed on the production auth gate before reaching EOF. However, the lane's explanation of the old test is inaccurate. The old source at that exact base had if err != nil { t.Fatalf(...) } at the three call sites; the gate error made those tests fail, not pass as a false green. The repair still addresses the real reachability defect by satisfying the test authorization precondition and then requiring the EOF-specific output and unchanged ownership state. The description "false green" should be corrected in the round-1 evidence.

## P2 — authority fixture is a positive precondition, not the tested denial

trust_uninstall_test.go:15-29 routes the command through operatorAuthFixtureContext. That fixture stamps a verified operator principal and editor membership at operator_test_fixture_test.go:61-72. WithVerifiedPrincipal itself calls WithEnforcement at internal/operatorauth/context.go:54-57. This is intentional for reaching the prompt after the production boundary at trust.go:180; it does not prove or claim an unauthenticated denial.

The denial test at trust_uninstall_test.go:87-106 is specifically the JSON/no-approval case: it requires approval guidance and verifies the ownership record remains. It is not asserting the operator-auth gate denial. No self-stamped-auth denial finding.

## P3 — exact run and CI inclusion

Run 44867291850 is pull_request, completed/failure, exact branch head 5be4f003aa1be5ff732e149a1c4a179d3abda047. The run archive from the GitHub API was 123,536 bytes and expanded to 505,982 bytes. gh run view ... --log and --log-failed each returned 0 bytes in this environment; I used the run archive and per-job log endpoints instead. Job logs: cli-0 = 23,647 bytes; cli-3 = 22,930 bytes.

The selected gate plan says UNIT_SCOPE=cli, NATIVE_REQUIRED=false, runtime_required=false. All four PR Go unit CLI shards executed: cli-1 and cli-2 succeeded; cli-0 and cli-3 failed. The selected test-name hash in scripts/pr-go-unit-shard.py maps the three EOF tests to cli-0, TestTrustStatusAbsentCoreInsideAndOutsideRepository and TestTrustStatusRetainsOwnedRecordsWithoutCore to cli-3, and TestTrustStatusUnreadableStateNotReportedAbsent to cli-1. The tests are in the actually selected command-package inventory, not a skipped test group. No test from the two changed files appears among the run's first-level FAIL lines.

Native/runtime/HA/release checks marked skipped were not required by the successful trusted gate plan for this CLI-only test diff. The required CLI unit group did not pass, so the exact-head required-check evidence is not green.

## P4 — classify every failing test, do not call them inherited

The combined run archive contains exactly three first-level --- FAIL: Test... lines, and zero occurrences of the exact operator-auth gate text "Managed-environment machine operations require an authenticated BaseHarbor operator":

- cli-0: TestAppListAllTargetsWorksAfterInstallationDestroy, app_list_all_targets_test.go:26 — all-targets inventory depended on deleted Target config "docker-dev": config.yaml is missing. This is the distinct 0428-210 / PR #1739 defect.
- cli-0: TestSecureProfileExportCommandPathAssemblesProductionWiring, secure_profile_export_command_test.go:125 — operator authentication needs interactive setup but input is not a terminal. This maps to 0428-219; the current base lane later added commit e45430f2 ("test(0428-204): authenticate secure export command path"), but the tested merge ref still used old base 80dc.
- cli-3: TestTargetInspectionProjectsBuiltInAccessCapabilities, target_hotfix_test.go:201 — target "edge-a" is not configured. This is the 0428-220 target inspection fixture issue; the PR run's old merge base predates the later base-lane target-registration correction.

None of these has the specified gate text, so none is classified as the inherited operator-auth class. The 0428-210 failure remains the distinct outstanding failure after the later base-lane changes; the other two are explained by the stale PR merge base. No rerun was triggered.

## P5 — write-set and protected paths

gh pr diff --name-only returns exactly:
- cmd/baha/trust_status_regression_test.go
- cmd/baha/trust_uninstall_test.go

No .github/**, internal/operatorauth/**, internal/capability/perses_selection.go, or owner-stack files for #1615/#1625/#1623, #1650/#1606, #1614, #1731, or #1704 are in the diff.

## P6 — cleanliness and recorded test scope

The lane round-1 evidence says it started no container, network, volume, or state directory and records empty docker ps -a output before and after. It also says the ambient shared stack had been removed by a prior lane before its recorded before snapshot; this is evidence that the lane left no test-owned container, not a witness of the earlier ambient state. The product diff is test-only; no generated baha binary is a container. I ran no local tests or containers during this read-only review.

## Required correction and stop criterion

The content correction is directionally valid, but this card cannot be accepted on the reviewed evidence because the terminal required run is failed and tested against stale base 80dc, not current base e454. The older lane evidence also describes the old assertion backwards.

Recipe for the worker/coordinator:
1. Correct evidence/r28-welle4-2026-11-21/trust-uninstall-false-green/round-1.md to say that the old bare-context tests failed at the auth gate before reaching the prompt; remove the claim that the gate error satisfied a passing err != nil shape. Keep the observed red lines as proof of the unreachable prompt.
2. Once the 0428-210 failure is resolved in the base chain, update this candidate to the then-current base lane head. Do not weaken or skip the CLI tests.
3. Obtain a terminal PR Selected Checks run on the candidate's synthetic merge against that current base. Confirm all four required PR · Go unit · cli-* jobs execute and succeed, and the three EOF tests are in the selected cli-0 set. If any EOF test fails, correct cmd/baha/trust_uninstall_test.go and rerun that test through the selected CLI shard.

Stop when the evidence accurately describes the pre-fix behavior, the current base is an ancestor of the candidate, and an exact current-base PR run has all required CLI shards successful with the trust regressions executed. No product change is required by this review if those tests continue to pass.

## END

END_DONE codex-rev-cli2b: review completed; REQUEST CHANGES at PR head 5be4f003aa1be5ff732e149a1c4a179d3abda047.

## Planning publication witness

Command: git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main && git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan ls-tree -r --name-only origin/main | grep '^evidence/r28-welle4-2026-11-21/trust-uninstall-false-green/review-1.md$'

Exact output:
evidence/r28-welle4-2026-11-21/trust-uninstall-false-green/review-1.md
