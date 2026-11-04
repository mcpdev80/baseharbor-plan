# isolation-1: w78-seam-isolation — isolate 11 shared-state hosted fails (r27-state-owner)

- Task: `t-20261018-r27-state-owner` (validierungs-restarbeit)
- Worker lane: `w78-seam-isolation` · Coordinator: `f49a3303`
- Repo: `baseharbor` (product) · Branch: `work/r27-state-owner`
- Head: `f3ea54e2…`
- PR: #1347
- Isolated worktree: `/tmp/opencode/w78-stateowner-wt`
- Evidence: `baseharbor-plan/evidence/r27-welle3-2026-11-03/state-owner/isolation-1.md`

## PLAN (board + JSON live board in sync)

1. ✅ Read mission w78; reality-check: `git fetch origin` refs, `worktree add /tmp/opencode/w78-stateowner-wt work/r27-state-owner`, verify heads (`f3ea54e2` / `2cadfcee`).
2. ⏳ Establish baseline: `go build ./...` + `go test` the 4 packages green on develop; reproduce the 11 fails red on the branch under shared HOME (TMPDIR announcement).
3. ⏳ Categorize 11 cases (shared-state vs true regression); isolate each via `t.Setenv HOME/XDG_DATA_HOME/XDG_CONFIG_HOME -> t.TempDir()` (PR #1351 pattern), no prod code, no test deleted, no skip.
4. ⏳ Verify each of 11 cases red-then-green locally.
5. ⏳ `go build ./...` green; `go test ./internal/telemetry ./internal/externalprovider ./cmd/baha ./internal/providers/runtime/podman -count=1` green (GOCACHE=/tmp/opencode TMPDIR=/tmp); `gofmt -l` empty.
6. ⏳ Push FF ancestry rc=0; ls-remote==head + cat-file -e.
7. ⏳ Watch PR #1347 checks terminal — validation green; lifecycle/backup-restore may stay red (infra-ref).
8. ⏳ Write evidence, update todos board, post END_DONE.

## TASK / CONTRACT

Isolate 11 shared-state/hosted test fails on `work/r27-state-owner` following the proven
pattern from PR #1351 (`t.Setenv HOME/XDG_DATA_HOME/XDG_CONFIG_HOME -> t.TempDir()`), turning
each case **red-first** (shared HOME forced via TMPDIR announcement) then **green** (env-independent).
Rules: NO production code, NO test deleted, NO skip. The three fail-closed documentation cases
(app-edit ADR-0022) stay UNTOUCHED. STOP if a case stays red even when isolated.

## END
END_BLOCKED w78-seam-isolation: <sha> | <one line + candidate SHA>
