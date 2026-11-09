# 0427-172 r3 — bughunt-upname-entrypoint-develop-rot (native rot fix)

**Card:** 0427-172 · **PR:** [#1502](https://github.com/mcpdev80/baseharbor/pull/1502) · **Branch:** `fix/0427-172-adopt`
**Verdict basis:** `act-1502-review-r2.md` (KORREKTUR) — the native rot is a **real candidate bug**, not runner-isolation STATE.
**Author / role:** worker (0427-172 r3), 2026-11-09 · **No subagents (§4.8).**

## 1. Fund (native rot)

On CI runner (no `XDG_DATA_HOME` set), the native second-target conflict cell
`TestSecondSameHostCoreNativeConflictInCI` failed with:

```
bootstrap leftover marker missing (teardown not guaranteed):
open /tmp/baseharbor-ci-data-<n>/baseharbor-bootstrap-cleanup-pending: no such file or directory
```

Two independent defects combined:

1. **`bootstrapLeftoverMarkerPath()` had no `DataRoot()`/HOME fallback.**
   It only honoured `BASEHARBOR_STATE_DIR` and `XDG_DATA_HOME` and returned
   `""` otherwise. On the runner neither is set, so TestMain created **no**
   marker and `ensureRuntimeIntegrationTrustPlane`'s teardown found nothing.
2. **The production `TestMain` teardown removed a stale marker path.**
   `ensureRuntimeIntegrationTrustPlane()` switches `XDG_DATA_HOME` to a fresh
   per-run temp data home and carries the durable claim there; the production
   TestMain removed the marker path captured *before* that switch, so
   `os.Remove` failed with `no such file or directory` and the **FAIL-OPEN**
   package-teardown path forced exit code 1 — even though the target test
   itself passed.

`r2` was right: the marker-root mismatch is candidate code, not an environment.

## 2. Fix (candidate code only, `cmd/baha`, no `.github/**`)

Branch `r172-r3-fix` on top of PR head `e69de123d` (base develop
`20902f0a6` is an ancestor). Five commits, only two files touched:

- `cmd/baha/runtime_integration_test_support_test.go`
- `cmd/baha/runtime_integration_cleanup_coverage_test.go`

### Fix A — `DataRoot()` fallback (marker is now created)
`bootstrapLeftoverMarkerPath()` falls back to `deployment.DataRoot()` (HOME)
when neither env var is set, matching the deployment contract. Marker is always
created and always resolvable.

### Fix B — carry the claim across the data-home switch
`ensureRuntimeIntegrationTrustPlane()` captures the marker path before any
`setenv`, moves it into the per-run data home via the new `moveMarkerToRoot()`
helper, and records `runtimeIntegrationTrustPlaneDataRoot` so the teardown
re-reads the exact claim under the owned root. Both paths code-visible.

### Fix C — deterministic permission-error injection (r2 point 2)
New seam `runtimeBootstrapOrphanFileReadErr` + indirection
`bootstrapOrphanReadRuntimeFiles()` route `ExistingFilesForProject` through a
test hook. `TestBootstrapAdoptionFailsClosedOnRuntimeFilePermissionError` injects
a permission-denied deterministically (target has **no** owned projects, so the
engine inventory is never reached and the file read is the sole cause) and
asserts adoption refuses + the marker is kept. Also: `claimBootstrapLeftoverMarker`
now `MkdirAll`s the parent dir so the HOME-fallback claim dir exists on the runner.

### Fix D — remove the marker from the tracked per-run root
The production TestMain teardown now removes the durable marker from
`runtimeIntegrationTrustPlaneDataRoot` (the exact per-run root the teardown
owns), not the stale captured path. `TestBootstrapMarkerSurvivesDataRootSwitch`
proves the claim survives the switch. Panic/subprocess fixtures are unaffected
(the tracked root stays empty outside the native cell).

**Diff:** only `cmd/baha/` (two files). **No `.github/**` touched.** Base
ancestry `20902f0a6` confirmed; commit list contains only my five commits on
top of `e69de123`.

## 3. Determinism of the permission regression (r2 point 2)

`TestBootstrapAdoptionFailsClosedOnRuntimeFilePermissionError`:
- target has zero owned projects → `ExistingFilesForProject` is the **only**
  decision input reachable;
- `runtimeBootstrapOrphanFileReadErr = os.ErrPermission` forces that read to
  fail with a permission error regardless of real filesystem state;
- asserts `adoptBootstrapLeftoverMarkerFromDeadProcess()` returns an error and
  the marker still exists (fail-closed).

No injected-failure mutation can pass: removing the seam or the
`errors.Is(filesErr, os.ErrNotExist)` guard makes the test red locally.

## 4. Hosted CI — NATIVE CELLS GREEN (this run)

- **Run:** [`42546833737`](https://github.com/mcpdev80/baseharbor/actions/runs/42546833737)
- **Head:** `4362f4a16f821214774ff4a524efe6a35799d3a3` (my r3e commit)
- **Native destroy retry · docker:** job `128933577055` → **completed/success**
- **Native destroy retry · podman:** job `128933577080` → **completed/success**
- `TestSecondSameHostCoreNativeConflictInCI`: **PASS docker 60.55s / podman 67.53s**
- No `bootstrap leftover marker missing`; no `package teardown failed`; no
  `FAIL` line in either native log.

Both native jobs confirmed on head `4362f4a16f` via `gh api …/actions/jobs/…`
(`run_id` + `head_sha`). The native rot fund is fixed — **their rot was the fund
itself**, and it is GREEN this time.

## 5. F3 healing proof — PENDING (wartet auf landing)

PR #1502 is still **open** (`gh api …/pulls/1502 → state=open, mergeable=true`,
head `4362f4a1`). The F3 requirement is a **post-merge** develop push on the
exact post-merge SHA executing

- `TestUpNameResumesThroughCommandEntrypoint` and
- `TestControlPlaneSingleDefaultNativeRuntimeInCI`

in native Docker **and** Podman (**skip ≠ healing**). Until that real
post-merge run exists and both named tests execute and pass, the F3 healing
proof is **not** satisfied.

## 6. Stop criterion

Reached: native rot fund fixed, candidate GREEN on CI (native cells), evidence
published. F3 post-merge run pending on the Owner's merge — documented as
`wartet auf landing`. No `.github/**` change; one integration candidate per
chain; no subagents.
