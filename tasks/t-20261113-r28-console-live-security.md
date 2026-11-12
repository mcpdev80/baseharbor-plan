---
id: t-20261113-r28-console-live-security
card_number: "0428-017"
card_short_title: "Bind live Security view"
type: task
areas: [console]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: Connect ONLY Security read-only status/list with Core-authenticated state; no Recovery/Evidence and no new secret UI.
kanban_title: "0428-017 · Bind live Security view"
priority: normal
depends_on: [t-20261017-release-0-4-28-updates, t-20261113-r28-console-api-contracts]
repos: [mcpdev80/baseharbor-console]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
early: true
---

- [ ] t-20261113-r28-console-live-security · Connect security recovery views #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/console #kind/task
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

Connect ONLY Security read-only status/list with Core-authenticated state; no Recovery/Evidence and no new secret UI.

## Acceptance

Live redacted security state; denied roles/logout safe; no secret leak.

## Dependencies and file ownership

- Exclusive product writes: src/app/security/** and src/components/security/**; no shared adapters.
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

Current `src/app/security/page.tsx` explicitly calls `previewData.securityMaterials()`. Connect only authorized existing Core evidence; if no machine read model provides redacted security status, mark unsupported and hand one narrowly scoped Core gap to Coordinator; do not guess fields or expose secrets.

Before coding, confirm files against exact current develop/main HEAD and actual named CI. If source differs, stop and hand one precise diff to Coordinator; no guessed endpoint or promise of success.
