# PR #1357 Re-Review 090295ea

ROLLE=REVIEW, kein Merge. **Urteil: REJECT.** Task `t-20261022-r27-ci-access`; Reviewer Codex GPT-6 (exakte Variante nicht exponiert). Head `090295eaea747acc4424762129769af546b7d36d`, tree `90e7959b270ea07084d9ac311e1aa034c2846b8f`; develop `0107d8e1530ff3469048022d7035a2a472dbda34` ist Vorfahr. `git ls-remote` vor/nach bestätigt beide; PR OPEN/CLEAN. SHA-genaues Archiv; Kandidat unverändert.

## Gegenprüfung

1. **Mutation-Control und Teilmenge der Ready-Negativen wirksam.** Der reguläre Paketlauf besteht. Unabhängig nur im Archiv TLS-Server von `RequireAndVerifyClientCert` auf `NoClientCert` verändert: `TestCheckNegativesObserveReadyRoute` scheitert mit `readyz ... must not be entered` (**erwarteter FAIL**); damit ist die Assertion für fehlendes Cert diskriminierend. Positive Tests prüfen Ready-Recorder und Execute-Handler auf true. Die neue Testgruppe prüft fehlendes Cert und fremde CA auf beide Recorder, aber die ursprünglichen selbstsigniert- und falsche-Server-CA-Checktests (`client_test.go:580` bzw. `:748`) verwerfen weiterhin den Ready-Recorder und prüfen nur den Execute-Flag. Die Behauptung „beide recorder ... in allen negativen“ trifft somit nicht zu. **Rezept:** jeweils Recorder des tatsächlich aufgerufenen Ready-Pfads und Execute-Mutationszähler prüfen; alle negativen Handshake-Klassen samt positiver Gegenprobe tabellarisch abdecken.

2. **Fehlerursache nicht durchgehend TLS-typfest.** `assertTLSHandshakeCause` akzeptiert jedes `*net.OpError` mit `Op == "remote error"`, ohne dessen `Err` zu prüfen. Unabhängiger temporärer Test übergibt `&net.OpError{Op:"remote error", Err:errors.New("not a TLS error")}`: der Helper akzeptiert ihn, Gegenprobe FAIL. Ein separater Test für beschädigtes Client-Zertifikat fehlt weiterhin; der benannte `CorruptedClientCertKey` beschädigt nur den Key. **Rezept:** konkrete TLS-Alert-/x509-Fehlerkette oder nachweislich gleichwertige serverseitige TLS-Ablehnung assertieren und nicht-TLS-Remote-Fehler als Negativkontrolle zurückweisen; beschädigtes Client-Cert separat über `NewClient` testen.

3. **CI und Scope.** Hosted Run `41670724731` meldet denselben Head COMPLETED/SUCCESS; Source format und PR Selected Checks SUCCESS. Netto-Diff gegen develop: nur `internal/runtimeexecutor/client_test.go` und `internal/runtimeexecutor/handler.go`; der Handler enthält weiter ein Test-Flag im Produktionscode. Übrige Access-/Gate-Slices bleiben bei zuständigen Ownern; keine vollständige Matrix behauptet.

## Tests

`GOCACHE=/tmp/opencode/gc TMPDIR=/tmp go test ./internal/runtimeexecutor -count=1 -timeout 8m`: PASS (0.039s). Unabhängige Test-only-Mutation ohne Client-Zertifikatsprüfung: erwarteter FAIL; nicht-TLS-Remote-Error-Gegenprobe: unerwarteter Helper-PASS, deshalb übergeordneter Test FAIL. Alle Änderungen ausschließlich im temporären Archiv, kein Merge.
