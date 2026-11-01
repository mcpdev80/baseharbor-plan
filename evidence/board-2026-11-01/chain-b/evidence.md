# chain-b Evidence — 2026-11-01

Mission: coordinator/missions/chain-b.txt — chain link raised to current base and qualified. Two PRs in order.

## STARTING STATE (recorded before any change)
- baseharbor repo HEAD / origin/develop = 5c903560 (>= required base 5c903560) ✓
- Worktree chain-b created as independent baseharbor clone at workers/worktrees/chain-b
- gh authenticated as mcpdev80 (repo scope, ssh)
- Model: Ornith (worker-ornith1.5)

### PR #1242 (work/fix-observ-consent) — STARTING
- state: OPEN, base: develop (5c903560), head: work/fix-observ-consent @ f392273e
- single file: cmd/baha/app_observability_acceptance_test.go (Go test only)
- PR Selected Checks = fail (run 412513056466) → BLOCKED: coverage-unresolved: CLI runtime impact needs qualified targeted native coverage
- gate classification: cmd/baha/*.go → cli-unresolved-runtime-impact branch (requires qualified targeted native coverage, never path-resolvable)

### PR #1243 (work/gh-dispatch2) — STARTING
- state: OPEN, base: develop (5c903560), head: work/gh-dispatch2
- files: .github/workflows/runtime-broker.yml, .github/workflows/runtime-s3-acceptance.yml (workflow files only)

## PLAN
- [ ] 1. gh api PR state check — both open, base develop (done)
- [ ] 2. rebase each PR branch onto origin/develop (mechanical conflicts only; ours = PR change)
- [ ] 3. push origin work/<branch> (force only on same branch)
- [ ] 4. watch PR Selected Checks + affected gates to terminal (own-run duty; record Run-IDs + error lines)
- [ ] 5. PR #1242: coverage-unresolved = native-qualification case → probe-ref qual like parity-1257, END_DONE w/ both proofs (no bend). PR #1243: workflow files → workflow-design RED → probe-ref qual, END_DONE.
- [ ] 6. No merge (Coordinator), no --admin, no new gates/scripts, no ci.yml changes except PR's own
- [ ] 7. HANDOFF: post 35cdb02e-a3b3-4e6d-86f9-1cbb35822587 "END_DONE|END_BLOCKED chain-b: ..."

## END
<lane> DONE|BLOCKED: to be filled

