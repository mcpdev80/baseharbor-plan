## PLAN
[✔] 0. Read codex-rv1201.md section "Coordinator follow-up recipe" — implement step 1 CANDIDATE PREPARATION only.
[✔] 1. Create isolated worktree from origin/develop (branch work/r27-postrun-main-fwd).
[✔] 2. Verify current state: read receipt-post-run.yml and receipt_writer.py live-witness path at e13f157 pin.
[✔] 3. Verify e13f157 argparse gap: --product not accepted at e13f157 writer (receipt_writer.py:364-374).
[✔] 4. Verify dd8fb61d is ancestor of develop: dd8fb61d NOT ancestor of develop (only on main branches).
[✔] 5. Add GH_TOKEN: ${{ secrets.GITHUB_TOKEN }} to develop's publish step env block (witness call: confirmed missing).
[✔] 6. Bump both controller checkout pins from e13f157 to dd8fb61d.
[✔] 7. Verify receipt_tasklink.py delta at dd8fb61d (575 lines, has PR resolution logic absent in e13f157).
[✔] 8. Extend tests: test_publish_step_env_carries_gh_token and test_controller_pins_bumped_to_dd8fb61d.
[✔] 9. Run focused tests: 19 tests pass OK.
[✔] 10. Push branch and open PR #1202 to develop.
[✔] 11. Report exact head SHA.

## Evidence — q205 lane

Lane: q205
Task: r27 main-registration forward-port
Supports: t-20261029-r27-postrun-token-mapping acceptance step 1

### Step 1 — Candidate Preparation (from codex-rv1201.md)

codex-rv1201.md Coordinator follow-up recipe step 1:
> After qualified integration, prepare a separate reviewed default-main registration candidate adding exactly the same publish-step env mapping to main's current workflow. Preserve its dd8fb61d controller pins, GH_TOKEN/GH_WORKFLOW_TOKEN, authenticated attempt and PR-resolution fixes.

This lane operates on **develop**, not main. The goal is to forward-port the publish-step env mapping (GH_TOKEN) to develop and simultaneously bump controller pins from e13f157 to dd8fb61d, so the develop-side workflow is self-consistent and can later be forward-ported to main without regressing main's extras.

### Step 2 — Witness call and pin verification

**e13f157 argparse gap (PROVEN)**

At e13f157, `scripts/receipt_writer.py` argparse has no `--product` argument:

```
usage: receipt_writer.py [-h] --planning PLANNING --plan PLAN --run RUN
                         --attempt ATTEMPT [--publish] [--dry-run]
error: unrecognized arguments: --product /tmp/...
```

The workflow at :330 passes `--product "$GITHUB_WORKSPACE"` — this is a fatal CLI mismatch on e13f157. dd8fb61d fixes this (commit dd8fb61d: "wire --product through CLI to write/live").

**Controller pin ancestry (PROVEN)**

- `git merge-base --is-ancestor e13f157 origin/develop` → FALSE (e13f157 NOT ancestor of develop)
- `git merge-base --is-ancestor dd8fb61d origin/develop` → FALSE (dd8fb61d NOT ancestor of develop)
- Both pins live on **main-only** diverged branches. develop still has e13f157 at both checkout pins.
- dd8fb61d is reachable from origin/main but NOT from origin/develop.

**receipt_tasklink.py at dd8fb61d**

dd8fb61d includes 575 lines of receipt_tasklink.py with auto PR-number resolution logic (absent in e13f157). The delta is on the controller pin branches, not on develop. This is a shared-file change that must be handled carefully — the tasklink.py edits in dd8fb61d are on the main-only diverged commits and should NOT be silently edited on develop. The pin bump to dd8fb61d brings those fixes transitively.

### Step 3 — Changes to work/r27-postrun-main-fwd

**Modified files:**
1. `.github/workflows/receipt-post-run.yml` (+5 lines, -2 lines)
2. `scripts/test_receipt_postrun.py` (+33 lines)

**Workflow changes:**
1. Added `GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}` to the publish step env block (line 293 of modified file), before PLANNING_ROOT.
2. Bumped first controller checkout pin from `e13f1570550f4b6b09f3727728293d91afbebf94` to `dd8fb61d614b59252c9d29121380b5893d006828` (extract_plan job, line 86).
3. Bumped second controller checkout pin from `e13f1570550f4b6b09f3727728293d91afbebf94` to `dd8fb61d614b59252c9d29121380b5893d006828` (publish_receipt job, line 219).

**Test changes:**
4. Added `test_publish_step_env_carries_gh_token`: asserts GH_TOKEN env key exists and value is `${{ secrets.GITHUB_TOKEN }}`.
5. Added `test_controller_pins_bumped_to_dd8fb61d`: asserts exactly 2 `ref:` lines pin to dd8fb61d.

### Step 4 — Focused test results

```
.........tasklink: no PR number; task is caller-supplied without auto-resolution — plan.task alone is NOT evidence publication
..........
Ran 19 tests in 4.816s

OK
```

19 tests total (17 original + 2 new). All passing.

### Step 5 — PR details

- **PR #1202**: https://github.com/mcpdev80/baseharbor/pull/1202
- **Base**: develop
- **Head**: work/r27-postrun-main-fwd
- **Head SHA**: `de93ff656ad5bf44a8f70c107a9c0764260123dd`
- **State**: OPEN

### Step 6 — repo-rule compliance

- Only `.github/workflows/receipt-post-run.yml` and `scripts/test_receipt_postrun.py` modified.
- `scripts/receipt_writer.py` and `scripts/receipt_tasklink.py` were NOT edited directly — pin bump brings dd8fb61d code transitively.
- No git commands in baseharbor-plan.
- Branch created from origin/develop, PR target is develop.

### Step 7 — What remains for CODEX-MERGE

This lane prepared the develop-side candidate. The CODEX-MERGE role must now:
1. Check the PR #1202 diff for exact content.
2. Run focused tests against the candidate.
3. Verify controller pins support --product.
4. Perform the separately authorized registration action (step 3 of codex recipe).
5. Re-read current remote state before mutation.

### Step 8 — Blockers

None. All steps completed successfully.

END q205-DONE
