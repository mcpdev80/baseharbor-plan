# Codex review PR #1286

ROLLE: REVIEW
Zeit: 2026-11-02T12:55:59Z
Reviewer: OpenAI Codex, unabhängige Review-Session (Session-ID und genaue Modellkennung in dieser Umgebung nicht verfügbar; kein Horde-Task zugewiesen).
Urteil: REJECT

Kandidat: ef6a5763e5db6deb96ed783ac5337c1a815830dc; Basis develop: 9a93865a935624045e96a503da0a3a1c2f7d1559. `git ls-remote` bestätigte beide SHAs vor und nach dem Review. Vollständiger PR-Diff via `gh pr diff 1286 --repo mcpdev80/baseharbor` geprüft: nur scripts/pr-gate-plan.py und scripts/test_pr_gate_plan.py.

## Blockierender Befund und Rezept

`scripts/pr-gate-plan.py`, neuer Zweig bei etwa Zeile 1784: `path.startswith('internal/logs/') and path.endswith('.go')` setzt jeden passenden Pfad auf resolved, auch eine beliebige neue, ungetestete Go-Datei oder Datei in einem Unterverzeichnis. Es gibt keine Prüfung, ob die Pakettests die Datei tatsächlich abdecken. Die Kommentare behaupten ausdrücklich das Gegenteil; der neue Test für eine hinzugefügte Datei bestätigt gerade das breite Verhalten. Das verletzt die Vorgaben, Präfix-/Namensheuristik und Coverage-Widening zu vermeiden und unreviewte Pfade fail-closed zu halten. Die drei `LOGS_CHECKS` werden im Diff neu definiert; die Evidence belegt lokale Befehle, aber nicht, dass diese IDs bereits bestehende required validations waren.

Worker-Rezept: in scripts/pr-gate-plan.py eine explizite, fachlich geprüfte Pfadzuordnung für den tatsächlich qualifizierten Scope implementieren, unreviewte/neue und verschachtelte Pfade unresolved lassen, tatsächliche vorhandene Gate-Definitionen und deren Deckung nachweisen und irreführende Kommentare entfernen. In scripts/test_pr_gate_plan.py Regressionen für render.go und beliebige neue sowie verschachtelte Go-Dateien ergänzen; gemischte Diffs müssen unresolved bleiben. Passende Classifier-Tests ausführen und CI sowie Evidence für den neuen SHA erbringen. Stop, falls die fokussierten Checks die konkrete Änderung nicht ausreichend belegen; keine pauschale Paketfreigabe behaupten. Neuer SHA benötigt erneutes unabhängiges Review.

## Übrige Prüfpunkte

- GitHub meldet PR offen, base develop, MERGEABLE; keine Review-Threads. `PR Selected Checks` auf dem Kandidaten SUCCESS, Actions-Run 41446813284, Job 125282919828, App 15368. Fokussierte Python- und Planner-Validierung SUCCESS. Einzelne nicht ausgewählte Jobs skipped.
- Worker-Evidence `logsmap/evidence.md` geprüft: behauptet fail-closed und bestehende Gates, belegt aber nicht die behauptete Begrenzung. PLAN-Punkte 4–9 sind dort weiterhin offen. Grünes CI ersetzt die fehlende inhaltliche Abdeckung nicht.
- Kein Merge durchgeführt. Remote develop blieb 9a93865a935624045e96a503da0a3a1c2f7d1559.
