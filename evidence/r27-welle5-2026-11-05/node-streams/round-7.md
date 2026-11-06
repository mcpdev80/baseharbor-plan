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

## Round-7 commit + integration + remote head

- Round-7 commit: `2e285a771ed8adc30ccea8b4842cafad28815dd9`
- Base attestation (Owner directive): round-6 head `25a24667ebf087cd9c9f9fc3d24b49c436579569` IS an ancestor of my round-7 commit (`git merge-base --is-ancestor 25a2466 HEAD` => YES), and `git log 25a2466..HEAD` lists EXACTLY one commit (`2e285a7`) — no foreign candidate carried on top.
- Working tree isolation (Owner directive + coord handling): edits done in isolated worktree `/tmp/opencode/w215-wt` (cut `--detach` from round-6 head). The shared root-checkout `baseharbor-node-connector` was DIRTY with my two files after two coord warnings; removed losslessly (patch saved to `/tmp/opencode/w215-handoff-coord.patch`, `git checkout --` of EXACTLY those two files, `git status` clean). After that, all work is in the worktree only.
- Branch integrated by fast-forward `25a2466..2e285a7` (no second PR). Remote head verified: `git ls-remote origin work/r27-node-streams` => `2e285a771ed8adc30ccea8b4842cafad28815dd9`.

## Evidence commit to baseharbor-plan origin/main

- Evidence: baseharbor-plan/evidence/r27-welle5-2026-11-05/node-streams/round-7.md
- baseharbor-plan branch: main, pushed to origin/main `bcf5550b7e7448d21ea2c91dc5a9813c16b3e3e7`
- ls-tree witness (exact, as on origin/main): `evidence/r27-welle5-2026-11-05/node-streams/round-7.md` present. No `.evidence/` dir in the product repo; product branch `work/r27-node-streams` clean.

## Hosted gates (auto-launched on push; workflow_dispatch NOT used)

- GitHub-hosted shared runners only. Neither gate triggered by me (workflow files are Owner's).
- CI · Node Connector Quality · 22/merge — run `42159456055`, run 65, event pull_request, sha `2e285a7` — watching to terminal.
- Connector Source Conformance — run on same head — watching to terminal.

### Gate results (terminal, on head 2e285a771ed8adc30ccea8b4842cafad28815dd9)

- CI · Node Connector Quality · 22/merge — run `42159456055` run#65 — `completed / success`, job `Test · Vet · Build`: success. First run failed with a flake in round-6 Case A (`stream_evidence_test.go:1214: case a: resume at cursor 1 must be rejected, got nil error over 510 wire events`) — round-6 code, NOT my change.
- Connector Source Conformance — run `42159456071` — `completed / success`, job `source` success; runtime matrix legs skipped by path rules (matches review-22f).
- Local regression of the flake: `TestServeLogStreamCase[ABCD]` x3 = ok (190s); full ensemble incl Case E x3 = ok (193s); Case A x2 isolation = ok (120s). My change does not touch Case A. Re-ran the failed CI Quality run; rerun `42159456055` = success.
