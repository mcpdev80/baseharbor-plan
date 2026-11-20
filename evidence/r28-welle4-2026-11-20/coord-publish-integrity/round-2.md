# coord-publish-integrity round-2 (0428-175, correcture round)

- lane: coord-0428-175-publish-gates (worktree /tmp/coord-175-wt)
- commits: a7f98208 (r4) -> f91596bf (r5) -> 8488c38e (r6)
- base 63565328 confirmed ancestor of HEAD; no foreign commits in 63565328..HEAD
- commits durable via branch coord-0428-175-publish-gates (coordinator repo hat kein remote)
- scope: coordinator/ repo only. No product code, no baseharbor, no .github/**. Main tree not touched.

## Owner corrections addressed

1. **Structural-abort test produced no real git conflict (was rc=0, test setup wrong).**
   The old test wrote conflict markers directly into a working-tree file and asserted
   `resolve_conflict` aborts. But `git diff --diff-filter=U` only flags *unstaged*
   unmerged files (a real rebase leaves them); a marker-only working-tree edit showed
   no unmerged state, so `resolve_conflict` saw no conflict and returned True.
   Fix: the test now runs the REAL two-clone flow (both change the `owner:` line,
   second push fails fast-forward -> rebase -> genuine rc=1 conflict on the owner
   line). `resolve_conflict` now returns False (abort) and leaves markers + MERGE
   state intact. The full call chain now fails at point (c), not just a helper unit.

2. **Mutation proof added.** `test_owner_conflict_abort_mutation` neutralises the
   structural-abort branch (resolver returns True) and asserts the mutated resolver
   wrongly merges — i.e. the test is RED without the logic, GREEN with it. This proves
   the test actually exercises point (c), not that it passes vacuously.

3. **Fixture-leiche cleaned.** Tests previously left `tmp*/` dirs in the worktree
   (`scripts/tmp<rand>/` from watch tests, `tmp<rand>/` from Defect3). Both test
   classes now clean up in `tearDown` (`shutil.rmtree`) / `setUp` cleanup. Verified:
   0 untracked files after a full suite run.

## pytest lines (vorher / nachher)

- VORHER (Stand a7f98208): `python3 -m pytest -q` -> `1 failed, 22 passed in 0.38s`,
  `FAILED ...::Defect3ConflictTragend::test_owner_conflict_aborts`
  `AssertionError: 0 == 0 : rebase should conflict on owner`
- NACHHER (Stand 8488c38e): `python3 -m pytest -q` -> `13 passed in 0.36s`
- full-suite run repeated 10x, all `13 passed` (stable, no flakiness).
- worktree cleanliness after full run: `git status --porcelain` -> 0 lines.

## cleanliness: vorher / nachher

- vorher (Owner gemessen, Stand a7f98208): 6 untracked fixture dirs
  `scripts/tmpcdf12cj0/ scripts/tmpeos_pb5u/ scripts/tmpx_yyzvq7/ tmpnmcx0wm8/
  tmppnilfa5_/ tmpqm1fa7mu/`
- nachher (nach r6 cleanup): `git status --porcelain | grep -c "??"` -> 0
  (watch-only run: 0; full-suite run: 0)

## commit-sha for Owner

- branch: coord-0428-175-publish-gates
- commits this round: f91596bf (r5), 8488c38e (r6)
- prior: 26a99705 (r2), 16096c0d (r3), a7f98208 (r4)
- base: 63565328 (coordinator master, confirmed ancestor)
- Owner merges (I do not merge): report branch + commit-sha, Owner merges.
