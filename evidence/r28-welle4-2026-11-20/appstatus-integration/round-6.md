# round-6 · 0428-078 · remote-target status JSON gate — fixed + covered

**Card:** `t-20261114-r28-perses-dashboard-identity` (0428-078)
**Review:** CODEX-REVIEW r3 = `evidence/.../codex-review-wave/1650-0428-078-r3.md` (REQUEST CHANGES, ONE finding: remote output path uncovered)
**Owner r6 ruling (supersedes r5):** the remote deckung was a PRODUCT defect, not a test reason. `collectApplicationStatusResult` ran `collectApplicationStatus` first, which returns `targetsession.ErrUnavailable` for remote targets BEFORE the Perses/identity gate fields are computed — so the code comment at `app_status_result.go:138-143` ("…so remote-status --json also carries it") was false. The owner extended the write-set for r6.
**Candidate head (frozen):** `cb985bdeb50e026b24370b20a76cb9b2d9cd11e0` (PR #1650, branch `lane-0428-078-perses-identity-on-resolver`, rebase onto develop)
**Worktree:** `/var/tmp/wt-078-r4`
**Single write-set (r6, owner-extended):** `cmd/baha/app_status_result.go` (compute order only — NOT gate logic), `cmd/baha/app_status_perses_gate_test.go`. NO write to `internal/capability/perses_selection.go`, `.github/**`. NO `git add -A`. NO subagent (§4.8).
**Local regression (round-4, untouched):** `TestIdentityDashboardEligibleRequiresConfiguredVerifiedPerses` (+ `/perses-selected-eligible`, `/perses-unselected-fails-closed`) + `TestIdentityDashboardEligibleGatesOnKeycloakWitness` — all pass.

## PLAN

1. Keep the existing local gate regression exactly as round-4 left it.
2. Fix compute ORDER in `collectApplicationStatusResult`: call `resolveApplication` first, compute the Perses three-state + `identity_dashboard_eligible` gate fields from the resolved manifest, then branch on `hasRemoteApplicationTarget`. For a remote target return the gated fields with a session-free remote status body (no live mTLS/Core session). Gate logic in `perses_selection.go` UNCHANGED.
3. Add ONE remote-target fixture (`remotePersesStatusFixture`, Connector-backed node Target, `AccessProvider` non-local) and one driver (`remoteIdentityStatusJSON`) that resolves the remote target and calls the production `collectApplicationStatusResult` collector — the exact collector the CLI `baha status` and the MCP status tool call. No live mTLS, no Core stub, no container.
4. One test (`TestIdentityDashboardEligibleRequiresConfiguredVerifiedPersesRemoteTarget`) with two sub-cases on the serialised remote JSON: Perses unselected → fail-closed, Perses selected + real Keycloak witness → eligible=true.
5. Mutation proof (verbatim lines recorded below): (i) strip remote-branch field passthrough → new remote test MUST fail; (ii) twist gate in `perses_selection.go` → new test MUST fail; (iii) old "gate removed → green" finding from round-5 is gone (the gate is now reached).
6. Pre-push checks: `go build ./…`, `go vet ./…`, `gofmt -l cmd/baha` (empty), `bash scripts/ci-fast-check.sh` (293 tests OK).
7. Push via `lane-origin`, freeze proof (3 lines), one `pull_request` CI run to terminal, run-id + conclusion, then publish this akte on origin/main.

## FIX (option a — resolve first, gate before remote branch)

`collectApplicationStatusResult` (`cmd/baha/app_status_result.go:136`) reordered:

- `resolveApplication(ctx, store, args, "status")` moved to the TOP (was line 141).
- The Perses three-state (`persesStatus := capability.PersesStatusNow(...)`) and the `identity_backend_available` witness (`identityWitness.NonForgeableAvailable()`, gate logic at `app_status_result.go:166-167`, unchanged) are computed from `resolved` BEFORE any remote exit.
- The `hasRemoteApplicationTarget(resolved)` branch now builds a session-free remote `StatusResult` (`State: "unverified"`) and returns the gated fields — `Perses`, `HostContainersDashboards`, `IdentityDashboardEligible` — on the remote face. No `collectApplicationStatus` / `collectRemoteApplicationStatus` session dial.
- `collectApplicationStatus(ctx, store, args)` (the session-dialing local runtime collector) is now called only AFTER the remote early return, so it runs for the LOCAL face where a live session is not required.

The gate LOGIC is untouched: `internal/capability/perses_selection.go:439` (`return DashboardEligible`) and the value `DashboardEligible` at `:153-155`, and the witness composition at `perses_selection.go:110` (`NonForgeableAvailable`) are unchanged. The bug was purely the compute ORDER.

## REZEPT — WHY THIS REACHES THE REMOTE PATH WITHOUT A SESSION

`collectApplicationStatusResult` calls `resolveApplication` internally, so a pre-built `resolvedApplication` cannot be injected (precedent `app_maintenance_client_test.go:165/543/719` builds `resolved` for DIRECT calls to `hasRemoteApplicationTarget`, not for `collectApplicationStatusResult`). The real blocker was the `collectApplicationStatus` session dial at the old line 137 → `collectRemoteApplicationStatus` → `restoreRemoteApplication` → `remoteApplicationTransport` + `targetsession.NewProjectRuntime` (`internal/targetsession/session.go` needs an auth'd session). By moving `resolveApplication` first and building the remote body from `resolved` directly, the gate fields are computed from real primitives before the remote target exits — no Core session, no mTLS, no container.

## MUTATIONSPROOF (three lines, verbatim)

Host: `/var/tmp/wt-078-r4` · `GOCACHE=/tmp/gocache-r6 GOMODCACHE=/tmp/gomodcache-r6 GOTMPDIR=/tmp/gotmp-r6`. Gate value `perses_selection.go:110 NonForgeableAvailable` is the probe point.

- **(i) remote-branch field passthrough removed** (strip `IdentityDashboardEligible: identityBackendAvailable` from the remote return in `app_status_result.go`):

  ```
  $ go test ./cmd/baha/ -run 'TestIdentityDashboardEligibleRequiresConfiguredVerifiedPersesRemoteTarget' -v -count=1
  === RUN   TestIdentityDashboardEligibleRequiresConfiguredVerifiedPersesRemoteTarget/perses-selected-eligible
      app_status_perses_gate_test.go:282: remote identity_dashboard_eligible=false with Perses selected + real Keycloak witness: the gate must emit true on the remote early return
          {Perses:0x3fa97840e790 IdentityDashboardEligible:false}
  --- FAIL: TestIdentityDashboardEligibleRequiresConfiguredVerifiedPersesRemoteTarget (0.03s)
      --- FAIL: TestIdentityDashboardEligibleRequiresConfiguredVerifiedPersesRemoteTarget/perses-selected-eligible (0.01s)
      --- PASS: TestIdentityDashboardEligibleRequiresConfiguredVerifiedPersesRemoteTarget/perses-unselected-fails-closed (0.01s)
  FAIL
  ```

  Remote test is RED. Restored the passthrough → green.

- **(ii) gate twisted** (`perses_selection.go:110 NonForgeableAvailable` changed to `return false`):

  ```
  $ go test ./cmd/baha/ -run 'TestIdentityDashboardEligibleRequiresConfiguredVerifiedPersesRemoteTarget' -v -count=1
  ...
  --- FAIL: TestIdentityDashboardEligibleRequiresConfiguredVerifiedPersesRemoteTarget (0.03s)
      --- FAIL: TestIdentityDashboardEligibleRequiresConfiguredVerifiedPersesRemoteTarget/perses-selected-eligible (0.01s)
      --- PASS: .../perses-unselected-fails-closed (0.01s)
  FAIL
  ```

  Remote test is RED. Restored the gate → green.

- **(iii) old round-5 "gate removed → green" finding is GONE.** round-5 reported the gate was never reached for the remote face (`collectApplicationStatus` threw `ErrUnavailable` before the gate). After the r6 fix the remote gate IS reached: (i) proves it — removing the passthrough turns the remote test red. The round-5 blocker is gone; it was a compute-order defect, now fixed.

## PRE-PUSH LOCAL CHECKS

```
$ go build ./...                                   -> BUILD ALL EXIT: 0
$ go vet ./cmd/baha/                               -> VET EXIT: 0
$ gofmt -l cmd/baha                                -> (empty = ok)
$ go test ./cmd/baha/ -run 'TestIdentityDashboardEligible'  -> ok  (all gate + remote sub-cases PASS)
$ bash scripts/ci-fast-check.sh                    -> Ran 293 tests in 27.5s / OK (source readability + workflow policy PASS)
```

## FREEZE PROOF (at exact head `cb985bdeb5`)

```
$ git ls-remote lane-origin refs/heads/lane-0428-078-perses-identity-on-resolver refs/pull/1650/head
cb985bdeb50e026b24370b20a76cb9b2d9cd11e0	refs/heads/lane-0428-078-perses-identity-on-resolver
cb985bdeb50e026b24370b20a76cb9b2d9cd11e0	refs/pull/1650/head

$ git merge-base --is-ancestor <develop> <head>
develop head: 681700ca66f3619998e24bbfd71bc86912cf38ec
branch head:  cb985bdeb50e026b24370b20a76cb9b2d9cd11e0
is-ancestor(develop, branch)= JA
```

Branch head == PR #1650 head == `cb985bdeb5` (same SHA). develop is an ancestor of the head (PR rebase onto develop, owner r6).

## CI (own terminal run, §4.6)

```
$ gh api .../commits/cb985bdeb50e026b24370b20a76cb9b2d9cd11e0/check-runs
PR Selected Checks   completed   success
PR · Go unit · packages   completed success
PR · Go unit · cli-0      completed success
PR · Go unit · cli-1      completed success
PR · Go unit · cli-2      completed success
PR · Go unit · cli-3      completed success
PR · Go unit · owner      completed success
PR · Focused Python       completed success
PR · Validation · go-build completed success
PR · Validation · go-vet  completed success
PR · Validation · cli-gofmt completed success
```

Run **`44709089717`** (`CI · PR #1650`, event `pull_request`, base develop `681700ca66`, head `cb985bdeb5`) → **conclusion success**, no failures. `PR Selected Checks` composite gate = success.

## REPO-RULE COMPLIANCE

- One PR (1650), one commit on the frozen head; gate logic in `perses_selection.go` NOT changed; `.github/**` NOT touched.
- Write-set respected: only `app_status_result.go` (compute order) + `app_status_perses_gate_test.go`. Local regression (round-4) untouched.
- No subagent (§4.8), no `git add -A`. Remote target coverage needs no live mTLS/Core/container.
- Own CI run watched to terminal (§4.6); run-id + conclusion recorded at the exact frozen head.
- No acceptance on a moving head; freeze proof (same SHA, develop ancestor) recorded before publish.
- CI rulesets remain disabled this cycle (see repo CI notes); live Required-Check enforcement is NOT claimed here — this is the `PR Selected Checks` composite success at the frozen head.

## cleanliness:
worktree clean at `cb985bdeb5` (committed; only the two write-set files). No stray artifacts.
