# PR #1575 Review R7 (r6 correction: Perses field present on remote-target status)

## PLAN

1. Read r6 akte (act-1575-review-r6.md, plan main 1f3dc0da): two blockers — remote-target early-return omits perses + omitempty; #1577 wording cross-check; an internal inconsistency in the #1575 candidate's own docs.
2. Set `Perses` before the remote-target early return; drop the duplicate local declaration.
3. Add a positive is-equality assertion on the parsed `app status --json` `Perses` field (like the local root-status assertion).
4. Align the internal `management-access-v1.md` bullet with the three-state vocabulary.
5. Local build/vet/tests; exact-headed hosted CI terminal PASS; round-7.md; push candidate + evidence to planning origin/main; END.

## Provenance

Fresh clone at `/tmp/opencode/mission-1575-r4`. `git ls-remote`:

```text
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
a5a5abed6a2a3d65b90768530374a304c9931656	refs/pull/1575/head (current)
```

`git merge-base --is-ancestor 0e9ccb582f5bdcdc74049bbe3996263cdce6500c a5a5abed` succeeded. Branch head (ls-remote witness):

```text
ls-remote refs/heads/lane-0428-075-perses-seam   -> a5a5abed...
ls-remote refs/pull/1575/head                    -> a5a5abed...
```

Only the named #1575 candidate chain sits on top of develop:

```text
a5a5abed fix(0428-075): set Perses field before remote-target early return (r7)
28492bd1 fmt(0428-075): gofmt perses.go constants
181872c9 fix(0428-075): expose Perses three-state contract in public status JSON (r5)
792c921c ci(0428-075): re-trigger hosted CI for exact head c195a9a (r4)
c195a9a2 test(0428-075): execute the genuine baha status path for the Perses seam + unknown-owner fail-closed (r3)
dc670bfd fix(0428-075): ground Perses seam in manifest truth, fail-closed + unverified reachability
61f76fa1 feat(0428-075): define optional Perses provider seam (fail-closed)
```

## What r6 required and how it is satisfied

### Remote-target early return — fixed

Before, `cmd/baha/app_status_result.go` computed the Perses state only after the
local state computation and returned the remote-target result early, before the
field was set:

```go
if hasRemoteApplicationTarget(resolved) {
    return applicationStatusResult{...}, nil   // Perses left nil → omitempty drops it
}
// persesStatus := ... (only reached for the local path)
```

The fix computes `persesStatus` from manifest truth **before** the remote-target
early return and assigns it to both return arms:

```go
persesStatus := capability.PersesStatusNow(resolved.Manifest.Services.ObservabilityManagementUI && resolved.Manifest.Services.Perses)
if hasRemoteApplicationTarget(resolved) {
    return applicationStatusResult{..., Perses: persesStatus}, nil
}
```

The value is manifest-declaration truth (`PersesStatusNow`), so no remote
health assumption is made: a selected + validly pinned remote manifest reports
`configured_unverified`, an unselected one reports `not_configured`.

Note: in practice a remote target only reaches this early return when a valid
Core connection profile is present — `resolveApplication` fails closed on a
missing `BASEHARBOR_CONNECTION_PROFILE` before the status collector runs (see
`app_remote_status.go`, `management_remote_connection.go:77-87`). The field-set
before the return is therefore defensive correctness for the remote face, kept
so the public JSON contract holds on every status path.

### Positive is-equality coverage on `app status --json`

`TestBahaStatusPersesCLIEntrypointResolvesWithoutContainer` now additionally
asserts `assertPersesConfiguredUnverified(t, appReport)` on the parsed
`app status --json` field — direct is-equality coverage of the app-status JSON
field for the selected + no-health case, not only through the root-status
surface. Existing tests `TestBahaStatusPersesConfiguredUnverifiedPositive`
(selected → `configured_unverified`) and
`TestBahaStatusPersesNotConfiguredWhenUnselected` (unselected →
`not_configured`) cover the other two states.

### #1577 wording — internal alignment

The #1577 PR is a separate draft (HEAD `29dba54d`) and was **not** edited — its
docs change is a follow-up that its own lane must land before its own review.

The internal inconsistency in the #1575 candidate's own
`docs/spec/management-access-v1.md:41-43` (which called the unprovisioned case
`unsupported` / "never as configured") is fixed to match the three-state
vocabulary: a selected but unprovisioned surface is reported
`not_configured` (fail-closed), never `configured_unverified` or `verified`.
The three-state block (`:50-61`) already used the correct names.

## Hosted run

Exact headed CI run `43659466298` on commit `a5a5abed`, status Success, total
duration 5m 14s (triggered via PR #1575 synchronize, 15 Nov 2026 00:41). Draft
selection skips the runner-interface / PR Selected Checks jobs (expected); all
other jobs — PR Trusted Plan, PR Native impact selection, PR Source format, PR
Draft source and routing (5 Go shards), PR Public Contracts (selected runtime),
PR Native Greenfield two-engine proof, PR Focused Python, Release Source
Preflight, validate — concluded success. No failing or cancelled check observed.

## Local verification

Go toolchain from go.mod. On the exact candidate working copy (`a5a5abed`):

```text
go build ./...                                          -> exit 0
go vet ./cmd/baha/ ./internal/application/ ./internal/capability/
gofmt -l (Go files)                                     -> clean
go test ./cmd/baha/ -run "Perses"                       -> ok
```

All perses tests pass: `TestBahaStatusPersesSurfaceFailsClosedAndUnverified`
(selected + unselected-fail-closed),
`TestBahaStatusPersesSurfaceReachableOnlyWithObservabilityManagementUI`,
`TestBahaStatusPersesCLIEntrypointResolvesWithoutContainer`
(now with direct `appReport.Perses` equality),
`TestBahaStatusPersesUnknownOwnerFailsClosedThroughCLI`,
`TestBahaStatusPersesReportsUnsupportedAuthThroughCLI`,
`TestBahaStatusPersesConfiguredUnverifiedPositive`,
`TestBahaStatusPersesNotConfiguredWhenUnselected`,
`TestPersesReleaseFailClosedOnUnknownAuthClass`.

## repo-rule compliance

Evidence is in the actual planning repository, not the workers bookkeeping
checkout. Product remote state was measured from a fresh clone and
`git ls-remote`; the quarantined stale-ref checkout was not used. No workflow
files were edited, no runner infrastructure was built or repaired, no
containers were started, and no `.github/**` was touched. The #1577 PR was left
untouched (separate draft). The candidate branch head is exactly
`a5a5abed...` and PR #1575 stays DRAFT (merge frost honoured). No second branch
was invented for the same card; the correction landed on the named candidate
branch.

## END DONE
