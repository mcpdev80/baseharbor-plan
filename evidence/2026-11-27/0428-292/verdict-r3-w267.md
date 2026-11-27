# PR #1884 / 0428-292 — re-verdict round 3

ROLE=REVIEW
Reviewer: w267-0428-284-pridentity
Decision: PASS for the requested consent-correctness content at the exact candidate head. This is not a green CI qualification or merge authorization; Freeze #136 remains in effect.

## PLAN

1. Refresh PR #1884, exact head, develop base, and both supplied Hosted run IDs.
2. Compare the exact head to develop and inspect the consent binding, lifecycle cleanup, and sequential regressions.
3. Record the run outcomes, including skipped jobs and the terminal aggregate.
4. Stage this read-only verdict; do not edit or merge the product PR.

## Exact candidate

Repository: mcpdev80/baseharbor
PR: #1884, branch lane-0428-292-consent-ux, OPEN, not draft, mergeable reported true.
Exact head: b25c192159f78b2e3ed4d49f0ea587e216f04ace.
Exact develop base: 6944e8761af6f07b801f55e39bb9a5409226c10b.
GitHub compare reports the candidate ahead by five commits and not behind the supplied develop base. The compared write-set is nine files: seven cmd/baha source/test files and scripts/pr-gate-coverage.json. The requested change is the final correction from prior content verdict 4e499b3cf67ad86cb022640589dba05bfa26922d to b25c192159f78b2e3ed4d49f0ea587e216f04ace.

Prior published correction evidence: https://github.com/mcpdev80/baseharbor-plan/blob/2f40ca1630f5919ec7c129a038ff6e2185130966/evidence/2026-11-27/0428-292/korrektur-1884-fix.md. The newly mentioned local w401 staging file was not present at review time; the exact candidate diff and hosted run records were inspected directly.

## Recipe review

- Consume-on-read: PASS. At cmd/baha/app_candidate_consent_interactive.go:49-60, the binding is set to nil before identity comparison; a matching identity returns its digest once, and a mismatch returns no digest after retiring the entry.
- Clear on mismatch: PASS. The same lines 56-59 clear before checking application/target identity. The regression at cmd/baha/app_candidate_consent_test.go:811-824 verifies a mismatched identity yields no digest and leaves none for the original identity.
- Explicit flag cannot leave a stale interactive binding: PASS. cmd/baha/app_candidate_consent_interactive.go:82-93 consumes and clears pending binding before returning the explicit digest. The regression at app_candidate_consent_test.go:787-809 checks no binding remains and a following refusal fails closed.
- Unconditional lifecycle cleanup, including success: PASS by source inspection. runApplicationApplyLifecycle clears at entry and defers clearing on every return at cmd/baha/app_apply.go:139-146. Its successful return is at lines 275-278, so the defer executes on success as well as error. The outer entry path also clears/defer-clears at app_apply.go:114-123, and the remote path does so at app_remote_lifecycle.go:83-90. The regression at app_candidate_consent_test.go:835-871 checks entry and exit cleanup. It does not assert that this test invocation reaches the success return; the unconditional defer itself is direct evidence of success-path cleanup.
- Second invocation requires a fresh prompt: PASS in the added regression at app_candidate_consent_test.go:751-785. It binds an affirmative answer for candidate A, then invokes the prompt again with EOF for the same candidate and asserts that the write fails with errConsentRequiredForCandidateSubmission rather than reusing the earlier answer.

The implementation retains source digest revalidation and constant-time digest comparison as described by the preceding correction evidence; no change in this re-verdict weakens that boundary.

## Hosted evidence and qualification state

Run 46051642251 and run 46051804829 are two distinct terminal pull_request runs on exact head b25c192159f78b2e3ed4d49f0ea587e216f04ace and branch lane-0428-292-consent-ux.

Both runs are FAILURE, not success. In each, Workflow policy, PR · Source format, and PR · Native gate plan succeeded; PR · Trusted Plan failed because the trusted base/controller catalog does not contain runtime owners for four changed source files (including app_candidate_consent_interactive.go, app_candidate_consent_test.go, app_remote_lifecycle.go, and core_installation.go). The logged ValueError requests coverage entries for those files. This is the class-A catalog/freeze blocker reported by the lane.

The jobs requiring downstream execution, including PR · Go unit shards and native runtime jobs, are SKIPPED. PR Selected Checks is FAILURE; its selected Go shard coverage check rejects empty UNIT_SCOPE with UNIT_RESULT=skipped and “REJECT: Go test selection missing or invalid”. Therefore the statement “only Trusted Plan is red and the rest are green” is not literally accurate: the final aggregate is red and the test/runtime jobs are skipped, not green. The empty UNIT_SCOPE is downstream of the Trusted Plan abort, not evidence that the new tests fail or that they ran.

No local tests were run. No PR mutation or merge was performed.

## Final disposition

Content verdict: PASS for the requested singleton-consent correction. The candidate may be reported as content-review complete and ready for the owner’s freeze-lift decision. It is not CI-qualified or merge-ready yet: after the class-A catalog prerequisite is lifted, require the applicable exact-head Hosted checks to execute and the terminal PR Selected Checks aggregate to succeed. Merge remains prohibited until Freeze #136 is lifted.

END_DONE w267-0428-284-pridentity: #1884 content PASS at b25c192159f78b2e3ed4d49f0ea587e216f04ace; both supplied PR runs terminal failure from Trusted Plan and downstream skipped coverage; no merge.
