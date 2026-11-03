# Review 1347s

## Abschlussurteil nach neutralem Vergleich

ROLLE=REVIEW. **Urteil: ACCEPT-WITH-DEFERRAL** für `be00b1c8ca7e39c063c75f154c1e3c3fe21f01d5`, bezogen auf die sachliche Review-Matrix; die unten dokumentierten BLOCKED-Zwischenstände sind hiermit abgelöst. `git ls-remote` bei Abschluss: PR-Head `be00b1c8ca7e39c063c75f154c1e3c3fe21f01d5`, develop `1706272c3e8d53d37cf4da8f9f1411e5fe419a94`. Kein Merge.

Der unabhängige Worker-Vergleich [verify-cli-1347.md](verify-cli-1347.md) berichtet den vollständigen gefilterten `cmd/baha`-Lauf für genau diesen Head und für das genannte develop: beide FAIL mit denselben zwei Gruppen und `provider-registry-ownership-unverifiable` an `provider_external_removal_test.go:53` und `:151`; Deployment und Delivery bestanden auf beiden Ständen. Damit ist der vom Auftrag tolerierte Vergleich mit dem vorbestehenden Befund dokumentiert. Der CLI-Lauf ist **nicht grün**; der Bericht zeigt gleiche Fehler auf beiden Ständen, belegt aber für sich genommen keine abschließende technische Ursachenanalyse des Provider-Registry-Zustands. Die im Bericht erwähnte vollständige Ausgabe lag diesem Review nicht zur eigenen Einsicht vor. Der CLI-Sammellauf wurde auf ausdrückliche Anweisung nicht wiederholt.

Die Review-eigenen Deployment-/Delivery-Läufe bestanden; echte Core-Owner-Fixtures, negative Familien und Guard-Reihenfolge wurden wie unten belegt geprüft. Same-target Installation-ID-Bindung bleibt gemäß Task-Kartennotiz an den Authority-Vertrag delegiert. Der unabhängige kombinierte Prioritätstest war nur im Review-Archiv vorhanden; als dauerhafte Regression nachführen. Der missverständliche Helper-Kommentar ist nicht blockierend. GitHub meldete OPEN / UNSTABLE; dieses Sachurteil behauptet keine grüne CI und ersetzt keine erforderlichen Merge-Gates.

## Historische Zwischenstände

## Fortsetzung nach /tmp-Bereinigung

ROLLE=REVIEW. **Urteil: BLOCKED-LAUFZEIT; kein Abschlussurteil.** Einmaliger, durch die weiterhin geltende 90-Sekunden-Regel begrenzter Lauf: `TMPDIR=/tmp GOCACHE=/tmp/opencode/gc go test ./cmd/baha -run 'Deployment|Owner|Tenant|Scope|Binding|List|Guard|Retention|Vanish' -timeout 8m -count=1 -v`. Der Build gelang, mehrere ausgewählte Tests bestanden, aber der äußere 90-Sekunden-Timeout beendete den noch laufenden Sammeltest mit Exit 124 (`cmd/baha` 76.686s). Zuletzt aktiv: `TestApplicationDestructionRequiresCurrentOuterScopeAndSeparateDataConsent` in `cmd/baha/application_destroy_authorization_test.go:36`; der frühere Stack verortete das Warten in `Compose.ListRuntimeContainers` und einem Kindprozess. Die Suite ist unvollständig; kein PASS und kein Produktfehler daraus abgeleitet. Keine Wiederholung. Der bestandene Deployment-/Delivery-Lauf und der unabhängige Prioritätstest sind unten dokumentiert; Installation-ID-Bindung bleibt delegiert.

`git ls-remote` vor und nach dem Lauf: PR `be00b1c8ca7e39c063c75f154c1e3c3fe21f01d5`, develop `1706272c3e8d53d37cf4da8f9f1411e5fe419a94`. Nächster Schritt: CLI-Pflichtlauf bzw. dessen Umgebungsblockade außerhalb dieser zeitbegrenzten Review-Sandbox abschließend belegen; danach vollständige Matrix beurteilen. Kein Merge.

## Re-Attempt mit vorgegebenem CLI-Lauf

ROLLE=REVIEW. **Urteil: BLOCKED (Disk-Quota beim Build), kein Abschlussurteil.** Der unveränderte Kandidat und die bereits dokumentierten positiven Deployment-/Delivery- und unabhängigen Prioritätsbefunde bleiben gültig; der CLI-Pflichtlauf ist weiterhin nicht absolviert. Es handelt sich hier nicht um den 90-Sekunden-Laufzeitfall, sondern um einen sofortigen Buildfehler.

Einmaliger Lauf im SHA-genauen Archiv: `TMPDIR=/tmp GOCACHE=/tmp/opencode/gc go test ./cmd/baha -run 'Deployment|Owner|Tenant|Scope|Binding|List|Guard|Retention|Vanish' -timeout 8m -count=1 -v`, durch äußeres 90s-Limit begrenzt. Ergebnis innerhalb weniger Sekunden: `compile: writing output: write $WORK/b415/_pkg_.a: disk quota exceeded` in `internal/hostresource`; weitere `write /tmp/go-build.../importcfg: disk quota exceeded`, `FAIL .../cmd/baha [build failed]`. Kein Test wurde ausgeführt; kein grünes Gate behauptet. `/tmp` meldete 2,5 GiB frei, was eine separat wirkende Quota nicht ausschließt. Eigene alte Cache-Dateien umfassen nur 11 MiB, der vorgegebene `/tmp/opencode/gc` ist gemeinsamer Cache und wurde nicht gelöscht. Keine Wiederholung.

Vor und nach dem Re-Attempt `git ls-remote`: `refs/pull/1347/head` = `be00b1c8ca7e39c063c75f154c1e3c3fe21f01d5`, `refs/heads/develop` = `1706272c3e8d53d37cf4da8f9f1411e5fe419a94`; PR OPEN, UNSTABLE. Kein Merge. Nächster Auslöser: ausreichend nutzbare `/tmp`-Quota bzw. geeignete Umgebung bereitstellen und den vorgegebenen CLI-Lauf dort vollständig durchführen; anschließend Ergebnismatrix entscheiden. Same-target Installation-ID-Bindung bleibt gemäß Karte delegiert.

Historischer Stand: ROLLE=REVIEW (kein Merge), damals **BLOCKED / kein Abschlussurteil**. Der CLI-Pflichtlauf war durch Timeout unvollständig; ein Umweltfehler dieses konkreten Timeouts war nicht unabhängig nachgewiesen. Kein Produktfehler allein aus dem Timeout abgeleitet.

## Identität

- PR #1347: `be00b1c8ca7e39c063c75f154c1e3c3fe21f01d5`, Tree `07fb48b193f775a6ce6341ed3765cd7a55b3abf7`.
- Vor und nach Review `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1347/head refs/heads/develop`: PR `be00b1c8ca7e39c063c75f154c1e3c3fe21f01d5`, develop `1706272c3e8d53d37cf4da8f9f1411e5fe419a94`. Develop ist Vorfahr des Kandidaten. GitHub meldete OPEN / UNSTABLE; hosted CI ist hier nicht als bestanden belegt.
- Review des SHA-genauen Archivs; Kandidat nicht verändert. Delta zu `ccb5e83f` betrifft ausschließlich zwei Testdateien und den neuen Test-Helper.

## Befunde

1. Die vorher in review-1347r beanstandeten Guard-/Retention-Fixtures rufen nach Setzen des State-Verzeichnisses den Helper auf: 15 One-Writer- und 10 direkte Retention-Fixtures sowie die gemeinsame Byte-Stability-Fixture für fünf Fälle. Der Helper nutzt `coreinstallation.Run` und erzeugt einen echten autoritativen Core-Owner; kein globaler Bypass, kein Abschalten der Prüfung. Ein Kommentar des Helpers zur Reihenfolge ist missverständlich; der tatsächliche Aufruf erfolgt nach der Umgebungseinrichtung.
2. Negative Missing-/Foreign-/Corrupt-/Vanish-/Scope-Familien sind nicht durch das Delta entfernt oder global umgeseedet.
3. Ein unabhängig im temporären Review-Archiv hinzugefügter kombinierter Test bestand: identischer delegierter Datensatz und Save-Pfad liefert ohne Installation-Owner zuerst `ErrDeploymentOwnerMissing`; nach Wiederherstellen des Owner-Dokuments `ErrUnauthorizedMutation`, bei unveränderten Deployment-Bytes. Dieser Test ist **nicht** Bestandteil des PR; als dauerhafte Regression nachführen.
4. `TMPDIR=/tmp go test ./internal/deployment ./internal/delivery -count=1`: PASS (beide Pakete). Der Lauf `go test ./cmd/baha -run 'Deployment|Owner|Tenant|Scope|Binding|List|Guard|Retention|Vanish' -count=1 -timeout=120s` endete mit Timeout während `TestApplicationDestructionRequiresCurrentOuterScopeAndSeparateDataConsent`, Stack in `Compose.ListRuntimeContainers`/Kindprozess. Einzelwiederholung desselben Tests mit 25 Sekunden lief ebenfalls in Timeout (Docker-Engine-Kindprozess). Dies ist keine vollständige CLI-Evidence und kein Nachweis, dass genau dieser Fehler bereits auf develop auftritt.

## Rezept / Stop-Kriterium

CLI-Sammellauf auf geeigneter Testumgebung vollständig abschließen oder den konkreten Timeout unabhängig auf demselben develop-Stand reproduzieren und als vorbestehenden Umgebungsbefund belegen; übrige Resultate vollständig erfassen. Erst danach Urteil auf Basis der gesamten Matrix entscheiden. Same-target Installation-ID-Bindung bleibt gemäß Task-Kartennotiz an den Authority-Vertrag delegiert. Für die dauerhafte Prioritätsabsicherung den kombinierten Save-Test in `internal/deployment` aufnehmen und mit den Pakettests prüfen. Kein Merge aus diesem Zwischenstand.
