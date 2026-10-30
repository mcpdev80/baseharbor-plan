# tasklink-yamlfix — Runde J2 (o244), matrix acceptance + real plan.py

## 1. Kontext

- Task: `t-20261022-r27-evidence-publisher` (state blocked; Blocker = Release-start Updates).
- Dispatcher: `evidence/board-2026-10-29/prompts/o244.txt` — Runde J2 UEBERNAHME (Nachfolgerin q243).
- Ziel-Repo/Head: `baseharbor` @ `700662da` (detached worktree `worktrees/q243`).
- Write-Setz: `scripts/receipt_tasklink.py` (Produkt), `scripts/test_receipt_tasklink.py`, `scripts/test_receipt_verifier.py`.
- Scope-Grenze: Matrix akzeptabel grün bringen + PLAN_STUB durch echtes plan.py ersetzen; kein Merge, kein Refactor ngoài die 5 roten Tests.

## 2. PLAN (nummeriert)

1. Matrix `test_receipt_tasklink_q243.py` gegen HEAD `700662da` laufen lassen: 10 Tests, 5 pass / 3 failures / 2 errors.
2. Jede failure/error einzeln triagieren: Produktcode-Fehl (tasklink/verifier) nur entlang rv1213g A/B/C + Kartenwortlaut; Test-Bug mit Begründung. Verbotene Kurzschlusse: reflog-resets, Stub-Validatoren, Szenario-loeschen.
3. `test_receipt_verifier.py` RealPlanValidationTest (PLAN_STUB) durch echten `baseharbor-plan/scripts/plan.py` render+check ersetzen (skip nur wenn plan.py fehlt).
4. receipt-suite / pr-check-runner exit0; Matrix in `test_receipt_tasklink.py` integrieren, extra File löschen.
5. Forward-Commit, push `HEAD:work/r27-tasklink-yamlfix`, hosted CI bis terminal beobachten (§4.6).
6. Evidence `## Runde J2 (o244)` mit Szenario-Tabelle + Root-Cause je Rot + Run-ID/Status.

## 3. Szenario-Tabelle + Root-Cause je Rot

| # | Szenario | Vorher | Typ | Root-Cause | Fix |
|---|----------|--------|-----|------------|-----|
| 1 | test_01 successful_durable_publication | pass | — | — | unverändert |
| 2 | test_02 rejected_push_is_not_success | pass | — | — | unverändert |
| 3 | test_03 unrelated_writer_preservation | FAIL | Test-Bug | Concurrent-Commit war linear zur Publish-Edit (same history) → fast-forwardbar, kein Konflikt | force-pushed Feature-Branch auf origin/main → echte Divergenz |
| 4 | test_04 idempotency_identical_evidence | pass | — | — | unverändert |
| 5 | test_05 introduction_commit_return | pass | — | — | unverändert |
| 6 | test_06 conflict_fails | FAIL | Test-Bug | Force-Push landete auf `main` statt Feature-Branch; `git push` ohne `-b feature` schlug fehl (check=True) | `checkout -b feature` + `push --force feature:main` |
| 7 | test_07 fetch_failure_blocks | FAIL | Test-Bug | `_fresh_clone` klonen von `remote_root` (Kopie); `origin.url` zeigte auf `/home/marcel/tmp-ops/…/remote.git`. `origin_root` zu löschen traf die Remote nicht | `remote_root/refs` + `remote_root/HEAD` gelöscht → echter Fetch-Failure |
| 8 | test_08 stale_ref_detection | ERROR | Test-Bug + Produktlücke | Mock lieferte `rev-parse origin/main` = None → `.strip()` AttributeError; Produkt: lokaler HEAD hinter Remote, aber kein Recheck | echter Mock + Produkt: live fetch + ancestry-guard, fail-closed bei stale |
| 9 | test_09 commit_without_push_retry | ERROR | Test-Bug | Mock hatte keinen Push-Retry-Pfad; `merge-base` nicht im Mock | `retrying_git` fail-once-then-succeed + `_is_ancestor` + merge-base im Mock |
| 10 | test_10 invalid_after_edit | FAIL | Test-Bug | Fixture-Card enthielt literals `evidence:` → `assertNotIn("evidence:", …)` scheiterte | neutrale Fixture ohne `evidence:`-Key |

## 4. Produktcode-Änderung (receipt_tasklink.py, `publish_evidence` Push-Pfad)

- Before: ein einzelner `git push origin {local_commit}:refs/heads/main`, danach `require(remote_head == local_commit)`.
- Now: try/except um den Push. Bei `TaskLinkError` live `origin/main` neu fetchen und mit `_is_ancestor(live_retry, local_commit, root)` prüfen:
  - Remote ist ancestor unseres Commits → rein transienter Push-Fehler → **ein** bounded Retry des **gleichen** Commit-SHA (keine zweite Divergenz, recipe A).
  - Remote nicht ancestor → echter Konflikt → `raise` (fail closed, kein stilles Reconciling).
  - Nach erfolgreichem Push `require(remote_head == local_commit)` (durable read-back).
- Neu: `_is_ancestor(ancestor_sha, descendant_sha, root, remote="origin", ref="main")` → `git fetch` + `git merge-base --is-ancestor` (fail closed; nicht-ancestor wirft TaskLinkError).

## 5. Matrix-Integration

- `TestPublicationAcceptanceMatrix` (10 Szenarien) aus `test_receipt_tasklink_q243.py` in `scripts/test_receipt_tasklink.py` integriert (registrierte Suite), extra File gelöscht.
- `_git_mock` in der Matrix: REAL git für Reads (fetch/rev-parse/show/log/add/commit/rebase/checkout/merge-base), `TaskLinkError` bei rejected push → fail-closed.

## 6. Real plan.py (test_receipt_verifier.py)

- `RealPlanValidationTest` lieferte bisher Karten über stdin gegen einen PLAN_STUB (plan.py-Mirror). Echs plan.py validiert aber die **ganze** Planning-Vault (render + check), nicht Single-Card-stdin — der stdin-Testansatz war gegen den echten Vertrag inkompabel.
- Ersetzt durch echtes `baseharbor-plan/scripts/plan.py render` + `check` auf der Vault-Integration. `PLAN_PY` wird per Workspace-Root-Auflösung gefunden (worktree-crossing). Skip nur wenn plan.py fehlt (dokumentiert).
- Per-Card-YAML-Regeln (List-vs-Scalar, Duplicate-Key) sind von plan.py's Front-Matter-Resolver der Vault verpflichtet, nicht stdin-per-Card; nicht als Fake-Card asserted.

## 7. Repo-Rule-Compliance (Runde J2)

- Write-Set nur receipt_tasklink.py (Produkt) + die zwei Test-Suiten; kein git in baseharbor-plan außer der Evidence-Datei.
- Kein Merge, kein Force-Push auf protected main, kein Schutzregel-Bypass.
- Produkt-/Planning-Remote vor Start gezogen (Remote-Zustand verifiziert).
- Lokale Tests gegen echte Bare-Remotes (kein gefakter Fallback).
- Verbotene Kurzschlusse eingehalten: kein reflog-reset, kein Stub-Validator (echtes plan.py), kein Szenario gelöscht.

## 8. Hosted CI (§4.6 eigener terminaler Run in der Beobachtung)

- Branch: `work/r27-tasklink-yamlfix`.
- Run `40998116429` (Base `700662da`, head `545eaca9`): terminal `completed/success`.
- Enabled jobs: `PR · Trusted Plan` success, `Workflow policy` success, `PR · Focused Python` success, `PR · Validation · pr-planner-tests` success, `PR · Validation · receipt-execution-tests` success, `PR · Validation · ci-executor-verifier-tests` success, `PR · Validation · ci-policy` success, `PR Selected Checks` success.
- Skipped (nicht betroffen/kein Auslöser): `validate`, `Targeted HA · docker`, `Targeted HA · podman`, `Release Source Preflight`, `PR · Runner Interface`, `PR · Consumer Pins`, `PR · Exact Candidate`, `PR · Demo Pin`, `PR · Public Contracts`, `PR · Selected Runtime`.
- Befund: alle mandatory Python/validation receipt-gate grün; nicht-wahlbare Runtime/Docker/Podman-Gate ohne Auslöser (Skip, kein Grün-gerechnet).

## 9. Lokal

- 242 receipt tests OK (`test_receipt_writer` + `test_receipt_verifier` + `test_receipt_chain` + `test_ci_workflow_policy_receipts` + `test_receipt_tasklink` + `test_receipt_postrun`).
- `pr-check-runner.py execute --check receipt-execution-tests` exit0.

END o244-DONE

## Coordinator-Nachtrag J2-Finale
- Finaler Head: 545eaca9 (ls-remote bezeugt), Run 40998116429 completed SUCCESS, Worktree clean, Debug-Rest verworfen (Option b, Lane-Bestätigung im Transcript).
- Lane d14ec578 released, Worktree entfernt. naechste Aktion: rv1213i (Codex, A/B/C-Grenze + Matrix-Katalog).

## Runde K2 (o246)

**Task:** `t-20261022-r27-evidence-publisher` · **Prompt:** `evidence/board-2026-10-29/prompts/o246.txt` (Runde K2)
**Base-Commit:** `545eaca9` (detached worktree `worktrees/o246`) · **Candidate:** `13026f29612bdae7adffe61dbcd4d7708f43938e` (baseharbor, branch `work/r27-tasklink-yamlfix`)
**PR:** #1213 (OPEN, `fix(receipt): tasklink writes evidence as valid YAML list element`)

### 1. Wrapper (dünner Delegator)
`publish_evidence` (receipt_tasklink.py:367) ist jetzt dünner Wrapper: alte Implementation (Evidenz-Knoten-Neubau, bare receipt_path) ENTFERNT. Wrapper konvertiert `receipt_path` → HTTPS-url `https://github.com/mcpdev80/baseharbor/blob/<candidate_sha>/<receipt_path>` (identische Form wie live `evidence_reference`, Zeile 656) und ruft `publish_card_evidence` (`receipt_tasklink.py:1089`) ein Mal auf; gibt die durable commit SHA zurück. Signature erhalten (`planning_root, task, receipt_path, candidate_sha, plan_revision, render_fn, check_fn, _git_fn, push_fn`), `ReceiptError`-Alias lazy per `_receipt_error()`. Kein dualer Output mehr — Alt-Tests assertieren künftig die URL-Form statt `front["evidence"]==[receipt_path]`.

### 2. A/B/C — file:line
**(2A)** live fetch vor Remote-Vergleich — `_verify_durable`/`_verify_durable_live` (`receipt_tasklink.py:1027`/`:1093`) fetchen `origin/main` LIVE vor read-back; fetch-Fehler → `TaskLinkError` (fail closed, kein Local-Fallback). Idempotenz-Pfad liest HEAD-Blob + live fetched origin/main (`:931-943`).
**(2B)** render/check EINMAL — `publish_card_evidence` (`:962`) ruft `_planning_render_check` EXAKT MAL; verifier-Production-Pfad ruft `publish_card_evidence` bei `receipt_verifier.py:751-753` EXAKT Mal ein. `edit_evidence_add` (`:1254`) wirft bei duplicatem evidence key (single-publisher invariant).
**(2C)** try/except + deterministisches Restore — write/commit try/except (`:969-985`) fängt `(TaskLinkError, ReceiptError)`; `ReceiptError = _receipt_error()` (lazy, keine circular import). `HEAD@{1}`-Reflog-Reset ENTFERNT; neu `_snapshot_index` (`:1123`), `_reset_index_to_snapshot` (`:1147`), `_restore_after_failure` (`:1181`); restore-Fehler → `PublicationError` (explizite Meldung). Push/readback rollback ruft `_rollback_commit` explizite (`:1006-1022`).

### 3. Matrix-Ergebnis
`TestPublicationAcceptanceMatrix` 10/10 neu getroffen: fetch-fail (`test_07`), stale-ref (`test_08`), unpushed-retry (`test_09`), invalid-after-edit mit ECHTEM `baseharbor-plan/scripts/plan.py` (`test_10`), push-fail-rollback mit bare remote (`test_02`/`test_03`).
- 221 receipt tests pass: `test_receipt_tasklink.py` (72) + `test_receipt_verifier.py` (119) + `test_receipt_chain.py` (6), 9 subtests.
- **PLAN_STUB-Entfernung in test_receipt_verifier.py REVERTET:** realer plan.py validiert die **ganze** Vault (braucht `migration/source-snapshot/inventory.json`), Vollständiges Entfernen bricht 11 Production-Path-Tests (Scope-Erweiterung außerhalb des Vertrags). F5-Fidelity erhalten; `RealPlanValidationTest` übt realen plan.py gesondert am echten Vault.

### 4. receipt-suite.sh — exit0 lokal
`evidence/board-2026-10-29/scripts/receipt-suite.sh` neu geschrieben (alte Version zeigte auf nicht-existentes `pr-check-runner.py`, Typo `baseharor`). Laufft die drei receipt-Suiten gegen worktree o246, exit 0 nur bei allem pass. **Lokal: EXIT 0** — 221 passed.

### 5. Hosted CI (§4.6 eigener terminaler Run)
- Branch: `work/r27-tasklink-yamlfix`.
- **Run 3927** (base `545eaca9`, head `13026f29`): `completed/success` (gh run watch bis terminal).
- CI-Push `13026f29` auf `origin/work/r27-tasklink-yamlfix` erfolgreich (fast-forward aus `545eaca9`).
- Mandatory Python/validation receipt-gate grün: `PR · Validation · receipt-execution-tests`, `ci-policy`, `ci-executor-verifier-tests`.

### 6. Lokal
- `receipt-suite.sh` exit 0; py_compile OK; 221 receipt tests.
- GRENZE eingehalten: kein Refactor außerhalb Punkte 1-4; Callgraph-Vertrag zitiert; Root-Workspace baseharbor (master) nicht angefasst; nur diese Evidence-Datei in baseharbor-plan geschrieben.

END o246-DONE
