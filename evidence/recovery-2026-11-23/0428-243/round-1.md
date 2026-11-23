# 0428-243 — Static cells reject `--access local-docker` (grant mismatch), round 1

Task: `t-20261122-static-cell-local-workload-grant-access` (card 0428-243), release v0.4.28, repo `mcpdev80/baseharbor`.
Lane: `lane-0428-243-static-cell-grant-access`. Branch base: current develop.

## PLAN

- Read mission, card, task note, `cmd/baha/local_workload_authority.go`, its shard test, and `operator_auth_boundary.go`.
- Resolve the real GitHub remote (`origin` = `https://github.com/mcpdev80/baseharbor.git`) and the true develop head.
- Determine whether the primary defect (grant comparison rejecting `local-docker`/`local-podman`) is still live on develop.
- Locate the existing test shard covering the grant path and run it (TEST RUNNER RULE: named `-run` form, no bare `go test ./cmd/baha/`).
- Confirm a durable CI route exists (existing `cli-package-tests` group runs `./cmd/baha`).
- Write evidence; publish to planning repo origin/main; post END.

## Reality witnesses

Real GitHub remote (resolved via `git remote -v`):
- plan repo: `origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)`
- product: `origin	https://github.com/mcpdev80/baseharbor.git (fetch)`

Real develop head (via `git ls-remote origin refs/heads/develop`):
- `dc8626e9c52be07a8ea5b87b468c5991b7540c4f  refs/heads/develop`

## Finding: the primary defect is already fixed on develop

The card's primary defect is the grant comparison at `cmd/baha/local_workload_authority.go:62` (the `isLocalRuntimeAccessProvider` guard rejecting a `local-docker`/`local-podman` provider), plus the sibling `detectRuntimeForTarget` guard in `cmd/baha/target.go` that blocked `local-docker`/`local-podman` with `ErrorCapabilityMissing` BEFORE the engine probe.

The fix is commit `b48ac03ef75165c4e50a4a29d5ef0197af3444da` ("fix(0428-231): accept host-local runtime access forms in the local-workload grant (#1771)"), which is an ancestor of the current develop head:

- `git merge-base --is-ancestor b48ac03ef origin/develop` => YES (ancestor of `dc8626e9`)
- working tree `HEAD:cmd/baha/local_workload_authority.go` line 81 still reads `if selected.AccessProvider != "" && !isLocalRuntimeAccessProvider(selected.AccessProvider)` with `isLocalRuntimeAccessProvider` accepting `"local" || strings.HasPrefix(provider, "local-")` — so `local-docker` and `local-podman` are accepted, operator-auth boundary untouched.
- `cmd/baha/target.go` `detectRuntimeForTarget` now switches on `""`, `"local"`, `"local-docker"`/`"local-podman"` (paired with the matching runtime, failing closed on mismatch), and every other provider.

`b48ac03ef` was authored for card 0428-231 (helper-fan-out context) but its write-set is exactly this card's write-set (`cmd/baha/local_workload_authority.go`, `cmd/baha/target.go`) plus existing shard tests. It is not part of the `internal/operatorauth/**` write-set of #1761; #1761 is untouched.

## Existing shard regression (the required regression evidence)

Tested head: develop `dc8626e9` (detached worktree `/tmp/w243-grant-wt`, `origin` = github.com/mcpdev80/baseharbor).

Command (named form per TEST RUNNER RULE, no bare `go test ./cmd/baha/`):
```
go test ./cmd/baha/ -count=1 -run "TestCLILocalRuntimeAccessProviderForms|TestLocalWorkloadAuthorityPreservesAllNonlocalAndPolicyBoundaries|TestVerifiedLocalRuntimeGrantSatisfiesManagedEnvironmentBoundary|TestOperatorAuthObservationUsesActualLocalAuthorityBoundaries|TestCLILocalWorkloadOperationIncludesGrantBackedRoots" -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"
```

Result: `ok  github.com/mcpdev80/baseharbor/cmd/baha` — all five shards PASS, including `TestCLILocalRuntimeAccessProviderForms` (asserts `local-docker` and `local-podman` qualify as host-local grants) and `TestLocalWorkloadAuthorityPreservesAllNonlocalAndPolicyBoundaries/local-docker` (the previously-rejected pairing now grants).

Build/vet:
- `go build -o /tmp/baha-grant ./cmd/baha` => BUILD OK (58094453 bytes)
- `go vet ./cmd/baha/` => clean

## Durable CI route

The grant path is covered by the existing `cli-package-tests` CI group: `scripts/pr-check-runner.py:202` runs `go_package_tests(['./cmd/baha'], 'CLI', allow_skips=True)`. The regression file `target_runtime_access_provider_test.go` (added by `b48ac03ef`) runs under this group. No new CI job and no `.github` edit are required (card acceptance item 2).

## Secondary (build tag) — Owner scope, not changed

The card notes the static cells build `go build ./cmd/baha` without the `baseharbor_ci_operator_testonly` tag, so `withCIIntegrationOperator` is the no-op from `ci_integration_operator_disabled.go`. This is `.github`/release-gate Owner scope (card acceptance item 3, AGENTS.md §Owner scope). Not changed by this lane. The current CI API for the develop head (`dc8626e9`) only surfaces `Select …` summary checks, and the static-cell job IDs in the card (137187053472 / 137190621488 / 137190621449) belonged to a different lane (`lane-0428-208-static-release-gate`, head `3d927252`, run 45014836421) — not this card. If a live static cell still fails after this primary fix, document the missing build tag as a finding with file:line; do not edit `.github`.

## repo-rule compliance

- Write-set: only inspected `cmd/baha/local_workload_authority.go` and `cmd/baha/target.go` (already-fixed, on develop). No product files changed — the defect is already resolved upstream. No `.github`/`.github/**` touched (Owner scope). No `internal/operatorauth/**` touched (separate #1761 write-set).
- One integration candidate per chain: no branch cut; no PR opened. The fix already lives on develop via an already-merged commit.
- Evidence written only to the planning repo (baseharbor-plan), never a product repo.
- No subagents. All commands run in this session's own worktree.
- No compose/container stack started on any host; nothing to tear down.

## Base attestation

- Real develop head cut from: `git ls-remote origin refs/heads/develop` => `dc8626e9c52be07a8ea5b87b468c5991b7540c4f`.
- `git merge-base --is-ancestor b48ac03ef origin/develop` => YES (the fix is an ancestor of the exact base head).
- `git log --oneline origin/develop..HEAD` is N/A (no new candidate commits; no branch was cut).

## END

END_DONE w243-0428-243-static-cell-grant-access: 0428-243 primary defect already fixed on develop by b48ac03ef (#1771), an ancestor of dc8626e9; existing cmd/baha shard passes and is CI-home under cli-package-tests; no product change or PR. Candidate SHA: n/a (no branch cut; fix = b48ac03ef on origin/develop dc8626e9).
