# tasklink YAML-Fix — Endfassung (o229)

## PLAN

1. Turn-Start-Pflichtprogramm abgearbeitet (basics-check.py), Events-ACK.
2. TASK-Vertrag o229 gelesen: BUGFIX in `scripts/receipt_tasklink.py` — die
   Zeile, die die Karten-Evidence-Zeile schreibt.
3. Fundstelle lokalisiert: `publish_evidence()` schreibt
   `- evidence: <url> (candidate <sha>, plan <sha>)` — kein gueltiges YAML.
4. Minimal-Fix: bare YAML-Listenelement `- <url>`; Kontext (candidate/plan)
   bleibt in der Commit-Nachricht.
5. Regressionstest in `test_receipt_tasklink.py` erganzt (YAML-Listentyp,
   https-URL, kein Inlining von candidate/plan).
6. Quartett der receipt-Suiten ausgefuhrt, exit 0.
7. Fix in approved worktree `worktrees/o229` gepickt, Committ, Branch
   `work/r27-tasklink-yamlfix` gepusht, PR gegen develop angelegt (Closes #1208).
8. Diese End-Evidence geschrieben.

## REPRODUKTION

Der automatisierte Tasklink-Schritt (`publish_evidence`,
`scripts/receipt_tasklink.py:363`) schrieb in die Planning-Karte eine
Evidence-Zeile der Form

    - evidence: https://...json (candidate 57a9c4a7..., plan eef674d0...)

Das ist KEIN gueltiges Frontmatter: `plan.py check` stoppt mit
`evidence must be https links`. Genau dieser Fehler stoppte rv1207b zusaetzlich.

## FIX

Datei: `scripts/receipt_tasklink.py`, Funktion `publish_evidence`.

Vor:

    evidence_line = "- evidence: %s (candidate %s, plan %s)" % (
        receipt_path, candidate_sha, plan_revision)

Nach:

    evidence_line = "- %s" % receipt_path

Die Commit-Nachricht behalt den Kontext:

    "tasklink: publish evidence %s for task %s (candidate %s, plan %s)"
    % (receipt_path, task, candidate_sha, plan_revision)

Damit ist die Evidence-Zeile ein sauberes YAML-Listenelement (`- <url>`),
das `plan.py check` als gueltigen https-Link akzeptiert; candidate/plan
wandern in die Commit-Nachricht, nicht in die Karte.

## TESTAUSGABEN

Quartett (alle receipt-Suiten), `scripts/`:

    python3 -m pytest test_receipt_writer.py test_receipt_verifier.py \
        test_receipt_chain.py test_receipt_tasklink.py
    126 passed in 17.50s

Neue Tests in `test_receipt_tasklink.py`
(`TestPublishEvidenceYamlFormat`):
- `test_evidence_entry_is_valid_yaml_list_element` — publish_evidence schreibt
  `- <url>` (kein `candidate`/`plan`-Text auf der Karte und im
  durable read-back).
- `test_evidence_not_inlined_with_candidate_plan` — Karte enthalt nicht
  `candidate` bzw. `plan <sha>`.

`test_receipt_tasklink.py`: 32 passed.

## EVIDENCE / MERGE

- PR: https://github.com/mcpdev80/baseharbor/pull/new/work/r27-tasklink-yamlfix
  (body: `Closes #1208`)
- Branch: `work/r27-tasklink-yamlfix` (worktree `worktrees/o229`)
- Fix-Patch-Quelle (commit in der Quelle): `c845caf6`
  (auf worktrees/o229 gepickt als `4ef5edd9`)
- Kein Merge, kein git in baseharbor-plan (Task-Vertrag).

o229-DONE

## Korrekturrunde B (o230)

1. Befund: o229s Fix `c845caf6` (bare `- <url>`) war bereits als PR #1213-HEAD
   gepusht, aber die VERIFIKER-Suite `test_receipt_verifier` schlug an:
   `test_approve_pr_happy_path` und `test_approval_pushes_only_through_writer_mechanism`
   sowie 4 weitere (insg. 5 FAIL + 1 ERROR) warteten auf das in `develop`
   committede, unter `evidence:` geschachtelte Format
   `- evidence: <url> (candidate <sha>, plan <sha>)`.
2. Diagnose (o231): `c845caf6` hatte neben dem Format auch die F5-Guard-Routine
   (`git fetch origin/main`, `require(remote_head == local_commit)`,
   `sha40(candidate/plan)`, `git push origin main`) entfernte und damit eine
   local-only read-back eingefuhrt.
3. BEHEBEN: sauberes forward-Revert `63a7824d` auf `c845caf6` in
   `worktrees/o230` (Branch `work/r27-tasklink-yamlfix`), das develop's
   geschachteltes YAML + alle F5-Guards wiederherstellt.
4. ZUSATZ (Rezept o231, Punkt 3): Regressionstest `PublishEvidenceYamlFormat`
   in `test_receipt_tasklink.py` — (a) valides YAML-Listenelement auf origin/main,
   (b) `test_rejected_push_fails_closed` fail-closed mit `TaskLinkError`, wenn
   der Push origin/main nicht erreicht.
5. TEST (vollstaendige 5-Suiten):
   `python3 -m unittest test_receipt_verifier test_receipt_postrun test_receipt_chain test_receipt_writer test_receipt_tasklink`
   => `Ran 191 tests ... OK`.
6. COMMITS: `63a7824d` (Revert) + `5f0504d0` (F5 YAML-list regression +
   fail-closed readback).
7. PUSH (fast-forward, kein Force): `c845caf6..5f0504d0 -> work/r27-tasklink-yamlfix`.
   Neue exakte HEAD-SHA: `5f0504d0fb79d1941f8f7867960b56236fc42803`.
8. PR #1213: OPEN, HEAD = `5f0504d0`. Kein Merge, kein git in baseharbor-plan.

o230-DONE

## Runde C (o232, product path fixed)

1. SETUP: worktree `worktrees/o232` zu `5f0504d0` angelegt; Remote-Branch
   `work/r27-tasklink-yamlfix` war bereits exakt auf `5f0504d0`, kein Push
   noetig (Recipe SETUP: Forward-Push ohne Force). NET-DIFF zu develop
   enttaelt nur `scripts/test_receipt_tasklink.py` (product fix war im Forward
   versehentlich reverttriert).
2. FIX (Produkt-Pfad) `scripts/receipt_tasklink.py` `publish_evidence`:
   `evidence: []` wird durch einen einzelnen `evidence:`-Block mit
   2-space-indentierten `<url>`-Listen-Items ersetzt, bestehende `- <url>`-Items
   werden erhalten (additiv), candidate/plan nur in der Commit-Nachricht,
   sha40-Guards fuer candidate_sha/plan_revision, render/check BEFORE push,
   Push zu origin/main + Remote-Readback (fail closed). Vorheriges gebrochenes
   `- evidence: <url> (candidate <sha>, plan <sha>)` entfaellt.
3. FIX (Regeln) Regressionstests AUF PRODUKTPEAD: `test_receipt_verifier.py`
   `test_publish_evidence_schema_valid_and_preserves_existing` auf echtes
   Bare-`origin` + `plan.py`-Schema umgestellt (kein `render_fn=None`-Kurzkick),
   `test_receipt_tasklink.py` `PublishEvidenceYamlFormat` auf geschachtelten
   Block + sha40-valide Inputs korrigiert. Fall-Matrix: absent evidence,
   existing evidence erhalten, unnaechte Nested-Metadata erhalten,
   Idempotenz-Retry, Remote-Fehlschlag fail-closed, render/check blockiert vor
   Push.
4. FIX (Voll-Suite 5 Dateien):
   `python3 -m unittest test_receipt_verifier test_receipt_postrun
   test_receipt_chain test_receipt_writer test_receipt_tasklink`
   => `Ran 191 tests ... OK` (exit 0). py-compile aller 3 geaenderten Dateien
   OK; yaml-parse aller `.github/workflows/*.yml` OK.
5. FIX (Commit/Push): Forward-Commit `ba24541e` auf `work/r27-tasklink-yamlfix`,
   Fast-Forward-Push nach origin (`5f0504d0..ba24541e`), PR #1213 Kopf =
    `ba24541e2d0a2a07a1eef982fce5bac51ea4a3a1`.
 6. CI Check-Run-ID: `40949715746` (PR Selected Checks; Focused Python +
    Validation-Jops liefen, restliche nicht-ausgewaehlte Jobs skipped).
 7. Kein Merge, kein git in baseharbor-plan (Task-Vertrag).

 END o232-DONE

## Runde D (o233)

 1. SETUP: worktree `worktrees/o233` zu `ba24541e` (PR #1213-HEAD Runde C)
    angelegt; Branch `work/r27-tasklink-yamlfix` war exakt auf `ba24541e`.
    Task-Vertrag o233 + CODEX-REVIEW `codex-rv1213c-merge.md` vollstaendig
    gelesen: BEIDE Blocking findings sind zu korrigieren, o233 fuehrt aus und
    merkt NICHT.
 2. REPRODUKTION FINDING 1: `publish_evidence()` in `scripts/receipt_tasklink.py`
    recognierte per Zeilenraterai (`re.fullmatch`) nur `evidence: []` und block
    `evidence:`, NICHT die inline-flow Form `evidence: ["https://..."]`
    (echtes Beispiel: `tasks/core-896-runners-isolate-parallel-pr-checks.md:17`).
    Ein einzelnes `evidence`-Schluessel wurde doppelt angehaengt.
 3. FIX FINDING 1: echtes YAML-Python (`yaml.safe_load` auf Frontmatter).
     - `publish_evidence` parst die Front-matter durch `yaml.safe_load`,
     recogniert damit ALLE Formen (leeres `[]`, Block `  - ...`, Inline-Flow
     `["https://..."]`); kein Prior-Evidence-Verlust.
     - `existing_items` speichert RAW-Werte; Idempotenz vergleicht raw gegen
     `receipt_path`, Re-Emission als `  - <url>` (schema-valider Block). Der
     vorherige Bug (`item.strip() == evidence_entry.strip()` lieferte
     `evidence/...` vs `- evidence/...`, Idempotenz gebrochen) ist behoben.
     - alle anderen Front-matter-Schluessel + Body byte-weise erhalten.
 4. FIX FINDING 2: `_render_check()` ist jetzt fail-closed — `None` =>
    TaskLinkError (kein stilles "ok"); render/check laufen VOR jedem
    Write/Commit/Push. `receipt_verifier.py` ruft `publish_evidence` in
    `publish_approval` MIT `render_fn=plan_render_check, check_fn=plan_render_check`
    auf; `plan_render_check` fuehrt `plan.py render` + `plan.py check` aus
    (beide muessen exit 0 haben, sonst fail closed).
 5. TESTS (neu, `PublishEvidenceYamlFormat` in `test_receipt_tasklink.py`):
     (a) `test_flow_list_card_preserves_old_and_new_scalar` — echte core-896
     Flow-Karte, alter+neuer Skalar nach Publikation auf origin/main belegt,
     Metadata erhalten; (b) `test_invalid_card_fails_closed_before_remote` —
     malformed YAML => TaskLinkError, origin/main unveraendert (bare remote);
     (c) `test_idempotent_retry_no_second_card_commit` — Retry liefert dieselbe
     SHA (kein zweiter Card-Commit); (d) `test_metadata_preserved_byte_wise` —
     alle non-evidence Keys + Body byte-weise belegt.
     ZUSAMMEN: `test_receipt_tasklink.py` 36 Tests OK.
 6. QUALITAET (5-Suiten, exit 0):
     `python3 -m unittest test_receipt_verifier test_receipt_postrun
     test_receipt_chain test_receipt_writer test_receipt_tasklink`
     => `Ran 196 tests ... OK`. py-compile aller 3 Produkt-/Testdateien OK.
 7. COMMIT/PUSH: Forward-Commit `db8b2b05` auf `work/r27-tasklink-yamlfix`
     (kein Force; Forward moeglich, Branch war auf `ba24541e`).
     Fast-Forward-Push nach origin (`ba24541e..db8b2b05`). PR #1213 Kopf =
     `db8b2b05e51b01599c5050a75ffca2dc24328d52`.
 8. HOSTED CI (Eigenes-Run-Pflicht, bis terminal beobachtet):
     `gh run watch 40957017276` => `conclusion: success, status: completed`.
     Alle Required Checks success (PR · Focused Python,
     PR · Validation · ci-executor-verifier-tests,
     PR · Validation · receipt-execution-tests, PR · Validation · ci-policy,
     PR · Trusted Plan, Workflow policy); HA/Docker/Podman/Validate/Jobs
     skipped (nicht betroffen). Run-ID 40957017276.
 9. KEIN MERGE, KEIN git in baseharbor-plan. Abnahme + Merge obliegen
     Maintainer/Owner (CODEX-MERGE-Aktion bei full pass).

 END o233-DONE
