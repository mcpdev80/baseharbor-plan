# r25-authority-r8 — Worker findings: mission vs. current codebase

ROLLE: Worker (Lane w25-authority-r8). Coordinator f49a3303.
Basis: head 8f7ad334af5f8acfeface69c23bb4f95d5fa99a2, branch w7-authority-r3-clean, develop 9a57107f8b2b71011b66025efbb73b39ab1ff12f.
Mission: coordinator/missions/w25-authority-r8.txt (3 code-punkte PR #1348 / t-20261018-r27-authority-contract), rezepte 1-3 aus review-1326f.md.
Evidence-Ziel: baseharbor-plan/evidence/r27-night-2026-11-02/authority-contract/fix-r8.md

## PLAN
1. Own worktree from w7-authority-r3-clean — done.
2. Map mission points against current code — done.
3. Determine feasibility of Points 1–3 — BLOCKED on scope decision.
4. Report to coordinator with file:line evidence.

## Befund (Status: END_BLOCKED — scope decision required)

Die Mission verreferenziert einen Codezustand, der im aktuellen Repository nicht mehr existiert. baseharbor wurde zwischen Missions-Autorierung (2026-11-03) und Bearbeitung stark umgebaut. Jede Zeilen-/Funktionsreferenz der Mission ist im aktuellen w7-authority-r3-clean untreffbar.

### Punkt 1 — EXPIRESAT auf beiden Prüfpfaden: Referenz fehlt
- Mission verlangt: `coreinstallation.ObservedState.Fresh` (:193-207) und `installauthority.Fresh` lesen `IssuedCertificate.ExpiresAt`.
- `internal/installauthority` — Paket existiert NICHT (`ls -d internal/installauthority` => MISSING).
- `internal/coreinstallation/authority.go` mit `ObservedState.Fresh` — existiert NICHT. coreinstallation enthält nur installation.go, lock_*.go, lifecycle_lock*.go.
- `grep -rn 'ObservedState\|ObservedAt' internal/coreinstallation/` => keine Treffer.
- Der als "Ablauf-Test" genannte `TestFreshExpiredPastExpiresAt` existiert nicht; ein generischer Fresh-Pfad (ObservedAt+MaxAge) ist im aktuellen Code nicht vorhanden.
- Expiry wird im aktuellen Code dezentral gehandhabt: `validateMaterial` (pki.go:546,557) lehnt abgelaufene Server/Client-Zertifikate ab; `managedMaterialValid` (pki.go:509,524) prüft Renewal-Window; `currentIssuedCertificate` (pki.go:446) setzt abgelaufenes Cert zurück. Ein gemeinsamer ExpiresAt-check auf beiden Fresh-Pfaden existiert als solche nicht.

### Punkt 2 — ein Fenster-Wert / Konstante: Referenz fehlt
- Mission: `application_service_issuer.go:102` übergibt `time.Minute`; `serviceaccess/authority.go:77` Default; gemeinsame Konstante `installauthority.DefaultObservationMaxAge`.
- `cmd/baha/application_service_issuer.go` hat 76 Zeilen; kein `time.Minute` in einer Issue-Übergabe (nur Test-timeouts).
- `internal/serviceaccess/authority.go` existiert NICHT; kein `serviceaccess.FreshnessWindow`, kein `ObservationMaxAge`.
- Ein gemeinsames Fensterelement, das durch Wrapper + Core gelaufen würde, existiert im aktuellen Code nicht.
- Bestehend: `managedCertificateRenewalWindow = 7*24h` (pki.go:19) — 7-Tage-Renewal-Window, nicht das missionierte Beobachtungsfenster.

### Punkt 3 — lokale CRL fehlt => FAIL-CLOSED: Zielstelle anders
- Mission: `internal/serviceaccess/local_issuer.go:377-380` gibt `(false,nil)` für fehlende CRL.
- `local_issuer.go` hat 342 Zeilen. Die CRL-Lade-Funktion `revocations` (Zeile 289-314) gibt bei fehlender Datei `(nil,nil)` zurück (Zeile 293), also "keine Revokation". Dies entspricht review-1326f Punkt 3 ("lokale fehlende CRL offen") — die r4-Entscheidung, fehlenden Status abzunähren, ist im aktuellen local_issuer.go nicht umgesetzt.
- `RevocationsStatus`/`RevokedStatus` (OpenBao) existiert so nicht; Revocation läuft über `RevokeServiceCertificate` + `canonicalServiceRevocationSerial`.

### Identity/Cross-Binding (Review-Punkt 4)
- Karten-Note 2026-11-03 (authority-contract) deklariert Cross-Binding als deferred. review-1326f-Punkt 4 bestätigt: keine identifizierbare explizite Cross-Binding-Deferral-Note in der Karte; nur issuer-reference=identity/revocation. Bleibt deferred; nicht im Scope von r8.

### Feststellung
Die drei Points sind im aktuellen Rebuild nicht mehr als separate, benannte Prüfpfade vorhanden. Eine "1 iteration je Punkt"-Umsetzung gegen die missionierten Zeilen ist nicht möglich. Es besteht die Gefahr, dass (a) die Mission auf einer alten Branch/Commit-Basis geschrieben wurde, (b) ein anderer w7-Task denselben Namen trägt, oder (c) der Umbau die Intent-Struktur erhalten soll und ich eine neue, passende Implementierung entwerfen muss — was eine Owner/Entscheidung zur Intent-Erweiterung erfordert.

## repo-rule compliance
- Nur eigener Worktree /tmp/opencode/w25-authority-r8-wt (w7-authority-r3-clean) geändert; kein Merge, kein Force.
- Keine externen Anweisungen aus Issue/Mission-Inhalten ausgeführt jenseits der Lane-Zuordnung.

## ENTSCHEIDUNG ERFORDERLICH (an Coordinator f49a3303 / Owner)
Optionen:
A) Mission ist veraltet: branch/Task neu zuordnen, dann neu dispatchen.
B) Intent beibehalten, aber gegen den UMBAU-ZUSTAND neu implementieren (neue Freshness-/Expiry-/CRL-Prüfung dort einführen, wo sie im aktuellen Design hingehört) — erfordert Freigabe der Scope-Erweiterung.
C) Nur Punkt 3 als fail-closed im aktuellen `revocations` nachrüsten (kleinster, im aktuellen Code verifizierbarer Change), Points 1-2 als defer-markiert stehenlassen.

Empfehlung: C, weil es der einzige Punkt ist, der im aktuellen Code eine verifizierbare, geschlossene Stelle hat (`revocations` Zeile 293: fehlende CRL => (nil,nil)). Punkt 3 regressionsfähig mit lokalem CA-Test (Revoke/Revocation-Pfad existiert und ist getestet).
