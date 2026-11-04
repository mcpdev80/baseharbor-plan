# consent-harness-4 — demo PR #128, fourth correction round (lane w100-demo-r4)

## END
END_DONE w100-demo-r4: head=061be773dd testtraegt=production-pfad gegenproben=4 lsremote=061be773dd | Der Dauer-Test importiert drive und misst alle vier Gegenproben gegen drive.run_guided_consent_flow mit production up_rules; fremder Fehler erreicht keinen zweiten Lauf, rc=0 nur mit READY, dokumentierter Abort erreicht zweiten Lauf.

## WAS WIRD ENTWICKELT
Der demobasierte, geführte Candidate-Consent-Flow (baha `init` -> `up` ->
`up --confirm-candidate`) bekommt einen Dauer-Regressionstest, der nun GEGEN den
ECHTEN production decision path von `drive.up_rules` misst — nicht mehr gegen die
test-lokalen Kopien `complete_rules()`/`TWO_PROMPT_RULES`. Damit ist sicherge-
stellt, dass ein fremder Fehler im Produktionspfad NIE einen zweiten `up`
auslöst (fail-closed), dass ein normaler rc=0-Lauf NUR mit READY-Pass wird und
der dokumentierte Candidate-Consent-Abbruch den echten zweiten Lauf erreicht.

## Head / Basis
- Fix-Kandidat (dieser Branch): `061be773ddb7168aa2760afc9bb8cba18421fd93`
- Basis main (aktuell, unveraendert): `cd9176e0129f01270ca85fd6b29acf99404f6dcd`
- `baseharbor-core.ref` unveraendert auf `488a39e6f67ecbc733dc6acdee2443b36db4717c` (Luna-kritik verlangt keine Aenderung; Net-Diff vs main laeuft ueber die Round-3-Aenderung des Branches).
- `git ls-remote origin w85-demo-guided-consent` => `061be773ddb7168aa2760afc9bb8cba18421fd93`
- PR #128: OPEN, non-draft, mergeable.
- Net-Diff vs origin/main = EXAKT 3 Dateien: `baseharbor-core.ref` (M, seit Round 3 unveraendert), `tests/guided/drive.py` (M), `tests/guided/test_consent_capture.py` (A). demo/consent-harness-3.md NICHT im PR-Diff.

## Änderungen (netter PR #128 Diff gegen main)
- `tests/guided/test_consent_capture.py` — COMPLETE_RULES/TWO_PROMPT_RULES ENT-
  RENNEN; stattdessen die IMPORTIERTE `drive.up_rules` (Modulkopie) als Pflicht-
  regel-set. Echter production decision path wird aufgerufen: first_rc /
  feature-detection / hash-auswertung / Abort->zweiter-Lauf sequenz. VIER
  gegenproben messen ALLE gegen den ECHTEN decision path. Assertion: fremder
  Fehler erreicht NIE einen zweiten Lauf.
- `tests/guided/drive.py` — unveraendert (production path ist bereits fail-closed;
  nur der TEST wurde von der lokalen zur Produktions-Grundlage verschoben).
- `baseharbor-core.ref` — unveraendert.

## TEST-Struktur (production pfad statt test-lokal)
- `import drive`; verwendet `drive.up_rules` (referenzielle Kopie des Moduls,
  keine syntaktischen Kopie).
- Aufruf des echten guided-flow callers + feature probe / second-run branch.
- VIER gegenproben:
  1. rc=0 ohne READY-marker => ABORT (production up_rules: mandatory READY).
  2. required prompt fehlt => ABORT (production mandatory-READY coverage).
  3. rc!=0 + hash + FOREIGN error => ABORT, kein zweiterlauf (production path).
  4. rc!=0 + hash + unvollstaendige interaktion => ABORT (production coverage).
- Assertion im productionpfad: foreign error -> NEVER second up.

## Regressionen (tests/guided/test_consent_capture.py, fail-closed)
1. rc=0 ohne READY-Marker => ABBRUCH (kein READY-PASS)
2. Pflicht-Prompt fehlt => ABBRUCH
3. rc!=0 ohne Hash => ABBRUCH
4. rc!=0 mit Hash aber fremdem Fehlertext => ABBRUCH, kein zweites up
5. rc!=0 mit Hash aber unvollstaendigen Interaktionen => ABBRUCH
6. dokumentierter consent-abbruch (Hash + exakter Fehlertext + alle Interaktionen) => zweiter lauf => READY
7. regulärer erfolg ohne Hash => READY-Erfolg

## Ergebnisse lokaler Lauf
- `python3 -m py_compile tests/guided/drive.py`: rc=0
- `python3 -m py_compile tests/guided/test_consent_capture.py`: rc=0
- `python3 tests/guided/test_consent_capture.py`: CONSENT-CAPTURE EVIDENCE PASS 8 cases (rc=0)
- `python3 -m unittest discover -s tests/guided -p "test_*.py"`: 8/8 OK (rc=0)
- `git diff --check`: rc=0
- 8/8 Regressionen/Assertionen gruen (7 Luna-Faelle + foreign_error_second_up-Assertion).

## repo-rule compliance (baseharbor-demo/AGENTS.md)
- Tatsächliche Repo-Checks verwendet (py_compile, unittest discover, git diff --check).
- PR-Diff vs origin/main EXAKT 3 Dateien: drive.py (M), test_consent_capture.py (A), baseharbor-core.ref (M, unveraendert).
- demo/consent-harness-3.md (demo-zweig) NICHT im PR-Diff (nur drive.py+test+core.ref).
- CI-Workflow-Änderung NICHT gemacht (owner-seitiges CI-Territorium; nicht im Write-Set dieser Lane).
