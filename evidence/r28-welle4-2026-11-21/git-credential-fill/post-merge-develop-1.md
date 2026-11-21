ROLLE: REVIEW

## PLAN

1. Measure remote develop and verify PR candidate ancestry. Done.
2. Inspect credential prompt environment handling on develop and verify the three PR commits. Done.
3. Inspect develop hosted run and per-job evidence for relevant CLI shard status. Done; CI log archives could not be read.
4. Publish the read-only post-merge review evidence to baseharbor-plan origin/main. In progress.
5. Post final lane status with develop SHA. Pending.

## 1. Remote develop and ancestry

- Real product remote verified first: `lane-origin https://github.com/mcpdev80/baseharbor.git (fetch)` and `lane-origin https://github.com/mcpdev80/baseharbor.git (push)`. The shared checkout also has `origin` and `upstream` pointing to the same GitHub URL; reads used `lane-origin`.
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` returned `dea88c8f2caa2db93c1216c619993e444080a9d2 refs/heads/develop`.
- Fetched `lane-origin develop`; `FETCH_HEAD` was `dea88c8f2caa2db93c1216c619993e444080a9d2`.
- `git merge-base --is-ancestor 6f8fa120f7e5e79d260ed89d486633bc152105de FETCH_HEAD` exited 0. The merged PR candidate is an ancestor of current develop.
- The three PR commits each passed `git merge-base --is-ancestor <commit> FETCH_HEAD` (exit 0): `b0e995027`, `20ad0713e`, and `6f8fa120f`.
- `git log --oneline FETCH_HEAD -- cmd/baha/app_inspect_remote.go | head`:
  - `6f8fa120f fix(0428-217): clone inspect must inherit parent env while suppressing git prompt (BEFUND 1)`
  - `b0e995027 fix(0428-217): git credential fill must fail closed non-interactively with host-named no-credential error`
  - `e3b4300f3 fix fish shell context wrapper compatibility (#1713)`

## 2. Code on develop

`git grep -n "GIT_TERMINAL_PROMPT" FETCH_HEAD -- cmd/baha internal/credential` and `git grep -n "cmd\.Env" FETCH_HEAD -- cmd/baha internal/credential` were inspected against fetched develop, not the PR checkout.

- `cmd/baha/app_inspect_remote.go:74` assigns `cmd.Env = withGitPromptDisabled(os.Environ())` for `git clone` (`:61`). The parent `HOME`, `PATH`, and configured credential helpers are retained.
- `cmd/baha/app_update.go:478` appends `GIT_TERMINAL_PROMPT=0` to the supplied environment; `gitOutputDisabledPrompt` supplies `withGitPromptDisabled(os.Environ())` at `:493`.
- `cmd/baha/management_core_git_source.go:42` assigns `append(os.Environ(), "GIT_TERMINAL_PROMPT=0", "GIT_OPTIONAL_LOCKS=0")` to the environment for the Git verification command at `:41`.
- `internal/credential/native/host.go:42` assigns `appendNonInteractiveEnv(cmd.Env)`. Its helper at `:68-81` uses `os.Environ()` when `cmd.Env` is nil, removes inherited prompt-channel keys, and appends its noninteractive values. The Git credential caller is `internal/credential/native/gitcredential.go:52`; the other production caller inspected is `ssh-add` in `internal/credential/native/sshagent.go:58,72`.
- Other `cmd.Env` assignments found in this path are not literal Git child environments: `cmd/baha/app_access.go:49,88` uses process-env replacement for database/cache clients, and `cmd/baha/update_mutation.go:397` passes the environment built by `selfUpdateEnvironment` to the `baha` executable.
- No `cmd.Env` assignment creating a Git child from a literal list without `os.Environ()` was found. No code defect found in the requested develop-head trace.

## 3. Hosted evidence on develop

Exact develop head: `dea88c8f2caa2db93c1216c619993e444080a9d2`.

`gh run list --commit dea88c8f2caa2db93c1216c619993e444080a9d2` returned two runs:

- Run `44909775538`, `Runtime · Podman Core`, event `push`, terminal `completed / success`, exact head `dea88c8f2caa2db93c1216c619993e444080a9d2`. Selector job `136862904001` succeeded; `podman-quadlet`, `Native single-default · Podman`, and `Native Keycloak+SQL single · Podman` were skipped.
- Run `44909775545`, `Runtime · Docker Core`, event `push`, terminal `completed / success`, exact head `dea88c8f2caa2db93c1216c619993e444080a9d2`. Selector job `136862903844` succeeded; `provider-ha`, `docker-runtime`, `mcp-edit-native`, `Native single-default · Docker`, and `Native Keycloak+SQL single · Docker` were skipped.
- `CI · Source & Quality` workflow has no run at this develop head. Its newest listed run for branch `develop` is older (`43861879543`, head `521ff2f04e858feb5920a1b601b41e0ccc8f23e1`, event `pull_request`, conclusion `failure`). This older run is not evidence for current develop.
- The develop-head check-run inventory contains the two runtime workflow runs only; no `unit_tests` job or CLI shard ran at this SHA. Therefore there is no develop CLI shard conclusion to compare with the PR-head shards and no basis to report a merge-induced CLI regression.
- Per-job log retrieval was attempted with `gh run view 44909775538 --job 136862904001 --log` and the analogous Docker selector command (`44909775545`, job `136862903844`). Both returned `failed to get run log: zip: not a valid zip file`. No valid per-job log bytes were available. Accordingly the requested per-job `--log` bytes / `--log-failed` bytes / line-count triplets are unavailable; failed retrievals are not recorded as zero-byte logs. No test-receipt counts are inferred from skipped jobs.

## Finding and disposition

**befund: develop-head unit-test evidence is absent.** The PR candidate and its three listed commits are present on develop, and the inspected code retains the parent environment while disabling terminal credential prompts. However, no `CI · Source & Quality` or `unit_tests` run exists at the current develop head, and both runtime workflows skipped their native test cells. The run evidence therefore does not establish that the PR's tests passed on the merged develop commit. No CLI shard was red on develop because no CLI shard ran.

Recipe: obtain an authorized, genuine hosted test run for exact develop SHA `dea88c8f2caa2db93c1216c619993e444080a9d2`, with executed `unit_tests`/CLI coverage and readable per-job logs. Re-evaluate only those exact-head results; do not treat skipped jobs or the older failed `CI · Source & Quality` run as evidence for this SHA. This review did not dispatch or rerun any workflow.

## cleanliness

Before review: own shell PID `3317607`; `docker ps -a` output:

```text
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

After review: own shell PID `3345271`; `docker ps -a` output:

```text
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

## Pre-push check

As instructed before a push, ran `bash scripts/ci-fast-check.sh` in the shared product checkout. It exited 1 after 295 tests: 294 passed and `test_real_candidate_go_registration_families` errored because Go could not write `/tmp/args2730772513` (`disk quota exceeded`). This is local test-discovery evidence, not a hosted develop run; no workflow was dispatched. The required evidence publication changes only this Planning file.

END codex-rev-1747 DONE: post-merge develop review recorded for `dea88c8f2caa2db93c1216c619993e444080a9d2`.
