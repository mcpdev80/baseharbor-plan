# W2 Evidence: Receipt, Plan, and Task Publication

## Summary

W2 implements the automatic receipt publication pipeline for the BaseHarbor CI replacement system. The implementation covers:

1. **receipt_writer.py** — Public publication interface with bounded exact edits, fast-forward push, conflict handling, and idempotent retry.
2. **receipt_tasklink.py** — Automatic task-link evidence reference with PR->task binding resolution.
3. **receipt-post-run.yml** — Production workflow wiring that removes the dormant guard and wires the actual controller invocation.

## repo-rule compliance

- No network-dependent mocks; all tests use temporary bare-Git remotes.
- No modification of `receipt_verifier.py` or `receipt-approval.yml` (W3 scope).
- Existing test suites preserved; no regression.
- Frozen interface maintained: six-field schema, GATE, REPOSITORY, PLAN_PATH.
- Helper scripts from current CI reused; no new production scripts built.

## Test Results

### test_receipt_writer.py — 16 tests, 16 PASS

| Test | Status |
|------|--------|
| `test_write_happy_path_creates_receipt_and_commits` | PASS |
| `test_write_rejects_dead_run_id_and_creates_no_artifacts` | PASS |
| `test_write_path_for_value` | PASS |
| `test_commit_file_fast_forward_divergence_detected` | PASS |
| `test_commit_file_matches_head_no_divergence` | PASS |
| `test_commit_file_clean_checkout_required` | PASS |
| `test_commit_file_no_symlink` | PASS |
| `test_commit_file_path_escapes_planning` | PASS |
| `test_commit_file_existing_rejects_conflict` | PASS |
| `test_commit_file_expected_rejects_changed_before_approval` | PASS |
| `test_commit_file_single_history` | PASS |
| `test_publish_first_receipt_pushes_successfully` | PASS |
| `test_publish_during_concurrent_unrelated_edit_retries` | PASS |
| `test_publish_idempotent_same_content_returns_existing` | PASS |
| `test_publish_remote_head_check` | PASS |
| `test_write_and_publish_returns_introduction_and_publication` | PASS |

### test_receipt_tasklink.py — 16 tests, 16 PASS

| Test | Status |
|------|--------|
| `test_produce_plan_fixture_writes_correct_fixture` | PASS |
| `test_load_plan_consumes_fixture` | PASS |
| `test_fail_closed_missing_task_reference` | PASS |
| `test_fail_closed_wrong_sha_format` | PASS |
| `test_fail_closed_wrong_workflow_id` | PASS |
| `test_idempotent_same_fixture_returns_existing_commit` | PASS |
| `test_fail_closed_different_receipt` | PASS |
| `test_dry_run_emits_to_stdout` | PASS |
| `test_cli_produces_plan` | PASS |
| `test_cli_fails_on_invalid_task` | PASS |
| `test_produce_plan_accepts_real_base_sha` | PASS |
| `test_cli_accepts_real_base_sha` | PASS |
| `test_fail_closed_rejects_non_hex_base_sha` | PASS |
| `test_fail_closed_rejects_short_base_sha` | PASS |
| `test_sha40_validates_all_sha_fields` | PASS |
| `test_produce_plan_with_mixed_valid_inputs` | PASS |

### Test Command

```bash
cd worktrees/w2/scripts && PYTHONPATH=. python3 -m unittest discover -s . -p 'test_receipt*.py' -v
```

## Key Design Decisions

### F1: Bounded exact edits in publish()

The `publish()` function implements:

1. **Fast-forward verification**: Before pushing, verifies the remote is an ancestor of the local commit using `git merge-base --is-ancestor`.
2. **Bounded retry on conflict**: If the push is rejected (non-fast-forward), re-reads the remote state and checks if the receipt content is identical. If identical, returns the existing commit (idempotent). If different, blocks.
3. **Idempotent retry**: Two calls with the same receipt content produce the same commit — no second commit created.
4. **Receipt conflict blocks**: Genuine concurrent edits (different receipt content) cause publish to raise ReceiptError.

### F2: Production workflow wiring

The `receipt-post-run.yml` workflow:

1. Removes the dormant guard (`github.repository == 'mcpdev80/receipt-post-run-dormant'`).
2. Uses `run.workflow_id` (the workflow definition ID) instead of `run.id` (the workflow run ID).
3. Extracts `head_sha`, `candidate_sha`, `base_sha` from the producer's `trusted-pr-plan` artifact — NOT from `workflow_run.head_sha` or branch-name fallback.
4. Checks out the IMMUTABLE controller Python from the reviewed CI repo (`develop`), NEVER the PR head.
5. Uses a separate `PLANNING_RECEIPT_WRITE_TOKEN` for Planning write access.

### F3: Automatic task-link evidence reference

The `produce_plan_fixture()` function:

1. When `pr_number` is provided, auto-resolves the task from the PR body using `Closes/Fixes/Resolves #NNN` pattern matching.
2. Validates the referenced issue points to a valid Planning task.
3. Missing PR number → task is caller-supplied but NOT auto-linked (plan.task alone is NOT evidence publication).
4. Ambiguous PR->task binding (multiple "Closes #NNN" references) → blocks.

## External Blocker

`PLANNING_RECEIPT_WRITE_TOKEN` is not yet provisioned. The code is prepared to accept exactly one secret input. No simulated token or second secret invented.

## PR

Draft-PR against develop: https://github.com/mcpdev80/baseharbor/pull/1108

## W2-DONE
