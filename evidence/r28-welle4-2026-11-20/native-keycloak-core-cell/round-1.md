# Native Keycloak/Core CI cell diagnosis — round 1

Lane: `w218-0428-204-native`
Task: read + local diagnosis only. No product change, no PR, no rerun, no new card.
Date: Fri 2026-11-20 (mission), Sat 2026-11-21 (run).

## Zweck
Der Owner misst an PR #1726 head `bf6f10aff6fe` ein rotes `PR · Native Keycloak/Core ·
docker` und `· podman` (das einzige required aggregate `PR Selected Checks`, ruleset
25223521, strict=true) und will wissen, ob diese Native-Zelle eine DRITTE, eigene
Ursache hat — neben den zwei bekannten roten Zellen `cli` (0428-204, Eintritts-
klassen-Seam) und `packages` (#1732-Fehl-Merge). Answer: **no third cause.** The
Native cell fails for the SAME root cause as the CLI packages.

## Base-Attestation
- develop head (base of #1726): `40cb28c758b02960356434b630086a341ebe1738`
  (`git ls-remote origin refs/heads/develop`, origin = https://github.com/mcpdev80/baseharbor.git)
- PR #1726 head: `bf6f10aff6fe5e7d69b7faffa5ee30b226685832`
- PR #1726 title: `fix(0428-198): give CLI unit tests an in-test operator identity`
  (base `40cb28c758`, head `bf6f10aff6fe`)
- plan repo remote (evidence target): https://github.com/mcpdev80/baseharbor-plan.git
  (`git -C baseharbor-plan remote -v`)

## Methode
1. `gh api repos/mcpdev80/baseharbor/commits/bf6f10aff6fe/check-runs?per_page=100`
   → `PR · Native Keycloak/Core · docker` job `136602097553` (run 44826908648),
   `· podman` job `136602097512`.
2. `gh api repos/mcpdev80/baseharbor/actions/jobs/<job-id>/logs` (raw, NUL-stripped).
3. Workflow inspection via gh API: `.github/workflows/ci.yml` job
   `pr_owner_node_native` runs `bash scripts/ci-owner-node-native.sh`
   (`require_pass ./cmd/baha TestControlPlaneSingleDefaultNativeRuntimeInCI 20m`),
   matrix `runtime: [docker, podman]`, env
   `BASEHARBOR_SINGLE_DEFAULT_NATIVE_ACCEPTANCE=1`.
4. Source read via gh API: `cmd/baha/control_plane_single_native_ci_test.go`,
   `cmd/baha/runtime_integration_test_support_test.go`,
   `cmd/baha/operator_test_fixture_test.go` (new in #1726),
   `cmd/baha/main.go` (runWithIO seam in #1726).
5. Local reproduction: shallow clone of `https://github.com/mcpdev80/baseharbor.git`
   into `worktrees/w218-native-repro`, build `./cmd/baha`, run
   `baha target create ... --default` and the Go test under
   `BASEHARBOR_SINGLE_DEFAULT_NATIVE_ACCEPTANCE=1 BASEHARBOR_TEST_RUNTIME=docker`.
   Same on clean develop `40cb28c758`. Docker daemon: rootless context, brought down
   at end (ps-witness below).

## Verbatim erste Fehlerzeilen (docker, job 136602097553)
```
control_plane_single_native_ci_test.go:30: prepare BaseHarbor integration trust plane: target "w169-ci-bootstrap-20d4bb4b" is not configured
--- FAIL: TestControlPlaneSingleDefaultNativeRuntimeInCI (0.00s)
bootstrap trust-plane package teardown failed: bootstrap trust-plane teardown could not begin: bootstrap trust-plane teardown target "w169-ci-bootstrap-20d4bb4b" is not configured
bootstrap trust-plane teardown left residual resources: wächter cannot inspect residuals: no runtime provider available for target "w169-ci-bootstrap-20d4bb4b"
```
podman (job 136602097512) identisch, Zielname `w169-ci-bootstrap-635be82e`.
Erster cmd/baha-Test startete 22:18:57.38, `--- FAIL` 22:18:57.38 (elapsed 0).
`TestKeycloakSingleNativeSQLInCI` davor PASS (49.42s / 62.17s) — Keycloak/SQL-Teil
läuft, nur der control-plane/bootstrap-Teil schlägt fehl.

## Einordnung: RUBRIK (a) — Operator-Seam
Erste fehlerhafte Stelle im Produktcode:
`cmd/baha/runtime_integration_test_support_test.go:722`
`func ensureRuntimeIntegrationTrustPlane` ruft `baha target create ... --default` und
`baha up --control-plane-only --yes` über `runWithIO`. Der Target wird nicht
persistiert, die `sync.Once` bricht mit `runtimeIntegrationTrustPlaneErr`; der
package-level teardown (dest. `bootstrapTeardownProvider`,
`cmd/baha/runtime_integration_test_support_test.go:1048`) meldet
`"bootstrap trust-plane teardown target %q is not configured"`.

Wirkliche Ursache (reproduziert lokal, nicht CI-harness): beim Aufruf von
`runtime_withIO` (cmd/baha/main.go:147) schlägt die produktive Operator-Enforcement-
Kette fehl mit:
```
Error
  Managed-environment machine operations require an authenticated BaseHarbor operator.
Affected  local/dev
Resolution  authenticate the BaseHarbor operator
What to do  Configure operator OIDC if required, run 'baha login' for the selected Target/environment, then retry.
```
**Dies ist exakt diezelbe Fehlermeldung wie die CLI-Package-Zellen** (0428-204
Eintrittsklassen-Seam, #1732-Packages). Der `local/dev`-Target ist eine
Managed-Umgebung; seit #1594 (develop head `40cb28c758`) entfiel der
dev→trusted-local Auto-Admit, und NUR dieser Operator-Check schlägt in
`runtime_integration_test_support_test.go:722` fehl.

### Beleg: lokale Reproduktion (deterministisch, beide Köpfe)
- `baha target create w168-ci-bootstrap-test --runtime-provider docker --access local
  --access-provider local --reference local --default` auf `bf6f10a`:
  `Managed-environment machine operations require an authenticated BaseHarbor operator.`
- `go test -p 1 ./cmd/baha -run '^TestControlPlaneSingleDefaultNativeRuntimeInCI$'`
  auf `bf6f10a` UND clean `40cb28c758`:
  `control_plane_single_native_ci_test.go:30: prepare BaseHarbor integration trust
  plane: target "w169-ci-bootstrap-... is not configured` + `--- FAIL` (0.00s).
- Der Keycloak/SQL-Test `TestKeycloakSingleNativeSQLInCI` läuft durch; der
  control-plane/bootstrap-Test schlägt an derselben Operator-Schleite fehl.

### Ursache-Kette
#1594 (develop `40cb28c758`) entfernte den dev→trusted-local Auto-Admit → jeder
cmd/baha-Test, der die produktive `runWithIO`-Laufbahn in einer Managed-Umgebung
fährt, schlägt mit der Operator-Meldung fehl. Die Native-Zelle ist ein solcher
Fall: `baha target create`/`up` über `runWithIO` schlägt fehl, Target nicht
persistiert, Teardown meldet "is not configured".

## WEN 0428-204 deckt vs. eigene Karte
- 0428-204 = CLI-Eintrittsklassen-Seam (die zwei roten Zellen `cli` + `packages`).
  Die Native-Zelle TEILT dieselbe Ursache (Operator-Seam in `runWithIO`), schlägt
  aber in einer SEPARATEN Testfunktion (`TestControlPlaneSingleDefaultNativeRuntimeInCI`,
  `./cmd/baha`) an, die von 0428-204s Seam `operatorAuthFixtureContext`
  (`cmd/baha/operator_test_fixture_test.go`, `init()` in #1726) NICHT erfasst wird:
  0428-204s Fix stempelt nur die Kontexte, die `runWithIO` in den CLI-Kommando-Tests
  berühren — nicht die `ensureRuntimeIntegrationTrustPlane`-Laufbahn des Native-Tests.
- **Ergebnis: 0428-204 deckt die Native-Zelle NICHT.** Die Native-Zelle braucht eine
  EIGENE Karte (Operator-Seam auf der Runtime-Integration-`runWithIO`-Laufbahn,
  `cmd/baha/runtime_integration_test_support_test.go:722`). Keine dritte INHALTLICHE
  Kategorie: dieselbe Rubrik (a) Operator-Auth, anderer Aufruf-Pfad.

## FOLGE FUER DIE KARTE
- Zusatzkarte noetig: operator-auth seam auf `ensureRuntimeIntegrationTrustPlane`
  (cmd/baha/runtime_integration_test_support_test.go:722), Rubrik (a), dieselbe
  Ursache wie 0428-204, separater Testpfad.
- Kein CI-/Harness-Defekt (Runner, workflow, image) — reproduziert lokal identisch.
- Owner: Karte anlegen, dann Native-Zelle mit derselben Operator-Auth-Lösung grün.

## repo-rule compliance
- Read-only Diagnosis. `git status --porcelain` im baseharbor-Checkout (develop,
  lane-origin) leer bezuglich dieser Akte; fremder Dirty-Stand anderer Lanes
  (`cmd/baha/app_apply.go`, `internal/application/prune-*/`) nicht angefasst.
- Keine Produkt-Änderung, kein PR, kein rerun, kein workflow_dispatch, keine
  Runner-/Runner-Infra, keine .github/**-Änderung.
- Keine Container/Volumes/Netzwerke zurückgelassen (ps-witness unten).

## vorher/nachher container/volumes
- vorher: keine BaseHarbor-Eigenen nach Testlauf (docker system prune --volumes).
- nachher ps-witness:
  `docker ps -a --filter 'name= bh-w169' --format '{{.Names}} {{.Status}}'` → leer
  (keine `bh-w169-ci-bootstrap-*` Container).
  `docker network ls` → keine `baseharbor`-Netzwerke des Testlaufs (nur fremde
  `bh-docker-dev-*`-Projekte, 13 Tage alt, nicht von dieser Lane).
  `docker volume ls` → keine Testvolumes.
  cleanup: `docker context use default && docker system prune -f --volumes`.
- cleanliness: kein state-verzeichnis, kein netz, kein volume dieser lane verbleibt.

## todo
aktuell (board file workers/todos/w218-0428-204-native.json geschrieben, schritte
numeriert, alle als done markiert nach abschluss).

END w218-0428-204-native DONE
