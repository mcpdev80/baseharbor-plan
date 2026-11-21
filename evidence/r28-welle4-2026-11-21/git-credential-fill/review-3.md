# PR #1742 fresh verdict r3

ROLLE: REVIEW
Karte: `t-20261121-git-credential-fill-bootstrap-hang` (0428-217)
Zeit: 2026-11-21 12:42 UTC
Backend/Modell: Codex via OpenAI AgentGateway; exact model ID is not exposed in this session.
Kandidat: `20ad0713e9892492204cf88910ee926ee20d1461`

## PLAN

1. Mission, Task-Vertrag und Review-2-Befunde prüfen.
2. Aktuelle GitHub-Refs und PR-Status messen, Ancestry, Diff und Commitliste für den exakten Head prüfen.
3. Die Clone-Environment-Änderung, alle `GIT_TERMINAL_PROMPT`-Vorkommen und die geforderte Mutationsevidence gegenprüfen.
4. Die vorgeschriebenen Checks und deren terminalen Status am exakten Head messen.
5. Das sha-genaue Verdict samt umsetzbaren Rezepten schreiben und ausschließlich diese Evidence-Datei publizieren.

## Wörtliches Verdict

**REQUEST CHANGES — exact candidate `20ad0713e9892492204cf88910ee926ee20d1461`.** The `GIT_TERMINAL_PROMPT=0` assignment is now before `cloneNonInteractive`, and the exact-head required checks are green. However, `cmd/baha/app_inspect_remote.go:70` still assigns an environment containing only that one entry to the clone process, so the fix drops inherited variables such as `PATH` and `HOME`. The required `round-4-clone-env.md` mutation evidence is also absent. The card's hosted-workaround closeout remains undocumented. Do not merge this candidate.

## Remote and provenance witnesses

Commands run against the resolved GitHub repository:

```text
git remote -v
lane-origin https://github.com/mcpdev80/baseharbor.git (fetch)
lane-origin https://github.com/mcpdev80/baseharbor.git (push)
origin https://github.com/mcpdev80/baseharbor.git (fetch)
origin https://github.com/mcpdev80/baseharbor.git (push)
upstream https://github.com/mcpdev80/baseharbor.git (fetch)
upstream https://github.com/mcpdev80/baseharbor.git (push)

git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1742/head
97b2ba5543f07b820b5c18a688058fd932c4516f refs/heads/develop
20ad0713e9892492204cf88910ee926ee20d1461 refs/pull/1742/head
```

`gh pr view 1742 --repo mcpdev80/baseharbor --json state,isDraft,mergeable,mergeStateStatus,headRefOid,baseRefName,changedFiles` returned `state=OPEN`, `isDraft=false`, `mergeable=MERGEABLE`, `mergeStateStatus=CLEAN`, `baseRefName=develop`, `headRefOid=20ad0713e9892492204cf88910ee926ee20d1461`, `changedFiles=8`.

The candidate is current-base-descended: `git merge-base --is-ancestor 97b2ba5543f07b820b5c18a688058fd932c4516f 20ad0713e9892492204cf88910ee926ee20d1461` returned 0. `git rev-list --count 97b2ba5543f07b820b5c18a688058fd932c4516f..20ad0713e9892492204cf88910ee926ee20d1461` returned `2`. The diff paths are exactly:

```text
cmd/baha/app_inspect_remote.go
cmd/baha/app_update.go
cmd/baha/app_update_gitstdin_test.go
internal/credential/native/credfill_noninteractive_test.go
internal/credential/native/credfill_pty_linux_test.go
internal/credential/native/credfill_pty_stub_test.go
internal/credential/native/gitcredential.go
internal/credential/native/host.go
```

`git log --oneline 97b2ba5543f07b820b5c18a688058fd932c4516f..20ad0713e9892492204cf88910ee926ee20d1461` lists only these two candidate commits:

```text
20ad0713e test(0428-217): prove the credential-fill fix on git's own prompt path
b0e995027 fix(0428-217): git credential fill must fail closed non-interactively with host-named no-credential error
```

The eight paths remain within the card's amended write-set. The diff contains no `.github/**`, `internal/operatorauth/**`, `internal/identityprovider/**`, or `internal/serviceaccess/**` path.

## Source review and findings

At the reviewed SHA, `cmd/baha/app_inspect_remote.go:61` creates the `git clone` command. Lines 67–70 now set non-TTY stdin and `cmd.Env = append(cmd.Env, "GIT_TERMINAL_PROMPT=0")` before the `cloneNonInteractive` call at line 71. This closes the ordering issue, but `exec.CommandContext` leaves `cmd.Env` nil by default; appending to nil creates a one-entry environment and does not inherit the parent process environment. By comparison, `cmd/baha/app_update.go:475–479` copies an input environment, and `:493` calls the helper with `os.Environ()`; `cmd/baha/management_core_git_source.go:42` also appends to `os.Environ()`.

The reviewed `GIT_TERMINAL_PROMPT` occurrences under `cmd/baha` resolve as follows: `app_inspect_native_counterprobe_test.go:44`, `app_inspect_remote.go:64`, `app_update.go:471` and `:482`, and `app_update_gitstdin_test.go:40` are comments; `app_inspect_remote.go:70` is the failing production assignment; `app_update.go:478` is the helper append whose caller supplies `os.Environ()` at `:493`; `app_update_gitstdin_test.go:42` sets the test environment; `management_core_git_source.go:42` explicitly appends to `os.Environ()`. Thus the parent-environment defect remains isolated to the inspect clone path.

### Finding 1 — inspect clone drops inherited environment

File: `cmd/baha/app_inspect_remote.go:70`.

Change: initialize the child environment from `os.Environ()` and set `GIT_TERMINAL_PROMPT=0` without discarding the inherited environment. Prefer the existing helper or an equivalent environment-copy/update helper that handles an existing key without creating duplicate conflicting values.

Test requirement: add a regression that exercises the actual inspect clone command path with a parent sentinel variable and a child probe. Assert the child sees the sentinel and sees prompt suppression. Mutate away environment inheritance and require the sentinel assertion to fail; mutate away prompt suppression and require the prompt assertion to fail. The existing native `ExecRunner` sentinel test does not cover this separate `exec.CommandContext` clone path.

Stop criterion: both mutations fail the focused regression, and the corrected production path passes with inherited sentinel and prompt suppression present. The regression must be in the same PR and run by the existing CLI CI group.

### Finding 2 — required round-4 clone-environment mutation evidence is absent

The mission-named `evidence/r28-welle4-2026-11-21/git-credential-fill/round-4-clone-env.md` is absent from the fetched planning `origin/main` tree. The round-3 hop evidence only records moving the prompt variable above `cloneNonInteractive`; it does not show the two environment mutations requested by this mission.

File: `evidence/r28-welle4-2026-11-21/git-credential-fill/round-4-clone-env.md`.

Change: publish the actual clone-path sentinel and prompt-suppression regression results, including each mutation command and its failing output. Do not treat the native credential helper sentinel test as proof for the inspect clone command.

Test requirement: run the focused regression in its unmutated state and both mutations; record that each mutation exits nonzero for its expected assertion. Keep the test reachable through the existing CLI shard.

Stop criterion: the artifact is present in planning `origin/main`, the unmutated regression passes, and both specified mutations fail for the expected reason.

### Finding 3 — hosted workaround closeout is not recorded

The round-2 evidence documents a prompt workaround, while the round-3 hop evidence only restates `GIT_TERMINAL_PROMPT=0`; it does not say whether earlier hosted cells now pass without `GIT_TERMINAL_PROMPT=0 GIT_ASKPASS=/bin/true SSH_ASKPASS=/bin/true`, nor name any remaining use by file and line. The green run alone cannot establish that required closeout.

File: `evidence/r28-welle4-2026-11-21/git-credential-fill/round-4-clone-env.md` (or the task's designated round-4 closeout evidence).

Change: identify each previously affected hosted cell, state whether the workaround is no longer needed, or list each remaining use by file and line with its reason. Tie the claim to the exact-head hosted run and inspect the invocation/configuration rather than infer removal from a green status.

Test requirement: verify the relevant hosted invocation/configuration and record the exact-head run result for the affected cell(s).

Stop criterion: every previously affected cell is accounted for, with the workaround explicitly closed or all remaining uses named and justified.

## Exact-head CI

`gh run view 44900657812 --repo mcpdev80/baseharbor --json headSha,status,conclusion,event,url` returned:

```json
{"conclusion":"success","event":"pull_request","headSha":"20ad0713e9892492204cf88910ee926ee20d1461","status":"completed","url":"https://github.com/mcpdev80/baseharbor/actions/runs/44900657812"}
```

`gh pr checks 1742 --repo mcpdev80/baseharbor` showed `PR Selected Checks=pass`, `PR · Go unit · cli-0=pass`, `cli-1=pass`, `cli-2=pass`, `cli-3=pass`, `PR · Go unit · packages=pass`, `PR · Trusted Plan=pass`, `PR · Native gate plan=pass`, `Workflow policy=pass`, and the selected source-format, focused-Python, and validation jobs passing. The four required CLI shard logs were individually queried with `gh run view 44900657812 --job <job-id> --log`; job IDs are cli-0 `136835719628`, cli-1 `136835719585`, cli-2 `136835719603`, cli-3 `136835719597`. Their terminal conclusions are pass. The required aggregate is terminal success on this exact SHA. Unselected runtime, release, pin, and draft jobs are skipped and are not counted as passes.

## Repo-rule compliance

This was a read-only product review. No product file, PR, merge state, workflow, card, or branch was changed. Only this review evidence file is staged for publication. No subagents were used. The planning checkout is `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`; its `git remote -v` resolves `origin` to `https://github.com/mcpdev80/baseharbor-plan.git`.

## cleanliness

`docker ps -a` before publication returned only the header (`CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES`), zero containers; shell PID was `2634758`. No container or compose project was started.

END REVIEW DONE — REQUEST CHANGES for `20ad0713e9892492204cf88910ee926ee20d1461`.
