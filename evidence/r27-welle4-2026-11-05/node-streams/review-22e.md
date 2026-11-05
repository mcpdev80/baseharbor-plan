# CODEX-REVIEW — connector PR #22, round 5

## Candidate and scope

- PR: [#22](https://github.com/mcpdev80/baseharbor-node-connector/pull/22), open against `main`.
- Reviewed head: `52db6dc1c6417b90fb342ebc6f79fdda01bd1609`.
- PR head, `git ls-remote` for `work/r27-node-streams`, and the mission SHA matched.
- Name-only diff from `main`: `internal/connector/stream_evidence_test.go`, `internal/connector/stream_replay.go`, `internal/connector/target_access_stream.go`, `internal/execx/executor.go`.
- Hosted runs [42058515798](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/42058515798) and [42058515839](https://github.com/mcpdev80/baseharbor-node-connector/actions/runs/42058515839) are terminal `success`, both at the reviewed head.

## Verification

- Exact mixed A–D command, run by this reviewer: `go test -race -count=20 ./internal/connector -run '^TestServeLogStreamCase[ABCD]_'` — `ok github.com/mcpdev80/baseharbor-node-connector/internal/connector 122.850s`.
- A/B chain inspection: `newHarness`/`newBoundedHarness` use `targetaccess.NewHandshakePair`; `resumeOverWire` creates a fresh pair and drives `ResumeAfter` through `h.access.ServeLogStream`. The cases assert wire events and the server-side result. `rg 'h\.access\.streams\.replay\(' internal/connector/stream_evidence_test.go` returned no matches (`NULL`).
- Trust/session blobs compared with `main` are unchanged: `internal/targetaccess/session.go` `cba4c3e7821916bc517d0167a1b720817e9662df`; `internal/targetaccess/session_trust.go` `34ddde35812253e460c4b10ec1d4e3a9d8169f29`; `internal/targetaccess/session_trust_test.go` `821f85f6a7453b69cb8b82bacc7a99df387542b0`.
- `internal/execx/executor.go` changes only the streaming pipe close after `cmd.Wait`: it closes with `io.EOF`, so a context-cancelled child ends the consumer stream as EOF and `ServeLogStream` emits terminal `StreamEnd` rather than forwarding the process-kill error. This behavior is exercised by case C's real child process path.

## Single-run mutants

Each mutation was isolated in a separate reviewer scratch worktree at this exact SHA; the candidate worktree remained unchanged.

- Stale-guard removed (`if stream.active && !stream.closed`): **survived**. Case A passed: `ok .../internal/connector 5.249s`. Case A drains its initial stream through terminal `StreamEnd` before issuing either resume, so the stream is no longer attached when the guard is tested. This does not prove the still-attached guard.
- Duplicate-allow (`event.Sequence > after` changed to `>=`): red as expected: `case b: wire replay must begin with data (a resume re-sends retained data, not a ready frame), got "ready"`.
- Premature-end witness (case C fake follow child changed from `sleep 3600` to `sleep 0.026`): red as expected: `case c: StreamEnd at 63.05153ms before the requested deadline 2s (premature runtime end, not a deadline end)`.
- Age gate removed from `resume`: red as expected: `case d: resume not rejected with the documented cursor-expiry reason, got "write pipe: i/o timeout"`.

The round-5 report's claim that removing the still-attached guard makes case A reject its cursor-1 request is not borne out: the reviewer-run mutant passes. The cursor-1 request is rejected by the separate age gate, and A only attempts resume after the first stream is terminal.

## Verdict and correction recipe

**REJECT.** The overall race ensemble and hosted runs pass, A/B use the real handshake and `ServeLogStream` resume path, and three discriminating mutants go red. The still-attached guard lacks a failing mutant proof. Change the A scenario to hold a follow stream live, issue a resume on a fresh mTLS line before that stream ends, and assert the exact still-attached rejection. Use a deterministic barrier to establish that the original stream is still active at the resume. Then run the stale-guard-removed mutant once and require a named red assertion, and repeat the exact race-20 ensemble and required exact-head hosted verification if the candidate SHA changes.

## Repo-rule compliance

SHA-exact, read-only review of the candidate. All local runs and mutations used isolated reviewer worktrees. No product source, PR, branch, or task card was changed; no PR action was taken. This review record is the only requested persistent write.
