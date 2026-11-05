# CODEX-REVIEW — baseharbor-node-connector PR #22, round 3

Verdict: **REJECT** — exact head `dc63758f37d4aa81904855d83457ad8077724695`.

## Candidate identity and changed surface

The requested mission file `coordinator/missions/codex-r22c.txt` is absent from this checkout; I followed the user-provided scope and the round-3 artifact. Read-only identity checks show remote `main` at `0643d51cc8e934f174fdf6ba875624c112f69235` and `work/r27-node-streams` at the exact candidate SHA above. The round-3 artifact reports terminal-success PR runs `41989934411` (Test · Vet · Build) and `41989934361` (source); the native-enrollment and actual-encrypted-transport jobs are skipped.

The `main..head` name-only diff is four files:

- `internal/connector/stream_evidence_test.go`
- `internal/connector/stream_replay.go`
- `internal/connector/target_access_stream.go`
- `internal/execx/executor.go`

The task's bounded write reservation is `internal/connector/target_access_stream.go`, `stream_replay.go`, `internal/targetaccess/streams.go`, and component tests. `internal/execx/executor.go` is outside that reservation and has product behavior changes (process group termination, `WaitDelay`, and pipe close semantics); no ownership amendment is evidenced. This also contradicts round-3's assertion that the round-3 write surface is only the evidence test: compared with round-2 head `d934fa7c5227b5fef115ce571703afccca9110de`, round-3 changes `stream_evidence_test.go` only, but the complete candidate still includes the earlier out-of-scope source changes.

The trusted handshake helper is imported from main, not copied. `internal/targetaccess/testwire.go` is byte-identical at base and candidate (blob `4e9782e39adabce875a5dfaeef78c7a90666a353`); `NewHandshakePair` is called at `stream_evidence_test.go:97,154,202`. The existing trust/session-chain files also remain identical: `internal/targetaccess/session.go` `cba4c3e7821916bc517d0167a1b720817e9662df`; `session_trust.go` `34ddde35812253e460c4b10ec1d4e3a9d8169f29`; `streams.go` `aba4709aac15f67a1a7487c6752c02a5a6c8894b`; `internal/connector/target_access_session.go` `9945b2f223a317b867b494bdc8b240760feb5844`.

## Technical checks

The exact-head focused cases A–D passed in the reviewer run. Round-3's two requested mutants are reported red: early fake-runtime exit in C yields an early-`StreamEnd` failure; disabling the cursor-age guard in D yields the asserted silent-resume failure. Those results do not close the inherited A/B findings, and D's exercised rejection does not establish the stated cancellation guarantee:

- **A — cursor expiry:** `stream_evidence_test.go:482-489` uses `h.access.streams.replay("stream-a", 1)` to test stale cursor rejection; lines `492+` use that same internal helper for in-window replay. No fresh-line `ResumeAfter` request traverses the production `ServeLogStream` resume path.
- **B — exact replay:** `stream_evidence_test.go:566-578` likewise obtains replay directly from `h.access.streams.replay`, rather than exercising reconnect over a fresh handshake and production resume request. The sequence assertions are useful but do not prove production reconnect behavior.
- **C — deadline:** the new assertion requires `StreamEnd` after approximately the full requested deadline and rejects early EOF/StreamError (`stream_evidence_test.go:591-660`). The round-3 early-exit mutation is discriminating for that assertion.
- **D — cancellation/no ghost:** the test drains the 600-line follow to its natural terminal completion before closing the client (`stream_evidence_test.go:742-750`). It then resumes at cursor `1` (`:791`), which is stale after 600 lines. `stream_replay.go:78-82` rejects that cursor on age alone; it does not reject a closed stream as such. Consequently the fresh-wire request and age-gate mutation prove stale-cursor rejection, not that cancelling an active follow prevents replay/resurrection of its retained history. The mutant targets the age gate, not a cancellation/retirement guard. `resumeOverFreshLine` also returns an empty error string when its reader fails (`:677-719`), so it does not distinguish all transport failures from an accepted response by itself.

The round-3 artifact records no bounded real log/PTY smoke. The harness's fake Docker and `net.Pipe` mTLS exercise do not supply that task-required runtime smoke; the skipped native jobs do not fill the gap.

## Recipe

- **Files:** `internal/connector/stream_evidence_test.go`; reconcile ownership for `internal/execx/executor.go` before retaining that out-of-reservation product change.
- **Change:** route A's expired and in-window resumes and B's exact replay through a fresh imported `NewHandshakePair` connection and `ServeLogStream` with `ResumeAfter`. For D, cancel while the follow is still active, wait for detach, then resume using a cursor still inside retained history; require an explicit cancellation/retirement rejection and prove no event replay or reactivation. Make the helper distinguish a returned protocol event, the exact server rejection, and transport/read failure. Keep C's full-deadline and early-exit discriminator.
- **Test requirement:** each corrected A–D test passes through the real `ServeLogStream` chain; A/B mutations (remove stale-cursor guard; duplicate/drop replay frame) and C/D mutations (early runtime EOF; remove cancellation/retirement resume rejection) each make their corresponding original test fail. Run the task-required bounded real log/PTY smoke and record its actual environment/result. Recheck exact-SHA terminal required gates.
- **Stop criterion:** reject while A/B bypass production resume, D cancels only after natural terminal completion or accepts a stale-cursor error as proof of cancellation semantics, the out-of-scope `execx` change lacks documented ownership, or the required real log/PTY smoke is absent.

No PR, merge, comment, or card action was taken.
