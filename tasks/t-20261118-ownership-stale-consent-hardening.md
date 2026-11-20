---
id: t-20261118-ownership-stale-consent-hardening
release: v0.4.28
repos: [mcpdev80/baseharbor]
depends_on: []
owner: w119-0428-119-pr1690-consentauth-r4
kanban_status: review
card_number: 0428-119
card_short_title: harden Prov ownership chain vs
kanban_title: 0428-119 · harden Prov ownership chain vs
prs: [mcpdev80/baseharbor#1690]
wait_reason: ""
blocker: ""
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/44464033443", "https://github.com/mcpdev80/baseharbor/actions/runs/44464060182"]

---
# t-20261118-ownership-stale-consent-hardening · close ownership-race windows behind stale-impact-consent

- [ ] t-20261118-ownership-stale-consent-hardening · harden provider ownership chain vs stale-impact-consent #task #release/v0-4-28 #status/review #view/review #kind/task
    <!-- generated:card -->
    **Owner:** w119-0428-119-pr1690-consentauth-r4  
    **PR:** [baseharbor#1690](https://github.com/mcpdev80/baseharbor/pull/1690)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/44464033443), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44464060182)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w119-0428-119-pr1690-consentauth-r4  
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

CODEX-r2 befunde VON MIR AM KOPF 5b9a9545a NACHGEMESSEN: provider_consent_authority.go:500-511 ohne Reference/OwnerEnvironment (beide felder registry.go:44/:45, reference loest auf :133); equalProviderCapabilities :552-565 duplikats-loch a=[x,x] vs b=[x,y] -> TRUE. Neue lane w119-pr1690-consent-auth auf ornith:2

sitz frei geworden (073-kandidat im review) -> sofort besetzt. Auftrag ist auf die AKTUELLE spitze gebracht und enthaelt jetzt den hopf-zwang: der basis-abstand von #1690 (223cb97a9) beruehrt scripts/pr-gate-plan.py und scripts/test_pr_gate_plan.py, also ist der alte lauf 44597195363 unabhaengig von seinem gruen-ergebnis ENTWERTET (meine eigene basis-distanz-regel)

beide befehle VON MIR AM KOPF 5be347068 NACHGEMESSEN, erfuellt: provider_consent_authority.go:512-513 vergleicht jetzt Reference UND OwnerEnvironment; equalProviderCapabilities zaehlt (map[Kind]int, counts[c]++ fuers b, counts[c]-- fuers a, <0 -> false, plus laengen-gleichheit) = echte multiset-gleichheit, das [x,x]/[x,y]-loch ist zu. HOPF-FORM korrekt, aber anders als gemeldet: der KOPF hat einen eltern, sein VATTER 6ca7516c2 hat zwei und bringt develop 4b3a35590 (ancestry 0, merge-tree konfliktfrei). ECHTER PR-BELEG = 44629547169 (pull_request, success, 22:36:50Z); die gemeldete '#6664' liefert 404 — im urteil als akten-befund weitergegeben. Am kopf SKIPPED: PR · Exact Candidate, Selected Runtime, Public Contracts, Main release checks — das urteil muss aus dem gate-plan sagen, ob das fuer diesen diff korrekt ist (§5.4). Akte: consent-authority-r2/1690-0428-119-r2.md (12607 bytes, anderer dateiname als mein befehl, inhalt mit ls-remote + PLAN + repo-rule)

CODEX-FUND behoben, am kopf gemessen: provider_consent_authority.go:516 vergleicht a.OwnerApplication == b.OwnerApplication (ID :515, Reference :517, OwnerEnvironment :518), kommentar :500-502 nennt beide felder als verschieden und authority-tragend. regression provider_consent_oscillation_test.go:656 + request-pfad application_provider_authorization_test.go:189. hopf: kopf ff9c59785, zwei eltern e31292073 + d5c11753ea43, draft=false. lauf 44647040369 pull_request completed/success am exakten kopf. OFFEN: runtime-zellen SKIPPED (owner-draht ORAS, docker-runtime-acceptance.yml PR-pfad :174-330 ohne install) und mergeable_state=behind (develop b7cbc00f0adf) — letzter hopf vor dem merge. urteil angefragt bei codex 95971e0a, zustellung accepted

CODEX-URTEIL r4 am exakten kopf ff9c59785: 'APPROVE CONTENT — MERGE BLOCKED pending current-develop hop and exact-head Docker lifecycle evidence' (1690-0428-119-r4.md). P1 'HEALED': comparator unterscheidet id und manifest-name und prueft BEIDE (provider_consent_authority.go:495-519), regressionen TestEqualRegistryBlockendOwnerApplicationOnly (nur OwnerApplication geändert, gleichheit verworfen) UND TestRequestPathRejectsOwnerApplicationRegistryChange (echter request-pfad, application_provider_authorization_test.go:168-247). P2: die VOLLSTÄNDIGE feldliste von ProviderInstance (registry.go:33-45) und ProviderBinding (registry.go:48-53) ist jetzt abgeglichen — meine frage, ob nichts mehr fehlt, ist damit beantwortet; BENANNT bleibt eine abdeckungsluecke bei Registry.ResolvePlacement/Reference (registry.go:127-151), die aus r3 mitkommt. ZWEI BEDINGUNGEN VOR DEM MERGE: (1) hopf auf die dann aktuelle develop-spitze (jetzt b7cbc00f0adf) mit terminalem pull_request-lauf, (2) der exact-head Docker-lifecycle-zeuge — haengt an der ORAS-luecke im PR-job (docker-runtime-acceptance.yml PR-pfad :174-330 ohne install), also OWNER-scope, nicht bahnen-verschulden. Karte bleibt review: inhalt angenommen, merge nicht moeglich. HOPF-LANE geht auf den ersten freien sitz (alle fuenf belegt, drei hopfs laufen bereits)
