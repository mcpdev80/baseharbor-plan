# Round 2 evidence — 0427-172 r2: fail-closed orphan inventory (PR #1502)

Worker session (0427-172 r2), PR #1502, branch `fix/0427-172-adopt`.

## WHAT is being developed (product language)

A BaseHarbor `up` that adopts a dead owner's leftover bootstrap marker can
mistake a **still-provisioned Core** for a **phantom target with nothing to
reclaim**, and silently consume that owner's retry claim. The adoption check
that decides "does this target actually own a provisioned Core?" was broken in
three ways:

1. The inventory context was **already canceled before the inventory ran**, so
   the engine inspection was aborted the instant it started.
2. When the engine inspection **failed** (engine down, resources unavailable),
   the check treated that failure as "no owned resources" and declared the
   target empty.
3. A **permission / I/O error** reading the target's runtime files was treated
   the same as "the files were never written".

The fix makes the decision **fail-closed**: only a genuine "files never written"
proves the Core was absent; a canceled, failed, or unreadable inventory keeps
the marker and the run fails closed, exactly like the previously fixed learning
case 163 F2.

## The fix (files, change)

`cmd/baha/runtime_integration_test_support_test.go` (the adoption helper lives
here in the PR):

- `backgroundInventoryCtx()` now returns `(context.Context, context.CancelFunc)`
  instead of a context it cancels itself via `defer cancel()`. The caller
  `destroyOrphanedBootstrapMarkers` invokes `inventoryCancel()` **after** the
  footprint inventory finished (was line 344-349 area).
- `ownedFootprintOnEngine()` no longer swallows errors from
  `ListRuntimeContainers` and `ListOwnedProjectResources`; any engine inventory
  error returns a non-nil error so adoption keeps the marker.
- `orphanBootstrapTargetHadFootprint()` now distinguishes `os.ErrNotExist` (the
  only signal that a Core was never provisioned) from every other
  `ExistingFilesForProject` error, which propagates fail-closed. A `nil`
  provider is now an unverifiable error, not `(false, nil)`.

New package-level hook `runtimeBootstrapOrphanInventoryProvider` + its wiring in
`bootstrapTeardownProvider()` lets the injected-failure regressions supply a
provider the inventory can fail through.

`cmd/baha/runtime_integration_cleanup_coverage_test.go` (new regression tests,
all pass):

- `TestBootstrapAdoptionFailsClosedOnEngineInventoryError` — a failing
  `ListRuntimeContainers` keeps the marker (fails closed), does not consume.
- `TestBootstrapAdoptionFailsClosedOnResourceInventoryError` — a failing
  `ListOwnedProjectResources` keeps the marker.
- `TestBootstrapAdoptionFailsClosedOnRuntimeFilePermissionError` — a
  non-not-found runtime-file error keeps the marker.

The mission's requested "inventory failure => refusal, not consumption" is
covered by the first two of these.

## HEALING PROOF (F3)

The candidate's own `PR · Validation · cli-package-tests` job **passed** on the
new head `e69de123d8f469ea65aa6c29b2a6110814ca8b79`. Run id
`42536968217` (event `pull_request`, conclusion `failure` overall — the failure
is the two pre-existing native destroy-retry jobs, see below). The
`cli-package-tests` step fetched develop `20902f0a6ab016fd8fe6a501751e1becc5f334dd`,
ran `go test ./cmd/baha`, and emitted

```
{"check": "cli-package-tests", "required_pass": [...], "matched_tests": ["./cmd/baha"]}
```

i.e. the **full** `cmd/baha` package (which selects the three new regression
tests) actually executed on the hosted runner and passed. This is CI routing
under the `pull_request` trigger (ci.yml, the `cli-package-tests` group runs
`BASEHARBOR_LOGS_ENABLED=false go test ./cmd/baha`).

F3 healing proof per the mission requires a **develop push** on the exact
post-merge develop head where `TestUpNameResumesThroughCommandEntrypoint`
(cmd/baha/runtime_ports_test.go:316) and
`TestControlPlaneSingleDefaultNativeRuntimeInCI`
(cmd/baha/control_plane_single_native_ci_test.go:18) run in **native Docker and
Podman** jobs and both pass — `skip` is not healing. That develop run is **not
yet produced**; the PR's native jobs (`PR · Native Keycloak/Core ·
${{ matrix.runtime }}`, run 42536968217) are `skipped`. **Until that develop
push runs and passes, this claim stays "wartet auf landing".**

## RUNNER-ISOLATION STATE (not fixed here — Owner / .github scope)

`PR · Native destroy retry · docker` (job 128903364099) and
`PR · Native destroy retry · podman` (job 128903364076) both failed at
`TestSecondSameHostCoreNativeConflictInCI` with the pre-existing marker error:

```
bootstrap leftover marker missing (teardown not guaranteed): open
/tmp/baseharbor-ci-data-1520143170/baseharbor-bootstrap-cleanup-pending: no such file or directory
```

This is the exact same failure the CODEX-REVIEW already recorded as
runner-isolation STATE; it predates this fix and is outside this lane's write
set. **No .github/** file was changed; no rerun was triggered.**

## Scope and provenance

- Changed paths only: `cmd/baha/runtime_integration_test_support_test.go`,
  `cmd/baha/runtime_integration_cleanup_coverage_test.go`. **No .github/** path.
- Base develop HEAD (ancestor): `20902f0a6ab016fd8fe6a501751e1becc5f334dd`.
  `git merge-base --is-ancestor 20902f0a6 ... <new head>` returned 0 (base is an
  ancestor of the new head).
- Branch `r172-inventoryfix` cut from `fix/0427-172-adopt` head `7ea003b87`
  (`20902f0a6` is an ancestor of `7ea003b87`). Branch log lists **only** the one
  fix commit `e69de123d8f469ea65aa6c29b2a6110814ca8b79`.
- Pushed to origin branch `fix/0427-172-adopt`; PR #1502 head is now
  `e69de123`. One integration candidate per chain.
- Local verification: `go build ./cmd/baha/...`, `go vet ./cmd/baha/`,
  `gofmt -l` all clean; `go test ./cmd/baha -run 'TestBootstrap'` and the three
  new fail-closed tests pass locally.

## CI routing / trigger summary

| Check | Run / Job | Result | Trigger |
| --- | --- | --- | --- |
| cli-package-tests (go test ./cmd/baha, selects new tests) | 42536968217 / 128903369257 | success | pull_request |
| Native destroy retry · docker | 128903364099 | failure (marker missing) | pull_request |
| Native destroy retry · podman | 128903364076 | failure (marker missing) | pull_request |
| Native Keycloak/Core (matrix.runtime) | 42536968217 / 128903370298 | skipped | pull_request |

## END

END_DONE 0427-172-r2 — fix landed on PR #1502 (head e69de123), cli-package-tests
passes on hosted runner. WARTET AUF LANDING: a develop push where
TestUpNameResumesThroughCommandEntrypoint and
TestControlPlaneSingleDefaultNativeRuntimeInCI both run in native Docker AND
Podman and pass. Native destroy-retry failures are runner-isolation STATE.

## Heil-Nachweis (coord, 2026-11-09, Landing)
- PR #1502 squash-gelandet (develop 1912734ff); karte closed. Rostblockade aufgehoben: folgende PR-gates (u.a. #1505 run 42590616765 auf base>=942111d5a) completed/success ohne die zwei benannten fails.
- Develop-push traegt nur Runtime-Core-Workflows; cmd/baha suite laeuft PR-seitig nach impact-selektor — dauerhafte Erfassung liegt beim CI-inhaber (.github scope), Befund notiert, kein Blocker.
