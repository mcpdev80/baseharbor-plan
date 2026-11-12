---
id: t-20261113-r28-console-monitoring-entry
card_number: "0428-014"
card_short_title: "Add Console Monitoring link"
type: task
areas: [console]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: Add a single Monitoring nav entry linking an authenticated operator to the validated installation-owned Grafana URL. Show clear…
kanban_title: "0428-014 · Add Console Monitoring link"
priority: normal
depends_on: [t-20261017-release-0-4-28-updates, t-20261113-r28-grafana-secure-access]
repos: [mcpdev80/baseharbor-console]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
early: true
---

- [ ] t-20261113-r28-console-monitoring-entry · Add Console Monitoring link #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/console #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261113-r28-grafana-secure-access](t-20261113-r28-grafana-secure-access.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261113-r28-grafana-secure-access](t-20261113-r28-grafana-secure-access.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Add a single Monitoring nav entry linking an authenticated operator to the validated installation-owned Grafana URL. Show clear disabled/not-authorized state; NO iframe, dashboard engine, direct arbitrary URL or guessed API routes.

## Acceptance

One safe link to the correct Core/Target-owned Grafana origin and no link for unauthorized/disabled cases.

## Dependencies and file ownership

- Hard prerequisites (not mere priority): t-20261017-release-0-4-28-updates, t-20261113-r28-grafana-secure-access.
- **Exclusive write ownership:** src/components/shell/** navigation and src/app/monitoring/** only; no shared machine decoders, Providers/Observability pages or auth modules.
- A referenced task must be accepted/merged before implementation if an actual interface is needed; read-only inspection and isolated schema fixtures may start earlier. Never base work on another worker's unmerged branch.

## Worker instructions (256k context budget)

1. Read this card and only the directly named source files, predecessor interface/commit and existing tests. Do not load the whole ecosystem into context.
2. Identify the exact existing implementation, change only the specified behavior and reserved files. If a missing dependency or conflicting owner appears, stop and hand the Coordinator one concrete missing contract/path; do not self-expand the scope.
3. Add/adjust the smallest executable positive and negative regressions described here. **Test -> existing CI check -> file-change trigger -> actual result** is mandatory; no skipped assertion may count as pass.
4. Run targeted source checks; native Docker/Podman/browser only where this card uniquely requires them. Reuse existing selected CI jobs and fixture owners; no shadow approval/evidence system.
5. Open one limited product PR against the normal development branch and hand off exact commit SHA, changed files, commands/check IDs, actual passed assertions, gaps and rollback. No worker self-merges.
6. **Codex reviews independently and merges** only after required tests on the exact PR HEAD. Coordinator updates this plan note/Obsidian state after acceptance; max five non-overlapping workers concurrently.

## Required checks and CI routing

Component/navigation test for enabled/disabled, origin mismatch and denied actor plus existing Console build.

## Handoff

Not claimed. Do not mark accepted from plan creation or a draft PR.

## Verified code entry points and no-guess rule (2026-11-13)

Current shell/session: `src/components/shell/core-session-provider` and `src/components/live/live-core-view.tsx` already enforce verified Core session. Use the authorized provider management surface URL from accepted Grafana contract (032) and access work (013), not arbitrary `NEXT_PUBLIC_` URL or hard-coded Grafana port. Scope UI navigation to selected installation.

Before coding, confirm files against exact current develop/main HEAD and actual named CI. If source differs, stop and hand one precise diff to Coordinator; no guessed endpoint or promise of success.
