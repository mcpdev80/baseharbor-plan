# CODEX-REVIEW 0427-173 r2 — PR #1505

ROLLE: REVIEW
Kandidat: `18e048681132c5d63bed10c17f7a48e454002723`
PR: https://github.com/mcpdev80/baseharbor/pull/1505
Ergebnis: KORREKTUR

## PLAN

1. Den live PR-Head, develop-Head, ancestry und exakten hosted Lauf verifizieren.
2. Die r1-Befunde an Selector, Ausgabeform und CLI-Einstieg gegen den Kandidaten vergleichen.
3. Die Lösch- und Target-Auflösungspfade sowie Tests und CI-Zuordnung prüfen.
4. Das SHA-genaue Urteil mit Korrekturrezept veröffentlichen.

## Befunde

1. **Blockierend — MCP ignoriert `input.Target` und kann das falsche Target verändern.** `registerMCPAppPruneTool` setzt das angeforderte Target in `cmd/baha/app_prune.go:311-313`. Danach setzt `resolvePruneByName` in `cmd/baha/app_prune.go:232-235` den Override explizit auf leer. `withTargetOverride` speichert diesen leeren Wert (`cmd/baha/target.go:53-55`); `effectiveTarget` fällt damit auf `BASEHARBOR_TARGET` oder das Default-Target zurück (`cmd/baha/target.go:87-95`). Sowohl die Autorisierung (`app_prune.go:317`) als auch die anschließende Löschung können daher ein gleichnamiges Deployment auf einem anderen Target treffen. **Rezept:** den expliziten MCP-Target-Override durch die Resolverkette erhalten; das autorisierte, aufgelöste Deployment anschließend unverändert an die Löschung übergeben oder seine Identität vor der Mutation erneut exakt validieren. Regression im MCP-Einstieg: zwei Targets mit gleichem App-Namen, explizit gewähltes Target wird entfernt, anderes bleibt byte-identisch, und Autorisierung bezieht sich auf dieselbe Target-/Deployment-Identität. **Stoppkriterium:** ein Target-Parameter darf niemals still auf ENV/Default umgelenkt werden; alle drei Identitätsprüfungen müssen im CI-Test grün sein.

2. **Blockierend — der applied-intent-Schutz ist in der behaupteten fehlende-Quelle-Konstellation nicht belegt.** `TestAppPruneRefusesRecordWithAppliedIntent` in `cmd/baha/app_prune_test.go:225-263` setzt `Repository: repo` auf ein existierendes `t.TempDir()`. Ebenso verwendet `TestAppPruneLiveSourceUnchangedOnRefusal` (`:378-424`) eine vorhandene Quelle. `executeApplicationPrune` prüft `SourceAvailable` zuerst (`cmd/baha/app_prune.go:90-99`), sodass beide Fälle vor dem applied-intent-Guard bei `:101-112` zurückkehren. Der Guard ist vorhanden, aber der r1-Nachweis für „Quelle fehlt, angewandte Absicht besteht, Eintrag bleibt unverändert“ ist weiter offen. **Rezept:** eine CLI-Entry-Regression mit nicht existierendem Repository und nicht leerem `Applied.Intent` hinzufügen; `runWithIO` muss verweigern und `deployment.json` byte-identisch erhalten. Den Test so ausstatten, dass kein Runtime-/Provider-Lifecycle gestartet wird; für die Live-Quellen-Verweigerung zusätzlich die behauptete Runtime-/Netz-/Volume-Unverändertheit durch einen expliziten Provider-Aufrufzähler oder geeignete Zustands-Snapshots belegen. **Stoppkriterium:** der neue Test muss den `RECORD_NOT_DANGLING`-Zweig tatsächlich erreichen und ein Lösch- oder Lifecycle-Aufruf muss als Fehlschlag auffallen.

3. **Korrektur — veraltete Selektor-Hinweise widersprechen dem jetzt erzwungenen Ein-Namen-Vertrag.** Die CLI verlangt genau einen Namen und weist Flags zurück (`cmd/baha/app_prune.go:208-225`), aber Datei-Kommentare versprechen weiterhin `--uuid`/`-e` (`:29-31`, `:79-85`) und der Mehrfachtreffer-Fehler verweist auf das nicht unterstützte `baha app prune --uuid ...` (`:265-282`). **Rezept:** entweder einen Selektor implementieren und mit Parsing-, Mehrdeutigkeits- und CLI-Regressionen absichern, oder alle nicht unterstützten Optionen aus Kommentaren/Fehlertext entfernen und ausdrücklich sagen, dass ein mehrdeutiger Name unverändert verweigert wird. **Stoppkriterium:** jeder ausgegebene nächste Schritt muss vom Parser akzeptiert werden; Mehrfachtreffer bleiben unverändert.

## Delta, Testabdeckung und hosted status

Der r1-Befund „fehlender Name kann alle/einen Eintrag auswählen“ ist geschlossen: `Usage` verlangt `<name>`; `requirePruneName` verweigert keinen Namen, zusätzliche Namen und Flags; `TestAppPruneRefusesNoName` läuft über `runWithIO` und prüft den Eintrag byte-identisch. Der r1-Befund zur gemischten Ausgabe ist für die CLI geschlossen: `--json` wählt JSON, sonst wird nur Klartext geschrieben; `TestAppPruneJSONOnlyValid` und `TestAppPruneHumanHasNoJSONTrailer` prüfen beide Formen. Der MCP-Pfad serialisiert allerdings erst in einen Puffer und parst dann mit `resultFromPruneOutput`; dieser Parser ignoriert JSON-Fehler und liefert bei Fehlern einen Nullwert (`app_prune.go:320-335`), statt wie die Runde-2-Akte behauptet direkt ein strukturiertes Ergebnis zurückzugeben. Ein MCP-spezifischer Regressionstest fehlt.

Die CLI-Regressionen sind nicht nur lokale oder VM-Belege: `scripts/pr-unit-database.sh:32-33` führt `go test ./... -count=1` aus; der Workflow-Runner ordnet `go-unit-tests` diesem Skript zu (`.github/workflows/ci.yml:915`). Der tatsächlich gehostete Job `PR · Validation · go-unit-tests` führte deshalb `cmd/baha` im Pull-Request-Lauf aus. Das deckt die Tests dauerhaft ab, auch wenn der Kartentext die Gruppe `cli-surface` nennt. Neue Tests aus der Korrekturrunde müssen ebenfalls von diesem Job ausgeführt werden. Kein Workflow wurde verändert oder erneut ausgelöst.

Run `42543119434`, event `pull_request`, exakt `18e048681132c5d63bed10c17f7a48e454002723`: terminal `completed/success`. `go-unit-tests` Job `128922288022` success; `go-build`, `go-vet`, `cli-gofmt`, Dokumentations-Audit, EN/DE MkDocs, Pages-Candidate-Build, wizard-registration-tests und `PR Selected Checks` Job `128924730658` success. Native destroy-retry Docker und Podman Jobs `128922275542` und `128922275557` success. Native Keycloak/Core wurde übersprungen und wird nicht als ausgeführter Pass gewertet.

## Base, Scope und abhängige Karte

`git ls-remote` zeigte PR-Head `18e048681132c5d63bed10c17f7a48e454002723` und damaligen develop-Stand `20902f0a6ab016fd8fe6a501751e1becc5f334dd` in der PR-Basis. Der aktuell gelesene develop-Head ist `b3a8042d18ea60f162a32a51df34a499cad6a237`; der Kandidat enthält diesen aktuellen Stand nicht als Ancestor. Der alte Basis-SHA `20902f0a6ab016fd8fe6a501751e1becc5f334dd` ist Ancestor des Kandidaten; der aktuelle develop-SHA ist es nicht. Vor weiterer Abnahme muss der Kandidat auf aktuellen develop integriert und der erforderliche Lauf auf dem resultierenden exakten Head beobachtet werden.

Der PR-Write-Set umfasst 15 Dateien aus `cmd/baha`, Dokumentation und Maschinenvertrag; keine `.github/**`-Datei. Die Review hat den Produktkandidaten nicht verändert. `scripts/plan.py show t-20261108-bughunt-app-prune-dangling-record` meldet außerdem, dass die Abhängigkeit `t-20261108-bughunt-list-stale-after-kill` noch nicht accepted ist. Diese Vorbedingung ist vor Kartenannahme aufzulösen.

## Remote witnesses

`git -C /tmp/opencode/0427-1500-r3-review-wt ls-remote origin refs/heads/develop refs/pull/1505/head` returned:

```text
b3a8042d18ea60f162a32a51df34a499cad6a237	refs/heads/develop
18e048681132c5d63bed10c17f7a48e454002723	refs/pull/1505/head
```

`git merge-base --is-ancestor 20902f0a6ab016fd8fe6a501751e1becc5f334dd origin/pr-1505` returned 0; the same check for current develop `b3a8042d18ea60f162a32a51df34a499cad6a237` returned 1. Planning remote verified as `https://github.com/mcpdev80/baseharbor-plan.git`; its live `origin/main` before this evidence commit was `b796a4f72875506c58d12ad57b94ca4b562ac4bd`.

## Urteil und Korrekturrezept

**KORREKTUR.** Die drei früheren Problembereiche sind nicht vollständig erledigt: verpflichtender Name ist nun fail-closed; CLI-Ausgabe ist jeweils ein Format; die relevanten Tests laufen im gehosteten `go-unit-tests`-Job. Die Review bleibt dennoch blockiert durch den verlorenen MCP-Target-Override und den nicht erreichten applied-intent-Schutztest. Dazu kommen irreführende `--uuid`-Hinweise und der Base-Drift.

Umsetzung in `cmd/baha/app_prune.go` und `cmd/baha/app_prune_test.go`: Target-Auswahl für MCP erhalten, aufgelöste Identität durch Autorisierung und Mutation stabil halten, fehlende-Quelle-plus-applied-intent als CLI-Regressionsfall ergänzen, MCP-Target-Auswahl und structured result testen, und Selektor-Hinweise parser-konsistent machen. Geänderte Tests müssen im gehosteten `go-unit-tests`-Job tatsächlich ausgeführt werden. Danach auf aktuellen develop integrieren und den exakten PR-Lauf erneut prüfen; die aktuelle grüne Run-ID ist kein Beleg für einen geänderten SHA.

END_DONE 0427-173-review-r2: KORREKTUR — Kandidat `18e048681132c5d63bed10c17f7a48e454002723`; Evidence auf baseharbor-plan origin/main zu publizieren.
