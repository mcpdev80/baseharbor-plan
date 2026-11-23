# Owner takeover of the #1746 recut branch (sweep-1746)

## Situation
Seat w27-pr1627-0428-061-pull re-cut the #1746 assertion fix clean after the backing
branch `lane-0428-208-static-release-gate` was contaminated by an unrelated concurrent
worker stack (5c8ce8db4, 18 files incl. .github/release-requirements.json from #1614/#1803).
Per coordinator decision (RE-CUT, no force) the fix was cut fresh from the clean merged
#1746 candidate 6ba380b9d.

- Commit: 51ff183bf fix(1746): widen v0.4.28 gate assertion for merged reality
- Delta vs candidate base 6ba380b9d: exactly `scripts/test_pre_release_check_plan.py`
- Diff: line 40 `assertEqual(v0428, {'atomic/static/ci-fast-check'})` ->
  `assertEqual(v0428, {'atomic/static/ci-fast-check', 'atomic/static/mcp'})`
  (the merged candidate carries develop's v0.4.28-tagged atomic/static/mcp from #1793
  alongside #1746's own ci-fast-check v0.4.28 gate).
- Local verification: 5/5 scripts/test_pre_release_check_plan.py pass, 27/27
  scripts/test_pre_release_runtime_reuse.py pass; `bash scripts/ci-fast-check.sh` EXIT=0.

## Corrected classification (coordinator, content-checked 2026-11-23)
This was NOT a foreign contamination. The recut branch head is carried by additive
owner-side / parallel convergence commits on w27's own line. Authorship witness:
76ad7a733 (and df2bfce6f) are committed under the OWNER identity
(Marcel Pfingstgraeef <22537373+mcpdev80>, 15:10/15:30). The owner carries the
boundary / fast-check fixes (fix(ci): keep unknown static gates...; preserve fast-check
executor) onto the recut branch himself. Owner pushes are authoritative, not contamination.

## Three witnesses (required)
1. Ancestor proof: `git merge-base --is-ancestor 51ff183 76ad7a733` -> TRUE.
   `git merge-base 51ff183 76ad7a733` = 51ff183bfdcceaa4b383281a5c68421d1b770814.
   51ff183 IS an ancestor of the owner head 76ad7a733.
2. Head contains my fix: line 40 of `76ad7a733:scripts/test_pre_release_check_plan.py`
   == line 40 of 51ff183:
   `self.assertEqual(v0428, {'atomic/static/ci-fast-check', 'atomic/static/mcp'})`.
3. PR diff vs develop on owner head 76ad7a733 = exactly 15 files (contract + fixes,
   clean, shrank from the 74-file contaminated diff):
   .github/workflows/pre-release-runtime-suite.yml,
   .github/workflows/pre-release.yml, CHANGELOG.md,
   docs/releases/v0.4.28.demo-ref, scripts/ci-fast-check.sh,
   scripts/pr-gate-coverage.json, scripts/pr-gate-plan.py,
   scripts/pre-release-check-plan.py, scripts/pre-release-runtime-impact.json,
   scripts/release-requirements.json, scripts/test_ci_v0427_gate_catalog.py,
   scripts/test_pr_gate_coverage.py, scripts/test_pre_release_check_plan.py,
   scripts/test_pre_release_runtime_reuse.py, scripts/validate-pr-gate-coverage.py.

ls-remote current head of lane-0428-208-static-release-gate-recut = 76ad7a733
(contains hop tip f3d847874 in ancestry).

## Action taken this seat
1. No further writes on either branch. No force-push. No new branch. (Coordinator: no race.)
2. This akte with the three witnesses above.
3. END. The owner-line review + merge track runs from the owner stand; w27 hands the
   acceptance (run-id + BASE_SHA + per-job conclusions + named fixed-test receipt) to the
   coordinator from the owner line, does not re-trigger or re-push.

## cleanliness
- Local worktree workers/pr1746-fix-wt left at 51ff183 (verified intact, no writes after
  commit). No containers started (docker ps -a empty at handoff). No artifact left on the
  remote by this seat beyond the already-verified 51ff183 push, which is an ancestor of the
  current owner head.
