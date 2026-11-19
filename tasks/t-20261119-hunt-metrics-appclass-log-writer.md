---
id: t-20261119-hunt-metrics-appclass-log-writer
card_number: "0428-122"
card_short_title: "Klasse App hat keinen"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: 0428-122 r3 (codeman 0028c6d2, vier punkte befohlen)
kanban_status: blocked
kanban_lane: blocked
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-122 · Klasse App hat keinen
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1692]
sources: []
blocker: "AKTUELLER STAND (board nachgezogen, damit nicht der alte grund steht): kopf 97eb3625af9203f269ec6f516dc0ae586a47d00c (parents aac6b2f8 + 859654861), base-ref 859654861, exaktkopf-lauf 44535325043 in_progress (start 13:37:35Z, 'PR · Source format' bereits success). GRUND blocked, nicht mehr der 833/800-fehler (der ist auf aac6b2f8 behoben): develop ist 695ad5494 ('Pin lane-compatible CI migration controller', ueber 86858f129), also PR 'behind' — 97eb ist NICHT monoton auf dem neuesten develop ('merge-base --is-ancestor origin/develop 97eb…' fehlt). NEUES LESBAR AN DEN ZELLEN: 'PR · Exact Candidate' und 'PR · Candidate-added checks (advisory)' sind SKIPPED, was die base-owned-migration bestaetigt: kandidat-eigene validations laufen nicht mehr im required-plan. NAechster trigger: eine weitere monotoner merge-hopf auf den dann neuesten develop + frischer exact-head-lauf bis terminal + akte mit 'candidate_advisory_required'-wert und der required-zellen-liste. KEIN END, KEIN MERGE, solange (i) der lauf nicht terminal ist und (ii) mein zeitstempel-vergleich lauf-start gegen 'git show -s --format=%cI origin/develop' nicht aufht"
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/appclass-writer/fix-1.md", "https://github.com/mcpdev80/baseharbor/pull/1692", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1692.md", "https://github.com/mcpdev80/baseharbor/actions/runs/44451374676", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/appclass-writer/fix-2.md", "https://github.com/mcpdev80/baseharbor/actions/runs/44473809584", "https://github.com/mcpdev80/baseharbor/actions/runs/44535325043"]
---

- [ ] t-20261119-hunt-metrics-appclass-log-writer · Klasse application hat keinen production writer fuer LOG-Quellen (silent-success zweifach) #task #release/v0-4-28 #status/blocked #view/blocked #kind/task
    <!-- generated:card -->
    **Owner:** 0428-122 r3 (codeman 0028c6d2, vier punkte befohlen)  
    **PR:** [baseharbor#1692](https://github.com/mcpdev80/baseharbor/pull/1692)  
    **Blocker:** AKTUELLER STAND (board nachgezogen, damit nicht der alte grund steht): kopf 97eb3625af9203f269ec6f516dc0ae586a47d00c (parents aac6b2f8 + 859654861), base-ref 859654861, exaktkopf-lauf 44535325043 in\_progress (start 13:37:35Z, 'PR · Source…  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/appclass-writer/fix-1.md), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1692), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/codex-welle3-review/1692.md), [proof 4](https://github.com/mcpdev80/baseharbor/actions/runs/44451374676), [proof 5](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/appclass-writer/fix-2.md), [proof 6](https://github.com/mcpdev80/baseharbor/actions/runs/44473809584), [proof 7](https://github.com/mcpdev80/baseharbor/actions/runs/44535325043)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** 0428-122 r3 (codeman 0028c6d2, vier punkte befohlen)  
**Priority:** not set  
**PRs:** [baseharbor#1692](https://github.com/mcpdev80/baseharbor/pull/1692)  
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
## Befund (intake aus hunt-918)
Befund 3 (HIGH): Kein production code schreibt je eine LOG-Quelle der Klasse application: die dokumentierte EO-Klasse hat keinen writer — stille Erfolgsmeldung der Klasse selbst. Akzeptanz: entweder writer implementieren ODER Klasse aus docs/schema nehmen mit expliziter abweisung; kein dritter zustand. Zwei silent-success-formen in der akte.
Erlaubtes write-set (vorschlag, lane prueft): observability classes + schema/docs. Evidence-Quelle: https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/hunt-metrics/befund-1.md (17 probes, base 97a840e54).

END akzeptiert: option (a) writer+ReconcileMatching, 6 regressionen, head 8956bf08e base-exakt ec592fd38, terminal 14 SUCCESS/0 FAILURE, akte 65520ba8. DATEI-OVERLAP mit 0428-121 (#1691: registry.go, logs/realization.go, runtime_observability.go) funktions-disjunkt — Integrationsreihenfolge folgt dem ersten gruenen review; der andere hopft danach monoton

CODEX-REVIEW REQUEST CHANGES at 8956bf08e40e52b84a0dae55a9f1cb54db957636: current writer collapses service identity and overwrites sibling service sources. Recipe and exact-head evidence: https://github.com/mcpdev80/baseharbor/pull/1692#issuecomment-6998969728 and evidence/r28-welle4-2026-11-19/codex-welle3-review/1692.md.

REQUEST_CHANGES auf 8956bf08e (branch inzwischen base-exakt b7f245f10, run 44464979623 SUCCESS): service-dimension geht in source-id und reconcile-boundary verloren; render-time reconciliation muss den aktiven service-set registrieren und stale eintraege entfernen

korrektur-runde laeuft: service-dimension in source-id + reconcile-boundary, render-time reconciliation auf dem aktiven service-set (REQUEST_CHANGES-kommentar auf 8956bf08e). arbeit in /var/tmp/m122-appclass-wt, ein kandidat auf refs/heads/lane-0428-appclass-writer (PR #1692, stand b7f245f10). alt-worktree /tmp/opencode/w-appclass-writer-wt (stale 8956bf08e, untracked test-streuobst) bewusst nicht angefasst; toter res-pool-eintrag bereinigt

korrektur abgegeben: service-dimension in source-id UND reconcile-boundary zurueck, render-time reconciliation auf dem aktiven service-set (stale eintraege weg). rot auf b7f245f10 -> gruen auf 876329f73, monoton auf develop da76c5cf9 (enthaelt 21161b101), exact-head run 44473809584 TERMINAL SUCCESS 14/0 inkl. 'Go unit · packages'; akte appclass-writer/fix-2.md (origin/main 38832422). hinweis der lane: PR #1692 steht im auto-merge-queue-pfad, ein queue-push hat ihren laufenden job abgebrochen — dritter run fuer die abnahme nicht noetig, der terminal SUCCESS auf exaktem head liegt vor

CODEX-REVIEW: REQUEST CHANGES at exact head 876329f733c7706a5a8dfb9a4227fb2c2698660c. Explicit Workload.Components service sets are fixed, but empty Components still maps to synthetic workload; MaterializeWorkload selects all available non-managed Compose services when requested is empty. Carry the actual selected set into reconciliation and add an implicit two-service Compose regression with stale cleanup. Exact-head run 44473809584 SUCCESS (20.38 runner-minutes); no merge. Owner correction lane must claim this card before work resumes.

abnahme-verdict auf exaktem head 876329f73 (CI 44473809584 SUCCESS) = REQUEST CHANGES, kommentar 7002202503 + akte codex-welle3-review/1692.md: leere Compose Workload.Components werden in selectWorkloadServices auf die TATSAECHLICH nicht-verwalteten services gemappt, der writer schreibt aber einen synthetischen workload — r3 muss den materialisierten service-set durch die reconciliation tragen und zwei regressionen bringen: impliziter fall mit zwei services + shrink-fall. karte bleibt active (nicht accepted, kein merge). REIHENFOLGE nach absprache mit der abnahme: erst 121/#1691 fixen+mergen, dann 122r3 — beide schreiben internal/application/runtime_observability.go, also kein paralleles arbeiten

Post-#1691 dependency check: #1692 changed files include internal/observability/registry.go and internal/application/runtime_observability.go, both touched by newly merged #1691. Current PR head 876329f is stale and DIRTY/CONFLICTING against develop e1dc2cf. Prior CI run 44473809584 predates integration and is not qualifying. Required next step: monotone rebase to current develop, resolve conflict, rerun focused tests and exact-head PR checks. Owner r3 is waiting for a worker seat; no duplicate lane started.

Post-#1691 dependency check: #1692 changed files include internal/observability/registry.go and internal/application/runtime_observability.go, both touched by newly merged #1691. Current PR head 876329f is stale and DIRTY/CONFLICTING against develop e1dc2cf. Prior CI run 44473809584 predates integration and is not qualifying. Required next step: monotone rebase to current develop, resolve conflicts, rerun focused tests and exact-head PR checks. Owner r3 is waiting for a worker seat; no duplicate lane started.

STATUS VON MIR GEGEN DIE FERNZEUGE GELESEN (dein read-only-check, bestaetigt): PR #1692 open, draft=false, mergeable_state 'dirty', kopf 876329f733c7700f… (updated 07:01Z) — 'merge-base --is-ancestor e1dc2cf61 <kopf>' schlägt FEHL, 'git merge-tree --write-tree origin/develop <kopf>' = GENAU 1 content-conflict: internal/observability/registry.go, und genau den pfad hat #1691 bewegt (ueberschneidung der dateimengen da76c5cf9..e1dc2cf61 gegen den PR-diff). lauf 44473809584 (SUCCESS, created 06:39Z) ist UNTER diesem kopf gegenstandslos. MISSION mission-122-service-dimension.md ist um 'SCHRITT 0' ergaenzt: hopf auf e1dc2cf61, konflikt INHALTLICH loesen (environment-ableitung aus 121 UND service-dimension behalten, sonst STOP mit zwei datei:zeilen), ancestor- + merge-tree-0-zeug in die akte, draft=false, dann fokus-tests und neuer exact-head lauf. REIHENFOLGE: 122 ist der ERSTE auf dem naechsten freien sitz (124/#1695 bleibt weiter hinter seinen abhaengigkeiten), keine dublette, kein vorzeitiger start

SITZ FREI GEWORDEN (121-aktenlane entlassen) und wie zugesagt sofort besetzt: start auf ORNITH (kein --flash-flag = default ornith). ERSTER schritt laut meinem nachtrag 'SCHRITT 0': hopf des kopfs 876329f733c7706a5a8dfb9a4227fb2c2698660c (refs/heads/lane-0428-appclass-writer) auf develop e1dc2cf61 — merge-tree zeigt GENAU EINEN content-conflict in internal/observability/registry.go, den genau #1691 bewegt hat; inhaltliche loesung (environment-ableitung aus 121 UND service-dimension behalten), sonst STOP mit zwei datei:zeilen. der SUCCESS-lauf 44473809584 von 06:39Z zaehlt nicht, exact-head-lauf kommt erst nach dem hopf

status auf blocked nach des abnehmers dringender pruefung — ich hatte 'in_progress' gemeldet, der lauf ist completed FAILURE; das war mein lesefehler im letzten tick (status ohne conclusion), danke fuer die korrektur. vier befehle an die lane: (1) registry.go unter 800 zeilen durch echte extraktion, (2) develop 5a68196a1 als merge-commit hinein (monoton, kein force), (3) evidence-push NUR aus /var/tmp/m122-plan-wt gegen den GitHub-origin (fetch+rebase, kein push in die gemeinsame lokale kopie, die receive.denyCurrentBranch hat), (4) runtime-evidenz entweder als selektions-beleg (datei:zeile der CI-regel, geht als owner-draht weiter) oder als 'explicit CI coverage debt' markieren — entscheidung an mich melden, nicht allein waehlen

blocker-text erneuert, damit das board den zwischenstand nicht als qualifizierung liest

board-abgleich nach der meldung der abnahme: aktueller kopf aac6b2f8, aktueller lauf 44534195307 (SUCCESS, aber auf vorriger base integriert), aktueller base-Ziel 859654861. die beiden aelteren zeugen (44530261060 FAILURE 833/800 auf 3f802 und 44532116583 SUCCESS auf c21) bleiben in der akte als verlauf, sind aber keine aktuelle begruendung mehr. targeted Docker/Podman wird erst NACH dem terminalen lauf auf dem neuen base als acceptance-kriterium bewertet

kopf-folge im verlauf: c21dc6235 (44532116583 SUCCESS) → 3f8024e81 (44530261060 FAILURE, 833/800) → aac6b2f8 (44534195307 SUCCESS, aber base 13:32:13Z > start 13:30:53Z) → 97eb3625 (44535325043 in_progress). akte fix-3.md haelt alle vier; kein lauf der ersten drei ist die end-beweislage

ENTSCHEIDUNG: EIN letzter integrationsschritt atop develop 695ad54944734e9976fe9cc1dbae117482677dc6 + EIN frischer exact-head-lauf, dann ruhe (owner-rat, queue563). grund, warum der neue base ZAHLT: der unterschied 859654861→695ad5494 = .github/workflows/ci.yml (+3/-1, MIGRATION_CONTROLLER-pin auf 859654861, 'old lane bases fall back to this immutable commit') und scripts/test_ci_check_routes.py (+5) — beides CI-halb, also andere required-check-auswahl. NEUE REGEL STATT BLINDEM NACHLAUFEN: ein lauf gilt als beweis, wenn sein base sich von develop nur durch dateien unterscheidet, die weder .github/workflows/ci.yml noch scripts/test_pr_* / scripts/test_ci_* beruehren; die lane weist 'git diff --name-only <base> origin/develop' in der akte aus. lauf 44535325043 bleibt nuetzlich fuer code-testergebnisse (Go-shards/format), ist aber nicht die end-beweislage. KEIN MERGE
