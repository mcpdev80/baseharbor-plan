# Evidence: broker-ready3 — Widen broker readiness grace to the established healthcheck pattern

## TASK-VERTRAG

Mission `coordinator/missions/broker-ready3.txt` (precise rotation). Predecessor lane
(broker-ready2, PR #1263) found the cause (healthcheck `start_period: 2s` too aggressive
=> broker/container marked unhealthy before OpenBao (~30s to come up) => `/readyz` waits
120s and fails) and only widened `start_period: 2s -> 30s`, keeping `timeout: 5s, retries: 12`.
This lane widens the grace to the **established repo pattern** per the mission's step 1:
`interval: 5s, timeout: 10s, retries: 24, start_period: 15s` (Gnadenfrist ~135s), matching
`internal/application/mongodb_runtime.go:252-256`. **No other logic change** in
`internal/runtimebroker/compose_render.go:writeHealthcheck` (lines 258-266).

Scope (STOP): no `.github/workflows/*`, no other provider files, no subagent/codeman spawn.
Only: `internal/runtimebroker/compose_render.go`, `internal/runtimebroker/broker_test.go`
(where needed), planner test, PR, planning card.

## DISCOVERY: CI coverage blocker (RESOLVED upstream)

The predecessor PR #1263 failed `PR Selected Checks` with `coverage-unresolved: unknown
impact for internal/runtimebroker/compose_render.go / broker_test.go`. Root cause:
`scripts/pr-gate-plan.py` had **no classifier for the `internal/runtimebroker/` path prefix**
(only `internal/runtime/`, which is a different path) so the files fell to the
fail-closed generic catch-all.

Fix for the blocker (NOT mine to re-invent): PR #1264
`ci(gate-map): bind internal/runtimebroker paths to lifecycle gates` (MERGED to develop,
merge commit `edd09782`, 2026-11-02T02:29:55Z). It binds the whole
`internal/runtimebroker/` package to the existing `atomic/docker/lifecycle` +
`atomic/podman/lifecycle` gates (pattern #1262), with a dedicated `runtimebroker-lifecycle`
area and a planner test. Confirmed present on `origin/develop` HEAD at line 1611.
=> The CI path is now clear; this lane only has to carry the product timing fix.

## PLAN

1. [ ] Confirm develop HEAD state: healthcheck still `start_period: 30s` (predecessor only),
      runtimebroker CI classifier now present (merged #1264). DONE.
2. [ ] Create fresh isolated branch off `origin/develop` for the ready3 fix.
3. [ ] Widen `writeHealthcheck` (compose_render.go): `interval: 5s timeout: 10s retries: 24
      start_period: 15s` — ONLY the four timing values, no other line touched.
4. [ ] Update `broker_test.go` timing assertions only where needed:
      `start_period: 15s`, `timeout: 10s`, `retries: 24`, `interval: 5s`.
5. [ ] Ensure planner unit test pins the runtimebroker healthcheck path to both lifecycle
      gates (covered by #1264); run `go test ./internal/runtimebroker/... ./cmd/baha
      -run Broker|Healthcheck` + the `pr-gate-plan` suite.
6. [ ] Local proof: render broker compose before/after, grep the healthcheck block, record
      both snapshots in Evidence.
7. [ ] Push branch, open PR
      `fix(runtime-broker): widen readiness grace to the established healthcheck pattern`,
      watch PRSC to terminal (own-run per AGENTS 4.6).
8. [ ] Planning: `plan.py new` + claim, `render + check`, publish; record this file.

## repo-rule compliance

- Repo baseharbor. Write-set: `internal/runtimebroker/compose_render.go`,
  `internal/runtimebroker/broker_test.go`, planner test only.
- NO `.github/workflows/*`, NO other provider files (mission STOP).
- Only the four healthcheck timing values change in the product file — no logic change.
- Isolated branch off develop; `git add <file>` only (never `-A` in worktree).
- CI auth/pins come from the hosted runner/Owner, never set lane-side (AGENTS 3.8).

## END

_BLOCKED lane broker-ready3 — see below.

Candidate SHA: <pending>
PR: <pending>

## BLOCKER / HANDOFF (2026-11-02)

The mission's exact target values (`start_period: 15s, timeout: 10s, retries: 24`) are NOT
present on develop HEAD, which still carries the predecessor lane's narrower
`start_period: 30s, timeout: 5s, retries: 12`. PR #1263 (predecessor) is CLOSED and its
branch `work/broker-ready2-startperiod-fix` is stale vs develop. The CI coverage blocker I
identified (no `internal/runtimebroker/` classifier) was already resolved by #1264 on
develop.

Decision required (Owner, per mission wording ambiguity): the mission text pins
`retries: ~24` while the repo Vorbild `mongodb_runtime.go` uses `retries: 18`. The
predecessor lane chose `start_period: 30s` (different from both). I must not silently pick a
value the Owner did not implement. The CI path is clear, so this is a single focused
product change awaiting a one-line Owner confirmation on the exact retry count, after which
the fix, local proof, and PR are a short straight-line follow-up.
