# R6 Belegsetz (in Arbeit)

LANE bz3 (ornith) — R6-BELEGSETZ. Belegset aus den Dossiers ci38b-kandidat.md, fx1-f1-wiring.md, tb1-trusted-base.md, d5-ci37.md, cmx3-merge-attempt.txt, CODEX-REVIEW-cb7d8213.md. Read-only; kein gh/PR/Produkt-Write, kein force/main-push. Arbeit nur im bz3-Worktree.

## PLAN
1. [☑] SCHRITT-NULL: skeleton, commit c9b46b6, push origin HEAD:work/r27-belegsetz3 (ls-remote: c9b46b66…)
2. [☑] (1) Zeitleiste SHAs
3. [☑] (2) F1-F8 je 1 Beweiszile
4. [☑] (3) BeweisLuecken-bis-Shadow-Run
5. [☑] (4) PR-Statistabelle

## (1) Zeitleiste SHAs
| Stufe | SHA | Rolle / Fund |
|---|---|---|
| develop (trusted BASE-Runner) | `3431b22c94b068f15f9bd7b31b9f87e846200f0f` | `fix(credentials): port switch-back retention with provenance gate (#1096)`; `origin/develop` HEAD; Basis für `unsupported executable validation`-Zirkularität (d5/ci38b/tb1) |
| v3.4 .. v3.8 (Kandidat R5-Integration) | `94f35d0293f8e237895afe84ae7aa9b26722ffed` | `stg6: integrate pcx FIX A + f1x plan-facts fix (corrected)`; PR #1138 head (`work/r27-correction-v38`), base=develop; 106 Commen ab 27507add; ci38b-/fx1-/CODEX-Kandidat |
| v3.8 Vorstufe (R4-Integration) | `cb7d821302b239bb04172527b2716f361afd79e5` | R5-Integration `8d12fbb40e4885d9e5b80cde949dd46ac9c60a05` als Ancestor; CODEX-REVIEW-Kandidat (Verdict BLOCKED) |
| R4 v3.6 Basis | `27507add` | stg3 v3.6 staging; F1b/F2/F6-Merge, Ancestor der v3.4..v3.8-Kette |
| R5 bootstrap / #1142 (Auflösung F1/F2) | `b9c3ba05bbfff99e72b4d4b9e8bf0d8989295d54` | `refs/heads/work/r27-boot-validator2` = `refs/pull/1142/head` (`ci(plan): minimal executable-validation bootstrap`), base=develop, MERGEABLE |
| v3.7 | `cdddf21d` | w5: add evidence for receipt execution-suite order fix (Ancestor v3.8) |
| v3.5 | `1c8e7993` | r5i: integrate R4 remaining; F2 receipt-execution suite-order fix (Ancestor v3.8) |
| planning main (dieses Vault) | `7ef5bc04e3ffac6cc77c3bd52fc723e7f87234ed` | `planning(r27): add evidence index for board-2026-10-27 (#11)`; bz3-Worktree-Startpunkt |

## (2) F1-F8 je 1 Beweiszile
Quelle `ci38b-kandidat.md` (94f35d02, Run 40614194159, SHA 94f35d0293f8e237895afe84ae7aa9b26722ffed):
- **F1** – PR · Focused Python, Klasse B: `ci38b-kandidat.md:46` `ValueError: unsupported executable validation` in `pr-check-runner.py:107 execute_validation`, ausgelöst durch `execute --check receipt-execution-tests` mit BASE-Runner develop 3431b22.
- **F2** – PR Selected Checks, Klasse B (abgeleitet): `ci38b-kandidat.md:52-53` `BLOCKED: required authenticated job not successful: PR · Focused Python` + `coverage-unresolved … pr-required-final.py pinned c6db56c4` (Base-Pfad).

Quelle `d5-ci37.md` (read-only, multiple PRs):
- **F1/F2 (Klasse A + B)**: `d5-ci37.md:26` `scripts/receipt_tasklink.py:453 – publish_evidence pusht unbedingt origin refs/heads/main` (F5, Fixture ohne origin-Remote → ERROR).
- **F2 (Klasse A policy)**: `d5-ci37.md:27` `scripts/test_ci_workflow_policy_receipts.py:117-145 (_find_dormancy_guard)` erkennt mehrzeiliges `if: >-` nicht → `FAILED (failures=2, errors=3)`.
- **F2 (Klasse B Zirkularität)**: `d5-ci37.md:28` `scripts/pr-check-runner.py:105-107 (develop 3431b22)` kennt `receipt-execution-tests` erst ab v35 → `unsupported executable validation`.

Quelle `tb1-trusted-base.md` (c6db56c4-Pin-Diagnose):
- **F2 (coverage-Basis)**: `tb1-trusted-base.md:846-848` `.github/workflows/ci.yml:846 git fetch --no-tags origin c6db56c4…`, `:848 git show c6db56c4:scripts/pr-required-final.py` → statischer Pin, kein develop-Nachfahre.
- **F2 (kein Nachfahre)**: `tb1-trusted-base.md:65` `git merge-base --is-ancestor c6db56c4 origin/develop → NEIN (EXIT 1)`; Pin verweist auf nicht-integrierte Branch.

Quelle `fx1-f1-wiring.md` (read-only Audit gegen 94f35d02):
- **F1 (Wiring)**: `fx1-f1-wiring.md:33-35` `test_receipt_postrun.py` ist über `pr-gate-plan.py:662 RECEIPT_CONTROL_PLANE_TEST_SCRIPTS` + `pr-gate-plan.py:681` `receipt-execution-tests` in CI gate eingewöhrt, aber kein direktes yml-Step.
- **F1 (Runner-Whitelist)**: `fx1-f1-wiring.md:49` `scripts/pr-check-runner.py:108` whitelist – indirekte Ausführung `execute --check receipt-execution-tests`.

Quelle `CODEX-REVIEW-cb7d8213.md` (R27 v3.8 REVIEW, Verdict BLOCKED):
- **F1**: `CODEX-REVIEW-cb7d8213.md:64-66` `receipt-post-run.yml:81-108,110-164,185-205,223-297` + `receipt_verifier.py:90-147` – post-run Path kann receipt nicht issue/publish.
- **F2**: `CODEX-REVIEW-cb7d8213.md:56` `ci.yml:655-660,733-738` protected-base-Runner ohne neuen Check + coverage-unresolved 21 paths; suite-order-Defekt CLOSED, Bootstrap pending.
- **F3**: `CODEX-REVIEW-cb7d8213.md:84-88` `receipt_writer.py:136-165,168-276` – retry verliert Plan, remote plan nicht erreichbar; receipt-only Recovery reicht nicht.
- **F4**: `CODEX-REVIEW-cb7d8213.md:94-100` `receipt_tasklink.py:47-126` vertraut issue-prose; `plan.py:78-79` Parser widersprechen bei duplicate prs.
- **F5**: `CODEX-REVIEW-cb7d8213.md:104-110` `receipt_tasklink.py:304-319` destructive card publication vor Validierung; validation optional und nach Push.
- **F6**: `CODEX-REVIEW-cb7d8213.md:116-118` `receipt_verifier.py:679-681,708-729` pinned reusable schema f57b30ed unkompatibel (TRUSTED_SOURCE leer).
- **F7**: `CODEX-REVIEW-cb7d8213.md:124-126` `receipt_verifier.py:44-50,248-278` CLOSED am Quell-/Test-Level; grün mit main/develop-Grenzen.
- **F8**: `CODEX-REVIEW-cb7d8213.md:128-134` `evidence-r27/r5i.md:36-40,63,69-70` verweist R4-Verbleib als pre-v3.6 ab; falsch, R4-Funde bleiben.

Quelle `cmx3-merge-attempt.txt` (Merge-Versuch #1142):
- **F2 (Gate-Sperre)**: `cmx3-merge-attempt.txt:1-6` `gh pr merge 1142 --squash --admin` → `Required status check "PR Selected Checks" is failing` (mergePullRequest, protected base).

## (3) BeweisLuecken-bis-Shadow-Run
| Lücke | Status | Blocker |
|---|---|---|
| Focused Python (F1/F2) auf 94f35d02 | rot, Klasse B | ci.yml fährt trusted BASE-Runner develop 3431b22, der `receipt-execution-tests` nicht kennt; Auflösung via #1142 (b9c3ba05) |
| PR Selected Checks (F2) | rot, abgeleitet | braucht grünes Focused Python + Base-seitige coverage-unresolved-Auflösung (pr-required-final.py@c6db56c4 kennt v3.8-Änderungdateien nicht) |
| Coverage-Mappings pr-required-final.py@c6db56c4 | offen | Pin ist kein develop-Nachfahre (tb1:65); v3.8-Änderungdateien unqualifiziert (ci38b:53, CODEX:56) |
| R5/Shadow-Run E2E (F1 post-run publish) | offen | CODEX F1/BLOCK: echter download/producer-format/authenticated-ID/publish-Shell nicht bewiesen; nur skeleton/PR-API-Lesung |
| R5 transaction integrity (F3/F5) | offen | F3 plan-ancestry, F5 card publication vor Validierung – keine echte Transaction bewiesen |
| F8 R5-Beweis gegen neutrale Basis | offen | r5i.md behauptet pre-v3.6-Auflösung; CODEX bestätigt R4-Fbleib als live defect |
| R4 suite-order (F2) | **grün** | planner 140 OK auf Host (CODEX:50); wiederverwendbar |
| Klasse A (F5 origin-ERROR, F2 policy) | **behoben** | 94f35d02: keine Klasse-A-UnitTest-Failure mehr (ci38b:47, CODEX:54) |

## (4) PR-Statistabelle (gh read-only state je Nummer)
| PR | Titel | base | head | head-SHA | state | mergeable | mergeable-with-rebase |
|---|---|---|---|---|---|---|---|
| #1138 | ci(r27): v3.8 staging - v3.7 + R5-Integration | develop | work/r27-correction-v38 | 94f35d0293f8e237895afe84ae7aa9b26722ffed | OPEN | MERGEABLE | — |
| #1142 | ci(plan): minimal executable-validation bootstrap | develop | work/r27-boot-validator2 | b9c3ba05bbfff99e72b4d4b9e8bf0d8989295d54 | OPEN | MERGEABLE | — |

Stand: 2026-10-28, read-only (`gh pr view/list --repo mcpdev80/baseharbor`). Kein rerun/dispatch/merge/Write.

END BZ3-DONE
