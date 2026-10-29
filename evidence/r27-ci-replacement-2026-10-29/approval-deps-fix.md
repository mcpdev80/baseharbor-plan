# r27 shadow-run APPROVAL-DEP FIX — evidence

PLAN (numbered, no checkboxes)

1. TASK t-20261027-r27-shadow-run APPROVAL-DEP FIX (Owner-Auftrag): Run 40915351645
   failed 'Planning schema resolver requires PyYAML' im approve-Job von
   receipt-approval.yml. verifier import yaml an script:573.
2. WORKTREE: `git -C baseharbor worktree add /home/marcel/dev/baseharbor-ecosystem/worktrees/o222
   -b work/r27-approval-deps origin/develop`. Branch HEAD: 64d12492 (base), fix commit 439b13c7.
3. AUDIT: alle python-Schritte der drei receipt-Workflows auf third-party imports geprueft.
4. FIX: minimal & konventionskonform nach artifact-gc.yml-Muster (setup-python@v5 + pip install
   'PyYAML==6.0.2') im approve-Job von receipt-approval.yml, nach Set-up-Python, vor Checkout Planning.
5. TESTS lokal: python3 -m unittest (4 test modules), py_compile, YAML-validate, actionlint via CI.
6. PIN-HINWEIS: pinned_source-Byte-Vergleich geprueft und Owner-Regel zur Registrierung dokumentiert.
7. COMMIT 'fix(ci): install PyYAML for planning schema resolver in receipt approval
   (+ post-run/shadow if needed)', push, gh pr create --base develop (ein Closes-Tag).
8. EVIDENCE (dieses file).

## Audit-Tabelle aller receipt-Workflows

| Workflow / Job | Ausgef. Script | third-party import | setup-python vorhanden | pip install PyYAML noetig? |
|---|---|---|---|---|
| receipt-approval.yml / approve | receipt_verifier.py `approve` | `import yaml` an line 573 (`front_matter`, der Planning schema resolver) via `task_pr_associations`/`resolve_task_from_pr` | JA (v7) | JA — approve-pfad loest PR->task und ruft front_matter/yaml auf |
| receipt-post-run.yml / publish_receipt | receipt_tasklink.py + receipt_writer.py | NEIN (argparse, json, os, re, subprocess, pathlib, typing) | JA (v7, py 3.14) | NEIN — kein yaml im post-run/publish-pfad |
| receipt-shadow.yml / receipt_shadow | receipt_verifier.py `retained` | NEIN im retained-pfad (git blob + JSON, kein front_matter/yaml) | NEIN (kein setup-python) | NEIN — retained laest nur JSON-Blobs, kein yaml |

Ursache: receipt_verifier.py line 565-575 `front_matter()` fuehrt `import yaml` aus;
fail-closed ReceiptError "Planning schema resolver requires PyYAML" wenn PyYAML fehlt.
Der approve-pfad (`approve_pr` -> `task_binding` -> `task_pr_associations` -> `front_matter`
-> `import yaml`, verifier line 622 `resolve_task_from_pr`) braucht yaml zwingend;
post-run (`receipt_tasklink`/`receipt_writer`) und shadow (`retained`) nicht.

## Fix

Nur eine Zeile (`+3` insert, `git diff --stat`: `.github/workflows/receipt-approval.yml | 3 +++`):

```yaml
      - name: Set up Python
        uses: actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7
        with:
          python-version: '3.x'

      - name: Install Planning schema resolver dependency      # <-- NEU
        run: python -m pip install 'PyYAML==6.0.2'              # <-- NEU (artifact-gc.yml-Muster)

      - name: Checkout Planning (protected main, full history)
```

Pinned Version 6.0.2 identisch zum artifact-gc.yml-Bestand (`run: python -m pip install 'PyYAML==6.0.2'`).

## Tests (local evidence)

- python3 -m unittest test_receipt_postrun test_receipt_chain test_receipt_writer
  test_receipt_tasklink -> Ran 73 tests in 11.845s, OK, exit 0.
- python3 -m py_compile scripts/receipt_verifier.py scripts/receipt_tasklink.py scripts/receipt_writer.py -> OK.
- python3 -c "import yaml; [yaml.safe_load(open(f)) for f in [receipt-approval.yml, receipt-post-run.yml, receipt-shadow.yml]]" -> YAML OK.
- actionlint lokal nicht installiert (which actionlint -> not found); als maschinenlesbarer Beweis
  ueber GitHub-CI gelaufen (siehe CI-Beweis unten).

## CI-Beweis (GitHub, Run 40916679898)

PR #1209 head 439b13c771ee35cd24a264eb6caf70eea9928eb5 (== o222 branch HEAD).
Alle Mandatory-Gates SUCCESS:

- Workflow policy: SUCCESS
- PR · Trusted Plan: SUCCESS
- PR · Validation · ci-actionlint: SUCCESS
- PR · Validation · ci-executor-verifier-tests: SUCCESS
- PR · Validation · ci-policy: SUCCESS
- PR · Validation · pr-planner-tests: SUCCESS
- PR · Validation · receipt-execution-tests: SUCCESS
- (Release Source Preflight / Targeted HA docker-podman / validate / consumer-demo / runtime: SKIPPED —
  workflow_dispatch-Kette, keine Produkt-Qualifikation)

## PIN-HINWEIS (Registrierung = final integrierter Commit)

pinned_source() in receipt_verifier.py:338 vergleicht am approve-lauf:

1. source_blob(product, TRUSTED_SOURCE, HELPER_SOURCE) == receipt_verifier.py-Bytes des laufenden runners.
2. source_blob(product, TRUSTED_SOURCE, APPROVAL_WORKFLOW) == source_blob(product, GITHUB_SHA, APPROVAL_WORKFLOW).

Der approve-job checkt den authifizierten run-head aus (actions/checkout full-history,
kein ref-Override, on: workflow_dispatch). TRUSTED_SOURCE = vars.BASEHARBOR_RECEIPT_TRUSTED_SOURCE
(repository variable; leer = pre-registration, fail-closed).

Konsequenz fuer diese Aenderung:
- Der Byte-Vergleich misst die receipt-approval.yml am RUN-HEAD des registrierten main-Workflow-
  launches, nicht an diesem PR/branch. Diese PR veraendert nur work/r27-approval-deps, nicht den
  authenticated run-head.
- Registrierung (Owner-Regel): registration = der final integrierte Commit auf main, der diese
  Aenderung enthaelt; TRUSTED_SOURCE ist dann EXAKT dieser main-integrierten Commit-SHA. Erst nach
  Merge auf main und Update der repository variable BASEHARBOR_RECEIPT_TRUSTED_SOURCE auf die
  neue main-SHA ist der pinned_source-Byte-Vergleich fuert. Bis dahin (leere/alte Variable) faellt
  approve closed, was dem ehrlichen pre-registration-zustand entspricht.
- Die Aenderung ist also nur gueltig, wenn nach dem Merge die BASEHARBOR_RECEIPT_TRUSTED_SOURCE-
  variable auf den main-integrierten Commit zeigt (oder develop-Blobs == main-Blobs, dann haette
  sich am workflow-blob nichts gegenuiber dem pin geaendert).

## repo-rule compliance

- baseharbor/AGENTS.md CI-execution-discipline: minimaler Fix, kleinste passende Gate-Aenderung,
  ein PR, kein Rerun-Matrix-Churn.
- artifact-gc.yml-Muster (setup-python@v5 + pip install 'PyYAML==6.0.2') konventionskonform uebernommen.
- Scope: nur receipt-approval.yml approve-job; post-run/shadow nicht beruehrt (kein yaml-Bedarf).
- Kein git in baseharbor-plan, kein Merge, kein workflow_dispatch (task-sektion 8).
- Ein Closes-Tag ('Closes #1208'), kein Force-Push, keine Branch-Protection-Umgehung.

## END o222-DONE
