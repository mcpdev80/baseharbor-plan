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
- Ancestry: 6ba380b9d is a proven ancestor of 51ff183.
- Local verification: 5/5 scripts/test_pre_release_check_plan.py pass, 27/27
  scripts/test_pre_release_runtime_reuse.py pass; `bash scripts/ci-fast-check.sh` EXIT=0.

## Owner-push reclassification (coordinator, 2026-11-23)
The commits that moved the recut branch past 51ff183 are NOT a foreign contamination.
Authorship witness: 76ad7a733 (and df2bfce6f) are committed under the OWNER identity
(Marcel Pfingstgraeef <22537373+mcpdev80>, 15:10/15:30). The owner is carrying the
boundary / fast-check fixes (fix(ci): keep unknown static gates...; preserve fast-check
executor) onto the recut branch himself. Owner pushes are authoritative instructions,
not contamination.

- 51ff183 test fix is contained in the owner line 76ad7a733 (line 40 identical:
  `{'atomic/static/ci-fast-check', 'atomic/static/mcp'}`).
- git diff --name-only 51ff183 76ad7a733 lists only the owner's own scope
  (cmd/baha/*, contracts/machine/v1/*, docs/cli/*, internal/*, scripts/pr-*.py,
  scripts/ci-fast-check.sh) on top of the contained test fix.
- ls-remote current head of lane-0428-208-static-release-gate-recut = 76ad7a733.

## Action taken this seat
1. No further writes on either branch. No force-push. No new branch. (Coordinator: no race.)
2. This akte.
3. END. The owner-line review + merge track runs from the owner stand; w27 hands the
   acceptance (run-id + BASE_SHA + per-job conclusions + named fixed-test receipt) to the
   coordinator from the owner line, does not re-trigger or re-push.

## cleanliness
- Local worktree workers/pr1746-fix-wt left at 51ff183 (verified intact, no writes after
  commit). No containers started (docker ps -a empty at handoff). No artifact left on the
  remote by this seat beyond the already-verified 51ff183 push.

## witness
- `git ls-remote origin refs/heads/lane-0428-208-static-release-gate-recut` = 76ad7a733...
- `git diff --name-only 6ba380b9d 51ff183` = scripts/test_pre_release_check_plan.py
- `git show 76ad7a733:scripts/test_pre_release_check_plan.py | grep v0428` line 40 == 51ff183 line 40
