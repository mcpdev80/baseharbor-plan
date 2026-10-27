# Evidence: diag1 — READ-ONLY CI-Triage PR #1115 / #1116 (rotierende Fix-PRs, r27)

Lane: diag1 (flash). Read-only Analyse; keine Produktänderungen, kein Dispatch.
Kategorien: A = fehlt der andere Branch als Basis (Abhängigkeit) · B = echter Fix-Gap (Owner-G) · C = Tooling/Umwelt.

## PLAN

1. [x] `gh pr checks` / `gh api` für #1115 (run 40509916015) und #1116 (run 40516178265); fehlende Jobs + Job-IDs erfasst
2. [x] Logs gezogen: #1116 via `gh run view --log`; #1115 via Job-Log-API (siehe Log-Pragmatik)
3. [x] Fehlerzeilen je Job extrahiert (gekürzt)
4. [x] Branches lesend verglichen (`git merge-base`, `git grep`, `git show`): Kreuzabhängigkeit #1115↔#1116 verifiziert
5. [x] G-Zuordnung aus `evidence-r27/f3b-fix.md` (Repo) + pr-gate-plan.py/belegte Registerlücke abgeleitet
6. [x] Diese Evidence geschrieben; render+check; EIN commit+push

## Log-Pragmatik

- #1115 (run 40509916015, jüngerer Lauf; Vorgänger 40509666697 cancelled): `gh run view --log --job=…` liefert 0 Bytes, aber direkter Endpunkt `gh api /repos/mcpdev80/baseharbor/actions/jobs/<id>/logs` funktioniert → Logs vollständig ausgewertet, kein 410-Notpfad nötig.
- Älterer Lauf 40500234432 (in `evidence/board-2026-10-27/ci1-repair.md` analysiert) zeigt ein überholtes Bild: dort war Focused Python noch YAML-Kaskade; im aktuellen Run 40509916015 sind die Python-Suiten grün und es schlagen die BF-W3-1-Publish-Tests fehl. Neueste versuchte Runs: #1115 → 40509916015, #1116 → 40516178265.

## PR #1115 — work/r27-ci-repair, run 40509916015 (HEAD 94655dcc, base develop 3431b22c)

### Job 122209053641 — „PR · Focused Python" — Kategorie A

Erste Fehlerzeilen:
1. `ERROR: test_receipt_execution_check_actually_runs_receipt_suites (ReceiptControlPlaneMappingTests)` → `RuntimeError: receipt discovery/execution failed: …`
2. `FAIL: test_approve_cli_full_chain_fails_closed_on_missing_publish` → `AssertionError: "BF-W3-1" does not match "Git operation failed: push"`
3. `FAIL: test_missing_publish_interface_blocks_publication` → Traceback `receipt_verifier.py:429 publish_approval → receipt_writer.py:122 git(root,"push","origin","<sha>:refs/heads/main")`

Begründung: Der Fail-closed-Wrap für BF-W3-1 (`try/except → "publication blocked via BF-W3-1"` in receipt_verifier.py:442–447 + Push-Fehler-Propagation 74b95e14) existiert nur in #1116; dieser Branch führt im Hermetik-Test noch den rohen Push aus.

### Job 122209053668 — „PR · Validation · pr-planner-tests" — Kategorie A

Erste Fehlerzeilen:
1. identischer Traceback `publish_approval → receipt_writer.publish → git push refs/heads/main` → `ReceiptError: Git operation failed: push`
2. `AssertionError: "BF-W3-1" does not match "Git operation failed: push"`
3. `FAILED (failures=2)` / `FAILED (errors=1)`

Begründung: Dieselbe Receipt-Kette wird im Validation-Owner mitausgeführt → dieselbe fehlende BF-W3-1-Komponente aus #1116.

### Job 122209863658 — „PR Selected Checks" — Kategorie B (primär) + A (Kaskade)

Erste Fehlerzeilen:
1. `BLOCKED: coverage-unresolved: … requires native qualification: .github/workflows/ci.yml; … evidence-r27/ci1-repair.md; evidence-r27/w1.md; evidence-r27/w3.md; scripts/pr-check-runner.py; scripts/test_pr_check_runner.py`
2. `BLOCKED: required authenticated job not successful: PR · Focused Python`
3. `BLOCKED: required validation not successful: pr-planner-tests (blocked)`

Begründung: Die Job-Kaskade ist A, aber `pr-gate-plan.py:1410–1421` stuft ci.yml/pr-*/evidence-Pfade als „unresolved" ein, solange kein Register-Eintrag in `docs/internal/ci-binding-qualifications.md` bindet — dieser fehlt in BEIDEN Branches und bleibt auch nach Kreuz-Merge rot → echter Fix-Gap ohne bisherige Owner-G-Nummer (neuer Befund).

## PR #1116 — work/r27-fix-g3-publication, run 40516178265 (HEAD d5105121, base develop 3431b22c)

### Job 122230572389 — „Workflow policy" — Kategorie A

Erste Fehlerzeilen:
1. `.github/workflows/receipt-post-run.yml:107:0: could not parse as YAML: could not find expected ':' [syntax-check]`
2. `    | 107 | import json, zipfile, sys`
3. `##[error]Process completed with exit code 1.`

Begründung: Der actionlint-YAML-Reparaturcommit 6c8aeef4 (einzeiliges `python3 -c '…'`) liegt nur in #1115; dieser Branch enthält weiterhin den kaputten Mehrzeilen-Block (in develop existiert die Stelle noch nicht einmal, 64 Zeilen dort).

### Job 122230644681 — „PR · Focused Python" — Kategorie A

Erste Fehlerzeilen:
1. alle Python-Suiten grün (`Ran 5/10/19/1/… tests` → `OK`; BF-W3-1-Tests hier bestehend)
2. `.github/workflows/receipt-post-run.yml:107:0: could not parse as YAML: could not find expected ':' [syntax-check]` (actionlint-Schritt am Jobende)
3. `exit status 1` / `##[error]Process completed with exit code 1.`

Begründung: Reine Kaskade desselben YAML-Fehlers aus dem actionlint-Schritt; Produkt-Python ist auf diesem Branch gesund.

### Job 122230644879 — „PR · Validation · ci-actionlint" — Kategorie A

Erste Fehlerzeilen:
1. `.github/workflows/receipt-post-run.yml:107:0: could not parse as YAML: could not find expected ':' [syntax-check]`
2. `exit status 1`
3. `##[error]Process completed with exit code 1.`

Begründung: Identische Ursache; Fix lebt in #1115.

### Job 122231289694 — „PR Selected Checks" — Kategorie B (primär) + A (Kaskade)

Erste Fehlerzeilen:
1. `BLOCKED: coverage-unresolved: … native qualification: .github/workflows/ci.yml; … evidence-r27/f1-fix.md; evidence-r27/f3b-fix.md; evidence-r27/w1.md; evidence-r27/w3.md; scripts/pr-check-runner.py; scripts/test_pr_check_runner.py`
2. `BLOCKED: required authenticated job not successful: PR · Focused Python` / `Workflow policy`
3. `BLOCKED: required validation not successful: ci-actionlint (blocked)`

Begründung: Wie bei #1115 — Kaskade (A) plus dieselbe Register-Lücke (B), die unabhängig vom Kreuz-Merge offen bleibt.

## Befund für Coordinator / Owner

- Die beiden PRs sind gegenseitig blockierende Basis-Abhängigkeiten: #1115 braucht d5105121/74b95e14 (BF-W3-1-Wrap) aus #1116; #1116 braucht 6c8aeef4 (YAML-Repair) aus #1115. Empfehlung: ein Branch auf den anderen rebase/merge (z. B. #1116 → #1115-Pfad), dann ein gemeinsamer Kandidat.
- Danach bleibt GRÜN in Selected Checks nur mit Owner-qualifizierten Einträgen in `docs/internal/ci-binding-qualifications.md` für ci.yml, scripts/pr-check-runner.py, scripts/test_pr_check_runner.py und die evidence-r27-Pfade (ci1-repair/f1-fix/f3b-fix/w1/w3) — neuer Befund, bisher keiner G-Nummer zugeordnet (G1b/G2/G3a/G3b deckten Syntax/Transitions/Force-push, nicht die Qualifikation des Planners).
- Kein Kategorie-C-Befund: Runner-Umwelt und Tooling (actionlint-Install, Node-20-Deprecation-Warning) waren nicht fehlerursächlich.

CATS: A=5, B=2, C=0 (je fehlgeschlagenem Job; Selected-Checks-Jobs zählen als B primär mit A-Kaskade).

END DIAG1-DONE CATS=5/2/0
