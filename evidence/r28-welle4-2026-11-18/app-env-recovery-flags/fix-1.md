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
- Docs audit: `bash scripts/documentation-audit.sh` green (structure/parity/integrity/language audit all PASS). This script is invoked by the repository's normal CI; it covers the affected EN/DE docs path.

## Runtime witness (built from 8dccd4fe1, in /tmp/117-envflags-probe, no baseharbor.yaml)

```
$ /tmp/117-envflags-baha app env foo --uuid abc123
Error: unknown option --uuid
Next:
  Run 'baha app env --help' for available options.
  Did you mean '--quiet'?
rc=2

$ /tmp/117-envflags-baha app env foo -e dev
Error: unknown option -e
Next:
  Run 'baha app env --help' for available options.
  Did you mean '-h'?
rc=2
```
Confirmed: `app env` selects by NAME and rejects `--uuid`/`-e` — exactly what the rewritten passage states.

## repo-rule compliance

- Docs-only change. No behavior change, no flag wiring into `app env`. No `.github/**` touched. No runner infrastructure. No container/compose. No subagent (self-run duty). Worktree under `/tmp`, caches under `/tmp`. Evidence committed only in baseharbor-plan.

- In progress: source witness captured, base attested at 8dccd4fe1, PR #1687 open.

## CI result (terminal, self-run)

- Run: `gh run list --repo mcpdev80/baseharbor --branch lane-0428-117-envflags-doc` → run #6501, workflow **CI · Source & Quality**, status `completed`, conclusion **success**, headSha `7aa8b01e97a425e30cdfc069206f35ac822bca82`, createdAt 2026-11-18T22:43:38Z, updatedAt 2026-11-18T22:45:00Z.
- This run covers the affected path (docs audit + Go unit suite incl. machine-docs consistency + CLI parsing). Trigger: pull_request on base develop.
- PR #1687 on base develop; merge left to the acceptance step (not performed in this lane).

## CI / trigger mapping (durable evidence)

- Docs audit (`bash scripts/documentation-audit.sh`) plus `go test ./cmd/baha/...` (machine-docs consistency, CLI parsing, app-env argument handling, duplicate-resolution/`--uuid`) run under the repository's normal branch CI on a push of this lane's PR to `develop`. Trigger: pull_request on base develop.
- No `.github/**` file was edited (Owner scope). The coverage of the affected docs path is already in the existing docs/CI group; no CI change is required to pick up this docs-only change.
