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

_DONE lane broker-ready3 — fix landed in PR #1287, CI all pass, merge state CLEAN.
Candidate SHA: 6ddef0ff2b575e9a9a3c4ee1a7bb988a5d1acd86
PR: #1287 (work/broker-ready3-startperiod-grace)

## PROOF: local render before/after

BEFORE (develop HEAD, predecessor #1263 narrowed):
  interval: 5s
  timeout: 5s
  retries: 12
  start_period: 30s

AFTER (my branch, commit 6ddef0ff):
  interval: 5s
  timeout: 10s
  retries: 24
  start_period: 15s

Only the four timing values changed; the healthcheck `test` line and all other
`writeHealthcheck` output are byte-identical. Produced via a temporary
`go test -run` that renders the broker compose and prints the healthcheck block.

## CI (own run, AGENTS 4.6)

PR #1287 CI run 41447175508 — all gates pass:
- PR Selected Checks: pass (the previously-failing coverage-unresolved gate is
  now RESOLVED — runtimebroker paths bind to atomic/docker + atomic/podman
  lifecycle gates, landed by #1264)
- atomic/docker/lifecycle: pass (3m53s)
- atomic/podman/lifecycle: pass (3m55s)
- source-contracts, cli-build, cli-vet, cli-guided-tests, Trusted Plan, Exact
  Candidate, Workflow policy: pass
- mergeStateStatus: CLEAN

Local: `go test ./internal/runtimebroker/... ./cmd/baha -run Broker|Healthcheck`
pass; `scripts/test_pr_gate_plan.py` suite passes (279/193 tests). The 2 failing
receipt/plan.py tests are PRE-EXISTING on clean develop (verified by stashing my
change), unrelated to this fix.

## HANDOFF to CODEX (AGENTS §5.2)

Worker role complete: product fix + local proof + PR + CI to terminal.
Per AGENTS 5.2 the acceptance is CODEX-REVIEW at the SHA and the merge is
CODEX-MERGE — the worker does not self-approve or merge. Card status is
#status/review; resolution stays empty until CODEX-ACCEPT.

## HANDOFF POST STATUS (2026-11-02 ~13:55)

Mission requires: `codeman agent post 35cdb02e-a3b3-4e6d-86f9-1cbb35822587
"END_DONE broker-ready3: pr=1287 head=6ddef0ff | ..."`. The coordinator
session 35cdb02e-... returned HTTP 404 (session not alive), so the post could
not be delivered live. Work is complete and durable:
- PR #1287 (6ddef0ff), mergeStateStatus CLEAN, all CI gates pass.
- Plan card t-20261102-broker-ready3-widen-readiness-grace active -> #status/review,
  published to baseharbor-plan main (80a7ec7).
Evidence persists on disk + GitHub. The END_DONE handoff is re-postable once the
coordinator session is reachable again; no further worker action is required
unless CODEX-REVIEW returns a contract deviation.

## SCOPE NOTE (Owner awareness)

The mission pins `retries: ~24`; the repo Vorbild (mongodb_runtime.go) uses
`retries: 18`. I followed the mission text literally (retries: 24 => ~135s grace,
start_period 15s, timeout 10s). If the Owner prefers the Vorbild's retries:18,
that is a one-line change to compose_render.go + the test assertion and re-runs
cleanly.

