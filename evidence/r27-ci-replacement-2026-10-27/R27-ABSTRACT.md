# R27 ABSTRACT — CI-Replacement-Dossier (qwen LANE, dosr)

Lane: dosr (qwen) — R27 ABSCHLUSS-DOSIER im PLAN-REPO
Dossier-Quelle: /home/marcel/tmp-ops/m-dossier.txt
Datum: 2026-10-27

## SHA-KETTE (baseharbor/origin/develop)

| Commit-SHA | Oneline | PR-Referenz |
|---|---|---|
| `f4b173d3` | ci(r27): FINAL candidate 4f0ce579 (H chain) against develop@109ada8d (#1151) | PR #1151 |
| `7d8f3fdc` | fix(ci): native qualification tuple for the R27 receipt candidate (#1154) | PR #1154 |
| `44726f54` | docs(ci): re-register candidate 4f0ce579 (40-file receipt inventory) (#1152) | PR #1152 |
| `109ada8d` | docs(ci): drop stale 40-file register blocks (base drift from #1148/#1147) (#1150) | PR #1150 |
| `b53632aa` | ci: self-binding — planner carries H inventory (Q') | PR #1147 |
| `64f2edf7` | docs(ci): register Q' self-binding record (R') | PR #1148 |
| `4ab93266` | ci: target-side receipt candidate binding (Q) | PR #1146 |
| `7896416c` | docs(ci): register receipt candidate 4f0ce579d binding (R) | PR #1145 |
| `de568356` | fix(ci/F2): receipt-execution-tests runs the exact registered receipt suites (#1142) | PR #1142 |
| `3431b22c` | fix(credentials): port switch-back retention with provenance gate (#1096) | PR #1096 |
| `577aac4a` | ci(plan): pre-land projection qualification mapping (#1106) | PR #1106 |
| `43ea0d0c` | ci(r27): emit the approval commit as a downloadable patch (#1105) | PR #1105 |

## REVIEW-REIHE R1..R7 VERDICTS

### R1..R6 (historisch, aus board-2026-10-24/o117-akte1056.md)

- PR #1056 (`o90-planner-pr`): FAIL `BLOCKED: coverage-unresolved` + BEHIND.
  Akte zahlt auf `reviewed_head = 4e737e26...`, der KEIN Ancestor von `7a220d26` ist.
- PR #1060 (`qual`): PASS Run `40078059133`. Akte zahlt auf `reviewed_head = 3fa4989e...`,
  der EIN Ancestor von `7a3c4520` ist.
- **Kernbefund:** #1056 vs #1060 ist kein Akte-Mechanismus-Defekt, sondern ein
  veralteter `reviewed_head`-Wert in der #1056-Akte.

### R7 Verdict (aus evidence/g1/evidence-r27/g1.md)

Worker g1 (ornith, F1 lane) schloss R27 F1 (post-run publication) mit:
- F1.1 authenticated run/PR/artifact facts: VERIFIED. `verify_producer` weist `workflow_id`,
  `head_sha`, `pr_number` korrekt zu.
- F1.2 run id vs definition id: VERIFIED. `RUN_ID` ist live `workflow_run.id`.
- F1.3 real Planning plan commit: VERIFIED. `--plan` ist ein echtes Planning-Commit.
- F1.4 valid here-doc delimiter: VERIFIED. `bash -n` clean, exit 0.
- F1.5 scoped ephemeral auth/identity: VERIFIED. Ephemeral, least-privilege identity.
- F1.6 producer-definition trust: VERIFIED. Protected `main` only.
- Tests: positive + 2 negatives + discover. `g1.md` END-G1-DONE.

## R7a/b WIDERLEGUNGEN

### R7a: "Phantom-Incident" — Widerlegung

Die behaupteten "phantom" errors (z.B. `bash: warning: here-document ... wanted PY`)
sind KEIN Produktdefekt, sondern ein lokaler Skript-Error im ursprünglichen Decoder.
**Beweis:** g1.md F1.4 dokumentiert exakt diesen Fehler als "here-doc with `PY` (not a
delimiter) produced `bash: SyntaxError`". Das war ein Skriptfehler im W2-Input, nicht
eine systemische Produkt-Behauptung. Nach g1s Rewrite ist der Block `bash -n` clean
und exit 0. Phantom-Incident ist widerlegt durch g1 Evidence.

**Quell-Pfad:** `baseharbor/evidence/g1/evidence-r27/g1.md:63-68`
**SHA-Zeuge:** `de568356` → `f4b173d3` (F1 Fix auf develop integriert)

### R7b: "Shadow-Block" — Widerlegung

Die behaupteten "shadow blocks" (40-file register, stale Akte-Bindung) sind
KEIN unauflösbarer Block, sondern ein korrigierbarer Stand.
**Beweis:** PR #1150 (`109ada8d`) löste die stale register blocks explizit:
"drop stale 40-file register blocks (base drift from #1148/#1147)".
PR #1152 re-registrierte den Kandidaten frisch (40-file receipt inventory).
**Quell-Pfade:** `baseharbor/` log --oneline `109ada8d`, `44726f54`
**SHA-Zeuge:** `109ada8d` → `44726f54` (drift behoben, candidate re-registered)

## WIDERSPRÜCHE ZWISCHEN R-REIHE UND SHA-KETTE

1. R7 (g1 F1) dokumentiert einen korrigierten Decoder-Fehler, während R7a/b
   behaupten, dass "Phantom" und "Shadow" systemische Probleme seien — beide sind
   durch g1 Evidence und PR #1150/#1152 widerlegt.
2. Die drei R7a/b-Widerlegungen basieren auf:
   - `datei:zeile` aus g1.md:63-68
   - SHA-Referenzen aus develop-Log (`f4b173d3`, `7d8f3fdc`, etc.)
   - Kein Spekulations-Input — alles mit Pfad/SHA-Zeuge

## DOKUMENTIERTE QUELLEN

| Quelle | Typ | Pfad |
|---|---|---|
| board-2026-10-24/o117-akte1056.md | Evidence Board | `baseharbor/evidence/board-2026-10-24/o117-akte1056.md` |
| g1.md | Worker g1 Evidence | `baseharbor/evidence/g1/evidence-r27/g1.md` |
| develop-Log | SHA-Kette | `git -C baseharbor log --oneline origin/develop -12` |

## END MARKER

END R27-ABSTRACT-DOSR (dossier abgeschlossen)
