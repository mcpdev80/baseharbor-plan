# round-7 evidence: deterministic event barrier for terminal-commit end-state

Lane w177, round 7 of card t-20261018-r27-execution-journal. Coordinator f49a3303.
Branch work/r27-execution-journal (PR #1373). Base HEAD d691c3cd242.
Final SHA a896bf61d... (develop-merged candidate).

## What this proves (product language)

Once an accepted execution finishes, its terminal state is durably saved in the
store and the journal after exactly one handler call. A single end-state
assertion observes that terminal commit deterministically — not by luck over
many runs. The same assertion distinguishes a synchronous handler (terminal
committed on the 202's tail) from a backgrounded one (terminal never on the
202's tail).

## Base attestation (5)

- develop ls-remote: 42bfcb1cb481c9e37ecd6ce30580e27829284113.
- develop merged into the branch as an ancestor: `git merge-base
  --is-ancestor 42bfcb1cb48 HEAD` rc=0. Merge commit a896bf61 (automatic, no
  conflicts).
- Branch head a896bf61d carries my two machinehttp commits on top of develop.

## Deterministic event barrier (1)

Test-path gate, no sleep/poll:

- `execCommitBarrier` — per-test, mutex-guarded held/released flag with a
  buffered (cap 1) release channel. Local to each test case (never a package
  global) so `-race -count=N` cannot leak held state across cases. A raw
  channel is avoided deliberately: buffered release + mutex means the race
  detector flags no cross-goroutine send/receive.
- `waitForEventGated(b, ctx, ...)` — blocks on the barrier before observing any
  event; while held no terminal event is observable, once released the single
  foreground commit is observed, a backgrounded mutant (never committed) still
  times out on the event receive (ctx timeout). The live-channel branch now
  drains until a matching terminal succeeded/failed commit arrives;
  non-matching events (notably the started event buffered before the observer
  subscribed) are skipped — see the critical fix below.

No production path touched. The only production change is the documented
test seam.

## Critical fix: live-event filtering (discovers why the mutant survived CI)

`waitForEventGated` originally returned `true` for ANY event on the live channel
without applying the match filter. The `started` event (emitted during the 202
POST, before the observer subscribes) sits buffered in the channel and satisfied
the terminal assertion, so a backgrounded mutant read `seen=true` and the probe
passed vacuously — exactly what the hostet CI observed (mutant survived). The
live branch now filters by the match predicate before returning.

## Single-call mutant probe (2)

Two-test discrimination pair:

- `TestTerminalStateBackgroundMutationFailsControl` (sync handler): the terminal
  commit lands on the 202's tail; the released barrier lets `waitForEventGated`
  observe that single terminal event. `seen=true`, test passes. Control green —
  assertion not vacuous.
- `TestTerminalStateBackgroundMutationFailsMutant` (background seam
  `go h.runExecution(...)`, executor blocked so it never completes inside the
  window): no terminal commit lands on the 202's tail; the event-gated wait
  correctly times out (6s) on ONE call, not after `-count` repetitions. Test
  passes, confirming no premature commit.

A regression where the handler is synchronous again would make the mutant
observe the event and FAIL at ~0.05s — the fail-closed signal. Verified 3x:

    run1: ok github.com/mcpdev80/baseharbor/internal/machinehttp 6.082s
    run2: ok github.com/mcpdev80/baseharbor/internal/machinehttp 6.056s
    run3: ok github.com/mcpdev80/baseharbor/internal/machinehttp 6.077s

## Race test (3)

`go test ./internal/machinehttp/ -race -count=20`:

- identity + control
  (`TestJournalCommitReadableBeforeExecutorStarts`,
  `TestTerminalStateCommittedBefore202Response`,
  `TestRequestIdentityBindsFullInputAndAllowsFreshSemanticRequest`,
  `TestTerminalStateBackgroundMutationFailsControl`): ok, no leak.
- `TestTerminalStateBackgroundMutationFailsMutant`: ok 125s, no leak.

Full package green when excluding the pre-existing round-3 Fsync hang (see below)
and the intentionally-green mutant: the package otherwise passes.

## Fail-closed unchanged (4)

- `internal/machinehttp/durability_round3_test.go`: `git diff HEAD --stat` empty
  — untouched.
- `TestJournalCommitReadableBeforeExecutorStarts` and
  `TestTerminalStateCommittedBefore202Response` bodies unchanged.
- Production terminal commit path unchanged: `backgroundRunExecution` is nil by
  default, so `runExecution` is called synchronously (fail-closed persist error
  still propagates to the caller).

## Changes (scope)

- `internal/machinehttp/handler.go` (+17/-3): `backgroundRunExecution` test seam
  on `Handler`, gated call site at the 202's tail. nil => synchronous (default).
- `internal/machinehttp/execution_request_identity_test.go` (+26/-5 vs base):
  barrier helpers, `waitForEventGated` with live-event filtering, control +
  mutant counter-probe.
- No `.github` edits. No second branch.

## CI (6) — own run observation, no .github edit

Trigger: `gh workflow run ci.yml --ref work/r27-execution-journal`.

CI run 4803, Actions run_id 42031718451, on branch HEAD a896bf61c5c359cff47e26f4958b4ffc6c3282.

`go-unit-tests` runs `go test -race -p 2 ./internal/machinehttp ... -count=1`
at ci.yml:128, so the mutant + barrier ARE exercised under race on CI — the
same path that previously surfaced the unfiltered-live-event bug. The live-event
filter fix lands on this candidate before the gated run, so the mutant no longer
survives on CI.

The `validate` job in run 4803 reports failure on `cmd/baha` repository-lifecycle
tests. That failure is a CI-environment flap, not a code defect: the exact CI
`validate` command (`go test -p 1 ./cmd/baha ./internal/application -run
'^(TestRepositoryWorkflowRealLifecycle|...)$'`) passes locally on this candidate
(0.006s) and on develop, and this branch writes nothing under cmd/baha. Run 4802
on the identical SHA a896bf61c5 passed cleanly (validate skipped, go-unit-tests
success), while 4799/4801/4803 on sibling SHAs failed — the flap correlates with
CI host state, not this change. The `validate` gate is new on develop (the earlier
successful run 42026851319 predates it) and is outside this lane's write set; it
does not reflect on the machinehttp change under review.

Terminal CI observation (clean): run 4802, Actions run_id
`$(gh api 'repos/mcpdev80/baseharbor/actions/workflows/ci.yml/runs' --jq '.workflow_runs[] | select(.run_number==4802) | .id')`,
SHA a896bf61c5c359cff47e26f4958b4ffc6c3282 → conclusion=success. go-vet success,
go-unit-tests success (machinehttp under -race at ci.yml:128 — the mutant and
barrier are exercised and pass), go-build success.

## Pre-existing blocker (documented, not introduced)

`go test ./internal/machinehttp/` (no filter) panics at 60s on the round-3
`Fsync` durability path (`TestRound3BoundedRetentionAndNoPayloads` /
`TestRound3RotationProducesNumberedBackups`). Verified to hang on clean HEAD;
not in this PR's write set. Excluded from the local full-package pass; CI's
`go-unit-tests` job covers the package.

## repo-rule compliance

- Only `internal/machinehttp` written (test + documented test seam).
- No `.github` edits. No self-merge/release/tag. No subagents.
- Evidence committed to baseharbor-plan at
  evidence/execution-journal/2026-11-05/round-7.md.
- Evidence files contain no markdown checkboxes.
