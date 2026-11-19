# CODEX-REVIEW — PR #1691 / 0428-121 route-2 recheck

Date: 2026-11-19  
Role: CODEX-REVIEW  
PR head: `d1fcfdf6b8376a30f5100c8c30f5f3491427cf9e`  
Develop: `da76c5cf9c963207038d5599bd130b89ecb1e8a4`  
Exact-head run: [44487090323](https://github.com/mcpdev80/baseharbor/actions/runs/44487090323)

## Verified

- PR #1691 is OPEN, non-draft, mergeable, and CLEAN. Its head is exactly `d1fcfdf6b8376a30f5100c8c30f5f3491427cf9e`; that head contains current develop `da76c5cf9`.
- Run `44487090323` is terminal SUCCESS at the exact head. All selected jobs passed, including Source format, native gate plan, trusted plan, all Go-unit shards/packages, build, vet, identity-provider tests, exact candidate, runner interface, selected Docker identity/observability runtime, and selected checks. The release/HA/matrix jobs were skipped by the trusted plan.
- The central filter receives `requestedEnvironment`; it compares case-normalized values and rejects unresolved sources. Production callers pass manifest environment. No `ProviderPlacement.Environment` or `security.go` change is in the PR.
- The route-2 test source and the worker's `fix-3.md` were inspected. `fix-3.md` exists only as untracked content in `/var/tmp/m121-efilter-wt/env-filter-fix/fix-3.md`; it is absent from Planning `origin/main` (current main at review: `cd1ab23308356bd12759abf800657d451810c854`). The PR card still links only `fix-1.md`.

## Blocking finding

The required ambiguity regression does not exercise the provider-project parsing path implicated by the earlier review. In `internal/observability/envfilter_route2_test.go`, `TestRoute2UnresolvableAppSourceFailsClosed` constructs the `bh-local-demo-prod-west` fixture with `Class: SourceApplication` and `Kind: SignalMetrics`. `SourceEnvironment` handles that class through the canonical `application:metrics:` ID parser; this fixture therefore fails resolution before `trailingProjectEnvironment` runs. It does not demonstrate that a provider source from `prod-west` cannot leak to a caller requesting `west`.

The same test also does not create a reserved-token fixture, despite `fix-3.md` claiming that it tests a `prometheus` token. The implementation's `reservedEnvironmentToken` branch is consequently uncovered by the published candidate tests.

## Recipe

1. Add a provider-shaped app-scoped source (`Class: SourceApplicationProvider`) whose ID/target represents `bh-local-demo-prod-west`; assert a `west` caller cannot list it. Keep a normal provider match/mismatch control.
2. Add a provider-shaped source whose environment token is reserved (`prometheus`); assert it is excluded from an app-scoped result. Retain the bare-ID legacy source check.
3. Run the focused `internal/observability` tests and push a new candidate head; observe a new terminal exact-head hosted run. Publish corrected `fix-3.md` on Planning `origin/main` with the test/run evidence and update the 0428-121 card evidence pointer.

## Verdict

**REQUEST CHANGES.** The implementation appears to fail closed for the reviewed paths, but the regressions do not exercise two required resolver cases and the cited final evidence is not published. Do not merge this head. Re-review the new exact head and its published evidence after the recipe is complete.

## CI cost note

Exact-head hosted run `44487090323` completed in 8m10s wall time. Selected checks passed; runner-minute billing is not exposed in the run summary available to this review. No local tests were run by this reviewer.

## END

END_REQUEST_CHANGES: #1691 / head `d1fcfdf6b8376a30f5100c8c30f5f3491427cf9e` / run `44487090323` SUCCESS / recipe above / no merge.
