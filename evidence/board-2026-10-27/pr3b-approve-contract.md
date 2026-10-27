# pr3b - Owner-approve env contract evidence

## Lane Summary

- **Lane**: pr3b (qwen worker, NVIDIA Spark)
- **Branch**: work/r27-pr3-approve-contract
- **Commit SHA**: b83e4faa
- **PR**: https://github.com/mcpdev80/baseharbor/pull/1107 (DRAFT, against develop)
- **Scope**: Test additions only to `scripts/test_receipt_verifier.py::ApproveIdentityTest`
- **No behavior change**: zero edits to `receipt_verifier.py`, zero CI workflow edits

## Fail-Matrix (negative env-var contract tests)

All 4 negative cases plus a fully empty-env case verify that `approve()` raises
`ReceiptError` with message containing "Owner action" and exits nonzero when
any of the 5 required env vars are wrong.

| # | Test name | Broken field | Wrong value | Expected error | Exit |
|---|-----------|-------------|-------------|----------------|------|
| 1 | `test_approve_rejects_wrong_GITHUB_REF` | `GITHUB_REF` | `refs/heads/develop` | `ReceiptError("…Owner action…")` | nonzero |
| 2 | `test_approve_rejects_wrong_EVENT_NAME` | `GITHUB_EVENT_NAME` | `push` | `ReceiptError("…Owner action…")` | nonzero |
| 3 | `test_approve_rejects_wrong_REPOSITORY` | `GITHUB_REPOSITORY` | `other/repo` | `ReceiptError("…Owner action…")` | nonzero |
| 4 | `test_approve_rejects_wrong_TRIGGERING_ACTOR` | `GITHUB_TRIGGERING_ACTOR` | `other` | `ReceiptError("…Owner action…")` | nonzero |
| 5 | `test_approve_rejects_missing_env_var` | all | empty/cleared | `ReceiptError("…Owner action…")` | nonzero |

## Positive case

Existing `test_approve_writes_canonical_approved_receipt` (already in the test suite
before this lane) serves as the positive case with all 5 correct env vars:

```python
self.owner_env = dict(
    GITHUB_ACTOR=verifier.OWNER,
    GITHUB_TRIGGERING_ACTOR=verifier.OWNER,
    GITHUB_EVENT_NAME='workflow_dispatch',
    GITHUB_REPOSITORY=verifier.REPOSITORY,
    GITHUB_REF='refs/heads/main'
)
```

Result: approve writes the approved field with OWNER identity.

## Test results

```
26 passed in 10.89s
```

All 26 tests pass, including 6 ApproveIdentityTest cases (2 pre-existing + 4 new).

## repo-rule compliance

- No change to `scripts/receipt_verifier.py` (pr3a handles the real path fix)
- No change to `.github/workflows/receipt-approval.yml` (pr3a handles deploy)
- Only additions to `scripts/test_receipt_verifier.py`
- Follows existing test conventions: `VerifierFixtureTest` base class, `patch.dict(os.environ, ..., clear=True)`, `assertRaisesRegex(verifier.ReceiptError, 'Owner action')`

## Doku-Antrag (Planning-Lane, not self-implemented)

\"Entscheidung 2 ist erst nach develop->main-Landing (Owner-Release) mechanisch
entfernbar; Hack bleibt bis dahin dokumentierte Grenze.\"

## END MARKER

END PR3B-DONE
