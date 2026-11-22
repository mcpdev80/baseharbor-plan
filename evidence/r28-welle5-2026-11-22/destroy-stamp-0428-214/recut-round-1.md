# 0428-214 recut round 1 (destroy-authority, additive on develop 6930872c5)

## Task
Recut PR #1738 (`test(0428-214): assert installation.destroy admitted mode through the real boundary`)
cleanly on fresh develop, additive single-file diff vs develop on
`cmd/baha/core_installation_runtime_test.go`. Card precondition "recut after #1750"
satisfied (#1750 = f6d3fc5c merged). Stale mission `0428-214-r5-bothdirections`
(rebase onto retired #1726, no-merge) SUPERSEDED. No new PR — 0428-214 is a recut
of a merged artifact; evidence + END to `9142ab1f`.

## Base
- Fresh lane `lane-0428-214-destroystamp-recut` at exactly `6930872c5` (develop HEAD),
  `git merge-base --is-ancestor 6930872c5 HEAD` = true, `git log origin/develop..HEAD` empty.
- Base SHA witness: `6930872c5 ci(0428-248): catalog cmd/baha/core_installation_runtime_test.go in the data-capabilities module (#1781)`.
- Note: task listed develop `31aededf`; develop is now `6930872c5`, 3 commits ahead of
  `31aededf`. `git diff 31aededf 6930872c5 --stat` = only `scripts/pr-gate-coverage.json`
  + `scripts/test_pr_native_gate_plan.py` (CI/scripts). Product code identical, so the
  recut behaves identically at either SHA.

## Recut finding (why the original PR diff does not pass as-written)
The original PR #1738 diff (head `2ba70a587`) adds two things to
`cmd/baha/core_installation_runtime_test.go`:
1. Extra operator-auth assertions inside `TestCoreBootstrapFixtureCleanupContextIsBoundToItsLocalTarget`
   (already green on develop — applied verbatim).
2. New test `TestCoreBootstrapFixtureDestroyRunsThroughInstallationApplicationScope`.

The original new test calls `buildRuntimeDestroyImpact(ctx, ..., true)` with an unverified
`ctx` (plain `t.Context()`) and asserts a confirmed `installation.destroy` scope admits
through the destruction-planner seam, and that missing consent fails closed with
`impact-confirmation-required`.

On current develop this FAILS before the scope claim is reachable:
- `buildRuntimeDestroyImpact` with `all=true` iterates deployments and calls
  `authorizeMCPOperation(ctx, "installation.destroy", ...)` per deployment.
- `authorizeMCPOperation` → `authorizeApplicationOperation` routes through
  `ensureOperatorAuthForBoundary` (operator_auth_boundary.go:55), which in a managed
  environment fails closed with
  `Managed-environment machine operations require an authenticated BaseHarbor operator`
  when no verified operator principal is in context.
- Reproduced on BOTH `31aededf` and `6930872c5` (same product code): the original test
  exits at the operator-auth seam with the managed-environment error, never reaching the
  `installationApplicationScope` claim.

## Recut fix
Establish the production operator-auth context the real `installation.destroy` operation
proves, on `t.Context()` before the fixture, so the fixture's own internal context
resolves the same seam:
```go
ctx := operatorauth.WithEnforcement(t.Context())
ctx = operatorauth.WithVerifiedPrincipal(ctx, &identity.Principal{
    Issuer: "https://issuer.example",
    Subject: "installation-destroy-operator",
    IssuerVerified: true,
    Groups: []string{"editor"},
})
ctx = operatorauth.WithMembershipProvider(ctx, &readGrantingMembershipProvider{})
```
Then pass that `ctx` to both `buildRuntimeDestroyImpact` calls. The `readGrantingMembershipProvider`
resolves the verified editor principal to a granting membership, exactly as the production
`installation.destroy` path does. The rest of the test (confirmed admits through the
destruction-planner seam; missing consent → `impact-confirmation-required`) is unchanged.

## Evidence (local)
- `go vet ./cmd/baha/` clean.
- `go build -o /tmp/baha-recut ./cmd/baha/` clean (binary produced).
- `go test ./cmd/baha/ -run 'TestCoreBootstrapFixtureCleanupContextIsBoundToItsLocalTarget|TestCoreBootstrapFixtureDestroyRunsThroughInstallationApplicationScope' -count=1 -v`:
  ```
  === RUN   TestCoreBootstrapFixtureCleanupContextIsBoundToItsLocalTarget
      core_installation_runtime_test.go:339: fixture cleanup admitted installation.destroy by operatorauth mode=authenticated subject=core-bootstrap-cleanup issuer=https://fixture.invalid methods=[]
  --- PASS: TestCoreBootstrapFixtureCleanupContextIsBoundToItsLocalTarget (0.01s)
  === RUN   TestCoreBootstrapFixtureDestroyRunsThroughInstallationApplicationScope
      core_installation_runtime_test.go:407: confirmed installation.destroy scope admitted through the destruction-planner seam
      core_installation_runtime_test.go:428: missing consent rejected with impact-confirmation-required
  --- PASS: TestCoreBootstrapFixtureDestroyRunsThroughInstallationApplicationScope (3.17s)
  ok      github.com/mcpdev80/baseharbor/cmd/baha
  ```
- Full `go test ./cmd/baha/ -count=1 -v` (1552 tests): **1552 PASS, 2 FAIL**.
- The 2 failures are PRE-EXISTING ENVIRONMENTAL, confirmed to fail identically on a clean
  `31aededf` baseline (no recut commit applied):
  - `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` —
    "baseline workload-only lifecycle failed: The application workload failed to start."
    Requires a live docker/podman workload; cannot start in this sandbox.
  - `TestPrepareStagedCoreGitCandidatePinsCanonicalApplication` —
    "stage pinned Core candidate: native Git archive failed: signal: killed"
    `git archive` subprocess is OOM-killed by the sandbox (60s timeout).
- Neither failure touches, imports or depends on the destroyed-authority recut; they are
  sandbox runtime limitations, not regressions. Local full `cmd/baha` is the standing
  evidence gate for this recut (no push-triggered hosted Trusted Plan / four data-capabilities
  CI jobs, since this is a recut of the already-merged #1750, not a new PR).

## Repo-rule compliance (baseharbor)
- Single-file additive diff vs develop: `cmd/baha/core_installation_runtime_test.go` only.
- No touched files outside the intended test. No `.github/operatorauth/237` touch.
- No rebase on retired #1726; no 275-commit stale head (`7e679293`).
- `internal/operatorauth`, `cmd/baha/operator_auth_boundary.go` read-only; only the
  test file written.
- No new test outside the data-capabilities module catalog without a catalog trigger;
  the file is already in the data-capabilities module (PR #1781), so CI runs it.
- No subagents used.

## Status: DONE
- Lane `lane-0428-214-destroystamp-recut` pushed to origin, head `2e654a131` (one own commit,
  fresh develop base `6930872c5`).
- Local green: go vet + go build clean; 1552 pass / 2 fail, both pre-existing environmental
  (baseline-confirmed).
- Akte published to baseharbor-plan origin/main (658915cfa).
- END to `9142ab1f`. This 0428-214 is a recut of the merged #1750 — no new PR opened;
  base develop work already landed in #1750. No subagents; no .github/operatorauth/237 touch.
