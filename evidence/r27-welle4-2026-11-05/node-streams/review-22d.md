# CODEX-REVIEW 22d (coordinator-recorded) — connector PR #22, round 4

Verdict: **REJECT** — exact head `cce09a86a59` (pane witness, session 5ec1339c, 2026-11-05 15:12-15:15Z).
The reviewer's own act write was rejected TWICE by her sandbox ("Sandbox-Quota-Fehler", then
"Read-only file system" on the released absolute path); at coordinator request she replied NEIN and asked
for transcription. All claims below are her pane statements, cross-checked by the coordinator where marked.

## Verified by the reviewer (and re-measured by the coordinator)

- Mixed A–D ensemble passes with `-race -count=20` at the exact head (coordinator: runs 42031707838-family
  analogues in connector repo: two hosted runs terminal SUCCESS at `cce09a86a59`; branch head matches real
  ls-remote; main is ancestor).
- `execx/executor.go` change limited to the io.EOF transition and justified in the stream-end path
  (coordinator: diff shows the file within the chain; blob scrutiny deferred to round 5).
- trust/session blobs identical to main.

## Blockers (reviewer findings)

1. **A and B still assert THROUGH THE HELPER**: `h.access.streams.replay(...)` direct calls remain the
   vehicle for expiry/replay assertions (coordinator grep-witness on the pushed head:
   `internal/connector/stream_evidence_test.go` lines 615, 627, 701 call `h.access.streams.replay` — the
   r4 claim "echte Kette" holds for C/D, not for A/B).
2. **Mutants NOT self-verified**: the reviewer's mutant cells (stale-guard removal, duplicate-allow) could
   not be run because of the sandbox write failure; they are OPEN, not green, not red.

## Recipe for round 5 (from the reviewer's pane, folded into mission w185)

- Route A (expiry) and B (exact replay) assertions through a fresh imported `NewHandshakePair` connection
  against `ServeLogStream` — the SAME ceremony C/D use; helper-direct replay calls are the stop criterion.
- Run all four mutants single-shot with the fixed harness and record literal FAIL lines.
- Keep execx/io.EOF (justified), but prove stream-end tests still bind via the real chain.

## Process notes

- Second occurrence of the vanished-act class (after 1373g): verdict lives in the pane, file absent.
  Coordinator transcription rule applies: findings are WITNESSES, not the reviewer's act; the reviewer must
  re-sign by writing the next act herself once her sandbox is healthy (tracked as operational defect:
  rebound codex session sandbox mounts the released path read-only — check project trust for the new
  workers/ working-dir).
