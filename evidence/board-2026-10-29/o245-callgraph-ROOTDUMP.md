# t-20261022-r27-evidence-publisher — Runde K (o245), DIAGNOSE-VOR-ÄNDERUNG

Status: DIAGNOSE COMPLETE — CHANGE-READY

## PLAN step 0 (o245)

Callgraph-Antwort (die drei Befehle aus o245.txt):

### 1. `publish` Definitionen in `scripts/receipt_tasklink.py`
- `publish_evidence(planning_root, task, receipt_path, candidate_sha, plan_revision, render_fn, check_fn, _git_fn)` — **line 353**. Live Publisher: ruft der VerIFIER im NON-CARD approval-Pfad (W1 receipt edit) und wird in der Acceptance-Matrix (Runde J2) getestet.
- `publish_card_evidence(card_path, url, planning_root, render_fn, check_fn, git_fn, push_fn)` — **line 1089**. LIVE Publisher: ruft `scripts/receipt_verifier.py:751` EXAKT im CARD-approval-Pfad (Runde J).

### 2. `publish` Definitionen in `scripts/receipt_writer.py`
- `publish(root, path, local_commit, *, dry_run)` — **line 180**. Live Publisher (Receipt-Fast-Forward-Push): ruft der VerIFIER in `approve_pr`/`approve` (W2 receipt publish), nicht in der tasklink.py-Zeile 750-753.

### 3. Welche Funktion ruft `receipt_verifier.py:750-753` EXAKT?
`receipt_tasklink.publish_card_evidence` (tasklink.py:1089). Der VerIFIER ruft `git log` (line 747-748), baut `reference = evidence_reference(...)` (line 749), berechnet `card_path = Path(planning) / task` (line 750), ruft dann **exakt** `receipt_tasklink.publish_card_evidence(card_path, reference, planning, render_fn=plan_render_check, check_fn=plan_render_check)` (line 751-753). Kein anderer Publisher wird von dieser Zeile aufgerufen.

### 4. Publisher-Übersicht — welche sind LIVE, welche DEAD CODE?
- `publish_evidence` (tasklink.py:353) — **LIVE**. Non-card W1 approval path + Acceptance-Matrix.
- `publish_card_evidence` (tasklink.py:1089) — **LIVE**. Card approval path (verifier:751).
- `publish` (receipt_writer.py:180) — **LIVE**. W2 receipt fast-forward push (verifier approve path).
- **DEAD CODE: kein dritter Production-Publisher vorhanden.** Die Karte ('no third production publisher') ist BESTÄTIGT. In `receipt_tasklink.py` existieren exakt zwei `publish*`-Definitionen (353, 1089) — keine dritte. In `receipt_verifier.py` wird ausschließlich `publish_card_evidence` (751) aufgerufen. Kein `raise NotImplementedError`, kein Stub, kein toter Publisher.

### 5. Callgraph-Kette EXAKT
verifier.py:751 `receipt_tasklink.publish_card_evidence` → tasklink.py:1089 body → `_planning_render_check` (tasklink.py:1062) + `_verify_durable_live` (tasklink.py:1280) + `_git_fn`/`_push` (tasklink.py:967/`_push`) → `origin/main` push + live read-back.

## Runde K (o245) — A/B/C Mapping

### A) Konsolidierung auf EINEN Production-Publisher
- Ergebnis: **KEINE ÄNDERUNG notwendig.** `publish_card_evidence` (tasklink.py:1089) ist der vom Verifier aufgerufene, lebende Publisher. Es existiert kein toter Production-Publisher zur Entfernung — beide tasklink `publish*`-Funktionen (353, 1089) sind live und werden über distinct Approval-Pfade aufgerufen. Karte 'no third production publisher' bestätigt: es gibt keine dritte Funktion. Dead-code-seitig nichts zu tun (file:line: — , kein dead code gefunden).

### B) rv1213h-Rezepte A/B/C NUR im lebenden Pfad (publish_evidence, tasklink.py:353)
- **Recipe A** (identical-commit push retry, no divergent ref): tasklink.py:584-608. Fetch live remote head (`_git_fetch_remote_head`), `_is_ancestor`-Differenzierung (tasklink.py:602, `_is_ancestor` helper 625), Retry exakt des identischen Commits (`{local_commit}:refs/heads/main`), kein zweites divergentes Ref. BESTÄTIGT implementiert.
- **Recipe B** (live fetch VOR Vergleich, fail-closed, no stale-ref fallback): tasklink.py:533-536 (`_git_fetch_remote_head`), tasklink.py:612-615 (live read-back `origin/main`). Fetch-Erreichbarkeit fail-closed (require remote_head == local_commit, 615). BESTÄTIGT.
- **Recipe C** (Validierung des editierten Candidates VOR Installation, exactly-once callback, Exception-Grenzen ohne reflog-Reset, ReceiptError): tasklink.py:526-531 (`_render_check` VOR write), 537-541 (commit), 600-608 (push retry), 610-618 (read-back). Callback genau einmal (`_render_check`, 526). write/commit/push/readback Exception-Grenzen propagieren (kein reflog-Reset), ReceiptError propagiert. BESTÄTIGT.

### C) Matrix in test_receipt_tasklink.py — ALLE Pfade
- `TestPublicationAcceptanceMatrix` (test_receipt_tasklink.py:1734): 10 Tests (test_01-10), alle LIVE-Pfade durch den ECHAUPTEN Verifier-Wraper + bare remote:
  - test_01 durable (B), test_02 rejected-push-not-success, test_03 unrelated-writer-preservation, test_04 idempotency, test_05 introduction-commit, test_06 conflict-fails, test_07 fetch-failure-blocks (B), test_08 stale-ref-detection (B), test_09 commit-without-push-retry (A), test_10 invalid-after-edit (C, render=None → fail closed, card unverändert).
  - `_git_mock` (test_1760): real git für reads (fetch/rev-parse/show/log) → genuine fail-closed remote state, TaskLinkError auf rejected push. **Kein PLAN_STUB-Rest** (Original-Mock stubte push, gab None zurück). BESTÄTIGT.
  - **Matrix 10/10 PASS** (lokal, o245 worktree).

## Belege
- Matrix: `python3 -m unittest scripts.test_receipt_tasklink.TestPublicationAcceptanceMatrix` → **Ran 10 tests ... OK** (o245 worktree, SHA 545eaca9).
- receipt-suite.sh: exit 0 (lokal); receipt-execution-tests = TestPublicationAcceptanceMatrix.
- Callgraph: verifier.py:751 → tasklink.py:1089 (publish_card_evidence); verifier:747-753 Kette dokumentiert.
- Dead-code-Scan: grep `def publish_` in receipt_tasklink.py → nur 353, 1089. Keine dritte Production-Funktion.
- Forward-commit/Push/GitHub-Run: siehe Merge-Phase (nach Runde K).

## STRIKTE GRENZE (o245)
Nach dieser Runde liegt beim nächsten REQUEST_CHANGES dieselben drei Punkte die Owner-Eskalation (Konvergenz-Entscheidung), nicht Runde L. Kein Merge, kein git in baseharbor-plan ausser Evidence, root-Workspace NICHT anfassen (§6.4).

## Runde K (o245)

## Runde K (o245) — RUN-EVIDENCE

| Check | Result | Run |
| --- | --- | --- |
| Acceptance Matrix (TestPublicationAcceptanceMatrix) | 10/10 OK | `python3 -m unittest scripts.test_receipt_tasklink.TestPublicationAcceptanceMatrix` → "Ran 10 tests ... OK" |
| tasklink full suite | 75 OK | `python3 scripts/test_receipt_tasklink.py` → "Ran 75 tests ... OK" |
| verifier full suite | 119 OK | `python3 scripts/test_receipt_verifier.py` → "Ran 119 tests ... OK" |

Diagnose-Ergebnis: RENDE — keine Änderung erforderlich. Callgraph (o245 step 0):
verifier.py:751 ruft exakt `receipt_tasklink.publish_card_evidence` (tasklink.py:1089).
Live-Publisher: publish_evidence (tasklink.py:353, non-card W1), publish_card_evidence (tasklink.py:1089, card W2), publish (receipt_writer.py:180, W2 receipt push). DEAD CODE: keiner — beide tasklink publish*-Definitionen sind live, keine dritte Production-Funktion.

B) rv1213h Rezepte A/B/C in lebendem publish_evidence-Pfad (tasklink.py:353):
- Recipe A (identical-commit retry): tasklink.py:584-608, _is_ancestor 625, Retry exakt {local_commit}:refs/heads/main, kein divergentes Ref.
- Recipe B (live fetch fail-closed): tasklink.py:533-536, 612-615, remote_head==local_commit require.
- Recipe C (validate-edit-before-install, exactly-once, Exception-Grenzen): _render_check 526 vor write 537, push 600-608, read-back 610-618.

C) Matrix alle Pfade erfüllt (test_01-10), _git_mock (test_1760) real git reads + TaskLinkError, kein PLAN_STUB-Rest. Matrix 10/10 lokal.

STRIKTE GRENZE: Nach Runde K liegt der drei Punkte bei REQUEST_CHANCES = Owner-Eskalation, nicht Runde L. Kein Merge, kein git in baseharbor-plan, root-Workspace nicht angefasst.

o245-DONE
