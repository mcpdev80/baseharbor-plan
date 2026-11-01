# p1241 Evidence — PR #1241 engine detection through the CI chain

- Lane: p1241 (.models/ornith)
- Task tag: p1241
- Mission: `coordinator/missions/p1241.txt`

## PLAN

- Read mission p1241; inspect PR #1241, fix commit ed5ca739, base cb6b7387 vs develop TIPP 5c903560
- Verify fix commit rebases cleanly onto origin/develop TIPP (5c903560); no divergence in cmd/baha/docker_engine.go
- Create p1241 worktree from origin/work/fix-engine-detect, rebase onto origin/develop -> 5664175c
- Force-push rebase onto own lane branch per mission (normal push after rebase ok); PR head updated to 5664175c
- Monitor PR #1241 Selected Checks until terminal; only cmd/baha/* touchable
- CI run 41338807540 = SUCCESS (all gates incl. PR Selected Checks)
- CODEX-REVIEW candidate vs contract -> APPROVE
- Write this evidence; post END_DONE/END_BLOCKED

## Work

### Rebase (mission step 1)
- Fixed head was `ed5ca739`, based on `cb6b7387` (intermediate receipt commit, NOT the develop tip).
- Mission requires rebase onto the origin/develop TIPP (`5c903560`), not the event base.
- `git rebase origin/develop` applied cleanly (1 commit, no conflict; `cmd/baha/docker_engine.go` unchanged between base and tip).
- New head: `5664175c`.
- Diff vs develop tip = exactly 2 files, both in `cmd/baha/*`:
  - `cmd/baha/docker_engine.go` (+18/-3): `engineBinaryName(provider)` selects `"podman"` for podman, `"docker"` otherwise; `inspectTargetDockerEngine` now passes `engineBinaryName(target.RuntimeProvider)`; `ensureTargetDockerBinding` accepts both docker and podman.
  - `cmd/baha/docker_engine_podman_test.go` (+19): `TestEngineBinaryNameSelectsPodmanForPodmanProvider` covers `""→"docker"`, `"docker"→"docker"`, `"podman"→"podman"`, `"unknown"→"docker"`.
- Pushed (force) onto `work/fix-engine-detect` per own-lane-branch rule. PR #1241 head = `5664175c`.

### CI observation (mission step 2) — Eigenes-Run-Pflicht (4.6)
- CI run `41338807540` (triggered via pull_request on work/fix-engine-detect), terminal result: **SUCCESS**.
- Gates: Trusted Plan ✓, Workflow policy ✓, Runner Interface ✓, Focused Python ✓, Exact Candidate ✓, cli-build ✓, source-contracts ✓, cli-vet ✓, cli-guided-tests ✓, Selected Runtime (podman + docker lifecycle) ✓.
- **PR Selected Checks: SUCCESS** — the gate that FAILED on the previous head `ed5ca739` now passes, because the runtime-qualification checks are no longer skipped on the develop-TIPP base.
- No red runs; no code fix needed.

### CODEX-REVIEW (pre-merge gate)
- Verdict: **APPROVE** (SHA-genauer, read-only gh API).
- head `5664175c` on `work/fix-engine-detect` vs `develop`; compare `5c903560...5664175c` = 1 ahead / 0 behind, exactly 2 files both `cmd/baha/*`.
- STOP criterion clean: no `.github/workflows/*`, no `scripts/ci-*` touched.

## repo-rule compliance
- Write-set confined to `cmd/baha/docker_engine.go` + `cmd/baha/docker_engine_podman_test.go` (mission scope).
- No `.github/workflows/*` or `scripts/ci-*` changes.
- No product rework beyond the rebased fix commit.

## HANDOFF
- Status: review. Candidate `5664175c` is code-ready and passes the full Selected Checks chain.
- CODEX-REVIEW APPROVE. Merge is a separate CODEX-MERGE authorization (not performed by this worker).

## p1241 END
END_DONE p1241: head=5664175c runs=41338807540 | PR #1241 green on develop-TIPP base, CODEX-REVIEW APPROVE
