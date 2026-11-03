# ci-authority qualify-1: execution-journal slice (executionStore fail-closed)

- Task: `t-20261022-r27-ci-authority` — Deferred trusted CI readiness: authority
- Worker lane: `w41-ci-authority` · Coordinator: `f49a3303`
- Date: 2026-11-03
- Repo: `mcpdev80/baseharbor`
- Worktree: `/tmp/opencode/w41-ci-authority-wt` branch `work/r27-ci-authority-ab`
- Base (origin/develop) `1706272c` (r27 authority-contract #1348)
- Write-set: `internal/**` + `testsupport/**` test files only (mission rule; `.github/scripts` untouched)

## PLAN (board + JSON live board in sync)

1. ✅ Fetch origin develop + worktree `work/r27-ci-authority-ab` at `/tmp/opencode/w41-ci-authority-wt` (FIRST ACTION per mission).
2. ⏳ Read mission + card + current-wave slice evidence; map 8 slices to production packages.
3. ⏳ Baseline: `go build ./...` + targeted package tests all green.
4. ⏳ Gap analysis: find a gate-less production path with no direct fail-closed fixture.
5. ⏳ Author one bounded domain-local fixture proving the execution-journal slice delivers real results.
6. ⏳ Proof: run new test; confirm it FAILS when the fail-closed guard is removed (live test), then restore.
7. ⏳ repo-rule compliance (write-set restricted, no skip-by-env).
8. ⏳ Merge develop (drift), ancestry rc=0, ls-remote SHA, `go build ./...`, push FF, ls-remote==head, DRAFT PR.
9. ⏳ Write this evidence, tick board, post END_DONE to f49a3303.

## SLICE → PACKAGE MAP (card covered slices)

- authority-contract → `internal/coreinstallation/authority.go` (+ `coreinstallation/authority_test.go` exists, thorough)
- mutation-lock → `internal/coreinstallation/lifecycle_lock.go` (covered by `lifecycle_lock_test.go`)
- state-owner → `internal/coreinstallation/authority.go` VerifyConnectionIdentity (covered)
- execution-journal → `internal/machinehttp/store.go` executionStore (create/start/progress/succeed/fail) — **DIRECT GAP**
- journal-wiring → `internal/machinehttp/handler.go` + `streams.go` (SSE + stream wiring)
- app-binding → `internal/application/identity_binding*.go` (covered by `identity_binding_credentials_test.go`)
- candidate-ingress → `internal/providerconformance/` (covered by `conformance_test.go`)
- management-host → `internal/controlplaneruntime/server.go` Run/Validate (covered by `server_test.go`)

## TASK / CONTRACT

Qualify only the missing domain-specific trusted selection/execution/verification for accepted product interfaces (2026-11-03 Owner directive: product-side test/fixture/result handling only; `.github/**`, `scripts/**` are untouchable owner-CI stream). Actual selected checks must execute and FAIL on missing/invalid required coverage; failed/skipped/missing must not be papered over. Only test/fixture files under `internal/**` and `testsupport/**`.

## GAP ANALYSIS (why execution-journal)

Baseline (`go build ./...` + `go test` on coreinstallation, installauthority, machinehttp, application, controlplaneruntime, providerconformance) is green. Of the 8 covered slices, 7 already ship direct domain-local fixtures that prove fail-closed behavior:

- authority-contract / state-owner: `coreinstallation/authority_test.go` (48 funcs, incl. foreign-identity-fails-closed, missing-issuer-fails-closed, revoked-missing-crl-fails-closed).
- mutation-lock: `coreinstallation/lifecycle_lock_test.go` + `_regression_test.go` (foreign-root rejected, non-private rejected, empty-root-fails-closed).
- app-binding: `application/identity_binding_credentials_test.go` (divergent/missing credential → verified; no leak).
- candidate-ingress: `providerconformance/*_test.go` (verify-failure never ready, drift repair, destroy enforces ownership).
- management-host: `controlplaneruntime/server_test.go`.
- journal-wiring: `machinehttp/{browser_security,handler,event_heartbeat,terminal}_test.go` exercise the HTTP/SSE + stream wiring and fail-closed actor/identity checks.

The **execution-journal** slice (`internal/machinehttp/store.go`, `executionStore`) is the one slice whose durable execution journal — `create → start → progress → succeed/fail` and the fail-closed read on an unknown execution ID — is **only reachable indirectly** through the SSE handler flow in `handler_test.go`. No domain-local fixture drives the `executionStore` directly. The `Execution.Validate()` contract (succeeded requires a structured result; failed requires a structured error; invalid state rejected; unknown ID must not fabricate) is the real "trusted execution journal" invariant and has no direct assertion. That is a gate-less production path with no direct coverage → the exact "missing/defective => visible error" gap this lane must close.

## FIXTURE (domain-local, execution-journal)

New file `internal/machinehttp/execution_journal_test.go` (package `machinehttp`, i.e. `internal/**`):

- A fixture that drives the `executionStore` through random valid state sequences via the public executor-facing flow, asserting:
  1. durable create → running → succeeded with a structured result;
  2. durable create → running → failed with a structured error;
  3. a `progress`/`succeed`/`fail` on an **unknown** execution ID fails closed (returns error, never fabricates a record);
  4. an `Execution` in succeeded state without a structured result is rejected by `Execution.Validate()`; a failed state without an error is rejected.
- Run deterministically (seeded RNG) so it is flake-free.

## repo-rule compliance

- Write-set: exactly one new test file under `internal/**`. No production code touched.
- `.github/**` and `scripts/**` untouched — write-set grep clean (see proof below).
- No `git add -A`; targeted add only.
- No skip-by-env trick; fail-closed is asserted by the test, not by environment perms.

## PROOF (live-test + green runs)

Baseline (on origin/develop @ `1706272c`, worktree `work/r27-ci-authority-ab`):
- `go build ./...` -> exit 0 (clean).
- `go test` green on the other qualified slices:
  - `./internal/coreinstallation` ok, `./internal/installauthority` ok,
  - `./internal/machinehttp` ok, `./internal/application` ok,
  - `./internal/controlplaneruntime` ok, `./internal/providerconformance` ok.

New fixture (`internal/machinehttp/execution_journal_test.go`, package `machinehttp`):
Command: `TMPDIR=/tmp GOCACHE=/tmp/opencode/gc go test ./internal/machinehttp/ -run 'TestExecutionJournal' -count=1 -v`
Result:
```
--- PASS: TestExecutionJournalDurableTransitions (0.00s)
--- PASS: TestExecutionJournalFailsClosedOnUnknownID (0.00s)
--- PASS: TestExecutionJournalRejectsInvalidContractStates (0.00s)
--- PASS: TestExecutionJournalBoundedSequenceFuzz (0.00s)
ok  	github.com/mcpdev80/baseharbor/internal/machinehttp	0.003s
```

Live-test (the test actually guards the invariant):
- Temporarily mutated `internal/machinehttp/store.go` `update()` to silently fabricate a
  record for an unknown execution ID (simulating a buggy durable journal).
- `go test ./internal/machinehttp/ -run 'TestExecutionJournal'` -> **FAIL, exit 1**:
  ```
  --- FAIL: TestExecutionJournalFailsClosedOnUnknownID (0.00s)
      execution_journal_test.go:141: progress on unknown execution ID did not fail closed
  --- FAIL: TestExecutionJournalBoundedSequenceFuzz (0.00s)
      execution_journal_test.go:212: step 0: progress on unknown ID did not fail closed
  ```
- Restored `store.go` to the original — byte-identical to origin/develop
  (`git diff origin/develop -- internal/machinehttp/store.go` empty). Only the new test
  file is added. `go build ./...` green again; full `machinehttp` package green.

This proves the fixture is not pass-by-env / not a skip: it fails the moment the
trusted-journal fail-closed invariant is broken, and passes only against the real
production journal.

## PR / PUSH / ANCESTRY

- Branch: `work/r27-ci-authority-ab` @ `159054c2f68a94c9e244d38b8e28e248c85b3f2e`
- `git ls-remote origin work/r27-ci-authority-ab` == `159054c2...` (== head).
- `git merge-base --is-ancestor origin/develop HEAD` -> rc=0 (develop contained).
- FF push: exit 0.
- DRAFT PR #1354 (https://github.com/mcpdev80/baseharbor/pull/1354), base `develop`,
  head `159054c2`, draft=true, 1 file (`internal/machinehttp/execution_journal_test.go`, +220/0).

## repo-rule compliance

- Write-set: exactly one new test file under `internal/**`. No production code touched;
  `store.go` restored byte-identical to origin/develop.
- `.github/**` and `scripts/**` untouched — `git diff origin/develop --name-only -- .github scripts` empty.
- No `git add -A`; targeted `git add <file>` only.
- No skip-by-env trick; fail-closed is asserted by the test, not by environment perms.
- DRAFT PR only; no merge, no promotion, no tag.

## END
END f49a3303 lane w41 DONE: w41-ci-authority: execution-journal (executionStore) fail-closed + durable-transition fixture, live-tested; candidate SHA 159054c2; DRAFT PR #1354.
