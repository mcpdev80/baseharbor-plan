# chain-a Evidence — 2026-11-01

Mission: coordinator/missions/chain-a.txt — chain link raised to current base and qualified. Two PRs in order.

## STARTING STATE (recorded before any change)
- baseharbor repo HEAD / origin/develop = 5c903560 (>= required base 5c903560) ✓
- Worktree chain-a created at baseharbor/worktrees/chain-a, branch work/gh-ci-core checked out (486abbca)
- gh authenticated as mcpdev80 (repo scope, ssh)

### PR #1239 (work/gh-ci-core) — STARTING
- state: OPEN, base: develop (5c903560), head: work/gh-ci-core @ 486abbca
- local merge-base vs develop = cb6b7387 → branch is BEHIND develop by ~14 commits
- rebase-starting origin/develop tip = 5c903560 Merge PR #1255

### PR #1238 (work/gh-acc-suite) — STARTING
- state: OPEN, base: develop (5c903560), head: work/gh-acc-suite @ 38073e9e
- local merge-base vs develop = cb6b7387 → branch is BEHIND develop (19 ahead / 1 behind)

## PLAN
1. gh api PR state check (done) — both open, base develop
2. rebase each PR branch onto origin/develop (mechanical conflicts only; ours = PR change)
3. push origin work/<branch> (force only on same branch)
4. watch PR Selected Checks + affected gates to terminal (own-run duty; record Run-IDs + error lines)
5. GREEN -> 'review' status in Planning card + PR comment with requal proof; RED (workflow-design) -> do NOT bend, document probe-ref qual like parity-1257, END_DONE; RED (real test failure) -> END_BLOCKED with error line
6. No merge (Coordinator), no --admin, no new gates/scripts, no ci.yml changes except PR's own

---

## PR #1239 (work/gh-ci-core)

### Rebase
- (status recorded here)

### Push
- (status recorded here)

### CI / gates (own run)
- Run-IDs:
- Results:

### Outcome
- GREEN -> review + comment
- RED workflow-design -> probe-ref qual + END_DONE
- RED test failure -> END_BLOCKED

---

## PR #1238 (work/gh-acc-suite)

### Rebase
- (status recorded here)

### Push
- (status recorded here)

### CI / gates (own run)
- Run-IDs:
- Results:

### Outcome
- GREEN -> review + comment
- RED workflow-design -> probe-ref qual + END_DONE
- RED test failure -> END_BLOCKED

---

## HANDOFF
post 35cdb02e-a3b3-4e6d-86f9-1cbb35822587 "END_DONE|END_BLOCKED chain-a: <pr>=<gruen|blocked>... runs=<ids> | <Grund>"
