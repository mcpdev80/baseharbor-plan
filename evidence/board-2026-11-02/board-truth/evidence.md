# board-truth — Board-Wahrheit nachziehen

**Mission:** `coordinator/missions/board-truth.txt`
**Datum:** 2026-11-02
**Arbeitsdepot:** baseharbor-plan (origin/main) — Planungsdepot
**Rolle:** Worker (Ornith)
**Stop-Regel:** kein Produktcode, kein baseharbor-Repo-Schreiben, kein spawn — nur Plan/Evidence-Änderungen

## PLAN-Checkliste

1. gh api pulls?state=closed — letzte 12 merge-teete PRs sammeln
2. Für JEDE Karte prüfen: existiert Karte? fehlt Resolution/Evidence-Link?
3. Karten ergänzen/korrigieren (only YAML-frontmatter + Handtext-Bulletpunkte; generierte Blöcke nicht anfassen)
4. scripts/release_cycles.py sync
5. python3 scripts/plan.py render + check => 0 Fehler
6. regulär auf main pushen (nur Plan/Evidence)
7. Evidence-Doku + codeman agent post

## END-DOKU

- Status: IN ARBEIT
- prs_geprueft=0 karten_neu=0 karten_fix=0 check_errors=0
- Codeman agent post 35cdb02e-a3b3-4e6d-86f9-1cbb35822587: pending
