# board-truth — Board-Wahrheit nachziehen

**Mission:** `coordinator/missions/board-truth.txt`
**Owner-Direktive:** 2026-11-02 (AUFGABEN-ZUSCHLAG — koordiniere Board-Schreiber, du bist einziger Plan-Repo-Schreiber)
**Datum:** 2026-11-02
**Arbeitsdepot:** baseharbor-plan (origin/main) — Planungsdepot
**Rolle:** Worker (Ornith)
**Stop-Regel:** kein Produktcode, kein baseharbor-Repo-Schreiben, kein spawn — nur Plan/Evidence-Änderungen

## PLAN-Checkliste

1. 6 blocked-Karten + zugehörige PRs gegen Live-Daten verifizieren
2. core-750: blocked→accepted via #1222 merge 8bc490ea
3. core-766: blocked→superseded (#1220 closed)
4. t-20261030-postrun-nonpr-producer-skip: blocked→accepted via #1252 (c8fe5cde) UND #1261 (f2e43b0a)
5. core-390: UNVERAENDERT blocked (wartet #1229)
6. t-20261017-release-0-4-27-prepare: UNVERAENDERT blocked (Release-Tor)
7. t-20261027-r27-cutover-pr3: #1226 STALE-DROP, blocked mit gefülltem Blocker-Feld (nur #1107 offen)
8. scripts/release_cycles.py sync
9. python3 scripts/plan.py render + check => 0 Fehler
10. regulär auf main pushen (nur Plan/Evidence)
11. Evidence-Doku + codeman agent post

## Endgültiger Board-Zustand (6 blocked-Karten, live verifiziert)

| Karte | Aktion | Begründung / Beleg |
|---|---|---|
| core-750 | blocked→**accepted** | #1222 merged 2026-11-02T01:20:49Z, merge_commit_sha 8bc490ea |
| core-766 | blocked→**superseded** | #1220 closed unmerged (head 5d5b5c30); cutover-pr3 #1226 STALE-DROP |
| t-20261030-postrun-nonpr-producer-skip | blocked→**accepted** | #1252 merged 2026-11-01T16:16:28Z (c8fe5cde) + #1261 merged 2026-11-01T23:10:41Z (f2e43b0a) |
| core-390 | UNVERAENDERT blocked | wartet PRSC/Merge #1229 (head 792ed1d1) |
| t-20261017-release-0-4-27-prepare | UNVERAENDERT blocked | echtes Release-Tor, 68/86 deps nicht accepted |
| t-20261027-r27-cutover-pr3 | UNVERAENDERT blocked | #1226 STALE-DROP, nur #1107 offen (head b83e4faa) — Blocker-Feld ausfüllen |

## END-DOKU

- Status: IN ARBEIT
- Karten_fix=3 (core-750, core-766, t-20261030-postrun), UNVERAENDERT=3 (core-390, release-0-4-27-prepare, r27-cutover-pr3)
- check_errors=0
- Codeman agent post 35cdb02e-a3b3-4e6d-86f9-1cbb35822587: pending
