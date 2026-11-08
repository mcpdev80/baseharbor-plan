# CODEX-REVIEW 0427-127 r2 — PR #1454

## PLAN

1. Prüfe den aktuellen Kandidaten und den PR-Run SHA-genau gegen die Remote-Refs.
2. Vergleiche den r2-Diff und die neuen Regressionen mit den r1-Befunden und dem Task-Vertrag.
3. Prüfe, ob Fehler beim Paket-Teardown und bei der Orphan-Adoption den CI-Prozess fehlschlagen lassen.
4. Prüfe, ob ein gehosteter CI-Job die neuen Tests unter dem Pull-Request-Trigger tatsächlich auswählt.
5. Veröffentliche das Urteil und die konkreten Korrekturen in dieser Akte.

## Ergebnis

**ROLLE: REVIEW**  
**URTEIL: KORREKTUR (REQUEST-CHANGES)**  
**Kandidat:** PR #1454, `8cadc33a8a6101a2b071bb092176a36b1a699109`  
**Basis:** `develop` `07ae6c3e91b081a189266ca4b162ba705d4aa78f`  
**Hosted run:** `42451808132`, terminal success auf dem exakten Kandidaten

Der Kandidat verbessert die beiden r1-Befunde substanziell. Die Paketbereinigung ist an `TestMain` gebunden statt an ein einzelnes `*testing.T`; das Watcher-Scope ist auf den laufbezogenen Target-/Projekt-Namensraum begrenzt, und die breite `bh-w169-*`-Filterung ist entfallen. Die neuen Paketlebenszyklus-Regressionen decken mehrere Aufrufer, Fehler nach Setup, Panic und Setup-Fehler ab. Diese Punkte reichen noch nicht zur Abnahme, weil die Fehlerpfade keine rote CI erzwingen und der grüne Hosted Run die neuen Tests nicht auswählt.

### Befunde

1. **Teardown-/Adoptionsfehler sind fail-open für den Testprozess.** In `cmd/baha/runtime_integration_test_support_test.go:154-162` schreibt `destroyBootstrapTrustPlaneAtPackageEnd` einen Cleanupfehler nur nach stderr. Der `TestMain`-Defer setzt den Exitstatus von `m.Run()` nicht auf Fehler. Außerdem hängt `destroyBootstrapTrustPlane` an Zeile 311 `os.Remove(marker)` auch dann an den Fehler an, wenn der Destroy an Zeile 303 misslingt; der Marker wird also gerade im Fehlerfall nicht zuverlässig als Retry-Beleg erhalten. Entsprechend ignoriert `adoptBootstrapLeftoverMarkerFromDeadProcess` an Zeile 208 den Rückgabestatus von `destroyOrphanedBootstrapMarkers`; der Helper gibt an Zeilen 234-285 keinen Fehler zurück und protokolliert Konfigurations-, Inventory-, Provider- oder Destroyfehler nur. Danach entfernt der Caller den Marker an Zeilen 212-215. Ein fehlerhafter Cleanup oder eine Adoption kann daher als erfolgreicher Paketlauf enden und den Beleg für verbliebene Ressourcen verlieren. Das widerspricht fail-closed und macht den Guard nicht CI-verbindlich.

   **Lösungsrezept:** In `cmd/baha/runtime_integration_test_support_test.go` Fehler aus der Paket-Teardown bis in `TestMain` propagieren und mit nicht-null Exit beenden, wenn Cleanup nicht erfolgreich war. Die Adoption muss Fehler ebenfalls zurückgeben; Marker erst entfernen, wenn die Zerstörung nachweislich erfolgreich war. Bei nicht lesbarer Konfiguration, unvollständigem Inventory oder nicht auflösbarem Provider Marker erhalten und den Lauf fehlschlagen lassen. Regressionen müssen sowohl den stderr-Text als auch den nicht-null Prozessstatus/erhaltenen Marker bei Cleanup- und Adoption-Fehlern belegen.

2. **Die gehostete PR-CI wählt die neuen Tests nicht aus.** Für die Paketregressionen dokumentiert `round-2.md` unter OWN-BLOCK 2, dass keine Selector-Gruppe des `PR · Validation · cli-package-tests` die 13 `TestBootstrap*`-Tests auswählt. Dafür fehlen ein Selector-Eintrag im `scripts/validation-owner.sh`-Fall `cli-package-tests` und die entsprechende Auswahl in der PR-Matrix in `.github/workflows/ci.yml` (round-2 nennt etwa Zeilen 759-875). Zusätzlich begrenzt der Runtime-Integrationsschritt in `.github/workflows/ci.yml:342-349` sein Muster auf fünf benannte Tests; `TestBootstrap*` fehlt. Der umgebende `validate`-Job ist an `.github/workflows/ci.yml:255-256` für Pull Requests ausgeschlossen. Der erfolgreiche Run `42451808132` ist daher kein Nachweis, dass die neuen Paketlebenszyklus-Tests auf PRs ausgeführt wurden; die Evidence `round-2.md` dokumentiert selbst beide Auswahl-Lücken und den Owner-Block. Die neue Testabdeckung ist so noch nicht dauerhaft durch den Pull-Request-CI-Trigger abgesichert.

   **Lösungsrezept:** Owner-Änderung an `.github/workflows/ci.yml:255-256` und `:342-349`, damit ein geeigneter PR-Job die relevanten Runtime-Integrationstests mit den erforderlichen Runtime-Variablen ausführt; das Laufmuster muss die relevanten Tests enthalten und Skips dürfen nicht als grüner Nachweis gelten. Zusätzlich muss die CI-Testauswahl über `scripts/validation-owner.sh` im Fall `cli-package-tests` die neuen Bootstrap-Regressionen aufnehmen und die PR-Matrix muss diese Selector-Gruppe ausführen. Workflow- und Matrix-Dateien sind Owner-Scope; ich habe sie nicht geändert und keinen Lauf ausgelöst. Der Owner muss die Trigger-/Selector-Änderung ausführen. Danach muss ein echter PR-Lauf auf dem korrigierten Kandidaten die betreffenden Tests sichtbar ausführen und grün beenden; ein Skip oder lokaler Lauf genügt nicht.

### Stop-Kriterium

Nicht freigeben, bis Paket-Teardown und Orphan-Adoption bei Cleanupfehlern den Prozess fehlschlagen lassen, der Marker bei erfolgloser Adoption erhalten bleibt, und ein gehosteter Pull-Request-Job die neuen Regressionen tatsächlich ausführt und besteht. Keine Freigabe allein aufgrund des derzeit grünen, aber nicht abdeckenden Runs.

## Evidence / repo-rule compliance

- Kandidatenkopf und PR-Run wurden SHA-genau geprüft; der Kandidat blieb unverändert.
- Remote-Zeuge: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1454/head` meldete `07ae6c3e91b081a189266ca4b162ba705d4aa78f refs/heads/develop` und `8cadc33a8a6101a2b071bb092176a36b1a699109 refs/pull/1454/head`.
- `gh run view 42451808132 --repo mcpdev80/baseharbor --json headSha,status,conclusion` meldete `headSha=8cadc33a8a6101a2b071bb092176a36b1a699109`, `status=completed`, `conclusion=success`.
- `git diff develop...8cadc33a8a6101a2b071bb092176a36b1a699109` betrifft ausschließlich die zwei in `round-2.md` beschriebenen Testdateien unter `cmd/baha/`; keine Produktionsdatei und kein Workflow wurde geändert.
- Keine Produkt-Tests, Containerläufe, CI-Reruns oder Workflow-Dispatches wurden gestartet.
- Hosted Run `42451808132`: terminal success auf `8cadc33a8a6101a2b071bb092176a36b1a699109`; dessen PR-Testauswahl deckt die neuen `TestBootstrap*`-Tests nicht ab.
- Planning-Repo: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`, Remote `https://github.com/mcpdev80/baseharbor-plan.git`.

## END

END 0427-127-r2-review BLOCKED — Korrektur erforderlich; Kandidat `8cadc33a8a6101a2b071bb092176a36b1a699109`.
