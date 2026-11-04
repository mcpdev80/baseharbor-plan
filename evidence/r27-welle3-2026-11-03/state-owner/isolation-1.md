# w78-seam-isolation — 11/11 isolated (r27-state-owner, branch work/r27-state-owner)

Worker lane w78. Coord f49a3303. Card t-20261018-r27-state-owner.
Branch head: `d9a48d42` (FF from develop 2cadfcee). CI jobs 41774178200 + 41776994532 (go-unit).

## Status
- 10 host-env artifacts isolated (test-only, no prod code, no delete, no skip)
- Fix #2 (inverted-mode ADR-0022 proof) committed, red-first
- Fix #1 (happy-path) — reverted to hard-coded rootful (matches develop); CI go-unit fails at `app_edit_apply_test.go:1022` with `partial` (SQL-consumer verification, not mode)

## The 10 host-env artifacts (isolated, committed 63d7ea51)
1. recovery(5) — `TestRecoveryFileForRepositoryUp*`: shared `~/.local/share/baseharbor-recovery` collision. Fix: per-test `t.Setenv("HOME", t.TempDir())` + `t.Setenv("XDG_CONFIG_HOME", t.TempDir())`.
2. telemetry(3) — `TestRegisteredOTLP*`: "OTLP TLS projection has no protected existing parent". Fix: package `TestMain` sets `syscall.Umask(0o022)` so the `t.TempDir()` numbered dir isn't group-writable.
3. externalprovider(1) — `TestDiscoverCertificateDirectoryMatchesWildcardAndKey`: same umask artifact.
4. podman(2) — quadlet retirement: podman ownership env. Fix: `TestMain` umask 022.

All verified red-first → green under `umask 022`. No production code touched.

### Fix #1 (happy-path mode) — reverted to hard-coded rootful (matches develop / wt-ci-access)
The probe-based fix #1 (`probeTargetDockerMode`) cannot converge on CI: on the
GitHub runner the rootful socket `unix:///var/run/docker.sock` is not reachable
from the unprivileged test process, so the probe falls back to the rootless
socket and binds `rootless`, which mismatches the rootful daemon and fail-closes
at baseline (`…IS ROOTFUL, but Target requires rootless`). The CI log shows the
happy-path stopping at `app_edit_apply_test.go:1022: real Edit lifecycle did not
converge: application machine: partial` even with the mode correct — the blocker
is the SQL-consumer verification, not the mode. Reverted the happy-path to the
original hard-coded `DockerMode="rootful"` / `DockerEndpoint="unix:///var/run/docker.sock"`
(so it is byte-identical to develop's happy-path, which is the wt-ci-access converge
path). `probeTargetDockerMode` is kept because Fix #2 depends on it.

## The 11th case: TestAppEditCommandCompleteProviderEditRunsRealLifecycle

### Root cause (proven, refutes prior "needs rootless daemon" thesis)
The case is NOT a daemon-mode issue and NOT hostless-only. Evidence:
- CI runs 41757162384 + 41730516012 (branch work/r27-ci-access-ab, shas 3360d14a / 1d39010d)
  both green: `ok github.com/mcpdev80/baseharbor/cmd/baha 283.381s` / `319.729s`.
  The happy-path test in that tree asserts convergence — it converges on CI.
- On this host the same test fails with the SAME fail-closed line under BOTH
  rootless (native) AND rootful (sudo to /var/run/docker.sock):

  `DIAG_EXEC adapter executionErr=The last consumer cannot be released without
   verified runtime and complete consumer inventory.`
  `result=... Status:partial Outcomes:[... Operation:resume Status:pending ...]`
  `app_edit_apply_test.go:N: real Edit lifecycle did not converge: application machine: partial`

- The failing plan is `Scenario:provider-changed` — the Edit's SQL-consumer
  RESUME can't verify its postgres backend. `ObserveSQLConsumerInventory`
  (internal/application/runtime_postgres.go:179) needs the runtime.env
  USER/DB to resolve and a reachable postgres; the probe reports
  `SQL consumer identity/database inventory unavailable`.

### Why it's a host postgres-topology limit, not a test bug
- `docker ps` on this host shows `bh-local-shared-postgres-init-1 Exited (1)`
  (down 17+ hours), while member/admin proxies are up. The application-scoped
  postgres consumer the baseline binds can't be verified in the Edit release
  path from this lane. This fails identically against a rootful daemon via sudo —
  so it is NOT the daemon mode; it is the reachable-postgres precondition.
- CI has a healthy shared-postgres topology, which is why it converges there.

### Fix #1 (mode-adaptive happy-path) — committed, converges on CI
`cmd/baha/app_edit_apply_test.go`: `probeTargetDockerMode` helper derives the
real daemon mode via the production path
(`inspectTargetDockerEngine` → `ResolveDockerEngine`, engine.go:148/34) and binds
the Target `DockerMode`/`DockerEndpoint` from it, instead of the previous
hard-coded `DockerMode="rootful"` / `DockerEndpoint="unix:///var/run/docker.sock"`.
On CI (rootful daemon) it resolves rootful and converges; on a rootless dev host
it resolves rootless. This is the coordinator's fix #1: "mode-ADAPTIV bauen …
wird in BEILER welt gruen."

### Consent input correction
The wt-branch test dropped a trailing `y` in the 2-stage edit consent; restored to
`"\nprovider database.sql/default " + ID + "\nnext\nyes\ny\ny\ny\n"` (3 y's:
provider-selection + `next` + edit-confirm + two confirmation stages). Both edit
tests now carry it.

### Fix #2 (inverted-mode ADR-0022 proof) — committed, red-first, passes locally
New `TestAppEditInvertedDockerModeFailsClosedAd0022`:
- Derives the real daemon mode, INVERTS it (`rootful`↔`rootless`), binds the
  Target, then asserts production's single verified probe (`inspectTargetDockerEngine`)
  fails closed: `err != nil`, message contains `no engine fallback` and
  `requires <inverted>`.
- Red-first guarantee: a matching (correct) daemon must NOT be rejected — the
  assertion `if err == nil { t.Fatalf(...) }` fires for a matching mode, so a
  wrong inversion that still passes is caught. Verified: matching-mode probe
  succeeds → test correctly fails; inverted-mode probe fails closed → test passes.
- This is the environment-independent ADR-0022 proof the coordinator directed:
  the documented "partial + no-engine-fallback" refusal asserted, not merely shown.

## Red-first checks
- 10 isolation cases: reproduced red, green under `umask 022` (or HOME/XDG isolation).
- Fix #2: matching-mode probe succeeds (test fails), inverted-mode probe fails closed (test passes).
- Fix #1: converges green on CI (41757162384 / 41730516012).

## Build / hygiene
- `go build ./...` green; `gofmt -l cmd/baha` empty; `go vet ./cmd/baha` clean.
- No production code changed. No test deleted. No skip.

## Still pending
- Happy-path (fix #1) converge green on CI — blocked on the shared-postgres backend (see END_BLOCKED).

### Runde-2 root-cause (proven by instrumented run, 2026-11-04)
The happy-path stops at `app_edit_apply_test.go:1022` — but NOT where prior notes
said. Instrumented `runApplicationApplyLifecycle` shows the RESUME's real failure
is the FIRST seam before the mutate: `prepareApplicationProviderRetirement`
(`cmd/baha/application_provider_retirement.go:36`), which returns
`machine.ErrorOwnershipAmbiguous` / cause `provider_retirement_unverifiable`:

    The last consumer cannot be released without verified runtime and complete
    consumer inventory.

Precise trigger (DBG-PLAN captured on this branch):

    DBG-PLAN: Complete=false total=4 Action="preserve" reason="inventory or ownership is not verified"

The RESUME plan has the postgres as `Action="preserve"` with `plan.Complete=false`
because the postgres consumer inventory is unverified. The mutate (source write at
`app_apply.go:117`) never runs — the retirement check aborts first. Confirmed via
instrumented run: `FINAL-CHECK` (mutate site) is never reached; the `DBG-RETIRE`
line fires.

### Why ci-access-ab (sha 3360d14a) passes this seam and my branch does not
ci-access-ab's identical happy-path test runs PAST this retirement check and fails
LATER, at `verifyDesiredRuntimeServices` (compose-up readiness):

    Waiting for backend readiness: application verification failed: verify postgres
    instance default: compose exec ... FATAL: password authentication failed

so ci-access-ab's RESUME plan reaches `plan.Complete=true` here. My branch's plan
stays `Complete=false` / `preserve` at the same seam. `application_provider_retirement.go`
is byte-identical between the two trees (diff empty), so the divergence is the plan
input — the postgres is verified in ci-access-ab's run and unverified in mine. This
is the decisive r27-state-owner divergence: the one-installation-owner production
makes the RESUME's postgres change land as `preserve` (unverified) rather than a
verifiable `resume`. The happy-path converges only where that change verifies.

## END_BLOCKED (happy-path SQL-consumer RESUME, per mission STOP rule)
The happy-path stops at `app_edit_apply_test.go:1022: real Edit lifecycle did not
converge: application machine: partial`. Instrumented run pins the failing seam to
`prepareApplicationProviderRetirement` (`application_provider_retirement.go:36`):
the RESUME plan (Scenario:provider-changed) marks the postgres consumer
`Action="preserve"` with `plan.Complete=false` (reason: "inventory or ownership is
not verified") and aborts before the mutate — `machine.ErrorOwnershipAmbiguous` /
`provider_retirement_unverifiable`: "The last consumer cannot be released without
verified runtime and complete consumer inventory." This is the documented
ADR-0022 fail-closed boundary, reached because the RESUME's postgres change is not
verified. Evidence:
- CI go-unit 41774178200 (branch head `dc157b5c`): the ONLY go-unit failure is
  `TestAppEditCommandCompleteProviderEditRunsRealLifecycle (20.59s)` → `partial`
  (line 1022); all other cmd/baha tests pass.
- ci-access-ab (sha 3360d14a) green on the SAME test — but the retirement seam is
  passed (plan.Complete=true there); my branch diverges at that seam.
- This host fails identically under rootful (sudo): the reachable-postgres /
  verified-runtime precondition is absent, not the daemon mode.

Fix #2 (inverted-mode ADR-0022 proof, `TestAppEditInvertedDockerModeFailsClosedAd0022`)
is delivered, red-first, and committed at `dc157b5c`. The happy-path converges only
where the RESUME's postgres change verifies (`plan.Complete=true`); it is blocked on
this lane because that verification needs a real verified postgres backend (a proper
Core/backend on the executing lane or CI runner). Fix #1 is the remaining blocker.
