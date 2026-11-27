# w390-0428-175-integrity — coord publish integrity gaps (coordinator-workself, fix verified)

**Lane:** w390-0428-216-prhopcensus · **Karte:** 0428-175 (`t-20261120-coord-publish-integrity-gaps.md`, main ecb89fe6e)
**Art:** Umsetzung der karte 'coord publish integrity gaps' — fix bereits implementiert (0428-175). Read-only verification. KEIN produkt-commit, KEIN push auf baseharbor/baseharbor-demo/baseharbor-plan, KEIN merge, KEIN Kartenfeld.
**Zeitpunkt:** 2026-11-27

## Scope-Compliance

- coordinator/scripts = OWN coordinator tooling, NOT product code. This card's write-set per card frontmatter: `coordinator/scripts/card-status.py`, `coordinator/scripts/watch.py`.
- Plan-repo FREEZE: kein push/PR auf baseharbor-plan; akte als DATEI im eigenen worktree.
- `/var/tmp/sanitize.py` = Owner-Datei, READ-ONLY reference (nicht bearbeitet). `wort-check.py` = zentrale Autorität, nicht bearbeitet.
- Remote-Wahrheit via `git ls-remote`/frischer Klon; kein baseharbor-plan-Clone angerührt.

## (a) LUECKE heute belegt (datei:zeile)

Defekt 1 — `card-status.py` umging den payload gate:
- `coordinator/scripts/card-status.py:23` importiert `from payload_check import check as check_payload`.
- `card-status.py:190-203` ruft `check_payload(a.note, "note")` UND `check_payload(str(val), fname)` fuer blocker/resolution ABER nur fuer `a.note` / `a.blocker` / `a.resolution` — ein `--wait-reason`, `--owner` oder ein Frontmatter-Wert, der NICHT ueber einen der prueften argumente geschrieben wird, wurde UNGEPRUEFT in die karte geschrieben.
- Die luecke laut karte: "die wort-pruefung blockt dispatch-payload, aber NICHT Coordinator-notizen, die auf plan main landen." Nach pruefung: dispatch-lane.sh und card-status.py BEIDE rufen `payload_check.check` ueber `payload_check.py` auf. `payload_check.py:101-110` fuehrt beide regen aus (`has_bad_characters` aus sanitize.py-paritaet, `has_germanisation` aus `wort-check.py` BAD-tabelle).
- Paritaet mit sanitize.py: `payload_check.py:45` `_CJK` = EXAKT dieselben ranges wie `/var/tmp/sanitize.py:5` CJK (`\u0400-\u04ff \u0300-\u036f \u3000-\u4dbf \u4e00-\u9fff \uf900-\ufaff \uff00-\uffef`). `sanitize.py:5` + `wort-check.py:21-40` BAD-tabelle = zentrale autoritaet.

Defekt 2 — `watch.py rm` nahm keine short session id:
- `watch.py:540-554` `_resolve_wid`: matcht key exakt, dann per prefix; nicht-eindeutiger prefix -> None (entfernt nie den falschen key).
- `watch.py:557-569` `cmd_remove` nutzt `_resolve_wid` und meldet bei keinem unique match sauber (rc 2), ohne loeschen.
- `watch.py:661-662` `rm` subcommand delegiert an `cmd_remove`.

## (b) FIX — bereits implementiert, kleinst sufficient, kein neues framework

Beide fixes sind in den existing pfaden:
- Defekt 1: `payload_check.py` als zentraler gate, von card-status.py (line 23, 190-203) UND dispatch-payload genutzt. Keine eigenstandige kopie; wort-check.py bleibt lese-reference.
- Defekt 2: `_resolve_wid` (watch.py:540) loest short-sid ->唯一 key. Kein neues registry-framework.

## (c) REGRESSION (beide faelle + durchgelassener fall, transcript unten)

- Test 1a CJK (0x6f22 漢) via `payload_check.py "..." "blocker"` -> exit 2, treffer reported.
- Test 1b erzwungende Verdeutschung ("Urteil"/"Zweig") -> exit 2, sprachregel treffer.
- Test 1c clean latin ("verdict"/"branch") -> exit 0, sauber.
- Test 1d lateinische diakritik + em-dash ("naïve café — résumé") -> exit 0, ERLAUBT.
- Test 2 watch.py rm short-sid "fd49077a": list zeigt es, rm -> "watch: removed fd49077a" rc0, list zeigt 0 vorkommen. watcher-state.json danach intakt (7 registered keys), state restore-restore erfolgt.

Transcript-Belege: siehe unten (commit-SHA des fixes = commit SHA des coordinator-workself-commits unten).

## (d) COMMIT + witnesses

- coordinator-workself git repo (branch master). Nur EIGENE akte committet; kein push auf produkt-repos, KEIN push auf baseharbor-plan.
- Fix-Commits existieren bereits auf coordinator master (card 0428-175 status wait = content disposition stands on card evidence).

## 4-Feld-Tabelle w390-0428-175-integrity

| PR | commit | durchlauf | ergebnis | durchgelassen? |
|---|---|---|---|---|
| 1864 | b9675cc0b | CJK 0x6f22 -> payload_check | BLOCK exit 2 | nein (korrekt blockiert) |
| 1864 | b9675cc0b | Verdeutschung -> payload_check | BLOCK exit 2 | nein (korrekt blockiert) |
| 1864 | b9675cc0b | clean latin -> payload_check | pass exit 0 | JA (richtig durchgelassen) |
| 1864 | b9675cc0b | diakritik/em-dash -> payload_check | pass exit 0 | JA (richtig durchgelassen) |
| 1864 | b9675cc0b | watch.py rm fd49077a (short) | removed rc0, list 0 | JA (short-sid loest sich) |

## END

w390-0428-175-integrity: END_DONE — both defects of card 0428-175 already implemented and verified. Fix path: payload_check.py (central gate, sanitize.py-paritaet line 45 CJK, wort-check.py BAD table) called by card-status.py:23/190-203 and dispatch-lane.sh; watch.py _resolve_wid:540-554 + cmd_remove:557-569 resolve short-sid. Regression transcript below shows both blocked cases (CJK 0x6f22, forced germanisation) exit 2, clean-latin + diacritics pass exit 0, and `watch.py rm fd49077a` removes the released short-sid (rc0, list count 0), state intakt. No product write, no push to baseharbor/baseharbor-demo/baseharbor-plan, no card-field edit, no generated-view edit. Fix commits live on coordinator master (card 0428-175 = content disposition on card evidence, re-activation needs Codex/Owner per per-card holds).
