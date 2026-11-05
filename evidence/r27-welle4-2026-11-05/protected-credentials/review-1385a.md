# CODEX-REVIEW — PR #1385 (read-only)

Verdict: **REJECT** — exact head `74a74e49fdcc592481cd29df44cc28dc50df1f79`.

## Identity and write set

The PR API and `ls-remote refs/heads/work/r27-protected-credentials` match the exact head. Develop `24c7d0492f34e58c2a6be505ba80b8bdfb151cb7` is its parent. The write set is exactly `cmd/baha/dev_access.go`, `internal/devaccess/rebind.go`, and `internal/devaccess/rebind_test.go`; there is no new `internal/credential` or store file. All 57 `internal/openbao/` tracked blobs and all 277 `internal/application/` blobs are identical to develop. The existing `internal/credential/prepared_material.go` blob is also unchanged (`3c05c5f52212f30800cf1701a1929c89545dc414`).

## Four recovery cells and authority check

I ran `go test ./internal/devaccess -run '^TestRecovery' -count=1 -v` at the exact head using host-backed temporary/cache directories; all four tests passed:

1. No local opt-in credential: `TestRecoveryFailsClosedWhenNoLocalOptInCredential` returns `Unrecovered` with `ErrNoRecoverableCredential`.
2. Existing managed object: `TestRecoveryUsesExistingManagedAuthorityWithoutDuplication` consults the managed authority and does not call the local store's `Persist`.
3. Local opt-in with no managed object: `TestRecoverySeedsManagedAuthorityOnceForFreshDevice` reaches `Recovered` and observes a store persist.
4. No local store and no managed object: `TestRecoveryFailsClosedWithoutLocalStoreWhenNoManagedObject` fails closed.

`recoverLocalCredential` is called only from `reconcileDeveloperCredentialAuthority` (`cmd/baha/dev_access.go:191,215`); `ensureAuthoritativeDeveloperCredentials` reaches that existing reconcile function at line 290. The new rebind type returns status only, not credential material. The only production managed-secret APIs used are the existing `GetManagedCredential` and `SetManagedCredential` functions; no second store or remote-to-workstation fallback was added by `rebind.go`.

## Finding: the production fresh-rebind path writes twice

The four tests exercise `devaccess.Recovery` with stubs and do not cover the complete production reconcile flow. On a local opt-in credential with no managed object:

1. `reconcileDeveloperCredentialAuthority` sees `ErrManagedCredentialNotFound` at `dev_access.go:180-185` and calls `recoverLocalCredential` at lines 191-195.
2. `Recovery.Recover` sees no managed object and calls `Store.Persist` at `internal/devaccess/rebind.go:105-110`; the production store calls `SetManagedCredential` at `dev_access.go:258-280`.
3. After that successful recovery, the switch falls through. `reconcileDeveloperCredentialAuthority` then unconditionally encodes `candidate` and calls `SetManagedCredential` again at `dev_access.go:200-205`.

So a fresh rebind seeds the same managed path twice, despite the helper's “exactly once” contract. There is also a lost-update race: if another actor creates the managed object after the first not-found read but before `Recovery.Managed.Exists`, recovery returns `Recovered` without persisting; the unconditional final `SetManagedCredential(candidate)` still overwrites the object that appeared in the meantime. This violates the existing managed authority's precedence and is not covered by the stub test's boolean `persisted` flag.

## Gates and repository status

Run `41974727140` is terminal success on the exact head; `PR Selected Checks` (integration 15368), `go-unit-tests`, build, vet and CLI checks passed. Runtime integration was skipped. `ls-remote` measured develop `24c7d0492f34e58c2a6be505ba80b8bdfb151cb7` and the feature ref at the exact candidate SHA. A local repeat of the package tests initially hit `/tmp` quota; rerun on the host filesystem passed all four recovery tests.

## Recipe

- **File:** `cmd/baha/dev_access.go` and a focused production-flow test at the existing reconcile seam; extend `internal/devaccess/rebind_test.go` only if needed to model concurrent managed-object creation.
- **Change:** make the recovery operation return/communicate that it has already seeded the existing managed authority, and return the recovered candidate without issuing the unconditional second `SetManagedCredential`. Before any write, preserve a managed object that appears after the initial lookup; do not overwrite it with a stale local candidate.
- **Test requirement:** inject/count managed Get/Set calls through the full production reconcile path. Assert one Set for absent-managed + opted-in local; assert zero Sets and preserve the winning value when a managed object appears between checks; assert existing-managed reads do not duplicate; retain the two fail-closed cells and exact-head selected checks.
- **Stop criterion:** if recovery can issue two writes or overwrite a managed value created concurrently, reject; do not add a new credential store or bypass the existing OpenBao authority.

No PR, merge, comment, or card action was taken.
