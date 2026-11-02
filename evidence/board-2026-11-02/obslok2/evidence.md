# obslok2 — Loki-Log-Ingestion Verifikation scheitert auf GH-hosted

## Diagnose

### CI Run-Log Analyse

**Run:** 41397537623
**Job:** docker (ID 125122005565) — Acceptance · Observability Full Stack
**SHA:** 735acd954079a29cf92c00e652b71a70480ba1d9
**Test:** `TestObservabilityFullStackAcceptanceInCI`
**Manifest:** observability-fullstack-ci, environment="dev"
**Log scope:** `application,application-provider,platform-provider`

**Metrics-Ingestion:** ✅ PASSED in 4.0s
**Log-Ingestion:** ❌ FAILED nach 45.0s Timeout

### Fehlerbild

Die "Verifying log ingestion" Phase wartet 4× 10s-Intervalle auf Loki-Daten, dann 45s-Timeout.
Die Metrics-Verifikation (gleicher Caddy-Proxy-Muster) läuft durch — das Problem ist Loki-spezifisch.

### Ursache: `render.go` Zeile 286 — Container-Namens-Muster passt nicht

In `internal/logs/render.go` Zeile 286 erzeugt `alloyConfigForModeSources()` das
Relabel-Muster für Provider-Log-Quellen:

```go
pattern := "^(?:" + regexp.QuoteMeta(project+"_"+service+"_") + "[0-9]+|" + regexp.QuoteMeta(project+"-"+service) + ")$"
```

Für `project="bh-local-shared"` und `service="loki"` ergibt dies:

```
^(?:bh-local-shared_loki_[0-9]+|bh-local-shared-loki)$
```

Die tatsächlichen Docker-Compose-Containernamen sind:

```
bh-local-shared-loki-1
bh-local-shared-loki-access-1
```

**Das Muster matcht KEINEN davon:**
- Alternative 1 (`bh-local-shared_loki_...`): Unterstriche statt Bindestriche — mismatch
- Alternative 2 (`bh-local-shared-loki`): Exakter Match, aber Container haben `-N` Suffix — mismatch

Die Workload-Pattern in Zeile 232 funktioniert, weil sie `-(.+)$` verwendet:
```go
pattern := "^" + regexp.QuoteMeta(project) + "(?:_(.+)_[0-9]+|-(.+))$"
```
Das matcht `bh-local-observability-fullstack-ci-dev-api-1` korrekt.

### Fix

**Datei:** `baseharbor/internal/logs/render.go`, Zeile 286

**Vorher:**
```go
pattern := "^(?:" + regexp.QuoteMeta(project+"_"+service+"_") + "[0-9]+|" + regexp.QuoteMeta(project+"-"+service) + ")$"
```

**Nachher:**
```go
pattern := "^(?:" + regexp.QuoteMeta(project+"_"+service+"_") + "[0-9]+|" + regexp.QuoteMeta(project+"-"+service) + "-?[0-9]*)$"
```

Das `-?[0-9]*` am Ende der zweiten Alternative matcht optional `-N` Suffix.
Die erste Alternative mit Unterstrichen ist für legacy/podman-Konvention; sie
matcht bereits korrekt, weil sie `[0-9]+` am Ende hat.

### Query-Zeitfenster

Das Query-Zeitfenster (`start=now-10min, end=now`) in `querySeries` und `queryStream`
ist für die CI-Szenario ausreichend — 10 Minuten > 45s Timeout. Kein Problem.

### Loki-Startbereitschaft

Loki ist healthy: `grafana/loki:3.7.8` läuft, Caddy-Proxy reachable,
`auth_enabled: false` für die API. Kein Start-/Healthcheck-Problem.

## Repo-Rule Compliance

- Nur `internal/logs/render.go` geändert (single-file fix)
- Keine Workflow-Gate-Änderungen (STOP-Kriterium)
- Keine subagent/codeman-Spawn (STOP-Kriterium)
- Keine interaktiven Frage-Dialoge

## Test-Evidence

- `go build ./internal/logs/` → ✅ PASS
- `go test ./internal/logs/` → 26 Tests, alle PASS (0.047s)
  - `TestRetainedLokiInventoryPreservesOwnersAndExternalStorage`: ✅
  - `TestLokiDriverConsumesProviderConformanceHarness`: ✅
  - `TestVerifyApplicationUsesServiceAccessTLS`: ✅
  - `TestLokiProviderRuntimeDoesNotMountContainerSocket`: ✅
  - `TestLokiProviderSeparatesInternalTrafficFromHostPublishing`: ✅
  - `TestWorkloadLoggingOverrideUsesLoopbackSyslog`: ✅
  - `TestLokiConfigKeepsWALOnWritablePersistentVolume`: ✅
  - `TestLokiConfigBindsIPv4ForLoopbackPublishing`: ✅
  - `TestPodmanJournalConfigAcceptsComposeAndQuadletWorkloadNames`: ✅
  - `TestProviderLogSourceVerificationRejectsInvalidSemanticIdentity`: ✅

## PLAN

- [x] 1. Volle Fehlerzeile + vorangehende Zeilen aus CI Run 41397537623 Job-Log ziehen
- [x] 2. Ursache triagieren: `render.go:286` — Container-Namensmuster matcht keine `-N` Suffix
- [x] 3. Minimaler Fix an `render.go:286` — `-?[0-9]*` an Pattern-Ende hinzufügen
- [x] 4. Local test verification (go test ./internal/logs — 26 Tests PASS)
- [ ] 5. PR gegen develop, Observability-Dispatch beobachten

## END_DONE

obslok2: fix applied at internal/logs/render.go:286 — renders `-?[0-9]*` suffix on provider log patterns. All 26 unit tests pass. PR against develop needed for CI validation.
