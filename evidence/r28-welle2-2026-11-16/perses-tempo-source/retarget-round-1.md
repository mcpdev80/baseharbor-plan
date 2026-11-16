# retarget-round-1 — PR #1645 base retarget to lane-0428-075-perses-seam

- **Card:** t-20261114-r28-perses-tempo-source (PR #1645 @ c781eb86)
- **Lane:** w091-tempo-r5-fix
- **Date:** 2026-11-16
- **Role:** Worker (self-run duty, §4.6)

## What is being built

The base-ref stacking fix for the perses/tempo-source card: PR #1645 (the Tempo datasource + witness rename) was stacked onto the contract-seam card #1575 per the precedence `0428-stack-regel`, but it was still *targeting* `develop`, so its live diff re-opened the still-unmerged seam #1575 and broke the one-PR-per-card rule. This lane retargets PR #1645's base to the contract-seam lane's head so the diff is Tempo-only, exactly matching the CODEX batch-10 recipe.

## Steps

- Create branch w091-tempo-r5-fix from exact head c781eb86 + ls-remote witness; base attestation 66ff93d1 ancestor-of-head
- Merge seam: seam 66ff93d1 already an ancestor of w091 head (git merge origin/lane-0428-075-perses-seam -> already up to date). Tempo commits only beyond seam.
- Retarget PR #1645 base to lane-0428-075-perses-seam via gh api PATCH (develop fae335a3 -> 66ff93d1); draft preserved true; head unchanged c781eb86
- go build + targeted tempo tests in worktree
- Push refspec + ls-remote witness; await terminal exact-head pull_request run; record in akte

## Base attestation (proof)

- Base SHA cut from / stacked on: `66ff93d1cfe18a81a3b2dc4bd3389655e29b9e08` (lane-0428-075-perses-seam)
- Branch head: `c781eb86fc996493bf5e0ee807913e81a51c3ab4` (mission-supplied exact head)
- `git merge-base --is-ancestor 66ff93d1 w091-tempo-r5-fix` -> **YES** (seam contained in branch)
- `git log 66ff93d1..w091-tempo-r5-fix` -> exactly the Tempo commits (c781eb86f, 5740a4d62, 601f3c3af, 7a2736ba5, 4b222b1dd, d8ffac475, c27e7a789). No foreign candidate commit carried on top.
- `git log --oneline` on the branch lists ONLY these own commits (no foreign ancestor).

## Steps executed

### (1) Branch + ls-remote witness

- Cut `w091-tempo-r5-fix` from exact head `c781eb86` in a fresh git worktree at `baseharbor/worktrees/w091-tempo-r5-fix` (base `baseharbor`, NOT the workers/ bookkeeping repo — the repo is confirmed `origin https://github.com/mcpdev80/baseharbor.git`).
- ls-remote witness before push: `git ls-remote origin w091-tempo-r5-fix` returned `c781eb86fc996493bf5e0ee807913e81a51c3ab4` (branch already existed on remote from the earlier chain push; re-push confirmed up-to-date).

### (2) Merge seam

- `git merge origin/lane-0428-075-perses-seam` -> **"Already up to date"** (the seam head `66ff93d1` is an ancestor of the branch head).
- Verified the seam is fully contained and the delta beyond it is Tempo-only (see base attestation). No conflict case; the stack rule is satisfied structurally.

### (3) PR base retarget (api PATCH; graphql disabled)

- BEFORE: `base_ref=develop`, `base_sha=fae335a3ec1ed93663e4971cbf71f157f1c07174`, `draft=true`, `head=c781eb86`.
- Command: `gh api -X PATCH repos/mcpdev80/baseharbor/pulls/1645 -f base=lane-0428-075-perses-seam`.
- AFTER: `base_ref=lane-0428-075-perses-seam`, `base_sha=66ff93d1cfe18a81a3b2dc4bd3389655e29b9e08`, `draft=true` (preserved), `head_ref=mcpdev80:w091-tempo-r5-fix`, `head_sha=c781eb86` (unchanged), `state=open`.
- `sha.base == 66ff93d1` confirmed equal to the seam head. Diff vs base: 21 files, 16879 additions, 0 deletions, mergeable=true.

### (4) go build + targeted tempo tests

- `go build ./...` -> **exit 0** (GOCACHE/TMPDIR redirected to the worktree because /tmp is at disk quota).
- Targeted perses/tempo tests `go test ./internal/metrics/ -run 'Perses|Tempo'`:
  - ALL PASS — `TestPersesReleaseIsPinnedAndCurrent`, `TestPersesTempoDatasourceNativeResourceShape`, `TestPersesTempoDatasourceValidateRejectsNonNativeResource` (all sub-cases), `TestPersesTempoDatasourceRealTraceQueryAnswers`, and every `*FailClosed` / verify-boundary assertion.
- Pre-existing, unrelated failure (NOT introduced by this change, NOT a tempo/perses file): `TestProviderFilesUsePinnedPrometheusAndHardenedSharedNetwork` (prometheus_test.go, docker-compose provider-file test). Failure is `http: TLS handshake error ... remote error: tls: bad certificate` from the shared docker daemon — an environment issue, not the Tempo delta. This is a STATE finding, not a scope/blocker.

### (5) Push + CI witness

- Push up-to-date; ls-remote witness: `c781eb86fc996493bf5e0ee807913e81a51c3ab4 refs/heads/w091-tempo-r5-fix`.
- CI run on head c781eb86 after retarget: **run 43876671426, status=completed, conclusion=success** (created 2026-11-16T13:32:03Z). Jobs: PR · Draft source and routing SUCCESS, PR · Draft Go · packages/cli-0..3 all SUCCESS; remaining gates skipped (draft PR). 0 failed.
- Prior run 43874313785 (also head c781eb86) SUCCESS (26 success / 13 skipped / 0 failed) — the exact-head `pull_request` run CODEX batch-10 required.

## repo-rule compliance

- No .github/** edits, no merge, no ready_for_review, no force-push, no retarget of other PRs, no subagents.
- Branch cut from mission-supplied exact head c781eb86; seam 66ff93d1 is an ancestor (stacking base rule).
- Evidence committed only to baseharbor-plan (origin/main), never in the product repo.
- No product code changed this round — base retarget + CI/test evidence only.

## END

- status: DONE
- candidate SHA: c781eb86fc996493bf5e0ee807913e81a51c3ab4
- lane: w091-tempo-r5-fix
