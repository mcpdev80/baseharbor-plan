# Team-auth Runde 3 — Implementierung und Nachweis

- Task: `t-20261018-r27-team-auth`
- Owner/Lane: `coord-welle4 (Codex-Worker cx08)`
- PR: #1369, branch `work/w92-team-auth-claim-mapping`
- Basis-Kopf zu Beginn: `f9507ff6ee00694b0125c577a4890918695b3fa8`
- Develop: `2ea2c6f1d344cca2b21c17e7acbebf711b1511a1`

## PLAN-Checkliste

1. Den Run-41884936792-Fehler und exakten vorhandenen Produkt-/Teststand SHA-genau festhalten.
2. Die bestehende IdentityTenantResolver-Datenquelle als aktuellen Membership-Pfad für Ansprüche anbinden; keine zweite Datenquelle oder permissive Ersatzauflösung schaffen.
3. Die Produktionskomposition in `cmd/baha` mit diesem Provider verbinden, ohne bereits bereitgestellte Test-/Aufruferprovider zu überschreiben.
4. Den bestehenden First-run-Test mit verifiziertem Principal und passender Zuordnung grün machen; den Test ohne Provider ausdrücklich rot/fail-closed und ohne Zustandsmutation belegen.
5. Aktuelle Zuordnung, Zwei-Team-Trennung und Widerruf mit leerer Membership erneut belegen; Widerruf muss vor State-/Netzwerknebenwirkung ablehnen.
6. Betroffene Pakettests, Build/Vet/Format ausführen; die betroffenen Hosted Checks für den neuen SHA auslösen und bis terminal beobachten.
7. Diff-Scope, Develop-Ancestry, `ls-remote`, Run-IDs und Resultate in dieser Datei aktualisieren; normal pushen, kein Merge.

## RED-FIRST — vorhandener Fehler vor Änderung

Run `41884936792`, head `f9507ff6ee00694b0125c577a4890918695b3fa8`, Check `PR · Validation · go-unit-tests`, Job `126766941366`:

```text
--- FAIL: TestRepositoryRuntimeInitRecordsPendingDeploymentBeforeStateMutation (0.00s)
    app_input_resolver_first_run_test.go:56: initialize repository deployment inputs: The verified operator carried no claim-based tenant membership that permits this machine operation.
```

Der gleiche Test und Fehler steht in `PR · Validation · cli-package-tests`, Job `126766941411`. Der lokale Kontrollvergleich aus `triage-1.md` bestand auf Develop `2ea2c6f1` und scheiterte auf diesem Kopf.

## Umsetzung und Ergebnisse

### Kandidat und Produktionsverdrahtung

- Neuer Commit: `a7fa573d5bff6e043fbecbb2aeb79833605dc304` (normaler Push, kein Force-Push); `git ls-remote origin refs/heads/work/w92-team-auth-claim-mapping` gab denselben SHA aus.
- `git merge-base --is-ancestor 2ea2c6f1d344cca2b21c17e7acbebf711b1511a1 HEAD` bestand (Exit 0).
- Einsetzstelle: `cmd/baha/main.go:125-127` installiert den DB-gestützten Provider vor den CLI-Operationen; `WithMembershipProviderIfAbsent` erhält bereits übergebene Provider (`internal/operatorauth/context.go:70-78`). Der Provider in `cmd/baha/operator_membership_provider.go:17-54` verwendet dieselbe `BASEHARBOR_API_DATABASE_URL` wie der API-Server und delegiert an den produktiven Resolver.
- Aktuelle Anspruchsbindung und Widerruf: `internal/database/identity_tenant_resolver.go:95-168` verlangt verifizierten Issuer+Subject, bindet Gruppen-/Anwendungsrollen-Ansprüche an aktuelle Datenbankmitgliedschaften und liest diese pro Entscheidung in einer read-only, identity-scoped Transaktion erneut.

### Verhaltensnachweise

- Bestehender `TestRepositoryRuntimeInitRecordsPendingDeploymentBeforeStateMutation` bleibt mit verifiziertem `editor`-Principal und der expliziten passenden Zuordnung vollständig erhalten; er prüft weiter Deployment-Record, `configured`-Status, lokale Eingabedatei und anschließendes Resolve.
- Neuer Gegenfall im selben First-run-Pfad: kein Provider und widerrufene/geleerte Zuordnung werden als `ErrorPolicyDenied` abgewiesen; Deployment-Record, `deployment.json` und Eingabedatei dürfen nicht entstehen. Der Widerrufsfall prüft zuerst die Autorisierung mit aktiver Zuordnung.
- `internal/database/identity_tenant_resolver_integration_test.go` prüft den echten DB-Resolver bei Maschinenautorisierung: passende aktuelle Gruppenmitgliedschaft wird erlaubt, dieselbe beanspruchte Rolle über zwei Teams wird verweigert, und nach Löschen der Mitgliedschaft wird die nächste Autorisierung verweigert.

### Lokale Prüfungen

- `gofmt` auf allen sieben geänderten Go-Dateien: sauber.
- `git diff --check`: sauber.
- Gehostete DB-Testvorrichtung `postgres:18-alpine`, `127.0.0.1:55435`, nur für die gezielten Tests gestartet und danach entfernt.
- `go test -p 2 -vet=off ./cmd/baha -run '^(TestRepositoryRuntimeInitRecordsPendingDeploymentBeforeStateMutation|TestRepositoryRuntimeInitRequiresCurrentClaimMembershipBeforeStateMutation)$' -count=1`: PASS.
- `go test -p 2 -vet=off ./internal/operatorauth -count=1`: PASS.
- `go test -p 2 -vet=off ./internal/database -run '^TestIdentityTenantResolverUsesIdentityScopedRLS$' -count=1`: PASS.
- Gesamter `cmd/baha`-Paketlauf ist durch den Hosted-Check `cli-package-tests` verpflichtend; dieser Bericht wird nach Abschluss mit dem terminalen Resultat ergänzt.

### Hosted CI — Laufbeobachtung

- Neuer, vom Push ausgelöster PR-Lauf: [41893767441](https://github.com/mcpdev80/baseharbor/actions/runs/41893767441), Head `a7fa573d5bff6e043fbecbb2aeb79833605dc304`; Event `pull_request`.
- Beobachtung mit `gh run watch 41893767441 --exit-status` läuft. `PR · Trusted Plan` (Job `126797695596`), `Workflow policy` (`126797695926`), `PR · Source format` (`126797696068`), `documentation-audit` (`126797846141`), `cli-gofmt` (`126797846242`), `pages-candidate-build` (`126797846274`) und `mkdocs-de-strict` (`126797846436`) sind bereits PASS. `cli-package-tests`, `go-unit-tests`, `cli-build`, `cli-vet`, `go-build`, `go-vet`, `source-contracts`, `Focused Python`, `mkdocs-en-strict`, `pages-candidate-build`-abhängige Gates sowie `Workflow policy` sind/waren bei Zwischenabfrage noch nicht alle terminal.
- Im vorherigen Lauf `41884936792` waren `go-unit-tests` und `cli-package-tests` rot mit den oben wortwörtlich gesicherten First-run-Fehlern. Der neue Lauf enthält die reparierten Testfälle; abschließender Beleg der geänderten Ergebnisse folgt aus dem terminalen Laufbericht.

### Scope und Regelkonformität

- Kandidatenänderung umfasst sieben Dateien: `cmd/baha/app_input_resolver_first_run_test.go`, `cmd/baha/main.go`, `cmd/baha/operator_membership_provider.go`, `internal/database/identity_tenant_resolver.go`, `internal/database/identity_tenant_resolver_integration_test.go`, `internal/operatorauth/authorization_test.go`, `internal/operatorauth/context.go`.
- Gesamter Name-only-Diff gegen Develop hat 17 Dateien: die vorbestehenden dreizehn Team-auth-Dateien plus diese vier zusätzlichen Pfade (`cmd/baha/main.go`, neuer Provider, Datenbankresolver samt Integrationstest); keine Codec-/Fremddatei, kein `.github`-Pfad.
- PR #1369 bleibt OPEN, nicht Draft; kein Merge und keine Statusänderung ausgeführt.
- ## repo-rule compliance
  - Derselbe zugewiesene Branch und dasselbe Worktree verwendet; keine zweite Branch/PR, keine Subagenten.
  - Nur aufgezählte Quelldateien gebündelt und gestaged; keine fremden oder ungesicherten Änderungen überschrieben.
  - Keine Tests entfernt/abgeschwächt, keine Workflowdatei geändert, kein Force-Push, keine CI-Reruns/Dispatches.

