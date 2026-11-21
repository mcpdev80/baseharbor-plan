# Stop record: lane 0428-211-hopdev (539ef145) — obsolete hop mission

The coordinator dispatched `coordinator/missions/0428-211-hopdevelop.md` at 10:3xZ against a board state that was
twenty minutes stale. While the mission was in flight the Owner merged PR #1733 and closed card 0428-211
`accepted` (plan commit `f011f6d6`).

- Remote witness read by the lane at stop time: `refs/heads/develop` = `44b55ea4b`, PR #1733 head = `3aec8701e497`
  (`mergedAt` 2026-11-21T09:34:10Z, base `develop`).
- Lane declaration: no push, no PR change, no rebase performed after the stop command.
- Disposition: `stopped-no-work`. Seat released for hunt slice H-V32 (post-merge desk for #1733).

## Lesson recorded

Before every dispatch the coordinator must read `gh pr view <pr> --json state,mergedAt` and not rely on the board
alone (AGENTS 3.5: idle or event does not prove task state; the same law applies to the mission's premise).
