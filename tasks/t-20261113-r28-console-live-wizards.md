---
id: t-20261113-r28-console-live-wizards
card_number: "0428-016"
card_short_title: "Wire live application wizard"
type: task
areas: [console]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: Connect ONLY existing application new/edit wizard to authenticated Core plan/confirm/apply. No Target or workspace wizard changes.
kanban_title: "0428-016 · Wire live application wizard"
priority: normal
depends_on: [t-20261017-release-0-4-28-updates, t-20261113-r28-console-api-contracts]
repos: [mcpdev80/baseharbor-console]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261113-r28-console-live-wizards · Connect existing management wizards #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/console #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261113-r28-console-api-contracts](t-20261113-r28-console-api-contracts.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261113-r28-console-api-contracts](t-20261113-r28-console-api-contracts.md)  
**Required by:** [t-20261113-r28-console-native-journey](t-20261113-r28-console-native-journey.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Connect ONLY existing application new/edit wizard to authenticated Core plan/confirm/apply. No Target or workspace wizard changes.

## Acceptance

App create/edit with actual Core result; denied, missing consent, stale session, duplicate submit tested.

## Dependencies and file ownership

- Exclusive product writes: src/components/wizard/application-* and src/app/applications/new/**; no shared adapters.
- Dependencies are the frontmatter depends_on values. Do not wait for unrelated Grafana/Console cards.
- Before implementation read current exact-source contract and named files only. If an API is missing, report one concrete blocker to Coordinator; do not invent a second API.

## Required checks and CI routing

- Small positive/negative tests for the listed acceptance; bind exact tests to existing selected CI triggers, native tests only for covered runtime behavior.
- Worker supplies exact PR HEAD, affected files, commands/checks, results and cleanup; no skipped test counted as passing.

## Coordinator / Codex handoff

- Coordinator assigns one independent ready task to one of five workers, claims it in planning before work, and dispatches only after accepted dependencies. Capacity is a ceiling, not a requirement to start five agents.
- Worker delivers one small PR against product repository's normal development branch with exact HEAD, tests -> selected check -> trigger -> execution result, and records a planning handoff; no self-review, merge or release.
- Codex is the independent reviewer and designated merger for approved, green PRs; it checks architecture, changed paths, test routing and exact-source evidence before merging. No merge on skipped/failed mandatory assertions.
- Following merge, coordinator reconciles the planning card and unlocks dependent ready work only after acceptance. No release/tag/promotion by worker or coordinator.

## Handoff

Not started. Claim, PR, checks, evidence and actual blockers will be recorded here.

## Verified code entry points and no-guess rule (2026-11-13)

Current `src/app/applications/new/page.tsx` renders `ApplicationInitWizard`; source `src/components/wizard/application-init-wizard.tsx`. Existing actual mutation UX in `src/components/live/live-core-view.tsx` has `ApplicationActions`; reuse `MachineSession` and safety consent from that component. Do not add a second wizard engine or direct runtime control.

Before coding, confirm files against exact current develop/main HEAD and actual named CI. If source differs, stop and hand one precise diff to Coordinator; no guessed endpoint or promise of success.
