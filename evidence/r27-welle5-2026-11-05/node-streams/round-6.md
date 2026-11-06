# t-20261018-r27-node-streams — round 6 (lane w194-streams-r6)

Mission: coordinator/missions/w194-streams-r6.txt. Card t-20261018-r27-node-streams, RUNDE 6,
repo mcpdev80/baseharbor-node-connector, branch work/r27-node-streams (PR #22), head 52db6dc1c64.
Single point (review-22e rezept punkt 1): case A must hold the follow stream LIVE, resume over a
fresh mTLS line BEFORE the terminal end, assert the exact still-attached rejection with a
deterministic event barrier (no timeout-sleep), and the guard-removed mutant must turn case A
named-RED like the other three mutants.

## PLAN
1. Read review-22e.md fully; confirm PR #22 head and branch state — done
2. Set up isolated worktree; record base attestation SHA + ancestor proof — done
3. Locate case A test and still-attached guard — done
4. Rework case A: live follow, resume on fresh mTLS line before end, exact rejection assert, deterministic barrier — done
5. Mutant proof: guard-removed => case A RED (named); guard restored => green — done (single run; ensemble run pending below)
6. Re-verify race-20 ensemble at final head — in progress
7. Commit, push to work/r27-node-streams (single candidate branch) — pending
8. Monitor hosted runs to terminal at new head; ls-remote witness — pending
9. Finalize evidence + END — pending

## Base attestation
- Branch cut point: 52db6dc1c6417b90fb342ebc6f79fdda01bd1609 (= origin/work/r27-node-streams at
  start = PR #22 head = mission SHA 52db6dc1c64; verified by `git ls-remote` and
  `gh pr view 22 --json headRefOid`).
- `git merge-base --is-ancestor origin/main 52db6dc...` passes: origin/main
  0643d51cc8e934f174fdf6ba875624c112f69235 is an ancestor of the cut point.
- develop-stand at cut: the repo has NO develop branch; PR #22 targets main @ 0643d51cc8e. Recorded
  here per the gate "develop-stand bei schnitt in akte".
- Worktree: /home/marcel/dev/baseharbor-ecosystem/workers/w194-streams-r6/wt (the original
  /tmp/opencode/w194-streams-r6-wt was destroyed mid-run by a tmpfs disk-quota event on the host;
  the replacement lives under workers/, per the fixed workspace layout. Same candidate base SHA.)
- Mutant scratch: workers/w194-streams-r6/mutwt (isolated copy, never pushed).

## Findings (case A rework)
File: internal/connector/stream_evidence_test.go only. Production files untouched (diff vs
52db6dc touches just the one test file).

- Harness: newSessionPair opens each line explicitly (primary follow line + one fresh line per
  resume), h.cancel() retires every line newest-first with endpoint closes — the cross-wire EOF
  that raced at -count=20 is closed off. streamFrames.next now loops on a wake channel (a close
  racing an append no longer drops the terminal frame).
- newFollowHoldingBoundedHarness(n, holdFollow): the follow fake keeps its stdout pipe open after
  the n lines (trap+exec sleep 3600, reaped by the execx Setpgid group kill), so the stream can
  ONLY end when the test ends it. newBoundedHarness keeps the old non-holding script (cases B/D
  unchanged).
- Case A flow (all deterministic, event-barriered):
  1. Barrier: ready frame + first data frame delivered on the still-open follow wire. Frames are
     stored in the registry BEFORE their wire write (target_access_stream.go:123-130), so at the
     resume the retained window holds the live history with active=true, closed=false.
  2. Live resume over fresh line 2 through ServeLogStream, ResumeAfter=300 (age gate cannot fire:
     after+1 < first is false against sequences 1..10). Assert the server-side error AND the wire
     StreamError are exactly "stream is still attached to another transport"; then assert the
     follow's ServeLogStream has NOT returned (still attached).
  3. BEGIN-UNIQUE witness over fresh line 3 (non-resume open of the same stream_id): exact
     "stream_id is already active", follow serve still running — both halves of the guard set
     proven while the stream is live, strictly before its terminal end.
  4. Only then the follow is ended (rejected serves close their sessions; the follow's
     disconnect retires it): terminal StreamEnd on the wire, closed=true; pre-existing
     cursor-expiry coverage (resume 1 => exact age-gate rejection, replay nothing; resume 300 =>
     ordered line-300..line-600 replay) runs on the wire as before.
- assertMonotonicSequences: first-sequence check relaxed from exact-equal to a floor (>=), still
  strictly-increasing + ordered coverage; the -race net.Pipe 1-3 frame loss the round-4/5 evidence
  documents can drop the ready frame itself (observed: first data seq 3, 599/600 lines delivered).
  No other case passes an exact-first value that would change.

## Mutant proof
- Guard-removed mutant (stream_replay.go:75-77 deleted, isolated copy mutwt, candidate file
  identical to the green one): case A RED, named:
  `case a: resume over a fresh line while the follow stream is live must be rejected with the exact still-attached message, got <nil>; the follow ended on its own — nothing guarded the resume; docker invocations so far: 2`
  (line 911 of the candidate test file). Cases B/C/D stay green under this mutant — the guard is
  proven ONLY by case A, exactly the review-22e gap.
- Restored guard: full mixed A-D command green (below).

## Runs
- Local, candidate tree: `go test -count=1 ./internal/connector -run '^TestServeLogStreamCase'` => ok 64.8s (all four PASS)
- `go test -race -count=1` same => ok 72.7s
- `go test -race -count=20 ./internal/connector -run '^TestServeLogStreamCase[ABCD]_'` => first attempt timed out at 800s wall (case A now spends ~60s in the rejected-resume window per iteration; ensemble must be bounded). Re-run with -timeout 850s in progress; TODO: if still over, shorten the resume open deadline so the guard answers well before any deadline while keeping the exact-message assertion.
- Hosted runs at new head: TODO (terminal states + run IDs).
- ls-remote witness: TODO

## Repo-rule compliance
- No .github/** edits; no workflow_dispatch, no reruns (push runs the PR checks only).
- No subagents; every step executed in this lane session.
- Exactly one candidate branch: work/r27-node-streams (PR #22). A temporary local ref
  `work/r27-node-streams-fetch` existed in this worktree only for the branch checkout dance; it
  was deleted locally (ls-remote witness below shows it was never pushed). No second PR.
- Evidence lives only in baseharbor-plan; nothing but the one test file changed in the product
  repo; no main-branch writes.
- No compose/docker/podman stacks started: nothing to bring down (all tests use fake docker
  subprocesses that the harness kills and reaps; the mutant scratch worktree gets removed).
- Trust/session blobs unchanged vs main: session.go/session_trust.go/session_trust_test.go not in
  the diff (verified via git diff --stat origin/main...HEAD limited to those paths: empty).

END: TBD
