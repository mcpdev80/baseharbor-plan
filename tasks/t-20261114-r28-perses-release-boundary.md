---
id: t-20261114-r28-perses-release-boundary
card_number: "0428-092"
card_short_title: "Align release docs with Perses"
type: task
areas: [release, documentation]
release: v0.4.28
version: ""
parent: v0.4.28
owner: coord
kanban_status: active
kanban_lane: active
wait_reason: ""
kanban_summary: "Align current Core release/audit entry points with the accepted public scope: Core, Demo, the delivered CLI and optional Perses.…"
kanban_title: 0428-092 · Align release docs with Perses
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1577]
sources: []
blocker: ""

resolution: ""
evidence: []
---

- [ ] t-20261114-r28-perses-release-boundary · Align release docs with Perses and archived projects #task #release/v0-4-28 #status/active #view/active #area/documentation #area/release #kind/task
    <!-- generated:card -->
    **Owner:** coord · **Priority:** high  
    **PR:** [baseharbor#1577](https://github.com/mcpdev80/baseharbor/pull/1577)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** coord  
**Priority:** high  
**PRs:** [baseharbor#1577](https://github.com/mcpdev80/baseharbor/pull/1577)  
**Source:** 
<!-- /generated:links -->

## Goal

Align current Core release/audit entry points with the accepted public scope: Core, Demo, the delivered CLI and optional Perses. Archived Console and Node Connector must not be required as active release consumers. Do not rewrite historical release records or claim a release has passed.

## Verified starting points and scope

- Review current Core `AGENTS.md`, `docs/DEVELOPMENT_GUIDELINES.md`, `docs/internal/pre-release-documentation-audit.md`, `docs/reference/releases.md`, `docs/development/pre-release-readiness.md`, `.github/workflows/pre-release.yml` and release scripts against actual current source. Core is authoritative for its own rules; this planning card does not override executable safety checks.
- Identify exact live release checks and archived-component requirements; propose the smallest evidence-backed change to active Core/Demo scope. Retain real ownership, security, compatibility, native/CI and provenance gates. No automatic release, tag, direct product commit or silent skipped test.
- Coordinate with release/CI owner before touching shared workflow or scripts; one small Core PR with EN/DE documentation where applicable. Review templates and planning release workflow under separate planning ownership if further discrepancies appear.

## Acceptance and checks

All live v0.4.28 Core entry points, documentation and selected gates consistently exclude archived repositories while honestly covering shipped supported functionality; Perses is optional and not asserted implemented. Exact impacted tests and docs audit map to actual existing CI triggers. Codex/Owner-delegated Maintainer reviews exact HEAD and merges only after required real checks.

## Owner decision 2026-11-15 (option 1)

Owner refinement 2026-11-15 (same turn): the normativity of `docs/spec/management-access-v1.md` is LIMITED to authentication and role-mapping findings. Perses pin, release scope and state semantics must NOT be derived normatively from that spec; keep those spots as short, factual release summaries (no pointer-based normativity). The reviewer pass covers ONLY the agreed mirror spots under this scope.

Original option 1 (scope corrected by the refinement above): replace deviating mirrors with a clear pointer to the spec plus a short factual summary for auth/role-mapping spots only. One mechanical correction round; the reviewer then checks #1577 against this approach once.
## Handoff

Planned, unassigned. No product work or release authorization.
