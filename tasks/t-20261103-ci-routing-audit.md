---
id: t-20261103-ci-routing-audit
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: ""
owner: "Codex (CI routing audit 2026-11-03)"
priority: critical
depends_on: [t-20261017-release-0-4-27-updates, t-20261103-ci-plain-checks]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261103-ci-routing-audit · CI: repair Go output parsing and audit every check route #task #release/v0-4-27 #status/active #view/active #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** Codex (CI routing audit 2026-11-03) · **Priority:** critical  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261103-ci-plain-checks](t-20261103-ci-plain-checks.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md)  
**Owner:** Codex (CI routing audit 2026-11-03)  
**Priority:** critical  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Owner requests the JSON parser fix and a complete audit of all existing CI mappings, including current open PRs. Normal tests and the two-field commit receipt remain; no evidence/approval architecture is added.

## Scope and ownership

- Own scripts/pr-gate-plan.py, scripts/pr-check-runner.py, their focused tests, .github/workflows/ci.yml and a compact source-routing inventory/check.
- Parser lane owns runner and runner tests; coordinator owns planner/workflow; audit lane reads all mappings and inventories declared checks, workflow executors, test families and native gates.
- Preserve active Codeman product claims, their source branches and unpublished work. Product failures in State Owner remain with the product owner.
- Deployment routing must execute its package/consumer tests and actual Docker/Podman lifecycle where production ownership/state behavior is affected. Unknown valid paths must execute conservative Go unit/vet/build checks and applicable Docker/Podman lifecycle tests instead of blocking solely on a missing mapping. Invalid source/diff/catalog data still fails.

- Owner additionally requests cheap Draft-PR checks, selected checks on ready PRs and later pushes, no ordinary branch-push CI, and no duplicate develop-push suite after merge. Explicit validation branches/manual runs stay available.

## Acceptance

Go tool diagnostics cannot crash JSON parsing or hide failing tests. Every declared normal check and selected native gate has a real workflow executor. All explicit path mappings and required test families are inspected; missing/unimplemented routes are repaired or reported explicitly. Current open PR diffs are evaluated with the resulting policy. Focused local checks and normal hosted CI pass before merge. Rulesets remain off; no release/tag.

## Handoff

Resumed on explicit Owner instruction to publish and continue fixing CI. Claimed after reading current remote instructions and active product claims. Baseline develop 9a57107f; #1348 currently exposes JSONDecodeError, #1333 unknown deployment paths, #1347 actual owner-binding failures, #1334 old pre-migration CI result. No product implementation is taken over.
