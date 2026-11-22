---
id: t-20261122-impact-consent-after-preview-contract
card_number: "0428-226"
card_short_title: "impact consent validated after"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: w21-pr1702-0428-142-compat
kanban_status: wait
kanban_lane: wait
kanban_summary: Define and enforce one consent contract for env destroy so that an impact consent produced by a preview is still authoritative…
kanban_title: 0428-226 · impact consent validated after
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: "Owner-Push auf cli2-env-delete (PR #1627): Patch round-2-proposal-i.patch.md ist fertig und 'git apply --check' ist sauber gegen b3b0c2c9efc; naechster ausloeser ist der neue exakte PR-run nach ihrem push"
resolution: ""
evidence: []
---

- [ ] t-20261122-impact-consent-after-preview-contract · Env destroy: impact consent validated after preview is structurally stale (five fixture rounds) #task #release/v0-4-28 #status/wait #view/wait #kind/task
    <!-- generated:card -->
    **Owner:** w21-pr1702-0428-142-compat  
    **Waiting:** Owner-Push auf cli2-env-delete (PR \#1627): Patch round-2-proposal-i.patch.md ist fertig und 'git apply --check' ist sauber gegen b3b0c2c9efc; naechster ausloeser ist der neue exakte PR-run nach ihrem push  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w21-pr1702-0428-142-compat  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Define and enforce one consent contract for `env destroy` so that an impact consent produced by a preview is still
authoritative when the destroy applies it, on both Docker and rootless Podman. Today the equality test between the
preview consent and the destroy-time authorization fails, and the native test
`TestEnvironmentDestroyNativeLifecycle` reports `stale impact consent after preview` in hosted CI.

## Scope

- In scope: the consent issuance/validation path that the destroy authorization checks (preview object identity,
  resolved deployment UUID, stop-plan/stop-mode binding and the runtime retirement binding), plus the native test
  fixture that has to present exactly the production shape.
- Out of scope: weakening or removing the stale-consent protection; any change that lets a destroy run without a
  freshly authorised plan.

## Acceptance

- A single documented contract states which fields bind a preview consent to its destroy apply, and where each field is
  re-resolved at apply time.
- `TestEnvironmentDestroyNativeLifecycle` executes (not skips) and passes on the exact candidate SHA in hosted CI for
  both the Docker and the rootless Podman coreless-lifecycle shards.
- One deterministic assertion proves the consent is rejected when the resolved target changes after preview, so the
  protection is regression-tested, not just satisfied.
- The five-round fixture-patch sequence on PR #1627 is replaced by at most one further change round whose diff names
  the contract line it satisfies.

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

- Owned files or areas: the consent issuance/validation path in the destroy authorization, and the native destroy test
  fixture. The `env destroy` branch `cli2-env-delete` (PR #1627) stays Owner-owned; this card does not take it over.
- Shared files: coordinate through the owning task.

## Handoff

- Origin of this card: five consecutive failed attempts on one assertion in
  `cmd/baha/env_destroy_integration_test.go:128` (`stale impact consent after preview`) across heads `8de37f58caa`,
  `62dd38f9b6d`, `ac05cc4efbc`, `38be89aa4a0` and `b3b0c2c9efc`. Both required engine shards failed on the exact run
  `44961334018`: Docker job `137020935578` and Podman job `137020935792`, log lines 1178-1192 resolving
  `prod/docker-dev` and the target deployment.
- Current state: PR #1627 (`0428-055`) is held from review and merge; a read-only diagnosis of the preview-to-apply
  consent path is dispatched and its artefact will be linked here.

STELLE BESATZT, coordinator-auftrag 02:5xZ. grund fuer den namen: die FRISCHE Lane w226-pr1627-0428-226-consent konnte nicht gestartet werden, weil 'worker-cleanup.sh w21-pr1702-…' mit PARTIAL 'session/OpenCode release incomplete' endete (tooling issue #6) und spawn-lane.sh deshalb ADMISSION-HOLD 'POOL-UNKNOWN: live worker without pool reservation' meldet. der sitz 0847d100 (w21) fuehrt diese karte daher in derselben session weiter - AGENTS 3.6 erlaubt das ausdruecklich als explizite uebergabe, und dieselbe session hat die diagnose bereits geliefert. PR-FELD bleibt leer, bis die lane ihren eigenen branch/PR eroffnet; integration in #1627 erfolgt erst, wenn der fix mit dem dann exakten develop 7d4351c6d64 bereit ist.

BELEGSTELLEN-KATALOG FÜR DEN FIX (alle von mir oder von session-LAESEN gemessen, develop 7d4351c6d64): cmd/baha/application_destroy_authorization.go:148 (erster plan-bau), :180 (consent-VALIDIERUNG ValidateProviderImpactScopeConsent), :183 (zweiter bau 'current'), :187-188 (Code 'stale-impact-consent' - der im protokoll von #1627 wirklich erschien, also war :180 erfolgreich und die REVALIDIERUNG verlor). cmd/baha/application_stop_impact.go:28 (buildApplicationStopPlan, vom fixture an cmd/baha/env_destroy_integration_test.go:117 benutzt) und :35 (dieselbe funktion meldet selbst 'stale-impact-consent' bei target-wechsel) sowie :210-215 (preview-bindestelle, von der review-session gelesen). cmd/baha/application_provider_authorization.go:70-76 (provider semantic compare). internal: provider_change_scope.go:93 (ComposeProviderImpactScope, sha256-planid) und provider_consent_authority.go:689, beide aus der abgelieferten diagnose (akte fifth-round-child-read-diagnosis.md, plan 93acaa790; review-placement-akte plan 22f3372c8a18). AKZEPTANZ-WEG: consent-scope aus demselben builder/kontext wie :183, ein Stabilitaets-test der revalidierung (zwei baue, gleicher planid), der negativfall bleibt. mission sha256 8e4ac837f1c1 plus zusatz-belege (sha256 im ledger).

UMSCHALTUNG VON ANALYSE AUF UMSETZUNG (Owner-Direktive 03:2xZ): die karte DARF NICHT als analyse-only geschlossen werden; acceptance ist implementierung plus grueren exakten hosted Docker- UND Podman-CI. sitz 0847d100 fuehrt sie als code-owner (mission sha256 8bcbd5ab9e40). WURZEL-NAMENSFORM NACH OWNER-LESE, ergaenzt unsere beiden befunde: es existieren ZWEI verschiedene digests - der PlanID des scope-owners (provider_change_scope.go:93 ComposeProviderImpactScope) und der Impact.PlanID des blatt-retirements; das fixture muss GENAU den wert binden, den der KEEP-gate liest. unsere eigene lese bestaetigt das muster: application_destroy_authorization.go:148 baut den plan, :180 validiert das consent gegen p.Scope, :183 BAUET denselben plan erneut, :187-188 verwirft bei abweichendem PlanID - der im protokoll von #1627 erschien, also die revalidierung verlor und nicht die validierung. INTEGRATION: der patch geht an den inhaber von #1627 (branch cli2-env-delete bleibt owner-eigentum), integration durch den owner, dann exact-head CI mit docker UND podman, von der lane bis terminal beobachtet; die test-selektionsstelle (scripts/pr-check-runner.py / scripts/pr-gate-plan.py) wird als befund mit datei:zeile gemeldet, weil scripts/** owner-scope ist. LOKALE TESTS SIND VERBOTEN (owner-direktive, mission sha256 d65b09b8ffed): ein lokaler compile-probe auf diesem sitz ist dokumentiert und gilt als NICHT-acceptance. kreuzverweis: die review-session hat ihre placement-akte auf plan 47b7e3e6555d nachgezogen.

STAND DER ERKENNTNIS, mit korrekter bescheidenheit (04:1xZ): die klassifikation 'produktseitiger single-consent design-fehler' ist HYPOTHESE, nicht belegte tatsache - der owner hat seine eigene These zurueckgenommen ('I cannot prove from the one-line CI error which compare fired'), und meine ruecknahme der anweisung 'capture-punkt angleichen' (mission d6a62563023b) war in der stoerke nicht gedeckt; nachricht 329dddd4ee90 stellt die pruefreihenfolge wieder her. VON MIR SELBST IN develop 7d4351c6d645 GEGELESEN, und das ist der grund, warum die meldung allein nichts entscheidet: der code 'stale-impact-consent' hat DREI emissionsstellen - cmd/baha/application_stop_impact.go:35 (target seit preview gewechselt), cmd/baha/app_runtime_retirement.go:116-117 (stopPlan.retirementPlanID != plan.Impact.PlanID, mit dem kommentar :108-111, dass bewusst der application-stop scope als consent-authoritaet gilt und an genau diesen retirement-plan gebunden wird) und cmd/baha/application_destroy_authorization.go:187-188 (zweiter bau, abweichender PlanID). das protokoll nennt nur 'provider change: stale-impact-consent'. DER PRUEFPUNKT: welcher der drei zweige schlug, muss aus dem hosted-protokoll belegt werden (gh api …/actions/jobs/137020935578/logs und …/137020935792/logs; gh run view --log liefert 0 bytes), nicht aus dem code-lesen gefolgert. DER KANDIDAT bleibt der aus round-1-planid-parity.md: fixture bindet den leaf-retirement Impact.PlanID plus parity-test - aber nur gueltig, wenn derselbe wert ALLE konsumstellen passiert (zerstoerungs-scope :180, verschachtelter stop-scope application_stop_impact.go:177, revalidierung :183-188/app_runtime_retirement.go:114-125). braeuchte eine ebene einen anderen wert, ist eine ausdrueckliche, gesicherte delegation noetig, und deren form entscheidet der owner. stale-pruefungen bleiben unveraendert streng; echte zustands-aenderung zwischen den bauten waere drift und fuehrt zu STOP und meldung. mission sha256 d650234… (s. ledger) praezisiert das.

STAND DER ERKENNTNIS, mit korrekter bescheidenheit (04:1xZ): die klassifikation 'produktseitiger single-consent design-fehler' ist HYPOTHESE, nicht belegte tatsache - der owner hat seine eigene these zurueckgenommen ('I cannot prove from the one-line CI error which compare fired'), und meine ruecknahme der anweisung 'capture-punkt angleichen' (mission d6a62563023b) war in dieser stoerke nicht gedeckt; die nachricht sha256 329dddd4ee90 stellt die pruefreihenfolge wieder her. VON MIR SELBST IN develop 7d4351c6d645 GEGELESEN, und das ist der grund, warum die meldung allein nichts entscheidet: der code 'stale-impact-consent' hat DREI emissionsstellen - cmd/baha/application_stop_impact.go:35 (target seit preview gewechselt), cmd/baha/app_runtime_retirement.go:116-117 (stopPlan.retirementPlanID != plan.Impact.PlanID; der kommentar :108-111 erklaert den application-stop scope zur consent-authoritaet und bindet ihn an genau diesen retirement-plan) und cmd/baha/application_destroy_authorization.go:187-188 (zweiter bau, abweichender PlanID). das protokoll nennt nur 'provider change: stale-impact-consent'. DER PRUEFPUNKT: WELCHER DER DREI EMISSIONSPFADE schlug, muss aus dem hosted-protokoll belegt werden (gh api …/actions/jobs/137020935578/logs und …/137020935792/logs; gh run view --log liefert dort 0 bytes), nicht aus dem code-lesen gefolgert; kann das protokoll es nicht entscheiden, soll die akte das bekennen. DER KANDIDAT bleibt der aus round-1-planid-parity.md: fixture bindet den leaf-retirement Impact.PlanID plus parity-/stabilitaetstest - gueltig nur, wenn derselbe wert ALLE konsumstellen passiert (aussen application_destroy_authorization.go:180 gegen buildApplicationDestructionPlan.Scope.PlanID, verschachtelt application_stop_impact.go:177 authorizeApplicationStop, revalidierung :183-188 app_runtime_retirement.go:114-125). braucht eine ebene einen anderen wert, ist die einzige zulaessige form eine ausdrueckliche, gesicherte delegation, deren gestalt der owner entscheidet. stale-pruefungen bleiben unveraendert streng; eine echte zustandsaenderung zwischen den bauten ist drift und fuehrt zu STOP und meldung.

lane hat den fixture-only fix gelauncht und gemeldet (END_BLOCKED): proposal i, cmd/baha/env_destroy_integration_test.go, kein internal/**; akten auf origin/main
