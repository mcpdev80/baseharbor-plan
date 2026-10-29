# tasklink-yamlfix Evidence (r27)

> Evidence-Datei fuer die YAML-Evidence-Edit-/Publish-Funktionen in
> `baseharbor/scripts/receipt_tasklink.py`. Strukturiert nach
> `baseharbor-plan/AGENTS.md` (Zeugnis-Pflicht, SHA-genau, fail-closed).

## Strategiewechsel F (o238)

PLAN (Schritte 1-6), erstellt 2026-10-29, Worker o238:

1. git worktree `/home/marcel/dev/baseharbor-ecosystem/worktrees/o238` bei
   SHA `29ccc9c2` (Kopf von `work/r27-tasklink-yamlfix`) — bereits existierend,
   verifiziert.
2. Implementiere `parse_card(text)`, `edit_evidence_add(original_bytes, url)`
   und den publish path (edit -> temp -> render/check -> commit -> push ->
   readback) + retry/idempotenz in `receipt_tasklink.py`.
3. Neue Testklasse `TestEvidenceEditDesign` in `test_receipt_tasklink.py`.
4. `receipt-suite.sh` (5 Suiten) exit0, Forward-Commit auf
   `work/r27-tasklink-yamlfix`, push, CI bis terminal beobachten.
5. Evidence unter ## Strategiewechsel F (o238) anhaengen, nummeriert ohne
   Checkboxen, letzte Zeile `END o238-DONE` / `END o238-BLOCKED`.
6. Kein Merge, kein git in baseharbor-plan (Datei OK).

ERGBNIS (o238, 2026-10-29): DONE.

1. DESIGN implementiert in baseharbor/scripts/receipt_tasklink.py:
   - `parse_card(text)`: frontmatter (zwischen 1./2. `---`) via
     yaml.safe_load getrennt vom KOERPER; KOERPER byte-faithful (trailing
     Newline erhalten).
   - `edit_evidence_add(original_bytes, url)` -> `(new_bytes, before, after)`:
     Document-Level-Rekonstruktion NUR des `evidence`-Schluessels, alle
     anderen Zeilen word-for-word; EXAKT ein evidence-key, url als HTTPS-
     Scalar; Duplikat-Pruefung (url bereits Ende der Liste -> TaskLinkError).
   - Format-Kosmetik: Flow-Form `evidence: [..]` -> Flow, Block-Form ->
     Block-Form (Schluessel- + Listenelement-Einrueckung aus Original
     uebernommen, gueltiges YAML), Scalar -> Scalar.
   - publish path (publish_card_evidence): edit -> working-tree staging ->
     render/check PFLICHT (Callback, None -> TaskLinkError VOR jedem git-
     Objekt) -> commit -> push -> readback origin/main byte-genau
     (_verify_durable, trailing-newline-normalisierung toleriert);
     PublicationError + Rollback bei readback-mismatch oder push-blockade.
   - retry/idempotenz: HEAD traegt target-url bereits -> (current_commit,
     True) ohne neuen Commit; teilweiser Fehlschlag (commit ja, push nein) ->
     Rollback, naechster Versuch findet denselben Stand -> keine Duplikate.
2. TESTS (new class TestEvidenceEditDesign, test_receipt_tasklink.py):
   golden fixtures fuer flow-list, block-list, nested metadata,
   empty evidence: []; jeder Roundtrip asserted byte-faithful KOERPER +
   EXAKT ein evidence-key; exception-rollback (bare remote, commit gesetzt,
   push geblockt) -> retry ohne Duplikat; publish durable commit+push+readback;
   idempotent second call (kein neuer commit); render-check failure blocks
   before commit; mandatory render-check; real baseharbor-plan plan.py check
   (path exists -> check+render exit 0). 16/16 green.
3. SUITE: 5 Python-Suiten (test_receipt_verifier, _postrun, _chain,
   _writer, _tasklink) => Ran 219 tests, OK. py_compile aller geaenderten
   Dateien OK.
4. COMMIT/PUSH: Forward-Commit `c4293237` on `work/r27-tasklink-yamlfix`,
   PR #1213 Kopf = `c4293237f099805f0e2c95075e895e2c4e2fc21a`.
5. HOSTED CI (Eigenes-Run-Pflicht, §4.6, bis terminal beobachtet):
   `gh run watch 40976218187` => `conclusion: success, status: completed`.
   Key gate: PR · Validation · receipt-execution-tests in 31s green.
   Run-ID 40976218187.
6. KEIN MERGE, KEIN git in baseharbor-plan. Abnahme + Merge obliegen
   Maintainer/Owner (CODEX-MERGE-Aktion bei full pass).

END o238-DONE
