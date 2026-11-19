---
id: t-20261118-ownership-stale-consent-hardening
release: v0.4.28
repos: [mcpdev80/baseharbor]
depends_on: []
owner: w99-0428-119 r3 (codeman f5dabf03)
kanban_status: active
card_number: 0428-119
card_short_title: harden Prov ownership chain vs
kanban_title: 0428-119 · harden Prov ownership chain vs
prs: [mcpdev80/baseharbor#1690]
wait_reason: ""
blocker: ""

---
# t-20261118-ownership-stale-consent-hardening · close ownership-race windows behind stale-impact-consent

- [ ] t-20261118-ownership-stale-consent-hardening · harden provider ownership chain vs stale-impact-consent #task #release/v0-4-28 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** w99-0428-119 r3 (codeman f5dabf03)  
    **PR:** [baseharbor#1690](https://github.com/mcpdev80/baseharbor/pull/1690)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w99-0428-119 r3 (codeman f5dabf03)  
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
