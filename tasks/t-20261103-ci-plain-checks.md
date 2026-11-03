---
id: t-20261103-ci-plain-checks
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: ""
owner: "Codex (Owner CI simplification 2026-11-03)"
priority: critical
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261103-ci-plain-checks · CI: remove evidence verification and keep normal checks plus commit receipts #task #release/v0-4-27 #status/active #view/active #area/ci #kind/task

## Goal

Owner explicitly authorizes complete removal of gate manifests, CI evidence collection/reverification, receipt approval/shadow chains and evidence reuse from CI, Pre-Release and Release. Normal tests remain mandatory. The only CI receipt is a small Planning file containing merge commit SHA and PR number. Rulesets stay disabled; no release or tag.

## Scope and ownership

- Product branch codex/ci-plain-checks owns CI/release workflows, evidence-only CI scripts/tests and their current documentation.
- Preserve active product claims and the separate unpublished authority-package correction; integrate only the normal package check needed by the current work.
- Coordinator owns ci.yml, planner/executor/final-check integration and minimal writer.
- Parallel release lane owns pre-release.yml, pre-release-runtime-suite.yml, release.yml, supplemental-release-validation.yml and release-only evidence helpers.
- Parallel workflow lane owns other runtime/acceptance workflows and evidence-only upload/collection steps.
- Parallel documentation/planning lane owns current CI documentation and superseding old receipt/evidence planning criteria.
- Historical release records and old receipt data remain unchanged.

## Acceptance

Normal selected CI and release test execution fail on failing/missing required jobs without Actions API or artifact evidence re-verification. No live/retained receipt verifier or separate approval workflow remains active. Commit receipts retain SHA/PR binding and safe publication. Focused regression tests, workflow policy and actionlint pass. Planning render/check pass.

## Handoff

Claimed under Owner instruction on 2026-11-03. Implementation and normal hosted checks pending.
