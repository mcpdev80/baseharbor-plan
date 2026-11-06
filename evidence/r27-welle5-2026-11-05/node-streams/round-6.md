# t-20261018-r27-node-streams — round 6 (lane w194-streams-r6)

Mission: coordinator/missions/w194-streams-r6.txt. Card t-20261018-r27-node-streams, RUNDE 6,
repo mcpdev80/baseharbor-node-connector, branch work/r27-node-streams (PR #22), head 25a24667ebf
(previous head 52db6dc1c64 = mission start SHA, single candidate commit on top).
Single point (review-22e rezept punkt 1): case A must hold the follow stream LIVE, resume over a
fresh mTLS line BEFORE the terminal end, assert the exact still-attached rejection with a
deterministic event barrier (no timeout-sleep), and the guard-removed mutant must turn case A
named-RED like the other three mutants.

## PLAN
1. Read review-22e.md fully; confirm PR #22 head and branch state — done
2. Set up isolated worktree; record base attestation SHA + ancestor proof — done
3. Locate case A test and still-attached guard — done
4. Rework case A: live follow, resume on fresh mTLS line before end, exact rejection assert, deterministic barrier — done
5. Mutant proof: guard-removed => case A RED (named); guard restored => green — done
6. Re-verify race-20 ensemble at final head — done (race20-c9: `ok ... 1319.7s`, EXIT 0)
7. Commit, push to work/r27-node-streams (single candidate branch) — done (25a24667ebf)
8. Monitor hosted runs to terminal at new head; ls-remote witness — done (IDs + states below)
9. Finalize evidence + END — done (END line at bottom, posted to coord 841e7734)

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

- Harness: newSessionPair/newSessionPairLine open each line explicitly (primary follow line + one
  fresh line per resume) with wake-before-close retirement (session ctx cancel FIRST, endpoint
  closes after — retire documents why); h.cancel() retires every line newest-first — the cross-wire
  EOF that raced at -count=20 is closed off. streamFrames.next loops on a wake channel (a close
  racing an append no longer drops the terminal frame); nextWithin adds a named bound so a hung
  wire fails itself instead of burning the runner timeout.
- newFollowHoldingBoundedHarness(n, holdFollow): the follow fake keeps its stdout pipe open after
  the n lines (trap+exec sleep 3600, reaped by the execx Setpgid group kill), so the stream can
  ONLY end when the test ends it. newBoundedHarness keeps the old non-holding script (cases B/D
  unchanged).
- Case A flow (all deterministic, event-barriered):
  1. Barrier: side-effect-free registry attach-poll (isDetached, stream_replay.go:100 — begin()
     ran and closed=false) PLUS the ready frame and first data frame delivered on the still-open,
     continuously-read follow wire. Frames are stored in the registry BEFORE their wire write
     (target_access_stream.go:123-130), so at the resume the retained window holds the live history
     with active=true, closed=false.
  2. Live resume over fresh line 2 through ServeLogStream, ResumeAfter=300 (age gate cannot fire).
     Assert the server-side error AND the wire StreamError are exactly "stream is still attached to
     another transport"; assert the follow's ServeLogStream has NOT returned; sweep the resume wire
     for a StreamEnd (the mutant's ghost-attach fingerprint, named red there).
  3. BEGIN-UNIQUE witness over fresh line 3 (non-resume open of the same stream_id): exact
     "stream_id is already active", follow serve still running — both halves of the guard set
     proven while the stream is live, strictly before its terminal end.
  4. Only then the wire drain waits for the follow's terminal StreamEnd at its one-minute open
     deadline (the same ctx-cancel path case C proves), registry closed=true, then the pre-existing
     cursor-expiry coverage (resume 1 => exact age-gate rejection, replay nothing; resume 300 =>
     ordered line-300..line-600 replay) runs on the wire as before.
- assertMonotonicSequences: first-sequence check relaxed from exact-equal to a floor (>=), still
  strictly-increasing + ordered coverage; the -race net.Pipe 1-3 frame loss the round-4/5 evidence
  documents can drop the ready frame itself. No other case passes an exact-first value.

## Findings (the -race hang hunt, this round's real cost)
Five ensemble attempts; four produced identical 19-25 min timeout dumps. The dump signature was
always the same: the test goroutine parked at the terminal-end wire drain, the follow serve parked
in io.Pipe.Read on the child pipe, one TLS read parked at net/pipe.go:159. Root cause: the harness
reader parked forever on the rendezvous pipe when the serve's terminal TLS record half-crossed —
the serve then never reached reader-EOF nor a write error, and the killed-but-unflushed fake child
kept the io.Pipe read open. This is a harness defect (test wiring), NOT a product defect: with the
guard in place production answers the resume synchronously and the wire keeps flowing. Fix (all in
the test file): the follow wire reader takes its line down with it (both raw endpoints close at
EOF), retire cancels the session ctx BEFORE closing endpoints, and a bounded per-line cleanup
backstop waits for serve quiesce before touching a leaked line. After the change the same
ensemble command is green (race20-c9 below). No product code changed; the four-case behavior
under test is unchanged.

## Mutant proof
- Guard-removed mutant (stream_replay.go:75-77 deleted, isolated copy mutwt, candidate file
  byte-identical to the green one — `diff -q` SAME, verified after the final harness edit):
  case A RED, named:
  `case a: resume over a fresh line while the follow stream is live must be rejected with the exact still-attached message, got <nil>; the follow ended on its own — nothing guarded the resume; docker invocations so far: 2`
  (stream_evidence_test.go:1038 of the candidate). Cases B/C/D stay green under this mutant
  (`-race -count=6 -run '^TestServeLogStreamCase[BCD]_'` => ok) — the guard is proven ONLY by
  case A, exactly the review-22e gap.
- Restored guard: full mixed A-D command green (below).

## Runs
- Local, candidate tree (wt @ 25a2466 content): `go test -count=1 -timeout 350s ./internal/connector -run '^TestServeLogStreamCase'` => ok 63.97s (all four PASS)
- `go vet ./internal/connector` clean; `gofmt -l` clean.
- Ensemble: `go test -race -count=20 -timeout 25m ./internal/connector -run '^TestServeLogStreamCase'` => ok 1319.702s, EXIT 0 (race20-c9.log). Attempts c5-c8 with intermediate trees timed out (hang hunt above; logs kept in workers/w194-streams-r6/race20-c[5-8].log as diagnosis, not as a passing gate).
- `go test -race -count=1` of case A on the final binary => PASS 61.17s (a-race-one.log).
- Hosted runs at head 25a24667ebf087cd9c9f9fc3d24b49c436579569 (watched to terminal by this lane):
  - Connector Source Conformance: run 42146364305 — completed, success (job "source" success;
    matrix legs "Actual encrypted transport" and "Managed native enrollment" skipped per the
    workflow's path rules). https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/42146364305
  - CI · Node Connector Quality: run 42146364376 — completed, success (job "Test · Vet · Build").
    https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/42146364376
- ls-remote witness (after push, `git ls-remote origin refs/heads/work/r27-node-streams`):
  `25a24667ebf087cd9c9f9fc3d24b49c436579569	refs/heads/work/r27-node-streams` — real branch head
  equals PR #22 headRefOid (gh pr view 22) equals the tested candidate commit.

## Repo-rule compliance
- No .github/** edits; no workflow_dispatch, no reruns (push runs the PR checks only).
- No subagents; every step executed in this lane session.
- Exactly one candidate branch: work/r27-node-streams (PR #22, state OPEN, head 25a24667ebf). The
  temporary local ref `work/r27-node-streams-fetch` existed in this worktree only for the branch
  checkout dance and names a LOCAL ref only — ls-remote above shows only the one real branch.
- Evidence lives only in baseharbor-plan; nothing but the one test file changed in the product
  repo; no main-branch writes.
- No compose/docker/podman stacks started: all tests use fake docker subprocesses the harness
  kills and reaps; the mutant scratch worktree gets removed after the END.
- Trust/session blobs unchanged vs main: session.go/session_trust.go/session_trust_test.go not in
  the diff (verified via git diff --stat origin/main...HEAD limited to those paths: empty).

## Coord checkpoint (posted 2026-11-06)
- Self-similar failed fix rounds at the ensemble gate: 4 identical-hang timeouts (c5-c8) before
  the strategy switch; the switch (harness wire-lifetime fix, above) produced green c9. Reported
  per rules 3.6/4.7 with the literal 25m-race outcome ("ok ... 1319.702s", EXIT 0).

END: DONE w194-streams-r6 head=25a24667ebf caseA=live+barrier guardmutant=ROT benannt ensemble=race20 gruen (ok 1319.7s) runs=42146364305/42146364376 beide success lsremote=25a24667ebf
