---
id: t-20261017-cli-package-layout-after-freeze
type: architecture
areas: [cli, architecture]
release: backlog
version: ""
parent: backlog
owner: ""
priority: low
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261017-cli-package-layout-after-freeze · CLI: assess package decomposition after the contract freeze #task #release/backlog #status/backlog #view/backlog #area/architecture #area/cli #kind/architecture
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** low  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** backlog  
**Release:** [backlog](../releases/backlog.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** low  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

After the contract freeze, assess whether decomposing the growing `cmd/baha` package would improve navigation and maintainability, then propose a small evidence-based pilot.

## Scope

- Deferred by the Maintainer on 2026-10-17: do not start now. No target release is assigned; this is not a v0.4.26, pre-release or freeze prerequisite.
- First map real dependencies, shared unexported helpers and CLI/domain boundaries. File count alone does not prove a package design defect.
- A possible direction is a thin `cmd/baha` entry point and cohesive CLI packages under `internal/cli` (for example app/Target/node), reusing existing domain authorities. This is a hypothesis, not an approved target architecture.
- Avoid import cycles, broad exported helper APIs, generic shared dumping grounds, a second domain layer and mass mechanical moves during parallel feature development.
- Do not start restructuring or expand current release scope from this note. Require fresh Maintainer assignment after the freeze.

## Acceptance

- A future assessment identifies concrete navigation/coupling problems and a bounded pilot with owned files and preserved interfaces.
- Implementation, if subsequently assigned, uses small independently reviewable PRs and preserves CLI/JSON/MCP behavior, authorization, locking, ownership, consent and error semantics.
- Verify compile/build and focused package/CLI/contract checks; native gates only for demonstrated affected behavior. No automatic full matrix for file moves.
- Estimate based on actual dependencies and the pilot. Earlier multi-day estimates were rough, not an audited delivery commitment.

## Required checks

Planning render/check for this note only. Product assessment and implementation are deferred, with no current runtime qualification.

## Dependencies and file ownership

Backlog only. No current release or task depends on this work. Scheduling requires completion of the contract freeze and an explicit Maintainer assignment; an empty dependency list is not permission to start backlog work.

## Handoff

Recorded per Maintainer instruction. Unassigned, not implemented, no product branch or PR. Current priority remains reaching the freeze.
