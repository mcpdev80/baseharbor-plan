---
id: t-20261118-ownership-stale-consent-hardening
release: v0.4.28
repos: [mcpdev80/baseharbor]
depends_on: []
kanban_status: planned
card_number: 0428-119
card_short_title: harden Prov ownership chain vs
kanban_title: 0428-119 · harden Prov ownership chain vs
---
# t-20261118-ownership-stale-consent-hardening · close ownership-race windows behind stale-impact-consent

- [ ] t-20261118-ownership-stale-consent-hardening · harden provider ownership chain vs stale-impact-consent #task #release/v0-4-28 #status/planned #view/ready #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
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
