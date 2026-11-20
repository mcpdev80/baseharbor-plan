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
