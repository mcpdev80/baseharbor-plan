# dr3 evidence — cmd/baha hosted `validate` silent drop

**Mission:** `cmd/baha` falls off in GH-hosted `validate` runs after ~4 min with no own error line (runs: 41377744199-Job validate 242s; observability 291s STILL-FAIL; Targeted 163s before #1265 fixes). The same families are GREEN in Selected-Runtime (Lifecycle) runs. Find the silent failure candidate + fix, or a documented END_BLOCKED (file:line).

**Task ID:** dr3 | **Branch:** dr3 (worktree) | **Base:** origin/develop @ 52d999b8 (>= aef6b0e1 ✓)
**Session:** 35cdb02e-a3b3-4e6d-86f9-1cbb35822587 | **Model:** worker-ornith1.5

## PLAN
1. Set up isolated dr3 worktree from origin/develop and read task + repo rules
2. Map the disaster-recovery validate test family (`=== RUN` vs `--- PASS/SKIP`) and its runtime prerequisites
3. Diagnose the silent-failure candidate: validate vs Selected-Runtime context (pg port, XDG, rootless, pkg timeout)
4. Apply minimal hardening in cmd/baha test setup OR deliver a file:line-bounded finding
5. Prove with `go test ./cmd/baha -run AppBackupRestore` before/after (local, isolated runtime)

## repo-rule compliance
- Worktree isolated from develop; no `.github/workflows/*`, no `scripts/pr-*` touched (STOP).
- No subagent/codeman spawn. No interactive question dialog (QUESTION line used instead).
- Changes scoped to `cmd/baha` test setup only, if a fix is delivered.

## Evidence log
- (log run IDs, SHAs, gate results as they happen)

## Status
END_BLOCKED dr3: <candidate name> | pr=<nr|none> | stelle=<file:line>
