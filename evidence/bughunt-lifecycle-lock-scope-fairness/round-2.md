# CODEX-REVIEW 0427-176 r2 — Korrektur (act-1507-review.md, plan 721eb449)

## Candidate and hosted evidence

- PR #1507 head after r2: `425cf9d2a98edd04a8aab8bb10556109e71c378a`
  (`cmd/baha/application_lifecycle_lock_test.go` + `internal/stableid/lock.go` +
  `internal/stableid/lock_test.go`).
- Live develop: `942111d5a1c43f5257bf1627a966fa9e6c6f24bd`; `git merge-base
  --is-ancestor 942111d5a … 425cf9d2a` returned 0 — develop is an ancestor of the
  candidate, no drift.
- `git ls-remote origin develop` confirmed `942111d5a…`; `git ls-remote origin
  0427-176-lockfairness` confirmed `425cf9d2a…`.
- Hosted run `42590829681` (event `pull_request`, base `develop`, non-draft) is
  terminal `completed/success` on the exact head.

## CI job results (run 42590829681)

All required ordinary jobs passed; skipped jobs are the non-required
Release/Source-pin/Selected-runtime gates (reported honestly, not counted as
failure):

- `PR · go-unit-tests` (job 129071833206): success — ran the corrected F1/F2 and
  the new F3 test on the exact head.
- `PR · go-vet`, `PR · go-build`, `PR · cli-gofmt`, `PR · Focused Python`,
  `PR · Native impact selection`, `PR · Trusted Plan`, `PR · Source format`,
  `PR · Workflow policy`, `PR · documentation-audit`, `PR · pages-candidate-build`,
  `PR · mkdocs-en-strict`, `PR · mkdocs-de-strict`, `PR · authority-package-tests`:
  success.
- `PR · Native destroy retry · docker` (129071806661) and
  `PR · Native destroy retry · podman` (129071806701): success — same-key
  destroy contention verified under both runtimes on the corrected head.
- **`PR Selected Checks` (129076063745): success** — terminal acceptance gate.

No `.github/**` file was edited in this task.

## What the three corrections prove

### BLOCKER 1 (F3) — proven cross-operation coordination (implementation)
`internal/stableid/lock.go::AcquireAppLifecycleLock` now creates the per-app
dotfile `<root>/deployments/.<scope>.app_installation.lock` inside a brief
exclusive critical section guarded by the shared target-wide owner lock
(`.installation.lock` under `<root>`). The `.installation.lock` is released
immediately after creation (only the per-app dotfile persists as the active
signal), so unrelated apps still converge in parallel. A target-wide mutation
(stop/destroy of the whole target, or a Target-definition change) takes the same
`.installation.lock` exclusively and scans the deployments namespace for per-app
dotfiles via `deploymentsHaveAppLocks(root)`, so it can never overlap a local app
lifecycle while unrelated apps still converge in parallel. The returned unlock
releases the per-app dotfile and deletes it so the scan no longer sees it.
Proven by the new test `TestLocalAppLifecycleCannotOverlapTargetWideMutation`:
a local app holds its per-app lock while a target-wide scan observes it and
refuses; a target-wide scan blocks a concurrent local app from dotfile creation.

### BLOCKER 2 (F1) — prove parallel acquisition, not serialized
`TestIndependentAppsDoNotSerializeOnSharedTarget` now holds alpha via an explicit
cleanup release channel, acquires beta in a goroutine, and asserts beta's acquire
signal fires while alpha is still held under a 3 s deadline. Regression-checked:
routing both IDs through one target-wide key makes this test fail.

### BLOCKER 3 (F2) — destroy competes on the same key
`TestDestroyNotStarvedByBoundedRetry` now uses the SAME deployment ID for the
up-holder and the destroy, proves the destroy observes a held lock (via a
non-blocking `AcquireAppLifecycleLock` probe) before the holder releases, then
acquires within the documented finite bound. Regression-checked: differing keys
make this test fail.

## Rollback regressions retained (all pass on corrected head)

- `TestRemoteUnsupportedProviderDisclosesCurrentImpactBeforeTechnicalDenial` —
  remote unsupported disclosure stages no local lock state.
- `TestCoreStopCLIJSONAndMCPExposeSameCurrentScopeWithoutEnvironmentConsentReuse`
  — core-stop consent remains scope-bound.
- `TestW138DestroyAfterRefusedReturnsZero` / `TestW138DestroyNeverDeliveredNoComposeReturnsZero`
  / `TestW138MissingRecordAfterPersistenceMustNotClaimNeverDelivered` /
  `TestW138DestroyWithoutYesPreservesNeverDeliveredProof` — never-delivered stays
  proof-gated and fail-closed.
- `TestSharedConsumersSerializeOnAppOwner` — same-app exclusion unchanged.

## Verification matrix

| Check | Result |
| --- | --- |
| `go build ./...` | pass |
| `go vet ./internal/stableid/... ./cmd/baha/...` | pass |
| `go test ./internal/stableid/...` ×5 runs | ok (deterministic) |
| focused lifecycle + 3 rollback tests (cmd/baha) | pass |
| `go-unit-tests` (hosted, exact head) | success |
| `PR Selected Checks` (hosted, exact head) | success |
| drift vs develop | develop is ancestor, no drift |
| new failures vs r1 baseline | zero (14 pre-existing UUIDv4 env failures on both) |
