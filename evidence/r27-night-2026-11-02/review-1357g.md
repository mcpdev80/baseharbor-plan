# PR #1357 Re-Review ea3e88e0

ROLLE=REVIEW, kein Merge. **Urteil: REJECT.** Task `t-20261022-r27-ci-access`; Reviewer Codex GPT-6 (exakte Variante nicht exponiert). Head `ea3e88e0769456abcc0ec4dc96eb9351f4ea78a2`, tree `0ac6df3a97b6fe132af44fb304cfa2537dd4b3ac`; develop `0107d8e1530ff3469048022d7035a2a472dbda34` ist Vorfahr. `git ls-remote` vor/nach bestätigt beide; PR OPEN/CLEAN. SHA-genaues Archiv, Kandidat unverändert.

## Gegenprüfung

1. **Nicht-TLS-Remote-Gegenprobe jetzt korrekt zurückgewiesen.** Ein unabhängiger temporärer Test ruft `assertTLSHandshakeCause` mit `&net.OpError{Op:"remote error", Err:errors.New("not a TLS error")}` auf: Test FAIL mit `not a classified TLS/handshake/verification cause`, wie beauftragt. Die frühere pauschale Akzeptanz ist damit für dieses konkrete Gegenbeispiel behoben. Echter TLS-Server mit `RequireAndVerifyClientCert` bleibt erhalten; positive Check-/Execute-Tests bestätigen ihre jeweiligen Handler-Flags.

2. **Nicht alle negativen Check-Fälle prüfen den richtigen Recorder.** `TestMutualTLSRejectsSelfSignedClientCert` (`client_test.go:676`, Recorder bei `:708` verworfen) und `TestMutualTLSRejectsWrongServerCA` (`:870`, Recorder bei `:876` verworfen) rufen `Check` auf `/readyz`, prüfen aber weiterhin nur `handler.HandlerReached` für den anderen `/internal/`-Handler. Der Delta ergänzt positive Kontrollen für missing-cert und foreign-CA, nicht die fehlenden Ready-Negativassertions dieser beiden Fälle. Die Mission verlangt beide Flags für sämtliche Negativen; dies ist nicht erfüllt. Ein separater Test für ein beschädigtes Client-Zertifikat fehlt weiterhin; `TestMutualTLSRejectsCorruptedClientCertKey` beschädigt nur den Key. **Rezept:** Ready-Recorder in beiden Tests behalten und `false` assertieren, Execute-Mutationszähler ebenfalls `false`; beschädigtes Client-Cert separat über `NewClient` testen und positive Kontrollen beibehalten. Test-Wrapper kann den rein testbezogenen Flag im Produktions-Handler ersetzen.

3. **CI und Slice-Grenzen.** Hosted Run `41677012219` meldet denselben Head COMPLETED/SUCCESS; Source format und PR Selected Checks SUCCESS. Netto-Diff gegen develop nur `internal/runtimeexecutor/client_test.go` und `internal/runtimeexecutor/handler.go`. Andere Access-/Gate-Slices und ihre Missing-Coverage-Nachweise bleiben bei den jeweiligen Ownern, keine Gesamtqualifikation behauptet.

## Tests

`GOCACHE=/tmp/opencode/gc TMPDIR=/tmp go test ./internal/runtimeexecutor -count=1 -timeout 8m`: PASS (0.046s); `gofmt -l` beider Dateien leer. Unabhängiger Fake-Remote-Error-Test erwartungsgemäß FAIL auf die zu testende Helper-Ablehnung; er war nur im temporären Archiv vorhanden. Kein Merge.
