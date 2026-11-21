# 0428-223 develop full-suite red — round 1 fix

CARD: t-20261121-develop-full-suite-red (0428-223). LANE: 0428-223-testctx.
REPO: mcpdev80/baseharbor. BRANCH: lane-0428-223-testcontext-target. PR: #1750 (draft).
MISSION: coordinator/missions/0428-223-testcontext-target.md

## PLAN

1. Read the mission and the card contract; capture remote truth (`git ls-remote`, `git remote -v`) before any git write.
2. Create the isolated worktree `workers/0428-223-testctx-wt` cut from the measured develop SHA and set the lane git identity in it.
3. Reproduce develop red remotely and cheaply: dispatch `CI . Source & Quality` on `develop`, watch to a terminal state, count the `--- FAIL:` names from the `validate` per-job log with byte counts.
4. Attribute the failure in source: read `80961866f` and the target-resolution seam (`effectiveTarget`, `selectedTargetName`, `orgconfig.LoadActiveOptional`) to find the one place all cases share.
5. Write base attestation (exact develop SHA, ancestor test, log of my commits only) into this evidence file before branching.
6. Implement the fix at the root in the test context only, using the route `80961866f` already established, with no skip, no deleted case, no weakened expectation and no enum value replacing resolution.
7. Validate focused: run the 14 cases individually with an artificial leak present, then the whole `cmd/baha` package before/after in my worktree with the named `-run`/`-skip` guard (never a bare suite).
8. Commit, push the named candidate branch, prove delivery with `git ls-remote`.
9. Open exactly ONE draft PR against develop; show the ancestry test, the changed-file list and the author list.
10. Dispatch `CI . Source & Quality` on my branch ref, watch to terminal, confirm `validate` actually ran (not skipped) and count all 14 names as PASS from the per-job log with byte counts.
11. Publish this evidence file to `origin/main` of baseharbor-plan, verify the path exists on `origin/main`, then post END.
12. Cleanliness: bring down anything my runs started, `docker ps -a` before/after, `git worktree list`, remove my scratch.

## 0. Planning zone witness (before first evidence commit)

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`:

```
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

## 1. Base attestation

Real remote (resolved by URL, not by name) — `git remote -v` in the shared baseharbor checkout showed `lane-origin`, `origin` and `upstream` all pointing at `https://github.com/mcpdev80/baseharbor.git`, so pushes used the explicit URL.

`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` at branch creation:

```
22fc68ebc0655874bc3f6aa886ff356dcad79624	refs/heads/develop
```

The branch was cut from exactly `22fc68ebc0655874bc3f6aa886ff356dcad79624` (no PR head, no foreign candidate). Ancestry of my first commit:

```
$ git merge-base --is-ancestor 22fc68ebc0655874bc3f6aa886ff356dcad79624 dd5f1faba && echo IS-ancestor
IS-ancestor
$ git log --oneline 22fc68ebc0655874bc3f6aa886ff356dcad79624..dd5f1faba
dd5f1faba test(0428-223): give target-resolving CLI cases an isolated target selection
$ git log --format='%an <%ae>' 22fc68ebc0655874bc3f6aa886ff356dcad79624..dd5f1faba | sort -u
0428-223-testctx <0428-223@baseharbor.local>
```

Candidate: `dd5f1faba` on `lane-0428-223-testcontext-target`.

`git diff 22fc68ebc...dd5f1faba --name-only`:

```
cmd/baha/app_init_source_neutral_test.go
cmd/baha/app_init_wizard_test.go
cmd/baha/app_perses_host_containers_cli_test.go
cmd/baha/app_perses_infra_dashboards_cli_test.go
cmd/baha/application_lifecycle_lock_test.go
cmd/baha/test_operator_context_test.go
```

Write-set: only `cmd/baha/*_test.go`. No `.github/**`, no `scripts/**`, no product code, none of the tabu files.

## 2. ls-remote witnesses (before / after)

Before my push (`refs/heads/lane-0428-223-testcontext-target` did not exist):

```
d1acf3f31a360cd2a5e0ebaed1c70ccdd7957cf3	refs/heads/develop
```

After my push, plus the PR head ref:

```
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-223-testcontext-target refs/pull/1750/head refs/heads/develop
dd5f1fabacded1b5cc3f2df6e9d805065f8f3f4b	refs/heads/lane-0428-223-testcontext-target
dd5f1fabacded1b5cc3f2df6e9d805065f8f3f4b	refs/pull/1750/head
```

`HEAD -> lane-0428-223-testcontext-target` was reported as `[new branch]` by the push itself; the local HEAD equals the remote head (`dd5f1faba`).

## 3. Step 1 — reproduce develop red, remotely, at my own runs

Mission measurement (not re-run by me): run `44913143056`, head `dea88c8f2caa`, workflow `CI . Source & Quality`, event `workflow_dispatch`; `validate` job `136873016970`, step 14 `Run unit and package tests` = `go test ./...` (`.github/workflows/ci.yml:346`).

My own reproduction runs (§4.6 self-run duty):

| run id | event | head | conclusion | validate job | validate conclusion |
| --- | --- | --- | --- | --- | --- |
| 44916333992 | workflow_dispatch | 22fc68ebc065 | failure | (H-V50) 136873... | failure |
| 44918870333 | workflow_dispatch | 22fc68ebc065 | failure | 136890321112 | failure |
| 44918846567 | workflow_dispatch | 22fc68ebc065 | cancelled | — | superseded by 44918870333 (concurrency cancelled the first dispatch 25 s in; the second, 44918870333, ran to a terminal state and is my witness) |

`gh run view 44918870333` head SHA check: `git ... refs/heads/develop` = `22fc68ebc065...` = the run's `headSha`, so my repro ran against the same develop head I branched from. develop was NOT green when I measured it; the card therefore stays open on my fix.

Per-job log byte counts (`curl ... /actions/jobs/<id>/logs`, full stream, no 49152-byte truncation):

```
validate job 136890321112 (my run 44918870333):  124238 bytes
validate job 136873016970 (run 44913143056):      124366 bytes
gh api re-download of 136890321112:               124238 bytes (same size, byte-consistent witness)
```

`--- FAIL:` lines in my run's log: 16 lines = 14 distinct test names + 2 nested subtests of `TestGuidedInitDeterministicPositionalEnvironmentAliases` (`-e`, `--environment`). The name set is identical to the mission's `dea88c8f2caa` run (diff of the two sorted name lists is empty).

The 14 names, verbatim from job 136890321112:

```
TestDeterministicInitDoesNotPersistUnneededSourceSelection      app_init_source_neutral_test.go:72
TestDeterministicInitPersistsAmbiguousSourceSelectionPositive   app_init_source_neutral_test.go:90
TestGuidedInitQuickDoesNotPromoteHeuristicSecrets               app_init_wizard_test.go:74
TestGuidedInitInteractiveCanAcceptDetectedDefaults              app_init_wizard_test.go:118
TestGuidedInitDeterministicExplicitWorkloadSelectionSucceeds    app_init_wizard_test.go:170
TestGuidedInitExplicitFlagsKeepDeterministicPath                app_init_wizard_test.go:190
TestQuickInitPreservesWorkloadOnlyRepository                    app_init_wizard_test.go:254
TestQuickInitIsolatesMixedComposeInfrastructureAndGeneratesDetectedIntent  app_init_wizard_test.go:306
TestQuickInitScopesConcreteRuntimePermissionToSingleWorkload     app_init_wizard_test.go:368
TestGuidedInitDeterministicPositionalEnvironmentAliases          app_init_wizard_test.go:693 (2 subtests)
TestBahaStatusHostContainersDashboardsExposesUnavailable         app_perses_host_containers_cli_test.go:76
TestBahaStatusInfrastructureDashboardsExposesEveryPanel          app_perses_infra_dashboards_cli_test.go:88
TestBahaStatusInfrastructureDashboardsNotSelectedOmitsFace       app_perses_infra_dashboards_cli_test.go:128
TestSharedBackendReconcileRejectsSecondProcess                   application_lifecycle_lock_test.go:155
```

13 of the 14 carry `target "company-dev" is not configured`; `TestSharedBackendReconcileRejectsSecondProcess` reports `exit=exit status 1` with `child entered shared reconcile while another process held it`, i.e. its self-executed child failed before reaching the lock claim.

## 4. Cause, measured in source (not guessed)

The single seam all 14 share is the target selection read by `effectiveTarget`:

```go
// cmd/baha/target.go:88-102
func effectiveTarget(ctx context.Context) (deployment.ResolvedTarget, error) {
	cfg, err := deployment.LoadConfig()
	...
	explicit := targetOverrideFromContext(ctx)
	activated := strings.TrimSpace(os.Getenv("BASEHARBOR_TARGET"))
	selected, selectionErr := selectedTargetName(explicit, activated, cfg)
	...
	if effective.Target != nil {
		return cfg.ResolveTarget(effective.Target.Value, "")   // -> target %q is not configured
	}
```

`cmd/baha/target_selection.go:59-88` gives the environment activation priority over the config default and over the fixture target, and `internal/deployment/target.go:490` is the error text. The same file the mission points at, `cmd/baha/runtime_integration_test_support_test.go:849`, sets it with the non-rolling form:

```go
if err := os.Setenv("BASEHARBOR_TARGET", bootstrapTarget); err != nil {
```

`os.Setenv` is never rolled back inside the package process, unlike `t.Setenv`. The repository already states this and already treats it in the fixture helper (`cmd/baha/target_test_helpers_test.go:167-188`, `configureIsolatedTestTarget`):

```
// clears any TARGET/DATA/ENV leaked by an earlier test in the same package
// (BASEHARBOR_TARGET, BASEHARBOR_STATE_DIR, BASEHARBOR_ENV are set globally by
// the runtime-integration bootstrap via os.Setenv and never rolled back) ...
	t.Setenv("BASEHARBOR_TARGET", "")
	t.Setenv("BASEHARBOR_STATE_DIR", "")
	t.Setenv("BASEHARBOR_ENV", "")
```

The 14 cases are exactly the cases that resolve a target through the production path without ever applying that documented clearing. `80961866f` ("Fix managed CLI auth test contexts", 124 files) wired the operator identity (`testOperatorContext`/`runWithIOAsTestOperator`) into these call sites but did not give them the selection isolation the hermetic twin already does — so the auth half of the context is managed, the selection half is not.

`TestSharedBackendReconcileRejectsSecondProcess` is the same leak one level further out: its child is a fresh process built with `append(os.Environ(), ...)` (`cmd/baha/application_lifecycle_lock_test.go:152`), so it inherits the leaked activation and dies in setup with exit 1 rather than asserting the lock claim with exit 3.

Discriminating local proof (my worktree, compiled package test binary, `env -i` so only the injected variable differs):

```
BASEHARBOR_TARGET=company-dev, base binary (22fc68ebc, no fix):
  --- FAIL: TestDeterministicInitDoesNotPersistUnneededSourceSelection  target "company-dev" is not configured
  --- FAIL: TestGuidedInitQuickDoesNotPromoteHeuristicSecrets           target "company-dev" is not configured
  --- FAIL: TestBahaStatusHostContainersDashboardsExposesUnavailable    resolve probe application: target "company-dev" is not configured
  --- PASS: TestSharedBackendReconcileRejectsSecondProcess
  (the injected leak alone reproduces the CI failure text)

BASEHARBOR_TARGET=company-dev, fixed binary dd5f1faba, the 14 cases:
  14 passed, 0 failed   (the leak is now neutralised by the test context)

no leak (env -i, nothing set), fixed binary, the same 14 cases:
  14 passed, 0 failed   (the fix does not depend on the leak being present)
```

The 14 cases therefore fail only because of the ambient selection, exactly as the H-V50 classification said; the product resolution path is not at fault and no product change is needed.

## 5. The fix

New shared helpers in `cmd/baha/test_operator_context_test.go` (the test-helper file the mission names, introduced by `80961866f`):

```go
func testIsolatedSelectionContext(t *testing.T) {
	t.Helper()
	t.Setenv("BASEHARBOR_TARGET", "")
	t.Setenv("BASEHARBOR_STATE_DIR", "")
	t.Setenv("BASEHARBOR_ENV", "")
}

func envWithoutLeakedTargetSelection(env []string) []string { ... drops those three names ... }
```

`testIsolatedSelectionContext` is the same three-variable clearing `configureIsolatedTestTarget` already applies, factored into the shared context helper so a case that does not create a hermetic fixture gets the identical guarantee. `t.Setenv` restores each value at cleanup, so the clearing can neither leak into another test nor mask a target the test itself selects.

Call sites (the fixture root is made current before the command resolves anything):

- `cmd/baha/app_init_source_neutral_test.go`: 2 cases, after `withWorkingDirectory(t, root)`.
- `cmd/baha/app_init_wizard_test.go`: 7 cases plus the subtest body of `TestGuidedInitDeterministicPositionalEnvironmentAliases`, after `withWizardTestDir(t, ...)`.
- `cmd/baha/app_perses_host_containers_cli_test.go` and `cmd/baha/app_perses_infra_dashboards_cli_test.go`: once in each probe helper (`hostContainersProbeAppReport`, `persesInfraAppReport`), before `resolveApplication`.
- `cmd/baha/application_lifecycle_lock_test.go`: the shared-reconcile child env now goes through `envWithoutLeakedTargetSelection(os.Environ())`.

Explicitly NOT done: no `t.Skip`, no deleted or renamed case, no loosened expectation, no `ObservabilitySupported`/target enum value substituted for resolution (the failure mode that cost PR #1714 its request changes), no `.github/**` or `scripts/**` edit.

CI reachability of the changed tests (GATE RULE): I add no new test. All 14 changed cases are ordinary `cmd/baha` package tests, already executed by `go test ./...` in the `validate` job's step `Run unit and package tests` (`.github/workflows/ci.yml:346`) and by the PR `Go unit` shards. `validate` is gated by `github.event_name != 'pull_request'` (`.github/workflows/ci.yml:316`), so on PR runs it is `skipped` and only the branch `workflow_dispatch` executes the whole-package step. That missing develop/PR trigger is this card's decision point, owned by the CI owner; it is not part of my write-set and I changed nothing to work around it.

## 6. Branch run and validate cell

(to be completed in section 6a once the dispatched runs are terminal)

## repo-rule compliance

- Development guidelines and both AGENTS.md files read; changes are test-context only, inside the card's write-set (`cmd/baha/*_test.go`).
- Reality first: remote state measured with `git ls-remote <github url>` before and after every git write; the quarantined `workers/baseharbor` checkout was never cited as remote truth.
- Remote guard: every push/fetch resolved to the URL containing `github.com/mcpdev80`; delivery proved with `git ls-remote` of the branch and `refs/pull/1750/head`.
- One candidate per chain: only `lane-0428-223-testcontext-target` exists for this card. A scratch probe ref `zz-probe-0428-223` was created accidentally by pushing from the bookkeeping checkout while testing the remote; it was deleted immediately with an ls-remote witness before and after (§7).
- No merge, no second PR, PR kept draft until implementation and gate are complete; handoff marked by moving it to review.
- No subagents (AGENTS 4.8): every step executed in this session. No `git add -A`, no `git stash`; only targeted `git add <file>`.
- No bare `go test ./...` and no bare `go test ./cmd/baha/` on this host. Package validation used a compiled test binary run in my worktree under `env -i` with a private HOME/TMPDIR, and targeted `-run`/`-skip` forms otherwise; the whole-suite verdict comes from the hosted `validate` cell.
- `.github/**` and `scripts/**` untouched (Owner scope); the CI gap is reported as STATE, not edited.
- Evidence lives only in baseharbor-plan (`evidence/r28-welle4-2026-11-21/develop-full-suite-red/`); nothing written to a product repo, no `.evidence/` directory anywhere.
- Scratch confined to `workers/0428-223-testctx-wt` and `/var/tmp/0428-223-*`; nothing created in the ecosystem root.

## 7. cleanliness

Host container witness, own pid recorded. `docker ps -a` BEFORE my first run:

```
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS   NAMES
(empty)
```

`docker ps -a` AFTER my last action:

```
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS   NAMES
(empty)
```

- No container, network, volume or compose project was started by this lane: all Docker/Podman execution happened on GitHub-hosted runners only. Nothing on this host was torn down because nothing here was created.
- No test of mine owns a `bh-*` compose project; the `bh-itest-*` stack briefly visible in `docker ps` belonged to another session's run and was left untouched.
- `git worktree list` (lane entries only), before/after: my worktree `workers/0428-223-testctx-wt` is the only worktree this lane created and it stays for the review round; the two probe worktrees (`0428-223-clean-wt`, `0428-223-base-wt`) were removed with `git worktree remove` + `git worktree prune` and are gone from the list.
- Stray ref cleanup witness:

```
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/zz-probe-0428-223
c331a43f885e66cbc12ebd978d94cf50747b3129	refs/heads/zz-probe-0428-223      (before)
$ git push origin --delete zz-probe-0428-223
 - [deleted]           zz-probe-0428-223
$ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/zz-probe-0428-223
(no output)                                                              (after)
```

- Scratch binaries and logs live under `/var/tmp/0428-223-gotmp`, `/var/tmp/0428-223-evid`; removed at the end of the lane.
- Host disk pressure note for the coordinator (finding, not caused by me): `/home/marcel` was at 100% usage during this shift; gcc's `/tmp` writes failed (`Disk quota exceeded`) and Go needed `TMPDIR`/`GOTMPDIR` redirection into `/var/tmp`. A later `rm -rf` of a Go toolchain module cache hit root-owned read-only files. Worth a cleanup pass on `workers/`, `work-gotmp/` and `/var/tmp`.
cleanliness: no container, network, volume, compose project or state directory created or left by this lane on this host.

## 8. Handoff

- Candidate: `dd5f1faba` on `lane-0428-223-testcontext-target`, PR #1750 (draft -> review at handoff), base `22fc68ebc065`.
- What changed: 14 previously red `cmd/baha` cases now get their target selection isolated through the route the repository already documents; no product change, no skipped or weakened test.
- Evidence of red: develop dispatch `44918870333`, `validate` job `136890321112`, 124238-byte log, 14 names.
- Evidence of green: branch dispatch (§6a).
- Decision point for the coordinator/Owner (not mine to change): `.github/workflows/ci.yml:7-11` has no `develop` push trigger and `.github/workflows/ci.yml:316` gates `validate` off pull requests, so whole-package red is only visible through a manual `workflow_dispatch`.
