# w74-basemerge-two — BASEMERGE 2x (mechanical, no content)

**Role:** Worker, Lane w74. **Coord:** f49a3303 (Qwen Flash).
**Mission:** Owner merged #1359 (CI-runtime-routing-fix) onto develop at `747aed4a`. Pull that base into BOTH work branches, one after the other, run the mandated local gates, push, and watch each PR's Selected-Checks gate to terminal green.

**Target base:** `origin/develop` = `747aed4a` (Merge PR #1359). #1359 touches only CI files: `.github/workflows/ci.yml`, `.github/workflows/pre-release-runtime-suite.yml`, `scripts/test_pr_runtime_workflow_shape.py` (75 insertions / 31 deletions).

## PLAN

1. Recon: confirm base commit and map conflict risk — DONE (both branches DELETE the CI-file lines #1359 adds; direct hunk overlap → expected conflict).
2. **A) access branch** `work/r27-ci-access-ab` (head `2819c522`): worktree add `/tmp/opencode/w74-bm-access-wt`; `git merge origin/develop`; resolve conflicts; `go build ./...` + `go test ./internal/runtimeexecutor -count=1` green; push; `ls-remote == head`; watch PR Selected-Checks gate terminal green.
3. **B) journal branch** `work/r27-ci-authority-ab` (head `f42be63f`): worktree add `/tmp/opencode/w74-bm-journal-wt`; `git merge origin/develop`; resolve conflicts; `go build ./...` + `go test ./internal/machinehttp -count=1 -timeout 8m` green; push; `ls-remote == head`; watch PR Selected-Checks gate terminal green.
4. Write this evidence with both SHAs, run-ids, both gate results; END an f49a3303.

## repo-rule compliance
- Mechanical merge only; no product content changes. Conflicts resolved by KEEPING each branch's own CI-file edits (delete the #1359 test invocation / revert its restructure where the branch deliberately removed it) — i.e. restore branch intent on the overlapping hunks. No scope creep.
- PRs not touched except observing their checks.

## Evidence log

### A) access
- worktree: `/tmp/opencode/w74-bm-access-wt`
- pre-merge branch head: `2819c522`
- post-merge SHA (access, local):
- post-merge SHA (access, remote/ls-remote):
- push run-id:
- ls-remote==head:
- go build ./...:
- go test ./internal/runtimeexecutor -count=1:
- PR Selected-Checks gate (access): terminal green|rot — run-id:

### B) journal
- worktree: `/tmp/opencode/w74-bm-journal-wt`
- pre-merge branch head: `f42be63f`
- post-merge SHA (journal, local):
- post-merge SHA (journal, remote/ls-remote):
- push run-id:
- ls-remote==head:
- go build ./...:
- go test ./internal/machinehttp -count=1 -timeout 8m:
- PR Selected-Checks gate (journal): terminal green|rot — run-id:

## END
END_DONE w74-basemerge-two: access=<sha> journal=<sha> gate=gruen(2x)|rot(auszug) | <Satz>
