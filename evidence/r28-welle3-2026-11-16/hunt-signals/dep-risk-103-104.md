# Dep-/Risk-Prüfung 0428-103 und 0428-104

Datum: 2026-11-17  
Rolle: CODEX-REVIEW / read-only Release-Scope-Analyse  
Produktbasis: `develop@bcae1e8c1261c9e44db03fe285a5d090c532dfcd`  
Vorherige Hunt-Akte: `befund-1.md` (Untersuchungsbasis `1df7c343`, zuletzt als unverändert bis `8db0d9bd` belegt)

## Ergebnis

| Karte | Empfehlung für v0.4.28 | Begründung und Sequenz |
| --- | --- | --- |
| 0428-103 — PostgreSQL-/Valkey-Adapter ohne Plan | **Ja, als release-kritische Vertrags-/Adapterarbeit nach #101 und #102; kein unbeschränkter Implementierungsauftrag.** | v0.4.28 verlangt reale Signale und nennt Datenbank- und Valkey-Dashboards. `RequiresAdapter` ist derzeit ausdrücklich nicht collectable; daher kann die aktuelle Capability-Deklaration diese Dashboard-Anforderung nicht erfüllen. Ohne Adapter dürfen keine Reihen erfunden werden. Die Karte muss zuerst Exporter, Signalvertrag, Deployment/Netzwerk, Ownership und Verifikation verbindlich festlegen; Umsetzung danach in einem begrenzten PR mit passender Runtime-Coverage. Eine Verschiebung nach v0.4.29 wäre nur mit einer ausdrücklichen Scope-Entscheidung möglich, die die Datenbank-/Valkey-Dashboard-Anforderung für v0.4.28 auflöst. Vor Beginn #101/#102 und deren Änderungen an Registry-/Runtime-Pfaden integrieren. |
| 0428-104 — Quellen ohne Destroy-Cleanup | **Ja, release-relevant nach #101 und #102; Umsetzung muss eng geschnitten und die gemeinsamen Lifecycle-Dateien reserviert werden.** | Persistente Registry-Einträge können nach Retirement weiterhin als Signale erscheinen und falsche/stale Observability erzeugen. Das betrifft Perses' reale Signal-Inventur und Runtime-Lifecycle. #104 hängt zwingend hinter #101: Keycloak registriert aktuell mehrere mögliche Instanzen unter `keycloak-metrics`; ein `Remove` vor der ID-Korrektur könnte die noch aktive Instanz mitentfernen. Nach #101 muss der Cleanup die korrigierte, instanzbezogene ID verwenden. Shared backends dürfen erst entfernt werden, wenn deren tatsächlicher Destroy erfolgt; ein App-Release darf keine noch genutzte Shared-Quelle entfernen. |

Der Readiness-Status `ready` in den beiden Karten bedeutet keine unabhängige Abnahme dieser Risiken. Für #103 ist die vorhandene Karte außerdem zu unbestimmt, um eine Implementierung zu starten: weder Exporter-Auswahl noch konkrete collectable Signals und Lifecycle-Vertrag sind festgelegt.

## Abgleich mit der aktuellen Produktbasis

Der Diff `8db0d9bd..bcae1e8c` enthält Änderungen an `runtime_observability.go`, `registry.go` sowie Prometheus-Datei- und Verifikationspfaden. #1676 fügt einen Workload-Snapshot mit `Verification: VerifyNone` hinzu. Der aktuelle Code dokumentiert den Target als symbolisch (`internal/application/runtime_observability.go:61-64, 78-93`); `syncProviderTargets` und `providerMetricNetworks` überspringen `VerifyNone` (`internal/metrics/prometheus_files.go:62-66, 160-164`), und `VerifyProviderSourcesAt` überspringt ihn ebenfalls (`internal/metrics/prometheus_verify.go:163-166`). Damit ist der frühere Hunt-Verdacht, ein solcher Snapshot werde als echter Scrape-Target ausgegeben, auf der aktuellen Basis ausgeräumt. Das erzeugt jedoch keinen PostgreSQL- oder Valkey-Exporter.

Auf der aktuellen Basis bleiben die Datenbank-/Valkey-Metriksignale in `reconcileRuntimeProviderObservability` auf Logs und Traces begrenzt (`internal/application/runtime_observability.go:141-171`). Die Capability-Deklarationen bleiben `RequiresAdapter` (`internal/capability/reference.go:35,48`); die Registry weist nicht-collectable Signale weiterhin zurück (`internal/capability/integration_contract.go:243-249`, `internal/observability/registry.go:193-207`). Im untersuchten Produktbaum ist kein PostgreSQL-/Valkey-Metrikadapter mit Compose-/Scrape-Pfad vorhanden.

Die Cleanup-Lücken aus Befund 3 bestehen in den geprüften Pfaden fort:

- **Keycloak:** Registrierung mit globaler ID `keycloak-metrics` (`internal/identityprovider/keycloak_realization.go:158-167`); Destroy-Pfade in `keycloak_realization.go:190-213` und `keycloak_files.go:382-408` entfernen keinen Registry-Eintrag.
- **Runtime Broker/Executor:** Registrierung in `cmd/baha/app_broker.go:137-158,279-299`; Broker-Retirement in `cmd/baha/runtime_destroy_all.go:365-368` und Executor-Destroy in `internal/runtimeexecutor/compose.go:232-247` entfernen ihn nicht.
- **Shared PostgreSQL/Valkey:** vollständiger Shared-Destroy läuft über `cmd/baha/runtime_destroy_all.go:459` nach `internal/application/shared_backends_resources_runtime.go:367-400`; der Destroy-Pfad entfernt keine Provider-Registrierungen. App-scoped Provider werden dagegen durch `PruneOwnedProviderInstances` in `runtime_observability.go:141-171` bereinigt. #104 darf diese bereits funktionierende App-scoped Bereinigung nicht duplizieren oder schwächen.

## Abhängigkeiten und Risikosteuerung

1. #104 benötigt #101 als akzeptierte Basis, bevor Keycloak-IDs gezielt entfernt werden können. Anschließend #102 berücksichtigen, weil es Signal-Registry-Konsumenten und den application-Provider-Pfad ändert.
2. #103 sollte erst nach #101/#102 neu bewertet werden. Exporter-Registrierung würde dieselben Capability-, Registry- und Runtime-Pfade berühren; ein gestapelter oder konkurrierender Edit wäre unnötig riskant.
3. #104 umfasst mehrere Lifecycle-Grenzen und eine gemeinsam genutzte Destroy-Datei. Vor Assignment die Write-Sets begrenzen (Keycloak, Runtime-Komponenten, Shared Backends), Tests den jeweiligen Destroy-/Retirement-Pfad abdecken lassen und die Projekt-/Sharing-Boundary beim Entfernen prüfen. Kein pauschales `Remove` auf Provider-Namen.
4. Für #103 muss zuerst festgelegt werden, welche echten Reihen ein Adapter bereitstellt, wie er sicher im vorhandenen Runtime-/Netzwerkmodell läuft und wie Docker/Podman sowie No-Data-Fälle geprüft werden. Ohne diese Entscheidungen ist die Karte keine ausführbare Implementierungsvereinbarung.

## Betroffene Dateien

Dateien, die auf `develop@bcae1e8c` direkt in den untersuchten Pfaden liegen:

| Thema | Produktdateien |
| --- | --- |
| #103 Registry-/Capability-Einordnung | `internal/capability/reference.go`, `internal/capability/integration_contract.go`, `internal/application/runtime_observability.go`, `internal/observability/registry.go` |
| #103 möglicher Adapter-/Prometheus-Pfad (Scope noch zu entscheiden) | `internal/metrics/prometheus_files.go`, `internal/metrics/prometheus_render.go`, `internal/metrics/prometheus_verify.go`, `internal/application/shared_backends_resources_runtime.go`; zusätzlich neue Adapter-/Compose-Dateien und fokussierte Tests erforderlich |
| #104 Keycloak | `internal/identityprovider/keycloak_realization.go`, `internal/identityprovider/keycloak_files.go`, passende Identity-Provider-Lifecycle-Tests |
| #104 Runtime Broker/Executor | `cmd/baha/app_broker.go`, `cmd/baha/runtime_destroy_all.go`, `internal/runtimeexecutor/compose.go`, `internal/application/runtime_component_observability.go`, passende `cmd/baha`-/Runtime-Executor-Tests |
| #104 Shared PostgreSQL/Valkey | `cmd/baha/runtime_destroy_all.go`, `internal/application/shared_backends_resources_runtime.go`, `internal/application/runtime_observability.go`, passende Shared-Backend-/Registry-Tests |

Die #103-Dateiliste ist ein Risiko-/Impact-Inventar, keine Freigabe, alle genannten Dateien in einen PR aufzunehmen. Tests sind hier als erwartete Nachbarbereiche aufgeführt, nicht als ausgeführte Prüfungen. Es wurden keine Produktdateien geändert und keine Produktchecks ausgeführt.
