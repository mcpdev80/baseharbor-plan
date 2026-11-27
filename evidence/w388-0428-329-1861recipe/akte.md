# Akte w388-0428-329-1861recipe — card 0428-329 / PR #1861 — local fan-in conflict-resolution recipe

**Lane:** w388-0428-329-1861recipe  **Repo:** baseharbor (product, read-only)  **PR:** #1861
**ART:** LOCAL recipe only. No push, no run, no merge, no PR-head change, no product/config commit. Worktree reset after every inspection.
**PUBLISHING:** plan-repo write freeze 2026-11-27T07:34:31Z (Coordinator-Hinweis): this akte is delivered as a FILE in my working tree only — no plan PR, no main push. Path + sha256 at END.

## PLAN

1. Witness PR #1861 via `gh pr view` (headRefOid, refs, state, mergeable) — DONE.
2. Create own worktree `workers/worktrees/w388-0428-329-1861recipe` from the PR branch; foreign worktrees untouched — DONE.
3. `git fetch origin develop`; `git merge origin/develop` ONLY locally; inspect; `git merge --abort` — DONE: merge is a clean NO-OP ("Already up to date"), zero conflicts, nothing to abort.
4. Per-region recipe for cmd/baha/core.go:71 and cmd/baha/main.go:610 with test file:line — DONE as a premise finding: neither region exists on the live refs (evidence below); the only merge with real conflicts (develop vs main) is catalogued with the semantic resolution rule.
5. Publish akte per freeze: file in worktree, path + sha256 in END — DONE.
6. Clean up probes, END post — DONE.

## 4-Feld

- Lane: w388-0428-329-1861recipe
- Karte: 0428-329 (tasks/t-20261126-hunt46-recovery-backup-volume-heuristic.md, kanban_status blocked; card frontmatter owner: `"" (unassigned — blocked-BASELINE as STATE: family catalog PR #1861 open, develop row pending freeze-lift per w267 7199390854)`; mission line 1 says `LANE: w388-0428-329-1861recipe` — that is my canonical lane name)
- Repo/PR: mcpdev80/baseharbor #1861, head `ade7dab3cf06658efd9a172ce3a674b887bd3c79`, base develop `ea5218d72e263f21e79853b679af50074dab8c25`
- Status: END_DONE (local recipe delivered; no push, no merge, no PR change)

## Commit identity block (visible, before any commit — none created; lane is no-push by mission)

- Exact per-card frontmatter owner VERBATIM (fetched from origin/main at runtime): `owner: ""` (full line quoted in 4-Feld above; card has no "(lane X)" value — mission line 1 names this lane).
- git identity I would use: `user.name=w388-0428-329-1861recipe`, `user.email=w388-0428-329-1861recipe@baseharbor.local`.
- Literal invocation form: `git -c user.name=w388-0428-329-1861recipe -c user.email=w388-0428-329-1861recipe@baseharbor.local commit ...`
- Pre-push gate line: `git show -s --format=%an HEAD` must equal `w388-0428-329-1861recipe` exactly. NOT exercised: the mission forbids any push and I created no commit (worktrees reset after every merge probe; `git status` clean at END).

## Wrong-zone check (planning repo identity)

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` (before any plan action):

```text
baseharbor      https://github.com/mcpdev80/baseharbor.git (fetch) [blob:none]
baseharbor      https://github.com/mcpdev80/baseharbor.git (push)
origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin  https://github.com/mcpdev80/baseharbor-plan.git (push)
upstream2       https://github.com/mcpdev80/baseharbor-plan.git (fetch)
upstream2       https://github.com/mcpdev80/baseharbor-plan.git (push)
```

Confirmed correct planning repo. NOTE: per the plan-repo write freeze this lane performed NO plan write; an isolated plan worktree `workers/w388-0428-329-1861recipe-plan` was created at origin/main then removed unused (`git worktree remove` completed, no commit, no push).

## (a) PR witness

`gh pr view 1861 --repo mcpdev80/baseharbor --json headRefOid,headRefName,baseRefName,state,mergeable`:

```json
{"baseRefName":"develop","headRefName":"w334-0428-329-recoveryheuristic","headRefOid":"ade7dab3cf06658efd9a172ce3a674b887bd3c79","mergeable":"MERGEABLE","state":"OPEN"}
```

`mergeStateStatus: BLOCKED` (catalog baseline, not a git conflict). ls-remote witnesses (real GitHub URL):

```text
ea5218d72e263f21e79853b679af50074dab8c25  refs/heads/develop
ade7dab3cf06658efd9a172ce3a674b887bd3c79  refs/heads/w334-0428-329-recoveryheuristic
ade7dab3cf06658efd9a172ce3a674b887bd3c79  refs/pull/1861/head
c3b78af7e5f1733a396f603f12da50bec5fa5bda  refs/pull/1861/merge
```

REMOTE GUARD: in the product checkout `/home/marcel/dev/baseharbor-ecosystem/baseharbor`, both `origin` and `lane-origin` resolve to `https://github.com/mcpdev80/baseharbor.git` (verified with `git remote -v` as first git action); all fetch/ls-remote/merge operations used only github.com/mcpdev80 URLs.

## (b) Worktree

`workers/worktrees/w388-0428-329-1861recipe`, created via `git worktree add ... ade7dab3c` (detached at the PR branch head) from the product checkout. Foreign worktrees (incl. `w377-0428-329-1861pre-1861pre`) untouched, not reused, not deleted.

## (c) Local `git merge origin/develop` — result: NO conflict, merge is a NO-OP

In the worktree at `ade7dab3c`: `git merge --no-ff --no-commit origin/develop` => `Already up to date.` (exit 0). Proof: `ea5218d72` is the DIRECT parent of `ade7dab3c` (`git log -1 --format='%h %p' ade7dab3c` => `ade7dab3c ea5218d72`; `git merge-base ade7dab3c origin/develop` => `ea5218d72`), and `git log --oneline origin/develop..ade7dab3c` lists ONLY `ade7dab3c` (own candidate commit). There was nothing to abort; no solution commit, no push; worktree left clean at `ade7dab3c` (`git status --short` = 0 lines).

## (d) Per-region recipe — PREMISE FINDING FIRST

### d.0 The two named regions do not exist on any live ref (w377 conflict report NOT reproducible)

The mission (after w377) names conflicts at `cmd/baha/core.go:71` and `cmd/baha/main.go:610` for the hop of head `ade7dab3c` against develop `ea5218d72`. Measured reality at head `ade7dab3c` and develop `ea5218d72` (own ls-remote above):

- `cmd/baha/core.go` does not exist: `git cat-file -e ade7dab3c:cmd/baha/core.go` and `... ea5218d72:cmd/baha/core.go` both fail. The file exists in NO reachable ref of this ecosystem — checked: develop, main (`cddc81b34`), every release tag through v0.4.27 (main.go only grows 56→349 lines, never a core.go), all 1493 `refs/pull/*/head`, all remote branches, all refs and dangling commits in both repos' object stores. GitHub commit search for path `cmd/baha/core.go` returns zero commits ever.
- `cmd/baha/main.go` is only 376 lines on develop and on the PR head (`git show <ref>:cmd/baha/main.go | wc -l` => 376/376) — line 610 does not exist; line 71 of main.go is inside `interruptibleProcessContext` (signal context helper), not a "help-Funktionszuordnung".
- The develop merge of the head is a no-op (section c), so there are no conflict regions at all on that pair.
- Cross-fan-in probes (merge of the PR head with each current sibling candidate, `--no-commit`, aborted): `#1812 c2dd3ff04`, `#1860 057ce8c55`, `#1862 5c20c2e32`, `#1863 0eafa9f5a`, `#1864 b9675cc0b/0abc27596`, `#1866 3702c0950`, `#1868 57320af69`, `#1869 467913b72`, `#1855 d18e4b367`, develop-merge-commit `c3b78af7e`, plan #136 heads `c4e440017`/`bcc30d999` => ALL "Already up to date" or "Automatic merge went well", ZERO unmerged paths, in every combination tried against both `ea5218d72` and `ade7dab3c`.
- The only ref pair in the product repo that produces real content conflicts is `origin/develop` vs `origin/main` (`cddc81b34`): 145 unmerged paths — one of them `cmd/baha/main.go` (conflict marker present, region ~line 71), NONE named `cmd/baha/core.go` (it never exists). The released-v0.4.27 main tree is the realistic source of a "core.go"-style help/runtime divergence claim; w377's cited line numbers match no measured file.

Disposition of the w377 report: the two named conflict regions are NOT on the live chain to fan in; the #1861 fan-in of develop is conflict-free BY ANCESTRY. This finding supersedes the recipe premise; the recipes below are given for the two real conflict classes so the integration hop can apply them verbatim.

### d.1 Region A — "help-Funktionszuordnung" (develop vs released-main lineage)

- Which side wins: BOTH — the develop-side function map wins as the file form, and the main-side help mapping is preserved only if it is a real behavior delta. Measured: on develop and on the PR head there is no second help-mapping site (help normalization lives in `cmd/baha/human_workspace.go:22` `normalizeWorkspaceHelp`, recursive at `:25`; usage-error help strings at `cmd/baha/commands.go:275` and `:286`). A conflict here can only come from the v0.4.27-main help mapping being reintroduced.
- Why (product behavior): develop's `cmd/baha/main.go:31-71` (`main` + `interruptibleProcessContext`) owns exit routing (Ctrl-C/SIGTERM → 130, JSON error envelope via `classifyMachineCLIError`/`cli.ExitCode`, lines 60-71 and 615-625 region of the tail). Help-function assignment must not bypass that: the help command mapping is display-only and must keep routing through the single `runWithIO` entry (`main.go:129`).
- How both behaviors survive: take develop's assignment table; if the main side adds a command→help pairing that develop lacks, add the pair to develop's table WITHOUT touching the exit-routing body. That is exactly the "build-time vs runtime" yardstick the mission names: build-time/version wiring (`defaultRuntimeImage(buildVersion)`, `main.go:117`) stays on the build-time side; runtime process wiring (signals, exit codes, grant scopes) stays runtime-side. Never merge a hunk that moves runtime behavior into the build-time table or vice versa.
- Proving tests (file:line on the fan-in result):
  - `cmd/baha/main_version_test.go` (exists on develop and head; version/help wiring of `main`).
  - `cmd/baha/agents_root_help_test.go` and `cmd/baha/help_newline_regression_test.go` (help mapping/normalization).
  - `cmd/baha/machine_coverage.go` contract tests (classifyMachineCLIError) and the main-level contract entry `33754a9a0 fix(0428-321): drive signal->exit mapping through main-level contract entry` (sibling of #1866; its tests live in #1866's diff against `cmd/baha/main.go`).
  - CI route: `go test ./cmd/baha/` in the PR Go-unit job, package-discovered (`go list ./...` doctrine; use named `-run` form with the RunsRealLifecycle skip per the test-runner rule when running anywhere manually).

### d.2 Region B — "runtime-flags" (`cmd/baha/main.go`, develop vs released-main)

- Which side wins: develop's flag set, extended additively; the main-side flag definitions survive only as the same flags already present at their develop locations.
- Why (product behavior): develop `cmd/baha/main.go:184` `extractGlobalOutputOptions` + `cliLocalWorkloadOperation` (`:158`) are the single global-flag/parser seam; the local-workload grant-scope comments at `:163`/`:168` tie flag parsing to the authorization path ("must receive the same local-runtime scope"). Losing either side changes consent behavior; a duplicated flag registration panics at startup.
- How both behaviors survive: keep both flag lists, deduplicate by flag name, and preserve develop's global-vs-per-command split (global output flags extracted in `main.go`, command flags declared in `commands.go`/`app_*.go`). Any new runtime flag goes into the develop-side parser entry, never into the build-time table of d.1.
- Proving tests (file:line on the candidate pair under this card):
  - `internal/runtime/repository_volume_inventory_test.go:64` `TestRepositoryVolumeInventoryRecoveryBackupFullDestroy` with `t.Run("docker")`/`t.Run("podman")` subtests at `:66` (engine selection = the runtime flag semantics for this change).
  - `cmd/baha/app_destroy_volumes_recovery_backup_test.go:53` `TestDestroyRepositoryDataVolumesRecoveryBackupAuthoritativeOwnership`, engine subtests at `:55`, destroy-plan assertions at `:96`/`:108`/`:118`/`:121` (real rendering path `cmd/baha/app_destroy_volumes.go:41 renderRepositoryDestroyVolumes`).
  - `cmd/baha/main_test.go` (global flag/parse behavior).
  - CI route: `go test ./cmd/baha/ -run TestDestroyRepositoryDataVolumesRecoveryBackupAuthoritativeOwnership` (named form, skip `RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication`) and `go test ./internal/runtime/ -run TestRepositoryVolumeInventoryRecoveryBackupFullDestroy`, both in the PR Go-unit job.
- Fan-in note: #1861 does NOT touch `cmd/baha/main.go` at all (`git diff ea5218d72..ade7dab3c --name-only` => exactly `cmd/baha/app_destroy_volumes_recovery_backup_test.go`, `internal/runtime/repository_volume_inventory.go`, `internal/runtime/repository_volume_inventory_test.go`). Region B can never block THIS card's hop.

## What actually blocks #1861 (STATE, not a git conflict)

Per w377's akte and the #136/w387 catalog-row demand (plan evidence, cross-checked here): the Trusted Plan gate fails on three uncataloged sources (`cmd/baha/app_destroy_volumes_recovery_backup_test.go`, `internal/runtime/repository_volume_inventory.go`, `internal/runtime/repository_volume_inventory_test.go`) — the develop baseline rows land via the 0428-359 family catalog-only product PR (w387 Group A #2/#3/#4; `scripts/pr-gate-coverage.json` insert point after develop `:2718`, each with docker+podman `data.capabilities` surfaces and `runtime_specific: true`). That is Owner/baseline routing; this lane makes no such edit.

## cleanliness

- No docker/podman/compose project started (read-only lane). `docker ps -a` not applicable; my shell pid recorded in session.
- No build, no test, no local run executed (pre-checks n/a: zero commits).
- Every probe merge aborted/reset; worktree final state: detached `ade7dab3c`, `git status --short` empty. Auxiliary probe branches in the worktree deleted; the shared main checkout's temporary `lane-w388/probe` branch was deleted after its state was restored (`git status` there shows only pre-existing untracked items `baha`, `workers/`).
- Removed: `workers/w388-0428-329-1861recipe-plan` (unused plan worktree, no commits).

## END

`END_DONE w388-0428-329-1861recipe` — local recipe complete; no push, no merge, no PR-head change. The two mission-named conflict regions are not reproducible on live refs (finding in d.0); the develop fan-in of #1861 is conflict-free by ancestry; recipes for the real develop-vs-main conflict classes are in d.1/d.2 with test file:line. Candidate SHA witnessed (unchanged): `ade7dab3cf06658efd9a172ce3a674b887bd3c79`.
