# CODEX-REVIEW — PR #1388 app-binding round 1

- Candidate: `4e4a23e89bd3ff9d6db1fc65d4a7ee7a7e44f7b6`.
- Base: `develop` `42bfcb1cb481c9e37ecd6ce30580e27829284113`; develop is an ancestor of candidate.
- PR #1388 is OPEN, ready, base `develop`, exact head above.
- `git ls-remote origin refs/heads/develop refs/heads/work/r27-app-binding`: develop `42bfcb1cb481c9e37ecd6ce30580e27829284113`; branch `4e4a23e89bd3ff9d6db1fc65d4a7ee7a7e44f7b6`.
- Hosted run `42020006887`: terminal success, exact candidate. `PR Selected Checks` passed. Focused CLI/package/build/vet/source-contract checks passed; targeted Docker/Podman/runtime and unrelated pins were skipped by selection.
- Name-only: `cmd/baha/app_binding_production_test.go`, `internal/application/app_binding_contract_test.go`, `internal/application/identity_resolution.go`, `internal/application/store.go`.

## Independent probes

At the exact candidate I ran the internal parallel registration case:

```text
go test -race ./internal/application -run '^TestConcurrentFirstRegistrationConvergesProves$' -count=20
ok github.com/mcpdev80/baseharbor/internal/application 1.064s
```

It starts 20 concurrent registrations on the same canonical store, then checks all results converge on the durable winner ID. There is no divergent identity/cross-rewrite.

I ran the production-path cells myself:

```text
go test ./cmd/baha -run '^Test(CLIProductionPathAssignsServerIdentityProves|CLITwoFreshHomesConcurrentRegistrationProves)$' -count=1
ok github.com/mcpdev80/baseharbor/cmd/baha 2.357s
```

These drive `runWithIO(..., []string{"app", "init", "--quick", ...})`, not `InitializeIdentity` directly. The two-home test creates two separate checkout roots, initializes each, reads each canonical store and verifies distinct server-assigned IDs with no cross-rewrite. The two-home CLI invocations are sequential; the concurrent race-20 proof is the separate internal-store test above.

### Mutant A — remove owner-name authorization

I disabled the `item.ApplicationID == m.ApplicationID && item.Name != m.Name` owner guard in a disposable exact-head worktree and ran the targeted test once:

```text
go test ./internal/application -run '^TestAttachToPermittedExistingAppProvesNamedDenial$' -count=1
--- FAIL: TestAttachToPermittedExistingAppProvesNamedDenial
    app_binding_contract_test.go:140: foreign-name attach over existing id was accepted; attach is not permission-gated
```

The mutation was restored and the source diff is clean.

### Mutant B — remove bounded winner retry

I mutated `concurrentLoadRetries` from 1000 to 0 and ran the concurrency cell once:

```text
go test ./internal/application -run '^TestConcurrentFirstRegistrationConvergesProves$' -count=1
--- FAIL: TestConcurrentFirstRegistrationConvergesProves
    app_binding_contract_test.go:95: concurrent registration did not converge: "<err>"
```

The mutation was restored and the source diff is clean. The test’s failure is deterministic in this single mutant run.

## Store boundary

`store.go` changes are limited to the bounded create/list binding seam: `Create` writes a complete manifest in a unique sibling temporary directory and atomically renames it into place; `List` ignores only names that cannot be valid application slugs and match the temporary-build suffix. `Load` is unchanged. I compared `internal/application/recovery_metadata.go`, `backup_metadata.go`, `update_metadata.go`, `runtime_lifecycle.go`, and `repository_manifest.go` against develop; all are byte-identical. No other store path was changed.

## Verdict: ACCEPT

The candidate satisfies the two-home server-ID and isolation check, the simultaneous registration race-20 convergence check, both single-run mutation checks, and the real CLI production-path requirement. The generic Store changes are confined to atomic create and transient-build filtering; other Store operation files remain unchanged. Required hosted validation is terminal success on this exact head.

No PR action was taken.
