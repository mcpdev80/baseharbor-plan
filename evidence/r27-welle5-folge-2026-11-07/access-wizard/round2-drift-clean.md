# 0427-access-wizard — round 2 evidence (drift cleanup + write-set purge)

Card: `t-20261018-r27-access-wizard`. Worker lane `0427-access-wizard`.
Owner directive (mission `0427-access-wizard-r2.txt`, 2026-11-07): candidate
`42607ca40` was delivered but **not abnahmereif** — drift + write-set collision.

## (a) Drift: rebase onto develop
- Fetch: `origin/develop` = `812c99c88` (`#1383 work/r27-compose-isolation`).
- `git rebase origin/develop` on branch `work/r27-access-wizard` → clean, no conflicts.
- New HEAD: **`3a699a2876c4d0349021b6222958d9a2f74b09dc`**
- Ancestry: `git merge-base --is-ancestor 812c99c88 HEAD` → **YES** (develop is an ancestor).
- One coherent commit, message: `feat(cli): add guided access assign/offboard wizard (r27 access-wizard)`.

## (b) Write-set collision — PURGED correctly
Mission warned the wizard diff touches the 3 lifecycle/fixture files owned by
`#110`/`#1383` (lane `3a4d5d33`). **Verified by diff:** the committed diff touches
**NONE** of `cmd/baha/app_repository_integration_test.go`,
`cmd/baha/app_workload_integration_test.go`, `cmd/baha/repository_runtime_fixture_test.go`.
The wizard needs no lifecycle/fixture files → no STOP + QUESTION required; the
write-set stayed inside the bounded set. The old `42607ca40` and the rebased
`3a699a287` both diff only these 6 files:
- `cmd/baha/access_wizard_command.go` (new)
- `cmd/baha/commands.go` (+1, wire `accessWizardCommand` into root tree)
- `internal/accesswizard/{wizard,authority,controller}.go` (new)
- `internal/accesswizard/wizard_test.go` (new, 15 tests)

## (c) Push (no PR — laptop cannot open one)
- `git push --force-with-lease lane-origin work/r27-access-wizard` → remote tip now `3a699a287`.
- Remote was holding only the stale pre-rebase tip `42607ca40` (my own commit on old develop);
  no divergent collaborator work on this ref. Force-with-lease safe.
- Proof: `git ls-remote lane-origin work/r27-access-wizard` → `3a699a2876c4d0349021b6222958d9a2f74b09dc`.
- **Coordinator opens the PR mechanically** (Owner scope; `.github/**` is not a worker write-set).

## (d) CI coverage (Aufnahmepflicht §5.3)
- `internal/accesswizard/*_test.go` runs under the required **"Release source tests"** job,
  `.github/workflows/ci.yml:121` → `go test ./contracts/... ./internal/... ./spec/...`.
- `cmd/baha` adapter compilation covered by the same job, line 122 → `go test ./cmd/baha`.
- **No `.github` trigger change is needed.** Existing required group already runs both the
  wizard package tests and the CLI adapter. No finding, no edit to owner scope.

## Local verification on drift-free candidate `3a699a287`
- `go build ./...` → pass
- `go vet ./...` → pass
- `gofmt -l` on my files → clean
- `go test ./internal/accesswizard/` → **15/15 PASS**
- doc-audit + source-readability-audit → pass (already green from round 1)

## Bugs fixed (round 1, documented)
1. `readLine` built a fresh `bufio.Reader` per call → dropped following-line bytes,
   corrupting piped/non-interactive wizard flow. Shared buffered reader now.
   Protected by `TestMultiLineInputIsNotCorrupted`.
2. EOF at the name prompt surfaced as a bare EOF instead of `ErrIncompleteConfig`;
   now fails closed uniformly.

## Next
Independent **CODEX-REVIEW** verdict against the task contract (candidate `3a699a287`),
then CODEX-MERGE if it passes. No subagents. END to 594fd2f5 after handoff.
