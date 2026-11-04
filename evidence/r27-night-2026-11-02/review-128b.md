# PR #128 Abschlussreview — Korrekturrunde b73be42

ROLLE=REVIEW, kein Merge. **Urteil: REJECT.** Reviewer Codex GPT-6 Luna. Karte `t-20261104-r27-demo-guided-consent`. Geprüfter Head `b73be42ba9944d21ffe8869382c37100c3e40384`, tree `d65427166f6413635910149e39b18b17d50bba96`; base `main` `cd9176e0129f01270ca85fd6b29acf99404f6dcd`; merge-base `9493e82faa66ade9c4bacbdb2c269d1f065adf39`. GitHub API und `git ls-remote` bestätigten vor der Prüfung den exakten Head und Base. PR #128 ist OPEN, READY (`draft=false`), CLEAN/MERGEABLE. GitHub weist genau zwei PR-Dateien aus: `tests/guided/drive.py` und `baseharbor-core.ref`; der Pin bleibt auf dem in der Karte begründeten `488a39e6f67ecbc733dc6acdee2443b36db4717c`.

Der demo-spezifische Checkhinweis ist berücksichtigt: [.github/workflows/v0424-targeted.yml](/home/marcel/dev/baseharbor-ecosystem/baseharbor-demo/.github/workflows/v0424-targeted.yml) wird nur bei Push auf Release-Branches ausgelöst. Für PR #128 auf `main` gibt es gemäß Repo-Konfiguration keine PR-Checks; `gh pr checks` meldete keine. Das ist hier kein Befund.

## Eigene Gegenproben

Die getestete `drive.py` stimmt bytegenau mit der Version in Head `b73be42` überein. Gegenproben liefen isoliert mit temporärem Artefaktverzeichnis und Kindprozessen; der Kandidat blieb unverändert.

- **(a) Exit != 0 ohne Hash:** Prozessende `7`, kein Hash. Der Aufrufer bricht wegen `first_rc != 0` und fehlendem Hash ab. **PASS**.
- **(b) Pflicht-Prompt fehlt:** Prozessende `0`, erforderliche Regel nie erfüllt. `run_tty(..., capture=True)` kehrt dennoch normal mit `rc=0` zurück; der Aufrufer sieht keinen Hash und läuft bis zur Meldung `READY reached`. **FAIL**. Der reale `up_rules`-Satz markiert zudem alle Regeln als optional und enthält keinen verpflichtenden READY-Abschlussmarker.
- **(c) Binary fehlt:** Probe liefert `False`; genau ein Probe-Aufruf, kein Supportsignal. Der Aufrufer wirft vor einem zweiten `up`. **PASS**.
- **(d) Exakte Unsupported-Antwort:** `unknown option --confirm-candidate` liefert `False`; genau ein Probe-Aufruf, kein zweiter `up`. **PASS**.
- Zusätzliche B2-Gegenproben: Timeout und unbekannte Fehlermeldung liefern ebenfalls `False`, je ein Probe-Aufruf. **PASS**.
- **Zusatzprobe B1:** Ein nicht-zero Prozess mit Hash im Transcript, aber einer anderen Fehlermeldung, wird nicht als unerwarteter Fehler abgewiesen: der Call-Site prüft nur „Hash vorhanden“ und würde bei erfolgreicher Capability-Probe den zweiten `up` ausführen. **FAIL**.

## Befund und Rezept

1. **B1 ist weiterhin nicht geschlossen; der Capture-Validator ist unerreichbar.** In `tests/guided/drive.py:261-262` kehrt `if capture: return rc, buffer` vor dem neuen Block zurück, der Exit-Code und fehlende nicht-optionale Regeln prüfen soll (`:270-294`). Dadurch passiert Gegenprobe (b). Außerdem sind alle Regeln in `up_rules` optional; der Guided-Aufrufer hat keine zwingende READY-Abschlussregel und gibt nach erfolgreichem `rc=0` ohne Hash stets `READY reached` aus. Der fehlende Pflicht-Prompt ist somit im tatsächlichen Aufruf weder durch `run_tty` noch durch den Aufrufer abgesichert. Zusätzlich erlaubt der Aufrufer bei `first_rc != 0` jeden Fehlertranscript mit einem gefundenen Hash als Zwischenzustand; er prüft nicht, ob der Abbruchgrund tatsächlich der dokumentierte Candidate-Consent-Refusal war. Bei anderem Fehler nach Hash-Ausgabe läuft er nach positiver Probe in den zweiten `up`-Versuch.

   Die Lane-Evidence `tests/guided/scripts/evidence_b1_b2.py` (Commit `7e972f0`, nicht Teil des PR-Diffs) belegt B2, aber nicht B1: Regression 1 prüft nur, dass `run_tty` `rc=7` zurückgibt, statt den behaupteten Abbruch am Aufrufer zu prüfen. Regression 2 verwendet ebenfalls `rc=7`, sodass der Aufrufer wegen „non-zero ohne Hash“ abbricht, unabhängig davon, ob fehlende Regeln validiert werden. Regression 3 bestätigt nur `rc=0` mit erfüllter Beispielregel; Regression 4 verwendet keinen Hash und beweist keinen erlaubten Candidate-Abbruch.

   **Rezept:** den frühen Capture-Return entfernen und den Validator tatsächlich ausführen. Für `up` einen expliziten, aus dem Core-Transcript stammenden READY-Erfolgsmarker verlangen. Den einzigen erlaubten non-zero Zwischenzustand als bekannten Candidate-Consent-Abbruch anhand der konkreten erwarteten Fehlerausgabe, extrahiertem Hash und vollständig erfüllten notwendigen Interaktionen klassifizieren; einen beliebigen anderen Fehler trotz Hash abbrechen. Die Regressionen am Aufrufer-/Guided-Flow testen: `rc=0` ohne READY-Marker, Pflicht-Prompt fehlt, `rc!=0` ohne Hash, `rc!=0` mit Hash aber unbekanntem Fehlertext, `rc!=0` mit Hash aber unvollständigen Interaktionen sowie dokumentierter Consent-Abbruch und regulärer READY-Erfolg. Assertieren, dass bei allen Negativfällen weder zweites `up` noch `READY reached`/PASS ausgegeben wird. **Stop-Kriterium:** jede fehlende Pflichtbedingung oder unerwartete Completion muss den Flow fail-closed beenden.

## Checks und Kandidatenintegrität

- Eigene B1/B2-Gegenproben: B1-(a) PASS, B1-(b) FAIL; B2 fehlendes Binary, Timeout, unbekannte Ausgabe und exakte Unsupported-Antwort PASS.
- Python-Syntaxprüfung von `drive.py`: PASS. `bash -n scripts/acceptance.sh`: PASS. `git diff --check` für die Korrekturrunde: PASS.
- `baseharbor-demo/AGENTS.md` verlangt die tatsächlichen Repo-Checks; keine branchfremde PR-CI erfunden oder als fehlend gewertet.
- Nachprüfung der Remote-Refs: PR-Head `b73be42ba9944d21ffe8869382c37100c3e40384`, `main` `cd9176e0129f01270ca85fd6b29acf99404f6dcd`; keine Änderung am Kandidaten.

## END

END_DONE codex-r128b: verdict=REJECT open=1 | B2 ist fail-closed; B1 bleibt offen, weil der Capture-Validator unerreichbar ist und ein fehlender READY-Prompt als Erfolg durchgeht.
