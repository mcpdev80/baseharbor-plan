# isolation-1: w78-seam-isolation — isolate 11 shared-state hosted fails (r27-state-owner)

- Task: `t-20261018-r27-state-owner` (validierungs-restarbeit)
- Worker lane: `w78-seam-isolation` · Coordinator: `f49a3303`
- Repo: `baseharbor` (product) · Branch: `work/r27-state-owner`
- Head: `f3ea54e2…`
- PR: #1347 · hosted run `41726952160`
- Isolated worktree: `/tmp/opencode/w78-stateowner-wt`
- Evidence: `baseharbor-plan/evidence/r27-welle3-2026-11-03/state-owner/isolation-1.md`

## PLAN (board + JSON live board in sync)

1. ✅ Read mission w78; reality-check: `git fetch origin` refs, `worktree add /tmp/opencode/w78-stateowner-wt work/r27-state-owner`, verify heads (`f3ea54e2` / `2cadfcee`).
2. ✅ Hosted run is the standard (coord decision 2026-11-04): PR #1354 go-unit-tests TERMINAL GRUEN on same runner pool. Pull exact FAIL lines from run 41726952160 via `gh api …/jobs --jq` + `gh api …/jobs/<id>/logs | grep FAIL`.
3. ✅ Reproduce red-first on EXACTLY those hosted lines; establish per-case baseline (develop vs branch).
4. ⏳ Isolate each case red-then-green: recovery(5)=HOME/XDG isolation; tmp/parent-mode via `t.Setenv TMPDIR -> t.TempDir()` (0700 by def); telemetry/podman env-expectation (PATH/XDG_RUNTIME_DIR) isolation — NOT privileges.
5. ⏳ `go build ./...` green; `go test ./internal/telemetry ./internal/externalprovider ./cmd/baha ./internal/providers/runtime/podman -count=1` green; `gofmt -l` empty.
6. ⏳ Push FF ancestry rc=0; ls-remote==head + cat-file -e.
7. ⏳ Watch PR #1347 checks terminal — validation green; lifecycle/backup-restore may stay red (infra-ref).
8. ⏳ scope-extension (owner-guard vs demo-state order in acceptance path) BEFORE END.
9. ⏳ Write evidence, update todos board, post END_DONE.

## TASK / CONTRACT

Isolate 11 shared-state/hosted test fails on `work/r27-state-owner` following the proven
pattern from PR #1351 (`t.Setenv HOME/XDG_DATA_HOME/XDG_CONFIG_HOME -> t.TempDir()`), turning
each case **red-first** (reproducible) then **green** (env-independent).
Rules: NO production code, NO test deleted, NO skip. The three fail-closed documentation cases
(app-edit ADR-0022) stay UNTOUCHED. Scope-extension (acceptance-path Core owner before first
state-save) is MANDATORY before END. STOP (per-case, with hosted line) only if a case stays
hosted-red with NO prior green — and after dating the interaction (parallelism/order/shared state).

## END
END_BLOCKED w78-seam-isolation: <sha> | <one line + candidate SHA>
