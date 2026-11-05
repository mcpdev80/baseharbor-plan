# CODEX-REVIEW — BaseHarbor PR #1373, round 6

Verdict: **REJECT** — exact head `d691c3cd2424d34fa39db58150df289cfd01583f`.

## Candidate identity, drift, and gates

PR #1373 is OPEN and ready (not draft), base `develop`; the PR API head and `git ls-remote origin refs/heads/work/r27-execution-journal` both equal `d691c3cd2424d34fa39db58150df289cfd01583f`. Remote `develop` is `42bfcb1cb481c9e37ecd6ce30580e27829284113`. The candidate is a single-child commit on `2b997f3c19e8677a019265fe1a74132d3024ead6`, which had incorporated develop `24c7d0492f34e58c2a6be505ba80b8bdfb151cb7`; current develop has since advanced by `42bfcb1c` (`fix: enforce state owner and complete app edit lifecycle (#1347)`). The current develop tip is therefore not an ancestor of this candidate; this is listed as base drift, not treated as a technical verdict by itself.

The exact round-6 name-only delta from `2b997f3c` is two test files: `internal/machinehttp/execution_request_identity_test.go` and `internal/machinehttp/handler_test.go`. No product handler or workflow file changed in this round. The requested hosted run `41998165081` is terminal `completed/success` on this exact SHA. Its `PR Selected Checks`, trusted plan, source format, workflow policy, focused Python, Go build, Go unit tests, and Go vet jobs passed; runtime/consumer jobs shown as skipped.

## Own race-20 and source inspection

On a detached worktree at the exact head, I ran:

```text
GOCACHE=<review-owned workspace cache> TMPDIR=<review-owned workspace temp> GOPATH=/tmp/codex-r1373f-gopath go test -race ./internal/machinehttp -run 'TestTerminalStateCommittedBefore202Response|TestTerminalStateBackgroundMutationFails|TestRunExecutionPropagatesTerminalPersistFailure|TestRequestIdentityIndexSurvivesJournalReopen|TestCreateReconnectIdenticalReturnsSameOperation|TestReconnectReturnsSameOperation' -count=20
```

Result: **PASS**, `ok github.com/mcpdev80/baseharbor/internal/machinehttp 14.375s`. Two initial attempts failed before test execution because the default cache was read-only and then the shared `/tmp` returned `disk quota exceeded`; the successful run used only the reviewer-owned cache/temp paths above.

A source grep and read of all `internal/machinehttp/*.go` found no `time.Sleep` call, sleep/poll loop, or `waitForCondition` implementation in the test code. Matches for “poll”/“sleep” are explanatory comments. The only ticker hit is the production SSE heartbeat (`handler.go:284`), not a test synchronization path. `git diff --check` is clean and the reviewer worktree is clean after mutation restoration.

## Background-execution mutation

I changed `handler.go:215` in the disposable reviewer worktree from synchronous `runErr := h.runExecution(...)` to a fire-and-forget `go h.runExecution(...)` and ran the candidate end-state tests. The mutation was detected in repeated runs, but **it is not reliably detected**:

- `TestTerminalStateCommittedBefore202Response -count=1` **passed under the background mutation** (surviving mutant).
- The same test with `-count=20` returned red with multiple `no terminal event recorded on 202 tail` failures, while other repetitions passed.
- `TestTerminalStateBackgroundMutationFails -count=20` also returned red, but the fast executor sometimes completed before the assertion observed the 202 tail.

This exposes a timing race in the evidence itself. The simple executor may finish in the background before the test reads history; therefore a single run can accept the exact asynchronous behavior the assertion is intended to exclude. A red aggregate does not cure the surviving individual mutant. The handler's synchronous call is correct at the candidate, but its regression evidence does not yet reliably distinguish that behavior from fire-and-forget execution.

## Recipe

- **File:** `internal/machinehttp/execution_request_identity_test.go` (and only its helper/call sites as needed).
- **Change:** make the end-state regression deterministic under a backgrounded handler. Use a controlled executor/persistence barrier and explicit start, handler-return, release, and terminal-commit channels so the test can assert the required ordering without relying on a very fast executor winning a scheduler race. Keep bounded timeouts only as failure bounds, not as a polling mechanism.
- **Test requirement:** on the unmodified candidate, rerun the affected identity/end-state set with `-race -count=20` and require green. Under the exact `go h.runExecution(...)` mutation, the focused original end-state assertion must fail even at `-count=1` and remain red across all 20 repetitions; restore the candidate and verify it passes. Preserve the sleep/poll-free source inspection and terminal hosted evidence for the corrected SHA.
- **Stop criterion:** reject while the asynchronous mutant can pass any single end-state assertion or survive any repetition, while race-20 baseline is red, or while a sleep/poll timing loop returns to the test synchronization path.

No PR, merge, comment, or task-card action was taken.
