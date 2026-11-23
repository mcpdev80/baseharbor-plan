# 0428-208 / #1746 — INGRESS akte: static PR-executed-gate mapping in base policy

Date: 2026-11-23
Route: ROUTEN-ENTSCHEID (coordinator) — INGRESS, NOT owner-scope (scripts/** is lane-fixable).

## Candidate (unchanged, FINAL)
- #1746 candidate head: `b68372ecf6f8d2e29dfb9b59e9f0ad63c62cd443`
  (release-scope move + release-only catalog + validator future-coverage fix + 5 regression tests +
  wrapper verification; catalog/requirements/validator/wrapper contents preserved).
- No further branch-side edit to `scripts/pr-required-final.py` on the #1746 branch — that part of the
  tip becomes redundant once the ingress merges (the mapping now lands in the base).

## Ingress PR
- #1793 `ingress-0428-208-static-gate`, base develop (`cd9cc483`), head `9ba8e9baa7fe99b4465124edf166db6e61824088`.
  Draft, one PR pro Karte.
- Diff vs develop: exactly 2 files.
  - `scripts/pr-required-final.py`: shared `ATOMIC_STATIC_FOCUSED_GATES = frozenset({...})` constant
    (with source reference to `pr-stage-boundary.py:ATOMIC_STATIC_PR_EXECUTED_GATES`) + the
    `elif gate in ATOMIC_STATIC_FOCUSED_GATES: required.add('pr_focused')` mapping before the `else`.
  - `scripts/test_pr_required_final.py`: 2 regression tests — (a) shell-ux, (b) static-class general
    (ci-fast-check). Both assert: without a successful `pr_focused` the run blocks, with it the
    `verify()` returns `[]` (pass).
- No `.github` change.

## Root cause fixed (decisive)
- The `PR · Selected Checks` aggregate runs `git show "$CONTROLLER_SHA:scripts/pr-required-final.py"`
  (ci.yml:780-781, 855-864; `controller_sha=$effective_base` = develop tip for this PR). It does NOT
  read the candidate branch.
- Base policy `scripts/pr-required-final.py:66-69` previously mapped only `atomic/{docker,podman}/*`,
  `integration/static/public-contracts`, and coreless-lifecycle. Every other `atomic/static/*` gate
  fell through to `else: 'selected gate has no workflow executor'` — the shell-ux blocker that failed
  4 runs across 4 bases.
- Verified against develop's own file: applying the 1-line mapping to `cd9cc483:scripts/pr-required-final.py`
  and running `verify()` with `atomic/static/shell-ux` selected returns `[]` (passes).

## pr-stage-boundary.py (mcp-class check)
- `pr-stage-boundary.py` on develop already carries both `atomic/static/shell-ux` and
  `atomic/static/ci-fast-check` in `ATOMIC_STATIC_PR_EXECUTED_GATES` (line ~25). No mcp-class补 needed;
  the static gates are already classified as PR-executed. The ingress maps them to the focused job.

## Exact hosted CI (Eigenes-Run-Pflicht)
- Run 45112077135 on head `9ba8e9ba` (event pull_request).
- Conclusion: success. Jobs: 6 success, 27 skipped, 0 failures.
- `PR · Selected Checks` aggregate: no longer FAILS on shell-ux. All executed jobs pass.
- Prior runs with the same blocker: 45102450630, 45099897243, 45108377482 (all BLOCKED shell-ux).

## Still pending
- Coordinator sets #1793 review → merge (run green, evidence above).
- After merge: #1746 final-hop onto the new develop tip + exact run (aggregate expected green) + END.
