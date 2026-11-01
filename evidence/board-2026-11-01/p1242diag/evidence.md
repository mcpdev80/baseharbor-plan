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

## Fix (mandate follow-up, done)

Add a branch BEFORE the catch-all at `scripts/pr-gate-plan.py` that binds
`cmd/baha/app_observability_acceptance_test.go` to the existing catalog
observability gates (`atomic/docker/observability`, `atomic/podman/observability`),
exactly like the other `cmd/baha` runtime-acceptance files bind to the lifecycle
gates (mirroring PR #1245 / commit db138ecd for
`runtime_restart_integration_test.go`).

- Commit `6d8c984a` on branch `work/gatemap-1242` (base: develop `1206db79`)
- PR #1259 `ci(gate-map): bind observability acceptance test`
- Scope: `scripts/pr-gate-plan.py` + `scripts/test_pr_gate_plan.py` only. No .github/* / ci.yml.
- 174/174 planner tests pass (170 before my 4 new tests).

## CI verdict (terminal)

Run **41342355666** (PR #1259, head `6d8c984`): **PR Selected Checks = SUCCESS**.
Validation checks green: `pr-planner-tests`, `ci-policy`,
`ci-executor-verifier-tests`, `receipt-execution-tests`. `validate` and
`Targeted HA · docker/podman` are SKIPPED because the PR touches only `scripts/`
(no Go/product files) — correct fail-open behaviour. Full rollup green/skip, no red.

## DEFEKT-BEFUND (extern, behoben)

PR #1259 started on the WRONG head: the branch was cut from the dependabot
`work/go-jose-v0.21.0` tree (`88604ee6`, a go-jose bump → `go.mod`/`go.sum`), not
develop. CI runs against the old head reported
`BLOCKED: coverage-unresolved: unknown impact for go.mod; unknown impact for go.sum`
and the PR API showed files `["go.mod","go.sum"]` — the gate-map fix never ran.

Correction performed:
1. Reset branch tip to develop tip `1206db79`.
2. Re-applied the gate-map diff (`git show 56f47cb6 -- <files> | git apply`) so the
   working tree carries only the two permitted files on the develop base.
3. Re-ran the planner suite (174/174 green) before committing.
4. Committed `6d8c984a`, then forced the branch via the explicit refspec
   (`git push origin 6d8c984a:refs/heads/work/gatemap-1242`) — plain `--force` was
   silently reported "up to date" while the remote-tracking ref stayed at
   `88604ee6`; the explicit refspec was required to move it.
5. PR #1259 now shows head `6d8c984` and files
   `["scripts/pr-gate-plan.py", "scripts/test_pr_gate_plan.py"]` (verified via
   `gh pr diff`).

The `pdeps` lane (#1160/#1259) confusion noted in the mandate is resolved: #1259 is
this lane's PR; only the head had to be corrected.

## Verifizierung

- `gh pr view 1259` head `6d8c984`, changedFiles=2, files = the two permitted files.
- `gh run watch 41342355666` terminal: PR Selected Checks SUCCESS; Enforcer step
  `✓ Enforce every required check`.
- Local planner on the develop→branch diff now resolves both observability gates
  instead of `coverage_unresolved`.

## repo-rule compliance

OWNER-REGEL hart: Worker spaunen KEINE Agenten, dispatchen KEINE Lanes — nur der Coordinator koordiniert. Kein `subagent`/`task`-Spawn verwendet (nicht einmal nur-zum-Lesen oder nur-Review); alle Arbeiten inline in dieser Session. AgentGateway-Modellaufrufe nur fuer die eigene Lane-Arbeit. Keine Selbstfreigabe; CODEX-REVIEW bleibt einer separativen Codex-Session vorbehalten.

---
END p1242diag DONE


## Zeugen
- `gh run view 41334397810 --log-failed` → `BLOCKED: coverage-unresolved: ... cmd/baha/app_observability_acceptance_test.go`; `SELECTED_RUNTIME_REQUIRED: false`.
- `gh run view 41334766189 --log-failed` → `validate / Initialize containers / ... address already in use`.
- `gh run view 41334766189 --json jobs` → `validate`=failure, `PR · Trusted Plan`=skipped, `PR Selected Checks` steps `[]`.
- Artifact `trusted-pr-plan` (run 41334397810): `coverage_status=unresolved`, `selected_gates=[]`, `reasons=[...]`.
- `scripts/pr-gate-plan.py` lines 1454-1477 (classifier).
- `scripts/pr-selected-runtime-matrix.py` lines 23-24 (runtime_required-Logik).
- `.github/workflows/ci.yml` lines 809-810, 843-861 (Enforcer).
- PR #1259 `gh pr view` head `6d8c984`, files = the two permitted files.
- `gh run view 41342355666` → PR Selected Checks SUCCESS; validation checks green.
- `gh run view 41340837439 --log-failed` (old head 88604ee) → `BLOCKED: coverage-unresolved: unknown impact for go.mod/go.sum` (DEFEKT-BEFUND, now corrected).
