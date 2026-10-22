---
id: t-20261022-r27-ci-authority
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
priority: critical
owner: ""
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

# Trusted CI readiness: authority

## Goal
Independently qualify the smallest trusted planner/executor/finalcheck checks for the authority domain before its new implementation files are exercised. This is a bounded CI prerequisite, not blanket approval for unrelated domains.

## Covered slices
- authority-contract
- state-owner
- mutation-lock
- execution-journal
- journal-wiring
- app-binding
- candidate-ingress
- management-host

## Acceptance
- Inventory existing production paths and check mapping, required check names, runner capabilities, test entrypoints and exact trust inputs; avoid speculative new checks.
- Add only missing coverage with executable positive and negative regressions, including changed-file detection and failure propagation.
- Independently review any trusted policy/coverage changes; preserve source/integration SHA and runner isolation.
- No self-qualification, full matrix, blanket bypass or merge without normal gates.
- Different domains may be worked in parallel by Codeman, maintainer sessions or contributors, but central CI workflow/policy files require explicit single-writer integration sequencing.
- Record exact accepted SHA and available check identity for dependent product slices.
