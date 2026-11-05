# CODEX-REVIEW — PR #1385 round 3

- Candidate: `b3c3c1c1405d3102c5f13f6cdf1d2da108d331ed`
- Task base: `24c7d0492f3`; current `develop` observed as `42bfcb1cb481c9e37ecd6ce30580e27829284113` (base drift listed, not treated as a blocker).
- PR #1385: OPEN, base `develop`, head exact candidate.
- Run `41998291745`: completed success on exact candidate.
- `git ls-remote origin refs/heads/work/r27-protected-credentials`: `b3c3c1c1405d3102c5f13f6cdf1d2da108d331ed`.
- Name-only from task base: `cmd/baha/dev_access.go`, `cmd/baha/dev_access_reconcile_test.go`, `cmd/baha/openbao.go`, `internal/deployment/operator_auth.go`, `internal/devaccess/rebind.go`, `internal/devaccess/rebind_test.go`, `internal/openbao/managed_credentials.go`.

## Checks performed

At the exact candidate, focused reconciliation tests and `go test ./internal/openbao ./internal/devaccess ./internal/deployment -count=1` passed. The round-3 test reaches its recovery/seed path: initial managed lookup is not-found, the fake recovery store's `Persist` injects the concurrent winner, reconciliation reads that value back, and the test asserts the winner and zero counted Sets. `operator_auth.go` adds only the `errors` import and named `ErrManagedCredentialAlreadyExists` sentinel; it has no side effects.

However, the checked-in race cell does **not** exercise the production CAS implementation. It replaces `devRecoveryFactory` with a test `reconcileLocalStore`, and `countedManaged.set` simulates the CAS behavior. I independently removed `-if-not-exists` from the production command in `internal/openbao/managed_credentials.go` in a disposable worktree and ran the single test `TestReconcilePreservesConcurrentManagedValue`; it remained green (`ok`, 0.088s). I restored the source and verified the diff was empty. Thus the requested production CAS mutation does not make the conflict cell red. The checked-in test also injects a winner into one reconcile path; it does not launch two enrollment paths concurrently.

## Verdict: REJECT

The production create-only command is present, but the tested conflict behavior is supplied by a fake rather than the actual adapter. The exact single-run mutation requested survives. The deterministic injected race demonstrates recovery control flow, but does not prove OpenBao's CAS option protects competing enrollment paths.

## Recipe

- **File:** `cmd/baha/dev_access_reconcile_test.go` and the production adapter in `internal/openbao/managed_credentials.go` (add an adapter test in the existing test suite if needed).
- **Change:** exercise the real `SetManagedCredentialIfAbsent` adapter through a controlled executor that models OpenBao's atomic create-only behavior, connected to the reconcile conflict path. Run two identical enrollment/reconcile paths concurrently against a barrier-controlled fake authority; assert that the concurrent winner survives and the conflict path performs zero overwriting writes. Do not substitute a fake store whose `set` independently implements the behavior under test.
- **Test requirement:** the unmutated concurrent test passes; removing `-if-not-exists` from the actual production command makes the single conflict test fail deterministically in one run. Confirm recovery/seed is reached and the winning value is read back.
- **Stop criterion:** stop and reject if the production-option mutation remains green, the paths are not actually concurrent, any conflict path overwrites the winner, or the mutation is timing-dependent instead of deterministically red.

No PR or branch action was taken.
