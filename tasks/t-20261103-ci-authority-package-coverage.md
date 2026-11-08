---
id: t-20261103-ci-authority-package-coverage
card_number: "0427-098"
card_short_title: "execute authority and"
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: ""
owner: "Codex (CI completion 2026-11-03)"
kanban_lane: closed
kanban_summary: "Resolve the real unknown-impact failure in PR 1326 by executing the authority, stable-ID and service-access package tests…"
kanban_status: closed
kanban_title: "0427-098 · execute authority and"
priority: high
depends_on: [t-20261017-release-0-4-27-updates, t-20261103-ci-receipt-source-recovery]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: superseded
superseded_by: t-20261103-ci-plain-checks
evidence: [https://github.com/mcpdev80/baseharbor/pull/1345]
---

- [x] t-20261103-ci-authority-package-coverage · CI: execute authority and stable-ID package checks for their real Go changes #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** Codex (CI completion 2026-11-03) · **Priority:** high  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1345)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** superseded  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261103-ci-receipt-source-recovery](t-20261103-ci-receipt-source-recovery.md)  
**Owner:** Codex (CI completion 2026-11-03)  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Resolve the real unknown-impact failure in PR 1326 by executing the authority, stable-ID and service-access package tests through normal hosted CI.

## Scope

- Add a bounded Go-package validation with genuine test execution and no secret/runtime dependency.
- Route the known package source changes to that check and preserve fail-closed handling for unrelated files.
- Qualify planner, executor and workflow together through existing exact-source CI bootstrap when required.

## Acceptance

- The complete real PR 1326 diff has resolved coverage and executes the package checks, documentation checks and final required verifier.
- Missing tests, failing tests or unsupported paths cannot become success.
- Keep all product files and active Codeman branches unchanged. No self-hosted runners, ruleset activation, receipt re-verification, release or tag.

## Required checks

- Focused planner/executor/workflow regressions; hosted normal selected CI and real package execution on an exact product candidate.
- Planning render/check, preserving concurrent writers.

## Dependencies and file ownership

- Own scripts/pr-gate-plan.py, scripts/pr-check-runner.py, scripts/test_pr_gate_plan.py, .github/workflows/ci.yml and the existing exact-source qualification register docs/internal/ci-binding-qualifications.md.
- No active published claim reserves these files for this correction. Authority product files remain owned by w1-authority; other product claims remain intact.

## Handoff

- Assigned under Owner CI-completion mandate after receipt task acceptance. PR 1326 run 41551484989 failed final with unknown impact for coreinstallation authority/locks, stableid locks and serviceaccess/local_issuer.go; all its selected documentation jobs passed.
- PR 1333 separately failed DE/EN integrity; its active Owner is already updating the product branch, so no competing product edits are assigned here.

## Superseded by integrated normal CI

The Owner expanded the assignment to complete CI evidence removal. Normal authority package execution is included in t-20261103-ci-plain-checks / Core #1345. Original unpublished work is preserved; no separate acceptance or source-verification gate remains assigned here.
