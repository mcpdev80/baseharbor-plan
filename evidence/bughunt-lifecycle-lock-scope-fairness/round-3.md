# CODEX-REVIEW 0427-176 r3 — PR #1507

## Candidate and hosted evidence

- PR #1507 head after r3 (rebased on current develop): `bf7e7d3ecf8160ce4077c41bbc8768b5549d4066`.
- Base: develop `fe16127ac19526e7ed287fd8d4d3428fa2a4f174`; `git merge-base
  --is-ancestor fe16127ac … bf7e7d3e` returned 0 — develop is an ancestor of the
  candidate, drift 0 before acceptance.
- `git ls-remote origin develop` confirmed `fe16127ac…`; `git ls-remote origin
  0427-176-lockfairness` confirmed `bf7e7d3e…`.
- Hosted run `42598253700` (event `pull_request`, base `develop`, non-draft) is
  terminal `completed/success` on the exact head `bf7e7d3e`.
- Prior run `42596428831` was terminal `completed/success` on `8dc5a9193` (the
  pre-rebase r3 commit).

## CI job results (run 42598253700, head bf7e7d3e)

- `PR · Validation · go-unit-tests` (job 42598253700): success — ran the F1/F2
  tests, the 3 rollback regressions, and the 3 new F3 production regression tests
  on the exact head.
- `PR · Validation · go-vet`, `PR · Validation · go-build`, `PR · Validation ·
  cli-gofmt`, `PR · Validation · pages-candidate-build`: success.
- `PR · Native destroy retry · docker` (129071806661-class) and `podman`: success.
- **`PR Selected Checks`: success** — terminal acceptance gate.
- 12 non-success jobs are all `skipped` (Release Source Preflight, Targeted HA
  docker/podman, pins, Native Keycloak/Core, Selected Runtime, Public Contracts,
  Runner Interface, Exact Candidate) — the non-required gates, reported honestly.

## What r3 implements (verdict act-1507-review-r2 F3)

### Exported target-wide production acquire path
- `internal/stableid/lock.go::AcquireTargetWideLifecycleLock(root)`: holds the
  shared `.installation.lock` EXCLUSIVELY for the whole whole-Target lifecycle
  mutation, scans the deployments namespace for held per-app dotfiles while
  holding it, and fails closed on an active app lifecycle OR a scan error. The
  same critical section that the per-app dotfile creation takes means direction 2
  (a new app cannot begin during a held scan) holds automatically.
- Re-exported in `internal/coreinstallation/lifecycle_lock.go::
  AcquireTargetWideLifecycleLock` with the same production signature.

### Fail-closed scan
- `internal/stableid/lock.go::deploymentsHaveAppLocks` now returns `(bool, error)`.
  A MISSING deployments namespace (never-staged/remote target) is an empty scan
  (no active app); any OTHER read error (permission, I/O, truncated directory)
  fails closed. The verdict point "a scan error must not count as an empty scan"
  is now enforced.
- `AcquireAppLifecycleLock` takes `.installation.lock` as a brief critical section
  before creating its per-app dotfile, so a new app fails fast on flock
  contention while a target-wide scan holds the lock; unrelated apps still
  converge in parallel (each holds its own dotfile, releases the target-wide lock
  immediately).

### Production integration
- `cmd/baha/application_lifecycle_lock.go` else-branch (remote/destroy/stop/
  control-plane target-wide seam) routes through `coreinstallation.
  AcquireTargetWideLifecycleLock` (no retry loop — a held app is a genuine
  conflict, fail closed).
- `cmd/baha/target_definition_change.go::lockExistingTargetDefinitionLifecycle`
  routes through the scan path.
- Bootstrap/provider-upgrade `AcquireLifecycleLock` callers
  (serviceaccess/local_issuer, coreinstallation/management_host,
  coreinstallation/installation, application/shared_backends*, update_ha_recovery,
  update_core_native) are intentionally unchanged — different lock purpose.

### Both-direction production regression (test-side + hosted)
- `TestProductionTargetWideMutationCannotOverlapLocalAppLifecycle` (direction 1):
  a local app holds its per-app lock; a real target-wide mutation through the
  production seam fails closed.
- `TestProductionAppCannotBeginDuringTargetWideScan` (direction 2): while the
  target-wide path holds `.installation.lock` to scan, a new per-app lock fails
  fast; after release it begins normally.
- `TestProductionTargetWideScanFailsClosedOnScanError` (scan-error fail-closed,
  root-skipped).
- F1 (`TestIndependentAppsDoNotSerializeOnSharedTarget`) and F2
  (`TestDestroyNotStarvedByBoundedRetry`) retained.

## Verification matrix

| Check | Result |
| --- | --- |
| `go build ./...` | pass |
| `go vet ./...` (stableid, coreinstallation, cmd/baha) | pass |
| `gofmt -l` on changed files | clean |
| `go test ./internal/stableid/...` ×3 | ok (deterministic) |
| focused lifecycle + 3 rollback + 3 production regressions | pass |
| `go-unit-tests` (hosted, exact head bf7e7d3e) | success |
| `PR Selected Checks` (hosted, exact head) | success |
| drift vs develop | 0 (develop fe16127ac is ancestor) |
| new failures vs r1 baseline | zero (14 pre-existing UUIDv4 env failures on both) |

## Scope notes

- No `.github/**` file edited.
- No subagents used (AGENTS §4.8).
- The r3 branch was rebased onto current develop (fe16127ac) so drift is 0 before
  acceptance; a fresh terminal CI run on the rebased head was required and is
  green.
