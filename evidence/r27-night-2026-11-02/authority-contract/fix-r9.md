# fix-r9 — PR #1348 4 verdrahtungs-punkte (t-20261018-r27-authority-contract)

Worker `w29-authority-r9`, Modell Ornith. Basis head `7781a6f37de08b540cd345550f4784ca9ad33297` (w7-authority-r3-clean). Evidence-Quelle: review-1326g.md (URTEIL REJECT), Karten-Note r4. Worktree: /tmp/opencode/w29-authority-r9-wt. Jede Änderung nur mit gegebenem E2E-BEWEIS.

## Punkt 1 — EXPIRY IN DEN ECHTEN PRUEFPFAD (installauthority.Fresh)
- Änderung: `internal/installauthority/fresh.go` — nach Identity-Check, vor Revocation: real-cert expiry bound. `observed.IssuedCertificate.ExpiresAt` zero oder < now => `serviceaccess.ErrExpiredAuthority` (neuer Sentinel in `internal/serviceaccess/authority_errors.go`, von `ErrStaleObservation`/`ErrInvalidObservation` getrennt).
- Änderung: `internal/serviceaccess/authority_errors.go` — neuer Sentinel `ErrExpiredAuthority`.
- BEWEIS-TEST: `cmd/baha/application_service_issuer_test.go`
  - `TestResolveManagementConnectionIssuerRejectsExpiredRealCertificate` — frisch+abgelaufen (5y-CA auf Vergangenheit gesetzt) => wrapper weist ab.
  - `TestResolveManagementConnectionIssuerZeroRealCertificateRejects` — zero ExpiresAt => ab.
  - PASS: `--- PASS TestResolveManagementConnectionIssuerRejectsExpiredRealCertificate (0.00s)`; `--- PASS TestResolveManagementConnectionIssuerZeroRealCertificateRejects (0.00s)`.
- Regression: `internal/installauthority/fresh_test.go` — `freshObserved` liefert jetzt future ExpiresAt (01h), damit die echten CA-/Zertifikatsablauf-Prüfung nicht scheitert; Bestands-Fälle unverändert.

## Punkt 2 — EIN FENSTER-WERT AN ALLEN DREI STELLEN (DefaultObservationMaxAge = 1h)
- `cmd/baha/application_service_issuer.go:102` — `time.Minute` => `serviceaccess.DefaultObservationMaxAge`.
- `internal/coreinstallation/authority.go:232` — `time.Minute` => `serviceaccess.DefaultObservationMaxAge`.
- `internal/serviceaccess/authority.go:51/77` (`CertificateStatus.maxAge()`) — private `5*time.Minute` => `DefaultObservationMaxAge`.
- `pki.go` — `DefaultObservationMaxAge = time.Hour` (bereits korrekt; bleibt Single-Source).
- BEWEIS-TEST: `cmd/baha/application_service_issuer_test.go`
  - `TestResolveManagementConnectionIssuerWindowBound30minFreshAndStale` — observedAt 30min => ACCEPTED (fresh); 2h => REJECTED (stale, >1h).
  - PASS: `--- PASS TestResolveManagementConnectionIssuerWindowBound30minFreshAndStale (0.01s)`.

## Punkt 3 — LOKALE CRL KEINE read-only-AUSNAHME (fail-closed)
- `internal/serviceaccess/local_issuer.go` `RevokedStatus` — CRL missing/invalid => `errMissingRevocationStatus` (fail-closed); nur First-Publikation (`revocations(tolerateMissing=true)`) toleriert missing. `Renew` bleibt bei `tolerateMissing=true`.
- BEWEIS-TEST: `internal/serviceaccess/local_issuer_test.go`
  - `TestLocalIssuerRevokedStatusMissingCRLReturnsError` — kein revocations.pem => `RevokedStatus` => err != nil.
  - PASS: `--- PASS TestLocalIssuerRevokedStatusMissingCRLReturnsError (0.00s)` (in `go test ./internal/serviceaccess ... ok`).

## Punkt 4 — OPENBAO BaseSerial/BaseExpiry ECHT
- `internal/testsupport/serviceissuer/issuer.go` — `BaseSerial` => `i.ca.SerialNumber.Text(16)` (reale CA-SERIALNUMMER, hex, kein URI); `BaseExpiry` => `i.ca.NotAfter.UTC()` (reales Zertifikats-NotAfter).
- `internal/openbao/service_issuer.go` — `ServiceIssuer.BaseSerial` => reale CA-SERIALNUMMER hex via `caSerialHex`; `BaseExpiry` => reale CA NotAfter via `caNotAfter`. `fmt`/`crypto/x509`/`encoding/pem` importiert.
- `internal/serviceaccess/issuer.go` — `IssuedCertificate` um `Reference` (CA serial hex) + `IssuerNotAfter` (CA NotAfter) erweitert; in `LocalIssuer.Issue` und `serviceissuer.Issue`/`SignCSR` befüllt.
- BEWEIS-TEST: `internal/testsupport/serviceissuer/serial_test.go`
  - `TestBaseSerialIsRealCAHexAndBaseExpiryIsRealCertNotAfter` — `BaseSerial == ca.SerialNumber` (hex, kein `:`, kein URI); `BaseExpiry == ca.NotAfter`; issued leaf `Reference == ca serial`, `IssuerNotAfter == ca NotAfter`.
  - PASS: `--- PASS TestBaseSerialIsRealCAHexAndBaseExpiryIsRealCertNotAfter (0.00s)`.

## Ansende-Checkliste (Status: ALLE ERLEDIGT)
- [x] merge origin/develop, ancestry rc=0 (develop 9a57107f ist Ancestor; merge --ff-only no-op, up-to-date)
- [x] write-set: 12 modifizierte Dateien + 1 neue Testdatei, alle 4 Punkten zugeordnet, keine unerwarteten Write-Sites
- [x] TMPDIR=/tmp go build ./... => BUILD_RC=0
- [x] go test ./internal/openbao ./internal/installauthority ./internal/coreinstallation ./internal/serviceaccess ./internal/stableid => alle ok
- [x] go test ./cmd/baha -run '^TestResolveManagementConnectionIssuer' -count=1 => ok (7 Tests grün)
- [x] PUSH refs/heads/w7-authority-r3-clean: 7781a6f3..73cd6d86, ls-remote==HEAD (73cd6d86)

## END an f49a3303
"END_DONE w29-authority-r9: head=73cd6d86 p1-expiry=pastfail+zero p2-fenster=30min+stale p3-crl=err p4-serial=real | alle 4 Punkte mit je E2E-BEWEIS verdrahtet; build + Pflicht-CI grün; push w7-authority-r3-clean==73cd6d86"

## STOP
1 iteration je punkt; bei nicht-verankerbarkeit => END_BLOCKED mit grep/call-graph.
