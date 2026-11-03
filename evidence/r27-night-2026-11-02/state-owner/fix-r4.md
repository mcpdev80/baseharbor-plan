# fix-r4 — state-owner: scope-error propagation + fixture fatal (worker w18-stateowner-r4)

- Role: Worker, lane w18-stateowner-r4, coord f49a3303. Base: head dea01b83, branch work/r27-state-owner. Basis of review-1347c findings 1+2 (finding 3 hook-semantik is ACCEPTED ok).
- Worktree: /tmp/opencode/w18-stateowner-r4-wt (checked out from origin/work/r27-state-owner = dea01b83).
- Commit: `4cc93db8a7f630fcaa9e6f55e6506505b1ca0b96` on work/r27-state-owner. Push FF dea01b83..4cc93db8. ls-remote == head. No CI run-logs, no merge PR.

## PLAN checklist
1. WORKTREE set up: fetch origin work/r27-state-owner + develop, worktree add /tmp/opencode/w18-stateowner-r4-wt (base dea01b83).
2. Scope confirmed against review-1347c findings 1+2. Fundstelle:
   - PUNKT 1: `tenantResolvedForTarget` (cmd/baha/deployment_record.go:245-248) translated a `connectorScopeForTarget` error into `(ResolvedTarget{}, false, true)` (isTenant=false, ok=true); the hook then hit the `!isTenant` branch and returned `(false, nil)` — the scope error was swallowed instead of propagating.
   - PUNKT 2: `backendBindingFixtureEmpty` (cmd/baha/application_backend_binding_change_test.go:42-44) ignored `os.Stat` error (`err == nil` only) and discarded `os.RemoveAll` error (`_ =`) — must bind to `t.Fatal` like `configureTestTargetEmpty`.
3. PUNKT 1 done: `tenantResolvedForTarget` now returns a 4-tuple `(ResolvedTarget, bool, bool, error)` carrying the resolved scope error; the `TenantOwnerResolver` hook propagates `scopeErr` as the first `(false, err)` return. A tenant with a corrupt/unreadable access scope is now refused with the real scope error, never admitted through the Core-owner path.
4. PUNKT 2 done: `backendBindingFixtureEmpty` binds `os.Stat` and `os.RemoveAll` setup errors to `t.Fatalf` in the `configureTestTargetEmpty` helper style; no test-assertion change.
5. Regression: tenant but scope corrupt/err => refused with scope error (not nil-passed); valid scope => through; genuine non-tenant => falls to core check. `TestTenantOwnerResolverCLIFallsThroughProvesNoBypass` (incl. `invalid-scope-tenant-refused`) + `TestDeploymentRecordHookPropagatesError` GREEN.

## repo-rule compliance
- Scope strictly limited to the two mission points: `cmd/baha/deployment_record.go` (tenant scope-error seam) + `cmd/baha/application_backend_binding_change_test.go` (`backendBindingFixtureEmpty`). No shared-test-file scope creep beyond what the fixture change requires; no product changes outside the tenant scope-error seam.
- No test-assertion semantics change for existing passing tests; only error handling strengthened (fatal on removal/setup errors) and error propagation added to the owner seam.
- Only explicit `git add <file>` (never `git add -A`); write-set grep over `.github/scripts` is empty.

## Regression accounting (REGRESSIONS=0 gate)
- Full `go test -count=1 ./cmd/baha/` (10-min run, FINAL_EXIT=1, 298.3s) — 5 top-level failing tests, 9 sub-fails total:
  1. `TestExternalProviderRemovalTransportsShareScopeAndExplicitStages` {cli, http, mcp}
  2. `TestExternalProviderRemovalChecksEveryManagedConsumerBeforeMutation`
  3. `TestExternalProviderRemovalCannotInferGlobalOwnershipFromTenantRole`
  4. `TestAppEditCommandCompleteProviderEditRunsRealLifecycle`
  5. `TestDoctorNotDeployedVersusIncomplete`
- All 5 verified PRE-EXISTING against clean committed base `dea01b83` (work stashed, same tests run on base): they FAIL identically on base. `TestAppEditCommand...`, `TestDoctorNotDeployed...` and the 3 `TestExternalProviderRemoval*` all fail on base `dea01b83` — NOT caused by this change.
- REGRESSIONS=0.
- `go build ./...` rc=0; `go vet ./cmd/baha` rc=0; `internal/deployment` GREEN.
- Note: worktree still carries pre-existing dirty files from a prior lane NOT related to this task (docs/de/spec/target-access-v1.md, docs/spec/target-access-v1.md, untracked docs/decisions/delivery-boundary/ + evidence-r27/delivery-boundary/). Left untouched per AGENTS 4.5.

## END
END_DONE w18-stateowner-r4: head=4cc93db8 scope-err=propagiert fixture=fatal | FF push dea01b83..4cc93db8, ancestry rc=0 gegen develop 9a57107f, write-set .github/scripts=0, REGRESSIONS=0 (full 10-min cmd/baha run: 5 env-fails TestAppEditCommand/TestDoctorNotDeployed/3x TestExternalProviderRemoval*, alle 5 auf clean base dea01b83 belegt = keine Regression)

## ANSANDE
- merge origin/develop rc=0 (branch already up to date; develop head `9a57107f8b2b71011b66025efbb73b39ab1ff12f`).
- ANCESTOR_RC=0 (develop IS an ancestor of branch HEAD via `git merge-base --is-ancestor`).
- write-set grep `.github/scripts` = 0; `go build ./...` rc=0.
- PUSH FF `dea01b83..4cc93db8` to work/r27-state-owner; HEAD `4cc93db8a7f630fcaa9e6f55e6506505b1ca0b96`; ls-remote == head.

## END
END_DONE w18-stateowner-r4: head=4cc93db8a7f630fcaa9e6f55e6506505b1ca0b96 scope-err=propagiert (tenant scope-err => hook (false,err), kein core-owner-fallthrough) fixture=fatal | FF push dea01b83..4cc93db8, ancestry rc=0 gegen develop 9a57107f, write-set .github/scripts=0, REGRESSIONS=0 (3 pre-existing TestExternalProviderRemoval* env-fails, clean-base belegt)
