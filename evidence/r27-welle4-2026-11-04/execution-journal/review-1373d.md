# CODEX-REVIEW — PR #1373, round 4 head

Verdict: **REJECT** — reviewed exact head `52e972fdbd25aa6dde5a82b0be55c064f5a2065d`.

## Candidate and drift

PR #1373 is open and its API head matches `52e972fdbd25aa6dde5a82b0be55c064f5a2065d`. This is a merge commit with parents `43b14463c498d73cd98c577844ee32612bba526e` and `512dcd721ac3fb739bfd4cb0b990fd68d6794762`. Its change set against the candidate base is restricted to seven `internal/machinehttp/` files: the request identity, reconnect and duplicate tests, new persist-failure test, handler, handler tests, and store. No workflow or unrelated path is in that change set.

Current remote develop is `24c7d0492f34e58c2a6be505ba80b8bdfb151cb7`, which is ahead of the candidate base. Drift after base `512dcd72` is `3b5974ca` (#1382), `1a84726d` (#1369), `c762022e` (#1381), `0476164a` (#1362), and `24c7d049` (#1371). This is listed as requested; it is not the finding or a recipe requirement.

`ls-remote` measured develop `24c7d0492f34e58c2a6be505ba80b8bdfb151cb7` and `work/r27-execution-journal` `52e972fdbd25aa6dde5a82b0be55c064f5a2065d`, matching the PR head.

## Technical checks

- End-state test: `internal/machinehttp/execution_request_identity_test.go:199-257` observes a terminal event after the request and checks the terminal journal line. I ran the relevant tests at this head: `TestTerminalStateCommittedBefore202Response`, `TestTerminalStateBackgroundMutationFails`, `TestRunExecutionPropagatesTerminalPersistFailure`, and `TestRequestIdentityIndexSurvivesJournalReopen`; all passed.
- Own mutation probe: in a disposable worktree only, I changed the handler call to `go h.runExecution(...)` and ran the two end-state tests 20 times. `TestTerminalStateCommittedBefore202Response` failed all 20 times with “no terminal event recorded on 202 tail”; restoring the synchronous call left the worktree clean. Thus the assertion is not vacuous.
- Persist failure: `execution_persist_failure_test.go:29-66` injects a terminal journal append failure after `start`, requires a non-nil error from `runExecution`, and ensures state is not reported as succeeded. It passes on the candidate.
- Sleep-free requirement is not met: `execution_request_identity_test.go:22-50` calls itself “no time.Sleep” but loops with `time.Sleep(time.Millisecond)` at line 40. The new terminal test invokes that helper at lines 243-249 after checking its event; other tests in the same new file also use it. This is unnecessary polling in the required verification path.
- Hosted run `41938868155` is terminal success on this exact SHA; `PR Selected Checks` is success (integration 15368). A later workflow-dispatch run `41940701025` is terminal failure in `validate`; PR run `41938868155` remains the successful PR event.

## Recipe

- **Files:** `internal/machinehttp/execution_request_identity_test.go` and its callers.
- **Change:** remove the sleep-based `waitForCondition` polling helper. Use a channel/event ordering that proves executor completion and terminal journal persistence before the handler returns; read the journal directly after the already-observed terminal commit.
- **Test requirement:** focused tests pass repeatedly under `-race -count=20`; reapply `go h.runExecution(...)` in an isolated worktree and verify the original end-state test reliably fails, then restore and verify a clean diff.
- **Stop criterion:** if a backgrounded execution can pass the end-state check, or any required assertion still relies on sleeping/polling, reject.

No PR, branch, or card action was taken.
