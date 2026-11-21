# PR #1742 exact-head review r4

ROLLE: REVIEW
Karte: `t-20261121-git-credential-fill-bootstrap-hang` (0428-217)
Zeit: 2026-11-21 13:01 UTC
Backend/Modell: Codex via OpenAI AgentGateway; exact model ID is not exposed in this session.
Kandidat: `6f8fa120f7e5e79d260ed89d486633bc152105de`

## PLAN

1. Read the r4 mission and confirm scope, evidence path, required checks, and stop conditions.
2. Verify resolved GitHub remotes, current develop and PR head, ancestry, diff, and candidate commit provenance.
3. Inspect r4 implementation, regression and mutation evidence, and hosted-workaround closeout against the card criteria.
4. Verify the required terminal CI aggregate and all required CLI shards for the exact candidate head.
5. Write the sha-specific verdict and findings in the designated plan evidence file.
6. Publish only the verdict file and verify its path on planning origin/main.

## Verdict

**Verdict: APPROVE CONTENT** for exact candidate `6f8fa120f7e5e79d260ed89d486633bc152105de`.

The clone environment fix inherits the parent process environment and applies prompt suppression. The regression demonstrates a parent sentinel reaching a child, and both requested mutations fail for their intended assertions. The current-head hosted CLI shards and `PR Selected Checks` pass. The round-4 evidence is present on planning `origin/main` and records both mutation results and the workaround closeout. No remaining content finding.

**Pre-merge condition: publish `round-4-clone-env.md` before merge.** It is already published at the fetched `origin/main` revision recorded below. **Merge PR #1742 next in this window.** This session did not merge or modify the PR.

## Remote state and exact diff

First Git action in the product checkout:

```text
git remote -v
origin https://github.com/mcpdev80/baseharbor.git (fetch)
origin https://github.com/mcpdev80/baseharbor.git (push)
```

The quarantined checkout was used only to resolve the remote URL; remote truth below comes from the explicit GitHub URL and GitHub API.

```text
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1742/head
97b2ba5543f07b820b5c18a688058fd932c4516f refs/heads/develop
6f8fa120f7e5e79d260ed89d486633bc152105de refs/pull/1742/head
```

`gh pr view 1742 --repo mcpdev80/baseharbor --json state,isDraft,mergeable,mergeStateStatus,headRefOid,baseRefName,changedFiles` returned `state=OPEN`, `isDraft=false`, `mergeable=MERGEABLE`, `mergeStateStatus=CLEAN`, `baseRefName=develop`, `headRefOid=6f8fa120f7e5e79d260ed89d486633bc152105de`, `changedFiles=9`.

The GitHub compare API for `97b2ba5543f07b820b5c18a688058fd932c4516f...6f8fa120f7e5e79d260ed89d486633bc152105de` returned `status=ahead`, `ahead_by=3`, `behind_by=0`, and merge base `97b2ba5543f07b820b5c18a688058fd932c4516f`. Thus the measured `develop` head is an ancestor of the candidate. The exact nine-file delta is:

```text
cmd/baha/0428-217_clone_env_test.go
cmd/baha/app_inspect_remote.go
cmd/baha/app_update.go
cmd/baha/app_update_gitstdin_test.go
internal/credential/native/credfill_noninteractive_test.go
internal/credential/native/credfill_pty_linux_test.go
internal/credential/native/credfill_pty_stub_test.go
internal/credential/native/gitcredential.go
internal/credential/native/host.go
```

The compare API lists these three commits, all on the existing PR candidate:

```text
b0e995027a35e44c236246e01b895f14cd2ad27c fix(0428-217): git credential fill must fail closed non-interactively with host-named no-credential error
20ad0713e9892492204cf88910ee926ee20d1461 test(0428-217): prove the credential-fill fix on git's own prompt path
6f8fa120f7e5e79d260ed89d486633bc152105de fix(0428-217): clone inspect must inherit parent env while suppressing git prompt (BEFUND 1)
```

No forbidden path appears in the delta: no `.github/**`, `internal/operatorauth/**`, `internal/identityprovider/**`, or `internal/serviceaccess/**`.

## Finding 1 verification: child environment inheritance

The candidate snapshot was read from GitHub at the exact commit. The `GIT_TERMINAL_PROMPT` occurrences that construct child environment vectors in the requested paths are:

- `cmd/baha/app_inspect_remote.go:74`: `withGitPromptDisabled(os.Environ())`; inherits the parent vector, then adds prompt suppression. Pass.
- `cmd/baha/app_update.go:478`: `withGitPromptDisabled` copies the supplied vector before adding `GIT_TERMINAL_PROMPT=0`; production caller at `:493` passes `os.Environ()`. Pass.
- `cmd/baha/management_core_git_source.go:42`: appends prompt suppression to `os.Environ()`. Pass.
- `internal/credential/native/host.go:75`: `appendNonInteractiveEnv` removes prompt-channel keys from a base vector and appends the fail-closed values. When the caller leaves `cmd.Env` nil, it first obtains `os.Environ()` at `:70-72`, preserving unrelated parent values. Pass.
- `internal/credential/native/host.go:102`: `CredentialFillEnvSickForTest`, an explicitly test-only round-1 vector. It starts from the supplied base or `os.Environ()` and intentionally leaves the old prompt channel in place to reproduce the defect; it is not a production child-environment path.

Other matches in these directories are comments or test setup (`t.Setenv` and assertions), not production child-list assignments. No production construction in the requested paths appends to a nil environment.

The exact-head source at `cmd/baha/app_inspect_remote.go:70-74` derives the clone environment from `os.Environ()` through the existing helper before `cloneNonInteractive` and `cmd.Run`. The helper copy and suppression behavior is covered by the new focused child probe.

## Finding 1 mutation and regression evidence

I fetched `evidence/r28-welle4-2026-11-21/git-credential-fill/round-4-clone-env.md` from planning `origin/main`. It records:

- `TestGitCloneInspectInheritsParentEnvAndSuppressesPrompt`: a child probe sees `BASEHARBOR_0428_217_SENTINEL=1` and `PATH`, while the effective final `GIT_TERMINAL_PROMPT` value is `0` despite an inherited hostile value of `1`.
- M1 mutation reintroducing `append(cmd.Env, "GIT_TERMINAL_PROMPT=0")` fails `TestGitCloneInspectEnvDerivationMutationAppendedNil` with the expected failure: the source still uses the buggy nil-environment append.
- M2 mutation removing prompt suppression fails `TestGitCloneInspectPromptSuppressionPresent` with the expected failure that the helper must append `GIT_TERMINAL_PROMPT=0`.

The recorded focused command uses the named `-skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"` exclusions. I did not run product tests in this review session. The artifact also records CI pickup through the existing `cmd/baha` CLI unit shards.

## Finding 3 verification: hosted workaround closeout

The exact-head run `44905476380` is completed/success on this PR head. The four CLI shards, `PR · Go unit · packages`, `PR · Trusted Plan`, `PR · Native gate plan`, and `PR Selected Checks` passed. The CLI job IDs were checked in their per-job logs: cli-0 `136850045521`, cli-1 `136850045574`, cli-2 `136850045487`, cli-3 `136850045507`. Their logs reached the completed-job cleanup; the terminal conclusions are pass as shown in `gh pr checks`.

I also scanned the exact candidate snapshot's workflow and script files for `GIT_TERMINAL_PROMPT`, `GIT_ASKPASS`, and `SSH_ASKPASS`. No workflow or test-script entry injects the triad `GIT_TERMINAL_PROMPT=0 GIT_ASKPASS=/bin/true SSH_ASKPASS=/bin/true` into these hosted jobs. The only grep hits in that scan are unrelated `GIT_TERMINAL_PROMPT=0` values in `scripts/receipt_writer.py`. The selected hosted CLI and package cells therefore passed without that CI-injected workaround. The round-4 closeout identifies the product-side non-interactive handling still present at `internal/credential/native/host.go:75-79` and the bounded update-path stdin assignments; it states there is no remaining workaround site to list. This closes the card's hosted-cell criterion.

`gh run view 44905476380 --repo mcpdev80/baseharbor --json headSha,status,conclusion,event,url` returned:

```json
{"conclusion":"success","event":"pull_request","headSha":"6f8fa120f7e5e79d260ed89d486633bc152105de","status":"completed","url":"https://github.com/mcpdev80/baseharbor/actions/runs/44905476380"}
```

The `gh pr checks` output for this same head showed `PR Selected Checks=pass`; `PR · Go unit · cli-0`, `cli-1`, `cli-2`, and `cli-3` all pass; `PR · Go unit · packages=pass`; `PR · Trusted Plan=pass`; `Workflow policy=pass`; source format and validation gofmt/build/vet pass. Runtime, release, and other unselected jobs are skipped and are not represented as passing checks.

## Planning evidence witness

Planning repository remote resolution:

```text
git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v
origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin https://github.com/mcpdev80/baseharbor-plan.git (push)
```

After fetching `origin main`, the required path lookup returned:

```text
evidence/r28-welle4-2026-11-21/git-credential-fill/round-4-clone-env.md
```

## Repo-rule compliance and cleanliness

This was a read-only product review. No product file, PR state, branch, workflow, task card, or merge state was changed. No tests or containers were started in this review session. I did not use a subagent or `git stash`.

`docker ps -a` returned only the header (`CONTAINER ID IMAGE COMMAND CREATED STATUS PORTS NAMES`), zero containers; shell PID was `2850483`. No compose project was started.

END REVIEW DONE — APPROVE CONTENT for `6f8fa120f7e5e79d260ed89d486633bc152105de`.
