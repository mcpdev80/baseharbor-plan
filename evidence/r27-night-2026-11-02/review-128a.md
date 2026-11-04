# PR #128 Abschlussreview — guided consent harness

ROLLE=REVIEW, kein Merge. **Urteil: REJECT.** Reviewer Codex GPT-6 Luna. Karte `t-20261104-r27-demo-guided-consent`. Geprüfter Head `683f1da7c5b67d71c25956252bade4af10c6e1f1`, tree `02dc8b598edae86a0832e0b4467c021c5af2d0e9`; `main` `cd9176e0129f01270ca85fd6b29acf99404f6dcd`. Vor und nach der Prüfung bestätigten `git ls-remote` und GitHub API dieselben Heads. PR #128 ist OPEN, READY (draft=false), CLEAN/MERGEABLE. Kandidat unverändert.

## Scope und Vertrag

GitHub PR-Dateiliste (merge-base `9493e82faa66ade9c4bacbdb2c269d1f065adf39`): `tests/guided/drive.py` und `baseharbor-core.ref`. Das passt zum erlaubten Harness-Write-Set und der bedingten Pin-Ausnahme. Der Pin ist exakt `488a39e6f67ecbc733dc6acdee2443b36db4717c`, wie in Task und `consent-harness-1.md` begründet. Kein Core-Datei-Write. Die drei zusätzlichen Unterschiede einer direkten Baum-Gegenüberstellung `cd9176e..683f1da` stammen aus der Branch-Basis, die hinter `main` liegt; sie sind nicht Teil der von GitHub ausgewiesenen PR-Dateiliste.

## Befunde und Rezept

1. **Capture überspringt Fehler- und Interaktionsprüfung des ersten `up`.** In `tests/guided/drive.py`, `run_tty` (Capture-Zweig nach Prozessende) gibt `capture=True` unmittelbar `(rc, buffer)` zurück, bevor `expected_returncodes` und nicht-optionale `rules` geprüft werden. Der Aufrufer speichert `first_rc`, wertet es aber nicht aus; falls kein Hash gefunden wird, läuft er direkt zur Meldung `READY reached`. Damit wird auch ein beliebiger Fehler ohne Hash oder ein Lauf ohne erwartete Interaktionen als erfolgreich ausgegeben. Unabhängige Gegenprobe mit demselben `run_tty`: Kindprozess Exit 7, erforderlicher Prompt fehlt; Capture kehrte normal mit `rc=7` zurück (**FAIL**). **Rezept:** Capture muss die erwarteten Prompt-Regeln weiterhin validieren und den Exit-Status auswerten. Nur den dokumentierten Candidate-Consent-Abbruch mit vollständig abgearbeiteten Interaktionen und extrahiertem Hash als ersten, erwarteten Zwischenzustand zulassen; den normalen Erfolgspfad ohne Hash nur bei erwarteten Exit-/Ready-Bedingungen akzeptieren. Bei sonstigem Exit oder fehlenden Bedingungen abbrechen. Regressionen für Exit!=0 ohne Hash, fehlenden Pflicht-Prompt, normalen Erfolg ohne Hash sowie den erwarteten Consent-Abbruch mit Hash ergänzen. Stop-Kriterium: kein `READY reached` und kein PASS bei einem beliebigen unerwarteten Exit oder fehlenden Pflicht-Prompt.

2. **Unklare Probe-Ergebnisse gelten als Feature-Support.** `binary_supports_confirm_candidate` gibt bei `OSError` und Timeout `True` zurück und klassifiziert jeden Prozessausgang als unterstützt, solange die konkrete Zeichenfolge `unknown option --confirm-candidate` fehlt. Ein fehlendes/defektes Binary, Timeout oder eine andere frühe Fehlermeldung ist kein positiver Support-Nachweis. **Rezept:** Support nur bei positivem, eindeutigem Merkmal bestätigen; die bekannte Unsupported-Antwort gezielt als „nicht unterstützt“ behandeln und andere Probe-Fehler fail-closed als Fehler/unklar ausgeben. Gegenproben: Binary fehlt, Timeout, unbekannte Fehlermeldung und exakte Unsupported-Antwort. Keine zweite `up`-Ausführung nach unklarem Probe-Ergebnis.

## Checks und Evidence

- PR checks: GitHub meldete `no checks reported` für den Branch.
- `python` Syntaxprüfung für `tests/guided/drive.py`: PASS. `bash -n scripts/acceptance.sh`: PASS. Demo-Fixture-Consent-Tests: `python3 -m unittest discover -s tests -p test_fixture_consent.py`, 4 PASS.
- Die vorhandene `consent-harness-1.md` dokumentiert den erfolgreichen Hash-Transport bis zum Apply auf dem gepinnten Core, danach aber einen Abbruch am OpenBao-Manager-Auth-Readiness-Gate. Sie ist kein grüner vollständiger Guided-Acceptance-Lauf. Die Detection-False-Zeile in der Matrix ist eine beschreibende Behauptung; kein separater ausführbarer Lauf/Artefakt dafür liegt bei.
- `up --help` wird nicht zur Detection verwendet; der Harness nutzt eine Verhaltensprobe und begründet dies mit der dort fehlenden Flag-Auflistung. Die Kartenanforderung und diese Abweichung müssen bei der Korrektur konsistent belegt werden.

## END

END_DONE codex-r128a: verdict=REJECT open=1,2 | Capture kann beliebige Fehler als READY melden; Probe-Fehler werden als Support fehlklassifiziert. Gegenproben und fokussierte Syntax-/Fixture-Checks dokumentiert; kein Merge.
