## PLAN
0. Read dispatch prompt q207.txt; read codex-rv1205.md fully; record plan.
1. Create worktree work/r27-develop-main-reconcile from origin/develop.
2. Compute git diff origin/develop..origin/main for affected files.
3. Apply main-only hardening lines onto develop version, preserving develop content.
4. Update focused tests; run test_receipt_postrun test_receipt_chain test_receipt_writer.
5. One coherent commit; push origin work/r27-develop-main-reconcile; gh pr create --base develop.
6. Report head SHA + PR number; write this evidence file; END q207-DONE.

## Evidence: develop-main-reconcile

Lane: q207
Task: t-20261029-r27-ci-replacement
Date: 2026-10-29
Commit SHA: 3dfd98c0d1ee2241beefdba7b74ac230f38062b1
PR: #1206 https://github.com/mcpdev80/baseharbor/pull/1206
PR state: OPEN, mergeStateStatus: UNSTABLE

### Root cause binding

Per codex-rv1205 finding 1: develop lacks main's CI hardening.
Direct main-to-develop diff showed:
- receipt-post-run.yml removes main's GH_WORKFLOW_TOKEN, authenticated attempt/identity forwarding, pull_requests[0].number fallback
- scripts/receipt_writer.py removes --product CLI support and forwarding

Both are main-only hardening improvements that must NOT be lost on promotion.

### Delta computation

```
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor diff origin/develop origin/main -- .github/workflows/receipt-post-run.yml
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor diff origin/develop origin/main -- scripts/receipt_writer.py
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor diff origin/develop origin/main -- scripts/receipt_tasklink.py
```

Only receipt-post-run.yml and receipt_writer.py had meaningful deltas.
receipt_tasklink.py had no delta between main and develop.

### Conscious merge decisions (file:line table)

**.github/workflows/receipt-post-run.yml:**
- Line 130: Added `GH_WORKFLOW_TOKEN: ${{ secrets.GITHUB_TOKEN }}` to extract_plan plan step env. (main-only: hardening)
- Line 140-141: Changed PR_NUMBER from `""` to `${{ github.event.workflow_run.pull_requests[0].number }}` + `${PR_NUMBER:-}` fallback. (main-only: identity hardening)
- Line 153-154: Added `export GH_TOKEN="${GH_WORKFLOW_TOKEN}"` and `ATTEMPT_RESOLVED="$(gh api ...)"`. (main-only: authenticated attempt)
- Line 163-165: Added `attempt=int(os.environ.get("RUN_ATTEMPT", "1"))` to rv.extract_facts call. (main-only: attempt binding)
- Line 255: Added `GH_WORKFLOW_TOKEN: ${{ secrets.GITHUB_TOKEN }}` to plan_commit step env. (main-only: hardening)
- Line 277: Changed `python3 scripts/receipt_tasklink.py` to `GITHUB_TOKEN="${GH_WORKFLOW_TOKEN}" python3 scripts/receipt_tasklink.py`. (main-only: token forwarding)
- Line 305: Removed PLANNING_RECEIPT_WRITE_TOKEN from publish step env (7 lines of comments + var). (main-only: token no longer step-env exposed)

**scripts/receipt_writer.py:**
- Line 350: `write_and_publish` signature gains `product=None`. (main-only: product param)
- Line 357: `write()` call passes `product=product`. (main-only: wire through)
- Line 369-370: CLI adds `--product` argument. (main-only: argparse)
- Line 382: `write_and_publish()` call passes `product=args.product`. (main-only: wire through)
- Line 386-387: `write()` call passes `product=args.product`. (main-only: wire through)

**scripts/test_receipt_postrun.py:**
- GH_EXPR dict: added `pull_requests[0].number` and `secrets.GITHUB_TOKEN` mappings.
- test_publish_step_env_carries_write_token: changed assertion to expect PLANNING_RECEIPT_WRITE_TOKEN NOT present.
- F1PositiveRun.setUp: added `self.bin` + `self._write_gh_stub()` for controlled gh stub.
- test_full_run_publishes_plan_and_receipt: added GH_WORKFLOW_TOKEN env, bin to PATH.
- F1WorkflowShellEndToEnd.test_real_tasklink_block_writes_plan_fixture: added GH_WORKFLOW_TOKEN env.
- FAKE_GH_STUB: added `actions/runs/` path handler for `--jq .run_attempt`.

### Test results

```
cd worktrees/q207/scripts && python3 -m unittest test_receipt_postrun test_receipt_chain test_receipt_writer
```

Result: 43 tests, 0 failures. All pass.

### Repo-rule compliance

- Focused changes only: receipt-post-run.yml, receipt_writer.py, test_receipt_postrun.py.
- No PR #1205 touched. No merges, no rulesets, no variables.
- No git in baseharbor-plan.
- Commit is coherent, one change set.
- Branch pushed to origin; PR opened base=develop.

## END q207-DONE
