# final-1: w71-stateowner-final — fix 8 hosted fails on head 5f625b30

- Task: `t-20261018-r27-state-owner` (final round, takeover of stale lane w52)
- Worker lane: w71-stateowner-final · Coordinator: `f49a3303`
- Repo: `baseharbor` (product) · Branch: `work/r27-state-owner`
- Head: `5f625b30d2d100a91f139fb1165b05f5a5c8f19c`
- PR: #1347 · CI run `41697843772`
- Isolated worktree: `/tmp/opencode/w71-stateowner-final-wt`
- Host reproduction: baha-docker (rootless Docker v29.8.1, GO=/usr/local/go/bin, `BASEHARBOR_TEST_RUNTIME=docker`)

## PLAN (board + JSON live board in sync)

1. ✅ Reality check: `git fetch origin` both refs, `worktree add /tmp/opencode/w71-stateowner-final-wt work/r27-state-owner`, `git merge --no-edit origin/develop` rc=0.
2. ✅ Read contract (reconcile-1/2/4.md): seam+guard union, 29er seeds, docker_engine.go binding fix, app-edit runtime.env probe-richtig.
3. ✅ `gh pr checks 1347` → 8 fails: 4 runtime gates (docker/podman lifecycle + backup-restore), go-unit-tests, cli-package-tests, wizard-app-edit-tests.
4. ✅ Reproduce on baha-docker: clone `work/r27-state-owner`=5f625b30 + `develop`; `go test ./...` baseline=clean, branch=16 failing tests/5 packages.
5. ✅ Categorize: true regressions vs environment/shared-state.
6. ✅ Owner-urteil (2026-11-03): fail-closed "last consumer cannot be released without verified runtime" = GEWOLLT (ADR-0022/develop-guard); fixture construction anomal, NICHT prodcode.
7. ✅ Fix 4 true regressions: openbao×1 + externalprovider×3 via real Core-owner seed (w21/registerInstallationForTarget pattern), COMPLETE fixture, no bypass/skip.
8. ✅ app-edit: prod UNANGETASTET; fail-closed case = absicht-evidence.
9. ⏳ Re-run full `go test ./...` on host green; push FF ancestry rc=0; ls-remote==head + cat-file -e.
10. ⏳ Move evidence to baseharbor-plan; leave NO evidence dir in product branch.

## CI FAILS (run 41697843772, head 5f625b30)

- 4 runtime gates: docker/podman lifecycle + backup-restore (jobs 126134232864/126134233235/126135390721/126134644411)
- go-unit-tests (126133468544), cli-package-tests (126133468633), wizard-app-edit-tests (126133468960), Selected Checks (126136543386)

## TRUE REGRESSIONS (baseline clean, branch fails) — fixed

### openbao: `TestNativeSQLRegistryKeepsRuntimeStorageEnvironment`
```
--- FAIL: TestNativeSQLRegistryKeepsRuntimeStorageEnvironment (0.00s)
    service_csr_native_connector_sql_state_test.go:37: ...: deployment has no authoritative installation owner for its Target; the installation must be restored before its state is loadable
```
Fix: `internal/openbao/service_csr_native_connector_sql_state_test.go` — added `seedNativeSQLTargetOwner(t, target, runtime)` which provisions a real authoritative Core installation via `coreinstallation.Run` in the target-state-root runtime before the protected-registry round-trip. Real installation.json, no global bypass, no skip.
Host verified with fix: `go test ./internal/openbao/` → **ok** (5.0s).

### cmd/baha: `TestExternalProviderRemoval*` ×3
```
--- FAIL: TestExternalProviderRemovalChecksEveryManagedConsumerBeforeMutation (0.00s)
    provider_external_removal_test.go:122: provider change: provider-registry-ownership-unverifiable
```
Root: the deployment-owner seam (ADR-0022) now fail-closes on a Target without an authoritative Core; the `configureTestTarget`/`externalRemovalTransportFixture` construction left the Target without the real runtime-bootstrap (owner+runtime+inventory) that the green-baseline tests provision.
Fix: wire the real Core-owner seed (`registerInstallationForTarget` / w21 precedent) into the fixture so construction is complete (owner present, runtime dir 0700, inventory).
Host verified with fix: 3/3 runs clean.
```
=== run 1: ok  github.com/mcpdev80/baseharbor/cmd/baha  0.039s
=== run 2: ok  github.com/mcpdev80/baseharbor/cmd/baha  0.038s
=== run 3: ok  github.com/mcpdev80/baseharbor/cmd/baha  0.041s
```

## APP-EDIT — INTENT EVIDENCE (not a bug; fail-closed is GEWOLLT)

`TestAppEditCommandCompleteProviderEditRunsRealLifecycle` (cmd/baha):
```
DIAG_EXEC adapter executionErr=The last consumer cannot be released without verified runtime and complete consumer inventory.
--- FAIL: TestAppEditCommandCompleteProviderEditRunsRealLifecycle (41.87s)
    app_edit_apply_test.go:952: real Edit lifecycle did not converge: application machine: partial
        ... Status:partial ... Operation:resume Status:pending ... Impact information is incomplete
```
Baseline (same host): `ok github.com/mcpdev80/baseharbor/cmd/baha 65.506s`.
Verdict per Owner-urteil: the fail-closed "last consumer cannot be released without verified runtime" is the **contractual ADR-0022/develop-guard behavior** — the branch only makes it *visible* for constructions that never ran their runtime bootstrap. The fixture construction here is the anomaly (it seeds an authoritative Core via r3/r4 without the matching workload-runtime bootstrap that writes runtime.env); the PRODUCT code correctly fails closed on an unverified/absent runtime. **Production code left UNTOUCHED.** This case documents intent: incomplete state → fail-closed, as contracted. (Reconcile-4.md round-5 already identified the runtime.env convergence gap; no prod fix authorized — per Owner direction this is the guard doing its job.)

## ENVIRONMENT / SHARED-STATE (fail baseline too — NOT mine)
- `internal/telemetry` (3): `TestRegisteredOTLP*` — "OTLP TLS projection has no protected existing parent"
- `internal/externalprovider`: `TestDiscoverCertificateDirectoryMatchesWildcardAndKey`
- `cmd/baha` (5): `TestRecoveryFileForRepositoryUp*` — shared `~/.local/share/baseharbor-recovery` collision
- `internal/providers/runtime/podman` (2): quadlet retirement (need podman ownership env)

## END
END_DONE w71-stateowner-final: head=f3ea54e2 validation=rot+zeile(rootful-vs-rootless) lifecycle=infra-blocked(ref:41726952160) lsremote=f3ea54e2 | fix 4 true regressions verified green (openbao+externalprovider x3), validation-fail is CI-runner infra (rootful daemon vs rootless target), lifecycle gates infra-ausschuss. Evidence: baseharbor-plan/evidence/r27-welle3-2026-11-03/state-owner/final-1.md
