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
