# PR-SWEEP #1614 — HOP-WELLE onto develop e8acf740 (card 0428-062)

Lane: w076-0428-076-1789rest (first free seat), mission /tmp/opencode/m_1614.md.g.
Branch `lane-0428-062-cli2-app-status`, worktree
`/home/marcel/dev/baseharbor-ecosystem/workers/sweep-1614-hop-wt` (new worktree created under
workers/, the branch had no live checkout; the old `ci-reds-fix-062-wt` holds the
-fix branch and was not extended). PR #1614 is DRAFT.

## PLAN

1. Resolve remotes; locate #1614 branch; ls-remote attestation of develop and refs/pull/1614/head.
2. `git fetch origin develop`; `git merge --no-ff origin/develop` (no force; union on the app_* cli2 family where base is consolidated).
3. Check: catalog byte-identical to develop; uid lanes merged (content in base); `.github` untouched; ancestry + log-line proof.
4. Push + ls-remote refs/pull/1614/head witness; no merge.
5. Watch exact hosted CI run to terminal; record head + run-id + gates.
6. Evidence to plan origin/main with ls-tree witness; END post.

## Remote resolution (REMOTE GUARD)

`git remote -v` in the worktree (first git action):

```
origin	https://github.com/mcpdev80/baseharbor.git (fetch)
origin	https://github.com/mcpdev80/baseharbor.git (push)
```

## BASE ATTESTATION

Pre-merge `git ls-remote origin refs/heads/develop refs/heads/lane-0428-062-cli2-app-status refs/pull/1614/head`:

```
e8acf740553f7218b259f4855f5b79f83f21ab6b	refs/heads/develop
80d4df52e913e4472334a5f257fe868d26d5976e	refs/heads/lane-0428-062-cli2-app-status
80d4df52e913e4472334a5f257fe868d26d5976e	refs/pull/1614/head
```

merge-base before hop: ae0602e02882619dea151dc82d62b98b72481566.
Develop advanced mid-hop to 1b7598ae (#1787 squash); my merge cut e8acf74055 as the mission named.
`git merge-base --is-ancestor origin/develop(1b7598ae) HEAD` after fetch: ae0602e0 remains
merge-base, e8acf740 is an ancestor of HEAD via the merge commit.

## uid-lane / catalog check (mission step 2)

- Branch heads `lane-0428-uid-app`, `lane-0428-uid-environment`, `lane-0428-uid-target` no longer exist on origin (squash-merged: #1578 uid-environment, #1579 0428-050 uid-app, #1591 env-registry, #1595 0428-059 all in develop history) → PR-new catalog rows replaced by base rows.
- `git diff e8acf740 HEAD -- scripts/pr-gate-coverage.json` → EMPTY (byte-identical, `git diff --quiet` exit 0). Also EMPTY vs current develop tip 1b7598ae.
- Trusted-base rows present: `cmd/baha/app_access.go` (json line 217), `cmd/baha/app_access_test.go` (line 225) → TP expectation satisfied (rows admitted in base).
- `.github/**` untouched: `git diff origin/develop HEAD --name-only -- .github/` → 0 files.

## Conflict list and resolution (all union; git content only)

| File | Kind | Resolution |
| --- | --- | --- |
| cmd/baha/app_status_result.go | content | union: develop Perses/dashboard fields + witness setters, our Versions/VersionWarnings in both setter paths (early remote-target return now also calls collectAppStatusVersions) |
| cmd/baha/app_workspace_source_model.go | content | take develop (per-operation authorizeWorkspaceSourceModel incl. workspace.map/init on path command; strictly supersedes HEAD central workspace.show) |
| cmd/baha/app_workspace_source_model_test.go | add/add | take develop (context-aware helpers + permission tests), keep our two helpers' behavior; our-only test funcs: none (verified by func-set diff) |
| cmd/baha/machine_coverage.go | content | take develop presentation rows (HEAD adds no map-only keys; classification funcs identical both sides) |
| cmd/baha/app_version_unified_test.go (auto-merged, then broken) | call-site adaptation | switched `baha app version` invocations to runWithIOAsTestOperator like the whole base after hop — NOT a content edit; without it the merged tree fails its own tests |
| docs/cli/command-index.md, docs/de/cli/command-index.md | content | take develop; final docs commit regenerates from merged command tree (BASEHARBOR_UPDATE_MACHINE_DOCS=1, 4-line syntax union) |
| docs/{de/}reference/cli-machine-coverage.md | content | take develop; regenerated coverage == committed (machine docs tests pass) |
| internal/development/source.go | content | take develop ResolveWorkspace (mapping-root + resolveContainedWorkspaceDirectory symlink hardening; HEAD-only lexical check is the weaker subset; validateLocalSourceLocation identical both sides) |
| internal/development/source_model_test.go | add/add | union (develop symlink test + rollback tests, our tests) |
| internal/development/source_mutation.go | add/add | take develop (superset with readRollbackSnapshot/restoreFileSnapshot/saveRemovableSource; HEAD-only funcs: none) |

Final heads: merge commit `4bfc775dab3b5ef11d5b144bb063507ddf8ff509`, docs-regen commit
(candidate SHA) `3ddf61e4423d7e8f81a5e96b452984c43c323576`.

## Branch content proof

`git log --oneline origin/develop..HEAD` (candidate vs tip 1b7598ae) lists only this chain:
4bfc775d merge, 3ddf61e4 docs-regen, then the PR's own history (80d4df52, 6377f1b2, 03e28080,
818d572b, 63468454, 0963d08d, 98877cc1, eda0cd61) — no foreign candidate.
`git diff origin/develop...HEAD --name-only` → 23 files in the cmd/baha app_*/workspace +
internal/development source family + contracts/docs (the PR's own 55-file footprint intersected
with base-drift, .github excluded).

## Push + delivery witness

`git push origin HEAD:refs/heads/lane-0428-062-cli2-app-status` → `80d4df52..3ddf61e4`.
`git ls-remote origin refs/pull/1614/head refs/heads/lane-0428-062-cli2-app-status`:

```
3ddf61e4423d7e8f81a5e96b452984c43c323576	refs/heads/lane-0428-062-cli2-app-status
3ddf61e4423d7e8f81a5e96b452984c43c323576	refs/pull/1614/head
```

No merge performed by this lane. PR stays DRAFT (hop-wave, handoff already review-shaped).

## Hosted CI (Eigenes-Run-Pflicht)

- Run: `CI · Source & Quality` — run-id **45103942765**, pull_request,
  headSha `3ddf61e4423d7e8f81a5e96b452984c43c323576`,
  url https://github.com/mcpdev80/baseharbor/actions/runs/45103942765
- Watched to terminal: `completed / success` (created 03:06:05Z, updated 03:09:50Z).
- Executed gates (draft path): PR · Draft source and routing + PR · Draft Go ·
  cli-0/cli-1/cli-2/cli-3/packages — ALL success.
- Skipped by plan: Trusted Plan, Selected Checks, runtime/native/validation jobs
  (draft gate selection; they bind at ready + exact-head run, not this lane's mission).
- Advisory: PR · Candidate-added checks — skipped (none added).

## Local checks

- `bash scripts/ci-fast-check.sh` before push: exit 0 (after docs regen; 344 python tests OK).
- `go build ./...`, `go vet ./cmd/baha/ ./internal/development/` OK.
- Named-form go tests only (skip RunsRealLifecycle etc.): cmd/baha workspace/version/documentation suites OK.
- Known ambient failure (NOT from this hop): `internal/development.TestStagePinnedGitTreeExportsCommitNotDirtyWorktree`
  "native Git archive failed: signal: killed" — reproduced identically on the untouched
  1620-hop worktree (develop-based, zero union content) => coordinator-host resource limit, not candidate content.

## cleanliness

- git/docs-regen hop: no containers, compose projects, networks or volumes started.
- `docker ps -a` on this host (pid 3508606): zero containers before and after; ambient untouched.
- New worktree lives at workers/sweep-1614-hop-wt (allowed zone); /tmp/opencode/gh-1614-probe cache under /tmp only.

END_DONE w076-0428-076-1789rest: #1614 hop-wave merged develop e8acf740 with union on 11 conflict files (no content invention), candidate head 3ddf61e4423d7e8f, catalog byte-identical, .github untouched, run 45103942765 completed/success (draft path), PR kept DRAFT, no merge.
