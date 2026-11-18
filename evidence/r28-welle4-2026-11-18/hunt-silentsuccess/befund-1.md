# Befund 1 — app-edit / MCP: partial provider-change result reported as success

- Schwere: **MEDIUM** (fail-closed in the interactive CLI edit path, but a silent-success in the machine/HTTP + MCP edit path)
- Reproduzierbar: unit-only möglich (RecordProviderChangeResult mit einer incomplete Impacts-Auflistung)
- Zone: cmd/baha (keine Änderung; Befundung)

## Was ist beobachtet

Bei einem multi-step `app edit apply` wird die Execution durch
`appMachineChangeDesired` (cmd/baha/app_machine_adapters.go:521-531) abgewickelt:

```
outcomes, executionErr := apply(...)        // app_machine_adapters.go:521
result, resultErr := application.RecordProviderChangeResult(fresh.Plan, outcomes)  // :522
if resultErr != nil { ... return ..., errors.Join(..., executionErr, resultErr) }  // :523-526
if executionErr != nil { return ..., errors.Join(..., executionErr) }  // :528-530
return result, nil   // :531  <-- kein Check auf result.Status
```

`RecordProviderChangeResult` (internal/application/provider_change_result.go) setzt
`result.Status` Standard auf `"partial"` und nur auf `"complete"`, wenn
`plan.Complete && applied == len(plan.Impacts)`.

`appApplyObservedOutcomes` (cmd/baha/app_apply_result.go:232-261) hängt PRO Impact
nur dann ein `ProviderExecutionOutcome` an, wenn es vollständig attestierbar ist
(`appAttestedRealizationOutcome` / `appAttestedSQLNewConsumer` /
`appObservedPendingUpdate`). Kann ein Schritt nicht vollständig attestiert werden
(z. B. ein `update` mit unaufgelösen Material-/Consumer-Konsequenzen, die nicht in
die `pending`-Klasse passen), wird **kein** Outcome angehängt. Damit landet dieser
Impact in `outcomes`-lokal als `"pending"` und das Ergebnis bleibt `"partial"` —
**ohne dass `resultErr` gesetzt wird**.

Konsequenz: `appMachineChangeDesired` liefert `(partial_result, nil)`.

### Differenz zwischen den zwei Aufrufern

- **CLI edit path** (`appEditApplyConfirmed`, cmd/baha/app_edit_apply.go:372):
  ```
  if changeErr == nil && result.Status != "complete" {
      return output, &appMachineError{Code: "partial"}
  }
  ```
  Fail-closed. ✓

- **MCP/HTTP edit path** (`app_registration_921.go:187-201`):
  ```
  result, err := appMachineChangeDesired(...)
  if err != nil { ... return machineMCPFailure(...) }
  return nil, result, nil   // <-- kein result.Status-Check
  ```
  Der `partial`-Fall wird hier nicht abgefangen: die Execution wird als Erfolg
  (`nil`-Error, MCP `IsError:false`) gemeldet, obwohl nicht alle Impakte
  attestiert sind. Das ist die **silent-success-Flaeche** (Teil b/c der Mission):
  ein Teilerfolg in einem der Execution-Schritte verlässt den Befehl exit-0.

## Repro (unit-only, ohne Container)

`RecordProviderChangeResult` mit einem `plan.Complete == true` Plan und einer
`outcomes`-Liste, in der ein Impact fehlt (`pending`):

- setup: `ProviderImpactPlan{Version: ProviderImpactVersion, PlanID: "x", Complete: true,
  Impacts: [{ID:A,Op:X}, {ID:B,Op:Y}]}`
- outcomes: nur `[applied A]` (B nicht attestierbar => fehlt)
- assert: `result.Status == "partial"` und `resultErr == nil`
- assert downstream: `appMachineChangeDesired` liefert `(partial, nil)`
- assert MCP-Pfad `app_registration_921.go:201` liefert `nil, result, nil` => IsError:false

Der CLI-Pfad (`appEditApplyConfirmed:372`) schlägt dagegen fehl; der MCP-Pfad
nicht. Das ist der Unterschied, den der Test abdecken muss.

## Geplante Korrektur (Owner-Scope, nicht in dieser Lane)

In `app_registration_921.go:193-201` den `result.Status != "complete"`-Check des
CLI-Pfades spiegeln (oder `appMachineChangeDesired` bei `Status == "partial"`
überhaupt einen error zurückgeben lassen). Kein Produkt-Change in dieser Hunt-Lane.

## Schnitt-Abschnitte ohne Fund (dokumentiert)

Schnitt (a) `err != nil` nahe `return nil`, cmd/baha + internal/application:
- review aller Multi-step lifecycles (apply, up, restore, update, destroy, doctor,
  remote apply, retirement, status, preflight, backup) => durchweg fail-closed.
- `observeApplicationProviderFacts` (app_core_requirement.go:401-408) liest
  `applicationRuntimeOwners` und überspringt bei error die Owner-Facts, liefert
  aber nur eine PARTIELLE facts-Map zurück. Aufrufer (`verifyApplicationRuntimeRetirement`,
  application_runtime_retirement_verification.go:14-25) behandeln einen fehlenden
  Fact als **Verification-Failure** (conservative), also kein silent-success.
- `complete := true`-Flags (application_provider_container_observation.go,
  application_provider_completion_observation.go, provider_material_files.go)
  werden durchgehend UND-verknüpft => fail-closed.

Schnitt (b) multi-step apply/reconcile/provision:
- repository_up.go, app_up_lifecycle.go, app_apply.go, restore lifecycle,
  update lifecycle: jeder Schritt propag seinen error, `recordObservedDeployment(...,true)`
  nur nach erfolgreichem verify. Kein "step 2 fehler => successful".
- `observeCanonicalProviderCompletion` (application_provider_container_observation.go:63):
  `complete` UND-verknüpft. Fail-closed.

Schnitt (c) exit-code-protokoll gegen CLI2-vertrag:
- `main.go:57-70` + `internal/cli/cli.go:82` (ExitCode): nil => 0, usage => 2, else 1.
- `app_machine_adapters.go:531` (`return result, nil`) ist die Stelle, an der ein
  `partial`-Result ohne error den Maschinendruck erreicht; der CLI-Pfad fängt es ab,
  der MCP/HTTP-Pfad nicht (siehe Befund).

## PLAN

- Mission gelesen, Scope als hunt-only (Befundung, keine Änderung, kein .github) bestätigt
- baseharbor remote HEAD verifiziert: 8dccd4fe1 (develop, nur merged content)
- Schnitt (a): sweep `err != nil` nahe `return nil` in cmd/baha + internal/application — durchweg fail-closed dokumentiert
- Schnitt (b): multi-step lifecycles (apply/up/restore/update/destroy/doctor/remote/retirement) — kein "step-2-fehler => successful"
- Schnitt (c): exit-code-protokoll gegen CLI2/MCP-vertrag — gap lokalisiert
- Befund 1 dokumentiert (partial-result silent-success im MCP/HTTP edit-pfad) mit Schwere + repro + PLAN
- evidence geschrieben, keine produkt-aenderung

## CLEANLINESS

- Kein Container / Compose Projekt gestartet (R1, hunt-only).
- Kein `.github/**` geändert, kein workflow_dispatch / rerun ausgelöst.
- git-Zustand unangetastet (nur lesen). `baseharbor`-Checkout nur Lesezugriff via git log/show.
- Keine fremden container/netzwerke/volumes berührt.
- cleanliness: OK — keine test-eigenen artefakte erzeugt.

## END

END_DONE mission-hunt-silentsuccess.md: Befund 1 (partial-result silent-success im MCP/HTTP edit-pfad), SHA 8dccd4fe1; Befundung abgeschlossen, keine produkt-aenderung.
