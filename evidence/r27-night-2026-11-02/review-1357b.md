# PR #1357 Re-Review 067274a1

ROLLE=REVIEW, kein Merge. **Urteil: REJECT.** Task `t-20261022-r27-ci-access`; Reviewer Codex GPT-6 (exakte Variante nicht exponiert). Head `067274a1d2c509c67b341a0849cb1490df2c4b7b`, tree `17f2bd9b7b92183542cda2e6b1fa1cea24fbf153`, develop `1706272c3e8d53d37cf4da8f9f1411e5fe419a94` ist Vorfahr. `git ls-remote` vor/nach bestätigt beide. PR OPEN, UNSTABLE. SHA-genaues Archiv; Kandidat nicht verändert.

## Befunde und Rezept

1. **TLS-Prüfung richtig eingerichtet, geforderter Handler-Nichtaufruf nicht belegt.** `internal/runtimeexecutor/client_test.go:198-225` startet einen echten TLS-Server mit `ClientCAs` und `RequireAndVerifyClientCert`. Positive Tests nutzen produktives `NewClient`, `Execute` und `Check`; negative Selbstsignatur/fremde Client-CA/falsche Server-CA rufen `Check` auf und erwarten irgendeinen Fehler. Es gibt jedoch keinen Zähler/Flag auf dem Handler oder ResourceManager, keinen direkten Nachweis der Handshake-Fehlerklasse und keinen negativen Execute-/Mutationsversuch. Ein späterer HTTP-Fehler würde diese negativen Assertions ebenfalls erfüllen. Die Tests für defekten Key und ungültiges CA-PEM scheitern zutreffend bereits beim Laden, nicht beim Handshake. `TestMutualTLSRejectsMissingClientCertificate` verwendet ein selbstsigniertes Zertifikat und testet keinen tatsächlich fehlenden Client-Cert. **Rezept:** Handler-/Mutationszähler und konkrete TLS-Fehlerursache bei fremdem/selfsigned Client und falscher Server-CA assertieren, mit produktivem Check/Execute und Null-Aufrufen bei Ablehnung; tatsächlich fehlendes Zertifikat separat testen, beschädigten Cert zusätzlich zum Key abdecken. Ladefehler als solche benennen.

2. **Bestehende Regressionen gelöscht.** Entgegen Auftragsannahme entfernt Delta `195886cc..067274a1` alle früheren sieben Tests: `TestNewClientRequiresHTTPS`, `TestNewClientRejectsEmptyURL`, `TestNewClientRejectsUnparseableURL`, `TestNewClientRejectsMissingCA`, `TestCheckReadinessRejectsNon200`, `TestExecuteRoundTripRequiresClientIdentity`, `TestExecuteRejectsNon200`. Insbesondere HTTPS-Enforcement, fehlerhafte URLs und Nicht-200-Verhalten werden nicht durch die neuen Tests ersetzt. **Rezept:** vorherige Tests wiederherstellen oder funktional gleichwertig erhalten; die neuen mTLS-Tests additiv ausführen.

3. **Gehostete Pflichtchecks nicht grün.** GitHub Actions run `41635298972`: `PR · Source format` FAILURE und `PR Selected Checks` FAILURE; go-build/go-vet/go-unit-tests sowie ausgewählte Docker-/Podman-Lifecycle-Jobs SUCCESS. Der neue Testcode ist nicht gofmt-formatiert. **Rezept:** Go-Datei formatieren, betroffene lokalen und gehosteten Checks auf dem finalen SHA erfolgreich abschließen; keine Gate-Umgehung.

4. **Slice-Matrix:** Diese Änderung qualifiziert ausschließlich den runtimeexecutor-Client-Testpfad; andere auf der Karte genannte Access-Slices und konkrete Ausführung/fehlende Coverage bleiben bei den zuständigen CI-/Slice-Ownern, wie in review-1357a festgehalten. Keine Behauptung vollständiger Access-Gate-Qualifikation.

## Eigener Test

`GOCACHE=/tmp/opencode/gc TMPDIR=/tmp go test ./internal/runtimeexecutor -count=1 -timeout 8m`: **PASS** (0.023s). Dieser Lauf belegt die vorhandenen Assertions, nicht den fehlenden Handler-Nichtaufruf oder gelöschte Regressionen.
