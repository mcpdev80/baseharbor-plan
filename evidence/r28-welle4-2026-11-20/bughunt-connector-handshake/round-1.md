# BUG-HUNT H-V16 — connector handshake: timeout/retry + identity provider/connector

Reine Befundung. Kein Produktcode, kein Commit, kein PR, kein Merge.

## Anker (develop)

- `internal/identityprovider/keycloak_realization.go` (registration, readiness)
- `internal/observability/registry.go` (List/Remove, exakte ID)
- `internal/logs/realization.go` (Loki-Signale, placement.Project)

Verbindliche develop-HEAD, gegen den gelesen:

- `git ls-remote origin refs/heads/develop` -> `36d075fad77fa61ac8c153e979855546589b32c2`
- Akten-Source = frischer exact-develop Clone: `/var/tmp/baseharbor-hv16-dev`, Branch `develop`, HEAD `36d075fad77...`.
- Planning-repo `origin/main` gelesen gegen: `c61d7253b6a0985c761e97617cb82b6018802d38`.

## PLAN

1. planning-repo root attestieren (origin/main) + remote develop HEAD.
2. frischer exact-develop Clone von baseharbor in /var/tmp (read-only anchor source).
3. S1: configurierte Wartezeit + Zeile, die sie setzt (keycloak_realization.go registration/readiness).
4. S2: nach Timeout ist der Zustand wieder betretbar (idempotent) oder bleibt ein halb-regiertes Signal stehen.
5. S3: zwei schnelle parallele Versuche — verliert einer stille Information?
6. S4: Provider ohne Signale — fail-closed oder leer sichtbar (registry List/Remove exakte ID, logs Loki placement.Project).
7. Akte + commit/push origin/main.

## PRUEFWEG (jede Zeile mit datei:zeile belegt)

### S1 — Wartezeit: was ist wirklich konfiguriert, welche Zeile setzt sie?

Die Readiness-Wartezeit des Connector/Identity-Handshakes liegt im Driver, der
die Realization aus `keycloak_realization.go` antreibt.

**keycloak_driver.go:704** — `const identityEndpointReadyTimeout = 4 * time.Minute`

**keycloak_driver.go:706-740** `waitIdentityEndpoint` — pollt `GET /realms/master/.well-known/openid-configuration`
in 500ms-Ticks bis 4 min; gibt `nil` bei HTTP-Status < 500, sonst `last`-Fehler;
nach Ablauf: `keycloak_driver.go:734` -> `"...identity endpoint readiness timeout after 4m: %w"`
bzw. `keycloak_driver.go:736` -> `"...identity endpoint readiness timeout after 4m"`.
`ctx.Err()` schlägt einen eigenen Timeout durch (`keycloak_driver.go:730-732`).

Diese 4-Minuten-Wartezeit wird in **keycloak_realization.go:89** nur als
diagnosticCtx (15s) fortgesetzt, NACHDEM `lifecycle.Apply` fehlgeschlagen ist —
die eigentliche Readiness-Wartezeit des Handshakes ist also die 4-min `waitIdentityEndpoint`,
aufgerufen in **keycloak_driver.go:335** (`adminClient`).

Zusätzliches Login-Retry nach der Readiness:

- **keycloak_driver.go:349** — `loginCtx` = `ctx` + 20s.
- **keycloak_driver.go:351** — `ticker := 500ms`.
- **keycloak_driver.go:355** — pro Versuch `attemptCtx` = 5s.
- **keycloak_driver.go:363-364** — retrybar nur bei `transientKeycloakAdminLogin` oder
  `400 + body contains "invalid_grant"`.
- **keycloak_driver.go:370** — nach `loginCtx`-Ablauf: `ctx.Err()` weitergeben, sonst
  `keycloak_driver.go:373` -> `"...Keycloak admin authentication did not converge within 20s: %w"`.

Loki-Readiness (logs/realization.go):

- **logs/realization.go:140** — `waitLokiReady(ctx, ...)` im `Apply`.
- **logs/query.go:20-44** — pollt `/ready`, 500ms-Tick, gibt nach `ctx.Done()`
  `logs/query.go:41` -> `"...Loki readiness: %w"` zurück (kein eigener konstanter
  Timeout, `ctx` ist der Gatekeeper).
- **logs/realization.go:151** — nach erfolgreicher Readiness folgt `registerProviderSignals`.

Keycloak PKI-Rotate (retry-Wege im Connector):

- **keycloak_driver.go:506-515** `waitKeycloakNativeCertificateReload` — Timer
  `2*keycloakCertificateReloadPeriod + 2s`, sonst `ctx.Err()`.
- **keycloak_database_reload.go:68** — per-attempt `10s`; **keycloak_database_reload.go:87**
  Fehlermeldung mit `attempts` + `per-attempt timeout: 10s`.

ERWARTET (Vertrag): eine konstante, begrenzte Wartezeit pro Phase.
IST (gemessen): `4m` Readiness (keycloak_driver.go:704), `20s` Admin-Auth
(keycloak_driver.go:349), `5s` per-attempt (keycloak_driver.go:355), 500ms Ticks
(keycloak_driver.go:710, keycloak_driver.go:351). Keine unendlichen Wartezeiten.
VERHALTEN KORREKT.

### S2 — nach Timeout ist der Zustand wieder betretbar (idempotent) oder bleibt ein halb-regiertes Signal stehen?

`keycloak_realization.go:85-95` (lifecycle.Apply): schlägt fehl, ruft
`Diagnostics(ctx)` mit 15s diagnosticCtx und gibt den Fehler zurück. `Apply`
bricht ab, **bevor** `keycloak_realization.go:114 registerKeycloakSignals()` läuft.
Ein halb-regiertes Signal bleibt also NICHT stehen — die Signalregistrierung ist
die letzte Aktion von `Apply` und wird bei fehlgeschlagenem Lifecycle-Skip umgangen.

Wiederholter `Apply` (idempotent):

- `RegisterProviderSignals` (registry.go:250-260) ersetzt Einträge durch
  `existing.ID == registration.ID && existing.Provider == Descriptor.Provider.Kind`.
  Zweiter Aufruf löscht den alten Eintrag exakter ID und schreibt neu — kein
  Duplikat, kein stehengebliebener halber Zustand.
- `registerKeycloakSignals` (keycloak_realization.go:132-171) baut `registrationID`
  = `"keycloak:" + files.Project` neu, `signals`-Map lokal, `RegisterProviderSignals`
  ersetzt by-ID. Saubere Wiederholung.
- `Existing` (keycloak_realization.go:173) und `Diagnostics` (keycloak_realization.go:186)
  erlauben Wiederaufnahme ohne neuen lifecycle.Apply.

Keycloak `reconcile` in RotatePKI (keycloak_driver.go:526-578) ruft `Apply`
zweimal (`reconcile(true)`, `reconcile(false)`) und verifiziert mit
`adminClient` (keycloak_driver.go:574). Ein fehlgeschlagenes Reconcile gibt
zurück ohne stehende Halbstate.

ERWARTET: nach Timeout/Wiederholung kein stehendes halb-regiertes Signal.
IST: durch Replace-by-ID + Signalregistrierung als letzte Aktion. VERHALTEN KORREKT.

### S3 — zwei schnelle parallele Versuche — verliert einer stille Information?

Single-writer-Protokoll in registry.go:

- **registry.go:707-748** `mutate` — `os.OpenFile(path+".lock", O_RDWR)` +
  `syscall.Flock(fd, LOCK_EX)` (keycloak_driver.go:716-719). Zwei parallele
  `RegisterProviderSignals`/`Remove`/`pruneSignals`/`PruneOwnedProviderInstances`
  blockieren an der Lockdatei; nur einer schreibt, dann der andere. Kein
  verlorenes Schreiben, kein stilles Überschreiben.
- `read` (registry.go:750-764) lädt die Datei, validiert jeden `SignalSource`,
  sortiert stable by `(Kind, ID)`. Deterministisch.
- `RegisterProviderSignals` ersetzt exakte `(ID, Provider)`-Paare
  (registry.go:253) — parallele Versuche verschiedener Projekte (`keycloak:<p1>`,
  `keycloak:<p2>`, `loki:<p3>`) berühren disjointe Schlüssel, kein Kollision.

`RegisterProviderSignals`-Validierung vor dem Schreiben (registry.go:186-205):
`ID` required, `Descriptor.Validate`, nur deklarierte/collectable Signale,
nur realisierte Signale. Ein Versuch mit ungültiger/undeklarierter Signal-ID
schlägt FEHL, bevor geschrieben wird — kein stilles Verlieren.

ERWARTET: parallele Versuche verlieren keine stille Information.
IST: flock-geschützter Single-writer + Replace-by-ID + Validate-before-write.
VERHALTEN KORREKT.

### S4 — Provider ohne Signale: fail-closed oder leer sichtbar?

Registry-ID je Provider (exakte ID als Schlüssel):

- **keycloak_realization.go:135** — `registrationID := "keycloak:" + files.Project`.
- **logs/realization.go:238** — `ID: "loki:" + placement.Project`.

Beide leiten die ID aus `placement.Project` / `files.Project` ab, also aus der
konkreten Projekt-Zuordnung (placement.Project). `PruneOwnedProviderInstances`
registry.go:327 matcht `(Provider, Class, Scope, OwnerApplication)` und behält
nur `keepIDs`.

List — fail-closed ohne gültige Signale / ohne Umgebungsauflösung:

- **registry.go:527-599** `List` — filtert nach `Kind`, `Class`, `Scope`,
  `OwnerApplication`, `SharingBoundary`.
- **registry.go:572** — app-scoped Quelle nur sichtbar bei
  `SourceMatchesEnvironment(source, requestedEnvironment)`.
- **registry.go:622-628** `SourceMatchesEnvironment` — `false`, wenn die Umgebung
  nicht auflösbar ist oder anders aufgelöst wird -> **Quelle wird ausgeschlossen
  (fail-closed)**, keine Umgebungs-Leckage.
- `read` (registry.go:532-534) -> `os.ErrNotExist` zurückgegeben als `nil, nil`
  (leere, gültige Resultate — kein Crash, kein Rauschen).

RegisterProviderSignals — fail-closed ohne deklariertes Signal:
registry.go:200 `"...runtime signal %q is not declared"`, registry.go:203
`"...is not collectable"`, registry.go:221 `"...has no runtime realization`.
Ein Provider ohne deklariertes Signal schlägt im Register FEHL — leer, nicht
falsch sichtbar.

**logs/realization.go:215-246** `registerProviderSignals`: `metricsEnabled`
standardmäßig, aber `signals`-Map wird nur befüllt, wenn `metricsEnabled`
(true). Scope `Application` erzwingt zusätzlich `Collect[...]`. Kein Signal
-> `Enabled: {SignalMetrics: false}`, kein Eintrag im Register -> fail-closed
in List.

ERWARTET: Provider ohne Signale = fail-closed (nicht leer-falsch-sichtbar).
IST: exakte Projekt-ID, `SourceMatchesEnvironment` fail-closed, Validate-before-write.
VERHALTEN KORREKT.

## repo-rule compliance

- Reine Befundung. Kein Produktcode geschrieben, kein Commit, kein PR, kein Merge.
- Kein Subagent verwendet (§4.8). Alle Schritte in der eigenen Session.
- Keine `.github/**`-Änderung, kein Workflow-Rerun, kein `workflow_dispatch`.
- Anchor-Dateien ausschließlich aus read-only exact-develop Clone in /var/tmp gelesen.
- Plan-Datenschreiberei nur im planning-repo; kein Write in
  `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (quarantiniert).
- Kein `git -A`. Nur die eigene Evidence-Datei.
- Keine Secrets/Tokens gefunden (nur Metadaten-Scan, nichts gelesen).

## findings

0 (null) — alle vier Prüfschnitte VERHALTEN KORREKT.

- S1: Wartezeiten konstant + begrenzt (4m Readiness keycloak_driver.go:704, 20s Admin-Auth keycloak_driver.go:349, 5s per-attempt keycloak_driver.go:355). Keine unendlichen Wartezeiten.
- S2: kein stehendes halb-regiertes Signal — `registerKeycloakSignals` ist letzte Aktion von `Apply`, Replace-by-ID (registry.go:253).
- S3: flock-Single-writer (registry.go:716) + Validate-before-write — keine stille Information verloren.
- S4: Provider ohne Signale fail-closed (registry.go:572, registry.go:622); exakte Projekt-ID `keycloak:`/`loki:` + placement.Project.

## EVIDENCE

- Read-source: `/var/tmp/baseharbor-hv16-dev` (Branch `develop`, HEAD `36d075fad77fa61ac8c153e979855546589b32c2`).
- `git ls-remote origin refs/heads/develop` -> `36d075fad77fa61ac8c153e979855546589b32c2`.
- `git ls-remote origin main` -> `c61d7253b6a0985c761e97617cb82b6018802d38`.

## END_DONE

BUG-HUNT H-V16: 0 funde. Alle Prüfschnitte VERHALTEN KORREKT.

cleanliness:
- vorher: keine container/netzwerke/volumes/state-dir-starts; nur read-only Klon in /var/tmp + reads.
- nachher: kein container, kein network, kein volume, kein state-dir; /var/tmp/baseharbor-hv16-dev nur als read-only anchor (kein Write im Produkt); evidence-datei im planning-repo.
- ambient-core bilder fremder karren: unangetastet.
