# CODEX-REVIEW — PR #1373 (round 5, read-only)

Verdict: **REJECT** — exact candidate `2b997f3c19e8677a019265fe1a74132d3024ead6`.

## Candidate and drift

PR #1373 is open and its API head matches the requested SHA. `ls-remote` reports `develop=24c7d0492f34e58c2a6be505ba80b8bdfb151cb7` and `work/r27-execution-journal=2b997f3c19e8677a019265fe1a74132d3024ead6`. This is a merge commit whose second parent is the current develop head; `develop` is an ancestor. The PR change set is seven files, all under `internal/machinehttp/`: four execution tests, `handler.go`, `handler_test.go`, and `store.go`. No `.github` path is changed.

Since the prior reviewed base `512dcd721ac3fb739bfd4cb0b990fd68d6794762`, the measured develop drift is `3b5974ca` (#1382), `1a84726d` (#1369), `c762022e` (#1381), `0476164a` (#1362), and `24c7d049` (#1371). That drift is incorporated by the merge parent and is listed, not treated as a recipe requirement.

## Checks and mutation

At the exact SHA I ran:

`go test -race ./internal/machinehttp -run 'TestTerminalStateCommittedBefore202Response|TestTerminalStateBackgroundMutationFails|TestRunExecutionPropagatesTerminalPersistFailure|TestRequestIdentityIndexSurvivesJournalReopen' -count=20`

Result: **PASS** (`ok`, race enabled, count 20). I then changed the handler's synchronous `h.runExecution(...)` call to a background goroutine in disposable worktree `/tmp/review1373e` and ran the original end-state test with `-count=20`. It failed all 20 invocations with `no terminal event recorded on 202 tail`. The mutation was restored; the worktree has no remaining diff.

The independent required sleep-free point is still not met. `internal/machinehttp/execution_request_identity_test.go:22-50` retains `waitForCondition`; its loop calls `time.Sleep(time.Millisecond)` at line 40 and it is used in the request-identity/reconnect tests. The helper's comment says “no time.Sleep” but the implementation polls. The successful end-state mutation probe does not cure this remaining timing-based synchronization.

Hosted run `41981442440` is terminal success at the exact candidate SHA, including `PR Selected Checks` success, Go unit tests, build, vet, source format and trusted plan. The gate result does not waive the source-level sleep-free acceptance point.

## Recipe

- **Files:** `internal/machinehttp/execution_request_identity_test.go` and callers of `waitForCondition`.
- **Change:** replace the polling/sleep helper with explicit channel/event synchronization that signals the exact executor or journal transition each test waits for. Remove the misleading “no time.Sleep” comment only after no sleep/poll loop remains.
- **Test requirement:** rerun the affected tests with `-race -count=20`; repeat the background-execution mutation and require the original end-state assertion to fail, then verify the synchronous control passes and the mutation worktree is clean.
- **Stop criterion:** any required assertion still depends on sleep/poll timing, or the asynchronous mutant passes the original end-state test.

No PR, branch, or card action was taken. The requested mission file was absent from this checkout; the prior #1373 review recipes and the owner's stated round-5 requirements were used.
