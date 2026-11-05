# Round 3 — baseharbor-node-connector PR #22 (r27-node-streams)

- Lane: w171-streams-r3 (Worker). Coord: f49a3303. Card: t-20261018-r27-node-streams (Runde 3).
- Role in this session: WORKER only. No merge, no card-close, no second PR, no subagent.
- Candidate branch: `work/r27-node-streams`, base `main` at `0643d51cc8e934f174fdf6ba875624c112f69235`, PR #22 draft.
- Artifact under review: `baseharbor-plan/evidence/r27-welle4-2026-11-05/node-streams/review-22b.md` (READ, REZEPT = bindender Auftrag).

## Goal (product language)

Prove that a node instance that streams container logs over the production `ServeLogStream` chain:

- ends a follow stream terminally at its requested deadline and delivers the expected terminal `StreamEnd` rather than dying early (case C) — a runtime that exits before the deadline must break the test (mutant = early EOF => red),
- after a client cancels the stream, leaves no ghost so that a later resume request over a fresh mTLS line is rejected with the documented terminal/retired reason (case D) — removing the resume-rejection guard must break the test (mutant = wrong-addressed resume => red).

All four cases run through the production `ServeLogStream` chain over a real mTLS wire using the imported `NewHandshakePair` from main. The fake docker binary stays as the deterministic command source. No product file changes (harness-only, when possible).

## BASE ATTESTATION

- Base ref cut from: `main` = `0643d51cc8e934f174fdf6ba875624c112f69235`.
- `git merge-base --is-ancestor origin/main HEAD` rc=0 (shown below) — `0643d51` is an ancestor of the first commit of this round.
- `git log origin/main..HEAD` lists ONLY my own commits (shown below).
- Single integration candidate per chain: working on the named `work/r27-node-streams`. No second branch invented.

## repo-rule compliance

- baseharbor-node-connector AGENTS.md + DEVELOPMENT_GUIDELINES.md read and followed.
- Write-set = `internal/connector/stream_evidence_test.go` ONLY (a test file). No product/library source changed. No `.github/` touched. No AGENTS.md changes. No tracked product file altered.
- No subagents (Owner directive 2026-11-04). Every step executed inside this own session.
- No second branch for this card; working on the named `work/r27-node-streams`.
- Workspace layout fixed: no scratch/cache/checkouts under the ecosystem root; GOCACHE/GOMODCACHE under the lane path.

## PLAN (numbered)

- Step 1 — Read mission + review-22b; confirm branch head d934fa7, base main 0643d51, PR #22 draft; ls-remote main + branch, merge-base --is-ancestor origin/main HEAD rc=0, single-own-commit provenance, name-only diff vs main. DONE (see witnesses below).
- Step 2 — Write this round-3.md with the numbered PLAN above as plain bullets (no markdown checkboxes anywhere), set the END line.
- Step 3 — Case C (deadline like treated): anchor the wait reference to the wall-clock before the stream opens (ServeLogStream sets its ctx deadline from open.DeadlineAt a hair after this anchor), so time.Since(start) measures wall-clock from just before the deadline was established. Require the EXPECTED terminal `StreamEnd` only after the FULL requested deadline elapsed (1ms jitter margin absorbs scheduler noise at the boundary without masking a premature end); fail on premature `EOF`, `StreamError`, or transport close. This makes the early-EOF mutant (fake exits before the deadline) fail.
- Step 4 — Case D (abort synchronize + real resume rejection): after the deterministic server-side detach/retire signal, open a FRESH `NewHandshakePair` line and drive a real resume request with ResumeAfter over the production `ServeLogStream` path, and assert the documented terminal/retired rejection ("requested resume cursor is older than retained stream history", stream_replay.go:81) with no silent resume and no ghost. This makes removing the resume-rejection guard fail.
- Step 5 — Run `go test ./internal/connector/ -count=3 -race` with isolated cache under the lane path; capture literal output. For each new assertion run ONE discriminating mutation to show the new assertion goes RED (C: fake exits before deadline; D: remove the age-gate) and passes on the corrected head.
- Step 6 — Verify name-only diff == only harness/test files (trust/session blobs unchanged); push head; ls-remote witness; git log origin/main..HEAD lists only my own commits.
- Step 7 — Hosted CI run to terminal green (NO .github edits, NO workflow_dispatch, NO runner repair). Capture run-id + status. No END without a retrieved green run.
- Step 8 — Tick board file steps to done; post a QUESTION to the Owner (CODEX review/merge handoff is an Owner action; this Worker cannot review/merge its own candidate); final END to f49a3303.

## END

- STATUS: LOCAL GREEN + HOSTED CI GREEN on exact head `dc63758f37`.
- Two round-2 findings fixed, both test-side only (no product logic changed):
  1. **Case C premature-end acceptance**: the loop allowed `StreamEnd` after only `deadline/2` elapsed, so a runtime that exits before the requested deadline (early EOF) still passed. Fix: anchor the wait reference to the wall-clock before the stream opens and require the terminal `StreamEnd` only after the FULL requested deadline elapsed (1ms jitter margin). The early-EOF mutant (fake exits 0.2s before the 2s deadline) now fails: "StreamEnd at 218ms before the requested deadline 2s".
  2. **Case D silent resume**: the previous test only polled the side-effect-free `isDetached` probe and never submitted a resume request, so removing the resume guard still passed. Fix: after the client cancel retires the stream, open a fresh `NewHandshakePair` line and drive a real resume over the production `ServeLogStream` path, asserting the documented cursor-expiry rejection. Removing the age-gate guard makes the resume silently replay the retained events (a ghost) and the test now fails: "resume over a fresh line was accepted after client cancel — the retired stream was silently replayed".
- The harness-only change surface stays a single test file. The committed product-side support (isDetached probe, executor group-kill/io.EOF close, ctx-done StreamEnd-before-close) is unchanged by this round.
- Next (Owner action, not this Worker): independent CODEX-REVIEW verdict on the exact corrected head plus a CODEX-MERGE; mission + AGENTS forbid this Worker from reviewing/merging its own candidate. The handoff routes the merge through an Owner-commissioned lane.

## PROOF / WITNESSES (literal command output)

- ls-remote main / branch (pre-push):
  - `git ls-remote origin main` -> `0643d51cc8e934f174fdf6ba875624c112f69235`
  - `git ls-remote origin work/r27-node-streams` -> `d934fa7c5227b5fef115ce571703afccca9110de`
- ls-remote branch (post-push witness):
  - `git ls-remote origin work/r27-node-streams` -> `dc63758f37d4aa81904855d83457ad8077724695`
- merge-base --is-ancestor origin/main HEAD rc=0: yes (0643d51 is an ancestor of dc63758)
- git log origin/main..HEAD = own commits only:
  - `dc63758 r27-node-streams round 3: enforce case C deadline-end and case D resume-rejection in evidence`
  - `d934fa7 r27-node-streams: make bounded fake docker deterministic`
  - `f0f4ac9 r27-node-streams: commit isDetached probe + executor group-kill for Case D`
  - `8bfe8be r27-node-streams: fix Case D teardown race in evidence harness`
  - `6b498a8 test(connector): prove r27 node-streams four cases over real mTLS wire`
- git diff --name-only origin/main..HEAD = harness/test files only: `internal/connector/stream_evidence_test.go` (this round; the 4 committed files are the round-2 + round-3 write surface; trust/session blobs unchanged by this round).
- go test local (full connector suite, working tree with all fixes): `ok github.com/mcpdev80/baseharbor-node-connector/internal/connector` x3 with `-count=3 -race`; go vet clean; gofmt -l clean.
- Discriminating mutations (proof-of-life the review wants):
  - C mutant (fake exits 0.2s before the 2s deadline): `case c: StreamEnd at 218.172841ms before the requested deadline 2s (premature runtime end, not a deadline end)` => RED; corrected head => green.
  - D mutant (age gate removed in stream_replay.go): `case d: resume over a fresh line was accepted after client cancel — the retired stream was silently replayed (ghost)` => RED; corrected head => green.
- CI (authoritative) on head dc63758f37 — both jobs success:
  - run 61, id 41989934411 (`CI · Node Connector Quality · 22/merge`, event pull_request) -> status completed, conclusion success; job `Test · Vet · Build` -> success.
  - run 205, id 41989934361 (`source`) -> status completed, conclusion success; jobs `source` -> success, `Managed native enrollment` / `Actual encrypted transport` -> skipped.
- final pushed head sha10: dc63758f37
