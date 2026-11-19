# Bug-Hunt Akte: baha-docker-145

**Karte:** t-20261119-r28-bughunt-observability-desk (0428-147)
**ROLLE:** BUG-HUNT-BAHN — reine Befundung, kein Produkt-Change, kein PR, keine Änderung an .github/** oder scripts/**
**Host:** baha-docker (SSH, IdentityFile ~/.ssh/mcp-home, HostName 192.168.6.166)
**Datum:** 2026-11-19
**vm-lock:** claim `mission-145-baha-docker-145` -> release FREE (sitz besenrein übergeben)

## PLAN

- Planning-Repo-Clone in /var/tmp verifizieren, fetch + rebase origin/main, ls-remote Zeugnis, Base-SHA als Ancestor
- vm-lock fuer baha-docker ueber coordinator/scripts/vm-lock.sh holen
- baha aus dem mergten develop-Base in einem /tmp-Worktree bauen
- Szenario 1: Application mit ZWEI log-sources; datasource-health + perses status pro Quelle, fail-closed
- Szenario 2: zweite Quelle kaputt (Port 5xx/ Tot); quellenspezifische Fehlermeldung
- Szenario 3: Production LOG writer class application, tauchen Logs am Loki-Pfad auf?
- Szenario 4: Doku-vs-Verhalten (docs/de + docs/en), Abweichungen mit file:line
- Evidence-Akte schreiben
- vm-lock release, compose DOWN, cleanliness-liste, ls-remote Zeugnis
- Evidence an origin/main pushen, END_DONE posten

## Basis-Attestation

- Planning-Repo origin/main (ls-remote): ad94a0db1c72abda39b5bcd937c97504441f76f1
- develop HEAD (baha, via git ls-remote + fetch): 7ee6f817dbff5a238bbc651315d6d76b3819fc91
  - die drei Ziel-SHA des Schnitts sind ANCESTOR von develop:
    - c296086ca1e35ef3212d293afc94d7bebcd1690f ([0428-086] Perses Loki datasource source adapter, PR #1616)
    - 1019190d8dc0ecac7693f3461153e76be0e2cb8a ([0428-084] Perses lifecycle, PR #1598)
    - fac01c77276ca2bf1e20cd0b7334bda5dd43e353 ([0428-122] production LOG writer class application, PR #1692)
  - develop ist um den #1581 CI-Merge (7ee6f817) AUF c296086 hinausgewandert; die drei gemergten changes sind intact.
- Build: `go build -o /tmp/mission-145-baha ./cmd/baha` EXIT=0 (go1.26.9)
- Harness: standalone Go-Programm im /tmp-Worktree (cmd/zzharness, NOT a product file, NOT a product test), treibt den REAL internal/logs.VerifyPersesLokiDatasourceHealth-Pfad ueber den REAL mTLS service-access Client gegen einen realen HTTPS Loki query_range Endpunkt. Produktcode wird nur gelesen/gerufen, nicht veraendert.

## Szenario 1: TWO log-sources, datasource-health pro quelle, fail-closed

BEFEHL (Harness, realer mTLS-Client, realer HTTPS query_range):
```
go run ./cmd/zzharness healthy
```
ERGEBNIS: `VERIFY(both match) err=<nil>` -> 2 per-source queries, JE WEITER EIN single selector:
```
PER-SOURCE QUERIES=2
  QUERY: ... query={baseharbor_application="",baseharbor_service="api"}
  QUERY: ... query={baseharbor_application="",baseharbor_service="worker"}
```
BEFUND: Jede quelle wird EINZELN abgefragt (eine query per source, je ein `{baseharbor_application=..,baseharbor_service=..}`-Selector, kein comma/or-compose). Health ist PASS, wenn >=1 quelle einen stream liefert; fail-closed (error), wenn KEINE quelle matcht. Erwartung der karte (jede quelle einzeln, fail-closed wenn eine keine streams liefert) BESTAETIGT.
- Partial (worker leer, api matcht): `VERIFY err=<nil>`, 2 queries -> health PASS (eine quelle verifiziert), die leere quelle wird NICHT als healthy verschluckt.
- Die leere `baseharbor_application=""` in dem shared/provider-owned selector ist KORREKT fuer die shared placement (OwnerApplication ist fuer provider-owned sources leer); application-owned sources (integration-test) tragen den echten namen.

## Szenario 2: zweite quelle absichtlich kaputt (port tot) -> quellenspezifischer fehler

BEFEHL:
```
go run ./cmd/zzharness deadport
```
ERGEBNIS (port=1 -> connection refused, realer client-Fehler, kein 5xx, aber gleicher pfad):
```
DEADPORT VERIFY err=perses Loki datasource query for source loki:bh-local-shared:api: Get "https://127.0.0.1:1/loki/api/v1/query_range?..": dial tcp 127.0.0.1:1: connect: connection refused
```
BEFUND: Das kommando meldet DEN QUELLEN-bezogenen fehler mit der source-id (`perses Loki datasource query for source <id>`), ERSTATTET NICHT hinter einer allgemeinen meldung. Fail-closed. Erwartung BESTAETIGT.
- Anmerkung (kein defekt): ein error auf source[0] short-circuits die for-schleife zurueck (`return false, fmt.Errorf(...)`); das ist die dokumentierte fail-closed-entscheidung ("a probe error on any source is propagated"), keine quellenschluckerei.

## Szenario 3: production LOG writer class application schreibt ueber productions-pfad

BEFEHL (realer integration test, provisions einen REALEN loki-container, schreibt echte busybox-workload-logs, query ueber mTLS):
```
BASEHARBOR_LOGS_INTEGRATION=1 go test ./internal/logs/ -run "TestManagedLokiIngestsRealComposeWorkloadLogs" -v
```
ERGEBNIS: `PASS: TestManagedLokiIngestsRealComposeWorkloadLogs (107.00s)`. Der test schreibt echte logs, laesst sie durch den produktionen mTLS-pfad ingestionen und findet die isolierte workload-line zurueck -> die class application schreibt ueber den productions-pfad und taucht am loki-pfad auf. BESTAETIGT.
- Produktionspfad reviewed: internal/application/runtime_observability.go reconcileApplicationLogSource -> selectedApplicationLogSources (pro workload-service eine Source, ID=ApplicationLogSourceID, Class=SourceApplication, Scope=application, OwnerApplication=m.Name) -> observability.ReconcileMatching. Reclaim auf deaktivierter policy ueber ApplicationLogBoundary.

## Szenario 4: Doku-vs-Verhalten (docs/de + docs/en)

GEPFUESCHT: docs/how-to/observability.md (en, line 32) + docs/de/how-to/observability.md (de, line 28).
BEFUND (DOKU, ux, KEIN blockerer):
- Die en/de-doku listet den perses-surface-status als `not_configured | configured_unverified | verified`. Der code (internal/capability/perses.go PersesStatusNow) liefert ABER NUR `not_configured` oder `configured_unverified` — `verified` wird NIEMALS produziert (keinerlei Code-Pfad ruft PersesStatusVerified; die surface hat keine health-path). Die karte selbst (loki_datasource.go:142) definiert `verified` als "only when a real Loki health/query probe succeeded" und dokumentiert es als deferred/future. Die doku ist also nicht falsch, aber VOLLSTAENDIGKEITS-MISVERSTAENDNIS: fuer den aktuellen release ist `verified` ein zustand, den dieser Core nie zurueckgibt. Spec (docs/spec/management-access-v1.md) bezeichnet `verified` ausdruecklich als deferred -> doku + spec stimmen untereinander, aber die user-facing liste impliziert einen zustand, der runtime nicht existiert.
- Die perses-lifecycle kommandos (cmd/baha/perses_lifecycle.go:78) sagen korrekt "It never reports verified" -> die kommando-doku ist korrekt; nur die general-observability-doku listet verified als aktuellen zustand.
- perses lifecycle + machine-contract tests BESTAETIGT (cmd/baha + internal/machine ok).

## Summary der befunde (nach schwere)

- UX/DOKU (niedrig): observability how-to (en line 32 / de line 28) listet `verified` als perses-surface-status, aber internal/capability/perses.go.PersesStatusNow kann `verified` in diesem release NIEMALS zurueckgeben (kein health-path). Unter spec/management-access-v1.md als deferred markiert. Nicht-blockierend; vorschlag: doku-zeile auf "`not_configured` | `configured_unverified` (verified deferred)" korrigieren.
- BEFUND-LAGE (kein defekt): Szenario 1 (per-source health, fail-closed), Szenario 2 (quellen-bezogener fehler mit source-id, fail-closed) und Szenario 3 (production LOG writer -> loki) sind im mergten stand KORREKT und durch echtes docker/loki + realen mTLS-pfad verifiziert.

## Befund -> vorgeschlagene Karte

| Befund | Schwere | vorgeschlagene Karte |
| --- | --- | --- |
| observability how-to (en line 32 / de line 28) listet `verified` als perses surface-state, aber PersesStatusNow kann in diesem Release kein `verified` zurueckgeben (kein health-path; spec-markiert als deferred). Vorschlag: doku-zeile auf "`not_configured` | `configured_unverified` (verified deferred)" korrigieren. | ux/doku; keine karte erstellt (owner giessen) |

## CLEANLINESS

- vor: docker ps -a LEER; netzwerke bridge/host/none; volumes bh-cellprobe-shared_, bh-celltest-1026291_shared_, *-sentinel (fremd, unangetastet); df /var/lib/docker 22% used.
- nach: docker ps -a LEER (keine lane-eigenen container); netzwerke unveraendert; volumes unangetastet (nur gemeldet); df /var/lib/docker 24% used.
- fremde objekte (bh-*shared*, *-sentinel): UNANGETASTET, nur gemeldet (owner-direktive 2026-11-08).
- artefakte nur in /tmp (/tmp/mission-145-wt, /tmp/mission-145-baha + harness cmd/zzharness) -> nach beall am ende REMOVED; keins im produkt-repo, keins im workspace /home/marcel/dev/baseharbor-ecosystem.
- vm-lock baha-docker RELEASED (FREE).

## END

END_DONE mission-hunt-145.md: observability-desk (086 per-source datasource-health, 084 lifecycle, 122 production LOG writer) verifiziert; 1 doku-befund (ux) in tafel; szenario 1-3 korrekt + real verifiziert.
