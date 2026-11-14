---
id: t-20261114-r28-cli2-coordination
card_number: "0428-072"
card_short_title: "coordinate five workers"
type: task
areas: [cli, architecture]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: Coordinate the CLI redesign as one owner-requested programme with at most five implementation/audit workers and one coordinator.…
kanban_title: 0428-072 · coordinate five workers
priority: high
depends_on: [t-20261017-release-0-4-28-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261114-r28-cli2-coordination · CLI redesign: coordinate five workers #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/architecture #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Coordinate the CLI redesign as one owner-requested programme with at most five implementation/audit workers and one coordinator. Maintain the existing `t-20261114-r28-cli-command-semantics` umbrella and all release prerequisites.

## Coordinator duties

- Read [owner brief](../evidence/cli-redesign-20261114/brief.md), [mapping](../evidence/cli-redesign-20261114/command-map.md), [code entry index](../evidence/cli-redesign-20261114/code-entry-index.md), product `AGENTS.md`, development guidelines and current release status. Recheck all source heads, card claims and existing work.
- Assign the five audit slices to separate workers only after their prerequisite is accepted. Claim one card per worker through the planning protocol. Do not treat unowned Ready cards as dispatched work.
- Preserve a single owner for the approved contract, registry/help integration, CI routing and other shared files. Resolve overlap before scheduling; workers must not edit another lane's files. Re-evaluate dependencies as findings and current state change, and preserve other agents' work.
- Maintain short context-limited task packets: exact goal, bounded files, predecessor interface, negative cases, tests and CI routing. Do not assume proposed CLI names are agreed; request missing product decisions through the Owner rather than inventing them.
- Collect exact-SHA PRs, real checks and handoffs. Send reviewable candidates to Codex acting under the Owner's maintainer delegation for actual review and, after required checks, authorized PR merge. Do not claim independent review, green tests, a merged PR, native execution or release merely because a worker reports it.
- Keep max five workers active, track blockers, avoid unnecessary waiting/retries, and transition/claim cards using the plan tool and normal concurrency-safe direct-main workflow. No release or tag is authorized.

## Acceptance

- Five audit slices and all implementation cards are coordinated against accepted prerequisites with no unowned overlapping writes.
- `t-20261114-r28-cli2-final-acceptance` receives a complete, evidence-backed handoff; all checks and mandatory CI test routing are either genuinely proven or reported as blockers.
- The existing v0.4.28 umbrella stays blocked until the final acceptance card is actually complete.

## Handoff

Planned, unassigned. No workers dispatched, implementation, product merge or release has occurred.
