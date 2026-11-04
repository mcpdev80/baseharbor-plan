# consent-harness-3 — demo PR #128, third correction round (lane w91-demo-r3)

## WAS WIRD ENTWICKELT
Der demobasierte, geführte Candidate-Consent-Flow (baha `init` -> `up` ->
`up --confirm-candidate`) wird fail-closed gemacht: Der Capture-Validator in
`drive.py` muss im Capture-Pfad wirklich Exit-Code und nicht-optionale Regeln
auswerten (nicht über einen frühen Return umgangen werden), ein verpflichtender
READY-Abschlussmarker wird zur Pflichtregel, und der Aufrufer klassifiziert den
Zwischenzustand nur noch am dokumentierten Candidate-Consent-Abbruch (exakter
Fehlertext + Hash + alle Interaktionen). Bei anderem Fehlertext nach Hash
Abbruch, kein zweiter `up`.

## Head / Basis
- Fix-Kandidat (dieser Branch): `138a793ab67ccc0f4cb2d5e8df5976d33453fd60`
- Ziel-Head der Runde (b73be42): `b73be42ba9944d21ffe8869382c37100c3e40384`
- Basis main: `cd9176e0129f01270ca85fd6b29acf99404f6dcd`
- `git ls-remote origin w85-demo-guided-consent`
- PR #128: OPEN, READY (`isDraft=false`), `mergeStateStatus=CLEAN`
- Net-Diff vs `origin/main` (git diff --stat): drive.py + test_consent_capture.py + core.ref (plus revert).

## Änderungen (netter PR #128 Diff gegen main)
- `tests/guided/drive.py` — (1) früher `if capture: return rc, buffer` ENTFERNEN; Validator läuft im Capture-Pfad (Luna review-128b B1). (2) `up_rules`: verpflichtende READY-Regel (non-optional). (3) Aufrufer: non-zero nur als dokumentierter Candidate-Consent-Abbruch (exakter Fehler + Hash + alle Interaktionen), sonst hard abort.
- `tests/guided/test_consent_capture.py` (NEU, permanent, auto-discovered `unittest`) — lunas sechs Fälle + Positivfall; fail-closed bei allen Negativfällen.

## NEGATIV: CI-Workflow zurückgezogen (Owner-Hinweis zweite Abgabe)
- ` .github/workflows/v0424-targeted.yml` wurde URSPRUNGlich geändert, um die Guided-Regression zu registrieren. CI-Territorium ist seit heute owner-seitig festgelegt (ChatGPT-Anweisung); das Write-Set dieser Lane erlaubt die Änderung NICHT.
- Aktion: `git checkout origin/main -- .github/workflows/v0424-targeted.yml` — Änderung zurückgezogen.
- Grund (zur Kenntnis des Owners): der Test `tests/guided/test_consent_capture.py` wurde als ECHTER dauerhafter `unittest`-Test angelegt, der per Standard-`discover -s tests -p test_*.py` gefunden wird; die Workflow-Änderung war nur die Registrierungsmaßnahme. Ohne CI-Territoriums-Änderung läuft der Test als Standard-Discovery mit, sobald die Repo-Konvention `test_*.py` greift. Diese Lane hat die Workflow-Änderung nicht freigegeben — der Owner entscheidet über eine Registrierung.

## Gegenprobe (b)-Fall wortlich nach Luna
`run_tty(..., capture=True)` mit Prozessende `0` und nie erfüllter
Pflichtregel => jetzt ABBRUCH (früher: `rc=0` + `READY reached`). Der
Pflicht-Prompt ist jetzt durch `up_rules` (non-optional) UND den Aufrufer
abgesichert.

## Regressionen (tests/guided/test_consent_capture.py, fail-closed)
1. rc=0 ohne READY-Marker => ABBRUCH (kein READY-PASS)
2. Pflicht-Prompt fehlt => ABBRUCH
3. rc!=0 ohne Hash => ABBRUCH
4. rc!=0 mit Hash aber fremdem Fehlertext => ABBRUCH, kein zweites up
5. rc!=0 mit Hash aber unvollständigen Interaktionen => ABBRUCH
6. dokumentierter consent-abbruch (Hash + exakter Fehlertext + alle Interaktionen) => zweiter lauf => READY
7. regulärer erfolg ohne Hash => READY-Erfolg

## Ergebnisse lokaler Lauf
- `python3 -m py_compile tests/guided/drive.py`: rc=0
- `python3 -m py_compile tests/guided/test_consent_capture.py`: rc=0
- `python3 tests/guided/test_consent_capture.py`: CONSENT-CAPTURE EVIDENCE PASS 7 cases (rc=0)
- `python3 -m unittest discover -s tests/guided -p "test_*.py"`: 7/7 OK (rc=0)
- `bash -n scripts/acceptance.sh`: rc=0
- `git diff --check`: rc=0
- 7/7 Regressionen grün.

## repo-rule compliance (baseharbor-demo/AGENTS.md)
- Tatsächliche Repo-Checks verwendet (py_compile, unittest discover, bash -n).
- Branchfremde PR-CI nicht erfunden (PR #128 auf main: keine PR-Checks laut Repo-Konfiguration, kein Befund).
- Regressions-Test als ECHTER dauertest im Diff (nicht als abgelegtes Evidence-Skript außerhalb des Diffs) — lunas Kritik an 7e972f0 berücksichtigt.
- CI-Workflow-Änderung zurückgezogen (siehe oben) — kein Eindringen in owner-seitiges CI-Territorium.
- Kein Force-Push, keine Branch-Protection-Umgehung.

## Status
END_DONE w91-demo-r3: validator=erreichbar regressions=7/7 | PR #128 netter diff = drive.py + test_consent_capture.py + core.ref.
