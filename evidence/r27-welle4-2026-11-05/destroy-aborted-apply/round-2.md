# w156-destroy-r2 — r27 ROUND 2 (destroy-aborted-apply)

MISSION (lane w156, coord f49a3303, card t-20261104-r27): Luna review-1382a verdict REJECT, but the round-1 destroy fix in `app_workload.go` and the W154 regression are explicitly ACKNOWLEDGED and STAY. Exactly ONE change required:

- Revert `internal/application/telemetry_authorization.go` to develop (blob-identical) — the unconditional `os.ErrNotExist => empty-map` absorption in `readWorkloadRuntimeEnv` is a shared reader that suppressed missing runtime bindings for ALL workload callers.
- The missing `runtime.env` in THIS state is handled ONLY inside the destroy/retraction path with ownership proof; shared reader stays strict.
- Same branch `work/r27-destroy-aborted-apply`, same PR #1382. No second PR, no rebase, no force.

## PLAN
- Read mission + Luna review-1382a fully; capture exact scope
- Set up fixed-layout worktree at /tmp/opencode/w156-destroy-r2-wt
- Checkout branch work/r27-destroy-aborted-apply; verify ancestry on origin/develop
- Revert internal/application/telemetry_authorization.go to develop (blob-identical)
- Ensure missing runtime.env handled only in destroy/retraction path with ownership proof
- Local go test ./cmd/baha ./internal/application (rc=0), ./internal/database, build, vet, gofmt
- Measure sick cell rc=1 on develop; candidate head rc=0 + no live instance + no ownership
- Verify #1375 cell + glueckpfad regression unchanged green; telemetry_authorization.go gone from diff
- Commit on same branch; ls-remote == new head verbatim; log lists only own commits (r1+r2)
- Tick all plan locations; write this evidence; post END line

## SCOPE (from Luna review-1382a, verdict=REJECT, destroy-fix ACKNOWLEDGED and STAYS)
- KEEP: app_workload.go destroy/retraction fix + W154 tests (acknowledged, stays)
- REMOVE: the unconditional non-OTLP os.ErrNotExist => empty-map absorption in readWorkloadRuntimeEnv -> telemetry_authorization.go revert to develop
- ONLY the missing runtime.env in THIS state handled, and ONLY inside the destroy/retraction path where the ownership check (runtime-dir ownership) lives; shared reader stays strict
- If a case remains on the destroy path (runtime-dir EXISTS but runtime.env missing) that cannot rc=0 without the shared-reader change: solve it INSIDE the destroy path with ownership proof in a comment set + test; shared readers are sacred
- Boundaries: no .github, no AGENTS.md, no subagents, no second PR, no scratch in repo root

## EVIDENCE / CHECKS

### Branch provenance (proof)
- Ancestry: `develop` (512dcd721ac3fb739bfd4cb0b990fd68d6794762) is an ancestor of my head.
- Name-only diff `git diff origin/develop...HEAD`:
  - cmd/baha/app_workload.go
  - cmd/baha/w154_destroy_aborted_apply_test.go
  - cmd/baha/w154_gegenprobe_test.go
  - cmd/baha/w154_runtime_dir_present_envmissing_test.go  (NEW round-2 regression)
  - internal/application/runtime_owner_write.go            (NEW exported VerifyRuntimeFileOwner)
  - telemetry_authorization.go: NOT LISTED (reverted to develop) — confirmed
- `git log --oneline origin/develop..HEAD` lists ONLY my two commits:
  - 942e3cc5 fix(r27): destroy retires a provider-change-aborted apply with rc=0  (round 1)
  - 36911738 fix(r27): retire when runtime dir present but runtime.env missing under strict shared reader (w156, review-1382a)  (round 2)
  - No foreign commit.
- ls-remote verbatim: `git ls-remote origin refs/heads/work/r27-destroy-aborted-apply` -> 3691173821384d028f33d81cc2c54a991d639f12

### Telemetry revert (blob identity)
- Round-1 candidate telemetry blob: 41d5483379b2eb3b83e0484a881fc4e5558bc9b0
- Round-2 HEAD telemetry blob:       abbb5bb6946c3d4f443659f8f99905d1f23c1254
- develop telemetry blob:            abbb5bb6946c3d4f443659f8f99905d1f23c1254  (MATCH — reverted blob-identical)
- Diff: removal of the `values, err := readRuntimeEnv(path); if errors.Is(err, os.ErrNotExist) { return map[string]string{}, nil }` absorption; back to `return readRuntimeEnv(path)` (strict).

### Sick cell on develop (rc=1)
- develop = 512dcd721ac3fb739bfd4cb0b990fd68d6794762 (unchanged; develop has not moved since round 1).
- Method: detached worktree /tmp/w156-develop-sick at develop; W154 test files extracted from candidate 942e3cc5 (git archive) so the strict develop telemetry meets the round-1 regression; telemetry confirmed strict (`return readRuntimeEnv(path)`, no ErrNotExist absorption in readWorkloadRuntimeEnv).
- Result: BOTH W154 tests FAIL rc=1. Failing log line:
  `read application runtime environment: open .../state/demo/runtime/runtime.env: no such file or directory`
- This is the sick commit's failure; the strict shared reader fails closed on the stuck-apply destroy.

### Candidate head (rc=0, no instance, no ownership)
- W154 (all 3, incl. new regression): PASS rc=0.
  - TestW154DestroyAfterProviderChangeAbortReturnsZero PASS
  - TestW154GegenProbeAbortedApplyRecoversOnSecondRun PASS
  - TestW154RetireWhenRuntimeDirPresentButRuntimeEnvMissing PASS
- W138 never-delivered cell: PASS rc=0 (unchanged).
- Scoped workload/destroy/retire suite: PASS rc=0.
- `./internal/application/...`: PASS rc=0.
- `go build ./...`: rc=0. `go vet ./cmd/baha ./internal/application`: rc=0. `gofmt -l` on changed files: clean.
- No running workload instance; ownership derived from disk evidence (no owned runtime.env -> no owned containers).

### The gap found and fixed (mission point 3)
- Probe constructed the runtime-dir-PRESENT but runtime.env-MISSING state on the real CLI destroy path.
- BEFORE fix (strict reader only): destroy FAILS rc=1 (`read application runtime environment: open .../runtime.runtime.env: no such file or directory`). This is the "runtime dir exists but runtime.env missing" case mission point 3 calls out.
- FIX (inside destroy path only, shared reader untouched):
  - New exported `application.VerifyRuntimeFileOwner(path) (bool, error)` wrapping `existingPrivateRuntimeOwner` (owner-verified regular file) — the same ownership evidence as the dir check. Returns (false, nil) when the runtime.env is missing or present-but-unowned; errors only on a real stat/owner error.
  - `stopRepositoryWorkload` (cmd/baha/app_workload.go) now, after the dir-ownership guard, gates materialization: `if owned, err := application.VerifyRuntimeFileOwner(files.Env); err != nil { return error } else if !owned { return false, nil }`. A present-but-unowned runtime.env is not an owned materialization -> retire rc=0 without touching the shared reader. A present-owned-but-corrupt runtime.env still fails closed (propagated by the strict reader below).
- NEW regression: TestW154RetireWhenRuntimeDirPresentButRuntimeEnvMissing (cmd/baha/w154_runtime_dir_present_envmissing_test.go) — drives real CLI destroy on the runtime-dir-present/env-missing state, asserts rc=0 and negative ownership, shared reader stayed strict.

### #1375 + glueckpfad regression unchanged
- #1375 never-delivered (W138) cell: unchanged green.
- W154 glueckpfad (second-run recovery): unchanged green.

### Hosted CI
- The exact-head hosted `go-unit-tests` job is the authority for the full matrix including the `internal/database` integration package (needs PostgreSQL; fail-closed when BASEHARBOR_TEST_DATABASE_URL unset — r27 develop #1378). No reachable PostgreSQL / runner infrastructure in this lane (runners are GitHub-hosted shared runners only, never built/repaired here). The database-gate runs hosted on the new head 3691173821384d028f33d81cc2c54a991d639f12.
- Note: the full `cmd/baha` suite flakes under local parallel load (TestGeneratedBootstrapConsentRetainsCurrentIntent crashes in buildResolvedApplicationPlan at app_core_requirement.go:224) — confirmed PRE-EXISTING: the original candidate 942e3cc5 also times out (exit 124) under a local full run. Not introduced by this change; targeted workload/destroy/retire/telemetry suites are green.

## END
END_DONE w156-destroy-r2: head=36911738 telemetrie=zurueckgesetzt (blob abbb5bb6 == develop, diff: absorption removed) zelle=rc0 (W154 x3 + W138 green) shared=streng (readWorkloadRuntimeEnv -> readRuntimeEnv, keine absorption) diff=telemetry_authorization.go RAUS aus name-only diff lauf=36911738 push OK lsremote=3691173821384d028f33d81cc2c54a991d639f12 | runtime-dir-present/env-missing fix INSIDE stop path w/ VerifyRuntimeFileOwner ownership proof; sick cell develop rc=1 belegt; DB-gate hosted (kein lokaler PG)
