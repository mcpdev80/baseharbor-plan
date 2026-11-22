---
id: t-20261122-footprint-show-not-admitted-in-data-capabilities-gate
card_number: "0428-227"
card_short_title: "footprint show gate admission"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: 0847d100 (lane, mechanismus-auftrag)
kanban_status: active
kanban_lane: active
kanban_summary: "The disposable acceptance gates that legitimately call baha app footprint show are admitted by the CI operator boundary, so the…"
kanban_title: 0428-227 · footprint show gate admission
priority: ""
depends_on: [t-20261121-develop-full-suite-red, t-20261122-ci-integration-operator-seams-without-gate-admission]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1753]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/footprint-gate-admission/review-1753-headd690d7ffd4d5.md", "https://github.com/mcpdev80/baseharbor/actions/runs/44993125398", "https://github.com/mcpdev80/baseharbor/actions/runs/44994268323", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/footprint-gate-admission/review-1753-heada40b76764c3c0.md", "https://github.com/mcpdev80/baseharbor/actions/runs/44998829701", "https://github.com/mcpdev80/baseharbor/actions/runs/45008538769", "https://github.com/mcpdev80/baseharbor/actions/runs/45014558296"]
---

- [ ] t-20261122-footprint-show-not-admitted-in-data-capabilities-gate · Acceptance contract: baha app footprint show is admitted only for the guided gate #task #release/v0-4-28 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** 0847d100 (lane, mechanismus-auftrag)  
    **PR:** [baseharbor#1753](https://github.com/mcpdev80/baseharbor/pull/1753)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/footprint-gate-admission/review-1753-headd690d7ffd4d5.md), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44993125398), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44994268323), [proof 4](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/footprint-gate-admission/review-1753-heada40b76764c3c0.md), [proof 5](https://github.com/mcpdev80/baseharbor/actions/runs/44998829701), [proof 6](https://github.com/mcpdev80/baseharbor/actions/runs/45008538769), [proof 7](https://github.com/mcpdev80/baseharbor/actions/runs/45014558296)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261121-develop-full-suite-red](t-20261121-develop-full-suite-red.md), [t-20261122-ci-integration-operator-seams-without-gate-admission](t-20261122-ci-integration-operator-seams-without-gate-admission.md)  
**Required by:** [t-20261120-workload-port-flag-ignored-locally](t-20261120-workload-port-flag-ignored-locally.md)  
**Owner:** 0847d100 (lane, mechanismus-auftrag)  
**Priority:** not set  
**PRs:** [baseharbor#1753](https://github.com/mcpdev80/baseharbor/pull/1753)  
**Source:** 
<!-- /generated:links -->

## Goal

The disposable acceptance gates that legitimately call `baha app footprint show` are admitted by the CI operator
boundary, so the gate fails on the contract and not on the command shape. Today the admission exists only for
`gate == "guided"`; on the `data-capabilities` gate the same canonical call is rejected and the job dies with
`command-not-in-managed-workload-set`, which blocks unrelated cards that merely select that gate.

## Scope

- In scope: `cmd/baha/ci_integration_operator_enabled.go` gate-admission branches and their regression tests, plus the
  data-capabilities fixture's use of the footprint read.
- Out of scope: broadening the managed-workload set to arbitrary commands; any change that admits a mutation outside a
  selected disposable target.

## Acceptance

- One documented rule states for which gates `app footprint show` (canonical read-only form) is admitted, and why.
- The chosen shape is implemented either as an additional gate admission or by removing the footprint call from the
  data-capabilities fixture; the reason is recorded in the PR.
- A regression test proves both directions: admitted on the gate that needs it, still rejected as
  `command-not-in-managed-workload-set` on a gate that must not run it.
- The data-capabilities Docker job that previously failed passes on the exact candidate SHA in hosted CI.

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

- Owned files or areas: `cmd/baha/ci_integration_operator_enabled.go` and its `cmd/baha` tests.
- Shared files: coordinate through the owning task. `scripts/pr-check-runner.py` and `scripts/pr-gate-*.py` stay CI-owner
  scope; a change there must be requested as a finding with file:line, not edited by this card.

## Handoff

- Origin of this card, measured by the Coordinator on develop `7d4351c6d645353b6b96c8d320b4c832d55f9047`:
  - `cmd/baha/ci_integration_operator_enabled.go:135` admits the footprint read only under `gate == "guided"`, through
    `ciIntegrationGuidedFootprintShow` (`:232-233`, exact shape `app footprint show -o json`).
  - `:179-180` is the fail-closed branch that produced `command-not-in-managed-workload-set: app footprint show …`.
  - The command itself is registered as read-only elsewhere: `cmd/baha/machine_coverage.go:97` maps
    `baha app footprint show` to `app.footprint.show`, and `cmd/baha/app_registration_921.go:40,43` documents the
    `-o json` form.
- Failure witness: PR #1723 (card 0428-199) exact run `44963676934`, Docker data-capabilities job `137028211165`
  failed with the message above; the same job family also reported that operator authentication wants an interactive
  setup while the input is not a terminal (`cmd/baha/operator_auth_boundary.go:117`), which is the separate
  prerequisite tracked on card 0428-223 (PR #1750).
- Classification: this is a shared acceptance contract in product code, not Owner-scope CI files and not a defect of
  card 0428-199. It is blocked behind nobody; it can be staffed as soon as a seat is free.

hop delivered by 0847d100: refs/pull/1753/head 71deb610a03, back=0 against develop 6209874428f, PR draft=false, exact run 44972857723 in_progress. a second re-hop branch lane-0428-227-footprint-gate-admission-rh2 (43d85d637a0) exists as surplus, nothing deleted. the data-capabilities gate still depends on the path-to-gate mapping (card 0428-228, Owner-scope)

independent review at exact head 91f4e38795a gives VERDICT APPROVE content, merge blocked by card 0428-228 path to gate entry at scripts/pr-gate-plan.py line 180 (reviewer akte review-1753-head91f4e38795a.md)

Corrected candidate head ce5cf8f3037 (back=0, ahead=1) mit run 44986388874 SUCCESS und 0 failed jobs; der erste versuch e120f0815 war durch eine beschnittene datei ungueltig und CI hat das sofort gezeigt. Selected Runtime ist auch hier SKIPPED (job 137097832863), grund: fehlende components- und native_checks-zeilen, karte 0428-230.

review am exakten head d690d7ffd4d = APPROVE (akte footprint-gate-admission/review-1753-headd690d7ffd4d5.md auf origin/main e7a30bd6848). Exakter run 44993125398 SUCCESS/0 failed, operator-job 137118399949 PASS. Commit ce5cf8f3037 ist kartenarbeit (footprint operator seam plus test), keine fremde arbeit. Kein merge in dieser runde: die karten-abnahme will die Zulassung im native-gate BELEGT, und 'PR Selected Runtime' 137118401195 ist am kandidaten noch SKIPPED, weil PR 1756 (die katalogzeilen) noch nicht in der base liegt. Naechster schritt nach dem 1756-merge: weiterer additiver hop, ein run mit echten runtime-zeilen, dann merge.

MEILENPFAHL: nach dem PR-1756-merge (develop 52a3c5446f4) laufen die nativen runtime-gates WIRKLICH. Am dritten hop-head a40b76764c3 (base 52a3c5446f4, back=0) zeigt der exakte run 44994268323: 'PR . Native gate plan' SUCCESS (137121803257), 'PR . Selected Runtime' docker/data-capabilities job 137122169353 und podman/data-capabilities job 137122169299 sind AUSGEFUEHRT (in_progress, nicht skipped); 'PR . Native Keycloak/Core' skipped als unrelated. Exaktes review am selben head ist aktiv bei fecbada9. Vorbedingung war der 1756-merge - damit ist die zulassungs-kette zum ersten mal maschinell sichtbar statt still uebersprungen.

EXAKTER RUN FEHLGESCHLAGEN, kandidat bleibt unge mergt: run 44994268323 am head a40b76764c3 faellt auf BEIDEN engineen in TestApplicationCapabilityLifecycleExistingCore/secrets beim start des secure runtime brokers (native jobs 137121839425 docker und 137121839379 podman, selected-runtime 137122169353 und 137122169299, aggregate 137124048433); readiness 503 not_ready, timeout ~2m/~5m, mTLS-identity davor in ordnung. Additivitaet ist in ordnung (hop nur develop-inhalt, back=0). Verdict des reviewers: HOLD ohne merge-empfehlung. Der fehler ist NICHT fussabdruck-cli-semantik, sondern die erstmals AUSGEFUEHRTE nativ-reihe zeigt einen broker-readiness-defekt - dafuer ist karte 0428-237 angelegt (rerun am selben head plus datei:zeilen-diagnose).

REIHENFOLGE-ROLLE BESTAETIGT, ihr fall ist der SCHLUESSELkandidat des fensters: PR 1753 laesst 'baha app footprint show' als canonical command in die admitted-matrix der selected data-capabilities - ohne ihn bleibt PR 1762 (tmpdir) rot, egal wie sein test aussieht. Rueckstand nur 29 commits, 2 dateien in cmd/baha. SEIN EIGENER blocker bleibt 0428-237: der exakte durchgang 44994268323 scheiterte in den nativen reihen (docker 137133647957, podman 137133625738) am broker-readiness-fall. Kette damit: 0428-237 (arbeit auf f0f6c8b4) -> 1753 -> 1762 -> dann 1723, 1725, 1761. Kein unveraenderter rerun vorher.

MESSE STATT MEINUNG, vier protokolle selbst gezogen (gh api job-logs): selected-docker 137139969524 (PR 1725) zeigt wortlich den fehlgeschlagenen aufruf 'app footprint show -o json' plus 'operator/automation consent (--confirm-candidate); refusing to record deployment state' (achtfach im selben job, digest 9a4da90e4e0d60e54a45a1ccf16b2a147a53eb7c865fc67d87d9b837df509295); selected-podman 137139969537 ebenso (257 KB / 242 KB protokolle). In ALLEN vier gelesenen jobs (dazu 137139636770 und 137139636747 von PR 1761) steht 'readiness timeout' NULL mal und 'not_ready' GENAU EIN mal (podman 137139636747). SHARED BLOCKER DAMIT: die fussnoten-ZULASSUNG, also dieser kandidat und karte 0428-227 - NICHT die broker-chronologie 0428-237. Ich habe 0428-237 umgeschichtet (keine aenderung an internal/controlplaneruntime ohne wiederholbaren not_ready auf develop 8629450ef3c).

MESSE STATT MEINUNG, vier protokolle selbst gezogen (gh api job-logs, 72-257 KB): selected-docker 137139969524 (PR 1725) zeigt wortlich 'app footprint show -o json' plus 'operator/automation consent (--confirm-candidate); refusing to record deployment state' (achtfach, digest 9a4da90e4e0d60e54a45a1ccf16b2a147a53eb7c865fc67d87d9b837df509295); selected-podman 137139969537 ebenso. In ALLEN vier gelesenen jobs (auch 137139636770 und 1371396747 von PR 1761) steht 'readiness timeout' NULL mal, 'not_ready' GENAU EIN mal (podman 137139636747). SHARED BLOCKER = die fussnoten-ZULASSUNG (0428-227), NICHT die broker-chronologie 0428-237; 0428-237 habe ich umgeschichtet (kein eingriff in internal/controlplaneruntime ohne wiederholbaren not_ready auf develop 8629450ef3c).

MESSE STATT MEINUNG, vier protokolle selbst gezogen (gh api job-logs, 72-257 KB): selected-docker 137139969524 (PR 1725) zeigt wortlich 'app footprint show -o json' plus 'operator/automation consent (--confirm-candidate); refusing to record deployment state'; selected-podman 137139969537 ebenso. In ALLEN vier gelesenen jobs (auch 137139636770 und 137139636747 von PR 1761) steht 'readiness timeout' NULL mal, 'not_ready' GENAU EIN mal (podman 137139636747). SHARED BLOCKER = die fussnoten-ZULASSUNG (karte 0428-227), NICHT die broker-chronologie 0428-237.

MESSE STATT MEINUNG, vier protokolle selbst gezogen (gh api job-logs, 72-257 KB): selected-docker 137139969524 (PR 1725) zeigt wortlich 'app footprint show -o json' plus 'operator/automation consent (--confirm-candidate); refusing to record deployment state'; selected-podman 137139969537 ebenso. In ALLEN vier gelesenen jobs (auch 137139636770 und 137139636747 von PR 1761) steht 'readiness timeout' NULL mal, 'not_ready' GENAU EIN mal (podman 137139636747). SHARED BLOCKER = die fussnoten-ZULASSUNG (karte 0428-227), NICHT die broker-chronologie 0428-237.

HOP IST GELANDET, drchung laeuft: branch lane-0428-227-footprint-gate-admission zeigt jetzt auf b86440c3 mit base develop 8629450ef3c, exact durchgang 45008538769 ist AKTIV auf beiden nativen UND beiden selected data-capabilities-reihen (docker + podman) - das ist der erste kandidat, bei dem die reihen wirklich AUSGEFUEHRT statt skipped laufen. Kein fehlerschlagender job bis zu dieser messe. Damit haingt alles folgende an diesem einen durchgang: gruen -> unabhaengige pruefung durch fecbada9, dann merge; rot -> die zwei job-ids sind der beweis fuer die zulassungs-ursache. ZEUGE GEGEN MEINE FRUEHERE THESE: 'readiness timeout' NULL mal in den vier gelesenen protokollen, 'not_ready' genau EIN mal (podman 137139636747 von PR 1761); shared blocker ist die fussnoten-ZULASSUNG, diese karte.

HOP IST GELANDET, durchgang laeuft: branch lane-0428-227-footprint-gate-admission zeigt auf b86440c389b mit base develop 8629450ef3c; exact durchgang 45008538769 AKTIV auf beiden nativen (docker 137165488041, podman 137165488058) UND beiden selected data-capabilities-reihen (docker 137165839346, podman 137165839308), 'Selected Core-less' 137165589059 skipped - der erste kandidat, dessen matrix wirklich ausgefuehrt wird. Kein fehlgeschlagener job bis zu dieser messe. Zeuge gegen meine fruehere these: 'readiness timeout' NULL mal in den vier gelesenen protokollen, 'not_ready' genau EIN mal (podman 137139636747 von PR 1761) - shared blocker ist die fussnoten-ZULASSUNG, diese karte.

HOP IST GELANDET, durchgang laeuft: branch lane-0428-227-footprint-gate-admission zeigt auf b86440c389b mit base develop 8629450ef3c; exact durchgang 45008538769 AKTIV auf beiden nativen (docker 137165488041, podman 137165488058) UND beiden selected data-capabilities-reihen (docker 137165839346, podman 137165839308); 'Selected Core-less' 137165589059 skipped. Der erste kandidat, dessen matrix wirklich ausgefuehrt wird - kein fehlgeschlagener job bis zu dieser messe. ZEUGE GEGEN MEINE FRUEHERE THESE: 'readiness timeout' NULL mal in den vier gelesenen protokollen, 'not_ready' genau EIN mal (podman 137139636747 von PR 1761) - shared blocker ist die fussnoten-ZULASSUNG, also diese karte.

DIE EIGENTLICHE blockade, von der lane-diagnose und meinem exakten-head-protokoll bestaetigt: 'app footprint show' ist im Trusted-Gate-Registry (internal/gate-registry.go ~45) nicht als lesende operation zugelassen, wird wie eine kandidaten-mutation behandelt und loest die Consent-kaskade aus, an der alle vier runtime-reihen rot werden. PR 1753 fuegt das kommando ein, aberr NICHT die zulassung. Auftrag an 0847d100: registry-zeile ergaenzen (readend), echter hop auf develop, EIN durchgang bis terminal, ziel alle vier reihen green. Kein merge bis dahin.

ZWEI-URECHEN-AUFTEILUNG, DIREKT GEMESSEN AN RUN 45008538769 (head b86440c3): NATIV (docker 137165488041 + podman 137165488058) readiness timeout=0, not_ready=1, 'Starting secure runtime broker' 32x, '503' 17x -> DER BROKER meldet 503 NICHT-BEREIT im capability-lifecycle-test. SELECTED (docker 137165839346) not_ready=0, confirm-candidate=8 -> NUR consent. PR 1753 braucht BEIDE gruen, deshalb zwei getrennte fix-schritte auf DEMSELBEN branch. Diese karte deckt die SELECTED-seite: registry-zulassung von 'app footprint show' als lesend (0847d100 erhaelt beide schritte, registry-zulassung + broker-readiness, in einem branch, EIN durchgang, ziel alle vier reihen green).

TRIAGE am frischen head 22ff5345335 (durchgang 45011764715): der commit 'admit app.footprint.show as read operation in gate registry' aendert internal/operatorauth/local_runtime.go + test - DAS IST EIN GESPERRTER PFAD (AGENTS 5.6 / write-ban internal/operatorauth/**), SCOPE-VERSTOSS, Ruecknahme pruefen. INHALTLICH war die kommando-zulassung schon wirksam (ihr ci-operator-log bestaetigt 'app footprint show -o json admitted'). Der SELECTED-fehler ist daher NICHT mehr zulassung, sondern confirm-candidate=8 + CONTRACT-mismatch=4 (footprint json weicht von der erwartung ab) = KARTE 0428-241 (fixture/contract), plus consent als harness-verhalten. Fuer DIESE karte heisst das: die zulassung ist ERLEDIGT, ihr rest = contract-/consent-seite liegt bei 0428-241, und die NATIVE-seite bei 0428-237. PR 1753 bleibt offen.

#1753 dritter hop (head 73631921, run 45014558296) wieder FAILURE: selected docker+podman data-capabilities = 'app footprint show -o json' verlangt --confirm-candidate (show wird ALS MUTATION klassifiziert, 0428-227), dann 'contracts differ' (0428-241); NEU cli-1 + source-format fail = merge-format-regression. Mechanismus-auftrag an 0847d100: show-KLASSE auf read-only fixen (kein mutation-consent), dann contract, dann format. Wenn show danach consent verlangt: STOP + die klassifizierende datei:zeile, owner entscheidet. #1725 zeigt dieselbe consent-wurzel (nur runner-state, kein regress). PR bleibt offen.
