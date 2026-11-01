# plan-hygiene — Evidence

Lane: plan-hygiene (worker, Coordinator session 35cdb02e) · Repo: baseharbor-plan
Base: origin/main @ edbf183c69a1034ced0f5d055e18bbc077e7f1ac · Datum: 2026-11-01

Kontext: Wiederholungsauftrag nach vorzeitig beendetem Erstanlauf. Der Owner hat die
Lösung verbindlich präzisiert: in den betroffenen evidence/*.md jede Checkbox-Zeile
`- [ ] `/`- [x] ` zu normalem `- ` (Text beibehalten, nur Checkbox-Tilgung); kein
Präfix-Umformulieren, keine WORKFLOW.md-Änderung, Commit + Push direkt auf main.

## PLAN

1. done — Remote-Stand baseharbor-plan main geholt (origin/main @ edbf183, working tree clean).
2. done — `python3 scripts/plan.py check` reproduziert exakt die 78 Errors in 11 evidence-Dateien (liste unten).
3. done — Checkbox-Tilgung: jede Top-Level-Zeile `- [ ] ` / `- [x] ` in den betroffenen evidence/*.md wurde zu `- ` (Text byte-identisch erhalten). Kein Inhalt, kein Befund, kein SHA verändert; keine Datei außerhalb evidence/ angefasst; scripts/plan.py unverändert.
4. done — `python3 scripts/plan.py render` ausgeführt (rc=0), dann `check`: 0 errors, 339 tasks unverändert.
5. done — Regressionstest-Nachweis: scripts/plan.py + scripts/tests per `git diff --name-only origin/main...HEAD` als UNVERÄNDERT belegt; die Validator-Suite (48 Tests, enthält `test_checkbox_outside_tasks_is_rejected`) läuft grün auf dem Kandidaten. Kein Relaxing der Regel.
6. done — Committed, normaler Push auf origin main (kein Force), push-Referenz verifiziert.

## Files changed (78 checkbox lines, content preserved)

| File | Lines |
| --- | --- |
| evidence/review-A.md | 9 |
| evidence/board-2026-10-31/native-probe/native-probe.md | 9 |
| evidence/board-2026-10-31/ruleset-inventory/INVENTORY.md | 8 |
| evidence/board-2026-10-31/review-nc/PLAN.md | 7 |
| evidence/board-2026-10-31/openbao-cauth/EVIDENCE.md | 7 |
| evidence/board-2026-10-31/dep-1160/todo.md | 7 |
| evidence/board-2026-10-31/dep-1160/evidence.md | 7 |
| evidence/board-2026-10-31/t-openbao-pgauth/EVIDENCE.md | 6 |
| evidence/board-2026-10-31/podman-gh/evidence.md | 6 |
| evidence/board-2026-10-31/gh-dispatch2/gh-dispatch2.md | 6 |
| evidence/board-2026-10-31/docker-endpoint-context/evidence.md | 6 |

Maschinelle Verifikation der Texterhaltung: `git diff -U0` zeilenweise verglichen — jede Addition = `- ` + wortwörtliche Removal-Zeile ohne Marker; 78/78 Übereinstimmung, 0 Mismatches.

## repo-rule compliance

- baseharbor-plan/WORKFLOW.md: "Exactly one checkbox per task note, not indented: the card line" — CardBoard rendert jede Top-Level-Checkbox außerhalb von tasks/ als Karte; Evidence-Dateien tragen daher keine Checkbox-Syntax. Umsetzung = Checkbox-Tilgung, genau diese Konvention.
- Scope-Grenzen der Mission eingehalten: ausschließlich `evidence/**` geändert; scripts/plan.py, tasks/*.md-Frontmatter, Karten-Status/Tags, Produkt-Repos, Coordinator-Skripte: NICHT angefasst. WORKFLOW.md-Ergänzung (Missionsschritt 4) nicht nötig: die Regel steht bereits unverändert in WORKFLOW.md ("Do not use checkboxes here: only the card line above is a checkbox"; check_stray_checkboxes-Regelquelle). Prävention ist damit dokumentiert, keine Validator-Änderung.
- Stop-Kriterium geprüft: kein evidence-Checkbox trägt ein Board-relevantes Tag (`#task|#roadmap|#release/...`) — 0 Treffer; die CardBoard-Boards filtern Allow auf genau diese Tags, evidence/ hat keine Karten-Semantik. Keine Verschiebung nach tasks/ nötig.
- Publishing-Regel (WORKFLOW.md/AGENTS.md): planning updates direkt auf main, kein PR; normaler Push, kein Force-Push. Worktree-Basis origin/main @ edbf183; zur Push-Zeit war remote main unverändert (fetch vor push = ahead 1, keine Rebase nötig).
- Konflikt ecosystem AGENTS.md 4.4 ("## PLAN-Checkliste" in Evidence) vs. Plan-Repo-Regel: dokumentiert; operative Auflösung ist hier die PLAN-Sektion als nummerierte Liste (diese Datei). Empfehlung an Coordinator/Owner: 4.4 als "nummerierte PLAN-Liste" präzisieren.
- Claim: kein Karten-Claim möglich, weil die Mission keine bestehende Karte nennt und das Anlegen einer neuen tasks/-Karte außerhalb des erlaubten Write-Sets (nur evidence/** + WORKFLOW.md) liegt — bewusst nicht angelegt; diese Evidence-Datei ist der Beleg.

## CHECK

Vorab-Realitätsabgleich (dieser Turn): Basis-Check auf origin/main @ edbf183 meldet wörtlich
`339 tasks, 7 epics, 13 releases, 16 decisions; 78 errors, 0 warnings` — reproduziert wie in der
Mission angegeben. Die 11 betroffenen Dateien und ihre Fehlerzahlen stimmen exakt mit der
Missionsliste überein.

### vorher (origin/main @ edbf183, wörtliche Ausgabe)

```
$ python3 scripts/plan.py check
...
error: evidence/review-A.md: checkbox outside tasks/ would become a CardBoard card (line 6)
(78 error-Zeilen, vollständige Liste identisch zur Missionsangabe)
339 tasks, 7 epics, 13 releases, 16 decisions; 78 errors, 0 warnings
```

### nachher (Kandidat, wörtliche Ausgabe)

```
$ python3 scripts/plan.py render
$ python3 scripts/plan.py check
339 tasks, 7 epics, 13 releases, 16 decisions; 0 errors, 0 warnings
```

### render / generated

`python3 scripts/plan.py render` rc=0; Generated-Dateien (views/, roadmap/) unverändert — keine Task-Metadaten berührt: `git diff --stat` zeigt nur die 11 evidence-Dateien (78 insertions, 78 deletions, jeweils Paare).

### Tests (CI-Pfad validate.yml: "Unit tests" + "Validate vault")

```
$ python3 -m unittest discover -s scripts/tests
Ran 48 tests in 0.645s
OK
```

A3-Nachweis: `git diff --name-only origin/main...HEAD` = ausschließlich die 11 evidence-Dateien + diese Datei; scripts/plan.py und scripts/tests/* nachweislich unverändert. Der Regel-Test `test_checkbox_outside_tasks_is_rejected` läuft unverändert grün — Validator bleibt strikt, kein Relaxing.

## Handoff

- Candidate: Commit auf baseharbor-plan main (SHA siehe git log / letzte push-Zeile unten).
- Previous: 78 errors → Current: 0 errors; 339 tasks → 339 tasks.
- Board wieder publizierbar gemäß RUNBOOK 2.5 (check=0).

END plan-hygiene DONE
