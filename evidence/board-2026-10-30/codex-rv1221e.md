ROLLE: REVIEW

## PLAN
- ✓ (evidence-note) 0. Read dispatch and binding policies; record plan. Native TodoWrite unavailable.
- ✓ (evidence-note) 1. Refresh exact candidate and inspect base-SHA hardening and regression tests.
- ✓ (evidence-note) 2. Run focused tests and verify exact-head hosted result; record verdict and executor prerequisite.
- ✓ (evidence-note) 3. Record evidence and applicable Planning status without merging.

## ROLLE: REVIEW

Verdict: REQUEST_CHANGES. Exact head 3be6095aaf0c431fc2f75ee37d33c7e30535b53a against develop 72ba7a99ff7dcd4b04ee3cf16516991ef567d376; detached /tmp/review1221e/deep/worktrees/product. HTTPS ls-remote witnessed both refs. Review limited to rv1221d point 2; executor registration (#1225) remains a separate merge-readiness prerequisite.

The guard now rejects nonzero lookup rc, empty/non-hex/short/all-zero values at .github/workflows/receipt-post-run.yml:146-166. However the actual authenticated Actions run response for exact-head run 41074920080 has top-level `base_sha: null`, with its PR association containing `pull_requests[0].base.sha=72ba7a99ff7dcd4b04ee3cf16516991ef567d376`. The workflow reads the absent top-level field at :147 and rejects that real run; tests at scripts/test_receipt_postrun.py:886-887 fabricate a top-level base_sha. The positive synthetic tests therefore do not establish production eligibility. The compare shape guard at workflow :187-203 tests only a leading `[` and does not establish full JSON array type or completeness of the returned file set.

Worker recipe: obtain and validate the run-bound base from actual authenticated producer metadata using the observed API contract, bind it to the unique PR/run head and trusted immutable context, fail closed for missing/ambiguous/invalid inputs, and use a validated complete compare result. Replace synthetic run shape with a sanitized real-shaped fixture (base nested in pull_requests), and test real-shaped positive, rc/null/zero/malformed, non-array, truncation, and head/base drift cases. Run focused tests and exact-head hosted validation; stop if the API cannot establish an immutable base rather than inferring one.

Direct test_receipt_postrun unittest: 45 passed, but synthetic metadata differs from observed API. Exact-head hosted run 41074920080: PR Selected Checks SUCCESS app 15368; selected Python/actionlint/validation jobs succeeded, non-selected skipped. PR remains OPEN; no merge in this mission. Planning task t-20261029-r27-ci-producer was observed under an existing owner; no unverified status change or claim takeover was made.

## repo-rule compliance
Read-only product review; no product changes, approval, protection change or merge. Coordinator reminders remain unresolved.

END rv1221e DONE
