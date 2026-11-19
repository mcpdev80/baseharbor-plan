---
id: t-20261118-ownership-stale-consent-hardening
release: v0.4.28
repos: [mcpdev80/baseharbor]
depends_on: []
owner: codeman-9a898351 (w99-0428-119, claim c55a8b4f)
kanban_status: review
card_number: 0428-119
card_short_title: harden Prov ownership chain vs
kanban_title: 0428-119 · harden Prov ownership chain vs
prs: [mcpdev80/baseharbor#1690]
wait_reason: ""
blocker: ""

---
# t-20261118-ownership-stale-consent-hardening · close ownership-race windows behind stale-impact-consent

- [ ] t-20261118-ownership-stale-consent-hardening · harden provider ownership chain vs stale-impact-consent #task #release/v0-4-28 #status/review #view/review #kind/task
    <!-- generated:card -->
    **Owner:** codeman-9a898351 (w99-0428-119, claim c55a8b4f)  
    **PR:** [baseharbor#1690](https://github.com/mcpdev80/baseharbor/pull/1690)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** codeman-9a898351 (w99-0428-119, claim c55a8b4f)  
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
