ROLLE: REVIEW

## PLAN
- [x] 0. Read dispatch and binding policies; record plan. Native TodoWrite unavailable.
- [x] 1. Refresh exact candidate and inspect run-bound PR base, API-shaped fixtures and negative cases.
- [x] 2. Run focused tests and verify exact-head hosted status; record verdict and executor prerequisite.
- [x] 3. Publish the evidence and applicable Planning status safely, without merging.

## ROLLE: REVIEW

Verdict: REQUEST_CHANGES. Exact head 91009d0b5c22d07b2f93d9a96bc5efd497df184b against develop 72ba7a99ff7dcd4b04ee3cf16516991ef567d376; detached /tmp/review1221f/deep/worktrees/product. HTTPS ls-remote witnessed both. Review limited to rv1221e finding; #1225 executor registration remains a separate merge-readiness prerequisite.

The top-level-null API mismatch is avoided, but the requested run-bound base and drift negative are not met. .github/workflows/receipt-post-run.yml:104-117 receives the completed run's pull_requests array, yet :143 reads `.base.sha` from the current live `pulls/$PR` object instead of the run's associated `pull_requests[0].base.sha`. These can diverge after base movement without a head change; the resulting compare can classify the wrong diff. test_receipt_postrun.py:1346-1363 calls its case drift-fails-closed but asserts success and eligibility for differing synthetic bases, while its run fixture does not put the base in the PR association. Real authenticated run 41082880747 exposes the association base 72ba7a99ff7dcd4b04ee3cf16516991ef567d376 and head 91009d0b5c22d07b2f93d9a96bc5efd497df184b; no top-level base_sha is needed.

Worker recipe: extract and validate the unique run association's base.sha and head.sha, compare against any live PR object used and fail closed on base or head drift, malformed/missing/ambiguous associations, or incomplete compare. Construct fixtures in the observed API shape and make an actual differing run-base/live-base case assert failure, alongside positive and null/empty negatives. Preserve the separate #1225 prerequisite; stop until independent exact-head review and mandatory CI pass.

Direct test_receipt_postrun unittest: 48 passed, but drift test asserts success rather than the requested negative. Hosted exact-head run 41082880747: PR Selected Checks SUCCESS app 15368, selected Python/actionlint/validation jobs succeeded; non-selected skipped. PR remains OPEN. Planning task t-20261029-r27-ci-producer was observed closed/accepted under q202 and no task tag was changed on the basis of this separate PR review. No merge attempted.

## repo-rule compliance
Read-only product review; no product changes, approval or protection change. Coordinator reminders remain unresolved.

END rv1221f DONE
