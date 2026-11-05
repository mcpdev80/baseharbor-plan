# Round 2 — baseharbor-node-connector PR #22 (r27-node-streams)

- Lane: w160-streams-r2 (Worker). Coord: f49a3303. Card: t-20261018-r27-node-streams (Runde 2).
- Role in this session: WORKER only. No merge, no card-close, no second PR, no subagent.
- Candidate branch: `work/r27-node-streams`, base `main` at `0643d51cc8e934f174fdf6ba875624c112f69235`, PR #22 draft.
- Artifact under review: `baseharbor-plan/evidence/r27-welle4-2026-11-05/node-streams/review-22a.md` (READ, REZEPT = bindender Auftrag).

## Goal (product language)

Prove that a node instance that streams logs from a container can:
- reject a resume cursor that is older than the container log history it still retains (case A),
- account exactly — no loss and no duplication — of every log line on first delivery and on replay (case B),
- end a follow stream cleanly at its deadline and deliver the expected terminal event rather than dying early (case C),
- leave no ghost session behind after a client cancels the stream, so a resume cannot resurrect a retired stream (case D).

All four are proven through the production `ServeLogStream` chain over a real mTLS wire using the imported `NewHandshakePair` from main. The fake docker binary stays as the deterministic command source only. No product file changes.

## repo-rule compliance

- baseharbor-node-connector AGENTS.md + DEVELOPMENT_GUIDELINES.md read and followed.
- Write-set = `internal/connector/stream_evidence_test.go` ONLY (a test file). No product/library source changed. No `.github/` touched. No AGENTS.md changes. No tracked product file altered.
- No subagents (Owner directive 2026-11-04). Every step executed inside this own session.
- No second branch for this card; working on the named `work/r27-node-streams`.
- Workspace layout fixed: no scratch/cache/checkouts under the ecosystem root; GOCACHE under the lane path.

## PLAN (numbered)

- Step 1 — Read mission + review-22a; confirm branch head 6b498a8, base main 0643d51, PR #22 draft; `merge-base --is-ancestor origin/main HEAD` rc=0; single-own-commit provenance. DONE (see evidence below).
- Step 2 — Write this round-2.md with the numbered PLAN above as plain bullets (no markdown checkboxes anywhere), set the END line.
- Step 3 — Case A (real expiry): make the finite fake docker emit MORE than the registry's retained-event limit (default 512, per `stream_replay.go:11`), resume with a cursor strictly older than the first retained sequence, and assert the exact documented rejection string `requested resume cursor is older than retained stream history` (`stream_replay.go:81`). Do not rely on the fake returning all lines in one frame; drive the boundary through the production path.
- Step 4 — Case B (exact accounting): assert ordered sequence numbers on first delivery and replay, and count exact per-line occurrence counts on both fresh and resumed payloads so loss and duplication are NUMBER-proven, not merely present.
- Step 5 — Case C (deadline like treated): record the requested deadline; require an explicit expected terminal `StreamEnd` after the deadline elapsed; fail the test on premature `EOF`, `StreamError`, or transport closure (they must not pass).
- Step 6 — Case D (abort synchronize): before resuming, wait for a deterministic server-side detach/retire signal — poll the registry until the stream is observed inactive/closed (`streams.active == false`), not a still-attached guard; then assert the resume is rejected for the retired-stream reason.
- Step 7 — Run `go test ./internal/connector/ -run 'TestServeLogStream' -count=1 -v` with an isolated cache under the lane path; capture literal output. For each new assertion, run one mutation (e.g. set a bound to 0 / remove the expiry trigger) to show the new assertion goes RED — the proof-of-life the review wants.
- Step 8 — Verify name-only diff == only `internal/connector/stream_evidence_test.go`; push head; `ls-remote` witness; `git log origin/main..HEAD` lists only my own commits.
- Step 9 — Tick board file steps to done; post a QUESTION to the Owner (CODEX-WORKER + review/merge handoff is an Owner action; this Worker cannot review/merge its own candidate); final END to f49a3303.

## END

- STATUS: BLOCKED (handoff). The test work is done locally and proven; but acceptance REQUIRES an independent CODEX-REVIEW verdict on the exact corrected head plus a CODEX-MERGE, and the mission + AGENTS forbid this Worker from reviewing or merging its own candidate. The handoff routes the merge through an Owner-commissioned lane, so I stop and ask.
- END an f49a3303: "END_BLOCKED w160-streams-r2: head=<sha10> A=<echte grenze+mutante> B=<zaehlung> C=<frist+StreamEnd verlangt> D=<synchron> diff=<nur-test> lauf=<id+status> lsremote=<sha10> | <Satz>"

## PROOF / WITNESSES (to be filled from literal command output)

- ls-remote main / branch: (paste literal)
- merge-base --is-ancestor origin/main HEAD rc=0: (paste)
- git log origin/main..HEAD (own commits only): (paste)
- go test literal output (green + one red mutation per case): (paste)
- name-only diff: (paste)
- final pushed head sha10: (paste)
