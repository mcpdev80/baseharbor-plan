---
id: t-20261118-ownership-stale-consent-hardening
release: v0.4.28
repos: [mcpdev80/baseharbor]
depends_on: []
owner: w119-0428-119-consenthop (codeman 80aa0bf4, ornith:2) — uebernommen von w99-0428-119 r3 (session f5dabf03 ist weg)
kanban_status: wait
card_number: 0428-119
card_short_title: harden Prov ownership chain vs
kanban_title: 0428-119 · harden Prov ownership chain vs
prs: [mcpdev80/baseharbor#1690]
wait_reason: "korrektur fertig gemessen, aber KEIN freier sitz (pool 5/5; der sitz kommt frei, sobald die hunt-lane 99dda85e ihre meldefrist erfuellt hat). INHALTLICH offen (CODEX-r2 REQUEST CHANGES auf 5b9a9545aa9adb74870695133daa0561cac5c5ca, VON MIR IM CODE BESTAETIGT): (1) internal/application/provider_consent_authority.go:502-511 sameProviderInstanceAuthority vergleicht ID/ProviderID/ProviderVersion/ProviderProtocol/Kind/Capabilities/Scope/SharingBoundary/Ownership/OwnerApplicationID, laesst aber 'Reference' UND 'OwnerEnvironment' weg — beide felder existieren (internal/capability/registry.go:44/:45) und 'reference' loest externe provider aktiv auf (registry.go:133). (2) equalProviderCapabilities :552-565 hat ein DUPLIKATS-LOCH: a=[x,x] vs b=[x,y] -> laengen gleich, mitgliedschaft erfuellt, TRUE, obwohl die mengen verschieden sind. ZUSATZ: die regression (provider_consent_oscillation_test.go:566+) endet bei DescribeProviderChanges/revalidation, der antrag-pfad in cmd/baha ist nicht belegt. LAUFZEIT-GATES weiter owner-draht 114(a) (ORAS-install im PR-job fehlt)."
blocker: ""
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/44464033443", "https://github.com/mcpdev80/baseharbor/actions/runs/44464060182"]

---
# t-20261118-ownership-stale-consent-hardening · close ownership-race windows behind stale-impact-consent

- [ ] t-20261118-ownership-stale-consent-hardening · harden provider ownership chain vs stale-impact-consent #task #release/v0-4-28 #status/wait #view/wait #kind/task
    <!-- generated:card -->
    **Owner:** w119-0428-119-consenthop (codeman 80aa0bf4, ornith:2) — uebernommen von w99-0428-119 r3 (session f5dabf03 ist weg)  
    **PR:** [baseharbor#1690](https://github.com/mcpdev80/baseharbor/pull/1690)  
    **Waiting:** korrektur fertig gemessen, aber KEIN freier sitz (pool 5/5; der sitz kommt frei, sobald die hunt-lane 99dda85e ihre meldefrist erfuellt hat). INHALTLICH offen (CODEX-r2 REQUEST CHANGES auf 5b9a9545aa9adb74870695133daa0561cac5c5ca, VON MIR…  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/44464033443), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44464060182)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w119-0428-119-consenthop (codeman 80aa0bf4, ornith:2) — uebernommen von w99-0428-119 r3 (session f5dabf03 ist weg)  
**Priority:** not set  
**PRs:** [baseharbor#1690](https://github.com/mcpdev80/baseharbor/pull/1690)  
**Source:** 
<!-- /generated:links -->

## Goal
Hunt 916: the chain provider_union.go:164-168 -> digest -> application_provider_authorization.go:59 can yield stale-impact-consent when ownership state is unverifiable; the audit lists 8 race windows and 6 coverage gaps. Close the windows where an add/remove/re-add leaves a consumed-but-unverified ownership state, and add the missing matrix tests (each new test must run inside the existing CI-selected application group).

## Scope
- internal/application provider-union/authorization files + tests. Contract question (whether unverifiable should FAIL CLOSED with a distinct error) decided inside the lane with documented rationale + review.

## Required checks
- internal/application unit + selected docker lifecycle tests on exact head.

## Dependencies and file ownership
- Source: hunt 916 befund-1.md (races/coverage), evidence/r28-welle4-2026-11-18/hunt-ownership/befund-1.md. Related symptom: #1663 run 44407750981 document_database failure.
## Dependency decision (coord, 2026-11-18)
Separate fix card = YES (this one). Linkage to t-20261115-bughunt-d28-i18n-achtung/#1663 is CONDITIONAL: if the in-flight lane triage shows the document_database failure reproduces on plain develop (pre-existing race per hunt 916 windows), #1663 proceeds via one sanctioned rerun and no depends_on edge is added. If it reproduces ONLY with the 093 merge, add depends_on: [t-20261118-ownership-stale-consent-hardening] to the 093 card before any re-review.

END akzeptiert: head d94cc67d auf base 7d3438364 (exakt develop), exact-run 44437197853 SUCCESS terminal, akte fix-1.md 0da426cc am band mit revision-labels. hunt-916 race-fenster laut akte geschlossen; Routing an CODEX-REVIEW

REQUEST_CHANGES vom reviewer (kommentar 6997135020 auf d94cc67d): consent-equivalence ignoriert Realization.Verified+Evidence (fail-closed-luecke im echten authorization path, validateApplicationProviderExecution verlangt keinen verified state) + docker-gate fehlt (targeted HA/selected runtime nur skipped). korrektur-r2-mission RESERVIERT (mission-119r2-consent-semantics) fuer ersten echten END-freiraum; pool ist voll, keine doppelarbeit

docker-lage berichtigt: run 44454644057 workflow-seitig success, aber job 'Targeted HA · docker' skipped (0 steps) — lane hat das korrekt festgehalten (mein queue-394-ansatz war auf run-ebene, nicht job-ebene). die drei targeted-integration-fehler (#557-#559) scheitern im schritt 'Verify exact SHA input' (push-pfad ohne inputs) — wiring-befund, keine produktschuld. kartenpflicht 'selected docker lifecycle tests on exact head' wird jetzt per dokumentiertem workflow_dispatch (gate coreless-runtime, ref=4e032c858) erfuellt; lane beobachtet bis terminal

kein abnahme-zeug, kein merge (owner-wort). docker-route-erklaerung: targeted-integration ist integriert-only (ref: develop + HEAD==CANDIDATE_SHA), daher #557-#561 alle im schritt 'Verify exact SHA input' gebrochen. dreistufen-route an lane: docker-runtime-acceptance inputs.ref pruefen, sonst host-lokaler baha-docker-zeuge nach praezedenz 088-r3, fehlender hosted-draht als owner-befund

PR #1690 head ist nach berichtigtem hopf wieder auf dem lane-exklusiven branch: 84ee9a93e (ec592fd385/deeeb6477 ancestry, seitenzweig getilgt), r3-code unveraendert, akte r4-routentabelle published

Delegated reviewer ruling (2026-11-19): do not qualify run 44464033443 unit success plus run 44464060182 runtime failure as acceptance. Need content-bearing exact-head Docker lifecycle PASS. The Docker job did execute, but target setup failed at the ORAS prerequisite; this is not a product pass. Try a supported exact-SHA runtime route with verified ORAS setup. If it cannot be provided without altering protected security.go or violating CI-owner constraints, close out as ZWEIFEL with evidence and release the lane to the next independent ready card. No merge.

Handoff decision: 0428-128 already owns the read-only Docker/ORAS route probe; do not duplicate it. After 0428-119 evidence/END is captured, release its lane to the next independent ready card. Re-open 0428-119 only when a supported exact-head Docker lifecycle witness can run; no waiver for unit success plus runtime abort.

119-lane ist bereits entlassen (f5dabf03 deleted) — sitz traegt jetzt 121-r2/128-probe; keine nicht-ueberlappende quellarbeit an 119 bis 128 die route klaert

STATT EINES HOLDS: der sitz bekommt echte, konfliktfreie arbeit, und der owner-ZWEIFEL bleibt unangetastet. gemessen gegen develop 1019190d8dc0ecac7693f3461153e76be0e2cb8a: EIGENE aenderungen = 5 dateien (cmd/baha/application_provider_authorization.go, internal/application/provider_change_plan.go, provider_change_types.go, provider_consent_authority.go, provider_consent_oscillation_test.go), disjunkt zu allen vier aktiven lanen, 'git merge-tree --write-tree origin/develop <kopf>' = 0 konflikte, PR 'behind' (base deeeb6477). AUFTRAG NUR: monotoner hopf + terminale exact-head-CI + akte, damit nach deinem ORAS-draht sofort abgenommen werden kann, ohne nochmal zu hopfen. ICH AKZEPTIERE DAMIT NICHT: die karte behaelt deinen wortlaut 'kein abnahme-freiraum fuer unit gruen + runtime-versuch rot', und der grund bleibt aussen — '.github/workflows/docker-runtime-acceptance.yml' hat im PR-zweig_keinen ORAS-install-schritt (zeilen 174-330) waehrend die install-zeilen 127-128 nur im push-job stehen (114, punkt (a)); eine lane aendert daran nichts, sie meldet nur. wenn der required-aggregate gruen ist und der runtime-rest offen bleibt, geht die karte zurueck auf blocked mit genau diesem wortlaut

END (session 80aa0bf4, fresh takeover of vanished f5dabf03): branch lane-0428-119-consent-hard neu auf develop 1019190d8 gecutt, 5 files aus dem squash 84ee9a93 aufgebracht, commit 184eefde (nur meine commits, 84ee9a93 nicht Ancestor), PR #1690 head auf 184eefde upgedatet. Exact-head run 44563139929 SUCCESS; Go unit owner (internal/application) shard PASS inkl. TestConsentSurvivesUnverifiableStateOscillation + TestConsentDoesNotFoldUnwitnessedRuntimeState; docker/podman/core-less SKIPPED (ORAS wire 114(a)). required-aggregate gruen, runtime-rest offen -> karte auf blocked mit lautlaut 'owner wire 114(a)'. Evidence fix-2.md (a1cdc884 auf origin/main). Kein merge. Lane fuer next ready card freigegeben.

Independent read-only review (2026-11-19) of PR #1690 head `184eefde9b84ff7d6bfb3dc0017989a2143ddede` found an additional code blocker: `equalRegistry` compares only map lengths, allowing same-cardinality registry mutation to pass consent equivalence. Exact-head run 44563139929 passed unit checks but skipped Docker lifecycle; PR base 1019190d is behind current develop 558dc42d. See [review evidence](../evidence/r28-welle4-2026-11-19/codex-review-wave/1690-0428-119-independent-review.md). No merge recommendation.
