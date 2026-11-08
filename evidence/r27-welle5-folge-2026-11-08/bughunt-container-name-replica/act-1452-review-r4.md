# CODEX-REVIEW 0427-128 r4 — PR #1452

## PLAN

1. Prüfe PR-Kopf, develop-Basis, r3-Ancestry, Delta und exakten Hosted Run.
2. Prüfe die r3-Befunde in Retirement, Control-Plane-Observation, Cross-Project-Pinned-Identität und Selected-Stop-Postcondition auf Produktionspfaden.
3. Erfasse den terminalen CI-Fehler und die fehlende Owner-seitige Runtime-Integration-Auswahl.
4. Schreibe Urteil, konkrete Reparaturen, Tests und Stop-Kriterium in diese Akte.
5. Veröffentliche die Review-Akte im Planning-Vault und verifiziere die Remote-Präsenz.

## Urteil

**ROLLE: REVIEW**  
**URTEIL: KORREKTUR (REQUEST-CHANGES)**  
**PR #1452 Kopf:** `48814ecc5e8603f16f4849249fffc9b0c8abd7ab`  
**Basis develop:** `07ae6c3e91b081a189266ca4b162ba705d4aa78f`  
**r3-Kopf:** `54a6fd11dd639062e537a44815f25a80c3c4b8b2`  
**Exakter Hosted Run:** `42455350913`, terminal failure auf dem exakten r4-Kopf

### 1. STATE: gehostete Pflichtprüfungen sind rot; r4-Handoff „CI grün“ ist unvollständig

`PR · Validation · go-unit-tests` ist in Run `42455350913` fehlgeschlagen. Die Logzeilen nennen mehrere Panics beim Retirement:

- `TestControlPlaneLastPermissionConsumerRetirementKeepsDataAndRecovery` — `panic: runtime error: invalid memory address or nil pointer dereference`; Stack: `internal/runtime.expectedContainerNameSet` in `container_identity.go:37`, aufgerufen aus `RetireOwnedServices` in `service_retirement.go:90`.
- `TestExposureRetirementPreservesSiblingAndOwnerForRetry` — derselbe nil-pointer panic; Stack führt ebenfalls über `expectedContainerNameSet` und `service_retirement.go:90`.
- `TestBrokerRetirementKeepsConsolidatedWorkloadBackendAndData` — derselbe nil-pointer panic; Stack führt über `expectedContainerNameSet` und `service_retirement.go:90`.

`PR Selected Checks` ist ebenfalls fehlgeschlagen; der Logeintrag lautet `BLOCKED: required job did not succeed: pr_validations`. Damit ist der Hosted Run nicht erfolgreich. Der r4-Evidence-Handoff beschreibt lokale Go-Prüfungen als grün, aber nicht das terminal rote Hosted-Ergebnis dieses exakten Kopfes; als Abschlussnachweis ist diese Aussage unvollständig (Eigenes-Run-Pflicht §4.6).

**Lösungsrezept:** In `internal/runtime/service_retirement.go:88-92` muss die optionale Renderfähigkeit sicher behandelt werden. Aktuell genügt die strukturelle `RuntimeConfigProvider`-Type-Assertion, auch wenn ein Wrapper die Methode durch Einbettung eines nil-Providers erhält; `expectedContainerNameSet` ruft dann den promovierten nil-Methodenpfad auf. Stelle sicher, dass nur ein tatsächlich initialisierter Renderer aufgerufen wird; aktualisiere die betroffenen Retirement-Testdoubles so, dass sie entweder einen sicheren Renderer implementieren oder die optionale Renderfähigkeit nicht vortäuschen. Behalte den canonical-only Fallback fail-closed für pinned Namen. Danach muss `go-unit-tests` auf einem korrigierten Kopf ohne Panic bestehen und `PR Selected Checks` auf demselben Kopf success sein. Kein Rerun wurde durch diese Review ausgelöst.

### 2. Retirement und Control-Plane-Observation: produktive Identitätsprüfung ist erweitert

Im r4-Delta berechnet `internal/runtime/service_retirement.go:79-105` den gerenderten Namen pro Service und prüft mit `ContainerNameInPlannedSet`; ein Container wird zuvor auf das exakte Projekt und den erwarteten Service begrenzt. `cmd/baha/control_plane_stop_observation.go:43-75` berechnet die Render-Menge vor der Replica-Prüfung und entfernt damit die r3-erwähnte frühe canonical-only Ablehnung. Die `ContainerNameInPlannedSet`-Implementierung prüft Projekt, Service und nativen Namen.

Diese r3-Produktionsbefunde sind im Quelltext behoben, wenn ein gültiges Compose-Modell verfügbar ist. Bei fehlgeschlagener/fehlender Render-Auflösung wird weiterhin auf den kanonischen Ordinalnamen zurückgefallen; ein unbekannter pinned Name wird dann abgelehnt, also fail-closed. Die neuen Retirement-Aufrufe laufen im Hosted Run jedoch in den oben genannten Panics und können deshalb noch nicht als erfolgreich validiert gelten.

### 3. Cross-Project-Pinned-Abdeckung: Matcher-Negativtest ist vorhanden, Produktionspfad-Regressionsbeleg fehlt

`internal/runtime/service_retirement_test.go:129-156` ergänzt `TestRetireOwnedServicesRejectsForeignPinnedReplica`, aber der zweite Teil ruft `ContainerNameInPlannedSet` direkt mit einem Fremdprojekt auf. Das `RetireOwnedServices`-Fixture wurde zuvor nur mit dem eigenen Projekt befüllt. Der Test belegt somit den Helper-Vertrag, nicht, dass Retirement oder Control-Plane-Observation bei einer Runtime-Inventur mit dem exakt gleichen pinned Namen im Fremdprojekt die fremde Ressource unberührt lässt. Der Quelltext filtert in Retirement nach `container.Project == project` und in Control-Plane-Observation nach dem Projekt, doch die r3-Auflage verlangte einen Cross-Project-Negativbeleg auf Produktionspfad-Ebene.

**Lösungsrezept:** Erweitere `service_retirement_test.go` und einen Control-Plane-Observation-Test so, dass der Produktionsaufruf eine fremdprojektgebundene Runtime-Container-Zeile mit exakt demselben pinned Namen und Service sieht. Belege, dass die fremde Zeile nicht als eigener Prozess akzeptiert, nicht ausgewählt und nicht mutiert wird; der Test muss den Produktionsaufruf statt nur des Matchers ausführen. Die erfolgreiche eigene pinned Retirement muss parallel erhalten bleiben.

### 4. Selected-Stop-Postcondition: Quelltext und Fake-Test decken den pinned Namen ab; Hosted-Ausführung fehlt

Die r3-Postcondition ist in `internal/runtime/service_stop.go:147-155` geändert: nach dem Stop wird die Beobachtung gegen die gerenderte `plannedByService`-Menge plus kanonischen Namen geprüft; ein noch laufender ausgewählter Prozess schlägt fehl. `TestSelectedStopAcceptsPinnedContainerName` führt den production `StopOwnedProjectServices`-Aufruf aus und verlangt `result.Verified`; `TestSelectedStopRejectsUnplannedPinnedReplica` deckt die negative Variante ab. Das ist für den gerenderten Compose-Pfad eine passende Quelltext-/Unit-Regression.

Der native Test `TestRepositoryComposePinnedWorkloadLifecycleInCI` ist auf `BASEHARBOR_CI_RUNTIME_INTEGRATION=1` gegated. `round-4.md` dokumentiert weiterhin den Owner-Befund `.github/workflows/ci.yml:349`: der Runtime-Integrations-Selector nimmt den Test nicht auf. Im exakten Run waren `validate`, `Targeted HA · docker` und `Targeted HA · podman` skipped; es gibt daher keinen gehosteten nativen Beleg für die neue pinned Lifecycle-/Postcondition-Abdeckung.

**Lösungsrezept:** Owner-Änderung an `.github/workflows/ci.yml:349`: `TestRepositoryComposePinnedWorkloadLifecycleInCI` in den passenden Runtime-Integration-Selector aufnehmen. Danach muss ein Hosted Run durch den vorgesehenen Trigger den Test tatsächlich ausführen und bestehen. Keine Workflow-Datei wurde geändert und kein CI-Lauf gestartet.

## SHA-, Scope- und CI-Zeugen

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1452/head` meldete `07ae6c3e91b081a189266ca4b162ba705d4aa78f refs/heads/develop` und `48814ecc5e8603f16f4849249fffc9b0c8abd7ab refs/pull/1452/head`.
- `git merge-base --is-ancestor 54a6fd11dd639062e537a44815f25a80c3c4b8b2 48814ecc5e8603f16f4849249fffc9b0c8abd7ab` lieferte Exit 0; `git merge-base --is-ancestor 07ae6c3e91b081a189266ca4b162ba705d4aa78f 48814ecc5e8603f16f4849249fffc9b0c8abd7ab` lieferte Exit 0.
- PR-Gesamtdiff laut `gh pr view 1452 --json files` ist auf `cmd/baha/**` und `internal/runtime/**` beschränkt; `.github/**` ist nicht geändert. r4-Diff gegenüber r3 betrifft `cmd/baha/application_native_backend_retirement_test.go`, `cmd/baha/control_plane_stop_observation.go`, `internal/runtime/service_retirement.go`, `internal/runtime/service_retirement_test.go`, `internal/runtime/service_stop.go` und `internal/runtime/service_stop_test.go`.
- Run `42455350913`: `headSha=48814ecc5e8603f16f4849249fffc9b0c8abd7ab`, `status=completed`, `conclusion=failure`. `PR · Validation · go-unit-tests` und `PR Selected Checks` failure; `validate`, `Targeted HA · docker` und `Targeted HA · podman` skipped.
- Die r4-Planungsakte wurde aus Commit `3e7876664c115da345b7e828a2f72f960078882a` gelesen. Der aktuelle Planning-Remote-Stand wurde separat frisch geholt und ist inzwischen weitergelaufen.
- Veröffentlichung vor dem END: `git ls-remote origin refs/heads/main` ergab exakt `a6f95079351a1c49c5212746a80fa84228e03414 refs/heads/main`; `git ls-tree origin/main evidence/r27-welle5-folge-2026-11-08/bughunt-container-name-replica/act-1452-review-r4.md` ergab exakt `100644 blob f2b751d94bf8772e9d85879f46300d2562b5c026 evidence/r27-welle5-folge-2026-11-08/bughunt-container-name-replica/act-1452-review-r4.md`.
- Review-only: keine Produktdatei geändert, kein Test lokal gestartet, keine Workflow-Datei verändert, kein Rerun/Dispatch und keine Containeroperation ausgeführt.

## Stop-Kriterium

Nicht freigeben, bis `go-unit-tests` und `PR Selected Checks` auf dem korrigierten exakten Kopf erfolgreich sind, Retirement-Renderer-Panics beseitigt sind, der Cross-Project-Negativfall einen echten Produktionsaufruf abdeckt und der Owner den gehosteten Runtime-Selector bei `.github/workflows/ci.yml:349` so ergänzt hat, dass der native pinned Lifecycle-Test auf dem PR-Kopf tatsächlich ausgeführt und bestanden wird. Keine Freigabe allein aufgrund lokaler Tests oder eines übersprungenen Runtime-Gates.

## END

END_BLOCKED 0427-128-r4-review — KORREKTUR; PR #1452 Kopf `48814ecc5e8603f16f4849249fffc9b0c8abd7ab`, Hosted Run `42455350913` terminal failure.
