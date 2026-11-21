ROLLE: REVIEW

## PLAN

1. Record the numbered review plan in the board and this evidence file.
2. Resolve the GitHub remote and verify current develop, PR #1742 head/base, exact CI run, and before/after candidate freeze.
3. Compare the exact PR diff against measured develop and the card write-set and criteria.
4. Review credential-fill TTY/PTY paths and Finding 1 regression tests.
5. Review update-path prompt-class coverage and Finding 2 mutation evidence.
6. Verify required exact-head CI, record verdict and recipes or merge instruction, and publish only review-2.md.

Timestamp: 2026-11-21 11:46 UTC
Backend/model: Codex API, GPT-6

## Verdict

**REQUEST CHANGES — exact candidate `719d28a888abf9dc2c7715fb002f1aa77fdf9708`.** The PTY/prompt-path correction from review-1 is materially addressed, and the update helpers now assign non-TTY stdin with a mutation-sensitive source pin. However, the clone command's newly unconditional environment assignment drops the inherited environment, and the card's workaround-closeout evidence is absent. The PR is also behind current `develop`; that is a freshness finding, not a product-code defect.

## SHA, scope, and hosted checks

Product remote: `origin git@github.com:mcpdev80/baseharbor.git` (fetch/push). Planning remote, verified this turn: `origin https://github.com/mcpdev80/baseharbor-plan.git` (fetch/push).

Fresh `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1742/head` output:

```text
97b2ba5543f07b820b5c18a688058fd932c4516f refs/heads/develop
719d28a888abf9dc2c7715fb002f1aa77fdf9708 refs/pull/1742/head
```

PR API reports `state=OPEN`, `draft=false`, `mergeable=true`, `mergeStateStatus=BEHIND`, base `develop` at `4fa5293a49b7a6cd74c6513cf329dec15d08cfa9`, and head `719d28a888abf9dc2c7715fb002f1aa77fdf9708`. Compare from the actual PR base to the candidate is `ahead_by=3`, `behind_by=0`, with exactly these eight paths:

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

All eight are in the card's allowed scope, including `app_update.go` under the coordinator amendment. No `.github/**`, `internal/operatorauth/**`, `internal/identityprovider/**`, or `internal/serviceaccess/**` file is changed.

Against current `develop` `97b2ba5543f07b820b5c18a688058fd932c4516f`, GitHub compare reports `status=diverged`, `ahead_by=3`, `behind_by=16`, merge-base `4fa5293a49b7a6cd74c6513cf329dec15d08cfa9`. The exact-head run is green but predates the current base.

Run [44895100181](https://github.com/mcpdev80/baseharbor/actions/runs/44895100181) completed successfully on exact head `719d28a888abf9dc2c7715fb002f1aa77fdf9708`, event `pull_request`. `PR Selected Checks`, `PR · Trusted Plan`, `Workflow policy`, `PR · Go unit · cli-0`, `cli-1`, `cli-2`, `cli-3`, and `PR · Go unit · packages` all passed. The packages job is the CI cell documented for `internal/credential/native`; the round-2 evidence maps its trigger to `pull_request`. Skipped non-selected jobs are not counted as passes.

## Prompt and PTY review

At `cmd/baha/app_inspect_remote.go:61-76`, the clone command is created, given empty non-TTY stdin, and assigned `GIT_TERMINAL_PROMPT=0` at `:70` before the `cloneNonInteractive` branch at `:71`; `cmd.Run` follows at `:76`. The assignment therefore applies on both branch outcomes and closes Git's terminal-prompt path for the eventual clone. The native credential pre-probe has its own production `ExecRunner` environment sanitation in `internal/credential/native/host.go:34-43,68-81`.

The prior PTY finding is closed by the current tests: `TestGitCredentialFillIsNonInteractiveUnderControllingTerminal` unsets inherited prompt variables, attaches a real controlling PTY through `pty.Open`/`setsid`/`ctty`, requires the hook to have run, and asserts bounded host-named failure rather than resolved credentials or deadline expiry. The raw `ForkExec` M1 witness also reaches Git's own askpass path with the round-1 vector; `round-2-promptproof.md` records red for that vector and green for the fixed production environment. The exact-head packages job passed. The update-path amendment is covered by `TestGitOutputUpdatePathNeverTakesControllingTerminal`: it calls `gitOutput` and `gitIsAncestor` under a deadline and its AST pin fails when either `cmd.Stdin` assignment is removed.

## Findings and recipes

### Finding 1 — clone child environment is replaced instead of extended

File: `cmd/baha/app_inspect_remote.go:70`. `cmd.Env` is nil when the command is created, so `append(cmd.Env, "GIT_TERMINAL_PROMPT=0")` makes the child environment contain only that variable. In the previous version, the `nativeUsed=false` path left `cmd.Env` nil and inherited the process environment; moving the assignment before the branch changes that path to an explicit one-variable environment. This drops inherited `PATH`, `HOME`, proxy, certificate, and Git configuration variables needed by `git clone`; the native-used branch already had the one-variable assignment before this PR.

Change: preserve the inherited environment and set/replace only `GIT_TERMINAL_PROMPT` with `0` (prefer one unambiguous value while retaining the rest of the environment).

Test requirement: add a focused clone-command regression using a sentinel environment/child capture (or a controlled Git helper) that proves `HOME`, `PATH`, and required transport configuration survive while the child sees `GIT_TERMINAL_PROMPT=0`; also assert the no-credential case terminates with a host-bearing error and no prompt.

Stop criterion: the clone child has the required inherited environment and prompt suppression on both `cloneNonInteractive` outcomes; the test fails if the environment collapses to only the sentinel.

### Finding 2 — card workaround closeout is not recorded in the round-2 evidence

File: `evidence/r28-welle4-2026-11-21/git-credential-fill/round-2-promptproof.md`. My search found no statement that the earlier `GIT_TERMINAL_PROMPT=0 GIT_ASKPASS=/bin/true SSH_ASKPASS=/bin/true` workaround is no longer needed, nor a named exception location. The exact-head checks prove the selected jobs passed, but the card separately requires this workaround status in the handoff evidence.

Change: record that the exact-head hosted cells passed without the workaround, or list each remaining location with `file:line` and the reason it still needs it.

Test requirement: tie the statement to run `44895100181` and the exact head; check the affected hosted-cell invocation/configuration for the workaround rather than infer removal from a green job alone.

Stop criterion: every previously affected hosted cell is accounted for, the workaround is confirmed unnecessary or all residual uses are named, and the exact-head result is recorded.

### Finding 3 — candidate is behind current `develop` (freshness only)

File: none; this is a branch-base finding, not a product-code defect. Current `develop` is `97b2ba5543f07b820b5c18a688058fd932c4516f`; the PR's base is `4fa5293a49b7a6cd74c6513cf329dec15d08cfa9` and the candidate is behind by 16 commits.

Change: hop the same candidate onto the then-current `develop`, then obtain a new exact-head required aggregate.

Test requirement: `PR Selected Checks`, `PR · Trusted Plan`, `Workflow policy`, and the required CLI shards pass at the hopped head; packages coverage for `internal/credential/native` remains executed.

Stop criterion: current `develop` is an ancestor of the candidate and the exact-head required checks complete successfully.

## Repo-rule compliance

Read-only product review; no product file, PR, workflow, or branch was changed. No local product tests were run. Only this review evidence file is to be published.

END REVIEW DONE
