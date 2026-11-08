# v0.4.27 — Open-board reconciliation (2026-11-08)

## Scope

Only release **v0.4.27** cards outside Closed: active, review, wait, ready, waiting/planned, backlog. Closed cards and other releases are excluded from this cleanup. Snapshot of generated release view at inspection: 152 release task rows, of which **44 not terminal** (active 9, review 1, wait 4, ready 15, waiting 15). These numbers are a snapshot, not a live worker allocation oracle.

## Confirmed repository-state corrections

| Card | GitHub PR truth | Action |
| --- | --- | --- |
| 0427-003 Greenfield stacks | #1429 merged; #1432 remains open | Added dated status to card, keep active until required SINGLE/HA topology evidence |
| 0427-039 Node CLI | #1436 open, Trusted Plan failed; #1438 merged | Keep wait, coordinator ownership and E2E obligations |
| 0427-110 Compose isolation | #1383 merged | Prior audit documented remaining Podman readiness; do not equate merge with acceptance |
| 0427-116 Remote-Up | #1407 merged during this audit (previously open) | Existing card closed/accepted already; **do not re-open**; update historical PR timeline separately |
| 0427-122 Keycloak orphan | #1444/#1448/#1449 merged | Earlier stale wait reason corrected, native exact-SHA resource count still required |
| 0427-123 Machine consent | #1445/#1446 merged | Keep wait pending native PTY negative/positive proof |
| 0427-127 Bootstrap leak | #1454 merged | Keep review until Docker/Podman cleanup evidence |
| 0427-130 Up alias parity | #1459 merged during audit | Added status to card; owner `pending-lane-0427-130-r5` not verified as an active process |
| 0427-132 Destroy retry | #1453 and downstream #1464 merged | Existing audit documents CI PASS, exact develop run remains to verify |
| 0427-133 Greenfield isolation | #1460 merged | Existing card remains active for distinct isolated greenfield E2E; its owner was concurrently changed to `lane-w133-greenfield-r4` by another actor, **not overwritten** |
| 0427-134 CA/PKCE | #1455 closed without merge; #1457 open | Require supersession/remaining-scope review before a status change |
| 0427-136 App-init owner seam | #1458 closed without merge; #1464 included relevant fix | Card itself already explains supersession, leave worker ownership intact |
| 0427-137 Ready-PR native CI | #1463/#1464 merged | Previously annotated; informational CI task needs a canonical acceptance/render decision, not a second worker |

## Scheduling and board semantics

- The 15 ready cards are unassigned work and must stay Ready until explicitly claimed. Do **not** allocate workers as a side effect of auditing.
- The 15 waiting/planned cards have open dependencies. They are not the same as `wait`, which requires a previously started task and an owner.
- Keep `blocked` for a true owner decision or currently impossible implementation only.
- No changes to Codeman's live branches, worker reservations, or active ownership were made.
- Changing task statuses requires **one coordinated** `scripts/plan.py render && scripts/plan.py check` cycle with refreshed generated views. This reconciliation changed narrative only, preserving synchronized board projections and avoiding an inconsistent generated vault.

## Priority follow-up

1. Validate whether 0427-130's `pending-lane-...` is a real worker; if not, mark the actual owner/acceptance handoff before closing.
2. Decide closure for 0427-137 CI information card using merged code and exact native tests; do not keep artificial implementation workload open.
3. Finish 0427-127 cleanup evidence and 0427-132 exact develop native acceptance.
4. Clarify 0427-134 (#1455 closed unmerged) versus #1457 scope.
5. Confirm 0427-003 #1432 required topology cells before merge.
