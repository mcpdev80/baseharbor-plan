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

Noch ausstehend.

