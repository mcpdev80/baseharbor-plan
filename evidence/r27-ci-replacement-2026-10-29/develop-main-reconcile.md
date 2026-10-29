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

## Korrekturrunde D

Lane: q207
Task: t-20261029-r27-develop-main-reconcile
Date: 2026-10-29
Prompt: q207b.txt
Reviewer: Codex RV1206 (blocking finding: PLANNING_RECEIPT_WRITE_TOKEN removed + test regression)
New head SHA: 089572fcd936e72421d7f86f2b9a9e94d79d1a8c
PR: #1206 https://github.com/mcpdev80/baseharbor/pull/1206
PR state: OPEN, mergeStateStatus: UNSTABLE

### Blocking finding (rv1206)

The first reconcile commit (3dfd98c0) removed the publish-step PLANNING_RECEIPT_WRITE_TOKEN env mapping that develop #1201 added. `scripts/receipt_writer.py:108-110` in `_push_authed` explicitly reads `PLANNING_RECEIPT_WRITE_TOKEN` from os.environ and rejects a real remote push when absent. Planning checkout receiving a secret in an earlier action does not export it to a later step. This reintroduced publication failure. The test was inverted from assertIn to assertNotIn to justify the removal.

### Fix applied

1. Restored publish-step env block with `PLANNING_RECEIPT_WRITE_TOKEN: ${{ secrets.PLANNING_RECEIPT_WRITE_TOKEN }}` and its comment block, EXACTLY as on origin/develop f95b3446, while KEEPING all main hardening already ported (GH_WORKFLOW_TOKEN, attempt, pull_requests fallback, --product forwarding, pins dd8fb61d).
2. Reverted test assertion in scripts/test_receipt_postrun.py: changed assertNotIn back to assertIn for PLANNING_RECEIPT_WRITE_TOKEN, plus restored the exact-expression check against `${{ secrets.PLANNING_RECEIPT_WRITE_TOKEN }}`.

### Two-way reconciliation diff summary

**.github/workflows/receipt-post-run.yml** (diff vs 3dfd98c0):
- Lines 308-315: Added back PLANNING_RECEIPT_WRITE_TOKEN env mapping and 7-line comment block to publish_receipt step env.

**scripts/test_receipt_postrun.py** (diff vs 3dfd98c0):
- test_publish_step_env_carries_write_token: changed assertNotIn to assertIn for PLANNING_RECEIPT_WRITE_TOKEN; restored exact-expression assertion against `${{ secrets.PLANNING_RECEIPT_WRITE_TOKEN }}` and doc/publish lookup.

### Test results

```
cd worktrees/q207/scripts && GOPATH=/tmp/gopath GOCACHE=/tmp/gocache python3 -m unittest test_receipt_postrun test_receipt_chain test_receipt_writer test_receipt_tasklink
```

Result: 73 tests, 0 failures. All pass.

### Combined state after Korrekturrunde D

The reconciled develop-side workflow now carries BOTH develop's token requirement (PLANNING_RECEIPT_WRITE_TOKEN) AND all main hardening (GH_WORKFLOW_TOKEN, attempt/PR fallback, --product forwarding, dd8fb61d pins). No publish-step env is lost.

## END q207-D
