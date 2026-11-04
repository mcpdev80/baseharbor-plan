# PR #1364 Abschlussreview — workstation enrollment

ROLLE=REVIEW, kein Merge. **Urteil: REJECT.** Reviewer Codex GPT-6 Luna. Task `t-20261018-r27-device-enrollment`. Geprüfter Head `2a4df949f5f39b67f1d098bb5faa226c8703ffb9`, tree `636c2bbf625d286751e63120189f90a75d1ff725`, PR-base `develop` `3d08ef72a967704075805a511fb361f30684763b`. PR #1364 OPEN/READY (`draft=false`), CLEAN/MERGEABLE. `git ls-remote` bestätigte PR-Head und `develop` `e3a0858e448127e67ad1c7752a9e603bbda739c1`. Develop ist seit der PR-Base vier Commits voraus; dieses Urteil gilt für den gemeldeten, unveränderten Diff und muss nach einer späteren Base-Aktualisierung erneut abgeglichen werden.

Der exakte PR-Diff fügt ausschließlich Dateien unter `contracts/workstationenrollment/v1/`, `internal/workstationenrollment/` und Task-Evidence hinzu. Keine `internal/targetenrollment`-Datei und keine vorhandene Register-/Routing-Datei wurde geändert. Das Workstation-Namespace ist getrennt vom Node/Connector-Pfad.

## Eigene Gegenproben

Die Probe lief auf einem SHA-genauen Snapshot unter `/tmp`; der PR-Head blieb unverändert.

1. **Token-Wiederverwendung:** `TestSecondUseRejected` plus eigene Probe: zweiter `Authority.Enroll` wird mit `ErrDenied` abgewiesen. Der HTTP-Fehlerpfad serialisiert den generischen Ablehnungsgrund `workstation enrollment is invalid, expired, or consumed`. **PASS**.
2. **Ablauf:** `TestExpiryRejected` legt einen abgelaufenen Grant an; `Store.Consume` weist ihn ab. **PASS**.
3. **Fremdes Ziel/Scope:** `TestForeignRecipientRejected` plus eigene Gegenprobe mit anderer Installation und gleicher Station: fremder Scope erhält `ErrDenied`; der gültige Besitzer kann den ursprünglichen Grant danach noch verwenden. **PASS**.
4. **Positivfall/Identität:** `TestEnrollPositiveIssuesLeafWithScopeAndTime` und `TestHTTPBootstrapThenEnroll` bestehen. Eigene Probe dekodierte das ausgegebene Leaf und bestätigte die getrennte URI `spiffe://baseharbor/workstations/<installation>/<station>` sowie Serial und Ablaufzeit. Die HTTP-Fakt-Antwort enthält Installation, Station, Serial, `ExpiresAt` und `At`. **PASS**.
5. **Keine Node-Enrollment-Dateien:** vollständige PR-Dateiliste bestätigt ausschließlich neue Workstation-/Contract-/Evidence-Dateien. **PASS**.
6. **Eigener Namespace/geteilte Register:** ausschließlich neue Workstation-Dateien; kein vorhandener Register- oder Node-Pfad editiert. **PASS**.

## CI und Kandidatenintegrität

- Der in der Task-Notiz genannte Run `41800237126` ist auf älterem Head `299f81434ef996b5408363dfd7b3eb67e4b1a148` und qualifiziert den aktuellen Head nicht.
- Aktueller exakter Run `41804060900` auf `2a4df949...`: COMPLETED/SUCCESS. `PR Selected Checks` (App 15368), `go-build`, `go-unit-tests`, `go-vet`, `source-contracts`, `pr-planner-tests`, `ci-executor-tests`, Source format, Exact Candidate, Demo Pin und beide ausgewählten Docker-/Podman-Lifecycle-Gates PASS. Die bedingten, nicht ausgewählten Jobs SKIPPED.
- Gezielter `go test`-Lauf für die Enrollment-Paketfälle und eigene Gegenproben für fremde Installation, Replay-Grund und Zertifikatsidentität: PASS. Der gefilterte lokale Aufruf hatte in `contracts/workstationenrollment/v1` keine Tests passend zum `-run`-Filter; die vollständigen Contract-Tests sind durch den exakten CI-`go-unit-tests`-Job abgedeckt und dort PASS. `git diff --check` gegen die PR-Base: PASS.

## Befund und Rezept

1. **Der Slice ist nicht in einen Produktionspfad eingebunden; der Task-Vertrag verlangt diesen ausdrücklich.** Im exakten Head gibt es außerhalb der neuen Workstation-Pakete keinen Import oder Aufruf von `internal/workstationenrollment` oder `contracts/workstationenrollment/v1`. `Handler.Router` wird nur durch `httptest` in den Tests registriert; keine Management-Route bindet ihn ein. `EnrollDevice` wird außerhalb seiner Definition und Tests nicht aufgerufen. Die einzige Store-Implementierung ist `NewMemoryStore`; sie wird nur in Tests verwendet und erfüllt die eigene `Store`-Anforderung der Persistenz über Prozessneustarts nicht. Der HTTP-Bootstrap nimmt Installation und Station direkt aus dem Request; kein Produktionsaufrufer bindet sie derzeit an eine autorisierte Installations-Policy. Die positive „registry fact“-Antwort wird erzeugt, aber nicht in einem produktiven Registry-Owner gespeichert. Das ist ein isolierter, getesteter Prototyp, aber noch kein callable production path. Die Task-Note sagt ausdrücklich: „a standalone unused adapter is not complete“.

   **REZEPT:** den HTTP-Handler über den bestehenden, authentisierten Management-Einstiegspunkt registrieren und dessen Installations-Policy/Owner als Quelle für den Scope erzwingen; keine allein vom Request gelieferten Installation-/Station-Werte autorisieren. Die akzeptierte Authority/Registry-Schnittstelle im Produktionspfad verdrahten, mit einem Store, der den one-use Grant und Consume gemäß Store-Vertrag dauerhaft/fail-closed hält, sowie mit dem genehmigten Registry-Owner, der Scope, Issue-Zeit und getrennte Workstation-Identität als Fakt persistiert. Keine `targetenrollment`-Datei und keine fremde Registerdatei direkt ändern; wenn dafür ein anderes Write-Set nötig ist, vorher den zuständigen Owner/Task einbinden. Regressionen am echten Management-HTTP-Pfad für Unauthorized Bootstrap, Replay mit protokolliertem Ablehnungsgrund, Ablauf, fremde Installation/Station, positiven Zertifikat-/Registry-Fakt und Neustart zwischen Ausgabe/Verbrauch ergänzen. **Stop-Kriterium:** kein READY/Acceptance, bis ein Produktionsaufrufer samt Installations-Policy, dauerhafter one-use Verarbeitung und Registry-Fakt nachgewiesen ist; Node/Connector-Scope und geteilte Write-Sets bleiben unberührt.

## END

END_DONE codex-r1364a: verdict=REJECT open=1 | Fachliche Gegenproben und exakte CI sind grün, aber die neue Enrollment-Authority bleibt ungenutzt und besitzt keinen produktiven Policy-/Registry-Aufrufer.
