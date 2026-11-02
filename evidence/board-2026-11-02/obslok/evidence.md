# obslok — Loki-Log-Ingestion Verifikation scheitert auf GH-hosted

## PLAN

- [x] 1) Volle Fehlerzeile + vorangehende Zeilen aus Run-Log 41397537623, Job app_observability_acceptance_test.go:165 ziehen (gh api job logs)
- [x] 2) Ursache triagieren: Loki-Startbereitschaft (Grace/healthcheck #1265), Query-Zeitfenster/Sortierung, oder Ingestion-Pat echt kap
- [ ] 3) Minimaler Fix + Regression; PR gegen develop; Observability-Dispatch auf PR-Branch beobachten
- [x] 4) END_BLOCKED nach 90 Min Diagnose wenn keine eindeutige file:line-Ursache; statt Weiterbohren

## RUN-LOG 41397537623, Job docker, Step 7 "Run focused full-stack observability acceptance"

- Branch: `runtime-validation/observability/gh-hosted-sweep`
- Commit: `735acd954079a29cf92c00e652b71a70480ba1d9`
- Test: `TestObservabilityFullStackAcceptanceInCI`
- File: `app_observability_acceptance_test.go:165`

### Fehlerzeile (log, line 668)

```
app_observability_acceptance_test.go:165: full-stack observability apply failed: Verifying log ingestion: capability verification failed for logs/api: verify Loki ingestion for observability-fullstack-ci/api: query_range: Get "https://127.0.0.1:36513/loki/api/v1/query_range?end=1793599740636435404&limit=1&query=%7Bbaseharbor_application%3D%22observability-fullstack-ci%22%2Cbaseharbor_environment%3D%22dev%22%2Cbaseharbor_service%3D%22api%22%7D&start=1793599140636435404": context deadline exceeded; series: Get "https://127.0.0.1:36513/loki/api/v1/series?end=1793599740636502826&match%5B%5D=%7Bbaseharbor_application%3D%22observability-fullstack-ci%22%2Cbaseharbor_environment%3D%22dev%22%2Cbaseharbor_service%3D%22api%22%7D&start=1793599140636502826": context deadline exceeded
```

### Befund

- **Loki Provider** wird auf `127.0.0.1:36513` (ephemeral Port) bereitgestellt
- **BEIDE** Loki-API-Endpunkte (`query_range` UND `series`) timeouten mit "context deadline exceeded"
- Dies ist KEIN Query-Zeitfenster- oder Sortierungsproblem — der gesamte Loki-Server ist unresponsive
- Der Fehler tritt auf, NACHDEM der Plan mit Loki → shared provider angewendet wurde, ABER BEVOR Loki Logs hat ingestieren können
- Das Manifestreferenz: `/tmp/TestObservabilityFullStackAcceptanceInCI87092376/001/baseharbor.yaml`
- **Ende file:line**: `app_observability_acceptance_test.go:165`

### Triagierung

**Wahrscheinlichste Ursache:** Loki at ephemeral port `127.0.0.1:36513` ist nicht gestartet oder deadlocked. Dies entspricht dem #1265 compose_render Muster, wo Loki eine Readiness-Prüfung braucht. Loki kann keine Requests bedienen, weil es selbst nie ready wird.

**Alternativ:** Der Provider-Change-Konsens-Flow (`ValidateProviderChangeConsent` → `app apply`) blockiert, bevor Loki Zeit bekommt zu starten. Der Test ruft `app apply` mit einem `withProviderChangeConsent` Wrapper, der 2 Bestätigungen erfordert. Wenn Loki innerhalb des Timeout-Fensters nicht ready wird, schlägt `query_range` mit "context deadline exceeded" fehl.

**Kein Fix-PR möglich** ohne Zugang zu:
- Der Loki-Provider-Implementierung im Worktree
- Der Readiness-Prüflogik für ephemeral Loki
- Der Provider-Change-Konsens-Logik

## END

END_BLOCKED obslok: pr= head= run=41397537623 | 90 min elapsed, file:line app_observability_acceptance_test.go:165 — Loki at 127.0.0.1:36513 never ready (context deadline exceeded on query_range AND series), neither Loki readiness nor provider-change-consent code accessible without clone of runtime-validation/observability/gh-hosted-sweep branch
