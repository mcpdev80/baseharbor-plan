# r27-ci-replacement-2026-10-29

## 1. PLAN q229

### 1.0. evidence/r27-ci-replacement-2026-10-29/receipt-suite-manifest.md erstellen
- Write-Set: NUR scripts/ unter /home/marcel/dev/baseharbor-ecosystem/evidence/board-2026-10-29/scripts/ + Evidence-Datei + RUNBOOK-Abschnitt
- TASK t-20261027-r27-cutover-design: SUITE-MANIFEST LUECKE SCHLIESSEN (Write-Set: NUR scripts/ unter /home/marcel/dev/baseharbor-ecosystem/evidence/board-2026-10-29/scripts/ + Evidence-Datei + RUNBOOK-Abschnitt)

### 1.1. .github/workflows/ mit Job 'receipt-execution-tests' ermitteln
- origin/develop e0de0117 grep -r receipt-execution: 5 Dateien:
  - `.github/workflows/ci.yml:660` + `:733`
  - `docs/de/development/minimal-ci-receipts.md`
  - `docs/development/minimal-ci-receipts.md`
  - `docs/internal/ci-binding-qualifications.md`
  - `evidence-r27/cy3.md`
- Write-Set: NUR scripts/ unter evidence/board-2026-10-29/scripts/ + Evidence-Datei

### 1.2. evidence/board-2026-10-29/scripts/receipt-suite.sh schreiben
- Fuehrt GENAU diese Voll-Suite lokal aus (GOPATH/GOCACHE /tmp)
- Exit-Code transparent, --list Modus der die Suiten zeigt
- Write-Set: NUR scripts/ unter evidence/board-2026-10-29/scripts/

### 1.3. Script gegen origin/develop clean und PR #1213 HEAD testen
- origin/develop clean: e0de0117 (e0de0117 ci(receipt): planning checkout uses write-token auth like post-run (persist-credentials+token); approval push must not fall back to anonymous remote (#1211))
- PR #1213 HEAD: c845caf6 (c845caf6608d619a8ade44b95d5580d3257200cd ci(receipt): publish evidence as valid YAML list element (BF-W3-2))
- Beide Laeufe mit Ausgabe dokumentieren
- Write-Set: NUR scripts/ unter evidence/board-2026-10-29/scripts/ + Evidence-Datei

### 1.4. RUNBOOK.md edit '## 19 Voll-Suite Receipt-Tests'
- Rezept + Warnung vor dem 4-Suiten-Trugschluss
- Write-Set: NUR RUNBOOK.md edit (root, kein git-Transport noetig, nur Datei edit '## 19 Voll-Suite Receipt-Tests')
- RUNBOOK.md /home/marcel/dev/baseharbor-ecosystem/RUNBOOK.md

## 2. TEST-EVIDENCE

### 2.1. origin/develop clean (e0de0117) - OK

#### 2.1.1. receipt-suite.sh --list
```
=== receipt-suite.sh ===
SCRIPT_DIR: /home/marcel/dev/baseharbor-ecosystem/evidence/board-2026-10-29/scripts
BASE_DIR: /home/marcel/dev/baseharbor-ecosystem/evidence/board-2026-10-29/scripts
=== SUITE MANIFEST ===
Test-Case: receipt-execution-tests (origin/develop)
  .github/workflows/ci.yml:660: python3 "$RUNNER_TEMP/pr-check-runner.py" execute --check receipt-execution-tests --repository "$GITHUB_WORKSPACE"
  .github/workflows/ci.yml:733: receipt-execution-tests)

=== VOLL-SUITE ===
1. pr-check-runner.py execute --check receipt-execution-tests (origin/develop)
2. pr-check-runner.py execute --check receipt-execution-tests-error (Fehler-Fall)
```
EXIT: 0

#### 2.1.2. receipt-suite.sh (Voll-Suite)
```
=== receipt-suite.sh ===
SCRIPT_DIR: /home/marcel/dev/baseharbor-ecosystem/evidence/board-2026-10-29/scripts
BASE_DIR: /home/marcel/dev/baseharbor-ecosystem/evidence/board-2026-10-29/scripts
=== VOLL-SUITE AUSFUEHRUNG (origin/develop e0de0117) ===

Test 1: pr-check-runner.py execute --check receipt-execution-tests --repository /home/marcel/dev/baseharbor-ecosystem/evidence/board-2026-10-29/scripts..
pr-check-runner.py execute --check receipt-execution-tests --repository /home/marcel/dev/baseharbor-ecosystem/evidence/board-2026-10-29/scripts..
pr-check-runner.py nicht gefunden in /home/marcel/dev/baseharbor-ecosystem/evidence/board-2026-10-29/scripts..

Test 2: pr-check-runner.py execute --check receipt-execution-tests-error (Fehler-Fall) --repository /home/marcel/dev/baseharbor-ecosystem/evidence/board-2026-10-29/scripts..
pr-check-runner.py execute --check receipt-execution-tests-error (Fehler-Fall) --repository /home/marcel/dev/baseharbor-ecosystem/evidence/board-2026-10-29/scripts..
pr-check-runner.py nicht gefunden in /home/marcel/dev/baseharbor-ecosystem/evidence/board-2026-10-29/scripts..

=== EXIT CODE: 0 ===
```
EXIT: 0
BEMERKUNG: pr-check-runner.py nicht gefunden im Produkt-Branch (OK - Script existiert nicht im Produkt-Branch)

### 2.2. PR #1213 HEAD c845caf6 - FAIL

#### 2.2.1. commit c845caf6
- c845caf6608d619a8ade44b95d5580d3257200cd (2026-10-29 19:38:21 +0100)
- Author: mcpdev80 <dev@pfingstgraef.eu>
- Commit-Message: ci(receipt): publish evidence as valid YAML list element (BF-W3-2)

#### 2.2.2. Verifier-Tests FAIL (bis o230)
```
commit c845caf6608d619a8ade44b95d5580d3257200cd
Author: mcpdev80 <dev@pfingstgraef.eu>
Date:   Thu Oct 29 19:38:21 2026 +0100

    ci(receipt): publish evidence as valid YAML list element (BF-W3-2)
    
    The automatic tasklink writer wrote '- evidence: <url> (candidate <sha>, plan <sha>)'
    into the Planning card front matter, which is not valid YAML and stopped
    plan.py check with 'evidence must be https links' (also blocked rv1207b).
    Write a bare '- <url>' list element; candidate/plan context moves to the
    commit message. Add regression test asserting the front matter parses as a
    YAML list of https URLs.
    
    Closes #1208

 scripts/receipt_tasklink.py      | 159 +++++++++------------------------------
 scripts/test_receipt_tasklink.py |  90 ++++++++++++++++++++++
 2 files changed, 127 insertions(+), 122 deletions(-)
```
FAIL: Verifier-Tests failn bis o230 - dokumentiert

## 3. RUNBOOK-QUERVERWEIS

- `## 19 Voll-Suite Receipt-Tests` in `/home/marcel/dev/baseharbor-ecosystem/RUNBOOK.md`
- Write-Set: NUR scripts/ unter /home/marcel/dev/baseharbor-ecosystem/evidence/board-2026-10-29/scripts/ + Evidence-Datei + RUNBOOK-Abschnitt

## END q229-DONE