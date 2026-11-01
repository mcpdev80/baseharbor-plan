# gatemap-r3 evidence

Mission: `coordinator/missions/gatemap-r3.txt`
Lane: `gatemap-r3` (Ornith worker) · Repo `baseharbor` · Base `origin/develop` @ `f2e43b0a`
Started: 2026-11-02

## Context

`PR Selected Checks` (CI · Source & Quality) fails closed with `coverage-unresolved` for two path families in `scripts/pr-gate-plan.py`:

- **#1222** (run 41360075776, job 125008939932): `unknown impact for testdata/adoption-parity/README.md|compose/compose.yaml|kubernetes/app.yaml|quadlet/storage.container` → the `else` catch-all at pr-gate-plan.py:1648-1650.
- **#1229** (run 41360080116, job 125008944450): `provider/capability registry or lifecycle impact ... internal/capability/{lifecycle,service_binding,service_binding_test}.go` → the `internal/capability/` branch at pr-gate-plan.py:1499-1503 (NOT in `SAFE_CAPABILITY_TESTS`, so it stays unresolved even though `require(CAPABILITY_CHECKS)` already emits `capability-package-tests`).

Repo paths are at repo root (no `scripts/` prefix — mission's `scripts/` is a doc-norm). Confirmed via `gh pr diff` and `git ls-tree origin/develop`.

## ## PLAN

- [x] Step 0: workers/todos/gatemap-r3.json + ## PLAN in evidence (see note below re: todowrite tool)
- [x] Step 1: Reality check — gh auth (mcpdev80, ssh), fetch, worktree gatemap-r3 @ f2e43b0a; reproduced both failures locally
- [x] Step 2: Reproduce both PRSC failures locally (planner.plan → coverage_status unresolved)
- [x] Step 3: Design: bind (1) testdata/adoption-parity/* else-catch-all -> INSPECT_CHECKS (same gate-Set as internal/repositoryinspect/*, pattern #1259); bind (2) internal/capability/{lifecycle,service_binding,service_binding_test}.go -> require(CAPABILITY_CHECKS)+selected.add('integration/static/public-contracts') (#1260: reference existing gates, NO new gate). Scope: only scripts/pr-gate-plan.py + test file, no .github/*
- [ ] Step 4: Edit scripts/pr-gate-plan.py: add testdata/adoption-parity/* branch before else-catch-all (1648); add capability-impl-resolved allowlist area before internal/capability/* branch (1499); update test_application_and_capability_production_remain_unresolved (remove lifecycle.go which now resolves)
- [ ] Step 5: Add planner tests (scripts/test_pr_gate_plan.py): per bind 1 positive resolved case + 1 regression unresolved/stays-unresolved case
- [ ] Step 6: Run planner tests locally full (>=179) green
- [ ] Step 7: PR against develop, title 'ci(gate-map): bind testdata/adoption-parity + internal/capability paths'
- [ ] Step 8: After PR's own PRSC GREEN, re-trigger PRSC on #1222 + #1229 (no empty rebase-repush; try `gh workflow run -- rerun --failed`; if plan-context stale, report). Watch to terminal.
- [ ] Step 9: Post END_DONE/END_BLOCKED handoff; record 1222/1229 status, PR nr, head SHA, test count

## Repo-rule compliance

- STOP (mission): no `.github/*`, only the two scripts files; no merge; no subagent/codeman-Spawn.
- AGENTS 4.2: changes hit exactly the two unbound path families.
- #1259 pattern (observability): bind to the same gate-Set as `internal/repositoryinspect/*` (`atomic/docker/observability` + `atomic/podman/observability` style — but here the capability/data static gates that already exist and run).
- #1260 pattern: reference existing gates, NO new gate.

## 1222 / 1229 status table

| PR | head SHA | before | after fix (own PR) | after re-trigger |
| --- | --- | --- | --- | --- |
| #1222 | 12828fa4 | coverage-unresolved (testdata/adoption-parity) | pending | pending |
| #1229 | befecb0c | coverage-unresolved (internal/capability/*) | pending | pending |

## END
(pending — not posted yet)
