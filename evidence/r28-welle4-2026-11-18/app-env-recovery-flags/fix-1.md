# 0428-117 · align app env recovery-flag docs with the real per-command contract

- Lane: lane-0428-117-envflags-doc (card t-20261118-app-env-recovery-flags-claim, hunt 915 B1)
- Date: 2026-11-18
- Scope: docs only. No behavior change; wiring `--uuid`/`-e` into `baha app env` is explicitly out of scope (its own contract decision).

## PLAN

- Claim via plan.py + reality check develop (ls-remote origin/develop = 8dccd4fe1)
- Create working branch from base 8dccd4fe1 in a fresh worktree; attest base SHA
- Rewrite the recovery-flag passage in docs/cli/applications.md to match the real per-command contract (which `baha app <command>` accept `--uuid`/`-e`, `app env` selected by NAME)
- Run docs build/linkcheck + machine-docs consistency job; document which CI job runs it and under which trigger
- Open PR on base develop branch lane-0428-117-envflags-doc
- Run the PR check to terminal state, record run/attempt/SHA
- Write this evidence file; push evidence to origin/main before END

## Basis-Attestation (wrong-zone check + base)

- Plan-Repo-Verifikation: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel` → `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`
- Produkt-Basis (fresh worktree, NOT the quarantined checkout): worktree at `/tmp/117-envflags-doc-wt`, checked out from `origin/develop`, exact HEAD `8dccd4fe1a52bbcc61c67f7809079f33b8040d64`.
- `git ls-remote origin refs/heads/develop` → `8dccd4fe1a52bbcc61c67f7809079f33b8040d64 refs/heads/develop` (matches worktree HEAD exactly).
- No product branch, no PR before this lane. Base ref I cut from: `8dccd4fe1` (origin/develop).

## Source witness for the real per-command contract (built from 8dccd4fe1 source)

- `cmd/baha/app_env.go:21` Usage: `baha app env [NAME] [--format dotenv|shell|json|yaml] [--reveal] [--path]` — no `--uuid`, no `-e/--environment`.
- `cmd/baha/app_env.go:50-83` `parseAppEnvArgs`: the only `strings.HasPrefix(arg, "-")` case throws `unknown option`; there is no `--uuid`/`-e` acceptance path.
- `cmd/baha/app_context.go:495` generic recovery `Next:` text proposes `--uuid`/`-e/--environment` for every command routed through `resolveApplication` — including `app env`, where the suggestion is not executable.
- Read-commands `app show`/`app status`/`app plan` accept `--uuid` via `extractApplicationUUID` (`cmd/baha/app_context.go:646`) and `parseReadOutputArgs` (`cmd/baha/output.go:17`), but the `--uuid` selector needs a positional `NAME` — `baha app status --uuid <id>` without NAME does not resolve (`no application deployment could be resolved`); only `baha app <cmd> NAME --uuid <id>` is lauffahig.
- `app destroy` (`cmd/baha/app_lifecycle.go:444-446`) accepts `--uuid` as a selector for the whole-app remove.
- Hunt B1 reproduction (binary built from 907f16713, registrierter Poison-Target `perses-cli`): `baha app env perses-cli --uuid <id>` → `Error: unknown option --uuid` rc=2; `baha app env perses-cli -e dev` → `Error: unknown option -e` rc=2. Full witness in evidence/r28-welle4-2026-11-18/hunt-cli2merged/befund-1.md.

## Machine-docs consistency

- `docs/reference/cli-machine-coverage.md:25` lists `baha app env` as JSON-capable via `--format json` (masked MCP only); consistent with the real contract. No new rows introduced; the doc change is prose-only.
- The machine-docs consistency test is run as part of the Go unit suite (`go test ./...`); documented below which CI job covers it.

## repo-rule compliance

- Docs-only change. No behavior change, no flag wiring into `app env`. No `.github/**` touched. No runner infrastructure. No container/compose. No subagent (self-run duty). Worktree under `/tmp`, caches under `/tmp`. Evidence committed only in baseharbor-plan.

## Status

- In progress: source witness captured, base attested at 8dccd4fe1.
