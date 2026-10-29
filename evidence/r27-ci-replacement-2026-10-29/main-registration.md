## PLAN
- ✔ 0. Read codex-rv1201.md "Coordinator follow-up recipe" steps 1-3 and main-fwd-port.md.
- ✔ 1. Create isolated worktree from origin/main (worktree: /home/marcel/dev/baseharbor-ecosystem/worktrees/q206, branch: work/r27-postrun-main-reg).
- ✔ 2. Verify current main state: read receipt-post-run.yml at origin/main (dd8fb61d controller pins, GH_WORKFLOW_TOKEN wiring, attempt forwarding).
- ✔ 3. Add PLANNING_RECEIPT_WRITE_TOKEN env mapping to the publish_receipt step env block, preserving ALL main-specific specifics.
- ✔ 4. Extend focused tests: added test_publish_step_env_carries_planning_receipt, updated GH_EXPR for main-specific expressions, added env block processing to _extract_run_block, extended FAKE_GH_STUB with --jq support and /actions/runs/ path.
- ✔ 5. Run focused tests: 17 tests pass OK.
- ✔ 6. Run actionlint on the changed workflow: passes with no errors.
- ✔ 7. Verify git diff shows ONLY added env lines (plus focused test additions).
- ✔ 8. Push branch and open PR #1204 against main (head SHA 3fc45250).
- ✔ 9. Check CI: Workflow policy passes; all other checks skip (expected for CI-only PRs).

## Evidence — q206 lane

Lane: q206
Task: t-20261029-r27-postrun-token-mapping
Supports: r27 main-registration default-main candidate

### Step 1 — Workflow change

Added to the publish_receipt step env block (lines 308-315 of modified workflow):

```yaml
          # The controller requires this token from the environment and fails
          # closed when it is absent (receipt_writer.py:108-110). The Planning
          # checkout step above already sources the same secret; the writer's
          # push auth path reads it from os.environ, so the step env must carry
          # it. The value is never echoed: _push_authed passes it via an
          # ephemeral http.extraheader and _scrub_secret redacts any bearer
          # diagnostic, so publication cannot leak the token.
          PLANNING_RECEIPT_WRITE_TOKEN: ${{ secrets.PLANNING_RECEIPT_WRITE_TOKEN }}
```

This preserves all main-specific specifics:
- dd8fb61d controller checkout pins (unchanged)
- GH_WORKFLOW_TOKEN / GH_TOKEN wiring (unchanged)
- Authenticated attempt forwarding (line 154: `gh api ... --jq .run_attempt`)
- PR-number resolution from `pull_requests[0].number` (line 142)

### Step 2 — Focused test changes

**scripts/test_receipt_postrun.py** changes:
1. Added `"${{ secrets.GITHUB_TOKEN }}": "fixture-token"` to GH_EXPR
2. Added `"${{ github.event.workflow_run.pull_requests[0].number }}": "1124"` to GH_EXPR
3. Extended `_extract_run_block` to process env block values and export them as shell assignments
4. Added `_gh_stub_path` helper to F1PositiveRun for gh stub on PATH
5. Updated F1PositiveRun test env to include gh stub PATH and GH_WORKFLOW_TOKEN env var
6. Updated F1WorkflowShellEndToEnd to use `_build_block_with_env` with extra_env overrides
7. Extended FAKE_GH_STUB with --jq filter support and /actions/runs/ path handling
8. Added `_get_step_env_for_role` and `_build_block_with_env` helper functions
9. Added `test_publish_step_env_carries_planning_receipt` test asserting PLANNING_RECEIPT_WRITE_TOKEN in publish step env

### Step 3 — Test results

```
.......tasklink: no PR number; task is caller-supplied without auto-resolution — plan.task alone is NOT evidence publication
..........

Ran 17 tests in 2.590s

OK
```

All 17 tests pass OK.

### Step 4 — Actionlint

```
/home/marcel/dev/baseharbor-ecosystem/worktrees/q206/.github/workflows/receipt-post-run.yml
```

Actionlint passes with no errors.

### Step 5 — Git diff

`git diff origin/main -- .github/workflows/receipt-post-run.yml` shows ONLY the added env lines (8 new lines including comment block).

### Step 6 — PR details

- **PR #1204**: https://github.com/mcpdev80/baseharbor/pull/1204
- **Base**: main
- **Head**: work/r27-postrun-main-reg
- **Head SHA**: `3fc45250b1210dd05e3853491d0ea5198519598b`
- **State**: OPEN
- **CI**: Workflow policy PASS; all other checks SKIP (expected for CI-only workflow change)

### Step 7 — Registration mechanism

Per codex-rv1201.md step 3 of the coordinator follow-up recipe, the separately authorized registration action remains to be performed. This PR is the candidate that, once approved and merged, registers the publish-step env mapping on default main.

The develop-side forward-port (PR #1202, merged f95b3446) already provides the same env mapping on develop with bumped controller pins. The main-side candidate (PR #1204) adds the same env mapping to main's existing workflow while preserving its dd8fb61d pins and all main-specific authentication fixes.

### Blockers

None.

END q206-DONE
