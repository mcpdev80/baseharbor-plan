# PR #1357 Re-Review bd7009c5

ROLLE=REVIEW, kein Merge. **Urteil: REJECT.** Task `t-20261022-r27-ci-access`; Reviewer Codex GPT-6 (exakte Variante nicht exponiert). Head `bd7009c5276c17b4453a3ee6dc817a481409098f`, tree `ef4fe923b99fae7e1d535e107d4d759975917b47`; develop `0107d8e1530ff3469048022d7035a2a472dbda34` ist Vorfahr. `git ls-remote` vor/nach bestätigt beide; PR OPEN/CLEAN. SHA-genaues Archiv, Kandidat unverändert.

## Zählung / Befunde

- Für die fünf explizit mit `newMutualTLSServerWithHandler` instrumentierten Negativfälle stimmen N und M: fehlendes Client-Cert (`client_test.go:611`), selbstsigniert (`:676`), fremde Client-CA (`:739`), defekter Client-Key (`:802`), falsche Server-CA (`:877`) prüfen jeweils Ready- und Execute-Flag false. Die ersten vier TLS-Identitäts-/Server-CA-Fälle scheitern beim Check-Handshake, der defekte Key bereits beim Laden. Positive Check-/Execute-Tests prüfen die jeweiligen Flags true.
- Der separate sechste Material-Negativtest `TestMutualTLSRejectsInvalidCAPEM` (`:841`) ruft `newMutualTLSServer` ohne zugängliche Recorder auf und assertiert deshalb nicht beide Flags; er beweist einen konkreten CA-Ladefehler vor Konstruktion, keine Handshake-Aussage. Ein expliziter Test mit beschädigtem Client-**Zertifikat** fehlt weiterhin: `TestMutualTLSRejectsCorruptedClientCertKey` beschädigt nur den Key. Das ist ein in r1357e/f mehrfach angeforderter, noch offener Negativfall; die fünfgezählte Tabelle erfasst ihn nicht. **Rezept:** defektes Client-Cert separat über echten `NewClient` und beide Handler-Recorder testen; Invalid-CA-Ladefehler ebenfalls mit zugänglichen Recordern/Null-Aufruf assertieren und die Matrix inklusive Lade- versus Handshake-Phase vollständig führen.
- Mutation-Gegenprobe ausschließlich im temporären Archiv: alle Testserver von `RequireAndVerifyClientCert` auf `NoClientCert` gesetzt; `TestCheckNegativesObserveReadyRoute` FAIL mit `readyz ... must not be entered`, wie erwartet. Keine Kandidatenänderung gepusht.
- Netto-Diff gegen develop betrifft `internal/runtimeexecutor/client_test.go` **und** `internal/runtimeexecutor/handler.go` (Test-Flag in Produktion); die Mission behauptete nur Testdatei. Übrige Access-/CI-Gate-Slices bleiben bei den zuständigen Ownern.

## Tests / CI

`GOCACHE=/tmp/opencode/gc TMPDIR=/tmp go test ./internal/runtimeexecutor -count=1 -timeout 8m`: PASS (0.058s). Hosted Run `41682175473` auf exakt diesem Head COMPLETED/SUCCESS; Source format und PR Selected Checks SUCCESS. Trotz grüner Checks sind die genannten Negativfälle nicht durch die aktuellen Assertions belegt. Kein Merge.
