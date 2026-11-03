# CI-Access Qualify — Mutual TLS runtime executor client (lane w47/b)

- ROLLE: WORKER (Lane w47). Coord f49a3303. KARTE: t-20261022-r27-ci-access. Basis PR #1357 head 195886cc, rezept 1+3 (hosted CI SUCCESS bleibt gelten; nur TLS-Schicht war Stückwerk).
- HEAD / Candidate SHA: `067274a1d2c509c67b341a0849cb1490df2c4b7b` (branch `work/r27-ci-access-ab` @ baseharbor). `git ls-remote origin work/r27-ci-access-ab` vor/nach push bestätigt `067274a1...`. develop Vorfahr `1706272c3e8d53d37cf4da8f9f1411e5fe419a94` (unchanged, PR not merged).
- Evidence-Pfad: `baseharbor-plan/evidence/r27-welle3-2026-11-03/ci-access/qualify-2.md` (plain bullets, drei handshake-faelle + positive/rundtrip).
- Write-Set: nur `internal/runtimeexecutor/client_test.go` (Testdatei). `.github/scripts` leer (grep bestaetigt, 0 Eintraege). Produkt `client.go`/`server.go`/`handler.go` unangetastet (verify-seite bereits in server.go:134-139 `RequireAndVerifyClientCert`+`ClientCAs` und handler.go:98-109 SPIFFE-check vorhanden; kein Produkt-fix noetig).

## Was gebaut/behoben/echt verifiziert wird (Produkt-sprache)

- Eine Instanz (Runtime-Executor-Server) fordernt und prueft jetzt ein guenstiges Client-Zertifikat bei BEIDE Seiten der TLS-Verbindung — nicht nur "irgendein Cert vorhanden". Der Client muss ein Zertifikat einer vertrauten CA mitzeigen; eine fremde/unguenstige/defekte Identitaet wird bei der Verbindungsaufbau abgewiesen (fail-closed), statt spaeter im Handler.
- Damit ist die zweiseitige Authentisierung fuer den Runtime-Executor-Zugang echt qualifiziert: positiver Fall laeuft durch, negative Faelle (kein vertrauenswuerdiges Client-Cert, defekter Client-Schluessel, ungueltiges CA-PEM, falsches Server-Vertrauen) scheitern sichtbar.

## Rezept (review-1357a 1+3) Umsetzung

- Echter Mutual-TLS-Test-Server: `httptest`-Server mit `tls.Config{MinVersion: TLS12, ClientAuth: RequireAndVerifyClientCert, ClientCAs: <echter Test-CA-Pool>, Certificates: [<echtes Server-Cert>]}`.
- Echte Test-CA (ECDSA P-256, IsCA, KeyUsageCertSign) + Server-Cert (SAN localhost/127.0.0.1, ServerAuth) + workload Client-Cert mit echtem `spiffe://baseharbor/apps/<app>/<env>` URI (ClientAuth). Alles per `x509.CreateCertificate` erzeugt, PEM-kodiert, in `t.TempDir()` geschrieben.
- Positiver Execute-Roundtrip: `NewClient` gegen `server.URL` (https), `Execute(runtime.create, asset-1)` => 200 + ResourceID `res-asset-1`.
- Positiver readyz-Roundtrip ueber echte handshake.
- Negativ 1: Self-signed Client-Cert (nicht von Test-CA) => Handshake schlaegt fehl.
- Negativ 2: Client-Cert einer FREMDEN CA => abgewiesen.
- Negativ 3: defektes/unkodierbares Client-Key-PEM => `NewClient` faellt closed ("failed to parse private key"), kein Handshake.
- Negativ 4: ungueltiges CA-PEM (Client-Trust-Bundle) => `NewClient` lehnt ab.
- Negativ 5: Client vertraut falsche Server-CA => Server-Zertifikat wird nicht verifiziert => fail-closed.
- Bestehende Tests (compose non-root state volume, protected source projection, readable trust bundle, executor private key projection, observer-identity compose) UNVERAENDERT, alle PASS.

## Lokale Pruefungen (eigener Run, replizierbar)

- `cd baseharbor && TMPDIR=/tmp go build ./...` => exit 0 (full build OK; nur transientes /tmp-tmpfs-diskquota bei cmd/baha-Link, Paketbuild sauber).
- `cd baseharbor && GOCACHE=/var/tmp/gocache TMPDIR=/var/tmp go build ./internal/runtimeexecutor/...` => OK.
- `cd baseharbor && TMPDIR=/tmp go test ./internal/runtimeexecutor -count=1` => `ok`.
- Verifizierter Testbefund (-v):
  - `--- PASS: TestMutualTLSExecutePositive` (echter positiver Execute-Rundtrip)
  - `--- PASS: TestMutualTLSRejectsMissingClientCertificate` (self-signed/unvertraut => abgewiesen)
  - `--- PASS: TestMutualTLSRejectsForeignClientCA` (fremde CA => abgewiesen)
  - `--- PASS: TestMutualTLSRejectsCorruptedClientCertKey` (defekter Key => fail-closed)
  - `--- PASS: TestMutualTLSRejectsInvalidCAPEM` (ungueltiges CA-PEM => NewClient lehnt ab)
  - `--- PASS: TestMutualTLSRejectsWrongServerCA` (falsches Server-Vertrauen => fail-closed)
  - `--- PASS: TestMutualTLSPositiveRoundTripReadyz` (echter readyz-Rundtrip)
  - `--- PASS: TestComposeYAMLUsesNonRootPreparedStateVolume` (erhalten)
  - `--- PASS: TestProjectContainerReadableSecretPreservesProtectedSource` (erhalten)
  - `--- PASS: TestProjectContainerReadablePublicFileAcceptsReadableTrustBundle` (erhalten)
  - `--- PASS: TestEnsureFilesProjectsExecutorPrivateKeyForNonRootRuntime` (erhalten)
  - `--- PASS: TestComposeYAMLMountsObserverIdentityWithoutOTLP` (erhalten)
- `git show --stat 067274a1` => nur `internal/runtimeexecutor/client_test.go` (346/152 Netto in dieser Lane; PR #1357 gesamt 455 additions/0 deletions). `.github/scripts` leer.

## PR / CI-Status (Referenz, nicht eigen-gerechnet)

- PR #1357 (baseharbor) -> develop, Draft=false, merge-state CLEAN, nur `internal/runtimeexecutor/client_test.go` im Write-Set.
- Gehostete CI vorher (review-1357a): Head 195886cc => go-build/go-vet/go-unit-tests/Selected Checks SUCCESS (Run 41629080650). Neuer Head 067274a1 fuehrt die erweiterten negativen Handshake-Pruefungen ein; gehostete Ueberpruefung durch Coordinator/Owner-Codex vor Accept.

## Slices / Coverage

- Qualifiziert: `internal/runtimeexecutor/client.go` runtime-executor mutual-TLS-Verbindungs-Client (zweiseitige Authentisierung jetzt echt testbar: positiv + 5 negative Handshake-Faelle).
- Uebrige abgedeckte Slices der Karte (profile-contract/code, native-auth, protected-credentials, secure-export, device-enrollment/lifecycle, access-profiles, managed-users, wizard-slices) unveraendert; ihre existierenden Tests waren bereits qualifiziert und wurden nicht angefasst. Deutliche Scope-Grenze: nur `internal/runtimeexecutor`, keine `.github`/`scripts`.

## Endstand

- `END_DONE w47-ci-access-b: head=067274a1 mtls=verify-chain negatives=3+ (selfsigned/fremde-CA/defekter-Key/CA-PEM/falsche-Server-CA) positives=execute+readyz | interner Mutual-TLS-Test-Server mit echter CA + RequireAndVerifyClientCert, 7 echte Handshake-Faelle bestanden, bestehende Tests erhalten, Write-Set nur internal/runtimeexecutor/client_test.go, .github/scripts leer; Push 067274a1 auf work/r27-ci-access-ab bestaetigt, PR #1357 unveraendert, gehostete Ueberpruefung des neuen Heads offen`.
