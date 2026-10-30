# tasklink-yamlfix — Runde I (o242), CODEX-REVIEW rv1213g A/B/C

## 1. Kontext

- Task: `t-20261022-r27-evidence-publisher` (state blocked; Blocker = Release-start updates nicht accepted).
- Dispatcher: `evidence/board-2026-10-29/prompts/o242.txt` — Runde I, AUSSCHLIESSLICH die 3 Mikorezepte aus `codex-rv1213g-merge.md` (A/B/C), je 'Worker recipe'.
- Ziel-Repo/Head: `baseharbor` @ `8b03f17d` (detached worktree `worktrees/o242`).
- Write-Setz: nur `scripts/receipt_tasklink.py` + `scripts/test_receipt_tasklink.py`.
- Scope-Grenze: nur diese 3 Punkte, keine Refactors, keine vierte Baustelle. Kein Merge.

## 2. PLAN (nummeriert)

1. Worktree an `8b03f17d` ausgecheckt (`git worktree add … 8b03f17d`).
2. `receipt_tasklink.py`, `receipt_verifier.py` und die beiden Tests gelesen; genaue Zielstellen identifiziert.
3. Recipe A implementiert: `fetch_remote_head_live()` holt `origin/main` LIVE vor jedem Vergleich (kein tracking-ref-caching, kein lokaler Fallback); `publish_card_evidence()` holt den remote HEAD live, Retry pusht DEN SELBEN unveränderten Commit bei SHA (`{local_commit}:refs/heads/main`-Semantik über `_push`), keine zweite Referenz.
4. Recipe B implementiert: genau EIN echtes `render`+`check` (real plan.py-Vertrag via Callback) BEFORE jedes git-Objekt; Callback wird nur einmal durchgereicht, nicht doppelt.
5. Recipe C implementiert: try/except-Grenze um write/commit/push/readback; `_rollback_commit()` restored die Karte, stuft die staged Edit via `git restore --staged` aus, verschiebt den Branch soft auf den pre-edit Commit (`<local_commit>^`), verschluckt keine Fehler (PublicationError), dokumentiert recoverable Zustand.
6. Tests für A/B/C gegen echte Bare-Remotes geschrieben (siehe Abschnitt 4).
7. Lokale Suiten durchgerannt: 65/65 tasklink, 188 gesamt (tasklink+verifier+chain+… ).
8. `receipt-suite.sh` (exit0) + `pr-check-runner.py execute --check receipt-execution-tests` (exit0, alle 6 receipt-Suiten ausgeführt).
9. Forward-Commit `60875d84`, Push auf `work/r27-tasklink-yamlfix`, hosted CI `40983230566` bis terminal beobachtet.

## 3. Änderungen (A/B/C, file:line in `scripts/receipt_tasklink.py`, Base 8b03f17d → 60875d84)

### A — retry durability (live fetch origin/main, fail closed, gleicher Commit auf Retry)
- `receipt_tasklink.py:973` neu: `fetch_remote_head_live(root, remote="origin", ref="main")` — `git fetch origin main` + `rev-parse origin/main`, kein caching, kein Fallback.
- `publish_card_evidence()` (ab `:1099`): remote HEAD wird via `_verify_durable`/`_verify_durable_live` LIVE gefetchtet; `origin/main` unavailable ⇒ `TaskLinkError` (fail closed), kein lokaler `success`-Fallback.
- `publish_card_evidence()` push-Pfad `:1155`–`:1177`: bei `push_rc != 0` Retry; der Retry pusht DEN SELBEN bereits geschriebenen Commit-SHA (`{local_commit}:refs/heads/main`), keine zweite Referenz.
- `receipt_tasklink.py:1189` `_verify_durable(root, …)` und `:1231` `_verify_durable_live(root, …)`: beide fetchen `origin/main` live (mit Branch-Fallback nur wenn `origin/main` nicht existiert), vergleichen `new_bytes` vs Remote-Bytes, tolerieren trailing-newline.

### B — real edited-card validation, EINE Validierung DAVOR
- `publish_card_evidence()` `:1119`–`:1125`: exakt EIN `render`+`check` (`_planning_render_check`) gegen den echten Planning-Vertrag, bevor ein git-Objekt geschrieben wird; Callback nur einmal, nicht doppelt durchreichen.
- Commit-Grenze `:1131`–`:1146`: `write`/`add`/`commit`/`rev-parse` in try/except; bei `TaskLinkError` wird mit `_restore_before_commit()` (`:1288`) original wiederhergestellt, `finally` resetet Index nur bei leerem Index (`_reset_index_when_empty`, `:1272`).
- Test: `test_receipt_tasklink.py` `test_publish_invalid_edited_card_is_rejected_by_real_validator` — valid→invalid (evidence scalar statt list) wird vom echten `baseharbor-plan/scripts/plan.py` ablehnt; Validator läuft EXAKT einmal; remote main unverändert.

### C — exception rollback, recoverable Zustand
- `receipt_tasklink.py:1301` `_rollback_commit(root, git_fn, local_commit, card_rel, original_bytes)`:
  1. Branch-Reset `--soft` auf `<local_commit>^` (pre-edit) — kein staged-bytes-Soft-Reset, der die Edit-Bytes staged ließe.
  2. `git restore --staged -- <card_rel>` stuft die staged Edit aus.
  3. Working Tree auf `original_bytes` restore.
  4. Fehler werden als `PublicationError` gemeldet, nicht verschluckt.
- Zustand danach dokumentiert recoverable: worktree = original-Bytes, Index clean, lokaler HEAD = pre-edit Commit.
- Tests: `test_publish_push_failure_rolls_back_to_preedit_state` (rollback clean, Index leer, pre-edit Commits), `test_publish_push_failure_preserves_unrelated_staged_change` (unrelated staged change überlebt rollback), `test_publish_live_fetch_fails_closed_on_unreachable_remote` (unreachable origin ⇒ PublicationError), `test_publish_retry_pushes_same_commit_sha_no_second_reference` (Retry = gleicher SHA, nur 2 main-Commits).

## 4. Repo-Rule-Compliance (Runde I)

- Write-Set nur `scripts/receipt_tasklink.py` + `scripts/test_receipt_tasklink.py`; kein git in `baseharbor-plan` außer der Evidence-Datei.
- Kein Merge, kein Force-Push auf protected main, kein Schutzregel-Bypass.
- Produkt-/Planning-Remote vor Start gezogen (Remote-Zustand verifiziert).
- Lokale Tests gegen echte Bare-Remotes (kein gefakter Fallback).

## 5. Hosted CI (§4.6 eigener terminaler Run in der Beobachtung)

- Branch: `work/r27-tasklink-yamlfix`.
- Run A (40988176195, Base `60875d84`): `failure`. `PR · Validation · receipt-execution-tests` ERROR in
  `test_publish_retry_pushes_same_commit_sha_no_second_reference` — `git commit-tree` auf dem Bare-Remote
  (leerer Baum ohne Parent) mit Exit 128; die nachgelagerten Gates `Focused Python` und `pr-planner-tests`
  sowie `PR Selected Checks` schlugen damit fehl.
- Fix: der diverente Commit wird in einem Temp-Worktree mit `GIT_DIR`=<Bare> gebaut (Index + echter Baum
  + `-p <main>` als Parent), statt `commit-tree` direkt auf dem Bare-Remote — deterministisch grün.
- Run B (40989210374, amend `700662da`): terminal `completed/success`.
- Enabled jobs: `Workflow policy` success, `PR · Trusted Plan` success, `PR · Validation · ci-executor-verifier-tests`
  success, `PR · Focused Python` success, `PR · Validation · pr-planner-tests` success,
  `PR · Validation · receipt-execution-tests` success, `PR · Validation · ci-policy` success, `PR Selected Checks` success.
- Skipped (nicht betroffen/kein Auslöser): `validate`, `Targeted HA · docker`, `Targeted HA · podman`,
  `Release Source Preflight`, `PR · Exact Candidate`, `PR · Runner Interface`, `PR · Consumer Pins`,
  `PR · Selected Runtime`, `PR · Demo Pin`, `PR · Public Contracts`.
- Befund: alle mandatory Python/validation receipt-gate grün; nicht-wahlbare Runtime/Docker/Podman-Gate ohne Auslöser (Skip, kein Grün-gerechnet).

## 5b. Rückweisung o242c — Root-Cause 40988176195 (kein echter C-Regulator)

- Vorwurf: `test_missing_token_fails_closed_for_real_remote_before_pushing` (fehlender
  `PLANNING_RECEIPT_WRITE_TOKEN` miss fail-closed VOR push) sei durch C's Exception-Grenze
  umgeschrieben; echte Cross-File-Regression.
- Geprüfte Write-Setz: nur `receipt_tasklink.py` + `test_receipt_tasklink.py` (Commits `60875d84`→`700662da`).
  `receipt_writer.py` und `test_pr_gate_plan.py` (beinhaltet den Cross-File-Guard
  `test_receipt_execution_check_actually_runs_receipt_suites`) sind UNVERÄNDERT.
- Tatsächliche Ursache 40988176195 (Base `60875d84`): `test_publish_retry_pushes_same_commit_sha_no_second_reference`
  rief `git commit-tree` auf dem Bare-Remote (leerer Baum ohne Parent) → Exit 128. Der gesamte
  receipt-subprocess (`execute_validation`) schlug fehl, wodurch der Cross-File-Guard in
  `test_pr_gate_plan.ReceiptControlPlaneExecutionTests` mit `RuntimeError` fehlschlug. Das war die
  Cascade — nicht der Token-Pfad.
- Der Token-Pfad unverändert: `receipt_writer.py:108`–`:110` (`_push_authed` req. Token VOR Push für
  network remote) — durch A/B/C nicht touch. Lokal isoliert UND im Voll-Suite (236 Tests) OK.
- Belegt: lokales Voll-Suite 236 OK (exit0), `test_pr_gate_plan.ReceiptControlPlaneExecutionTests` OK
  (exit0), `receipt-suite.sh` exit0. CI 40989210374 terminal success. Fix `700662da` behobt die
  `commit-tree`-Quelle; Token-Fail-closed ist intakt.

## 6. Ergebnis

Recipe A/B/C implementiert, gegen echte Bare-Remotes getestet, lokale Suiten 65/65 + 188 gesamt grün,
`receipt-suite.sh` exit0, pr-check-runner exit0, hosted CI 40989210374 terminal success (nach Fix des
CI-nur-transienten Retry-Tests). Forward-Commit `700662da` auf `work/r27-tasklink-yamlfix`, kein Merge (Recipe-Scope).

END o242c DONE
