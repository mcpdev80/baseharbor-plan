ROLLE: REVIEW — rv1231

## PLAN

0. DONE — Auftrag und bindende Richtlinien gelesen; PLAN erfasst. Native TodoWrite ist nicht verfügbar.
1. DONE — Kandidat, Task, Evidence und Remote-Runs SHA-genau geprüft.
2. DONE — Podman-Dispatch und Docker-Fail-Closed anhand Diff und Tests geprüft; Urteil und Rezept erfasst.
3. DONE — Dossier zur Veröffentlichung vorbereitet; Push und ls-remote im Transcript bezeugen.

## Verdict: REQUEST_CHANGES

PR #1231 offen, Head b3dcb602a365d7fbae612e263741df35a88448de, Branch `runtime-validation/ha/control-plane/podman/quadlet-engine-o261`, Basis develop 72ba7a99ff7dcd4b04ee3cf16516991ef567d376; HTTPS ls-remote bezeugt die SHAs. Diff: ausschließlich `internal/runtime/docker_engine.go` und `docker_engine_test.go`. Planning o261.md enthält END; Task in review, Release-Abhängigkeit nicht accepted.

Run 41120505623 completed/success am genauen Head; Job `Targeted HA · podman` und `TestExistingControlPlaneRestartRequiresAndUsesRecoveryFile` liefen tatsächlich und bestanden (306 s). Das belegt diesen HA-Pfad, nicht alle Engine-Selection-Varianten. Exact-head PR Selected Checks sind failure (App 15368); Docker-Run 41120505740 failure ist laut Auftrag dokumentierter Fremdblocker und hier kein inhaltlicher Review-Gegenstand. Kein Merge.

**1. Docker-Resolver verändert:** `docker_engine.go:39-53,60` ersetzt bei `BASEHARBOR_TEST_RUNTIME=podman` auch im produktiven `ResolveDockerEngine` den angeforderten Docker-Befehl durch Podman. `cmd/baha/docker_engine.go:127-132` ruft diesen Resolver gerade für einen expliziten lokalen Docker-Target auf. Damit bestimmt eine Test-Umgebungsvariable den zu prüfenden Engine-Typ trotz Docker-Target; der behauptet unveränderte Docker-Pfad gilt nur für unset/docker. Das Test-Doppel prüft nicht Docker-Target bei gesetzter Podman-Testvariable. Keine Behauptung, dass der Docker-CI-Fremdblocker dadurch verursacht wurde.

**2. Podman-Zweig bleibt Docker-Context-gebunden:** `docker_engine.go:78-107` liest weiterhin `DOCKER_CONTEXT`/`DOCKER_HOST`, ruft `context show`/`context inspect` mit Docker-Endpunktformat auf und konstruiert beim `default`-Context `/run/user/<uid>/docker.sock`. Nur der Name des Programms wechselt. Die Aufgabe fordert, dass der Podman-Job keinen Docker-Context prüft; dieser Code stellt das nicht sicher. `docker_engine_test.go:129-150` liefert simulierte Docker-kompatible Antworten und prüft nur den Namen des Commands; bei default rootless wird der angebliche podman.sock-inspect-Zweig gar nicht erreicht. Lokales Podman-Binary war nicht vorhanden, deshalb kein eigener echter CLI-Test. Der grüne HA-Run bleibt gültiger Nachweis für den dort ausgeführten Fall, ersetzt aber keine Abdeckung von Context-/Endpoint- und Docker-Target-Fällen.

## Worker-Rezept

In `internal/runtime/docker_engine.go` Docker-Target-Auflösung unabhängig von `BASEHARBOR_TEST_RUNTIME` halten und Runtime-Auswahl an die tatsächliche Target-/Provider-Grenze oder eine ausdrücklich testlokale Dispatch-Stelle binden. Für Podman den nativen, tatsächlich unterstützten Podman-Pfad verwenden, ohne Docker-Context, Docker-Host oder Docker-Socket abzuleiten; vorhandene Docker-Endpoint-, Context- und Fail-Closed-Semantik unverändert erhalten. In `docker_engine_test.go` und passender Consumer-/Integrationstestdatei echte Dispatch-Aufrufe mit verbotenem Docker-Probe im Podman-Fall sowie explizitem Docker-Target bei gesetzter Podman-Testvariable prüfen; default und explizite Auswahl, Fehler und keine Engine-Fallbacks abdecken. Focused Tests und betroffene echte Podman-Qualification auf dem endgültigen SHA nachweisen. Stop bei Docker-Context-Aufruf im Podman-Pfad, durch Test-ENV geänderter Docker-Bindung, fehlender nativer Evidenz oder ungrünen Pflichtgates; erneut unabhängig prüfen lassen.

## repo-rule compliance

Lesende Prüfung, kein Produkt-Push, kein Merge, kein Claim-/Statuswechsel. Event geprüft und ack ausgeführt; übrige Coordinator-Reminders/Pool/PLAN-Hinweise bleiben offen.

END rv1231 REQUEST_CHANGES
