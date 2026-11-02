# board-truth — Board-Wahrheit nachziehen (REST-AUFGABE)

**Mission:** `coordinator/missions/board-truth.txt`
**Owner-Direktive (2026-11-02):** 3 veraltete blocked-Karten selbstrichtiggestellt (750 accepted 8bc490ea, 766 dropped, postrun accepted 1252+1261, render+check 0 errors, gepusht). **REST:** nur pruefen, ob die anderen heutigen Mergel (1160, 1242, 1258?, 1259, 1260, 1261, 1262, 1241) ihre Karten-Eintrae/Resolutionen haben; fehlende ergaenzen; END_DONE mit Zaehler.
**Datum:** 2026-11-02
**Arbeitsdepot:** baseharbor-plan (origin/main, HEAD c4b655b)
**Rolle:** Worker (Ornith)
**Stop-Regel:** kein Produktcode, kein baseharbor-Repo-Schreiben, kein spawn

## PR-Status gegen Karten (live verifiziert via gh api)

| PR | Merge SHA | merged_at | Karte | Zustand |
|---|---|---|---|---|
| #1160 | a567ff46 | 2026-11-02 | t-20261101-deps-gatemap-1160 | accepted + evidence OK |
| #1242 | e0dce0d6 | 2026-11-01 | (keine eigene; #1259-Diagnose p1242diag referenziert) | ok |
| #1258 | c5c3fe6c | — | open (kein Merge) | **ausser Scope** |
| #1259 | 46307b75 | 2026-11-01 | t-20261101-p1242diag-gatemap-1259 | accepted + evidence OK |
| #1260 | 790e5426 | 2026-11-01 | t-20261101-deps-gatemap-1160 | accepted + evidence OK |
| #1261 | f2e43b0a | 2026-11-01 | t-20261030-postrun-nonpr-producer-skip | accepted (Owner) OK |
| #1262 | 048a806c | 2026-11-02 | **t-20261101-gatemap-1262 NEU** | accepted + evidence |
| #1241 | 1206db79 | 2026-11-01 | t-20261030-podman-quadlet-engine-probe | accepted + evidence OK |

## Erledigt

- #1262 hatte KEINE Karte -> neue Karte `tasks/t-20261101-gatemap-1262.md` angelegt:
  - Frontmatter: id, type=task, areas=[], release=v0.4.27, owner Ornith-Worker (lane gatemap-1262), priority high,
    depends_on [t-20261017-release-0-4-27-updates], repos mcpdev80/baseharbor, prs [#1262],
    resolution accepted, evidence [PR-URL, merge 048a806c].
  - Body: Gate-map follow-up (mirrors #1259/#1260), `scripts/pr-gate-plan.py` only.
  - Generierte Blocke via render/Check neu generiert; handgenerierte Blocke NICHT manuell editiert.
- `scripts/release_cycles.py sync` -> 28 Zykle synchronisiert; gatemap-1262 in release-0-4-27-prepare dep-Graph gewirkt.
- `plan.py render` + `plan.py check` => **0 errors** (1 erwartete warning: core-750 accepted trotz offener Abhaengigkeit cutover-pr3 — korrekt, laut Owner-Direktive).
- Auf main gepusht: `c4b655b` (working tree clean).

## ZAHLER (fuer END_DONE)

- **prs_geprueft = 8** (1160, 1242, 1258, 1259, 1260, 1261, 1262, 1241)
- **karten_neu = 1** (t-20261101-gatemap-1262)
- **karten_fix = 0** (die 3 stale Karten vom Owner selbstrichtiggestellt, nicht in dieser Lane)
- **check_errors = 0**
- ausser Scope: #1258 (open)

## END-DOKU

- Status: **END_DONE**
- push_SHA: c4b655b
- codeman agent post 35cdb02e-a3b3-4e6d-86f9-1cbb35822587: PENDING (letzter Schritt)
