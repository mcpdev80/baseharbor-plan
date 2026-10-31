## PLAN
✔ Schritt 0: Richtlinien und Auftrag gelesen; natives TodoWrite ist in dieser Sitzung nicht verfügbar.
✔ #1225: Run und Logs forensisch geprüft.
✔ #1220: Plan-Artefakt, Job-Inventar und Verifier geprüft.
✔ #1226: Logs und gemeinsame Dateien geprüft.
✔ #1229: Selected-Checks-Fehler geprüft.
✔ Trusted-Base-Code und mögliche Bootstrap-Wirkung geprüft.
☐ Evidence-Push: blockiert; Datei liegt außerhalb des Plan-Repos, und diese Diagnose erteilt keine Erlaubnis, ein anderes Ziel zu ändern oder Git-Metadaten außerhalb des freigegebenen Bereichs zu schreiben.

## Diagnose

Alle vier PR-Heads und alle folgenden Run-IDs wurden über GitHub API überprüft. develop steht auf 72ba7a99ff7dcd4b04ee3cf16516991ef567d376. Logzeilen unten sind Zeilen der direkt über `gh api .../actions/jobs/<id>/logs` geladenen Dateien; #1226-Logs wurden mit `gh run view --log` geladen.

### #1225 — 5060cb23
[PR Selected Checks, Run 41113767536, Job 124263543045](https://github.com/mcpdev80/baseharbor/actions/runs/41113767536/job/124263543045), Log `d25-124263543045.log:232`: `coverage-unresolved`: native Qualifizierung für `.github/workflows/ci.yml`, `.github/workflows/podman-acceptance.yml` und spezifische Qualifizierung für `scripts/pr-check-runner.py` fehlen. Die fünf Validation-Matrix-Jobs waren erfolgreich; diese ersetzen die fehlende native/Executor-Qualifikation nicht. Der Kandidat ergänzt daneben die vier Resolver-IDs im Executor-Registry, die im aktuellen develop fehlen (siehe #1220).

[Targeted runtime docker, Run 41113763606, Job 124262557169](https://github.com/mcpdev80/baseharbor/actions/runs/41113763606/job/124262557169) ist ein separater Push-Run auf `runtime-validation/ha/control-plane/both/750-reg`, nicht ein PR-Run; darum läuft ein native Test trotz reinem CI-Diff. Log `d25-124262557169.log:2-3` belegt Hosted Compute Agent, `:263-266` Gate control-plane und docker, `:309-314` den echten Testfehler: `runtime_restart_integration_test.go:25`, Docker endpoint `unix:///run/user/1001/docker.sock` ohne verifizierbare daemon identity. Dies ist ein ausgeführter Testfehler unter einem ungeeigneten/nicht verifizierten Runtime-Endpunkt; das Log belegt keinen Produktregressionsnachweis. Nächster Schritt: Routing und isolierten Rootless-Runner mit validierter Daemon-Identität prüfen; erst dann relevante, explizit begründete Qualifikation ausführen und deren Authentizität/Kompatibilität belegen. Kein Skip gilt als Erfolg.

### #1220 — 5d5b5c30
[Run 41125285701, Job 124303300472](https://github.com/mcpdev80/baseharbor/actions/runs/41125285701/job/124303300472), `d25-124303300472.log:225-235`: generisches `missing or duplicate required Actions job`, nennt keinen Job. Authentifiziertes Plan-Artefakt 13009713144 verlangt acht `PR · Validation · <id>` Jobs; die API-Liste enthält keinen einzigen davon. Die vier Resolver-IDs `resolver-consumer-build`, `resolver-gofmt`, `resolver-package-tests`, `resolver-vet` fehlen in develop `scripts/pr-check-runner.py:90-98`; `:212-218` verwirft jede unbekannte ID. Trusted-Plan-Job 124302019381 Log `:300-308` zeigt `ValueError: unsupported validation check`. Verifier `scripts/pr-authenticated-results.py:20-22,42-48` verlangt genau einen Job pro ID und meldet nur generisch. Kein Duplikat belegt. Der konkrete Auslöser ist die Executor-Registratur-Lücke, die #1225 in seinem Diff adressiert. Nächster Schritt: nach qualifiziertem Bootstrap frischen Plan und vollständige erforderliche Validierung für den tatsächlichen Kandidaten laufen lassen; keine Erfolgsgarantie aus dem Merge allein ableiten.

### #1226 — d2fc3432
[Selected Checks Run 41081616567, Job 124153363443](https://github.com/mcpdev80/baseharbor/actions/runs/41081616567/job/124153363443), `d25-124153363443.log:224`: coverage-unresolved für `ci.yml`, `pr-check-runner.py`, `pr-receipt-enforcement-check.py`. [validate Run 41083351842, Job 124157971824](https://github.com/mcpdev80/baseharbor/actions/runs/41083351842/job/124157971824) ist ein separater Push auf `runtime-validation/ci/pr-gate/1226`: `d25-124157971824.log:686-703` zeigt vier fehlgeschlagene Integrationstests, weil der gewählte rootless Docker-Socket nicht verfügbar ist; ein weiterer Test skipped. Kein Nachweis einer Produktregression. #1225 und #1226 ändern beide `.github/workflows/ci.yml`, `scripts/pr-check-runner.py`, `scripts/pr-gate-plan.py` und `scripts/test_pr_gate_plan.py`. Reihenfolge: zuerst unabhängig prüfen und die Bootstrap-Lücke qualifizieren, erst nach zugelassener Integration #1226 auf aktuelle Basis integrieren, überlappende Änderungen prüfen und gezielt neu qualifizieren. Wegen Maintainer-Pause keine Integrationsarbeit hier.

### #1229 — df1c9dac
[Run 41102396309, Job 124268282805](https://github.com/mcpdev80/baseharbor/actions/runs/41102396309/job/124268282805), `d25-124268282805.log:226-227`: `coverage-unresolved` für `internal/capability/lifecycle.go`, `service_binding.go`, `service_binding_test.go` und zusätzlich `missing required gate: integration/static/public-contracts`. Das ist weder belegter base.sha- noch Wizard-Fact-Fehler. Nächster Schritt: betroffene Capability-Wirkung und benötigtes statisches Vertrags-Gate anhand vertrauenswürdiger registrierter Evidence qualifizieren und dann aktuellen Kandidaten erneut prüfen.

### Trusted base und Grenzen
Die develop-Kopie `scripts/pr-gate-plan.py:1438-1447` klassifiziert nicht ausdrücklich sichere Capability-Dateien als unresolved; `:1512-1525` unterscheidet registrierte Planning-Skripte von ungelösten Workflow-/Executor-Änderungen. `scripts/pr-check-runner.py:90-98,212-218` verlangt registrierte IDs. Der #1225-Diff ergänzt die vier Resolver-Executor-IDs: die konkret nachgewiesene #1220-Registraturlücke kann nach Integration dieser Änderung auf trusted develop verschwinden, aber die erforderlichen Checks müssen danach tatsächlich bestehen. Ein #1225-Merge allein beweist weder die geforderte Qualifikation von #1225/#1226 noch behebt er die Socket-Verfügbarkeit; #1229-Capability-Unresolved und das fehlende Public-Contracts-Gate sind ebenfalls nicht durch die gezeigten Änderungen als behoben belegt. Für jeglichen tatsächlichen Merge gelten alle unabhängigen Review-, Evidence- und CI-Gates sowie die Maintainer-Pause.

END codex-d25 BLOCKED natives TodoWrite nicht verfügbar; Evidence-Push nicht durchgeführt

END codex-d25 DONE
