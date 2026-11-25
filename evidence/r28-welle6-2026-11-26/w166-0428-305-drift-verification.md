# w166-0428-305-drift-verification: H-V34 CLI doc-drift re-verify on develop a87da7d17

- Lane: w166-0428-302-coverage-rows
- Card: t-20261125-hunt34-cli-docs-drift (0428-305) — "3 doku findings: stale examples/flags in docs/reference/cli.md per akte rows; docs-only fix"
- Status: END_DONE — all 3 drift spots RE-VERIFY as FALSE POSITIVES on a87da7d17. No doc change required; card dropped.

## Base attestation

- Planning repo remote (first action): `origin https://github.com/mcpdev80/baseharbor-plan.git` (fetch), `origin https://github.com/mcpdev80/baseharbor-plan.git` (push).
- baseharbor real GitHub remote: `origin https://github.com/mcpdev80/baseharbor.git` (confirmed via `git remote -v`; no local-filesystem origin in this checkout).
- Base develop (ls-remote + fetch, fresh): `a87da7d179e08d43e8987885c38ab459ff1d887d refs/heads/develop`.
- Branch cut: `lane-0428-305-cli-docs-drift` at `a87da7d179e08d43e8987885c38ab459ff1d887d`; `git merge-base --is-ancestor origin/develop HEAD` = develop IS ancestor; `git log --oneline origin/develop..HEAD` = empty (no commits; false-positive disposition, no product/doc change).
- Git identity: `user.name=w166-0428-302-coverage-rows`, `user.email=w166-0428-302-coverage-rows@baseharbor.local` (card frontmatter owner EXACT; verified).
- Binary ground truth: `go build -o /tmp/baha-305 ./cmd/baha` (go1.26.8), driven against the a87da7d17 tree.

## Method

For each H-V34 doku row: read the doc claim on develop a87da7d17, build the binary, drive real `baha <cmd> --help` as ground truth, and grep the exact file:line witness. All three rows were found on the stale H-V34 anchor `f7540e591609e0db6453e9b690fbb5d6686448a2` (confirmed an ancestor of a87da7d17 — i.e. predates now).

## Finding 1 (H-V34 BF-01): `baha app show` is NOT a real subcommand — FALSE POSITIVE on a87da7d17

- Doc claim (docs/cli/applications.md line 18): `| baha app show | Show the resolved application contract |`.
- Witness (binary, a87da7d17): `/tmp/baha-305 app show --help` -> `show - Show a coherent application overview` (exit 0, real subcommand).
- Witness (binary, a87da7d17): `/tmp/baha-305 app --help` lists `show  Show a coherent application overview` in the subcommand table.
- Resolution: the ghost-command drift H-V34 saw against the f7540e59 tree is resolved; `app show` parses and appears in `app --help` on a87da7d17. No doc change required.

## Finding 2 (H-V34 BF-02): `--json` not universally valid — doc already canonicalized on a87da7d17

- Doc claim (H-V34): Applications.md / command-index mix `-o json`, `--output json` and `--json`; doc examples assume `--json` works everywhere.
- Witness (binary, a87da7d17): `baha app env [NAME] [--format dotenv|shell|json|yaml]` — canonical flag is `--format`, with `json` as one accepted value. `/tmp/baha-305 app env foo --format json` parses (rejects only the unknown NAME, not the flag); `/tmp/baha-305 app env foo --json` -> `unknown option --json`.
- Resolution: the JSON flag contract is now documented and implemented as `--format <dotenv|shell|json|yaml>`; the loose `--json`-everywhere framing H-V34 saw is stale. No doc change required (the canonical flag is already the source of truth).

## Finding 3 (H-V34 BF-03): EN lacks the machine-generated command-index.md that DE ships — FALSE POSITIVE on a87da7d17

- Doc claim (H-V34): `docs/cli/` has no `command-index.md`; only `docs/de/cli/command-index.md` exists.
- Witness (a87da7d17): `docs/cli/command-index.md` EXISTS (197 lines), header line 3: `Entries are generated from the shipped command tree.`; line 7 references `[JSON/MCP mapping](../reference/cli-machine-coverage.md)`.
- Witness (a87da7d17): `docs/de/cli/command-index.md` EXISTS (197 lines).
- Witness (parity): `diff <(grep -vE '^\s*#' docs/cli/command-index.md) <(grep -vE '^\s*#' docs/de/cli/command-index.md)` differs only in DE prose headers; command table bodies are identical.
- Resolution: EN command-index parity is already in place and regenerated from the shipped tree. No doc change required.

## Cross-check: subcommands H-V34 BF-05 listed as missing are present on a87da7d17

- Witness (binary): `app pull`, `app update`, `app tls`, `app sql`, `app cache` all parse (`--help` exit 0). `app --help` full subcommand table also lists `secure-profile`, `export`, `logs`, `shell`, `exec`, `perses`, `status`, `doctor`, `down`, `stop`, `destroy`.
- Resolution: the tables H-V34 called non-exhaustive now cover the shipped subcommands; no doc change required.

## Why H-V34 saw drift

H-V34 ran on develop anchor `f7540e591609e0db6453e9b690fbb5d6686448a2` (ls-remote). That anchor is an ancestor of a87da7d17 (`git merge-base --is-ancestor f7540e59... a87da7d17` = true). The `app show`/`app pull`/`app tls`/`app sql`/`app cache` subcommands, the EN command-index parity row, and the canonical `--format json` flag were added on a later develop (e.g. `0428-061` app pull #1752, `0428-062` app status/versions #1614, `0428-063` logs/exec/urls #1623). On a87da7d17 all three drift rows are already correct.

## repo-rule compliance

- Read-only desk + build against a87da7d17; no product code changed; no flag renames; no `cmd/` changes.
- No `.github/**` edits; no workflow triggers; no runner changes.
- Evidence written ONLY to baseharbor-plan evidence path (below); no writes to any product repo.
- No candidate commit exists (false-positive disposition): `git diff a87da7d17..HEAD --name-only` empty.

## cleanliness

- `docker ps -a` before: header only. `docker ps -a` after: header only.
- No containers/compose started; `docker ps -a | wc -l` unchanged. No podman run.
- cleanliness: read-only desk + one `go build`, zero runtime started, no orphaned resources.

## END

w166-0428-302-coverage-rows END_DONE — 3/3 H-V34 doc-drift rows re-verified FALSE POSITIVE on a87da7d17 (app show parses; --json canonicalized to --format json; EN/DE command-index parity already present). No doc change required. Card 0428-305 dropped. Branch lane-0428-305-cli-docs-drift at a87da7d17, no commits, no product/doc change.
