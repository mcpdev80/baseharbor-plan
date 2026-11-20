# CLI2 context-shell round 1 — 0428-068

**Card:** t-20261114-r28-cli2-context-shell (0428-068) · Lane: `w068-pr0428-068-context-shell`
**Release:** v0.4.28 · Product repo: `mcpdev80/baseharbor`
**Owner:** w068-pr0428-068-context-shell
**Date:** 2026-11-20
**Status:** DONE — product PR #1710 head `eff023c0` green and frozen; awaiting Owner-ordered CODEX-REVIEW on the frozen head.

## PLAN

1. Establish zones and remote truth (remote guard, wrong-zone guard, base attestation).
2. Read task contract + owner inputs: card Goal/Scope/Entry points, owner brief, command-map, code-entry-index, owner-approved CLI contract v1.
3. Resolve the scope conflict with the Owner (ruling 2026-11-20, two sessions): additive context group, own new files, no rename, one-time hook setup.
4. Re-validate the current develop (HEAD 36d075fa) target/use/completion/prompt surface against the contract's proposed context group.
5. Implement context use/clear/show + hook setup in own new files; add precedence tests.
6. Local vet/build, one PR (base develop), observe one pull_request run to terminal, record run-id + conclusion.

## Remote witnesses

Branch head frozen at eff023c0; product PR #1710 base.sha = develop 36d075fad77f, draft false, mergeable clean.

```
$ git -C /tmp/opencode/x-068-wt/core rev-parse origin/develop
36d075fad77fa61ac8c153e979855546589b32c2
$ git -C /tmp/opencode/x-068-wt/core ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/b-068-cli2-context-shell refs/pull/1710/head
eff023c07810c45217b205622b6c677fbb580621	refs/heads/b-068-cli2-context-shell
eff023c07810c45217b205622b6c677fbb580621	refs/pull/1710/head
$ git -C /tmp/opencode/x-068-wt/core merge-base --is-ancestor 36d075fad77fa61ac8c153e979855546589b32c2 refs/pull/1710/head; echo $?
0
```

CI run 44700679422 on frozen head eff023c0: completed | success, 30 jobs (19 success, 0 failure, rest skipped). All Go shards (cli-0..cli-3, packages, owner) + documentation-audit green.

## Precedence

Order is an acceptance criterion (owner ruling 2026-11-20, ruling 2); one focused test per level in `cmd/baha/context_terminal_test.go`:

- flag > env: `TestContextPrecedenceExplicitFlagWins` — explicit `--target`/context override stage wins.
- shell-env > default: `TestContextPrecedenceShellEnvWinsOverDefault` — per-terminal BASEHARBOR_TARGET beats configured-default.
- default fallback: `TestContextPrecedenceDefaultFallback` — configured-default wins with no env.
- winner named: `TestContextShowReportsWinningStage` — `context show` prints the winning precedence level.

Supporting tests: `TestContextUseEmitsExportSnippet`, `TestContextUseFishSnippet`, `TestContextUseRejectsUnknownShell`, `TestContextUseRequiresTarget`, `TestContextClearUnsetsInProcess`, `TestCompletionHookEmitted`, `TestActivationSnippetRender`, `TestShellAbsentFallbackHints`, `TestContextGroupRegistered`.

## Repo-rule compliance

- Additive only: `commands.go` gains one `contextCommand()` line in `rootCommand()` (+1 line, no rename, no helper move, no signature change on noArgs/noArgsCtx/usageError).
- New content in own new files only: `cmd/baha/context_terminal.go`, `cmd/baha/context_terminal_test.go`, `cmd/baha/completion_setup.go` — names absent on develop.
- `cmd/baha/completion.go` change is additive (hook appended, +27 lines); existing completion tab logic unchanged, existing completion path not broken.
- `cmd/baha/machine_coverage.go` +4 presentation rows so `classifyCommandCoverage` no longer returns `gap` for context; `docs/cli/command-index.md`, `docs/de/cli/command-index.md`, `docs/reference/cli-machine-coverage.md`, `docs/de/reference/cli-machine-coverage.md` regenerated/extended (+4 rows each).
- `cmd/baha/app_status_result.go` NOT touched.
- No `.github/**` changes; no subagents (§4.8); no merge; no `git add -A` in the product worktree (selective `git add` only).
- `go build ./...` and `go vet ./...` clean (exit 0).

## Outcome

<status> — run-id 44700679422 (success, head eff023c0) — conclusion: DONE. Product PR #1710 (base develop 36d075fa, head eff023c0, not draft) is green on the frozen head. Working tree frozen in the product clone; no further product push pending acceptance. Awaiting Owner to order CODEX-REVIEW on the frozen head; an explicit verdict (not the interruption record 1709-0428-168-r2) is the gate for acceptance.

---

# CLI2 context-shell round 2 — 0428-068 (r2: CODEX-REVIEW REQUEST CHANGES fixed)

**Date:** 2026-11-20
**Status:** r2 fix DELIVERED; PR #1710 head = d1ec4b72; CI 44712300731 terminal-success. Owner ordering file-move to new `cmd/baha/context_hook.go`; no further push pending Owner direction.

## The 4 blockers (r2)

CODEX-REVIEW 1710-0428-068 verdict REQUEST CHANGES, 4 blockers. Owner ruling = option 4: an interactive-shell wrapper function named `baha` that calls the real program with `command baha` (recursion guard) and propagates `context use`/`context clear` into the parent shell's own process (export/unset `BASEHARBOR_TARGET`). Child changes nothing about parent; the interactive parent changes itself. No PID, pane id, or marker file.

- **Blocker 1** (parent-shell effect without eval): added `baha()` wrapper + `_baha_context_wrapper` in `completion_setup.go:41-104`; wired into `completion.go:203-270` emitters. Fixes `context_terminal.go:153-163` (os.Unsetenv in child only). Interactive guard: bash/zsh `[[ $- == *i* ]]`, fish `status is-interactive`.
- **Blocker 2** (native per-shell + completion safety): per-shell native mechanism; non-interactive `bash -c`/pipelines never see the wrapper; wrapper forwards `command baha __complete` so completion works through the interactive function.
- **Blocker 3** (precedence fallback): unchanged order explicit flag > `BASEHARBOR_TARGET` (wrapper-set) > terminal env > existing user/system selection contract (`selectedTargetName`/`targetSelectionOrigin`). Wrapper writes no config.
- **Blocker 4** (test quality): precedence tests now drive real `baha context show`; real interactive bash sources the wrapper in `TestEndToEndBashInteractiveContextUseAndClear`; one mutant proof per stage.

## Mutant proofs (blocker 4), live, one at a time

- Mutant A (wrapper `export BASEHARBOR_TARGET` line removed): `TestEndToEndBashInteractiveContextUseAndClear` RED (`AFTER_IS=<empty>`). Restored.
- Mutant B (interactive guard `[[ $- == *i* ]]` removed): `TestInteractiveGuardPresent` RED. Restored.
- Mutant C (wrapper `command baha` recursion guard broken): `TestEndToEndBashInteractiveContextUseAndClear` RED. Restored.

## CI run observing (r2)

- Run **44712300731** (event pull_request, head d1ec4b72): **completed | success**.
- Full context/completion suite green; coverage/docs/gofmt/DE-integrity/documentation-audit all PASS.

## Owner clarification ruling 2026-11-20 (second round)

- FRAGE 1 (wrapper file): DER WRAPPER GEHOERT IN NEUE DATEI `cmd/baha/context_hook.go`. r2 (d1ec4b72) currently lives the wrapper body in `completion_setup.go:41-104` + wiring in `completion.go:203-270`. Compliance move: relocate `contextWrapperBody`/`contextInteractiveInstall`/`contextHookInstalled` + marker consts to new `cmd/baha/context_hook.go`; keep `activationSnippet` in `completion_setup.go`. New file, no `commands.go` touch, no `.github/**` — no boundary violated.
- FRAGE 2 (shell name `baha`): NO Go-side symbol conflict. `grep` confirms no Go function named `baha` (only `rootCommand` + unrelated `bahaLoanContext`/`bahaTestIsolationMarkerPresent`/`bahaEffectiveBootTargetName`). Shell-level name `baha` is Shell-world, not Go. Answer: NEIN — `baha` stays.
- FRAGE 3 (subcommand collision): NEIN — the `context` family belongs to this card.

## Critical discrepancy for the Owner

The PR head moved from eff023c07810 (r1, frozen) to d1ec4b72 (r2) because the r2 correction WAS delivered and passed CI run 44712300731. The Owner's freeze instruction ("head frozen at eff023c07810, no push") assumed the correction had not yet been pushed. It was. The Owner now wants the wrapper relocated to `cmd/baha/context_hook.go`.

## Pending Owner direction

(a) accept d1ec4b72 as-is (already green), or (b) apply the `context_hook.go` relocation as a follow-up commit (new CI run). No further push without Owner confirmation.
