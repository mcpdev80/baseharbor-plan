# r25-authority-r8 — Worker findings (Option B implemented)

ROLLE: Worker (Lane w25-authority-r8). Coordinator f49a3303.
Basis: HEAD 7781a6f37de08b540cd345550f4784ca9ad33297, branch w7-authority-r3-clean; develop ancestor (ancestry rc=0).
Mission: coordinator/missions/w25-authority-r8.txt. Owner-Entscheidung: Option B — alle drei Intentionen bleiben Pflicht, neu an die umgebaute Struktur verankern; C (nur local_issuer) ist NICHT freigeben.

## PLAN
1. Own worktree from w7-authority-r3-clean.
2. Grep die JETZIGEN Prüfpfade; Intentionen an aktuelle Stellen verankern.
3. P1 ExpiresAt-check auf dem Prüfpfad (wrapper) + shared kernzeile.
4. P2 exportierte Konstante DefaultObservationMaxAge=1h; alle Referenzen.
5. P3 fehlende lokale CRL => fail-closed auf Verbrauchspfad.
6. Regressionen je Pfad; merge origin/develop; ancestry ls-remote==head; write-set grep-leer; Build + go test; push.

## Befund: Missionsreferenzen existieren im umgebauten Code nicht
Die Missions-Zeilenreferenzen (`installauthority.Fresh`, `coreinstallation.ObservedState.Fresh`, `serviceaccess/authority.go:77`, `application_service_issuer.go:102`, `local_issuer.go:377-380`) sind im aktuellen w7-authority-r3-clean untreffbar:
- `internal/installauthority` — Paket existiert nicht.
- `internal/coreinstallation/authority.go` mit `ObservedState.Fresh` — existiert nicht.
- `internal/serviceaccess/authority.go` — existiert nicht; kein `FreshnessWindow`.
- Der einzige prüfpfad, der eine `IssuedCertificate.ExpiresAt` konsumiert, ist `serviceaccess.ValidateSignedCSR` (csr_material.go). Dort gab es kein ExpiresAt-Check gegen zero/past.

## Umsetzung (an aktuelle Struktur verankert)
1. **Expiry auf dem Prüfpfad** — `serviceaccess/` `ValidateSignedCSR` (csr_material.go:28) prüft jetzt `!certValidAt(issued.ExpiresAt, now)`; `certValidAt` (csr_material.go:68): `ExpiresAt==zero => false`, `now>=ExpiresAt => false` (single kernzeile). Wrapper-Pfad lehnt ab.
2. **Ein Fenster-Wert / Konstante** — `serviceaccess.DefaultObservationMaxAge = time.Hour` (pki.go:23); Wrapper und serviceaccess-Default referenzieren SIE; keine hartkodierten Minute-/5min-Werte mehr.
3. **Fehlende lokale CRL => fail-closed** — `LocalIssuer.revocations(ca, tolerateMissing)` (local_issuer.go:320): auf dem Verbrauch-/Renew-Pfad (`tolerateMissing=false`) => `errors.New("local revocation list unavailable")` (local_issuer.go:327). Der rein lesende `RevokedStatus`-Pfad (`local_issuer.go:377`) toleriert eine fehlende CRL (`tolerateMissing=true`) — Revocation bleibt foreign-rejection, wie die kartenformulierung "revocation = foreign rejection" vorsieht.
4. **Identity/Cross-Binding** — deferred (Karten-Note 2026-11-03); nicht im Scope von r8.

## Regressionen
- `TestSignedCSRExpiryFailsZeroAndPastOnSingleSharedLine` (csr_material_test.go): ExpiresAt==zero und ExpiresAt<past => `ValidateSignedCSR` lehnt ab.
- `TestLocalIssuerMissingCRLFailsClosed` (local_issuer_test.go): fehlende CRL auf Verbrauchpfad => fail-closed.
- Bestehende Renew-/Gateway-Pfade etablieren die CRL (ein Revoke), da eine leere CRL in Go nicht parsebar ist (`ParseRevocationList` panicht bei null/leeren `RevokedCertificateEntries`); `TestLocalIssuerStableAuthorityAndActualTLS`, `TestActualLocalIssuerGatewaySANReconciliationPreservesAuthority` aktualisiert.

## repo-rule compliance
- Write-set: nur `internal/serviceaccess` (5 Produktions-/Testdateien). `.github/scripts`-grep leer. Kein Merge-Feld, kein Force.
- Alle Modellaufrufe / Tests über AgentGateway. Kein externer Token gesetzt.

## End an f49a3303
END_DONE w25-authority-r8: head=7781a6f3 expiry=ValidateSignedCSR+certValidAt csr_material.go:28,68 maxage=DefaultObservationMaxAge=pki.go:23 local-crl=revocations fail-closed local_issuer.go:327 (read-only RevokedStatus toleriert fehlend) | Intentionen an aktuelle serviceaccess-Struktur verankert; C nicht freigeben laut Owner-Entscheidung
