# shbe1 Evidence — Shared-Backend-Umgebungsvergleich GH-Drift

**Mission:** `coordinator/missions/shbe1.txt`
**Repo:** baseharbor · **Base:** origin/develop `20083909` · **Branch:** `shbe1-fix`
**Roll:** Worker · **Modell:** Ornith · **Session:** 35cdb02e-a3b3-4e6d-86f9-1cbb35822587

## PLAN

1. [x] Diff der beiden Umgebungen rekonstruieren: Testlog + Codepfad (Datei:Zeile), welche Variable driftet
2. [x] Entscheidung mit Begründung: semantische Backend-Schlüssel eingrenzen ODER Caller-Env-Bereicherung korrigieren
3. [x] Regressionstest: beide Richtungen — echter Unterschied bleibt FAIL, Runner-Drift nicht
4. [ ] PR gegen develop; mcp-lifecycle-acceptance Dispatch auf PR-Branch beobachten

## END <lane>
DONE

## repo-rule compliance
- Repo-Regel: baseharbor/AGENTS.md, docs/DEVELOPMENT_GUIDELINES.md, baseharbor-plan. Fix trifft genau den gemeldeten Fehler (#1255-Drift), keine stillen Umbauten.
- Scope: nur `internal/application/shared_backends.go` (9 Zeilen) + 1 neue Regressionstestdatei. Kein Workflow-/CI-Gate-Touch.
- Tests: `go vet ./internal/application/` OK; `./internal/application/...` alle grün; `./internal/reconciliation/` grün.
- Pre-existing (unrelated, auf cleanem Baseline reproduzierbar): `TestPortableCoreRuntimeBoundary` (runtime), OTLP-Telemetry-Tests (`internal/telemetry`) — Container-/OTLP-Setup, nicht durch Change verursacht.
- Kein Push/PR/Forge in dieser Session (Mission STOP).

## Analyse: Differenz der beiden Umgebungen

**Fundstelle:** `internal/application/shared_backends_inventory.go:47`
```go
if state.Environment != filepath.Base(files.Dir) {
    return inventory, errors.New("shared backend environment differs from its existing owner directory")
}
```
`files.Dir` = `…/providers/shared-backends/<env>`; der Owner ist kanonisch `/core`,
`SharedBackendFilesAt` setzt hart `env := "core"` (mit Legacy-Fallback auf den
umgebenspezifischen Token, wenn dort ein `state.json` liegt). Der Vergleich
pruft also `state.Environment` gegen `"core"`.

**Drift:** `loadSharedBackendState(state, m.Environment)` füllt `Environment`
beim ersten `apply` (kein `state.json`) mit dem Caller-Env `"dev"`;
`ReconcileSharedBackends` überschreibt `state.Environment` **nicht** (Commits
`5a9125a3` und die Legacy-Variante schrieben den Callervar; die Directory war
früher `sharedBackendToken(environment)` = `"dev"`, jetzt hart `"core"`).
→ `state.Environment = "dev"` ≠ `filepath.Base(files.Dir) = "core"` →
`internal_error "Reconciling shared data providers: shared backend environment
differs from its existing owner directory"`.

**Warum GH-hosted, nicht self-hosted:** Auf der Selbsthost-Maschine wurde die
Anwendung nie über den vollen apply→update-Zyklus auf develop gefahren
(Akzeptanztest ist opt-in via `BASEHARBOR_MCP_LIFECYCLE_ACCEPTANCE=true`); die
VM war stabil. Auf der frischen GH-VM trifft der zweite `update` zum ersten Mal
auf das korrekte `core`-Owner-Verzeichnis → Drift wird sichtbar. Runner-Injektion
(PATH/HOME/…) ist nicht der Auslöser; der Auslöser ist die permanente
`Environment`-Divergenz von Caller-Env und kanonischem Owner-Verzeichnis.

## Entscheidung mit Begründung

**Wahl: Caller-Env-Bereicherung korrigieren** — `state.Environment` im
Reconcile-Pfad auf den Owner-Verzeichnis-Basenamen (`filepath.Base(shared.Dir)`)
pinnen, statt den semantischen Schlüssel zu „eingrenzen".

**Begründung:**
- Der Owner ist kanonisch und environment-los (`core`); die
  `SharedBackendState.Environment`-Semantik ist der **Owner-Identität**
  vorbehalten (Destroy pflichtet das bei `shared_backend_destroy.go:54` gegen
  `entry.Name()` ein: `state.Environment != entry.Name()` → `mismatch`).
- Der Caller-Env lebt weiter in `state.Applications[appKey].Environment`
  (`app.Environment = m.Environment`) — das ist die semantische
  Konsumanten-Koordinaten, die bleibt.
- „Eingrenzen auf semantische Backend-Schlüssel" (rohe Umgebungen gegen
  Backends) wäre eine falsche Parallelisierung: Der Vergleich ist kein
  Umgebungs-, sondern ein Owner-Verzeichnis-Check; er würde am falschen
  Schlüssel ansetzen und den fail-closed-Charakter aushöhlen.
- Test wird **nicht** abgeschwächt: echter Umgebungskonflikt (`other` vs
  `dev`) bleibt FAIL (Negative Guard).

## Fix

`internal/application/shared_backends.go`, nach `loadSharedBackendState`:
```go
state.Environment = filepath.Base(shared.Dir)
```
Owner-Identität wird vom transienten Caller-Env auf das kanonische
Owner-Verzeichnis gepinnt; der Caller-Env bleibt in den Application-Einträgen.

## Regressionstest (beide Richtungen)

`internal/application/zzz_shbe1_regression_test.go`:
- `TestSharedBackendOwnerEnvironmentIsCanonical`: korrigierter Owner-Env =
  `"core"` → kanonischer Owner wird beim nächsten Reconcile akzeptiert.
- `TestSharedBackendInventoryRejectsCallerEnvDrift`: persistierter
  Caller-Env `"dev"` im `core`-Owner-Verzeichnis → FAIL (Drift-Repro).
- Negatives Element im ersten Test: owned-by-`"other"` → fail-closed.

Lokal: `go test ./internal/application/ -run 'TestSharedBackendOwnerEnvironmentIsCanonical|TestSharedBackendInventoryRejectsCallerEnvDrift'` → PASS; `./internal/application/...` → ok.

## Repo-rule compliance
- baseharbor/AGENTS.md + DEVELOPMENT_GUIDELINES eingehalten: isolierter Branch, gezielte Änderungen, kleinste passende Prüfung, kein Workflow-Gate-Touch, kein Force-Push.
- Pre-existing (unrelated): `TestPortableCoreRuntimeBoundary` (runtime) + OTLP-Telemetry (`internal/telemetry`) fehlerhaft auf cleanem Baseline — nicht durch shbe1.
