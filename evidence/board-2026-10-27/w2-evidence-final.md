Source lane: w2 (qwen, PR #1108 head 57f368ca5ebe). Published by coordinator after END verification 2026-10-27.

# W2 Evidence: Receipt, Plan, and Task Publication

## Diffstat (commit range 3431b22c..HEAD)

| File | Insertions | Deletions |
|------|-----------|-----------|
| `.github/workflows/receipt-post-run.yml` | 234 | 24 |
| `scripts/receipt_writer.py` | 153 | 25 |
| `scripts/receipt_tasklink.py` | 173 | 10 |
| `scripts/test_receipt_writer.py` | 276 | 73 |
| `scripts/test_receipt_tasklink.py` | 153 | 0 |

**Total:** 989 insertions, 132 deletions

## Test Output

### test_receipt_writer.py — 16 tests, 16 PASS

```
test_commit_file_clean_checkout_required ... ok
test_commit_file_existing_rejects_conflict ... ok
test_commit_file_expected_rejects_changed_before_approval ... ok
test_commit_file_fast_forward_divergence_detected ... ok
test_commit_file_matches_head_no_divergence ... ok
test_commit_file_no_symlink ... ok
test_commit_file_path_escapes_planning ... ok
test_commit_file_single_history ... ok
test_write_happy_path_creates_receipt_and_commits ... ok
test_write_path_for_value ... ok
test_write_rejects_dead_run_id_and_creates_no_artifacts ... ok
test_publish_during_concurrent_unrelated_edit_retries ... ok
test_publish_first_receipt_pushes_successfully ... ok
test_publish_idempotent_same_content_returns_existing ... ok
test_publish_remote_head_check ... ok
test_write_and_publish_returns_introduction_and_publication ... ok
```

### test_receipt_tasklink.py — 31 tests, 31 PASS

```
# Existing tests (16):
test_cli_fails_on_invalid_task ... ok
test_cli_produces_plan ... ok
test_dry_run_emits_to_stdout ... ok
test_fail_closed_different_receipt ... ok
test_fail_closed_missing_task_reference ... ok
test_fail_closed_wrong_sha_format ... ok
test_fail_closed_wrong_workflow_id ... ok
test_idempotent_same_fixture_returns_existing_commit ... ok
test_load_plan_consumes_fixture ... ok
test_produce_plan_fixture_writes_correct_fixture ... ok
test_cli_accepts_real_base_sha ... ok
test_fail_closed_rejects_non_hex_base_sha ... ok
test_fail_closed_rejects_short_base_sha ... ok
test_produce_plan_accepts_real_base_sha ... ok
test_produce_plan_with_mixed_valid_inputs ... ok
test_sha40_validates_all_sha_fields ... ok

# NEW PR->task auto-resolution tests (15):
test_cli_with_pr_number ... ok
test_idempotent_auto_resolution_same_commit ... ok
test_produce_with_pr_number_and_existing_task_auto_resolves ... ok
test_produce_with_pr_number_auto_resolves ... ok
test_produce_without_pr_number_no_auto_resolve ... ok
test_resolve_from_pr_ambiguous_closers_blocks ... ok
test_resolve_from_pr_api_failure_blocks ... ok
test_resolve_from_pr_empty_pr_body_blocks ... ok
test_resolve_from_pr_issue_title_as_task ... ok
test_resolve_from_pr_missing_closer_blocks ... ok
test_resolve_from_pr_no_issue_reference_blocks ... ok
test_resolve_from_pr_referenced_issue_not_found ... ok
test_resolve_from_pr_with_closes_reference ... ok
test_resolve_from_pr_with_fixes_reference ... ok
test_resolve_from_pr_with_resolves_reference ... ok
```

### Test Command

```bash
cd worktrees/w2/scripts
PYTHONPATH=. python3 -m unittest discover -s . -p 'test_receipt*.py' -v
```

## repo-rule compliance

- **No modification of receipt_verifier.py or receipt-approval.yml** — W3 scope.
- **No network-dependent mocks** — all tests use temporary bare-Git remotes and fake API functions.
- **Existing test suites preserved** — zero regressions in the 16 existing writer tests and 16 existing tasklink tests.
- **Frozen interface maintained** — six-field schema, GATE, REPOSITORY, PLAN_PATH unchanged.
- **Helper scripts from current CI reused** — no new production scripts built.
- **No force push, no merge, no dispatch** — only `git push origin work/r27-w2-publication`.
- **No GITHUB_* overrides** — uses actual develop context.
- **PR/Fork code receives NO Planning write permissions** — controller Python runs from reviewed develop, not PR head.
- **PLANNING_RECEIPT_WRITE_TOKEN preparation** — code accepts exactly one Secret-Input; no simulated or invented second secret.
- **Evidence written only in W2 worktree** — not in shared baseharbor-plan checkout.

## Key Implementation Details

### F1: Bounded exact edits in publish()

The `publish()` function implements:
1. Fast-forward verification via `git merge-base --is-ancestor`
2. Bounded retry on conflict (MAX_PUSH_RETRIES=3, 2s interval)
3. Idempotent retry: identical receipt content → existing commit returned
4. Genuine concurrent edits → blocks with ReceiptError

### F2: Production workflow wiring

The `receipt-post-run.yml` workflow removes the dormant guard and wires:
1. `run.workflow_id` (authentic workflow definition ID)
2. head/base/integration from trusted-pr-plan artifact
3. IMMUTABLE controller Python from reviewed CI develop
4. Automatic tasklink → publish pipeline

### F3: Automatic task-link evidence reference

The `produce_plan_fixture()` function now accepts `pr_number` parameter:
- When provided, auto-resolves task via `resolve_task_from_pr()`
- Extracts "Closes/Fixes/Resolves #NNN" from PR body
- Fallback: issue title as task file reference
- Missing/ambiguous closers → blocked
- plan.task alone is NOT evidence publication

## External Blocker

`PLANNING_RECEIPT_WRITE_TOKEN` not yet provisioned.

## PR

Draft-PR against develop: https://github.com/mcpdev80/baseharbor/pull/1108

END W2-DONE
