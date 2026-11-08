# Round 1 — baha up NAME alias-parity fix

- Task: `t-20261108-bughunt-0427-up-name-alias-parity` (card 0427-130), owner `lane-w130-upalias`
- Shift: r27-welle5-folge-2026-11-08
- Date: 2026-11-08
- Session model/backend: recorded at END

## PLAN

- Step 1: Fetch develop `07ae6c3e9`, verify planning repo + product remote HEAD
- Step 2: Claim task via central protocol
- Step 3: Reproduce IST bug — `baha up NAME` rejected, `baha app up [NAME]` works
- Step 4: Fix — align `cmd/baha/runtime.go` `up` parser with `app up` (`cmd/baha/app_lifecycle.go`): accept optional positional NAME + identical resolution; no consent-semantics change; do NOT touch `orgconfig/profiles.go`
- Step 5: Add parser parity test to existing cli-surface/selected group (no new CI framework)
- Step 6: Regression — `go test ./cmd/baha/` + `go vet`, document which CI job/trigger covers it
- Step 7: Docs line if alias surface is documented
- Step 8: PR against develop, watch CI to terminal, ls-remote + cleanliness

## Ground truth (reality witnesses)

- Planning repo: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` (NOT `workers/baseharbor-plan`, which points at `baseharbor.git` and is quarantined).
- `git remote -v` on planning repo:
  - `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`
  - `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`
- Product repo: `/home/marcel/dev/baseharbor-ecosystem/baseharbor`
- `git ls-remote origin develop` => `07ae6c3e91b081a189266ca4b162ba705d4aa78f  refs/heads/develop` — exactly the mission's target commit. Local `develop` matches.
- Base SHA cut-from: `07ae6c3e91b081a189266ca4b162ba705d4aa78f` (develop) — shown as ancestor of first commit.

## IST repro

- Reproduced with a build from clean `develop` at `07ae6c3e9`.
- Command: `baha up somedeployment --yes --skip-memory-preflight` (outside a repo):
  - Output: `Error: unknown option somedeployment` / `Next: Run 'baha up --help' for usage.`
  - `baha app up somedeployment` accepts the positional NAME (parser `parseAppUpOptions`, `cmd/baha/app_lifecycle.go` lines 18-37).
- Root cause: top-level `up` registered in `cmd/baha/commands.go` line 79 -> `runtimeUpCommandWithInputResolver` -> `parseRuntimeUpOptions` had NO positional-NAME handling; every non-flag token hit `unknownOptionUsage`. The NAME was never threaded to `resolveApplication` (called with `nil` at `app_input_resolver.go:526` and `runtime_repository_up.go:46`).

## Fix

- `cmd/baha/runtime.go`:
  - Added `Name string` to `runtimeUpOptions`.
  - Rewrote `parseRuntimeUpOptions` to accept an optional positional NAME (mirrors `parseAppUpOptions`: first non-flag becomes `opts.Name`, a second NAME -> `usageError("baha up accepts at most one NAME")`, leading `-` -> `unknownOptionUsage`). Flag/`--flag=value` semantics unchanged; consent semantics unchanged.
  - Added `upNameArgs(name string) []string` helper returning `nil` (resolve by directory) or `[]string{name}`.
  - Threaded `opts.Name` via `upNameArgs` into both `resolveApplication(..., "up")` sites.
- `cmd/baha/commands.go`: added `[NAME]` to the `up` Usage string (documents the alias surface).
- NOT touched: `orgconfig/profiles.go` (drift guard), consent semantics, CI workflow files.

## Tests (added to existing cli-surface/selected group — no new CI framework)

- `cmd/baha/runtime_ports_test.go`:
  - `TestParseRuntimeUpOptionsAcceptsOptionalName` — `up NAME` parses, `opts.Name` set.
  - `TestParseRuntimeUpOptionsRejectsSecondName` — two names -> error.
  - `TestParseUpParsesIdenticalToAppUpEnforcesParity` — machine/CLI grammar parity: `up` and `app up` accept identical flag/argument grammar and resolve the same NAME.
- CI coverage: these live in the `cmd/baha` unit-test group. Which workflow file runs the `cmd/baha` unit group and under which trigger is a CI-group ownership question — if the trigger/selection rule must change, that is an Owner scope change under `.github/**`; report here rather than editing: state job + trigger in the evidence after CI runs.

## Regression / verification

- `go build ./cmd/baha` — OK.
- `go vet ./cmd/baha/...` — clean.
- `go test ./cmd/baha/ -run 'Runtime|Up|Parser|Parse|Completion|Grammar|Human|Canonical'` — PASS (all runtime/parser/parse/grammar/completion/human/canonical tests green, incl. new parity test).
- Full `go test ./cmd/baha/` suite: long-running; reported after completion.
- `baha up --help` after fix shows `Usage: baha up [NAME] [-e ENV|...`.
- `baha up somedeployment --yes --skip-memory-preflight` now returns `Error: inspect repository: repository inspection size limit exceeded` (a `/tmp` directory-size artifact, NOT a parser rejection) — proves the NAME is accepted end-to-end.

## CI (run 42461878643 on SHA `fecfbabc7`)

- Draft-PR gate jobs: `PR · Source format` **success**, `Workflow policy` **success**, `PR · Trusted Plan` **success**.
- Standard CI: `PR · cli-gofmt` **success**; `PR · Selected Runtime` **skipped** (no runtime-provider path touched — correct scope selection).
- Validation in progress: `PR · Validation · go-vet`, `go-unit-tests`, `go-build`, `PR · Focused Python` — observed running.

## Docs

- `docs/` has no `baha up [NAME]` usage line overriding the CLI Usage string; the CLI Usage is now the source of truth. No docs edit required beyond the Usage string already updated. (If a docs section documents the alias surface without `[NAME]`, note file:line.)

## Repo-rule compliance

- Wrote only within owned files: `cmd/baha/runtime.go`, `cmd/baha/commands.go`, `cmd/baha/runtime_repository_up.go`, `cmd/baha/app_input_resolver.go`, `cmd/baha/runtime_ports_test.go`.
- Did not touch `orgconfig/profiles.go` (drift), consent semantics, or `.github/**`.
- No subagents used (Owner directive 2026-11-04); all steps executed in this session.
- No runner infrastructure built/registered/repaired (GitHub-hosted shared runners only).

## END status

- Lane: 0427-130-upalias
- Status: IN PROGRESS — fix + parity test implemented and locally verified; PR against develop pending.
