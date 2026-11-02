# gatemap-r6 — Torbindung: cmd/baha/*_test.go an BESTEHENDES cli-gofmt-Tor

## Task-Vertrag (Mission gatemap-r6)
**Ziel:** `cmd/baha/*_test.go`-Pfade kommen durch, weil die Klassifizierung
Aenderungen an Testdateien nur an Lifecycle-/Runtime-Gates bindet, `cli-gofmt`
aber nicht verlangt. Fundstelle: `scripts/pr-gate-plan.py` `cmd/baha`-Zweige
(Zeilen ~1401+ und die `#1268`-Bindung), Vorbild: bestehende
`require(CLI_GOFMT...)`-Nutzung in anderen Zweigen.
- **KEIN neues Gate, KEIN Workflow-Wechsel, KEIN Merge, KEIN subagent, KEIN Frage-Dialog.**
- Minimaler, kommentierter Mapping-Fix im Stil von `#1264/#1266`.

## PLAN-Checkliste
1. [x] Pruefen, unter welchem bestehenden Gate-Token cli-gofmt laeuft (ci.yml referenzen).
2. [x] Branch in `pr-gate-plan.py` ergaenzen: `cmd/baha/*_test.go` -> cli-gofmt, EXAKTE Stellung VOR `cli-unresolved-runtime-impact`; mcp_ und registration-mixed bleiben unberuehrt. Fail-closed ancestry fuer exact-reviewed test-Dateien gewaehrleistet.
3. [x] `test_pr_gate_plan.py` um zwei Faelle ergaenzen (Testdatei->cli-gofmt; mcp_/registration unveraendert).
4. [x] Lokale `pr-planner-tests` (unittest) ausfuehren -> alle gruen.
5. [x] PR gegen develop pushen; PRSC + pr-planner-tests terminal beobachten (erster Lauf: AppID_FIX-Regression, gefixt).

## Repo-Regel-Konformitaet
- Repo: baseharbor; Branch/Worktree: `gatemap-r6` @ `940cc1cd` (origin/develop, entwickelt).
- Nur Produkt-/Skript-Aenderungen im eigenen Worktree; keine `git add -A`.
- Kleinstes Gate: bestehender `cli-gofmt`-Token (`gofmt -l cmd/baha`), kein neues Gate.

## Befunde / Evidence
- `cli-gofmt` existiert in `scripts/pr-gate-plan.py` als `WIZARD_BASE_CHECKS[0]`
  (id `cli-gofmt`, command `test -z "$(gofmt -l cmd/baha)"`) und in
  `.github/workflows/ci.yml` line 705 als Gate-Handler. Es ist ein
  VALIDIERUNGS-Check (in `required_validation_checks`), kein Release-Gate.
- Aktuell faellt jede `cmd/baha/*_test.go`-Datei (außer special clauses wie
  `docker_engine_podman_test.go`, `runtime_restart_integration_test.go`,
  `app_observability_acceptance_test.go`, Wizard-Dict, mcp_) auf den
  `cli-unresolved-runtime-impact`-Catch-All (line ~1606) -> `coverage_status: unresolved`.
- FIX (Zeile nach internal/runtimebroker clause, VOR cli-unresolved-runtime-impact):
  `elif path.endswith('_test.go') and path.startswith('cmd/baha/') and \
   all(p.endswith('_test.go') for p in paths) and \
   not any(_is_reviewed_test_file(p) for p in paths):` -> `require(CODE/CLI/WIZARD_BASE)`
  (= cli-gofmt + build/vet/contract). Nur test-only PRs UND keine
  exact-reviewed test-Datei (REVIEWED_TEST_FILES/Hilfe `._is_reviewed_test_file`),
  damit APPID_FIX-Einzelkandidat fail-closed bleibt; mcp_/registration-mixed
  bleibt auf eigener unresolved-clause (Sitz NACH ihnen).
- Verifiziert (lokal, REQ-Katalog): generische `_test.go` -> `resolved` mit
  `cli-gofmt` in den required_validation_checks; mcp_ -> unveraendert `unresolved`
  (mixed); lone app_workload_integration_test.go -> unveraendert `unresolved`
  (fail-closed ancestry); test+production -> `unresolved`.
- Test-Regression erkannt/fixt: initially loeser `all()`-guard loeste den
  APPID_FIX-Einzelkandidat auf; _is_reviewed_test_file() wieder einfgehrt.

## Status
END_DONE — Mapping-Fix implementiert, pr-planner-tests gruen, PR #1276 gegen develop gepushed; CI terminal verifiziert (success).
- PR: #1276 (work/gatemap-r6-cli-gofmt-test-binding -> develop)
- head SHA: 3576d3d1 (Commits: 69a14663 + 3576d3d1 [AppID_FIX fail-closed Fix])
- CI run id: 41425856907 (conclusion=success; pr-planner-tests ID 125212256789 gruen)
