# CODEX-REVIEW — PR #1823 / card 0428-277

- Role: `CODEX-REVIEW`
- Verdict: `RC` (request changes; no merge)
- Candidate head: `f072dcb58302c7db2f362b563fe7b3a870d2950f`
- PR run: `45395054488` — completed `SUCCESS`, all required checks green
- PR Selected Checks: success, GitHub Actions integration `15368`
- Card: `0428-277`, failed reveal must not record `AuthorizationResult=allow` with `Outcome=failed`; fail-closed deny or an explicit discrepancy marker is required.

## Review

The production correction is at the shared audit recording path. `recordRevealFailed` in `cmd/baha/secret_operations.go` calls `recordRevealForTarget` with an explicit `deny` override. The shared builder first copies the authenticated decision's `Actor.Subject`, `Actor.Assurance`, and `Actor.Methods`, then applies the override before appending the event. This prevents `Outcome=failed` from being paired with `AuthorizationResult=allow` without dropping actor attribution.

The regression at `cmd/baha/secret_audit_test.go:329-373` seeds an upstream allowed decision and asserts failed outcome, deny result, and preserved `Actor.Subject`. It does not seed or assert `Actor.Assurance` or `Actor.Methods`. Since actor preservation is part of this review's acceptance, the regression does not yet guard the complete behavior: a future change could lose either field while this test stays green.

## Correction recipe

In `cmd/baha/secret_audit_test.go:329-373`, set distinctive non-empty Assurance and Methods values in the seeded `operatorauth.AuthorizationDecision.Actor`, then assert the persisted event preserves Subject, Assurance, and the exact Methods list. Retain the existing assertions for `Outcome=failed` and `AuthorizationResult=deny`. The production implementation may remain unchanged if those assertions pass.

**Stop criterion:** do not approve until the expanded regression passes in terminal-green CI on the final exact head and covers all three actor fields plus fail-closed deny.

## Merge recipe after correction and re-review

1. Re-review the final exact-head diff; require the authorized write-set to remain `cmd/baha/secret_operations.go` and `cmd/baha/secret_audit_test.go`.
2. Verify all required checks on that exact head, including `PR Selected Checks` from integration `15368`.
3. Confirm no unresolved review findings or required review threads.
4. Squash-merge with an expected-head guard for the reviewed SHA. Stop if the head advances or any required check is not terminal-green.

No merge was performed. The candidate diff and test were inspected with `gh pr diff 1823` and `git show f072dcb58302c7db2f362b563fe7b3a870d2950f:cmd/baha/secret_audit_test.go`.
