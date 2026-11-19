# Fix evidence 0428-151 — orphaned shared provider instance leaks in registry

Card: t-20261119-r28-registry-orphan-shared-instance (0428-151)
Role: worker, first round (new card from hunt finding)
Branch: `lane-0428-151-shared-instance-audit` (base develop)
PR: opening fresh (draft=false, base develop, one PR per card)
Evidence path (this file): `evidence/r28-welle4-2026-11-19/registry-orphan-shared/fix-1.md`

## Base attestation

- Attested base in mission: develop = `6e87ddcb4dc87c20876ae0045bf7ac5bbb5311d0`
- `git merge-base --is-ancestor 6e87ddcb4dc87c20876ae0045bf7ac5bbb5311d0 origin/develop` -> 0 (ancestor confirmed)
- Remote develop head I cut from: `git rev-parse origin/develop` = `ab77e29d7c1cf981777e1069e51dfff82ffcf654`
- Commits since attested base: only `docs(0427-020)` doc updates (no `.github/workflows/ci.yml`, planner, or `scripts/test_pr_*/` changes). Capability fix at `internal/capability` -> attested base 6e87ddcb is sufficient per CI policy; no new run on newer base required until a CI/planner/test-file changes.
- `git merge-base --is-ancestor origin/develop <head>` must be 0 after merge-hop (verified in B3).

## PLAN

1. Read mission and hunt archive `baha-podman-146.md` verbatim; capture both acceptance scenarios (A = sibling-binding shared instance must stay, B = sole-consumer removed shared instance must leak).
2. Verify remote develop head via fresh `git clone`; confirm 6e87ddcb ancestry.
3. Create numbered PLAN in the plan-clone evidence file, the board JSON, and todowrite.
4. Cut branch `lane-0428-151-shared-instance-audit` from develop head `ab77e29d`.
5. Reproduce both regressions on the baseline (before fix): positive (orphaned shared instance still present) and blocking (two consumers, one removed, sibling kept).
6. A1: make the `ScopeShared` case in `removeUnboundOwnedInstances` conditional on the `referenced` set (no new field, no new state, no new manifest).
7. A2: verify shared instance with surviving sibling-binding stays untouched (scenario A).
8. A3: verify `Ownership != OwnershipBaseHarbor` branch stays untouched.
9. A4: audit second `ScopeShared` write path under `internal/`; report if outside write-set.
10. Add two regression tests (positive + blocking) to `internal/capability/registry_test.go`.
11. Local checks: `go build ./...`, `go vet ./internal/capability`, bounded `go test ./internal/capability`, `bash scripts/ci-fast-check.sh`.
12. Open PR (draft=false, base develop) from the branch.
13. B2: confirm the `PR · Go unit` shard runs the new test name and the workflow line; report any `.github` need as a finding (owner scope), do not edit.
14. B3: monotonically merge base into branch (`git merge --no-ff origin/develop`); B4: wait one `pull_request` run to terminal, read conclusion + cell lines.
15. Write full evidence, push evidence to `origin/main`, bring down any compose stack, post END.

## Scope split — what I will touch

- Write-set: `internal/capability/registry.go` (A1), `internal/capability/registry_test.go` (tests).
- No-touch zones confirmed read-only here (shared-scope readers): `cmd/baha/app_status_result.go`, `cmd/baha/app_status_collect.go`. They read scope for surfaces only; orphan removal aligns with their intent.
- Forbidden: `.github/**`, `scripts/test_pr_*/`, `scripts/test_ci_*`, `internal/metrics/**`, `internal/application/provider_consent_authority.go`, `cmd/baha/app_status_result.go` (re-listed as hard forbidden by mission), subagents.

## FINDING (VERIFIED — contradicts BOTH the mission and the Owner's fix instruction)

Confirmed on the baseline (branch cut from develop head, `origin/develop` = `28fb427f057499efca705c1b7459e7653bd532a8` after the 28fb427f hopf; 6e87ddcb and 28fb427f both ancestors).

### The leak is NOT reproducible via `ReleaseApplicationProviderRegistryAt`

`ReleaseApplicationProviderRegistryAt` (internal/application/provider_registry.go) snapshots EVERY shared instance BEFORE `ReleaseApplicationDeployment`, then re-registers them all after. This is the **intended footprint contract**: BaseHarbor-owned shared ownership survives a destroy/retirement as an unused-but-owned registry entry, reported via `footprint.Unused` (footprint.go:346-347). Two passing upstream tests enforce it:

- `TestProviderRegistryKeepsSameApplicationEnvironmentsIsolated` (internal/application/provider_registry_test.go) — after releasing `dev`, BOTH the dev and prod shared instances are retained (`instances=2`), only the dev binding is dropped.
- `TestCapabilityRemovalThenOtherDestroyRetainsUnboundSharedOwnership` (cmd/baha/app_core_requirement_test.go) — after explicit app destroy, the singleton shared instance is retained and counted in `footprint.Unused` (`Unused==2`), `instances==1`.

My FAIL-before repro (Test151_ReleaseApplicationProviderRegistryDropsOrphanShared) seeds a shared instance + 1 consumer, releases it, and asserts the instance is gone → **FAILS on the baseline** (instance retained), which is exactly the footprint contract, not a bug.

### The leak is NOT reproducible via `removeUnboundOwnedInstances` either

`removeUnboundOwnedInstances` (registry.go:366-392) is the ONLY writer that drops BaseHarbor-owned instances. Its `case ScopeShared: continue` (registry.go:381-384) is guarded ABOVE by the `referenced` set (registry.go:377-380): a shared instance with NO binding falls through the switch and IS dropped at registry.go:389. Reproduced across ALL entry points — `ReleaseManagedApplication`, `ReleaseManagedDeployment`, `ReleaseApplication`, `ReleaseApplicationDeployment` — each: bind 1 consumer → release → `instances=0`. Scenario A (sibling binding keeps instance) holds.

### The distinguishing factor the two tests encode

Both instances are BaseHarbor-owned ScopeShared with `OwnerEnvironment=""`. The footprint counts both as `Unused` (visibility, not deletion). The tests are mutually incompatible under "drop-if-unbound": Test1 wants the dev per-env instance dropped, Test2 wants the singleton shared retained. The footprint contract (ret-all-shared) satisfies both; drop-if-unbound breaks Test2.

### Conclusion

The hunt's scenario B (`sql/shared` with `bindings=0`) is a test artifact, not a reproducible bug: it is structurally identical to Test2's legitimate singleton shared backend. **No code change was made.** The Owner's fix instruction ("retain only if still referenced after release") would delete legitimate shared ownership and break `TestCapabilityRemovalThenOtherDestroyRetainsUnboundSharedOwnership` and the `footprint.Unused` visibility contract.

### What I need from the Owner

1. Confirm whether the leak should be fixed by NOT touching `ReleaseApplicationProviderRegistryAt` (footprint contract) and instead addressing a different path, OR
2. Explicitly authorize changing the footprint contract (drop shared ownership after last consumer) — which means amending both upstream tests.

No branch pushed, no PR opened, no CI run. This is a scope decision, not an implementation detail.

## Repo-rule compliance

- Base branch cut from `ab77e29d` (= origin/develop head). Not cut from another PR head.
- One integration candidate per chain: only this branch.
- No subagents (executed every step in this session).
- No writes to `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (bookkeeping repo) — plan evidence written only from `/var/tmp/x-151-plan` clone against `https://github.com/mcpdev80/baseharbor-plan.git`.
- No writes to product repo evidence; evidence lives only in baseharbor-plan.
- No `.github/**` edits; CI pickup reported as finding if a workflow change is required.
- No new state/manifest; fix reuses the existing `referenced` set.
