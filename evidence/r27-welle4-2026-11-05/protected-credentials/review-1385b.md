# CODEX-REVIEW — PR #1385, round 2 (read-only)

Verdict: **REJECT** — exact candidate `e295127e45b1c1d2c9929a312fa344095469c864`.

## Candidate identity, commits, write set, and OpenBao blobs

PR #1385 is open, ready, based on `develop`; the API head equals the requested SHA. `ls-remote` reports `develop=24c7d0492f34e58c2a6be505ba80b8bdfb151cb7` and `work/r27-protected-credentials=e295127e45b1c1d2c9929a312fa344095469c864`. The candidate is based on current develop. There are exactly two commits in `develop..head`: `74a74e49` (round 1) and `e295127e` (round 2).

The exact name-only field is:

```
cmd/baha/dev_access.go
cmd/baha/dev_access_reconcile_test.go
cmd/baha/openbao.go
internal/devaccess/rebind.go
internal/devaccess/rebind_test.go
```

No `internal/openbao/` path changed. All 57 tracked `internal/openbao/` blobs are identical between develop and candidate; in particular `internal/openbao/managed_credentials.go` is `36419821e7e241ba55f29a8169c5dadda48e55e6` on both. `cmd/baha/openbao.go` does change to expose `openBaoRuntime` as an injectable test seam; it is listed above and is outside `internal/openbao/`.

## Independent run and counts

At the exact head I ran:

```
go test ./cmd/baha -run '^TestReconcile(SeedsManagedAuthorityExactlyOnce|PreservesConcurrentManagedValue|ExistingManagedReadsWithoutDuplicate|FailsClosedWithoutOptIn)$' -count=1 -v
go test ./internal/devaccess -run '^TestRecovery' -count=1 -v
```

Both commands passed. The production-reconcile test counters establish: fresh opt-in path = one Set and read-back; already-present managed path = zero Sets; no-opt-in fail-closed path = zero Sets. The four recovery unit cells also pass.

The checked-in `TestReconcilePreservesConcurrentManagedValue` does **not** exercise its claimed race: at `cmd/baha/dev_access_reconcile_test.go:124-128`, it initializes `managed.value` but leaves `notfound` false. The first Get therefore returns the value immediately and `reconcileDeveloperCredentialAuthority` returns at its existing-managed branch, before calling Recovery or `Managed.Exists`. It is duplicate early-return coverage, not the required race.

I changed only that fixture in a disposable worktree to set `notfound: true`, leaving a concurrent value for Recovery.Exists and the read-back to observe. The test passed, demonstrating the narrower interleaving (the managed object appears before Exists checks). I then independently injected a value after the checker observed absence but before `Persist` writes. That counter-probe failed: `sets=1`, and the returned value was the stale local opt-in credential rather than the concurrent winner. `SetManagedCredential` uses `bao kv put` (`internal/openbao/managed_credentials.go:20+`), an unconditional write; there is no create-only/CAS guard between the Exists check and Persist. This leaves a genuine check-then-write race that can overwrite a newly created managed authority.

I also restored the prior unconditional second-Set mutant in the disposable worktree. With the race fixture corrected to enter Recovery, `TestReconcileSeedsManagedAuthorityExactlyOnce` failed with `Set calls = 2`, and the race case failed with `Set calls = 1, want 0`. The mutation and fixture changes were removed; the candidate worktree is clean.

## Hosted gates

Run `41985472620` is terminal success at the exact candidate SHA. `PR Selected Checks` is **success** (not skipped); Go unit tests, build, vet, CLI package/guided tests, CLI vet/gofmt, source contracts, focused Python, source format, workflow policy, and trusted plan passed. Docker/Podman and runtime-specific jobs were skipped as unaffected. No rerun or PR action was performed.

## Recipe

- **Files:** `internal/openbao/managed_credentials.go`, `cmd/baha/dev_access.go`, and `cmd/baha/dev_access_reconcile_test.go`.
- **Change:** make the fresh seed conditional/atomic using the existing OpenBao authority (for example, a create-only/CAS write); on a conflict, read and return the already-managed winner. A prior `Exists` result cannot authorize an unconditional `bao kv put`.
- **Test requirement:** fix `TestReconcilePreservesConcurrentManagedValue` so the initial managed Get returns not-found and Recovery reaches Exists/read-back; add a deterministic concurrent-create-after-Exists-false/before-seed case. Assert exactly one Set for fresh creation, zero overwriting Sets when the concurrent value wins, and verify the returned value is the stored winner. Retain the existing/exactly-once and fail-closed cells; rerun relevant tests and selected checks at the corrected SHA.
- **Stop criterion:** any interleaving can overwrite a concurrently created managed value, the checked-in race test exits before Recovery, or the unconditional second-Set mutant passes.

No PR, merge, comment, or card action was taken.
