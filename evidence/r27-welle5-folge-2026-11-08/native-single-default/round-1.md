# 0427-156 DIAGNOSE — Native single-default test cause analysis (round 1)

- Lane: mission-156-diag (worker session)
- Date: 2026-11-08
- Task: 0427-156 DIAGNOSE — pure cause analysis, no fix, no PR, no product change, no CI change
- Hosts: read-only (no changes on any host)
- No subagents executed (4.8)

## TASK (verbatim from mission file, translated)

develop `8ecd1ea5d` has two red push cells (native single-default docker run 42485190712 + podman 42485190770, `TestControlPlaneSingleDefaultNativeRuntimeInCI bootstrapleftovermarkermissing`).

Assignment:
1. Read job-logs of both runs, note exact failure location + message chain (file:line in the test, expected marker path, timing of disappearance).
2. History comparison: did the test pass at `d30de3a4a`/`cd494610c`/`223042bc0`? (runs of the respective pushes), narrow down WHICH merge tipped the behavior.
3. Document hypothesis assigned with proof line-for-line, not guessing.
4. Decision proposal: which of the three card domains carries the fix.

## 1. Exact failure location + message chain

Both runs (`42485190712` docker, `42485190770` podman) are from the **same push** = `develop` #973. Both fail at the SAME step with the SAME message:

```
control_plane_single_native_ci_test.go:31: prepare BaseHarbor integration trust plane:
  bootstrap leftover marker missing (teardown not guaranteed):
  open /tmp/baseharbor-ci-data-3702801192/baseharbor-bootstrap-cleanup-pending:
  no such file or directory
```

Docker run (`42485190712`), log line:
- `control_plane_single_native_ci_test.go:31: prepare BaseHarbor integration trust plane: bootstrap leftover marker missing (teardown not guaranteed): open /tmp/baseharbor-ci-data-3702801192/baseharbor-bootstrap-cleanup-pending: no such file or directory`

Podman run (`42485190770`), log line:
- `control_plane_single_native_ci_test.go:31: prepare BaseHarbor integration trust plane: bootstrap leftover marker missing (teardown not guaranteed): open /tmp/baseharbor-ci-data-2288908417/baseharbor-bootstrap-cleanup-pending: no such file or directory`

Timing:
- Docker: test `start` → `run` at `2026-11-08T13:31:01.095Z`, `fail` at `13:31:01.103Z`, elapsed `0.00s`. The test failed **immediately**, before any docker/podman interaction.
- Podman: same shape at `2026-11-08T13:31:09.965Z`, elapsed `0.00s`.

The failing line numbers trace as follows:
- `control_plane_single_native_ci_test.go:31` → `ensureRuntimeIntegrationTrustPlane(t, ctx)`
- inside `runtime_integration_test_support_test.go`: line 452 `if err := ensureBootstrapLeftoverMarker(); err != nil {`
- `ensureBootstrapLeftoverMarker()` at line 577-589: `bootstrapLeftoverMarkerPath()` returns a path (non-empty), then line 582 `os.ReadFile(marker)` fails with `no such file or directory`, returned at line 584: `bootstrap leftover marker missing (teardown not guaranteed): %w`.

The expected marker path is `<data-root>/baseharbor-bootstrap-cleanup-pending`. The data root is the `XDG_DATA_HOME` temp dir set by the fixture at `runtime_integration_test_support_test.go:423` (`XDG_DATA_HOME=/tmp/baseharbor-ci-data-<rand>`), created by `os.MkdirTemp`. That directory EXISTS; the marker file INSIDE it does not.

## 2. Mechanism (why the marker is missing)

`ensureBootstrapLeftoverMarker()` requires the marker to exist AND to be owned by the current PID. The marker is written by `claimBootstrapLeftoverMarker()` which `TestMain` calls in `runRuntimeIntegrationTestMain()` at line 104 — but ONLY when `setupBootstrapLeftoverMarker()` returns a non-empty path.

`setupBootstrapLeftoverMarker()` (`runtime_integration_test_support_test.go:148-158`):

```go
func setupBootstrapLeftoverMarker() string {
    cell := os.Getenv("BASEHARBOR_CI_RUNTIME_INTEGRATION") == "1"
    if !cell {
        return ""          // <-- non-cell runs return ""
    }
    marker := bootstrapLeftoverMarkerPath()
    if marker == "" {
        return ""
    }
    return marker
}
```

So the marker is written by `TestMain` **only when `BASEHARBOR_CI_RUNTIME_INTEGRATION=1`**. In `single_default_native`, this env is NOT set at the test step, so `TestMain` never writes the marker, yet `ensureIntegrationTrustPlane` always calls `ensureBootstrapLeftoverMarker()` unconditionally → fail-closed.

## 3. Which CI step sets the marker — and which does not

In `.github/workflows/docker-runtime-acceptance.yml`:
- Job `single_default_native` (lines 105-170) sets, at job scope:
  - `BASEHARBOR_TEST_RUNTIME: docker` (line 112)
  - `BASEHARBOR_SINGLE_DEFAULT_NATIVE_ACCEPTANCE: "1"` (line 113)
  - `DOCKER_CONTEXT: ""` (line 114)
  - **No `BASEHARBOR_CI_RUNTIME_INTEGRATION`.**
- The test runs at line 132: `go test -p 1 ./cmd/baha -run '^TestControlPlaneSingleDefaultNativeRuntimeInCI$'`.
- `BASEHARBOR_CI_RUNTIME_INTEGRATION: "1"` is set ONLY at line 152, inside the *separate* step "Validate native pinned workload lifecycle and backup" for a **different** test (`TestRepositoryComposePinnedWorkloadLifecycleInCI`), which runs AFTER the failing test.

The podman workflow `.github/workflows/podman-acceptance.yml` has the identical shape (`single_default` job at the top runs the same test without `BASEHARBOR_CI_RUNTIME_INTEGRATION`; the env is only set later on the pinned-workload step).

Cross-check of the docker-runtime job that DOES pass the whole suite: `single_default_native` and the podman `single_default` never set the cell flag for THIS test. The `docker-runtime` job passes its integration tests (`main.jsonl`) only because its `Run runtime integration tests serially` step (line 323) explicitly sets `BASEHARBOR_CI_RUNTIME_INTEGRATION: "1"`.

## 4. History comparison — which commit introduced the regression

`git log` of the test-support fixture (`runtime_integration_test_support_test.go`), newest first:
- `22a3cb8a7` [0427-127] deterministic teardown of integration trust-plane (fix bh-w169-ci-bootstrap-* leak) (#1454) — **2026-11-08 10:00**
- `beb923fe6` fix(r27 remote-up): test-scope owner loan at VerifyDeploymentOwner seam (0427-117) (#1419)
- `b11eec12f` test(ci): compose InCI tests run against per-test isolated runtime state (r27 compose-host-isolation, lane w259)
- `f314bf84d` ci(gh-hosted): publish rootful DOCKER_HOST in podman prepare; drop invalid obs scopes
- ...

`22a3cb8a7` is the commit that INTRODUCED `TestMain` + `setupBootstrapLeftoverMarker()` + `ensureBootstrapLeftoverMarker()`. It is the sole author of the marker contract. Every commit after it (including the three history points) CARRIES this contract as an ancestor.

Ancestry check (via `git merge-base --is-ancestor`):
- `22a3cb8a7` IS an ancestor of `d30de3a4a`, `cd494610c`, `223042bc0`, `8ecd1ea5d`.
- The referenced commits `d30de3a4a`, `cd494610c`, `223042bc0` are all from the same develop line dated 2026-11-08 and each already includes the `22a3cb8a7` marker contract.

Which merge tipped the behavior: the marker contract landed on develop via the PR merge for #1454 (`22a3cb8a7`, merged ~10:00 today). The `single_default_native`/`single_default` CI jobs were never updated to set `BASEHARBOR_CI_RUNTIME_INTEGRATION=1` for that test, so the **push that followed `22a3cb8a7`** on develop is the first red push. The three history points named in the mission are post-`22a3cb8a7` commits and therefore also contain the failing contract; they are not points where the test "passed before." The distinguishing commit is `22a3cb8a7`, not any of the named history SHAs.

## 5. Hypothesis assignment (line-for-line, not guessing)

Three candidate domains per the mission:

### Hypothesis A — test build / 1464-semantics (ACCEPTED, with proof)
**The test harness is mis-built for the non-cell CI job: `ensureBootstrapLeftoverMarker()` is called unconditionally, but the marker is only written when `BASEHARBOR_CI_RUNTIME_INTEGRATION=1`, which the `single_default_native`/`single_default` job does not set for this test.**

Line-for-line proof:
- Failure at `control_plane_single_native_ci_test.go:31` → `ensureRuntimeIntegrationTrustPlane` → `ensureBootstrapLeftoverMarker()` (`runtime_integration_test_support_test.go:577`).
- `ensureBootstrapLeftoverMarker()` line 582 `os.ReadFile(marker)` fails because the file does not exist.
- The file is written by `claimBootstrapLeftoverMarker()` (line 163-167) called only in `runRuntimeIntegrationTestMain()` line 104.
- `runRuntimeIntegrationTestMain` line 99-104 calls `setupBootstrapLeftoverMarker()` and `claimBootstrapLeftoverMarker()` only when the former returns non-empty.
- `setupBootstrapLeftoverMarker()` (line 149) returns `""` unless `BASEHARBOR_CI_RUNTIME_INTEGRATION == "1"`.
- The `single_default_native` job sets `BASEHARBOR_TEST_RUNTIME`, `BASEHARBOR_SINGLE_DEFAULT_NATIVE_ACCEPTANCE`, `DOCKER_CONTEXT` — but NOT `BASEHARBOR_CI_RUNTIME_INTEGRATION` (only the later pinned-workload step does, line 152).
- Result: marker path is non-empty (XDG_DATA_HOME temp dir exists) but the marker file is absent → fail-closed.

### Hypothesis B — remote-start refactor (223042bc0: no local Core bootstrap → marker never written)
**NOT the cause.** `223042bc0` ("fix(r27 remote-up): pure-client app up routes through connector, no local Core bootstrap (#1407)") is a product change on the remote-up path. The failure at `ensureIntegrationTrustPlane` happens BEFORE any product `up`/bootstrap is invoked (marker check at line 452 predates `target create` at line 479 and `up` at line 495). The marker's absence is a harness env gap, not a consequence of the pure-client routing change. `223042bc0` merely sits later on the same develop line.

### Hypothesis C — real product regression
**NOT the cause.** No product code is exercised at the point of failure. The failing assertion is a fail-closed harness precondition (marker ownership), not a runtime/control-plane assertion. The test never reaches the container/daemon layer (elapsed 0.00s).

**Assigned cause: Hypothesis A (test build / harness contract).**

## 6. Decision proposal — which domain carries the fix

The fix belongs to the **test/build domain** (the third option in the mission's framing: "new acceptance expectation in the test"), specifically to the CI job wiring, NOT to product runtime code and NOT to the 1464 test-semantics.

Concrete fix (two equivalent, both test-only):
- **Option 1 (recommended):** set `BASEHARBOR_CI_RUNTIME_INTEGRATION: "1"` at the `single_default_native` job scope in `.github/workflows/docker-runtime-acceptance.yml` (and the podman equivalent), alongside the existing job-scope env. This makes `TestMain` write the marker before the test runs.
- **Option 2:** make `ensureBootstrapLeftoverMarker()` tolerate the non-cell contract, e.g. only require the marker when `BASEHARBOR_CI_RUNTIME_INTEGRATION == "1"` (or write the marker unconditionally in `TestMain` for the non-cell path too).

Owner-scope note: Option 1 edits `.github/workflows/*` (Owner scope, 2026-11-04) — the exact needed change is reported here as a finding with file:line; the Owner applies it. Option 2 edits a test file (also test/build, not product runtime). Either way the fix is test/build, never product runtime.

## repo-rule compliance

- Read-only on all hosts: no container, compose, daemon or file changes anywhere.
- No CI workflow edits, no reruns, no workflow_dispatch (Owner scope .github/**).
- No subagents (4.8). All steps executed inside this session.
- Remote state verified via `git ls-remote` / `git fetch` / `gh` API only.
- Quarantined checkout `/home/marcel/dev/baseharbor-ecosystem/workers/baseharbor` not cited; product repo read from `/home/marcel/dev/baseharbor-ecosystem/baseharbor`.

## PLAN
- Read CI logs of both failing runs; capture exact failure location + message chain (file:line, marker path, timing).
- History comparison: confirmed `22a3cb8a7` (#1454) introduced the marker contract; all three history SHAs are post-`22a3cb8a7` develop commits carrying it.
- Hypothesis documented line-for-line; assigned to Hypothesis A (test build / harness env gap).
- Decision proposal: test/build domain carries the fix; exact change reported with file:line for Owner scope.
- Write this evidence, commit to `origin/main` in baseharbor-plan, push, post END.

## END
mission-156-diag DONE — cause = harness contract gap (TestMain writes the bootstrap marker only under `BASEHARBOR_CI_RUNTIME_INTEGRATION=1`, which the `single_default_native`/`single_default` CI job does not set for this test); fix domain = test/build, exact CI change reported with file:line.
