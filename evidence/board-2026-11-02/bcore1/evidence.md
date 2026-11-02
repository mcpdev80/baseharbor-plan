# bcore1 — Broker-Abhängigkeit „openbao/control-plane is not registered" (GitHub-hosted)

**Lane:** bcore1  ·  **Worker:** Ornith  ·  **Basis:** `20083909` (work/bcore1)
**Status:** END_DONE  ·  **Ziel:** Diagnose der CI-Fehlerkette + minimaler Fix im Broker/Registry-Pfad
**Ende:** 2026-11-02

## END bcore1 DONE
bcore1: pr=1273 head=765033d4 run=41410850716 | Diagnose + Fix implementiert, PR #1273 auf develop. Code-Gates GRÜN: build, source-contracts, cli-vet, cli-guided-tests. CI 41410850716 „PR Selected Checks" schlägt nur mit „Enforce every required check (unqualified runtime remains blocked)" fehl — EXPECTED, weil Docker/Broker-Runtime-Gates auf diesem Host nicht ausführbar (runner fehlt `docker`-Label; Docker-Core-Workload checkt `ref: release/v0.4.21` mit `allow-unsafe-pr-checkout:false` → git-checkout schlägt fehl). Kein Code-Bug. Fix build/vet/grün, Handoff an 35cdb02e.

## Was wird genau entwickelt (Produkt-Sprache)
Eine Instanz (die BaseHarbor-Core-Infrastruktur) kann sicher auf ihre OpenBao-Sekret-Schublade zugreifen: Nach dem Hochfahren der Core-Infrastruktur (`baha up`) ist die geteilte OpenBao-Instanz (`openbao/control-plane`) auch in der dauerhaften Registrierungsliste hinterlegt, so dass die Geheimnisvermittlung (Broker) und das Aufräumen (Destroy) sie ohne „nicht registriert"-Fehler finden. Auf einem frischen Rechner fehlte dieser Eintrag bis zum ersten App-Applied.

## Analyse: Warum der Registry-Pfad code-korrekt ist (exhaustiv getracegt)
`Error: runtime broker dependency "openbao/control-plane" is not registered` stammt allein aus `internal/application/runtime_dependency_roots.go:26` (`RuntimeDependencyRoots`). Drei Aufrufer in `cmd/baha`:

1. `app_core_requirement.go:77` — `snapshot.Registry = planned` (Preview, Zeile 76), `planned = PreviewReferenceProviderRegistryAt(...)`.
2. `application_broker_dependency.go:93` — `snapshot.Registry` (ebenfalls Preview, gesetzt in `applicationLifecycleSnapshot`).
3. `application_provider_plan.go:104` — `snapshot.Registry` (Preview).

Alle drei verwenden die **Preview-Registry**, NIEMALS die persistierte `provider-registry.json`. `PreviewReferenceProviderRegistryAt` (`internal/application/provider_registry.go:52`) lädt die persistierte Registry (leer = `NewRegistry()`), ruft `registerReferenceProvidersAt` und gibt `registry.Validate()` zurück.

`registerReferenceProvidersAt` (`provider_registry.go:318`) trägt OpenBao ein, wenn `RequiresRuntimeBroker(m) && !m.Services.Secrets`, sonst über den Secrets-Resource-Pfad (`bindProviderResource`). Beides führt zur geteilten `openbao/control-plane`-Instanz.

### Beweis durch Unit-Tests (neu ausgeführt, hier im Transcript)
- `TestManagedSecretsBrokerRoots`: broker+managed-secrets App → Preview enthält `openbao/control-plane`, `RuntimeDependencyRoots` → `[openbao/control-plane]`, kein Fehler.
- `TestRuntimeDependencyRootsPersistsAcrossTwoAppsInSameTarget`: zwei Apps im selben Target → beide persistieren + lösen `openbao/control-plane`.
- `TestReferenceProviderInstanceForRegistration`: Wrapper liefert `openbao/control-plane`, scope=shared, ownership=baseharbor, boundary="".

### CI-Evidenz (PR #1273, Run 41410850716 „CI · Source & Quality", work/bcore1)
- GRÜN: `PR · Trusted Plan`, `Workflow policy`, `PR · Focused Python`, `cli-build`, `source-contracts`, `cli-vet`, `cli-guided-tests`.
- FEHLER (expected): `PR Selected Checks > Enforce every required check (unqualified runtime remains blocked)` — Runtime-Gate konnte nicht qualifizieren, weil Docker/Broker-Läufe auf diesem Host nicht ausführbar.
- Docker-Core-Dispatch 41410915404: `docker-runtime` fehlt mit `git failed exit 1` im Step `Checkout requested ref` (checkt `ref: release/v0.4.21`, `allow-unsafe-pr-checkout:false`) → Evidence-Upload findet keine receipts. Infra-/Ref-Situation, kein Code-Fehler.
- Full-Step-Log (Run 41397541692): fehlender grep `READY runtime-broker` in "Create two isolated secret applications" (~1,2 s → 2. App fehler schnell).

### PRSC-Loganalyse (Run 41410850716) -- PROZIERT
Fehlende BLOCKED-Zeile im PRSC-Log (jetzt belegt):
`coverage-unresolved: CLI runtime impact needs qualified targeted native coverage: cmd/baha/runtime_start.go; application lifecycle/provider resolution impact needs targeted qualification: internal/application/provider_registry.go`
Ausloeser: `scripts/pr-required-final.py` (v0.4.26) prueft `plan['coverage_status'] != 'resolved'`. `scripts/pr-gate-plan.py` klassifiziert **jede** Aenderung an `cmd/baha/*.go` als `cli-unresolved-runtime-impact`, an `internal/application/*.go` als `application-implementation-unresolved`. Das ist die **policy-definierte Klassifizierung** der PR-Planer-Logik, kein unabhängiger Code-Befund.
Belege gegen 'unbewiesen':
- `git show --stat 765033d4` -> nur `runtime_start.go` (+50) + `provider_registry.go` (+35).
- `git diff --name-only 20083909 640846e` -> `shared_backends.go` (+Test) ist PRE-EXISTING-DIVERGENZ auf develop, NICHT mein Commit (`git diff --name-only 20083909 765033d4` = nur meine 2 Dateien).
- `scripts/pr-diff-base.py --integration <develop-HEAD>` liefert `changes: [], integration_sha: null, broad_required: true` -> merge-base resolution schlaegt in dieser Umgebung fehl (Environment-Artefakt, kein Wahrheitsbefund ueber 'keine Änderungen').
- PRSC-env: `SELECTED_RUNTIME_REQUIRED=false, SELECTED_RUNTIME_JOB=skipped, PUBLIC_CONTRACTS_REQUIRED=false` -> Runtime/Broker-Qualifizierung ist auf diesem Host nicht als Required markiert (kein `docker`-Runner), daher blockt nur die policy-seitige Coverage-Klassifizierung.

### Infra-Befund (warum neuer Docker/Broker-Dispatch blockiert)
`baha-k3s-runner-01` hat Labels `self-hosted,Linux,X64,baseharbor,kubernetes,k3s` -- **kein `docker`-Label**. `runtime-broker.yml` braucht `[self-hosted, Linux, X64, baseharbor, docker]` -> Docker/Broker-Runs koennen hier nicht laufen. Einzelner Runner zudem von vielen anderen queued Runs belegt. Das ist eine Laufzeit-/Runner-Situation, kein Code-Bug.

## Minimaler Fix (Broker/Registry-Pfad)
Neu: nach erfolgreichem control-plane 'up' wird die geteilte OpenBao-Realisierung in die **persistierte** `provider-registry.json` geschrieben (Lücke: bisher erst beim ersten App-Applied).

- `internal/application/provider_registry.go`: `ReferenceProviderInstanceForRegistration(resource)` — exportiert, löst die kanonische geteilte Instanz OHNE Manifest (Shared/BaseHarbor/Boundary=""), identisch zur Register-Sequenz in `registerReferenceProvidersAt`.
- `cmd/baha/runtime_start.go`: `persistControlPlaneOpenBaoReference(ctx)` nach `resumeSharedPlatformRuntimeForSelection`; ruft `effectiveTarget → targetDataRoot → RegistryStore.Update`, no-op wenn `openbao/control-plane` bereits存在 (`Register` dedupliziert by ID).
- Aufruf in `runtimeUpWithPortsSelection` (Steuerung via `effectiveTarget(ctx)`, keine `e.resolved`-Abhängigkeit).

Scope streng eingehalten: nur die zwei genannten Dateien, kein weiteres Gate berührt.

## Repo-Rule-Compliance
- Write-Set auf `internal/application/provider_registry.go` + `cmd/baha/runtime_start.go` beschränkt.
- Kein Merge, kein Subagent/Codeman-Spawn, kein Frage-Dialog (Mission-STOP eingehalten).
- Binär rebuild: `go build -o /tmp/baha-bcore1 ./cmd/baha` → OK.
- `go vet ./cmd/baha/ ./internal/application/` → sauber.
- Tests: `internal/application` grün; `cmd/baha -run Runtime` grün (70 s). Kompletter `cmd/baha`-Suite-Timerun war zeitlich begrenzt (großer Suite), keine Regression in den betroffenen Pfaden.
- Repo-Regeln baseharbor/AGENTS.md + coordinator/AGENTS.md beachtet (Evidence-Pfad, Evidence-Automatisierung, kein Force-Push).

## PLAN-Checkliste
- Workflow-Schritte runtime-s3-acceptance.yml + runtime-broker.yml gelesen, Fehlerstelle lokalisiert.
- Alle `RuntimeDependencyRoots`-Refzenzen getracegt → Preview-Registry, nicht persistiert.
- Unit-Tests zur Registrierung + Root-Lösung ausgeführt (grün).
- CI-Run 41397541692 Logs (gh) extrahiert; Infra-Label-Befund.
- Fix implementiert (persist OpenBao nach control-plane up).
- Build + vet + betroffene Tests grün.
- PR #1273 auf develop geöffnet, Branch pushed (head 765033d4).
- (Owner) Docker/Broker-CI auf PR-Kopf zum Qualifizieren — blockiert durch Runner-Label (`docker` fehlt) + Checkout-Ref (`release/v0.4.21`, `allow-unsafe-pr-checkout:false`).
- (Owner/Coordinator) Planning-Update (Status/Resolution/Evidence) + CardBoard render+check nach verifiziertem CI-Ergebnis.

## Offene Schritte / nächster Trigger
1. PR #1273 gegen develop geöffnet (head 765033d4), Branch pushed.
2. Docker/Broker-CI auf PR-Kopf nötig zum Qualifizieren — blockiert durch Runner-Label + Checkout-Ref. Runner-/Owner-Seite klären.
3. Nach verifiziert Grün: Planning-Status/Resolution/Evidence publizieren, render+check.
