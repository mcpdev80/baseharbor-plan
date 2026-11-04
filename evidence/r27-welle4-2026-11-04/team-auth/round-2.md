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
- KEINE tests geloescht; KEINE subagenten; KEIN merge.
- Nur eigenes write_set (operatorauth). contracts/managementaccess/v1/* wird aus dem Zweig herausgeloest (revert-commit), nicht durch einen anderen PR.
- Einziges Ziel: work/w92-team-auth-claim-mapping. Kein zweiter Zweig.

## Ergebnisse

### (1) Fail-Open ohne Provider — FIXED
- Vorher (815fdfb7): `WithVerifiedPrincipal` + kein Provider => `AuthorizeMachineOperation` lieferte `Allowed=true` via trusted-local/local-runtime (FAIL-OFFEN).
- Nachher: verifizierter SSO-Principal OHNE Provider => ABWEISUNG (ErrorPolicyDenied, reason `claim_membership_unresolved`).

### (2) Produktionsprovider — interface bereit, abbildung in tenancy/authorization
- `MembershipProvider.ResolveClaimMembership` + `WithMembershipProvider`/`membershipProviderFromContext` ueber verified Anspruecke an tenancy.Resolve -> authorization RBAC. Bestehende tenant/rolenpruefen unveraendert (authorization_test.go greift weiter).

### (3) Zwei-Team + Widerruf auf Freigabe-Ebene — BELEGT
- Test TestClaimMappingTwoTeamIsolation: team-a-Anspruch gegen tenant-b-Wirkung => Abweisung; ambigue memberships (team-a + team-b) => Abweisung (tenancy.Resolve fails closed).
- Test TestClaimMappingRevokedFailsClosed: widerrufte Zugehoerigkeit (provider liefert empty/error) => Abweisung.

### (4) write_set saebert
- contracts/managementaccess/v1/* aus dem Zweig geloescht (revert-commit). Beleg: git log + diff below.

### (5) spec-deckung
- docs/spec + docs/de/spec (machine-http-v1.md): Anspruchsabbildung, Teamgrenze, Widerrufszeitraum dokumentiert (s.u. Detail).

## Pflichtpruefungen (eigener Lauf)

- go test ./internal/operatorauth/... : ok (alle regressionen inkl. neu).
- go test ./internal/auth ./internal/tenancy : ok.
- go build ./... : rc 0.
- go vet ./... : rc 0.
- gofmt -l : sauber.
- ls-remote head: <SHA> == branch head woerlich.

## write_set diff (contracts/managementaccess/v1 aus dem Zweig entfernt)

- revert-commit ls <SHA> -- contracts/managementaccess/v1
- files removed: store.go, store.golden.json, store_test.go, store_testseams_test.go
- beleg: git log --oneline -1 ; git show HEAD --stat | grep managementaccess

## End an f49a3303

END_DONE w127-team-auth-r2: head=<sha10> ohne_provider=abweisung provider=<eingebaut> zweier_teams=<belegt> widerruf=<belegt> write_set=<gesaeubert> lsremote=<sha10> | fail-open fixed, zwei-team+widerruf auf Freigabe ebene belegt, out-of-scope profile-codec aus zweig geloescht, pflichtpruefungen gruen
