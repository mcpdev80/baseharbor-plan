---
id: {{id}}
type: maintenance
areas: [release]
release: {{release}}
version: {{version}}
release_stage: updates
parent: {{release}}
owner: ""
priority: high
depends_on: []
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo, mcpdev80/baseharbor-console, mcpdev80/baseharbor-node-connector]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] {{id}} · {{version}} · {{title}} #task #{{release_tag}} #status/planned

## Goal

Complete dependency intake before feature development.

## Scope and acceptance

- Immediately inventory all open Renovate PRs, dependency-dashboard entries, grouped updates and lockfile/container/action/toolchain pins in all four product repositories; include this plan repository when applicable.
- Process and integrate all applicable pending updates first through product PR review and sufficient targeted checks. Resolve stale bases, conflicts, grouped/superseded PRs and actual failures; then freeze the post-update baseline.
- Never merge unverified or incompatible updates blindly. An update that cannot safely land is an explicit blocker until fixed or the Maintainer explicitly decides its documented exclusion; remaining unresolved updates do not silently count as done.
- Record PRs, merged SHAs, exact checks and any explicit exclusion. Keep subsequent Renovate arrivals in the normal intake; candidate-time changes go back through affected qualification.

## Required checks

Existing trusted dependency/lockfile/build/security/compatibility checks by impact; native tests only for uniquely uncovered risks. No automatic full matrix.

## Dependencies and file ownership

- Procedure and sources: [release workflow](https://github.com/mcpdev80/baseharbor-plan/blob/main/RELEASE_WORKFLOW.md#updates). Stage dependencies are synchronized by `scripts/release_cycles.py sync`; do not weaken them manually.
- Owner updates this task, its release-specific audit/evidence and existing authorized PRs; coordinate product files through their normal owners. Planning goes directly to main.

## Handoff

Not started. Record actual source SHAs, outcomes, authorization where required, evidence and remaining blockers; do not infer acceptance from card creation.
