## PLAN
- ✔ 0. Read codex-rv1204.md review findings.
- ✔ 1. Revert scripts/test_receipt_postrun.py to origin/main version, then add ONLY the smallest additive assertion block for PLANNING_RECEIPT_WRITE_TOKEN.
- ✔ 2. Reduce workflow comment additions to zero - the env line is the only change.
- ✔ 3. Run focused tests: 17 tests (15 pass from origin/main, 2 pre-existing failures from origin/main integration tests that fail against main-side workflow expressions, 1 new focused test PASS). actionlint passes.
- ✔ 4. Forward commit + push: head SHA f2aeafe89b80a61f61f48e44e9c34897973d28a8.

## Fix Round

### Finding 1 - Candidate scope
codex-rv1204 finding 1: The diff was 194 insertions/18 deletions across two files, exceeding the MINIMAL requirement.

**Fix applied:**
- Reverted `scripts/test_receipt_postrun.py` to origin/main version.
- Added ONLY the smallest additive assertion block (`test_publish_step_env_carries_planning_receipt_token`) proving PLANNING_RECEIPT_WRITE_TOKEN present in publish-step env. No shell-fixture expansion.
- Removed all 7 workflow comment lines; the env line `PLANNING_RECEIPT_WRITE_TOKEN: ${{ secrets.PLANNING_RECEIPT_WRITE_TOKEN }}` is now the only functional change in the workflow file.

**Result:**
- Workflow diff: exactly +1 line (`git diff origin/main... -- .github/workflows/receipt-post-run.yml` shows the single env line addition).
- Test file diff: +19 lines, -0 lines (only the new assertion method appended to DownloadInvocationTests).
- Total candidate diff: 19 insertions, 175 deletions (net -156 lines from original).

### Test execution

```
python3 -m unittest test_receipt_postrun test_receipt_chain

.......FF........
======================================================================
FAIL: test_full_run_publishes_plan_and_receipt (F1PositiveRun)
bash: line 10: ${{ github.event.workflow_run.pull_requests[0].number }}: bad substitution
======================================================================
FAIL: test_real_tasklink_block_writes_plan_fixture (F1WorkflowShellEndToEnd)
bash: line 26: GH_WORKFLOW_TOKEN: unbound variable

Ran 17 tests in ~12s
```

The 2 failures are **pre-existing on origin/main** - confirmed by running the same tests against origin/main directly (16 tests, same 2 failures). These are integration tests that execute actual workflow blocks against the main-side workflow, which uses expressions (`pull_requests[0].number`, `GH_WORKFLOW_TOKEN`) not handled by the test fixture. This is a pre-existing gap in the origin/main test suite, not introduced by this fix round.

The new focused test `test_publish_step_env_carries_planning_receipt_token` passes: pure YAML structural assertion, no shell execution.

### Actionlint

```
/home/marcel/dev/go/bin/actionlint receipt-post-run.yml
```

PASS - no errors.

### New head SHA

`f2aeafe89b80a61f61f48e44e9c34897973d28a8`

END q206-C-DONE
