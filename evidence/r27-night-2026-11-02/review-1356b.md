# PR #1356 Re-Review 1be411f6

ROLLE=REVIEW, kein Merge. **Urteil: ACCEPT-WITH-DEFERRAL** für den geprüften Test-Slice, keine Aussage vollständiger Qualifikation sämtlicher Runtime-Slices. Task `t-20261022-r27-ci-runtime`; Reviewer Codex GPT-6 (exakte Variante nicht exponiert). Head `1be411f6cd051b6de33252f58cf949908e0a6bf6`, tree `37930014604f535d8302c60b8d826962f6900f1f`; develop `1706272c3e8d53d37cf4da8f9f1411e5fe419a94` ist Vorfahr. `git ls-remote` vor/nach bestätigt beide; PR OPEN / CLEAN. SHA-genaues Archiv; Kandidat unverändert.

## Befunde gegen review-1356a

1. **Integration korrigiert.** Aktuelles develop ist Vorfahr. Netto-Diff umfasst nur `internal/deployment/runtime_selection_test.go`, `internal/providers/runtime/podman/local_authority_verify_test.go` und `internal/runtimeexecutor/handler_test.go`; `.github`/`scripts` unverändert.
2. **Regressionsverlust behoben.** Alle fünf develop-Tests einschließlich Legacy-Default, vier Umgebungen, fremde State-Felder, unbekanntes Profil und Kubernetes-Future-Provider sind inhaltlich erhalten; neue Runtime-Auswahlfälle sind additiv, ohne doppelte Testfunktionen. Die Negativfälle rufen tatsächliche Parser/Selection-Funktionen; die Podman-Prüfungen testen den realen Authority-Validator und fehlendes Executable; Handler-Tests üben die reale Handlerlogik und Ablehnung unzulässiger Eingaben. Synthetische PeerCertificates beweisen weiterhin keinen echten TLS-Handshake oder Remote-Runner-Isolation.
3. **Selektions- und Slice-Grenze.** Der verlangte `-run Runtime`-Lauf selektiert nicht alle Namen der Podman- und Handler-Negativtests; diese wurden deshalb separat direkt ausgeführt. Die Karte nennt node-service, node-trust, node-streams, node-cli, remote-material, remote-docker-web, remote-podman-web, remote-rollout, state-recovery und maintenance-client. Dieser Test-Slice allein qualifiziert sie nicht vollständig. Konkrete Check-Zuordnung, fehlende Coverage und tatsächliche Remote-/Runner-Nachweise bleiben bei den zuständigen CI-/Slice-Ownern; insbesondere remote-docker-web bleibt gemäß Mission beim Owner.

## Prüfungen und verbleibende Umgebungsklärung

- `GOCACHE=/tmp/opencode/gc TMPDIR=/tmp go test ./internal/deployment -run 'Runtime' -count=1 -timeout 8m`: PASS (0.004s).
- Direkte zusätzliche Auswahl `go test ./internal/providers/runtime/podman ./internal/runtimeexecutor -run 'TestVerifyLocalAuthority|TestVerifyLocalRuntimeAuthority|TestHandler|TestNewHandler' -count=1 -timeout 8m`: beide PASS.
- Zusätzlicher **vollständiger** lokaler Podman-/Runtimeexecutor-Paketlauf: Runtimeexecutor PASS; Podman FAIL in `TestRetiredQuadletDefinitionCannotReappearAtBootAndKeepsSiblingData` und `TestQuadletRetirementRejectsForeignModifiedOrReplacedOwner/replaced`, jeweils `Quadlet retirement has an ambiguous unit directory owner`. Diese Fehler betreffen nicht die neu hinzugefügten Tests; eine Baseline-/Umgebungsursache wurde in diesem Review nicht nachgewiesen. Als offener lokaler Befund an Podman-/CI-Owner übergeben, nicht als grün rechnen.
- GitHub Actions Run `41640414170` meldet denselben Head und COMPLETED/SUCCESS; Source format, go-unit-tests, deployment-package-tests, runtime-provider-package-tests und PR Selected Checks SUCCESS. Der gehostete Paketpass und der lokale Podman-Fehler sind unterschiedliche Beobachtungen.
- Prozessvermerk aus r1356a: PR wurde ready statt draft eröffnet; Coordinator hat dies laut Auftrag rückgemeldet.

## Rezept für Restpunkte

Podman-Owner klärt die lokalen Quadlet-Fehler gegen die dokumentierte Umgebung und reproduziert sie gegebenenfalls auf develop; CI-/Slice-Owner dokumentieren die tatsächlichen Check-Identitäten und Negativnachweise für die übrige Matrix, insbesondere remote-docker-web. Kein Merge in dieser Review-Rolle.
