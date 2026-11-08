# BaseHarbor Plan integrity audit — 2026-11-08

## Scope and evidence

- Main tree inspected: 2,359 tracked blobs, 415 task notes, 17 generated views.
- Read: planning workflow, native Bases configuration, CLI renderer/validator, release overview, selected active/review/wait tasks.
- Live GitHub PR merge states verified for #1151, #1383, #1407, #1427, #1436, #1438, #1444, #1445, #1446, #1448, #1449, #1453, #1454, #1455, #1457, #1458, #1459, #1460, #1463.
- This was **not** an exhaustive content inspection of each of the 415 cards. No unproven global clean bill of health.

## Corrected now

1. 0427-110: #1383 merged (812c99c8); residual Podman/contaminated acceptance kept open.
2. 0427-127: #1454 merged (22a3cb8a); cleanup proof missing, review not silently closed.
3. 0427-132: #1453 merged (d30de3a4), downstream native #1464 PASS per Owner handoff; exact develop push acceptance kept distinct.
4. 0427-133: #1460 merged (201735b0); greenfield isolated native E2E remains separate acceptance.
5. 0427-137: #1463 merged (88acebc5); downstream #1464 merged (cd494610) and native destroy-retry qualification passed, previous warning obsolete.
6. 0427-122: old wait_reason falsely said #1448 was still running after merge; updated without changing Wait.
7. README: replaced obsolete CardBoard setup text with native Bases workflow.

## Still requires verification, not silent status mutation

- 0427-039: #1436 open, Trusted Plan failed; #1438 integrated but full first-owner/connector native acceptance not proven. Wait retains coordinator ownership.
- 0427-116: accepted/closed while #1407 remains open; card acceptance and PR lifecycle must be tracked separately. #1407 Go-unit result not terminal at first check.
- 0427-110: #1383 merged, but Podman application readiness and matrix remain open; check owner lane is genuinely occupied before marking active.
- 0427-127: #1454 merged but no evidence link for Docker+Podman residual-resource cleanup.
- 0427-132: verify exact SHA develop push both runtimes before acceptance.
- 0427-133: owner value `pending-lane-0427-133-r4` needs reconciliation to an actual assigned worker; #1460 merge alone does not meet greenfield E2E contract.
- 0427-134: #1455 closed without merge, #1457 open; investigate whether #1455 was superseded rather than accidentally accepted.
- 0427-136: #1458 open, keep existing worker ownership.
- 0427-130: #1459 open; worker/Codeman ownership, no intervention.
- 0427-123: #1445 and #1446 merged; PTY native Docker+Podman acceptance still open; Wait is appropriate.
- 0427-006: release prepare waiting for explicit Owner publish decision, do not interpret merge #1151 as release authorization.

## Integrity rules

- Source of truth for task lifecycle is `kanban_status`; `kanban_lane` is the native board projection.
- Wait = paused assigned work with an explicit `wait_reason`; Blocked = Owner decision or technically impossible implementation.
- A merged PR does **not** imply completed acceptance. Never close without precise evidence and resolution.
- Treat historical status lines as historical; add dated append-only evidence rather than overwriting witnesses.
- After changing task status, execute `python3 scripts/plan.py render && python3 scripts/plan.py check` and publish the generated views together. This audit deliberately made no unrendered status transitions.
- Do not overwrite coordinator/worker live branches or reassign a claimed card without checking its session ownership.

## Remaining coverage limitation

A full vault-wide semantic check of every task and generated projection was not performed in this pass. Planning CI `Validate planning` is the authoritative repository structural validation; check the terminal result on current main before declaring structural consistency.
