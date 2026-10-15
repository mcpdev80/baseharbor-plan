---
id: 2026-10-15-task-prs-supersede-shared-release-prs
status: accepted
sources: []
---

# Task PRs against develop supersede the shared release-PR rule

## Context

Several sources still carry the section "Binding PR workflow: one shared release PR, two sessions (2026-10-10)" — baseharbor#174, #874, #875 and #876 — or a "two sessions per release" split (#174, #777, #818–#823). Later and explicitly broader sources say otherwise: baseharbor#155 and #427 (updated 2026-10-15) state that the shared-PR/two-session model applies **only to v0.4.25 (#872/#881)** and that from v0.4.26 #888 governs small task branches/PRs against develop; #174's own current-boundary section says the older session/shared-branch sections are historical; `docs/DEVELOPMENT_GUIDELINES.md` on develop says "From v0.4.26 each unit of work lands as its own small branch and pull request against develop."

## Decision

The later rule applies to every release from v0.4.26 on. The "session" splits in release notes are kept only as work areas with separate file ownership. Release notes and tasks in this vault say so where the source still contains the old rule; the original wording stays in the snapshot. core-882 remains the agreed separate `develop` prerequisite.

## Consequences

Before the cutover, the Maintainer should remove or mark the outdated sections in the source issues (listed in [migration/conflicts.md](../migration/conflicts.md)). This decision does not change anything about v0.4.25.
