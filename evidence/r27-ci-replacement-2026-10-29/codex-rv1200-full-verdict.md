ROLLE: REVIEW
UTC: 2026-10-29 09:52 UTC
Candidate: 114d6e48e0396d4a92a97f4fe4dca9badc4b0a63
Base: 80d0312276aab8829deb80188aa9902ff0183b73 (develop)
Planning main: 2eff5d668e772a42c6eca0f6cfbb1ed4242a5b9f
VERDICT: REQUEST_CHANGES

## PLAN
[✔] 0. Record plan; native TodoWrite is unavailable in this session.
[✔] 1. Refresh candidate and task contract, inspect complete diff and PR body.
[✔] 2. Run focused suites and check self-pin positive and negative paths.
[✔] 3. Verify current CI and map acceptance criteria to evidence.
[✔] 4. Record SHA-specific verdict, findings and actionable recipe.

## Review evidence
Fetched product origin; remote develop and PR branch resolve to the stated base and candidate. Planning SSH fetch failed due to system SSH config permissions; GitHub API independently confirmed origin/main SHA above, matching the locally available task contract. GitHub API confirmed current PR head and develop SHA. Reviewed the entire two-file three-dot diff. The temporary detached candidate worktree was clean before and after the tests; existing unrelated product working-tree changes were untouched.

Acceptance mapping:
1. Approval loads intended trusted source and rejects wrong or absent pins: workflow loads `vars.BASEHARBOR_RECEIPT_TRUSTED_SOURCE`, checks lowercase 40-hex, then calls `pinned_source` which compares actual verifier and workflow blobs. Candidate tests exercise same-commit and unchanged-descendant positive cases, missing, malformed, nonexistent SHA, divergent verifier and divergent workflow negatives. A different SHA with identical relevant blobs is intentionally accepted; comparison is byte equality, not identity. Registration must select a reviewed integrated commit with the candidate bytes. The PR body currently contradicts this requirement (see finding).
2. Shadow static pin/interface correctness: `b53632aaaee6067397c27000c229f34736ec2155` is an ancestor of the base; its shadow workflow blob equals the candidate's shadow blob. The called workflow requires receipt, plan, candidate and publication, all four wired from approval outputs. Hosted execution is explicitly assigned to the separate shadow-run task and was not claimed here.
3. Focused tests and workflow validation: in detached candidate worktree, `cd scripts && python3 -m unittest test_receipt_verifier test_receipt_chain` exited 0. Actual final output: `Ran 122 tests in 10.394s` / `OK`. The run emitted ResourceWarning messages for unclosed fixture files in existing test_receipt_verifier.py lines 1383–1402; no test failed. GitHub Actions run 40848710241 identifies this exact head and completed successfully; CI actionlint, CI policy, focused Python, receipt-execution and verifier tests passed. `PR Selected Checks` passed for exact head with app ID 15368. Several path-selected jobs were skipped; they are not represented as passing.

## Finding and recipe
The live PR #1200 body says both pins are set to b53632aa. That commit has the old approval workflow bytes and therefore cannot serve as TRUSTED_SOURCE for this candidate: `pinned_source` will reject it. The prompt's description of a self-pin claim is also not present in the current PR body. This is operationally material because following the body at registration causes approval to fail closed.

Recipe for the owner: update the PR body to state that the shadow call uses b53632aa, while BASEHARBOR_RECEIPT_TRUSTED_SOURCE must be set at registration to a reviewed final integrated commit containing the exact approval-workflow and verifier bytes. Do not set the variable or activate the workflow as part of this review. Verify the corrected body against the final integrated commit; if product bytes change, rerun affected tests and obtain a new SHA-specific review. Stop if the intended integrated commit does not contain the reviewed bytes or if required CI is not green. The static code acceptance criteria otherwise have the evidence above; the misleading registration instruction remains unresolved.

## Limits
No hosted shadow execution, registration, merge, push or production activation was performed. The system's TodoWrite tool was unavailable. The initial board check reported unknown Codeman session state and pending events/reminders; these were inspected but not acknowledged as resolved because their underlying sessions and outstanding actions could not be verified in this bounded review.
END RV1200FULL

## RV1200FULLB PLAN
[✔] 0. Record plan in evidence; native TodoWrite is unavailable.
[☐] 1. Fetch and verify unchanged PR head.
[☐] 2. Read and hash current PR body; compare with the requested correction.
[☐] 3. Record complete-candidate verdict and remaining findings.
