# Planning-Evidence-Index — board-2026-10-27

Stand 2026-10-28. Ein File für den Index; Quelle `baseharbor-plan/evidence/board-2026-10-27/`.
Erstellt durch LANE doc1 (ornith), Branch `work/r27-evidence-index`.

## Dossiers (Table)

| SHA | Datei | Zweck |
|-----|-------|-------|
| `551ef74922eb` | `b2-board.md` | B2 CardBoard sync 2026-10-27: prs/evidence/Blocker an 6 R27-Karten (v3.4/v3.5-v3.6 Wave-3), Status unverändert. PR #1125 (CLOSED) als v3.4-Kandidat; v3.6 PR #1134 (CLOSED), #1135 (CLOSED). |
| `1c8d0e9f7cfb` | `b4-board.md` | B4 CardBoard refresh R4 2026-10-27: prs += #1134/#1135, evidence + CODEX-REVIEW-27507add.md; R27-W-Karten bleiben review, shadow-run Blocker-Text aktualisiert. |
| `db8ec6c55c0d` | `ci1-repair.md` | ci1 W2-Reparatur HOST-CI-5: YAML-Parse-Fehler in `receipt-post-run.yml:107` (einzeiliger `python3 -c`), actionlint + ci-policy + gate-tests grün. PR #1115 (CLOSED). Tip-SHA `6c8aeef4e4cb`. |
| `58c296063ac1` | `d3-mergecheck-v36.md` | d3 READ-ONLY merge-tree Prognose v3.6-Kette (w4a/w4b3/w4c): Content-Konflikt in `scripts/test_receipt_verifier.py` (w4a×w4c); v3.6 ist keine grüne sequentielle Kette. SHAs via ls-remote frisch. |
| `912dac9e4c2c` | `diag1-ci-triage.md` | diag1 READ-ONLY CI-Triage PR #1115↔#1116 (kreuzabhängig, CATS=5/2/0); neuer Befund: Register-Lücke in `docs/internal/ci-binding-qualifications.md` (B, keine G-Nummer). |
| `611d6b9ec0de` | `f3b-fix.md` | f3b (ornith, `work/r27-fix-g3-publication`): G3a no-force-push, G3b bounded re-apply, G1b workflow-Übergaben, BF-W3-1 fail-closed. 122 Tests OK. Base `38771771`. |
| `ceb42526d0ce` | `i2-staging.md` | i2 V2-Partial-Integration: #1112 (#1112 pushswallow) + #1114 (tasklink) auf `work/r27-correction-v2`, Merge-Conflicts in erlaubtem Set, ci1-Territory nicht berührt. Merge-HEAD `38771771`. |
| `58c3b9cb96a5` | `p1-pilot-prereq.md` | p1 READ-ONLY Pilot-Vorprüfung (keine Promotion): gh-Token, GITHUB_*-Reads, PLANNING_RECEIPT_WRITE_TOKEN-Fluss, retained-no-workflow_id, 5 Gap-Liste für Pilot-Start auf main. |
| `332a0cf02c07` | `p3a-prep.md` | p3a (flash, scripts-only): pilot-run.sh/negatives.sh/capture-evidence.py/README — Doku-Skripte ohne Produktcode, Smoke-Tests rc=0. Write-Set disjunkt zu rv1/f1. |
| `ef15662b6289` | `pr3b-approve-contract.md` | pr3b (qwen): 6 neue ApproveIdentityTest-Fälle (5-Env-var fail-closed), kein Verhaltenswechsel, #1107 (CLOSED) DRAFT gegen develop. Commit `b83e4faa`. |
| `c662d95ce0af` | `rv1-review-ad4d0f28.md` | rv1 REVIEW (read-only): Kandidat PR #1111 @ ad4d0f28, 3 Pakete, 120 Tests (118 ok/2 BF-W3-1). Verdict ACCEPT_WITH_NONBLOCKING (BF-W3-1 + tasklink-Gap behebbar). |
| `3227d7ad84ba` | `rv3-review-f57b30ed.md` | rv3 (ornith) READ-ONLY v3.5-Vorprüfung: PR #1129 @ f57b30ed, D1/D2/D3 geprüft, 114/117 ok (3 Env-Fehler). End RV3-ACCEPT (Vorprüfung, keine Abnahme). |
| `9fd8af5d39bb` | `w1-evidence-final.md` | w1 evidence (PR #1109 @ 46a1c18d): F7 discovery gap + F6 shadow consumption fixed; receipt-execution-tests in selected CI, retained-only shadow. |
| `6ea667f66313` | `w2-evidence-draft.md` | w2 draft (PR #1108 @ 57f368ca): receipt/plan/task publication, F1/F2/F3; 47 tests OK, PLANNING_RECEIPT_WRITE_TOKEN externer Blocker. |
| `f9e99229109d` | `w2-evidence-final.md` | w2 final (PR #1108 @ 57f368ca): 16 writer + 31 tasklink tests OK, publish() FF/bounded-retry/idempotent. |
| `6aabf68f94d5` | `w3-evidence-final.md` | w3 final (PR #1110 @ a2d2e08c): genuine Owner/ref/producer identity + PR-auto-resolved approval + offline retained; 100 tests OK. |
| `a655650b0464` | `CODEX-REVIEW-27507add.md` | CODEX-R4 (v3.6 @ 27507add): BLOCKED — F1–F6 PARTLY, F8 OPEN; suite-order-Regression CLOSED; Class-B bootstrap separate prerequisite. |
| `1b8ca7473817` | `CODEX-REVIEW-804383ed3364.md` | CODEX-R3 (v3.7): Blocker-Dokumentierung am v3.6-SHA, reproduzierte PARTLY/OPEN-Blocker. |
| `44752ab10e60` | `CODEX-REVIEW-c7936e8bd838.md` | CODEX-R3 (v3.4): BLOCKED — F1–F6 PARTLY, F8 OPEN. |
| `b151266969c6` | `CODEX-REVIEW-cb7d8213.md` | CODEX-R27v5 (v3.8 @ cb7d8213): BLOCKED — F1–F6 PARTLY, F8 OPEN; suite-order-Regression CLOSED; D1–D3 PARTLY. |
| `307827898185` | `CODEX-REVIEW-f57b30ed48f1.md` | CODEX-R3 (v3.5 @ f57b30ed): PARTLY/OPEN-Blocker dokumentiert. |

## Sub-Dossiers / Skripte

| SHA | Pfad | Zweck |
|-----|------|-------|
| `e69de29bb2d1` | `cx-r27v4-27507add/*` | v3.6-R4 gefangene CI-/Probes-Logs (empty + nicht-empty). |
| `e69de29bb2d1` | `cx-r27v5-cb7d8213/*` | v3.8-R5 gefangene CI-/Probes-/Pin-Logs + trusted-pr-plan.zip. |
| `3d19416332dd` | `scripts/README-pr3-proof.md` | p3a: Pilot-Reihenfolge, Stopp-Kriterien, Platzhalter. |
| `456e377cc440` | `scripts/capture-evidence.py` | p3a: read-only gh→JSON Evidence-Capture. |
| `57aec05cb8f8` | `scripts/cx-r27v4-probes.py` | v3.6-R4 counterexample-Harness. |
| `a382fe8fbf5e` | `scripts/cx-r27v5-pin-probe.py` | v3.8 pin/interface probe. |
| `acb62cd9c86a` | `scripts/cx-r27v5-probes.py` | v3.8-R5 counterexample-Harness. |
| `0d7f3d2cce61` | `scripts/negatives.sh` | p3a: 3 kontrollierte Negative mit Fail-Erwartungen. |
| `647179805fd8` | `scripts/pilot-run.sh` | p3a: Positiv-Pfad als Doku-Skript (DryRun-Guard). |

## Querprüfung PR-Nummern (gh pr view --json state)

| PR | Repo | state | Bemerkung |
|----|------|-------|-----------|
| #1107 | mcpdev80/baseharbor | CLOSED | pr3b Owner-approve env contract (DRAFT gegen develop) |
| #1108 | mcpdev80/baseharbor | CLOSED | W2 automatic receipt/plan/task publication |
| #1109 | mcpdev80/baseharbor | CLOSED | W1 receipt control-plane suites + retained-only shadow |
| #1110 | mcpdev80/baseharbor | CLOSED | W3 genuine Owner/ref/producer identity + PR-auto-resolved approval |
| #1115 | mcpdev80/baseharbor | CLOSED | ci1 HOST-CI-5 actionlint parse error cascade |
| #1116 | mcpdev80/baseharbor | CLOSED | r27 G3/G1b no-force publication, bounded re-apply |
| #1125 | mcpdev80/baseharbor | CLOSED | v3.4 - v3.3 + approve-job outputs (F6 glue) |
| #1134 | mcpdev80/baseharbor | CLOSED | v3.6 staging Wave-4 integration (red-scope note in evidence) |
| #1135 | mcpdev80/baseharbor | CLOSED | w5 receipt execution-suite order fix |
| #1138 | mcpdev80/baseharbor | OPEN | v3.8 staging - v3.7 + R5-Integration (R5-Kandidat @ cb7d8213) |

Hinweis: b2/b4-Dossier nannten #1125 als OPEN; gh bestätigt CLOSED. Alle anderen Referenzen mit gh verifiziert.

## Referenzen

- CODEX-R27v5 (v3.8-Kandidat, aktuelle Runde): `evidence/board-2026-10-27/CODEX-REVIEW-cb7d8213.md`
