# Independent read-only review — PR #1620 / 0428-067

Reviewed 2026-11-19 against live GitHub metadata and the PR patch.

- Current head `e7eeeb5802a3c2203947655f5adcaa0a6aa9df0d`; base `cli2-env-policy-head` at `5ef9c329b84c52a242b17a9b3d3a63c9d3c314c3`.
- PR is Draft and `statusCheckRollup` is empty. No exact-head CI evidence is available; do not treat the candidate as validated or merge-ready.
- Existing plan evidence for 0428-114 already documents that PR chains based on `cli2-*` are outside the configured `lane-*` base filters, so changing Draft to ready alone will not trigger the required PR checks.

## Finding — audit failure does not block secret reveal

In `cmd/baha/app_access.go`, the `--reveal` branch calls `recordConnectionRevealAudit`; if persistence fails, it prints the error to `errOut` and then unconditionally prints `PASSWORD` and `URI`. This does not satisfy the PR's stated “fail-closed hardening”/accountability intent under an unavailable or unwritable audit store. Either fail the reveal before emitting the secret when the audit write fails, or explicitly revise the security contract and acceptance to best-effort auditing. Add a test that forces the audit append to fail and verifies the intended behavior.

No PR/product files, comments, claims, or merge state were changed by this review.
