# CODEX-REVIEW 0427-134 CA-trust / PKCE — PR #1455

## PLAN

1. Prüfe live PR-Kopf, Develop-Basis, candidate diff, ancestry und Run 42451110988 sha-genau.
2. Vergleiche den Kandidaten mit der CA-trust/PKCE-Akzeptanz und dem 0427-039 Enrollment-Review #1436.
3. Prüfe den verlangten w0427-targeted Host-Cleanup-Beleg in der Planning-Akte.
4. Formuliere Urteil, konkrete Korrekturen, Testanforderung und Stop-Kriterium.
5. Publiziere diese Review-Akte in baseharbor-plan und verifiziere deren Remote-Präsenz.

## Urteil

**ROLLE: REVIEW**  
**URTEIL: KORREKTUR (REQUEST-CHANGES)**  
**Eingereichter Kandidat:** PR #1455, `9a9630003b1c9913626923adc06ef7d3402e5e34`  
**Live PR-Zustand:** OPEN, Titel `[0427-134] destroy: resolve owned Core targets from data root`, base `develop`, Head-Branch `work/r283-ca-pkce`  
**Gegenwärtiges develop:** `07ae6c3e91b081a189266ca4b162ba705d4aa78f`  
**Run:** `42451110988`, completed/success auf dem exakten Head

### Befunde

1. **Der Live-PR-Kandidat erfüllt den CA-trust/PKCE-Vertrag nicht und hat einen anderen Scope.** SHA-genauer Diff `origin/develop...9a9630003b1c9913626923adc06ef7d3402e5e34` enthält genau `cmd/baha/runtime_destroy_all.go` und `internal/deployment/target.go`; beide Commits tragen die Nachricht `0427-134 destroy: resolve owned Core targets from data root`. Es gibt in diesem Kandidaten keine Änderung an OIDC-CA-Auflösung, Bootstrap-CA-Ablage, PKCE-Callback/Codefile, Dokumentation oder den dazugehörigen Regressionen. Die Live-PR-Metadaten und der unveränderliche Commitinhalt widersprechen damit dem CA/PKCE-Auftrag und der auf `round-1.md` beschriebenen Implementierung. Der grüne Run belegt nur den tatsächlich eingereichten Destroy-Diff.

   **Korrektur:** Stelle für 0427-134 den vorgesehenen CA/PKCE-Kandidaten als eigenen PR-/Kandidatenkopf bereit. Er muss die OIDC-Trust-Quelle vom Bootstrap bzw. der dokumentierten `--ca`-Option über den tatsächlichen OIDC-Clientpfad anbinden, mit Priorität `flag > env > default` und additivem System-Root-Pool. Für Headless-PKCE muss der festgelegte Callback-Port durchgehend gebunden, Auth- und Callback-URL ausgegeben und `--auth-code-file` unterstützt werden; Device-Flow bleibt außerhalb des Vertrags. Halte den hier vorliegenden Destroy-Inventory-Fix aus dem CA/PKCE-Prüfkopf heraus und ordne ihn separat seinem tatsächlichen Task zu.

2. **Der Kandidat ist nicht auf den aktuellen Develop-Stand integriert.** `git merge-base --is-ancestor origin/develop HEAD` auf dem frisch geholten PR-Kopf `9a9630003b1c9913626923adc06ef7d3402e5e34` liefert Exit 1 für `origin/develop@07ae6c3e91b081a189266ca4b162ba705d4aa78f`. Damit ist dieser SHA auch unabhängig vom Scope-Mismatch nicht abnahmefähig gegen die aktuelle PR-Basis. Run `42451110988` ist zwar für genau diesen SHA erfolgreich, kann aber einen fehlenden Drift-Merge nicht ersetzen.

   **Korrektur:** Den korrekten CA/PKCE-Kandidaten auf den aktuellen `develop`-Head integrieren, Konflikte und den finalen SHA prüfen und dann die dafür erforderlichen Hosted-Checks auf genau diesem SHA beobachten. Keine CI-Neustarts oder Workflow-Änderungen durch diese Review-Session.

3. **Die 0427-039 Enrollment-Akzeptanz bleibt eine eigene, nicht durch CA/PKCE allein erfüllte Schranke.** `act-1436-review.md` und `node-cli/round-4.md` unterscheiden explizit den einmaligen Bootstrap-Grant von der autoritativen Zertifikats-/Enrollment-Lifecycle-Antwort aus Core. Die spätere #1436-Review verlangte Tests durch den echten Node-CLI/Core-Pfad; round-4 hält außerdem offene Mutation-Lücken und fehlenden Hosted-CI-Nachweis fest. CA-Trust und headless PKCE beseitigen vorgelagerte Login-Hindernisse, beweisen aber weder eine eingelöste Connector-Enrollment-Identität noch korrekte enrolled/expired/revoked-Statusmeldungen. Der aktuelle PR enthält auch diesen Node-CLI/Core-Pfad nicht. Im Planning-Vault habe ich `act-1436-review.md` und round-4 als einschlägige Review-Linie gefunden; eine separate `act-1437-review`-Datei ist dort nicht vorhanden.

   **Korrektur/Testanforderung:** Für 0427-134 genügt ein CA-signierter OIDC Discovery-Test über den wirklichen Loginpfad plus ein vollständiger Headless-PKCE-Codefile-Test im CI. 0427-039 bleibt offen, bis dessen eigene Produktionstests den Grant über die Core-Authority einlösen und den autoritativen Enrollment-Lifecycle prüfen; kein lokaler Grant-Expiry-Wert darf als Enrollment- oder Zertifikatsstatus ausgegeben werden. Diese Review behauptet keine #039-Abnahme.

4. **Der angeforderte w0427-Host-Cleanup ist nicht belegt und der dokumentierte Zustand ist nicht sauber.** `evidence/.../e2e-abnahme/podman2.md` nennt vor dem Lauf 10 Container plus ein Core-Volume und attestiert am Ende noch eine laufende Managed-Core-Installation (Keycloak/OpenBao/Postgres/Gateway); der vollständige Destroy blieb am Consent-Gate hängen. `bughunt-ca-pkce/round-1.md` nennt anschließend 11 laufende Container inklusive des intakten w0427-Core. Das ist kein Vorher/Nachher-Beleg, dass ausschließlich das Ziel `w0427-owner-missing` gezielt entfernt wurde. Der Coordinator-Auftrag untersagt Gate-Bypass; diese Review hat daher weder interaktives Destroy versucht noch Container auf dem Host gestartet oder entfernt.

   **Korrektur/Testanforderung:** Der zuständige Host-Owner soll die freigegebene manuelle, nur auf `w0427-owner-missing` begrenzte Bereinigung ausführen und in einer Host-Akte die exakten Before/After-Inventare für Targets, zugehörige Container/Projekte und Volumes dokumentieren. `podman-local2` und ambient resources müssen unverändert bleiben. Der Stop-Punkt ist erreicht, wenn die Ziel-Installation und ihre zugehörigen Ressourcen entfernt sind, die unabhängigen Targets/ambient resources byte- bzw. inventargleich erhalten sind und keine interaktive Consent-Grenze umgangen wurde. Keine Container- oder Testoperation dieser Review-Session.

## Evidenz und Regeln

- Remote-Zeuge: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1455/head` meldete `07ae6c3e91b081a189266ca4b162ba705d4aa78f refs/heads/develop` und `9a9630003b1c9913626923adc06ef7d3402e5e34 refs/pull/1455/head`.
- `gh pr view 1455` meldete OPEN, base `develop`, head branch `work/r283-ca-pkce`, Titel `[0427-134] destroy: resolve owned Core targets from data root`; die Dateienliste entsprach exakt dem oben genannten zweifileigen Destroy-Diff.
- `gh run view 42451110988` meldete `headSha=9a9630003b1c9913626923adc06ef7d3402e5e34`, completed, success. Die Jobs `Workflow policy` und `Release Source Preflight` waren success; die PR-Validierungs-, native Keycloak/Core-, Docker-/Podman-, Exact-Candidate- und Selected-Checks waren skipped. Der Erfolg ist kein Nachweis für die fehlenden CA/PKCE-Tests oder eine abgeschlossene Host-Bereinigung.
- Candidate ancestry: `git merge-base --is-ancestor origin/develop HEAD` Exit 1.
- Kein Produktcode geändert, kein lokaler Test gestartet, keine Workflow-Datei verändert, kein CI-Rerun/Dispatch und keine Host-/Container-Bereinigung durch diese Review.
- Enrollment-Gegenprüfung: `evidence/r27-welle5-folge-2026-11-07/node-cli/act-1436-review.md` und `node-cli/round-4.md`; Aufgabe `tasks/t-20261018-r27-node-cli.md` bleibt eine getrennte Abnahme.
- Repo-Regelkonformität: Akte liegt nur im Planning-Vault; es sind keine Markdown-Checkboxen in dieser Akte enthalten.

## Stop-Kriterium

Keine Freigabe von PR #1455 als 0427-134, bis ein SHA-korrekter CA-trust/PKCE-Kandidat vorliegt, seine Integration auf den aktuellen Develop-Head bewiesen ist, die CA- und Headless-PKCE-Regressionen auf exakt diesem SHA durch Hosted-CI ausgeführt und bestanden sind, der scoped w0427-Cleanup mit Before/After-Inventar belegt ist und die getrennte 0427-039-Enrollment-Abnahme nicht als durch diesen Slice erledigt ausgegeben wird.

## END

END_BLOCKED 0427-134-ca-pkce-review — KORREKTUR erforderlich; eingereichter PR-Kopf `9a9630003b1c9913626923adc06ef7d3402e5e34` ist ein scope-fremder Destroy-Diff und nicht ancestry-clean gegen aktuelles develop.
