# CODEX-REVIEW — node streams, round 7

- Mission: `coordinator/missions/codex-r22g.txt`
- Role: CODEX-REVIEW (read-only; no PR action)
- Repository: `mcpdev80/baseharbor-node-connector`
- PR: #22, branch `work/r27-node-streams`
- Reviewed head: `2e285a771ed8adc30ccea8b4842cafad28815dd9`
- Base `main`: `0643d51cc8e934f174fdf6ba875624c112f69235`
- Review date: 2026-11-06
- Verdict: **ACCEPT**

## Candidate identity, scope, and ancestry

`git ls-remote origin` reported `2e285a771ed8adc30ccea8b4842cafad28815dd9` for
`refs/heads/work/r27-node-streams`, matching the open PR #22 head. Main was
`0643d51cc8e934f174fdf6ba875624c112f69235`; `git merge-base --is-ancestor origin/main HEAD`
returned 0.

The name-only diff from main is exactly:

- `internal/connector/stream_evidence_test.go`
- `internal/connector/stream_replay.go`
- `internal/connector/target_access_stream.go`
- `internal/execx/executor.go`

The three state-owner blobs are unchanged from main to candidate:

- `internal/targetaccess/session.go`: `cba4c3e7821916bc517d0167a1b720817e9662df`
- `internal/targetaccess/session_trust.go`: `34ddde35812253e460c4b10ec1d4e3a9d8169f29`
- `internal/targetaccess/session_trust_test.go`: `821f85f6a7453b69cb8b82bacc7a99df387542b0`

## 22f failure path and round-7 correction

Compared `internal/execx/executor.go` on this head with 22f (`25a24667ebf087cd9c9f9fc3d24b49c436579569`). The old implementation discarded `cmd.Wait()` and always closed the pipe with `io.EOF`. The candidate preserves the wait error unless the child succeeded or `isContextKilled(waitErr)` recognizes a context-driven signal termination. `ServeLogStream` therefore sees a genuine non-zero child exit as a `StreamError`; context cancellation/deadline still produces clean EOF and `StreamEnd`.

The new production-path cell is `TestServeLogStreamCaseE_FailureSurfacesNotEOF_ContextCancelStaysEOF`; its converse is `TestServeLogStreamCaseE_Converse_ContextCancelEndsCleanly`. Personally ran both on the exact candidate:

```text
go test -count=1 -timeout 5m ./internal/connector -run '^TestServeLogStreamCaseE_'
PASS (1.100s)
```

The tests drive `ServeLogStream` with fake runtime children: the first prints two lines then exits non-zero, and requires the terminal event to be `StreamError`; the converse ends by context deadline and requires a clean `StreamEnd`.

## EOF-mapping mutant and counterprobe

In isolated worktree `/tmp/opencode/codex-r22g`, mutated only the EOF discriminator:

```diff
- if waitErr == nil || isContextKilled(waitErr) {
+ if true {
```

This restores the old unconditional EOF behavior. `TestServeLogStreamCaseE_FailureSurfacesNotEOF_ContextCancelStaysEOF` turned **RED** with terminal type `end` instead of `StreamError`. The converse `TestServeLogStreamCaseE_Converse_ContextCancelEndsCleanly` stayed **GREEN** under the mutant. I restored `executor.go`; `git diff --quiet` returned 0.

## Case A–E regressions and race ensemble

On the restored exact candidate, personally ran:

```text
go test -count=1 -timeout 5m ./internal/connector -run '^TestServeLogStreamCase[ABCDE]'
PASS (64.722s)

go test -race -count=20 -timeout 25m ./internal/connector -run '^TestServeLogStreamCase'
PASS: ok github.com/mcpdev80/baseharbor-node-connector/internal/connector 1306.492s, exit 0
```

The case-family regression run covers the previously reviewed A–D cases and both E directions. The repeated race run also completed within the mission timeout. No product source was left changed in the isolated worktree.

## Hosted runs

Both required hosted runs were terminal success at the exact candidate SHA:

- `42159456055` — CI · Node Connector Quality · 22/merge; Test · Vet · Build succeeded.
- `42159456071` — Connector Source Conformance; source succeeded; runtime matrix legs were skipped by path rules.

## Conclusion

The real child-failure path now preserves a failure as `StreamError`, while context cancellation remains a clean stream end. The EOF-remapping mutant turns the child-failure cell red and leaves the cancellation counterprobe green. Case A–E regressions, race-20, both exact-head hosted runs, ancestry, and state-owner blob checks pass. No PR action was taken.
