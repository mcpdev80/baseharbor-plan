---
id: t-20261127-coord-session-retention
card_number: "0428-352"
card_short_title: "cleanup session retry safety"
aliases: []
type: maintenance
areas: [coordination, tooling]
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Make coordinator cleanup safely resumable after a partial release: resolve one Codeman lane to exactly one OpenCode session,…"
kanban_title: 0428-352 · cleanup session retry safety
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
created: 2026-11-27
---

- [ ] t-20261127-coord-session-retention · 0428-352 Coordinator cleanup preserves session identity through PARTIAL retries #task #release/v0-4-28 #status/planned #view/ready #area/coordination #area/tooling #kind/maintenance
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Make coordinator cleanup safely resumable after a partial release: resolve one Codeman lane to exactly one OpenCode session, preserve that reference across retries, and release the pool reservation only when the session is gone.

## Finding

- **(i) Ambiguous directory mapping:** `coordinator/scripts/release-lane.py:47-72` maps by working directory and may fall back to a clock/name heuristic; `_resolve_by_reference` compares the registered directory at lines 89-95. `coordinator/scripts/worker-cleanup.sh:76-88` inventories the lane and calls release-lane with the selected session ID. Lanes spawned from shared `workers/.models/<channel>` paths can share the same directory, so the directory is not a unique lane identity.
- **(ii) Retry reference is not durable on the first PARTIAL:** `release-lane.py:212-226` handles unresolved mapping by freeing the lane reservation and returning PARTIAL while retaining the idle session. The pending exact session mapping is written only later at lines 240-245, after a mapping has succeeded. Thus a partial attempt has no durable mapping for a later cleanup pass if its spawn reference is no longer available.
- **(iii) Session retains a seat after reservation release:** `worker-cleanup.sh:83-88` stops cleanup when release-lane reports incomplete. `release-lane.py:222-224` can free only the reservation while the session remains. `pool-reconcile.py status` then still sees the retained session and reports the seat occupied.

## Remediation

Use one of these durable identity strategies:

- Give every lane an unambiguous, lane-specific working directory so directory matching cannot select multiple sessions; or
- Persist the exact Codeman session ID and OpenCode session ID before any partial/destructive transition, and resume from that reference on every subsequent run.

In either strategy, the reference must survive the first PARTIAL result; do not consume or clear it until cleanup proves the Codeman session and OpenCode session are released. Keep the operation fail-closed: never guess a session or remove a sibling lane's reservation.

## Acceptance

- A regression reproduces two lanes under a shared `.models/<channel>` directory and proves that cleanup selects the intended session by the unique per-lane directory or persisted exact session IDs.
- A first PARTIAL attempt retains a durable retry reference. A subsequent `worker-cleanup.sh <lane> --run`, after structured acceptance and published evidence authorize release, uses that same exact reference and removes the Codeman session, deletes the mapped OpenCode session, and frees that lane's reservation.
- After successful release, `python3 coordinator/scripts/pool-reconcile.py status` reports the seat vacant. An idle retained session must not be mistaken for a freed seat merely because its reservation disappeared.
- A failure at any intermediate step preserves enough identity/state for retry and never deletes a different lane's session or reservation.
- Add regression coverage to the coordinator tooling's durable CI/native gate in the same implementation change; record the exact test, gate, trigger, and executed result in the handoff.

## Reproduction records

- `coordinator/board/acceptance.json#w401-session-retained` — `2026-11-27T19:08:09Z`: second cleanup PARTIAL; reservation released, idle session `2cd2e2d6` retained because no spawn reference was available.
- `coordinator/board/acceptance.json#w402-cleanup-partial` — `2026-11-27T19:25:00Z`: repeated PARTIAL from spawn-reference/session-mapping failure; reservation handled, session still idle.
- `coordinator/board/acceptance.json#cleanup-defect-rootcause` — `2026-11-27T19:30:29Z`: shared `workers/.models/<channel>` makes directory-to-session resolution ambiguous; proposed remedies are lane-specific working directory or persisted session-ID reference.
- `coordinator/board/acceptance.json#flash2-not-vacant` — `2026-11-27T19:44:38Z`: retained idle sessions continue occupying seats after reservations are freed; pool reconciliation refused dispatch because the seat was not vacant.

## Ownership

- Owned area: `coordinator/scripts/release-lane.py`, `coordinator/scripts/worker-cleanup.sh`, focused coordinator regression tests, and the relevant durable coordinator gate.
- No product PR or workflow change is part of this card creation.
