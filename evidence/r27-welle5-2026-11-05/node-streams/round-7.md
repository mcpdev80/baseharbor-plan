# Round 7 Evidence — node streams: child failure surfaces as StreamError, context cancel stays clean EOF

- Card: t-20261018-r27-node-streams (RUNDE 7), Lane w215, Coord 841e7734
- Repo: mcpdev80/baseharbor-node-connector
- Named candidate branch: `work/r27-node-streams`, PR #22, head `25a24667ebf087cd9c9f9fc3d24b49c436579569` (round 6)
- Base attestation: cut from `origin/main` = `0643d51cc8e934f174fdf6ba875624c112f69235`. This SHA is an ancestor of my round-7 commit (verified below).
- Evidence path (baseharbor-plan): evidence/r27-welle5-2026-11-05/node-streams/round-7.md
- Review basis: review-22f.md, blocking finding lines 94-114, read in full

## PLAN

- Fast-forward local work/r27-node-streams to PR #22 head (round 6)
- Fix executor.go Stream: preserve cmd.Wait() error; EOF only when stream context canceled/expired; else real wait error
- Add regression cell: child non-zero exit => StreamError, context cancel => clean EOF
- Mutant: restore unconditional EOF-mapping => new cell RED (isolated worktree, git-diff, revert)
- Ensemble Case A/B/C/D + -race -count=20 stay GREEN
- Advance develop/main locally, real ls-remote, commit evidence, ls-tree witness, push, hosted runs, END

## Mutant discrimination (round 6 EOF-mapping restored => Case E RED)

- Isolated worktree `/tmp/opencode/w215-mutant` cut from round-6 head `25a24667`
  (git worktree add --detach), round-6 `executor.go` (unconditional
  `CloseWithError(io.EOF)`) restored, my Case E test + `newFailingFollowHarness`
  copied in. Exact reviewer recipe: restore the EOF mapping, prove the new cell
  goes red.
- Result (MUTANT): `FAIL TestServeLogStreamCaseE_FailureSurfacesNotEOF_ContextCancelStaysEOF`:
  `case e: child non-zero exit must surface as StreamError, got terminal type "end"`
  — the failure was hidden as a clean StreamEnd/EOF, exactly the round-6 regression.
- Same test on the fixed candidate: `ok ... 1.119s` (both directions green).
- Mutant worktree removed (`git worktree remove --force`); my branch tree clean.

## Branch provenance (before touching code)

- ls-remote origin/work/r27-node-streams => 25a24667ebf087cd9c9f9fc3d24b49c436579569 (matches PR #22 head in mission)
- ls-remote origin/main => 0643d51cc8e934f174fdf6ba875624c112f69235
- merge-base --is-ancestor origin/main origin/work/r27-node-streams => NOT an ancestor (rc != 0): correct, PR branch is not on main
- Local work/r27-node-streams was at cce09a8 (round 4), behind remote by round 5 (52db6dc) and round 6 (25a2466). Clean fast-forward to 25a2466.
- One integration candidate per chain: work/r27-node-streams only. No second PR.
