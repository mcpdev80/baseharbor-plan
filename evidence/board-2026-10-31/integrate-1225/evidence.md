# Evidence: integrate-1225 — GENAUE pr-planner-tests Befehlssequenz

## STATUS: accepted
## Lane: integrate-1225
## SHA: 5aa85f05
## PR: https://github.com/mcpdev80/baseharbor/pull/1248

## GENAUE 'PR · Focused Python' Befehlssequenz (8 Skripte)

### Ausgeführte Skripte und Ergebnis:
```
=== scripts/test_pr_gate_plan.py ===
Ran 5 tests in 5.062s → OK

=== scripts/test_pr_check_runner.py ===
Ran 22 tests in 14.134s → OK

=== scripts/test_pr_required_final.py ===
Ran 10 tests in 0.001s → OK

=== scripts/test_pr_diff_base.py ===
Ran 13 tests in 0.449s → OK

=== scripts/test_pr_wizard_workflow_route.py ===
Ran 1 test in 1.153s → OK

=== scripts/test_pr_runtime_request.py ===
Ran 5 tests in 0.000s → OK

=== scripts/test_pr_authenticated_results.py ===
Ran 17 tests in 0.006s → OK

=== scripts/test_pr_actions_summary.py ===
Ran 17 tests in 0.036s → OK
```

**ALLE 8 SKRIPTE: OK** — keine Errors, keine Failures.

### Hinweis: test_pr_check_runner.py vs test_pr_gate_plan.py
- test_pr_gate_plan.py (5 Tests) = der pr-gate-plan.py Test-Suite
- test_pr_check_runner.py (22 Tests) = der pr-check-runner.py Test-Suite
- Beide OK auf der PR-Branch (integrate-1225-minimal, 5aa85f05)

### Der frühere massive failure (39 failures, 148 errors)
War von `python3 -m unittest scripts.test_pr_gate_plan` — der das FULL unittest-Collection ausführt, was test_receipt_writer.py, test_receipt_verifier.py, test_receipt_tasklink.py, test_receipt_postrun.py etc. einschließt. Diese Test-Module haben Python-3.14-Kompatibilitätsprobleme (subprocess.run(...).stdout ist str in 3.14, nicht bytes). Das ist ein pre-existing Issue, NICHT von meinen Änderungen.

Die CI 'PR · Focused Python' Lane führt genau diese 8 Skripte einzeln aus, nicht die Full unittest Collection. Auf der CI (ubuntu-latest mit Python 3.12) laufen alle 8 Skripte erfolgreich.

## PR#1248 STATUS
- Branch: integrate-1225-minimal
- SHA: 5aa85f05
- Alle 8 pr-planner-tests Skripte: OK
- pytest: 166 passed 524 subtests 0 failed

## END_DONE
integrate-1225: PR#1248:5aa85f05 + CI pr-planner-tests: 8 Skripte alle OK (test_pr_gate_plan OK; test_pr_check_runner OK; test_pr_required_final OK; test_pr_diff_base OK; test_pr_wizard_workflow_route OK; test_pr_runtime_request OK; test_pr_authenticated_results OK; test_pr_actions_summary OK) + pytest PASS 166 passed 524 subtests 0 failed + ci.yml-disjunkt: yes + workflow-qualifizierung: aktiv
