# CODEX-REVIEW — baseharbor-node-connector PR #22, round 2

Verdict: **REJECT** — exact head `d934fa7c5227b5fef115ce571703afccca9110de`.

## Candidate identity, imported wire, and files

PR #22 is OPEN/draft against `main`. PR API head and remote `work/r27-node-streams` equal `d934fa7c5227b5fef115ce571703afccca9110de`; remote `main` is `0643d51cc8e934f174fdf6ba875624c112f69235`, an ancestor of the head. Four own commits are included in `main..head`: earlier test commit `6b498a8`, then `8bfe8be`, `f0f4ac9`, and `d934fa7c`.

The actual name-only diff is **four files**, not only the evidence test:

- `internal/connector/stream_evidence_test.go`
- `internal/connector/stream_replay.go`
- `internal/connector/target_access_stream.go`
- `internal/execx/executor.go`

The new test imports `targetaccess.NewHandshakePair` (`stream_evidence_test.go:20,97`) and does not duplicate the handshake ceremony (`newTestCA`/`newTestLeaf` are absent). Existing trust/session files outside the changed stream implementation are blob-identical: `internal/connector/target_access_session.go` `9945b2f2…`, `internal/targetaccess/session.go` `cba4c3e7…`, `session_trust.go` `34ddde35…`, `streams.go` `aba4709a…`, and `testwire.go` `4e9782e3…`. However, `target_access_stream.go` and `stream_replay.go` are modified, and `internal/execx/executor.go` is a new product change outside the task card's reserved paths. Round-2 evidence first says the write set is test-only, then later acknowledges product-side changes; those statements do not match the pushed diff.

## Four cases and mutation probes

I ran `go test ./internal/connector -run '^TestServeLogStreamCase[ABCD]_' -count=1 -v` on the exact head: all four tests passed (4.598s). I then made temporary mutations only in a detached reviewer worktree and restored each file byte-for-byte.

| Case | Candidate test and probe | Result |
|---|---|---|
| A — expiry | Emits 600 data events against the 512-event retention limit and asserts the exact stale-cursor error. Disabling the expiry guard made the test fail with “resume at cursor 1 must be rejected … got nil error.” | Mutation detected. However, the expired resume is `h.access.streams.replay(...)` (`stream_evidence_test.go:484`), not a resume request over a fresh imported mTLS connection; the `replay` helper has no production call site. |
| B — exact replay | Asserts ordered sequences on initial delivery and replay. Duplicating each replay event made the test fail at sequence index 1 (`got 2 want 3`). | Mutation detected. However, replay is called directly on the internal registry at line 568, not through the production reconnect/mTLS path; production stream resumption uses `resume`. |
| C — deadline | Uses a two-second deadline, but accepts `StreamEnd` after only half the requested duration (`stream_evidence_test.go:624-645`). I changed the fake follow process from `sleep 3600` to `sleep 1.2`; the fake exited before the requested deadline, yet the test **passed** in 1.49s. | Mutant survived. A normal early runtime EOF is still accepted as a deadline end. |
| D — cancel/no ghost | It waits for `isDetached` or `closed`, but does not issue a resume request or assert a retired/terminal rejection. I disabled the terminal-session guard in `streamReplayRegistry.resume`; Case D still **passed** in 2.38s. | Mutant survived. The test proves a registry state transition, not that cancellation prevents a subsequent resume from replaying/resurrecting the stream. |

The baseline case D race fix is present (client close precedes polling), and the new side-effect-free `isDetached` probe is committed. Those improvements do not replace a post-cancel resume assertion.

## Gates

Both hosted PR runs are terminal success on this exact SHA: `41977680064` (`Test · Vet · Build`) and `41977680109` (`source`). The workflow also reports `Actual encrypted transport` and `Managed native enrollment` as skipped. The task's bounded real log/PTY smoke is not in the reported evidence: the new harness uses a fake Docker executable, even though it does exercise the imported mTLS test wire. `ls-remote` matches the exact head/base above. The candidate test file contains no `t.Skip` calls.

## Recipe

- **Files:** `internal/connector/stream_evidence_test.go`; for any product changes, first reconcile ownership of `internal/execx/executor.go` with the task owner. Keep the accepted test-wire helper imported; do not copy its handshake ceremony.
- **Change:** run A and B reconnect/resume through a fresh `NewHandshakePair` session and the production `ServeLogStream` request path. In C, require the requested deadline to elapse (with explicit timing anchored to when the deadline is established); reject EOF/StreamEnd from a runtime that exits early. In D, after observing detach/close, submit a real resume request and assert the precise terminal/retired rejection with no replay or reactivation.
- **Test requirement:** one discriminating mutation per case: remove the expiry guard; duplicate or drop a replay frame; make the runtime exit before the deadline; remove the terminal/retired resume guard. Each original test must fail under its corresponding mutation and pass on the corrected exact head. Run focused tests and the bounded real log/PTY smoke required by the card; retain terminal CI evidence on the reviewed SHA.
- **Stop criterion:** reject while C can pass on a pre-deadline runtime exit, D can pass without exercising resume rejection, A/B bypass the production reconnect path, or the unreserved `execx` change lacks an explicit ownership update.

No PR, merge, comment, or card action was taken.
