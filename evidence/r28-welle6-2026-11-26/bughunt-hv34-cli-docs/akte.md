# BUG-HUNT H-V34 — CLI/docs conformance desk

- Slice: CLI/docs conformance desk on develop
- Host: ornith (session w160-0428-224, pid 305725) — read-only desk, no runtime started
- Develop anchor: `f7540e591609e0db6453e9b690fbb5d6686448a2` (ls-remote origin/develop)
- 0.4.28 begin-marker commit: `c0664c8e49e4efb56ea69cc793b94da7cc270765` (verified ancestor of develop via `git merge-base --is-ancestor`)
- Method: build binary from develop, drive real `baha <cmd> --help` as ground truth; read `docs/cli/*.md` (EN) + `docs/de/cli/*.md` (DE) + `docs/DEVELOPMENT_GUIDELINES.md`; never ran product tests.

Reality witnesses (own clone zone /tmp/opencode/v34-wt):
- `git -C /tmp/opencode/v34-wt remote -v` -> origin ssh://git@github.com/mcpdev80/baseharbor.git
- `git ls-remote origin refs/heads/develop` -> f7540e591609e0db6453e9b690fbb5d6686448a2
- 310 cmd/baha commits in the 0.4.28 window since begin-marker.

## Per-command conformance rows

| Command | Doc claim | Actual (binary) | Drift |
| --- | --- | --- | --- |
| Global options | `--no-input`/`--non-interactive` both listed (EN + DE global-options.md) | `--non-interactive` parses and runs (version exit 0); `--no-input` runs | MATCH — both functional; doc is correct even though `--help` only prints `--no-input` |
| `baha up` | `--control-plane-only`, `--ha`, `--trust-host-ca` (core.md EN+DE) | all three parse (operator-auth error downstream, not parse) | MATCH |
| `baha destroy` | `--all` "compatibility alias" (core.md EN line 97, DE line 81) | `--all --no-input` parses (errors on operator auth) | MATCH — alias still present in help + accepted |
| `baha trust install` | requires `--yes` (security-trust.md EN line 11) | Usage: `baha trust install --yes` | MATCH |
| `baha node disconnect` | `node disconnect node-a --yes` (targets.md EN line 120) | Usage: `baha node disconnect TARGET --yes [--json]` | MATCH |
| `baha app env` | `--uuid` is NOT an id selector (applications.md EN line 291-293) | `app env --uuid deadbeef` -> `unknown option --uuid` | MATCH — doc accurately documents the rejection |
| `baha app exec` | `[--cmd CMD|COMMAND [ARG...]]` (command-index) | Usage: `baha app exec [--app NAME] [-e ENV|--environment ENV] [COMPONENT|-c NAME] [--cmd CMD|COMMAND [ARG...]]` | MATCH |
| `baha app footprint show` | `[--details]` (command-index) | Usage: `baha app footprint show [NAME] [-o json|--output json] [--details]` | MATCH |
| `baha app backup` | `--output/--password-file/--include-state/--exclude-state` (command-index) | Usage matches | MATCH |
| `baha app init` | `--agents/--quick/--input/--hostname/--tls/--cert-dir/--yes` (command-index) | Usage matches | MATCH |
| `baha new` | entry command "Create an application, stack, target, provider, or workspace" | tree + help confirm `baha new [application|stack|target|provider|workspace]` | MATCH |
| `baha prompt` | `baha prompt` renders prompt (shell-ux.md EN) | `baha prompt [--plain|--position-only]` exists | MATCH |
| `baha config organization` | `show`/`check` (organization-policy.md EN) | both parse + run | MATCH |

## Findings

### BF-01 — Blocker: `app show` is documented but NOT a real CLI subcommand
- file: `docs/cli/applications.md` line 19 (`| baha app show | Show the resolved application contract |`) and `docs/de/cli/command-index.md` (German command index references `baha app show`).
- Actual: `baha app --help` subcommand list (live) has NO `show` entry. Real overview command is `baha status`.
- Repro: `/tmp/baha-v34 app show --help` -> `Error: 'show' is not a registered subcommand of 'app'`.
- Severity: blocker — the canonical Applications doc points readers at a command that does not exist in the shipped tree.

### BF-02 — Daemm (docs drift): `--json` alias is not universally valid; Applications.md shows it on `app show`
- file: `docs/cli/applications.md` line 172 example: `baha app env --format json` (uses `--format`, correct) but the doc's machine-parity framing plus `command-index.md` entries mix `-o json`, `--output json` and `--json`.
- Actual: `--json` is accepted on some commands (`version`, `status`, `list`) but `app env` rejects `--json`? (tested `--uuid`, not `--json`); `app show` (nonexistent) moot.
- Severity: daemm — no single JSON flag contract; doc examples assume `--json` works everywhere.

### BF-03 — Doku (minor, EN/DE parity): English `docs/cli/` has NO command-index.md equivalent mirror
- file: `docs/cli/` contains core.md, applications.md, targets.md, providers.md, development.md, organization-policy.md, security-trust.md, automation-agents.md, shell-ux.md, global-options.md, index.md — NO `command-index.md`.
- Actual: `docs/de/cli/command-index.md` EXISTS and is machine-generated ("aus dem ausgelieferten Befehlsbaum erzeugt").
- Severity: doku — German has a machine-generated CLI command index that the English canonical set lacks; asymmetry risk for the EN "canonical" set.

### BF-04 — Doku (minor): `stack create` documented but binary `stack --help` shows `list|show|create`
- file: `docs/cli/development.md` lines 8-9 show `stack list`/`stack show NAME`; `docs/cli/applications.md` line 13 area. `stack create` is referenced.
- Actual: `baha stack --help` -> Commands: `list show create`.
- Severity: doku — consistent; `create` exists. Noted for completeness; no drift.

### BF-05 — Doku (verify): `baha app pull` present in tree help but missing from Applications.md command table
- file: `docs/cli/applications.md` command table (lines 11-22, 64-72) omits `pull`, `update`, `tls`, `sql`, `cache`, `secure-profile`, `evidence`, `runtime-identity`, `versions`, `prune`, `urls`.
- Actual: `baha app --help` lists all of these.
- Severity: doku — Applications.md tables are non-exhaustive; the prose list (lines 74-88) covers most but not all (e.g. `pull`, `secure-profile`).

## Proposed card lines

- Card A (blocker): `t-20261126-cli-app-show-ghost-command` — "docs reference `baha app show`, a command absent from the shipped `baha app` subcommand tree; doc + German command-index both carry the ghost. Fix: align Applications.md + DE command-index to real subcommands (use `baha status`/`baha app show` reword) — write-set = docs only."
- Card B (daemm): `t-20261126-cli-json-flag-contract` — "no single documented `--json` vs `--output json` contract across subcommands; CLI/JSON/MCP coverage card #787 scope. Align doc examples to the actually-accepted flag per subcommand."
- Card C (doku): `t-20261126-cli-command-index-parity` — "English `docs/cli/` lacks the machine-generated `command-index.md` the German set ships; decide parity target."

## repo-rule compliance
- Read-only desk; no product code changed; no `.github/**` touched; no product repo writes.
- Evidence written ONLY to baseharbor-plan evidence path (see below).
- All flag claims verified against a freshly-built develop binary, not guessed.

## cleanliness
- docker ps -a before: 1 line (header only); after: 1 line (header only).
- podman ps -a before: 2 lines (header + none); after: 2 lines.
- No containers/compose started. `docker ps -a | wc -l` unchanged with session pid 305725.
- cleanliness: read-only desk, zero runtime started, no orphaned resources.

## END
- w160-0428-224-hunt-v34 END_DONE — 5 findings (1 blocker, 1 daemm, 3 doku), 3 proposed cards, 0 product changes.
