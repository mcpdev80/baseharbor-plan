---
id: t-20261020-develop-appid-manifest-test-regression
type: bug
areas: [ci, contract]
release: v0.4.26
version: ""
parent: v0.4.26
owner: "Flash (codeman w1-baseharbor)"
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261020-develop-appid-manifest-test-regression · CI/Contract: develop integration tests still author app.id in developer manifests #task #release/v0-4-26 #status/active #view/active #area/ci #area/contract #kind/bug
    <!-- generated:card -->
    **Owner:** Flash (codeman w1-baseharbor) · **Priority:** high  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** none  
**Required by:** [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md)  
**Owner:** Flash (codeman w1-baseharbor)  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

`origin/develop` (bb91fbc3) fails `TestRepositoryWorkflowRealLifecycle` because the test fixture writes `app.id` into a developer manifest while `parseAppField` (manifest_parse.go:260) rejects non-canonical `app.id` (contract: app.id is system-owned per #872). This breaks the mandatory docker-runtime check that #998 needs for its final CI.

## Scope

- Update the outdated developer-manifest fixture(s) to the accepted contract (no manual `app.id`; explicit canonical path only where genuinely required).
- Test-side changes only unless the parser itself contradicts the accepted #872 contract.
- Green docker-runtime integration evidence via CI (durable run, not VM one-off).

## Acceptance

1. `TestRepositoryWorkflowRealLifecycle` PASS in GitHub Actions on develop head.
2. No contract semantics change; parser behavior stays fail-closed for non-canonical app.id.
3. Independent local review + evidence links on this card.

## Notes

Local evidence: `evidence/board-2026-10-19/p22-nativejob.md`. Found by p22 split triage on 2026-10-20; pre-existing on develop, surfaced via #998's mandatory CI.
