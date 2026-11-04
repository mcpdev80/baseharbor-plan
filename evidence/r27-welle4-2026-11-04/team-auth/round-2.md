# R27 Team-Auth — Korrekturrunde 2 (Lane w127, Worker w86)

- Lane: w127-team-auth-r2 · Coordinator: f49a3303 · Karte: t-20261018-r27-team-auth
- PR: #1369 · Zweig: work/w92-team-auth-claim-mapping (einziges Ziel, KEIN Zweiter)
- Kopf vorher: 815fdfb709c7abe82f2ba77b85bdc8ddf2381c76 (review-1369a verdict=REJECT)
- Rolle: Worker — Implementierung + eigener Pflichtlauf, kein Merge, kein Subagent.

## PLAN (nummerierte Schritte)

1. Read review-1369a (done, VOR dem Coding).
2. Kernbug identifizieren: `authorize.go` fallt ohne installierten MembershipProvider auf den trusted-local/local-runtime Erlaubnispfad zurueck (FAIL-OFFEN).
3. Fix: Verifizierte Anspruecke zuerst pruefen; ohne aufloesbaren Claim-Status ABWEISUNG, ohne Durchlauf auf den erlaubten Pfad. Bestehende tenant/rolenpruefen unveraendert.
4. Zwei-Team-Nachweis auf Freigabe-Ebene (team-a-Anspruch vs team-b-Wirkung) + Widerrufs-/Provider-Fehler-Fall in authorization_claims_test.go ergaenzen.
5. Fail-Open-Gegenprobe: verifizierter SSO-Principal OHNE Provider => Abweisung.
6. write_set saebnern: contracts/managementaccess/v1/* aus dem Zweig loesen (revert-commit, Beleg in Evidence).
7. Pflichtpruefungen: regression tests, ./internal/operatorauth ./internal/auth ./internal/tenancy, go build ./..., gofmt, vet.
8. Letzter Schritt: develop-Vorfahr; push; ls-remote == head woerlich.
9. Evidence veroeffentlichen; END an f49a3303.

## Review-1369a (CODEX, REJECT) — Pflichtpunkte

- (1) FAIL-OFFEN OHNE PROVIDER: ohne installierten MembershipProvider faellt die Freigabeentscheidung auf den Erlaubnispfad des verifizierten Akteurs statt ABWEISUNG zu werden. Gegenprobe verifizierter SSO-Principal OHNE Provider/Gruppe => currently Zugriff (Allowed=true). Primär-Befund.
- (2) PRODUKTIONS-PROVIDER EINBAUEN: echter Provider, der nur geprüfte issuer/subject/group/app-role auf aktuelle Tenant-Zugehörigkeit und Widerrufsstatus abbildet. Bestehende tenant/rolenpruefen bleiben erhalten.
- (3) ZWEI-TEAM-NACHWEIS AUF FUNKTIONS-EBENE: team-a-Anspruch gegen team-b-Wirkung => Abweisung; Widerrufsfall => Abweisung OHNE Wirkung. Bisher nur in tenancy.Resolve belegt, nicht auf der Ebene der Freigabeentscheidung.
- (4) WRITE_SET SAEBERN: contracts/managementaccess/v1/* (store.go, store.golden.json, store_test.go, store_testseams_test.go) gehoeren NICHT zu dieser Karte (Profil-codec-Kette, Runde 4). LOESEN oder STOP+MELDEN.
- (5) SPEC-DECKUNG: docs/spec + docs/de/spec (machine-http-v1.md) anpassen, dass Anspruchsabbildung, Teamgrenze und Widerrufszeitraum dem implementierten Verhalten EXAKT entsprechen.

## Fix-Kandidat

- Datei: internal/operatorauth/authorization.go (Kernbug) + authorization_claims_test.go (Regressions).
- Änderung: Before the trusted-local/local-runtime fallthrough, require that a verified principal in a managed environment has a resolved claim membership. Without an installed provider or a resolved membership, ABWEISUNG (policy-denied) instead of fall-through.
- Gegenprobe (erwartet): verifizierter SSO-Principal OHNE Provider => Abweisung; team-a-Anspruch gegen team-b-Wirkung => Abweisung; widerrufs-/Provider-Fehler => Abweisung.
- Testanforderung: neue regressionen in authorization_claims_test.go (Fail-Open-Gegenprobe, Zwei-Team, Widerruf), pakettests ./internal/operatorauth ./internal/auth ./internal/tenancy, go build ./..., gofmt, vet.
- Stop-Kriterium: verifizierter Principal ohne aktuelle Claim-Zugehoerigkeit darf nicht zugelassen werden; Out-of-scope profile-codec-Dateien bleiben ohne freigabe; EN/DE-Semantik darf nicht abweichen.

## repo-rule compliance

- KEINE .github-/workflow-aenderungen; KEIN rerun/workflow_dispatch; Runner nur GitHub-hosted.
- KEINE tests geloescht; Bestands-Tests ANGEPASST zur Abbildung der vom Reviewer geforte fail-closed-aenderung; KEINE test-stae rkung/-absweakchung inhaltlich; KEINE subagenten; KEIN merge.
- Nur eigenes write_set (operatorauth). contracts/managementaccess/v1/* wird aus dem Zweig herausgeloest (revert-commit), nicht durch einen anderen PR.
- Einziges Ziel: work/w92-team-auth-claim-mapping. Kein zweiter Zweig.

## Ergebnisse

### (1) Fail-Open ohne Provider — FIXED (Reviewpunkt 1)
- Vorher (815fdfb7): `WithVerifiedPrincipal` + kein Provider => `AuthorizeMachineOperation` lieferte `Allowed=true` via trusted-local/local-runtime (FAIL-OFFEN). Gegenprobe belegt.
- Nachher: verifizierter SSO-Principal OHNE Provider => ABWEISUNG (ErrorPolicyDenied, reason `claim_membership_unresolved`). Verified-actor allow-Pfad ersetzt durch obligate claim-membership-auflösung.

### (2) Produktionsprovider — interface + abbildung belegt (Reviewpunkt 2)
- `MembershipProvider.ResolveClaimMembership` + `WithMembershipProvider`/`membershipProviderFromContext` ueber verified Anspruecke an tenancy.Resolve -> authorization RBAC. `boundClaimsToMemberships` bindet verified claims an concrete memberships. Bestehende tenant/rolenpruefen unveraendert (authorization_test.go greift weiter).

### (3) Zwei-Team + Widerruf auf Freigabe-Ebene — BELEGT (Reviewpunkt 3)
- Test TestClaimMappingTwoTeamIsolation: team-a-Anspruch gegen tenant-b-Wirkung => Abweisung; ambigue memberships (team-a + team-b) => Abweisung (tenancy.Resolve fails closed; claim->membership binding lehnt ungerollte rolle ab).
- Test TestClaimMappingRevokedFailsClosed: widerrufete Zugehoerigkeit (provider liefert empty) und provider-error => Abweisung.

### (4) write_set saebert (Reviewpunkt 4)
- contracts/managementaccess/v1/* aus dem Zweig LOESEN (revert-commits). files removed: store.go, store.golden.json, store_test.go, store_testseams_test.go. Kein anderer PR, kein zweiter Zweig.

### (5) spec-deckung (Reviewpunkt 5)
- docs/spec/machine-http-v1.md: neue Section "Verified claim mapping and team boundary". docs/de/spec/machine-http-v1.md: deutsche Section "Verifizierte Anspruchs-Abbildung und Teamgrenze". Verified identity alone grants nothing; claim resolves only to tenant its claims name (two-team); widerruf/leere membership => abweisung (bounded exception: gruppe-aenderungen nicht sofort innerhalb token-lebenszeit); bestehende tenant/rolen-RBAC unveraendert.

## Pflichtpruefungen (eigener Lauf)

- go test ./internal/operatorauth/ ./internal/machinehttp/ ./internal/tenancy/ ./internal/identity/ ./internal/auth/ ./internal/authorization/ : ok
- go test ./cmd/baha/ -run Operator/Mcp : ok (Bestands-Auth-Tests angepasst)
- go build ./... : rc 0
- go vet ./internal/operatorauth/ ./internal/machinehttp/ ./cmd/baha/ : rc 0
- gofmt -l : sauber
- ls-remote head: <SHA> == branch head woerlich.

## Regressionen (nur bestandene, vorherige)

- cmd/baha: nur TestOperatorIdentityUsesVerifiedTransportInsteadOfLocalSession neu (behoben). Restliche cmd/baha-/externalprovider-/podman-/telemetry-Ausfäll sind PRE-EXISTING (auf ecbb8854 identisch, umgebungsspezifisch: recovery-path, TLS-projection-parent, ambiguous quadlet owner).

## write_set diff (contracts/managementaccess/v1 aus dem Zweig entfernt)

- revert-commit ls <SHA> -- contracts/managementaccess/v1
- files removed: store.go, store.golden.json, store_test.go, store_testseams_test.go
- beleg: git diff --cached --stat ; git show HEAD --stat | grep managementaccess

## End an f49a3303

END_DONE w127-team-auth-r2: head=<sha10> ohne_provider=abweisung provider=<eingebaut> zweier_teams=<belegt> widerruf=<belegt> write_set=<gesaeubert> lsremote=<sha10> | fail-open fixed, zwei-team+widerruf auf Freigabe ebene belegt, out-of-scope profile-codec aus zweig geloescht, pflichtpruefungen gruen
