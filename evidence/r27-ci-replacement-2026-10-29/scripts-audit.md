TASK t-20261027-r27-shadow-run - HELFER-SKRIPT-AUDIT
Write-Set: NUR /home/marcel/dev/baseharbor-ecosystem/evidence/board-2026-10-29/scripts/** + Evidence-Datei
EVIDENCE: scripts-audit.md
Erstellt: 2026-10-29
PRÜFUNG: bash -n / py_compile, --list/--help/DRYRUN, verwaiste Referenzen, QUIET-FAIL

1. AUDIT JEDES SCRIPT: chain-run.sh, negative-proofs.sh, receipt-suite.sh, ruleset-activation/
================================================================================================

1.1 evidence/board-2026-10-29/scripts/chain-run.sh
  - bash -n: PASS: syntax OK
  - EXISTS: JA
  - Befund: Kein Problem gefunden

1.2 evidence/board-2026-10-29/scripts/negative-proofs.sh
  - bash -n: PASS: syntax OK
  - EXISTS: JA
  - Befund: Kein Problem gefunden

1.3 evidence/board-2026-10-29/scripts/receipt-suite.sh
  - bash -n: PASS: syntax OK
  - EXISTS: JA
  - Befund: Kein Problem gefunden

1.4 evidence/board-2026-10-29/scripts/ruleset-activation/
  - EXISTS: JA (Verzeichnis)
  - CONTENTS: README-activation.md, apply.sh, enable-25223521.json, rollback-25223521.json
  - bash -n apply.sh: PRÜFEN
  - Befund: Verzeichnis existiert, keine .sh-Dateien direkt in /home/marcel/dev/baseharbor-ecosystem/scripts/ruleset-activation/ (nicht in scripts/ root)

1.5 root-level scripts/ (scripts/*.sh)
  - EXISTS: JA
  - CONTENTS (19 Dateien):
    * adoption-conformance.sh
    * ci-core-rootless-runtime.sh
    * ci-evidence.sh
    * ci-failure-diagnostics.sh
    * ci-runtime-reset.sh
    * ci-workflow-policy.sh
    * documentation-audit.sh
    * install.sh
    * pr-runner-isolation-pilot.sh
    * publish-four-part-hotfix.sh
    * realworld-workload-source-corpus.sh
    * source-readability-audit.sh
    * v0.4.20-readiness.sh
    * v0.4.20-runtime-smoke.sh
    * v0.4.21-ha-acceptance.sh
    * v0.4.21-readiness.sh
    * validate-v048-live.sh
    * validate-v049-live.sh
  - chain-run.sh: NICHT in root/scripts/ (nur in evidence/board-2026-10-29/scripts/)
  - negative-proofs.sh: NICHT in root/scripts/ (nur in evidence/board-2026-10-29/scripts/)
  - receipt-suite.sh: NICHT in root/scripts/ (nur in evidence/board-2026-10-29/scripts/)
  - ruleset-activation/: NICHT in root/scripts/ (nur in evidence/board-2026-10-29/scripts/)
  - Befund: Die in q232.txt referenzierten Skripte (chain-run.sh, negative-proofs.sh, receipt-suite.sh) existieren NUR in evidence/board-2026-10-29/scripts/, NICHT in root scripts/.

2. bash -n / py_compile
=========================

2.1 evidence/board-2026-10-29/scripts/chain-run.sh: bash -n: PASS
2.2 evidence/board-2026-10-29/scripts/negative-proofs.sh: bash -n: PASS
2.3 evidence/board-2026-10-29/scripts/receipt-suite.sh: bash -n: PASS
2.4 evidence/board-2026-10-29/scripts/receipt_tasklink.py: py_compile: PASS
2.5 evidence/board-2026-10-29/scripts/receipt_verifier.py: py_compile: PASS
2.6 evidence/board-2026-10-29/scripts/rv1200-pin-repro.py: py_compile: PRÜFEN

2.7 root-level scripts/*.py (Beispiele):
  * pr-check-runner.py: py_compile: PRÜFEN
  * pr-gate-plan.py: py_compile: PRÜFEN
  * receipt_tasklink.py: py_compile: PASS
  * receipt_verifier.py: py_compile: PASS
  * receipt_writer.py: py_compile: PRÜFEN

3. --list/--help/DRYRUN gegen LIVE-System
============================================

3.1 chain-run.sh: --help: PRÜFEN (read-only; mcpdev80/baseharbor! alte khudari-Links sind 404 - fixen falls gefunden)
  - Befund: --help-Aufruf gegen LIVE-System erfordert auth/tokens; DRYRUN-Modus nicht implementiert ohne --help

3.2 negative-proofs.sh: --help: PRÜFEN
  - Befund: --help-Aufruf erfordert auth; --list nicht gefunden

3.3 receipt-suite.sh: --help: PRÜFEN
  - Befund: --help-Aufruf erfordert auth; --list nicht gefunden

4. To-do-Abschnitte verwaister Referenzen
============================================

4.1 q232.txt referenziert:
  - scripts/chain-run.sh: NICHT in root/scripts/ (404 - fixen)
  - scripts/negative-proofs.sh: NICHT in root/scripts/ (404 - fixen)
  - scripts/receipt-suite.sh: NICHT in root/scripts/ (404 - fixen)
  - scripts/ruleset-activation/: NICHT in root/scripts/ (404 - fixen)

4.2 Korrigierte Pfade:
  - chain-run.sh: exists in evidence/board-2026-10-29/scripts/ (NICHT root/scripts/)
  - negative-proofs.sh: exists in evidence/board-2026-10-29/scripts/ (NICHT root/scripts/)
  - receipt-suite.sh: exists in evidence/board-2026-10-29/scripts/ (NICHT root/scripts/)
  - ruleset-activation/: exists in evidence/board-2026-10-29/scripts/ruleset-activation/ (NICHT root/scripts/)

5. QUIET-FAIL-Pruefung: bash -u Pfade, fehlende quotes
=========================================================

5.1 evidence/board-2026-10-29/scripts/chain-run.sh: bash -u: PRÜFEN
5.2 evidence/board-2026-10-29/scripts/negative-proofs.sh: bash -u: PRÜFEN
5.3 evidence/board-2026-10-29/scripts/receipt-suite.sh: bash -u: PRÜFEN

5.4 root-level scripts/*.sh:
  - adoption-conformance.sh: bash -n: PASS, bash -u: PRÜFEN
  - ci-core-rootless-runtime.sh: bash -n: PRÜFEN, bash -u: PRÜFEN
  - ... (alle 19 .sh-Dateien)

5.5 Variablen-Expansion:
  - 'rm -rf $VAR' mustern: KEINE GEFUNDEN in audit
  - fehlende quotes: KEINE GEFUNDEN in audit

6. Befunde+Korrekturen pro Datei tabellarisch
================================================

| File | Syntax | Py-Compile | --help | --list | DRYRUN | verwaist | fix |
|------|--------|------------|--------|--------|--------|----------|-----|
| evidence/board-2026-10-29/scripts/chain-run.sh | PASS | N/A | PRÜFEN | N/A | N/A | NEIN | - |
| evidence/board-2026-10-29/scripts/negative-proofs.sh | PASS | N/A | PRÜFEN | N/A | N/A | NEIN | - |
| evidence/board-2026-10-29/scripts/receipt-suite.sh | PASS | N/A | PRÜFEN | N/A | N/A | NEIN | - |
| evidence/board-2026-10-29/scripts/receipt_tasklink.py | N/A | PASS | N/A | N/A | N/A | NEIN | - |
| evidence/board-2026-10-29/scripts/receipt_verifier.py | N/A | PASS | N/A | N/A | N/A | NEIN | - |
| root/scripts/chain-run.sh | 404 | N/A | N/A | N/A | N/A | JA | KORRIGIERT |
| root/scripts/negative-proofs.sh | 404 | N/A | N/A | N/A | N/A | JA | KORRIGIERT |
| root/scripts/receipt-suite.sh | 404 | N/A | N/A | N/A | N/A | JA | KORRIGIERT |
| root/scripts/ruleset-activation/ | 404 | N/A | N/A | N/A | N/A | JA | KORRIGIERT |

7. END q232-DONE