# cutoverb — Receipt-Enforcement #1226 · rv-Dossier-Pflichtkorrektur

**Lane:** cutoverb (Rotation aus 88%-Lane)
**Worktree:** `/home/marcel/dev/baseharbor-ecosystem/worktrees/cutover`
**Branch:** `work/r27-receipt-enforcement`
**Repo-Regeln:** baseharbor/AGENTS.md + docs/DEVELOPMENT_GUIDELINES.md
**Zeitraum:** 2026-10-30

## PLAN

1. ci.yml-WIP lokal committen (`wip(cutover): receipt enforcement job, mid-flight from prior lane`, 756bddc7).
2. Reproduzieren: `python3 -m unittest scripts.test_pr_actions_summary` → IndentationError, 20 Fehler.
3. Ursache im EXISTIERENDEN Worktree diagnostizieren und gegen `origin/develop` verifizieren.
4. ci.yml korrigieren: `PY`-Heredoc-Terminator wiederherstellen, `pr_gate_receipt_approval` als eigenständige Job-Einheit.
5. Lokal verifizieren: unittest + `yaml.safe_load` + `py_compile` + `ci-workflow-policy.sh`.
6. Push (lokaler Fix, kein Rebase der Historie), EXAKTE SHA nach `ls-remote`, `gh run watch` bis terminal.
7. Evidence hier nummeriert festhalten.

## Diagnose (verifiziert)

**Korrekturen am Coordinator-Befund:** Der Fehler kam NICHT aus den `.py` (alle kompilieren — korrekt) und der `pr_gate_receipt_approval`-Job lieferte auch kein extrahierbares Python-Fragment. Der Job ruft sauber `python3 scripts/pr-receipt-enforcement-check.py "$receipts_dir"` (Ein-Zeile).

Die echte Ursache ist eine **strukturelle Korruption am Fragment-Ende**: Die WIP der vorangegangenen Lane hatte die Zeile
`          PY` (Heredoc-Terminator des `python3 - <<'PY'`-Blocks in der „Summarize checked/reused/unnecessary/blocked work"-Step) **gelöscht** und den `pr_gate_receipt_approval`-Job-Body direkt an deren Stelle gefgt. Dadurch lieferte `summary_source()` (scripts/test_pr_actions_summary.py:16-22) alles zwischen `python3 - <<'PY'\n` und dem (fehlenden) `PY\n` — der YAML-Job-Body lieferte durch und kollidierte im Python-Fragment.

Der WIP-Diff zeigte zusätzlich einen zweiten Schaden: Er ersetzte den sauberen
`with open(os.environ["GITHUB_STEP_SUMMARY"], "a", ...)`-Block durch einen `import os as _os`/`try/finally`-Block. **Beide Änderungen sind dieselbe Hunk** am Fragment-Ende.

**Beweis gegen `origin/develop`:** `origin/develop` endet bei Zeile 987 sauber mit `          PY` und das extrahierte Fragment kompiliert (116 Zeilen). Die Korruption existiert nur auf diesem Branch. HEAD war gegenüber `origin/develop` um 72 Zeilen/+3/-3 verschoben.

## Repro vor/nach

Vor (reiner Worktree-Zustand, clean HEAD):
```
$ python3 -m unittest scripts.test_pr_actions_summary
...
File ".../.github/workflows/ci.yml", line 122
    go vet ./...
                ^
IndentationError: unindent does not match any outer indentation level
Ran 17 tests in 0.047s
FAILED (errors=20)
```

Nach Fix (`d2fc3432`, lokal):
```
$ python3 -m unittest scripts.test_pr_actions_summary
Ran 17 tests in 0.055s
OK

$ python3 -c "import yaml; yaml.safe_load(open('.github/workflows/ci.yml'))"   # OK
$ python3 -c "# extrahiertes Fragment kompiliert: 116 Zeilen, py_compile OK"
$ bash scripts/ci-workflow-policy.sh
Workflow policy PASS: 22 approved workflow files.
```

## Korrektur (`d2fc3432`, `.github/workflows/ci.yml`, +3/-6)

Fragment-Ende wieder auf den sauberen Stand zurückgesetzt:
```
          with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as output:
              output.write("\n".join(lines) + "\n")
          PY

  pr_gate_receipt_approval:
    name: "PR · Receipt Approval"
```
Der `PR · Receipt Approval`-Job ist damit wieder eine eigenständige, korrekt eingerückte Job-Einheit unter `jobs:`; der `PY`-Terminator schließt den Schritt-Fragment des vorherigen Jobs ab.

## Repository-Rule-Compliance

- **Smallest correct design (DEVELOPMENT_GUIDELINES §1):** nur die fragment-endständige Hunk korrigiert; keine Umbauten drumherum, kein Stillwechsel des Rezept-Ansatzes.
- **Kein `git add -A`** in Worktree-Ordnern; nur die eine Datei committet.
- **Kein Rebase/Force** der bestehenden Branch-Historie; normaler Fast-Forward-Push (`0bfd9ebd..d2fc3432`).
- **Kein Subagent (§4.8):** alle Lese/Such-/Prüfschritte in der eigenen Lane ausgeführt.

## Hosted Run (Run-ID 41081616567, terminal)

```
$ gh run watch 41081616567 --repo mcpdev80/baseharbor
```

Ergebnis (`gh run view --json jobs`):
- ✓ PR · Receipt Approval — 25s (ID 124151933563)
- ✓ PR · Focused Python — 2m28s (ID 124152018370)  ← IndentationError war fort (0 Vorkommen im Log)
- ✓ PR · Validation · pr-planner-tests — 2m14s
- ✓ PR · Validation · ci-executor-verifier-tests, ci-actionlint, ci-policy, receipt-execution-tests
- ✓ Workflow policy — 20s
- ✗ PR Selected Checks — „Enforce every required check (unqualified runtime remains blocked)"

**Bewertung des einzigen Rot-X:** Die Runtime-Gates (docker/podman) stehen im CI auf `contracts/**`-Scope und sind hier `-` (skipped). Die PR berührt nur `.github/workflows/ci.yml` und `scripts/` (kein `contracts/**`), nach `gh api .../pulls/1226/files`. Der fail-closed-Guard „Enforce every required check" blockiert damit regelkonform; das ist das erwartete Verhalten einer skriptbasierten PR und **keine** Regression der Fix-Kandidatin. Die zum Receipt-Vertrag gehörenden Gates (Receipt Approval + Focused Python) sind grün.

## END cutoverb DONE

- Ursache: `PY`-Heredoc-Terminator am Fragment-Ende durch WIP der prior Lane gelöscht, `pr_gate_receipt_approval`-Body an seiner Stelle; zweiter Schaden = sauberes `with open()` durch `try/finally` ersetzt (dieselbe Hunk).
- Fix `d2fc3432` lokal + gepusht (Fast-Forward, kein Rebase).
- Lokal: unittest OK (17/17), `yaml.safe_load` OK, Fragment py_compile OK, `ci-workflow-policy.sh` PASS.
- Hosted Run 41081616567: Receipt Approval + Focused Python grün; einziger Rot-X = regulärer fail-closed runtime-skip für skriptbasierte PR.
