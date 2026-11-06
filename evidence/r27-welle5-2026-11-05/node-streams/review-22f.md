# CODEX-REVIEW 22f — node streams, round 6

- Mission: `coordinator/missions/codex-r22f.txt`
- Role: CODEX-REVIEW (read-only; no PR action)
- Repository: `mcpdev80/baseharbor-node-connector`
- PR: #22, branch `work/r27-node-streams`
- Reviewed head: `25a24667ebf087cd9c9f9fc3d24b49c436579569`
- Base `main`: `0643d51cc8e934f174fdf6ba875624c112f69235`
- Review date: 2026-11-06
- Verdict: **REJECT**

## Scope and candidate identity

`git ls-remote origin` reported `25a24667ebf087cd9c9f9fc3d24b49c436579569` for
`refs/heads/work/r27-node-streams`, exactly matching the PR head. It reported
`0643d51cc8e934f174fdf6ba875624c112f69235` for `refs/heads/main`.
`git merge-base --is-ancestor origin/main origin/work/r27-node-streams` returned 0.
The name-only diff from `origin/main` to the candidate is:

- `internal/connector/stream_evidence_test.go`
- `internal/connector/stream_replay.go`
- `internal/connector/target_access_stream.go`
- `internal/execx/executor.go`

No files were changed by this review. The guard mutant ran in an isolated detached
worktree and was restored; its source tree was clean afterward. No VM or Compose path
was used.

## Case A live attachment barrier

The test establishes an active follow on one mTLS line, waits for the attach barrier
(`isDetached` observes the registered, open stream), and confirms the ready and first
data frames on the still-live follow connection. Before the follow terminates, it
attempts resume on a fresh line and requires the exact rejection
`stream is still attached to another transport`; it also checks the concurrent-active
rejection. The original follow remains live for the assertions. This exercises the
production `ServeLogStream` path rather than calling the replay helper directly.

## Guard mutation discrimination

In `/tmp/opencode/codex-r22f-mutant`, I removed the actual `stream.active &&
!stream.closed` rejection guard from `internal/connector/stream_replay.go` and ran:

- `go test -count=1 -timeout 5m ./internal/connector -run '^TestServeLogStreamCaseA_'` —
  **FAIL as required**. Case A reported that resume over a fresh line while follow was
  live returned nil instead of the exact still-attached error; the follow ended on its
  own, proving the missing guard was detected.
- `go test -count=1 -timeout 5m ./internal/connector -run '^TestServeLogStreamCase[BCD]_'` —
  **PASS** (3.659s).

The guard was restored; the isolated worktree was clean (`git diff --quiet`, rc=0).

## Harness hang correction

The round-6 test harness fixes the net.Pipe terminal-read hang in the test file: the
follow reader closes both raw endpoints when it observes EOF, retirement cancels the
session context before endpoint closure, and bounded cleanup waits for serve quiescence
before touching a leaked line. The wake-channel frame reader loops across close/append
races and per-line reads have an explicit bound. This addresses the parked TLS reader
and test goroutine described in the prior timeout dumps; it is a harness correction,
not a workaround in production code.

## Own race-20 run

On the restored exact candidate, I ran:

```text
GOCACHE=/home/marcel/dev/baseharbor-ecosystem/.gocache
GOMODCACHE=/home/marcel/dev/baseharbor-ecosystem/.gomodcache
GOTMPDIR=/tmp/opencode/codex-r22f-race20
go test -race -count=20 -timeout 25m ./internal/connector -run '^TestServeLogStreamCase'
```

Result: `ok github.com/mcpdev80/baseharbor-node-connector/internal/connector 1285.395s`,
exit 0. The required run was observed to terminal by this review session.

## Hosted checks and state-owner blobs

At the exact reviewed head, hosted run `42146364305` (Connector Source Conformance) was
terminal `completed / success`; its source job succeeded and runtime matrix legs were
skipped by path rules. Hosted run `42146364376` (CI Node Connector Quality) was terminal
`completed / success`; `Test · Vet · Build` succeeded. These were independently checked
at the exact candidate SHA.

The state-owner files are unchanged from `origin/main` to the candidate:

- `internal/targetaccess/session.go` — blob
  `cba4c3e7821916bc517d0167a1b720817e9662df`
- `internal/targetaccess/session_trust.go` — blob
  `34ddde35812253e460c4b10ec1d4e3a9d8169f29`
- `internal/targetaccess/session_trust_test.go` — blob
  `821f85f6a7453b69cb8b82bacc7a99df387542b0`

## Blocking finding: child failures become successful stream ends

`internal/execx/executor.go` changes `Runner.Stream` from closing the pipe with
`cmd.Wait()`'s error to discarding that error and unconditionally closing with
`io.EOF`. `ServeLogStream` explicitly maps `io.EOF` to `StreamEnd` and any other reader
error to `StreamError`. As a result, a runtime log subprocess that exits non-zero for a
real failure is now reported to the client as a normal successful end. The stated
context-cancellation rationale only justifies mapping cancellation to clean EOF; it
does not justify hiding unrelated command failures. This regresses the existing runtime
failure signal and blocks acceptance even though the listed stream evidence and CI are
green.

### Required correction recipe

In `internal/execx/executor.go`, preserve `cmd.Wait()`'s error for ordinary process
termination. Map it to `io.EOF` only when the stream context was canceled or expired;
otherwise close the writer with the actual wait error. Add a focused regression test that
proves a child non-zero exit remains a stream error while context cancellation remains a
clean terminal end. Re-run the relevant connector and execx tests, then the required
hosted gates on the new exact head. Stop if the task owner has not authorized any needed
write-set expansion.

## Repository-rule compliance

This was a read-only CODEX-REVIEW. I made no product changes, did not alter the PR, and
took no merge action. The guard mutation was isolated and fully reverted. The review
artifacts and evidence describe the exact candidate SHA above.

## Conclusion

Case A now proves a live, barriered attachment rejection; the guard mutant is
discriminated (A red, B/C/D green); the harness hang fix is substantive; my own race-20
run, both required hosted runs, ancestry, and state-owner blob checks are green. However,
the unconditional EOF conversion suppresses real runtime subprocess failures. **REJECT**
until that failure path is corrected and re-proven.
