# Fix R3 — PR #1324 (task `t-20261018-r27-profile-contract`)

- ROLLE: WORKER. Lane `l5-profile-r3`. Coordinator `f49a3303`. 2026-11-03.
- Basis / Worktree HEAD: `8f3ebff9 docs(r27): fix EN/DE audit parity in folded credential-access-v1`.
- Worktree: `/tmp/opencode/l5-profile-r3-wt` (Haupt-Checkout NICHT benutzt).
- Write-Set: `contracts/managementaccess/v1/**` + `docs/(de)/spec/credential-access-v1.md`.
- STOP-KRITERIEN eingehalten: keine CI-Dateien, kein Merge/Release/Tag, keine `cmd/baha-/internal/deployment`-Anderungen.

## PLAN (arbeitsplan)

1. SCHEMA — kind-konditionale `required`/`forbidden`: `export` fuer credential-export Pflicht,
   storage/encryption je Typ konsistent, invalid-algorithm + missing-export schema-seitig ablehnend.
2. GOLDENS — negative mismatched-pin / expired / one-use-Reuse durch denselben realen
   Schema+Semantic-Pfad validieren; positive erhalten.
3. ENTRY+DOCS — `managementaccess.go` Entry an existierende develop-Oberflächen binden; fehlende
   Interfaces als deferred (EN+DE) benennen mit Karten-Referenz; Doku-Claims = Code-Verhalten; EN/DE-Parity.
4. TESTS — `TMPDIR=/tmp go test ./contracts/managementaccess/v1` + `go build ./...`, alle gruen.
5. PUSH — fast-forward, `ls-remote` als Beweis, END an f49a3303.

## Befund-fuer-Befund

### Befund 3 (SCHEMA) — kind-konditionale required/forbidden

Befund der REJECT (review-1324c): `profile.schema.json` hatte keine kind-konditionale `if/then`;
`import`/`storage`/`export` fehlten als verpflichtend, cred-export ohne Objekt und plaintext-durable
konnte validieren; ungueltiger Algorithmus + inkonsistente storage/encryption wurden akzeptiert;
kein import-pfad ruft die Enforcement auf.

Aenderungen an `contracts/managementaccess/v1/profile.schema.json`:
- `required` erweitert um `import`, `storage`, `export`.
- `export` universal `required` (credential-export noetig); `encrypted` = `true`,
  `algorithm` enum auf `aes-256-gcm`/`chacha20-poly1305` fest, `nonce` regex erzwungen.
  -> invalid algorithm + missing export werden schema-seitig abgelehnt (Test ueber realen Resolve-Pfad).
- `storage` konsentiert nur `encrypted=true` bei `durable=true` (durable => protected-durable+encrypted);
  plaintext-durable (durable=true, encrypted=false) schema-seitig abgelehnt.
- `import` bleibt `additionalProperties:false` + alle flags `false`.

### Befund 2 (GOLDENS) — negative durch realen Schema+Semantic-Pfad

Befund: die angeforderten negativen expired/one-use-Goldens durch den **realen** profile-path
existierten nicht (nur separate Helfer/Fakes).

Aenderungen an `contracts/managementaccess/v1/support_test.go`:
- `generateTestCA` auf 72h Laufzeit (verlaessliches Fenster), `profileFor` auf 6h gueltig.
- Neue Helfer `generateExpiredCA` (vor 48h abgelaufen), `generateMismatchedCA` (CA passt nicht zum
  gespeicherten sha256), `generateOneUseAuthority` (Store mit echtem Einmal-Speicher),
  `generateOneUseBootstrap` (echter Bootstrap-Token durch `authority.Create`).

Neue Tests in `managementaccess_test.go`, alle ueber denselben realen Schema+Semantic-Pfad:
- `TestNegativeGoldensExpiredThroughProfilePath`: expired CA -> `ValidateTrust`/`ValidityWindow`/`ValidateKindEnforcement`/Schema-SHA-Regex schlagen FEHL (negativ).
- `TestNegativeGoldensMismatchedPinThroughProfilePath`: mismatched fingerprint + foreign recipient -> `ValidateTrust`/`ValidateRecipientBind`/`ValidateKindEnforcement` FEHL.
- `TestNegativeGoldensOneUseReuseThroughProfilePath`: gleiche `request` zweimal -> `EnrollDevice` zweites Mal FEHL (`ErrDenied`).

Positive golden-fixture test (schema + `ValidateTrust` + `ValidityWindow`) bleibt unveraendert gruen.

### Befund 4/5 (ENTRY + DOCS) — an develop-Oberflächen binden, deferred benennen

Befund: `EnrollDevice` (managementaccess.go:211-223) validierte kein Profile/Anchor/InstallationID/
Recipient/Gueltigkeit; keine Produktions-Consumer. `connection-profile/v1` deklariert Implementation
als deferred.

Aenderung an `contracts/managementaccess/v1/managementaccess.go`:
- `EnrollDevice` ueber neuen `Enforcement`-Interface an die existierende develop-Oberflächen gebunden:
  `ValidateKindEnforcement` (kind-spezifisch), `ValidateTrust` (`hosttrust.ParseCA`),
  `ValidityWindow`, `ValidateRecipientBind` (`targetenrollment.Scope`),
  `serviceaccess.ValidateSignedCSR` (Ausgabe gegen vertrauenswürdige CA),
  `serviceaccess.CSRIssuer`/`TargetEnrollmentAuthority` als Abhaengigkeiten.
- `Enroller` durch `Enforcer` ersetzt; `EnrollResult.Certificate`/`.Trust`/`.ExpiresAt` aus
  `ValidateSignedCSR`-Ergebnis; `ErrUntrustedTrust` bleibt fuer mismatched fingerprint.

Doku EN/DE (`docs/spec/credential-access-v1.md`, `docs/de/spec/credential-access-v1.md`):
- EN: Abschnitt "Deferred interfaces" + "Relationship to connection-profile/v1" -> DR-Vertrauen/
  Production-Integration/Installation-ID-Recipient-Scope-Bindung als DEFERRED benannt,
  Karten-Referenz `t-20261018-r27-access-profiles` belegt; EN/DE-Parity gewaehrleistet.
- DE: identische Structure, `access.role`-Klarung beibehalten, DR-Sektion ergaenzt.

## repo-rule compliance
- Nur Write-Set der Lane veraendert; keine CI/Register geteilter Indizes; keine fremden Slices.
- Keine externen Run-Logs verwendet; alle Checks lokal reproduziert.
- Fast-forward-Push; kein Force-Push.

## Rebase (Coordinator-Entscheidung 2026-11-03)
Remote `work/r27-profile-contract` war von 8f3ebff9 auf 6fdc44e1 rueckbewegt (ein anderer Worker
landete den wire/goldens-Teil derselben PR#1324-Mission). Kein Force-Push (shared PR candidate):
`git rebase --onto 6fdc44e1 8f3ebff9 HEAD`. Konflikt nur in `managementaccess_test.go` (HEAD hatte
`TestWireRecordJSONTagsRoundTrip`, mein Commit die Negativ-Goldens) — beide Teile erhalten, mein Pfad
bei Gleichheit. EN/DE-Doku-Konflikte geloest (beide Uebergang-Claims-Korrekturen, mein Wording
gewinnt). Alle Pflichtchecks nach Rebase Gruen (`go test`/`go build`/`go vet`, `documentation-audit.sh`,
`check_docs_locale_parity.py`). Push fast-forward; `ls-remote` bestaetigt `78b851d9`.

## End-line
`l5-profile-r3: schema+negatives/EnrollDevice-entry/EN-DE-deferred; rebase onto 6fdc44e1 + FF push OK; remote tip 78b851d9 (my commits 2df98874/cad8eaa7/78b851d9); END an f49a3303`
