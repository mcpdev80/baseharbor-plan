---
id: t-20261119-r28-en-docs-warning-term
card_number: "0428-131"
card_short_title: "EN-Dokumentation nennt das"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: w131-0428-131-endocshowpf (codeman 93521518, ornith:1) — uebernommen von bbd9132d
kanban_status: blocked
kanban_lane: blocked
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-131 · EN-Dokumentation nennt das
priority: ""
depends_on: [t-20261119-r28-prgate-docs-internal-json-mapping]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1697]
sources: []
blocker: "owner-draht karte 0428-144: der documentation-audit laeuft fuer diesen kandidat NIEMALS, weil scripts/pr-gate-plan.py die Doku-auswahl nur auf '.md'/'.rst' (plus README/CONTRIBUTING/CHANGELOG/mkdocs*.yml/site/) stellt; die stelle ist datei scripts/pr-gate-plan.py zeile 1195 (die 1189 der lane-akte zaehlt die elif-kette von oben, ist also dieselbe stelle). DEINE 3 GEAENDERTEN DATEIEN SIND docs/internal/*.json — genau die fallen durchs raster, daher beweist der grüne PR Selected Checks ueberhaupt NICHTS fuer deinen inhalt"
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/en-docs-warning-term/fix-1.md", "https://github.com/mcpdev80/baseharbor/actions/runs/44478483899", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1697.md", "https://github.com/mcpdev80/baseharbor/actions/runs/44559589447"]
---

- [ ] t-20261119-r28-en-docs-warning-term · EN-Dokumentation nennt das Marker-Wort 'Achtung' statt 'Warning' (i18n-drift nach 0428-126) #task #release/v0-4-28 #status/blocked #view/blocked #kind/task
    <!-- generated:card -->
    **Owner:** w131-0428-131-endocshowpf (codeman 93521518, ornith:1) — uebernommen von bbd9132d  
    **PR:** [baseharbor#1697](https://github.com/mcpdev80/baseharbor/pull/1697)  
    **Blocker:** owner-draht karte 0428-144: der documentation-audit laeuft fuer diesen kandidat NIEMALS, weil scripts/pr-gate-plan.py die Doku-auswahl nur auf '.md'/'.rst' (plus README/CONTRIBUTING/CHANGELOG/mkdocs\*.yml/site/) stellt; die stelle ist datei…  
    **Needs:** [t-20261119-r28-prgate-docs-internal-json-mapping](t-20261119-r28-prgate-docs-internal-json-mapping.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/en-docs-warning-term/fix-1.md), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44478483899), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1697.md), [proof 4](https://github.com/mcpdev80/baseharbor/actions/runs/44559589447)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261119-r28-prgate-docs-internal-json-mapping](t-20261119-r28-prgate-docs-internal-json-mapping.md)  
**Owner:** w131-0428-131-endocshowpf (codeman 93521518, ornith:1) — uebernommen von bbd9132d  
**Priority:** not set  
**PRs:** [baseharbor#1697](https://github.com/mcpdev80/baseharbor/pull/1697)  
**Source:** 
<!-- /generated:links -->

## Goal

One or two sentences: the observable outcome.

## Scope

- In scope:
- Out of scope:

## Acceptance

- Each criterion as a plain bullet. Do not use checkboxes here: only the card line above is a checkbox.

## Required checks

- **Modified features:** Inventory and adapt all affected existing unit, contract, integration, regression, E2E and native-runtime tests; add missing cases.
- **New features/providers (e.g. Perses Provider Contract):** Implement NEW dedicated positive, negative, authorization, ownership, error-path, compatibility and lifecycle tests wherever relevant. Passing unrelated existing suites is not sufficient.
- **CI integration and mapping are part of implementation:** Register every new/changed test in its package/test inventory and update existing test-to-gate mapping, selectors, relevant `REQUIRED_CLIENT_TESTS`/package equivalent, `scripts/pr-gate-plan.py`, `scripts/release-requirements.json`, and CI workflow paths/triggers where applicable. Coordinate reserved CI files with their owner; no new CI framework.
- **Mapping selection proof:** Verify affected paths select the required tests, unrelated paths do not unnecessarily select them, and the applicable stacked-PR, ready-for-review, develop and release workflows cannot silently bypass them. Unknown coverage broadens selection instead of failing open.
- **Hard acceptance gate:** For every required test provide exact SHA -> test ID -> mapped check/native gate -> trigger -> actual run URL/outcome. Missing test, registration, mapping, selection, trigger or real passing execution BLOCKS acceptance. Docker/rootless Podman each require independent live evidence when applicable; do not rerun unaffected checks needlessly.


- **Test binding (select exactly one):** ☐ normal (auto-discovered) · ☐ contract → add to `REQUIRED_CLIENT_TESTS` or the package equivalent in the same PR · ☐ new check → update `scripts/pr-gate-plan.py` and `scripts/release-requirements.json` in the same PR.
- Name every new or changed test (package, exact test ID, fixture/env and native runtime if applicable). Targeted checks for the changed area; broaden when impact is unknown.
- Record the existing CI validation/check or Docker/Podman native gate that actually executes each test, and which PR paths, develop integration event or release candidate selection triggers it.
- If coverage is absent, implement/register it in the owning CI lane before acceptance; prove positive selection for a relevant change and negative/non-selection for an unrelated change. Missing, skipped or failed mandatory execution is NOT PASS.
- For Docker/Podman tests, prove native Docker and rootless Podman/Quadlet separately where required; unit fakes do not replace live runtime evidence. Cross-repo tests run through existing develop/release acceptance, not a blocking independent PR gate.
- Handoff must identify exact source SHA, test -> CI gate -> trigger -> actual run/outcome, or mark explicit CI coverage debt as blocking. No new CI framework or full automatic PR matrix.

## Dependencies and file ownership

- Owned files or areas:
- Shared files: coordinate through the owning task.

## Handoff

- Current state, branch, PR and evidence links. Newest first.

## Purpose
Nebefund aus der live-verify-kette 0428-130 (akte evidence/r28-welle4-2026-11-19/verify-env-chain/befund-1.md): nach 0428-126 heisst das annerkennende marker im ausgelieferten EN-katalog 'Warning', die englische dokumentation (EN-branch der doku, inkl. decisions-/cli-texte) verwendet an mindestens einer stelle weiterhin 'Achtung'. severity niedrig, aber kartenwuerdig, weil die EN-doku damit ein wort zeigt, das der EN-CLI nie druckt — dieselbe klasse wie der von 0428-126 behobene rename-drift.

## Acceptance
- alle EN-doku-stellen fuer das marker sagen 'Warning' (grep-beleg: kein 'Achtung' in EN-dateien), deutsche texte bleiben bei 'Achtung'
- ein docs-check laeuft in der betroffenen CI-gruppe mit (bestehender docs-audit genuegt, keine neue workflow-datei)
- akte evidence/r28-welle4-2026-11-19/en-docs-warning-term/fix-1.md mit datei:zeile je fundstelle + gruenlauf

abgegeben: EN-doku an drei stelle auf 'Warning' gezogen (docs/de bewusst unveraendert), grep-kontrolle leer, head 3448f73e base-exakt develop da76c5cf9, PR #1697 clean, run 44478483899 TERMINAL SUCCESS (14 jobs gruen, rest durch if-bedingungen skipped), akte origin/main 084c3f93, host besenrein (docker 7 ambient vorher==nachher, podman 0)

CODEX-REVIEW: REQUEST CHANGES at exact head 3448f73e697cd7fdb1a338ef8422b5d484bbe814. Content scope passes; required documentation-audit check is absent from exact-head CI because docs/internal/*.json did not select it. Recipe: select the existing docs-audit gate for those paths (or use the approved exact-head hosted CI route that executes it), then record terminal SUCCESS. Run 44478483899 PR Selected Checks SUCCESS does not prove the skipped/unselected docs check. No merge.

inhaltlich ist die korrektur in Ordnung (drei EN-JSON-stellen, docs/de unveraendert) — die karte haengt an der gate-auswahl, nicht am text

ZUORDNUNG DER UNABHAENGIGEN REVIEW (auf bitte der abnahme, read-only): ziel = PR #1697 auf genauen kopf 3448f73e697cd7fdb1a338ef8422b5d484bbe814 gegen base develop 1019190d8dc0ecac7693f3461153e76be0e2cb8a. umfang: die 3 dateien des diffs, EN/DE marker-term 'Warning' konsistenz, und die frage, ob der documentation-audit die geaenderten pfade erwischt (wenn nein: datei:zeile der selektionsregel als befuind, dann wird es ein weiterer 114-draht-punkt). REGELN DAFUER: nur lesen, kein commit/push auf den zweig, KEIN merge, KEIN urteil ueber andere koepfe; ein urteil gilt nur fuer DIESEN kopf und faellt mit jedem develop-sprung, der .github/workflows/ci.yml oder scripts/test_pr_*|test_ci_* beruehrt (meine base-abstands-regel). UMSETZUNG etwaniger funde bleibt bei einer worker-lane, die ICH dispatche (§2: die abnahme implementiert nicht), und der sitz dafuer wird erst frei, wenn 089s korrektur-lane laeuft oder ornith-holds verfallen

KANDIDAT IST TADELLOS UND FERNSICHTIG BELEGT, von mir im selben schritt gelesen: zweig-head 708f5c5c8acee5133e480d151544cb139bb3ded3 per ls-remote, base = develop 1019190d8dc0ecac7693f3461153e76be0e2cb8a, mergeable_state clean, draft=false, 'git merge-base --is-ancestor origin/develop 708f5c5c8' = 0 (monotoner hopf, KEIN rewrite), lauf 44559589447 completed SUCCESS auf GENAU DIESEM kopf (created 15:51:54Z, updated 15:56:50Z, nach dem develop-commit 14:56:29Z), 'PR Selected Checks' success, 0 fehljobs; dein diff gegen develop = genau 3 dateien docs/internal/*.json. AKTE auf main: evidence/r28-welle4-2026-11-19/en-docs-warning-term/fix-2.md (commit 09cba8e2, 12 zeilen mit den 40er-shas/lauf-id). DER GRUND WARUM SIE TROTZGRDEM BLOCKED BLEIBT UND NICHT REVIEW: ein 'review' verlangt einen pruefbaren kanditaten MIT PASSENDER EVIDENCE (§5.1), und die fehlende stelle ist nicht deine arbeit: ohne die DOC_CHECKS-abbildung kann dich niemand unabhaengig pruefen, weil der audit nicht einmal gestartet wird. NACH dem owner-draht: ein einziger exact-head-lauf mit documentation-audit in der ausgewaehlten liste, dann review — du musst dafuer NICHT nochmal hopfen, der kopf 708f5c5c8 bleibt gueltig, solange develop ihn enthaelt

Independent read-only review on 2026-11-19: wording diff is correct, but exact-head run 44559589447 did not execute documentation-audit, strict EN/DE MkDocs or Pages; head 708f5c5 and base 1019190d are behind current develop 558dc42d. Rebase, prove the required docs acceptance on the refreshed exact head. See [review evidence](../evidence/r28-welle4-2026-11-19/codex-review-wave/1697-0428-131-independent-review.md).
