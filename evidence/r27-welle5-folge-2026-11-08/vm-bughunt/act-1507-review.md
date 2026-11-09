# CODEX-REVIEW 0427-176 — PR #1507

## PLAN

1. Verify exact PR head, live develop base, ancestry, and terminal hosted checks.
2. Inspect per-app lock acquisition and the independent-app / same-app concurrency regressions.
3. Verify the destroy fairness test causes real lock contention and checks acquisition, not mere completion.
4. Recheck remote disclosure, core-stop consent, orphan-adoption, and fail-closed behavior.
5. Publish the SHA-specific verdict and correction recipe to baseharbor-plan origin/main.

## Candidate and hosted evidence

- PR #1507 head: `16dfda39f476a481dc72c85492c298230e51a59d`.
- Live develop: `b3a8042d18ea60f162a32a51df34a499cad6a237`; `git merge-base --is-ancestor b3a8042d18ea60f162a32a51df34a499cad6a237 16dfda39f476a481dc72c85492c298230e51a59d` returned 0.
- `git ls-remote` confirmed develop at `b3a8042d18ea60f162a32a51df34a499cad6a237` and PR head at `16dfda39f476a481dc72c85492c298230e51a59d`.
- Hosted run `42578679997` is terminal `completed/success` on the exact head. `PR Selected Checks` passed (job `129035550796`); `go-unit-tests` passed (`129032117596`); source format, build, vet, authority-package tests, docs, and wizard-app-new tests passed. Native destroy-retry Docker and Podman passed (`129032098227`, `129032098132`). Native Keycloak/Core, Selected Runtime, Targeted HA, and contract/pin jobs were skipped; they are reported as skipped, not as passes.
- Product diff is confined to lifecycle lock code/tests and lifecycle documentation; no `.github/**` changed.
- Local focused concurrency and rollback regressions passed: `go test ./cmd/baha -run '^(TestIndependentAppsDoNotSerializeOnSharedTarget|TestSharedConsumersSerializeOnAppOwner|TestDestroyNotStarvedByBoundedRetry|TestRemoteUnsupportedProviderDisclosesCurrentImpactBeforeTechnicalDenial|TestCoreStopCLIJSONAndMCPExposeSameCurrentScopeWithoutEnvironmentConsentReuse|TestW138.*)$' -count=1` and `go test ./internal/stableid ./internal/coreinstallation -run 'TestAcquireAppLifecycleLock' -count=1`.

## Findings

### F1 — blocking: the independent-app regression can pass when the apps serialize

The new lock key is per deployment ID (`internal/stableid/lock.go:84-98`), and `TestSharedConsumersSerializeOnAppOwner` checks mutual exclusion for 25 same-ID writers (`cmd/baha/application_lifecycle_lock_test.go:197-250`). However, `TestIndependentAppsDoNotSerializeOnSharedTarget` does not prove beta entered while alpha held its lock. Alpha sleeps 250 ms; beta calls the lock synchronously; after beta returns, the test accepts either state of `holderDone` (`:266-307`). If beta had blocked on a target-wide lock until alpha released, the test would still pass. The key implementation is per-app, but the required regression does not guard against the old serialization behavior.

### F2 — blocking: the destroy test uses a different app lock and demonstrates no fairness

`TestDestroyNotStarvedByBoundedRetry` holds the lock for deployment ID `alpha` and requests destroy for ID `destroyed` (`cmd/baha/application_lifecycle_lock_test.go:326-359`). Those are different per-app lock files, so destroy does not contend and can acquire immediately. The test therefore does not prove finite acquisition under up/destroy contention.

The retry loop at `cmd/baha/application_lifecycle_lock.go:86-119` retries both classes with the same backoff up to 15 seconds, then returns an error. `allowPriority` adds only one immediate attempt (`:90-95`); after a busy result, destroy and up/apply share the same retry policy. A finite timeout bounds how long a caller waits, but it does not prove that destroy acquires under contention or prevent a stream of same-app up writers from repeatedly winning. The task's stated fairness/finite-acquisition result is not evidenced by the current test.

### F3 — blocking concurrency concern: local app calls do not retain the target-wide lock

`cmd/baha/application_lifecycle_lock.go:57-72` returns after acquiring only the per-app lock for local app operations. The target-wide `.installation.lock` is acquired only by the fallback path at `:75-79` for operations without a local deployment ID or classified remote. This conflicts with the comment at `:23-25` claiming local callers layer the target owner lock on top. Target-definition changes still acquire `.installation.lock` (`cmd/baha/target_definition_change.go:161-176`), and control-plane stop/destroy also use the target-level path (`cmd/baha/control_plane_stop.go:45`, `cmd/baha/control_plane_destroy.go:101`). A local app lifecycle can therefore overlap those target-wide operations instead of coordinating with them. The r6 fixes for stop consent do not establish cross-lock mutual exclusion.

## Verified points

- Same-app exclusivity remains: `TestSharedConsumersSerializeOnAppOwner` uses the same deployment ID for all writers and asserts `maxConcurrent <= 1`.
- The three named rollback areas have source-level guards and focused tests: remote unsupported execution exits through its existing remote path before local lock staging; control-plane stop without environment-consent reuse remains covered by `TestCoreStopCLIJSONAndMCPExposeSameCurrentScopeWithoutEnvironmentConsentReuse`; never-delivered handling recognizes only a locally eligible proof and skips hidden lock entries in `eligibleNeverDeliveredLocalDestroy` (`cmd/baha/app_context.go:153-197`). The selected local tests above and hosted go-unit/native-destroy-retry jobs passed.
- Per-app locking is implemented with a private root check and `O_NOFOLLOW`/nonblocking flock through `lockNamed`; the lock file is hidden under `deployments`, so it is not mistaken for a record.

## Verdict

**KORREKTUR** for `16dfda39f476a481dc72c85492c298230e51a59d`.

The exact-head CI is green and same-app exclusion is covered. Acceptance is not complete: the independent-app test accepts a serialized execution, the destroy test uses a non-contending key, and the local app path no longer coordinates with operations holding the target-wide lifecycle lock despite the code claiming it does.

## Actionable correction recipe

- File: `cmd/baha/application_lifecycle_lock_test.go`, `TestIndependentAppsDoNotSerializeOnSharedTarget` around lines 256-307. Hold alpha with an explicit release channel; start beta acquisition in a goroutine; require beta's acquisition signal while alpha is still confirmed held, under a short deadline shorter than alpha's hold. Release alpha in cleanup. The test must fail if both IDs are routed through one target-wide lock.
- File: `cmd/baha/application_lifecycle_lock_test.go`, `TestDestroyNotStarvedByBoundedRetry` around lines 316-368. Use the SAME deployment ID for the held up and destroy attempt. Prove destroy actually receives a contention result before the holder is released, then assert it acquires within the documented finite bound. If the contract is starvation-free under sustained up arrivals, keep an up contender running and demonstrate destroy wins; otherwise narrow the contract and document that bounded waiting can end in fail-closed timeout rather than acquisition.
- File: `cmd/baha/application_lifecycle_lock.go` and the lifecycle-lock API. Preserve coordination between per-app local operations and target-wide stop/destroy/target-definition mutation without restoring serialization among unrelated apps. Implement an explicit compatible target-owner coordination mechanism (for example, shared target ownership for app operations and exclusive target ownership for target-wide operations), or document a proven existing mechanism. Update comments to match the actual lock layering.
- Retain the three rollback regressions: remote unsupported disclosure must stage no local lock state; core-stop consent must remain scope-bound; never-delivered adoption must remain proof-gated and fail-closed. Add a cross-operation regression showing target-wide stop or definition mutation cannot overlap a local app lifecycle.
- Test requirement: focused lifecycle tests plus the existing rollback tests in `go-unit-tests`; verify test names are executed by the hosted job on the corrected exact head. Require `PR Selected Checks` terminal success. Continue to report skipped jobs honestly.
- Stop criterion: do not approve until independent apps demonstrably acquire concurrently, same-app writers remain mutually exclusive, a same-key destroy contention test demonstrates the documented finite-acquisition/fairness guarantee, and target-wide owner mutations remain coordinated with local app operations without bringing back cross-app serialization. Verify exact-head CI after those corrections.

## repo-rule compliance

- Review-only; no product or workflow files changed.
- Product candidate verified unchanged after review: `16dfda39f476a481dc72c85492c298230e51a59d`.
- Evidence stored only in baseharbor-plan.
- No containers or compose projects were started.

END_DONE 0427-176-review: KORREKTUR PR #1507 head `16dfda39f476a481dc72c85492c298230e51a59d`; independent-app and destroy-fairness tests do not prove their stated concurrency outcomes, and local app operations do not retain target-wide locking; run `42578679997` terminal success.
