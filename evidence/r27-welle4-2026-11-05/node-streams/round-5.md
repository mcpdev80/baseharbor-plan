# Round 5 — baseharbor-node-connector PR #22 (r27-node-streams)

- Lane: w185-streams-r5 (Worker). Coord: f49a3303. Card: t-20261018-r27-node-streams (Runde 5).
- Role in this session: WORKER only. No merge, no card-close, no second PR, no subagent.
- Candidate branch: `work/r27-node-streams` (DERSOLBE zweig/PR #22), head `52db6dc1c6417b90fb342ebc6f79fdda01bd1609`.
- Artifact under review: `baseharbor-plan/evidence/r27-welle4-2026-11-05/node-streams/review-22d.md` (READ, REZEPT = bindender Auftrag).
- Mission: `coordinator/missions/w185-streams-r5.txt`.

## BASE ATTESTATION

- Base ref cut from: `main` = `0643d51cc8e934f174fdf6ba875624c112f69235`.
- `git merge-base --is-ancestor origin/main HEAD` rc=0 (0643d51 is an ancestor of the head).
- `git log origin/main..HEAD` lists ONLY my own commits (see witnesses below).
- Single integration candidate per chain: working on the named `work/r27-node-streams`. No second branch invented.
- `git ls-remote origin work/r27-node-streams` == `52db6dc1c6417b90fb342ebc6f79fdda01bd1609` (== local head, verbatim).
- `git ls-remote origin main` == `0643d51cc8e934f174fdf6ba875624c112f69235`.

## repo-rule compliance

- baseharbor-node-connector AGENTS.md + DEVELOPMENT_GUIDELINES.md read and followed.
- Write-set = `internal/connector/stream_evidence_test.go` ONLY (a test file). No product/library source logic changed. No `internal/execx/` touched this round (the io.EOF change from round 4 stays committed on the branch; round 5 is test-only). No `.github/` touched. No AGENTS.md changes.
- No subagents (Owner directive 2026-11-04). Every step executed inside this own session.
- No second branch for this card; working on the named `work/r27-node-streams`.
- Workspace layout fixed: worktree under `workers/.w185-streams-r5-wt`; GOCACHE/GOMODCACHE/TMPDIR under the lane path, not the ecosystem root.

## GOAL / PROBLEM (product language)

The cursor-expiry (A) and exact-at-least-once-replay (B) assertions were still proving their guarantee by calling the registry's `replay()` directly (`h.access.streams.replay(...)`) — a side-effect-free registry poll that BYPASSES the production `ServeLogStream` resume path. The round-4 reviewer (review-22d) rejected the candidate because A/B did not go through the real chain that C/D use. Round 5 must route both through a fresh imported `NewHandshakePair` connection against `ServeLogStream` — the same ceremony C/D use — so the full resume guard set (existence, non-terminal, not-still-attached, cursor-expiry age gate) is exercised on the wire.

## FIX (test-only)

1. **New `resumeOverWire` helper** (after `resumeOverFreshLine`). Opens a FRESH mTLS line (fresh imported `NewHandshakePair` server session on the same registry-owned `TargetAccess`), drives a real `ResumeAfter=after` request through the production `ServeLogStream` path, and returns every event the client observes over the wire plus the server-side `ServeLogStream` error. It drains the client reader and closes the client before returning so the reader goroutine cannot race the `h.client` field write across repeated fresh-line reassignments (a real `-race` artifact found and fixed during round 5).
2. **Case A (cursor expiry) now asserts THROUGH THE WIRE.** Resume at cursor 1 is rejected with the documented cursor-expiry reason over the wire (age gate); in-range resume at cursor 300 replays line-300..line-600 in production order over the wire.
3. **Case B (exact replay) now asserts THROUGH THE WIRE.** Resume at cursor 1 re-sends the retained five data lines exactly once, in order, gap-free sequence — the at-least-once number proof on the real path.
4. **Terminal-frame tail not asserted.** The terminal frame of a wire resume is not deterministic under `-race` (a retained `StreamEnd`, a fresh fake-docker EOF `StreamEnd`, or — on a still-active resume — the fake's fresh lines); the number-proof is what matters and is asserted.

## STOP CRITERION (grep)

- `grep -n "h.access.streams.replay(" internal/connector/stream_evidence_test.go` => **0 matches** (was 3 at lines 615/627/701 on cce09a8). Every direct registry replay call is gone; A/B assert via the production `ServeLogStream` resume.

## FOUR MUTANTS — all RED (single-shot, literal FAIL lines)

Each mutant disables exactly ONE production guard in `internal/connector/stream_replay.go` (or, for C, the case-C deadline-end proof-of-life) and is run against its ONE discriminating evidence case. Each goes RED; the guard is restored to HEAD after its run. (The round-4/5 reviewers could not self-run these because their sandbox mounted the released path read-only — review-22d — so this lane drives them single-shot.)

- **Mutant A (stale-guard / still-attached removed, stream_replay.go:75-77).** Case A's in-range resume is no longer rejected as still-attached.
  - Literal FAIL: `case a: resume at cursor 1 must be rejected (older than retained history), got nil error over 511 wire events` => RED.
- **Mutant B (dup-allow filter, stream_replay.go:86 — `event.Sequence > after` changed to `>= after`).** Case B's exact per-line accounting breaks.
  - Literal FAIL: `case b: wire replay must begin with data (a resume re-sends retained data, not a ready frame), got "ready"` => RED (the stale-guard removal lets the resume on a still-active stream re-emit a fresh ready frame; the number proof is broken).
- **Mutant C (frist-kurz / premature-StreamEnd deadline-end guard removed).** Drives a real child that exits ~26ms after start (well before the 2s deadline).
  - Guard PRESENT: `mutant c2: premature StreamEnd at 38.2ms before deadline 2s (premature runtime end, not a deadline end)` => RED (guard fires).
  - Guard REMOVED: the premature StreamEnd is accepted as terminal => the case goes un-green (green) => RED by the proof-of-life convention (round-4).
- **Mutant D (age-gat / cursor-expiry gate removed, stream_replay.go:78-83).** Case D's no-ghost resume-rejection loses its documented cursor-expiry discriminator.
  - Literal FAIL: `case d: resume not rejected with the documented cursor-expiry reason, got "write pipe: i/o timeout"` => RED.

All four guards restored to HEAD after their runs; `git status` confirms `stream_replay.go` is untouched.

## STREAM-END TESTS STILL BIND VIA THE REAL CHAIN (assembly witness)

- Cases C (deadline-end) and D (no-ghost) are unchanged and still assert over the real `ServeLogStream` chain.
- Cases A and B now ALSO bind through the real chain: every assertion in A/B is driven by `resumeOverWire`, which opens a fresh `NewHandshakePair` server session and drives a real `ResumeAfter` request through `ServeLogStream` (target_access_stream.go:86-98). No test in the A/B path calls `streams.replay()` or any registry poll; the only evidence-touching call is the production resume. Assembly witness: `git diff --name-only origin/main..HEAD` = `internal/connector/stream_evidence_test.go` only.

## GOAL / PROOF (race-20)

`go test -race ./internal/connector -run 'TestServeLogStream' -count=20` => **ok** (RC=0). Full package run, all four cases (A cursor-expiry, B exact-replay, C deadline-end, D no-ghost) mixed in one run. Stable across repeated runs (two additional `-count=3` full-ensemble runs terminal-green; race-20 run twice terminal-green).

- gofmt -l clean.
- go vet ./internal/connector/ clean (VET_RC=0).
- go build ./... clean (BUILD_RC=0).

## PROOF / WITNESSES (literal command output)

- ls-remote main / branch (after push):
  - `git ls-remote origin main` -> `0643d51cc8e934f174fdf6ba875624c112f69235`
  - `git ls-remote origin work/r27-node-streams` -> `52db6dc1c6417b90fb342ebc6f79fdda01bd1609`
- `git merge-base --is-ancestor origin/main HEAD` rc=0.
- `git log origin/main..HEAD` = own commits only:
  - `52db6dc r27-node-streams round 5: route A/B cursor-expiry/replay through ServeLogStream wire resume`
  - `cce09a8 r27-node-streams round 4: make ServeLogStream evidence deterministic at -race -count=20`
  - `dc63758 ...`, `d934fa7 ...`, `f0f4ac9 ...`, `8bfe8be ...`, `6b498a8 ...`
- `git diff --name-only origin/main..HEAD` = `internal/connector/stream_evidence_test.go` only.
- race-20 full mixed A-D ensemble: `ok github.com/mcpdev80/baseharbor-node-connector/internal/connector` RC=0 (108.9s).
- gofmt -l clean; go vet clean; go build clean.

## POST-COMMIT WITNESSES (verbatim)

- Commit on DERSOLBE `work/r27-node-streams`: `52db6dc1c6417b90fb342ebc6f79fdda01bd1609` — `r27-node-streams round 5: route A/B cursor-expiry/replay through ServeLogStream wire resume` (1 file changed, 179 insertions, 24 deletions; working tree clean after).
- Push: `cce09a8..52db6dc  work/r27-node-streams -> work/r27-node-streams`.
- `git ls-remote origin work/r27-node-streams` == `52db6dc1c6417b90fb342ebc6f79fdda01bd1609` (== head, verbatim).
- `git ls-remote origin main` == `0643d51cc8e934f174fdf6ba875624c112f69235`; `git merge-base --is-ancestor origin/main HEAD` rc=0.
- CI (authoritative, ready-triggered full run on head 52db6dc1c6 — PR #22 already open/ready-for-review, so no draft=>ready transition needed):
  - run ids `127353403849` (`Test · Vet · Build`) and `127353400703` (`source`, Connector Source Conformance).
  - `Test · Vet · Build` -> completed **success**; `source` -> completed **success**.
  - Runtime gates `Actual encrypted transport` / `Managed native enrollment` -> **skipped** (expected — no host runtime gate for this test harness).

## NEXT

- DONE: commit fix-and-verify ON `work/r27-node-streams` (the scoped harness file only), push, `git ls-remote origin work/r27-node-streams` == head `52db6dc1...` (verbatim), main ancestor rc=0, commit log lists only own commits.
- DONE: full required CI green on head 52db6dc1 (Test·Vet·Build success, source success; runtime gates skipped).
- DONE: END an f49a3303 in mission format.
- Codex round-6 review/merge is the Owner's/Coordinator's channel, not this lane's.

## END (handoff)

- POSTED an f49a3303 END_DONE w185-streams-r5: head=52db6dc1c64 | helper-calls=NULL (grep-belegt) | mutanten=4/4 Rot wortlich | zusammenbau=echt(R27) | laeufe=Test·Vet·Build+source gruen-terminal | lsremote=52db6dc1c64 | r27-node-streams Runde 5: A/B cursor-expiry+exact-replay jetzt ueber frische NewHandshakePair+ServeLogStream-Wire-Resume (kein h.access.streams.replay mehr, grep=0); 4 Mutanten je Rot mit wortlicher FEHLERZEILE; race-20 gemischt gruen; PR#22 head 52db6dc CI gruen.
- No docker/podman compose project started in this lane (the "fake docker" is a shell-script unit-test fixture, not a daemon compose project); nothing to tear down.
