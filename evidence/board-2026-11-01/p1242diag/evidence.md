# p1242diag — Befundaufnahme: 'PR Selected Checks' auf #1242 head 35e2df16 = SKIPPED

Lane p1242diag · Worker Ornith · 2026-11-01
PR #1242 `work/fix-observ-consent` · head `35e2df1673cbe19f8ea8f7edc256fdeebd3de973`
Basis (base.sha) `5c903560c1881b6cd658c22ad9f51e3a42f362c5` · integration `c6db56c4ac077dbc496134cb0871c8e996a593fe`

## PLAN

1. PR #1242 + CI-Rollup einholen; run 41334397810 (FAILURE) vs 41334766189 (RERUN, SKIPPED) vergleichen.
2. pr-plan.json (coverage_status / selected_gates) + pr-gate-plan.py classifier + pr-selected-runtime-matrix.py analysieren.
3. Enforce-Step-Log run 41334397810 lesen ('BLOCKED: coverage-unresolved'); RERUN-Cascade identifizieren.
4. Ursache mit file:line festmachen.
5. Diagnose + Rezept in Evidence. Ende: END_DONE oder END_BLOCKED.

## Befund

### Zwei Runs, zwei Gesichter
- **Run 41334397810** (18:01:06Z, attempt 1): `PR Selected Checks` = **FAILURE** (Job-ID 124931645458).
- **Run 41334766189** (18:05:22Z, RERUN): `PR Selected Checks` = **SKIPPED**.

### Der wahre Auslöser des SKIPPED (RERUN 41334766189)
Der RERUN schlägt nicht in `PR Selected Checks` selbst fehl, sondern **kaskadiert** hoch:

```
validate  Initialize containers  →  failure
  "docker start ... : Error response from daemon: failed to set up container
   networking ... failed to bind host port 0.0.0.0:5432/tcp: address already in use"
```

`validate` ist die `pr_validations`-Matrix. Weil `validate` fehlschlägt, schlagen in GitHub-Actions die `needs`-Abhängigkeiten von `pr_selected_final` durch:

- `ci.yml` line 809: `pr_selected_final` `needs:`
  `[workflow_policy, pr_plan, pr_focused, pr_validations, pr_candidate, pr_consumer_pins, pr_demo_pin, pr_runner_interface, pr_runtime_selected, pr_public_contracts]`
- `ci.yml` line 810: `if: always() && github.event_name == 'pull_request' && github.base_ref == 'develop'`
- Ohne eigenen `if`-Filter gilt die GitHub-Standardsemantik: **wenn eine `needs`-Abhängigkeit nicht `success` ist, wird der Job übersprungen**. `pr_validations` war `failure` → `pr_plan` (`PR · Trusted Plan`) skippt → `pr_focused`, `pr_candidate`, … skippen → `PR Selected Checks` = SKIPPED.

Beleg: im RERUN sind `validate`=failure und `PR · Trusted Plan`=skipped; alle anderen `PR Selected Checks`-`needs` sind skipt oder failure; `PR Selected Checks` hat keine ausgeführten Schritte (`steps: []`).

### Warum die Kaskade erst jetzt (und nicht bei #1242 initial) — der eigentliche Gate-Befund
Im initialen Run 41334397810 **lief** `PR Selected Checks` durch und wurde mit absichtlicher **FAILURE** bewertet. Das ist das Pflicht-Gate der Develop-Regeln korrekt aktiv. Der enforcer (ci.yml line 825-861) lief durch:

- `ci.yml` line 843: `test "$PLAN_JOB" = success` ✓ (`PLAN_JOB=success`)
- `ci.yml` line 844: `test -s pr-plan.json` ✓
- `ci.yml` line 845: Stale-Input-Assert gegen base/head/integration ✓
- `ci.yml` line 850: `SELECTED_RUNTIME_REQUIRED=false` → native-evidence-Block übersprungen
- `ci.yml` line 861: `python3 "$RUNNER_TEMP/pr-required-final.py" --plan pr-plan.json --results ... --requirements scripts/release-requirements.json`

…und brach ab mit:
```
BLOCKED: coverage-unresolved: CLI runtime impact needs qualified targeted native coverage: cmd/baha/app_observability_acceptance_test.go
[error]Process completed with exit code 1.
```

Ursache in `scripts/pr-gate-plan.py`:
- **Line 1473-1477** — `cli-unresolved-runtime-impact`-Catch-All: jede Datei
  `cmd/baha/*.go`, die keinem der reviewed-Patterns (z.B. Line 1454 `runtime_restart_integration_test.go`) entspricht, wird als `unresolved` markiert:
  `unresolved.append('CLI runtime impact needs qualified targeted native coverage: ' + path)`.
- PR #1242 fügt `cmd/baha/app_observability_acceptance_test.go` hinzu (ein Go-**Test** für die plan→apply-Consent-Stufe, kein Runtime-Mutation-Surfaze). Diese Datei trifft exakt diesen Catch-All.
- Folge in `pr-plan.json` (Artifact `trusted-pr-plan` von run 41334397810):
  - `coverage_status: "unresolved"`
  - `selected_gates: []` (leer)
  - `required: null`, `mode: null`
  - `reasons: ["cmd/baha/app_observability_acceptance_test.go: cli-unresolved-runtime-impact"]`
  - `unresolved_coverage: ["CLI runtime impact needs qualified targeted native coverage: cmd/baha/app_observability_acceptance_test.go"]`
- `scripts/pr-selected-runtime-matrix.py` line 23-24: bei leerem `selected_gates` → `{"required": false, "include": [{"id":"not-required",...}]}` → `runtime_required` = `false`. Deshalb sind in beiden Runs die `Targeted HA · docker/podman`-Jobs korrekt `skipped`. Das ist **beabsichtigt**, kein Fehler.

## Ursache mit file:line

**`PR Selected Checks` ist auf dem RERUN 41334766189 SKIPPED, weil der RERUN in `validate` an einem Runner-Umfeldfehler scheiterte (`docker ... : address already in use` auf Port 5432, `Initialize containers` = failure), wasn die `needs`-Kette von `pr_selected_final` (ci.yml line 809, `if: always()` line 810, Standard-Skip-Semantik) durchziehen ließ. Das ist ein Cascade-/Infra-Artefakt des RERUNs, kein Anzeigefehler.**

Der **inhaltliche Gate-Befund** ist dagegen korrekt aktiv: PR #1242 löst in
**`scripts/pr-gate-plan.py` line 1473-1477** (`cli-unresolved-runtime-impact`) einen fail-closed `coverage-unresolved`-Block aus (`pr-required-final.py`, ci.yml line 861). Der Auslöser ist die neue Datei
`cmd/baha/app_observability_acceptance_test.go`, die keinem reviewed-Pattern (z.B. line 1454 `runtime_restart_integration_test.go`) entspricht.

## Kein Ruleset-/Anzeigefehler
`merge_base_sha`/`target_base_sha`/`integration_sha` im plan stimmen mit base/head/integration überein (Stale-Input-Assert ci.yml line 845 lief grün). `coverage_status`/`selected_gates` sind planner-seitig korrekt `unresolved`/leer. Es liegt **kein** Ruleset-Anzeige-/IF-Fehler vor.

## Rezept (END_BLOCKED)
Mission erlaubt nur einen minimalen Fix, **wenn** die Ursache eindeutig in `scripts/pr-gate-plan.py` liegt und **kein** `.github/workflows/ci.yml`-Stück anfasst.

Die Ursache (`cli-unresolved-runtime-impact` catch-all line 1473-1477) liegt formal in `scripts/pr-gate-plan.py`. Ein Fix wäre, `cmd/baha/app_observability_acceptance_test.go` wie `runtime_restart_integration_test.go` (line 1454) in ein reviewed-pattern aufzunehmen und auf die bestehenden atomaren native lifecycle-gates (`atomic/docker/lifecycle`, `atomic/podman/lifecycle`) zu binden — analog zur #1245-Fixzeile (ci.yml line 1454-1472), **ohne** neues Gate und ohne Abschwächung. Das ist jedoch eine **Owner-Entscheidung**: es verändert die Fail-closed-Policy des plan-job und berührt die `cli-unresolved-runtime-impact`-Strategie. Nach Mission-STOP (keine ci.yml-/Ruleset-Änderungen) bleibt der Fix auf `scripts/pr-gate-plan.py` begrenzt; ein solcher Change benötigt Review + PR + Planning-Abschluss, nicht dieses Diagnose-Lane.

Zusätzlicher, separater Befund (nicht missionsscope): der RERUN-Skip durch `validate` port-5432-Kollision ist ein GitHub-Hosted-Runner-Infrafund und gehört in eine eigene Diagnose/Lane (z.B. Concurrency/Port-Slot für `validate`).

## Entschaidung
**END_BLOCKED** — Diagnose abgeschlossen, Ursache mit file:line festgemacht. Kein Produktfix in diesem Lane (STOP: keine ci.yml-/Ruleset-Änderungen; plan-job-Fix in `scripts/pr-gate-plan.py` erfordert gesonderte Owner-Autorisierung + Review + PR). Rezept o.g.

---
END p1242diag BLOCKED

## Zeugen
- `gh run view 41334397810 --log-failed` → `BLOCKED: coverage-unresolved: ... cmd/baha/app_observability_acceptance_test.go`; `SELECTED_RUNTIME_REQUIRED: false`.
- `gh run view 41334766189 --log-failed` → `validate / Initialize containers / ... address already in use`.
- `gh run view 41334766189 --json jobs` → `validate`=failure, `PR · Trusted Plan`=skipped, `PR Selected Checks` steps `[]`.
- Artifact `trusted-pr-plan` (run 41334397810): `coverage_status=unresolved`, `selected_gates=[]`, `reasons=[...]`.
- `scripts/pr-gate-plan.py` lines 1454-1477 (classifier).
- `scripts/pr-selected-runtime-matrix.py` lines 23-24 (runtime_required-Logik).
- `.github/workflows/ci.yml` lines 809-810, 843-861 (Enforcer).
