# i2 Staging Evidence — V2 Partial Integration (task r27)

**Lane:** i2 (ornith)  ·  **Branch:** `work/r27-correction-v2`  ·  **Worktree:** `baseharbor/worktrees/i2`
**Merge HEAD:** `38771771e30c0326bf5e1f814554a37bd25a6439`
**Purpose:** one branch holding #1112 (pushswallow `659734e0`) + #1114 (tasklink `9e90227c`); ci1 fix layered later by Coordinator.

## PLAN

1. Fetch, verify merge-source SHAs against origin.
2. Create worktree `../worktrees/i2` on branch `work/r27-correction-v2` off `ad4d0f28`.
3. Ordinary (non-fast-forward) merge of `659734e0` then `9e90227c`, resolving conflicts only in the 5 allowed files.
4. Run `scripts/test_receipt*` + `unittest discover` counts.
5. Read-only actionlint on receipt workflows (ci1-owned — no fix).
6. Write this evidence; push `work/r27-correction-v2`.

## Merge History

```
*   38771771 merge: integrate r27-fix-pushswallow + r27-fix-tasklink-autoresolve (V2 staging)
|\
| * 9e90227c fix: post-run tasklink auto-resolve from PR (BF-W3-2)      #1114
* | 659734e0 fix(f1): END line=abc36c9c FINAL                          #1112
* | abc36c9c ... (base ancestor chain at ad4d0f28)
Merge: 659734e0 9e90227c
```

- First merge of `659734e0`: fast-forward from `ad4d0f28` (3 files: `evidence-r27/f1-fix.md`, `scripts/receipt_writer.py`, `scripts/test_receipt_writer.py`).
- Second merge of `9e90227c`: ordinary merge, 3 conflict regions (2 in `scripts/`, 1 in `.github/workflows/`), all resolved in allowed set.
- Verified `659734e0` and `9e90227c` are both ancestors of HEAD (`git merge-base --is-ancestor`).
- No ci1-territory file (`ci.yml`, `pr-gate-plan.py`, `pr-check-runner.py`, `ci-workflow-policy.sh`, actionlint-ymls, planner-tests) was edited by the resolution.

## Conflict List

| File | Allowed? | Resolution |
|------|----------|-----------|
| `scripts/receipt_tasklink.py` | YES (receipt scope) | Auto-merger left markers; both branches implement `resolve_task_from_pr`. Took the `9e90227c` (tasklink) side — canonical #1114 fix, `%`-formatting + 4-space indent matching original file style. |
| `scripts/test_receipt_tasklink.py` | YES (receipt scope) | Took the `9e90227c` side; no leftover markers. |
| `.github/workflows/receipt-post-run.yml` | YES (explicitly listed) | Semantic conflict: HEAD side = full 248-line active PR2 production wiring; `9e90227c` side = 80-line DORMANT stub (tag-trigger commented, never-true guard). Took HEAD side (more complete, active). Result byte-identical to base `ad4d0f28`. |

### Conflicts touching ci1 territory
None resolved here. The auto-merger resolved all ci1 files (`ci.yml`, `pr-check-runner.py`, `pr-gate-plan.py`, `receipt-approval.yml`, `receipt-shadow.yml`, `receipt_verifier.py`, `test_receipt_verifier.py`, `test_receipt_chain.py`, `test_pr_*`) cleanly. Integration of this staging branch onto ci1 remains with the Coordinator.

## Test Count

Per-suite (run from `scripts/`, as tests import modules directly):
- `test_receipt_writer`: **17 tests** — OK
- `test_receipt_tasklink`: **30 tests** — OK
- `test_receipt_chain`: **6 tests** — OK

`python3 -m unittest discover -p 'test_receipt*.py'`: **120 tests**, **2 failures** (pre-existing, see below).

### The 2 failures are pre-existing, not introduced by this merge
`test_approve_cli_full_chain_fails_closed_on_missing_publish` and `test_missing_publish_interface_blocks_publication` (both in `test_receipt_verifier.py`) fail identically on base commit `ad4d0f28`:
- `test_receipt_verifier.py` is **not** in the allowed conflict-resolution set.
- Base `ad4d0f28` run: `Ran 120 tests ... FAILED (failures=2)` — identical count and identical 2 failures.
- Root cause is on the base candidate, not in the resolved files. No regression from this merge.

## actionlint (read-only, ci1-owned — no fix)

- `receipt-approval.yml`: clean.
- `receipt-shadow.yml`: clean.
- `receipt-post-run.yml`: **1 finding, pre-existing on base** — same as `ad4d0f28`:
  ```
  .github/workflows/receipt-post-run.yml:107:0: could not parse as YAML: could not find expected ':' [syntax-check]
      107 | import json, zipfile, sys
  ```
  False positive: unescaped newlines inside a `python3 -c "..."` within a `run: |` block — valid GitHub Actions. My i2 copy is byte-identical to base at this file, so this finding predates the merge. Not fixed (ci1 ownership + read-only mandate).

## repo-rule compliance

- **Write-set:** Only the 5 allowed files touched (2 modified in resolution by me; 3 changed by the pushswallow fast-forward). No product change outside merges. No ci1 files edited.
- **Merge method:** Ordinary `git merge` (no `--ff-only`, no `-X theirs`, no force). Push will be ordinary.
- **No self-approval, no force, no PR, no develop/main access** (branch stays on `work/r27-correction-v2`).
- **Evidence path:** `worktrees/i2/evidence-r27/i2-staging.md` (correct `evidence/...` location per protocol).
- **Scratch:** `/home/marcel/tmp-ops/i2-scratch` created; throwaway worktree `working` in repo (`baseharbor/worktrees/...`) to be cleaned by Coordinator per RUNBOOK, not me.

## END
END I2-DONE SHA=38771771e30c0326bf5e1f814554a37bd25a6439
