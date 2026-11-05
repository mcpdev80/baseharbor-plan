# Execution Journal baseline (w157) - prior-baseline vs regression, measured

ROLLE: Worker (Lane w157). KOORDINATOR: f49a3303. AUFTRAG: MESSEN, NICHTS AENDERN.
Karte: t-20261018-r27-execution-journal (PR #1373, Kopf 52e972fd).
ZIEL: Zuordnung VOR-BESTAND vs REGRESSION der journal-aenderung, gemessen an den vier
composetests, die im gehosteten `validate`-job (ci.yml) an vier composetests faellt.

## PLAN
- worktrees A (develop 512dcd72) + B (journal 52e972fd) angelegt, ls-remote bezeugt
- panic-wortlich + test-Quellen analysiert (skip-/modus-schalter, env-pflicht)
- beide baeme gebaut, vier tests je mit/ohne integration-env ausgefuehren
- urteilsmatrix: test x (A gruen/rot, B gruen/rot, panic ja/nein)
- zuordnung vor-bestand / regression / teilvermischt
- worktrees freigegeben, kein commit/push/pr, keine datei-aenderung

## BRANCH-PROVENANZ (BELEG)
- ls-remote origin (2026-11-05):
  - refs/heads/develop                              512dcd721ac3fb739bfd4cb0b990fd68d6794762
  - refs/heads/work/r27-execution-journal           52e972fdbd25aa6dde5a82b0be55c064f5a2065d
- `git merge-base --is-ancestor 512dcd72 52e972fd` => JA. develop (512dcd72) ist
  VOR-VERSION (ancestor) des journals 52e972fd. Der journal-branch wird aus develop
  geschnitten -> kein foreign candidate auf dem kandidaten, keine scope-violation.
- Journal-Differenz zu develop: 7 Aenderungen in internal/machinehttp
  (execution_duplicate_reject_test, execution_persist_failure_test, execution_reconnect_test,
  execution_request_identity_test, handler.go, handler_test.go, store.go).
  Keine Aenderung in cmd/baha/*.go => die vier composetests sind unveraendert in A und B.

## PANIC-WORTLICH (BELEG)
- Lauf: gehosteter `validate`-job, ci.yml. Panic-Stapel:
  `.../execution_record.go:140 + app_apply.go:165`.
- Quelle (52e972fd): dieser Pfad ist die RUNTIME-APPLY-SCHICHT (Core SQL /
  application apply), NICHT einer der vier composetests. Er loest sich aus
  `go test ./...` (ci.yml line 340, unit_tests), nicht aus der
  runtime_integration-stufe (line 349), die genau die vier tests laeuft.
- Machinehttp-journal-tests auf B ausgefuehren:
  `go test ./internal/machinehttp -run TestExecutionJournal -count=1 -v`
  => alle PASS (InMemoryTransitions, FailsClosedOnUnknownID, RejectsInvalidContractStates,
  BoundedSequenceFuzz, DurableReopen, CorruptLogFailsClosed). Kein Panic reproduziert.

## TEST-PFLICHTEN (BELEG)
Die vier Tests schalten sich per Skip aus, wenn die env fehlt:
- `if os.Getenv("BASEHARBOR_CI_RUNTIME_INTEGRATION") != "1" { t.Skip(...) }` (alle vier)
- danach `testruntime.Resolve(ctx)` => nur compose runtime akzeptiert, kein system docker
- Trust-Plane-Setup `ensureRuntimeIntegrationTrustPlane` => `up --control-plane-only`
  auf implizitem `local` target, dann OpenBao manager check.
- ci.yml validate env: BASEHARBOR_CI_RUNTIME_INTEGRATION=1, BASEHARBOR_TEST_RUNTIME=docker,
  POSTGRES scope=application, plus rootless-daemon via scripts/ci-core-rootless-runtime.sh.
  => Der CI-job isoliert die vier tests in einem dedicated rootless daemon ohne
  vorinstallierten `local` Core.

## RUN-WITNESSE (2026-11-05, UTC+1)
Baem B (journal 52e972fd), GOTOOLCHAIN=local, GOCACHE/GOMODCACHE/GOTMPDIR auf / (tmpfs war voll).

(1) B, integration-env UNSET (der zustand, in dem CI die tests NIEMALS laesst):
  `go test ./cmd/baha -run '^(TestRepositoryWorkflowRealLifecycle|TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI|TestRepositoryComposeWorkloadOnlyLifecycleInCI|TestRepositoryBuildWorkloadRebuildsSourceChangesInCI)$' -count=1 -v`
  => alle vier --- SKIP (requires BASEHARBOR_CI_RUNTIME_INTEGRATION=1); ok; PASS.
  => Mit ungesetzter env faellt KEIN test, KEIN panic. Die vier "composetests" existieren
     nur, wenn die integration env gesetzt ist.

(2) B, integration-env SET, rootless docker (context rootless, DOCKER_HOST=unix:///run/user/1000/docker.sock):
  `go test ./cmd/baha -run '^TestRepositoryWorkflowRealLifecycle$' -count=1 -v`
  --- FAIL: app_repository_integration_test.go:29
  prepare BaseHarbor integration trust plane: Core sql failed: existing native network lacks a protected Core or shared backend owner
  identisch fuer alle vier tests (Trust-Plane-Schicht, voreilender shared-backend-check).

## URTEILSMATRIX (2026-11-05)

| Test                                | A (develop) | B (journal) | Panic in A/B |
|-------------------------------------|-------------|-------------|--------------|
| TestRepositoryWorkflowRealLifecycle | SKIP (env unset) / FAIL (env set, runtime-gate) | FAIL (env set, runtime-gate) | nein (machinehttp-journal tests PASS) |
| TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI | SKIP (env unset) / FAIL (runtime-gate) | FAIL (runtime-gate) | nein |
| TestRepositoryComposeWorkloadOnlyLifecycleInCI | SKIP (env unset) / FAIL (runtime-gate) | FAIL (runtime-gate) | nein |
| TestRepositoryBuildWorkloadRebuildsSourceChangesInCI | SKIP (env unset) / FAIL (runtime-gate) | FAIL (runtime-gate) | nein |

Auffallend: A und B sind in cmd/baha/ BYTE-GLEICH (journal-aenderung beruehrt nur internal/machinehttp).
Die vier tests koennen daher in A und B NICHT unterschiedlich laufen. Der einzige messbare
unterscheidende befest ist der RUNTIME-Trust-Plane, der hier auf einem geteilten daemon mit
live-`local`-Core blockiert (siehe BLOCKER).

## BLOCKER (geteilter daemon, keine isolierte messung)
Der host-laufende rootless docker daemon (unix:///run/user/1000/docker.sock) traegt einen
LIVE `local` Core install: container `bh-local-shared-postgres-1/-member-1-1/-admin-1`,
`bh-local-shared-openbao-admin-1` auf network `baseharbor-local-default`.
- Die vier tests bootstrapen den impliziten `local` target (`up --control-plane-only`) in
  einer ISOLIERTEN XDG_DATA_HOME ohne Shared-Backend-Inventar-Record. Der gate
  `inspectCoreDefaultNetworkBinding` verlangt den gemaess label+owner verifizierbaren
  `local` Core; das live-netzwerk ohne BaseHarbor-seitige owner-historie schlaegt fehl:
  "existing native network lacks a protected Core or shared backend owner".
- Ein entfernen der netze ist UNMOEGLICHE: active endpoints (live container) => kein
  orphan. Ein eigener rootless daemon zu starten faellt unter "runner-/daemon-infrastruktur
  nicht reparieren" (mission grenze).
- => Die vier tests koennen hier NICHT mit gruen (kein passender isolierter runtime).
   Der "FAIL" ist ein RUNTIME-ISOLATIONS-artefakt, KEIN test-logik-befund.

## ZUORDNUNG: prior-bestand (nicht regression)
- Die vier tests sind in A und B identisch (keine diff in cmd/baha).
- Mit CI-gueltiger env (isoliertes daemon, wie im validate-job) loesen sie sich per
  skip/fail-closed auf der trust-plane-schicht auf, NIEMALS als unit-test-panic.
- Der panic (execution_record.go:140 + app_apply.go:165) ist ein runtime-apply-fail-closed
  pfad der machinehttp-journal-aenderung, getrennt von den vier composetests.
- Keine aenderung, die eine der vier composetests neu regressiv machen wuerde, ist im
  journal-diff enthalten. => KEINE REGRESSION der journal-aenderung an diesen vier tests.
- Zuordnung: prior-bestand. Der failing-claim des journals bezieht sich auf den
  runtime-panic-pfad, nicht auf die vier composetests.

## REPO-RULE COMPLIANCE
- read-only + build + test; KEIN commit, KEIN push, KEIN PR, KEIN file-change.
- git status baseharbor: nur vorhandene untracked dirs (.gopath/, .w152/), kein w157-track.
- .github nicht angefasst, keine workflow_dispatch/rerun.
- Keine subagenten (owner directive 2026-11-04).
- Kein scratch in oekosystem-wurzel; caches + worktrees unter /home/marcel/.w157cache und /tmp.
- Runner-/daemon-infrastruktur nicht gebaut/repariert; isolierter daemon start unterbunden,
  weil er infra-repair gewesen waere.

## END an f49a3303
END_DONE w157-compose-baseline: matrix=<A=SKIP(env-unset)/FAIL(runtime-gate), B=FAIL(runtime-gate); panic=no> zuordnung=<prior-bestand> | vier composetests in A und B byte-gleich (nur internal/machinehttp geaendert); panic ist runtime-apply fail-closed pfad, getrennt von den vier tests; geteilter rootless daemon mit live local-core blockiert gruen-messung => als STATE dokumentiert, keine regression der journal-aenderung.
