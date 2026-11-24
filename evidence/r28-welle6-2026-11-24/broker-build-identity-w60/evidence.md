# 0428-271 · broker-build-identity-commit (w60)

State: BLOCKED (catalog-baseline / 0428-274)
Card: t-20261124-r28-broker-build-identity-commit
Owner: w60-0428-271-brokerid
PR: https://github.com/mcpdev80/baseharbor/pull/1820

## Plan

- Read task note + `python3 scripts/plan.py show t-20261124-r28-broker-build-identity-commit`; branch `fix/broker-build-identity` cut off develop 3ebfb90d (ancestor-verified via `git merge-base --is-ancestor`).
- Write-set disjoint check: `verifyRuntimeBrokerBuildIdentity` lives in `cmd/baha/app_broker.go` (lines 652-676), disjoint from `cmd/baha/app_status_result.go` (#1818), `internal/metrics/perses_dashboard_provision.go` (#1819) and operatorauth (#1818/1819 owner restructuring). No QUESTION needed.
- Fix: replace the two-line discard `_ = expectedCommit / _ = actualCommit` with a fail-closed commit comparison: when CLI and broker both report a concrete, differing commit, return `errRuntimeBrokerIncompatible`. dev/edge pair with an empty commit stays green. Semver check untouched (not weakened).
- Regression test `TestVerifyRuntimeBrokerBuildIdentityCommitMismatch` in `cmd/baha/app_broker_compat_test.go`: same+same passes, same+wrong-commit fails, empty runtime commit stays green.
- Build (`go build ./cmd/baha/`) + `go vet ./cmd/baha/` both clean.
- Push exact head; PR #1820 opened, marked ready-for-review for exact-hosted CI.

## Fix (cmd/baha/app_broker.go)

Old (discard):

```go
// Commit SHAs are build provenance, not a runtime compatibility contract.
// Patch-only/docs-only CLI rebuilds may legitimately differ from the
// published runtime image while still speaking the same versioned API.
_ = expectedCommit
_ = actualCommit
return nil
```

New (fail-closed, documented):

```go
// Commit SHAs are build provenance. A development CLI (the `dev`/`edge`
// build pair) may legitimately run a runtime image built from a different
// commit, so a single empty commit never fails the probe. Outside that
// pair, the readiness path fails closed when both sides report a concrete
// commit and they disagree: a wrong-commit broker must not pass readiness
// on a matching semver alone. See verifyRuntimeBrokerBuildIdentity.
if expectedCommit != "" && actualCommit != "" && expectedCommit != actualCommit {
    return fmt.Errorf("%w: runtime build commit %s incompatible with CLI commit %s",
        errRuntimeBrokerIncompatible, actualCommit, expectedCommit)
}
return nil
```

## Write-set

- `cmd/baha/app_broker.go` (fix)
- `cmd/baha/app_broker_compat_test.go` (regression)
- No `scripts/**`, no `.github/**`.

## Evidence / CI

- Branch head (ls-remote): `f5e50f5a33fc8c50ef2104d243a36412567d522e`
- PR head (ls-remote): `refs/pull/1820/head => f5e50f5a`
- `git diff origin/develop..HEAD --name-only`: only `cmd/baha/app_broker.go` + `cmd/baha/app_broker_compat_test.go`
- `git log --oneline origin/develop..HEAD`: single commit `f5e50f5a`
- Exact-hosted CI (PR #1820, ready-for-review, run 45322761411):
  - `PR · Go unit => SKIPPED` (package-discovered; would run under the "PR · Go unit" group, trigger `pull_request` + `draft == false`)
  - `PR Selected Checks => SKIPPED / FAILURE (aggregate)`
  - `Trusted Plan => FAILURE`: uncataloged source `cmd/baha/app_broker_compat_test.go`. This is a `scripts/**` coverage-catalog row — owner-scope per #1817. Not my write-set.

## Catalog block (0428-274, owner baseline)

- `Trusted Plan` fails on the uncataloged regression test file. The catalog row for `cmd/baha/app_broker_compat_test.go` must be added to the coverage catalog, which is owner-scope (`scripts/**`, #1817 precedent).
- I did NOT add a catalog row. Filed 0428-274 (owner catalog-baseline) for exactly that row.
- On 0428-274 landing on develop: `git fetch` develop, `git switch --force-rebase` onto new develop head, push, mark #1820 ready, re-run exact-head CI.

## Cleanliness

- No containers/compose started. No `docker`/`podman` state. Host clean.

## End

END_DONE w60-0428-271-brokerid: CARD BLOCKED on 0428-274 catalog baseline. Fix + regression + build/vet complete; PR #1820 head f5e50f5a; CI Trusted Plan SKIPPED Go unit / FAILED on uncataloged test row (scripts/ owner-scope, #1817). Rebase + rerun on 0428-274 land.
