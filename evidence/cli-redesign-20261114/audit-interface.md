# Audit: CLI surface, dialogs, output formats, flags (IST-ZUSTAND)

Card: `t-20261114-r28-cli2-audit-interface` (0428-047) · Lane: `lane-0428-audit-interface`
Type: pure inventory (merge-frost, owner directive 2026-11-14). No product change, no PR, no release, no tag.
Inputs: [brief](brief.md), [command mapping](command-map.md), [code entry index](code-entry-index.md).

## PLAN

1. Claim leg: card published `active` with owner `lane-0428-audit-interface` on plan `origin/main`
   (`6b34b1d9`, coordinator). `python3 scripts/plan.py claim` refuses to re-claim an active card, so
   the claim requirement is satisfied by the published state; nothing was re-published.
2. Locate the authoritative planning repo and read the redesign inputs (brief, command-map, code-entry-index).
3. Pin product truth: `develop` = `0e9ccb582`, plus a clean persistent clone at exactly that SHA.
4. Inventory interactive/surface paths: wizard dialogs, output formats, global and per-command flags,
   completion / shell surface, exit codes, machine (JSON/MCP/HTTP) surface — each with file:line.
5. Judge each item against Core `AGENTS.md` and `docs/DEVELOPMENT_GUIDELINES.md` plus the owner brief
   decisions. Verdicts: `trifft` / `weicht ab` / `Konsistenz-Risiko`.
6. Cite external reference sources (context7 MCP, web search) for CLI-UX and MCP norms.
7. Deliver this dossier to `evidence/cli-redesign-20261114/audit-interface.md`, push to plan main,
   set the card to `review`, post END.

## 0. Zone and provenance witnesses

Wrong-zone guard (mandated one-liner):

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan rev-parse --show-toplevel
/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote get-url origin
https://github.com/mcpdev80/baseharbor-plan.git
```

`workers/baseharbor-plan` was never used. The quarantined `workers/baseharbor` checkout was never cited:
all product truth comes from `git ls-remote` on GitHub and from a fresh clone in this lane's own zone.

Base attestation:

```
$ git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor ls-remote origin develop
0e9ccb582f5bdcdc74049bbe3996263cdce6500c	refs/heads/develop
$ git -C /tmp/opencode/audit-interface-wt/core rev-parse HEAD
0e9ccb582f5bdcdc74049bbe3996263cdce6500c
$ git -C /tmp/opencode/audit-interface-wt/core merge-base --is-ancestor 0e9ccb582 HEAD; echo $?
0
```

The audited snapshot is exactly `origin/develop` at `0e9ccb582`
("chore: pin v0.4.27 demo acceptance (#1573)"). Clone method:
`git clone --no-checkout --filter=blob:none https://github.com/mcpdev80/baseharbor.git`
then `git checkout 0e9ccb582f5bdcdc74049bbe3996263cdce6500c`, in
`/tmp/opencode/audit-interface-wt/core`. The clone detaches at that SHA, so the ancestry test is
trivially satisfied (`0e9ccb582` is HEAD); no branch was cut and no PR was opened, per merge-frost.
All `file:line` references below were read from that snapshot and are reproducible with
`git show 0e9ccb582:<path>`.

## 1. Reference sources used

- Command Line Interface Guidelines, "Interactivity" and "Errors": prompt only when stdin is a TTY;
  `--no-input` must never prompt and must fail with an actionable message telling the user which flag
  to pass; never require a prompt; confirm before dangerous actions with an explicit non-interactive
  escape hatch. <https://clig.dev> (retrieved 2026-11-14 via web search).
- Model Context Protocol 2026-07-28, client elicitation and Multi Round-Trip Requests (SEP-2322,
  SEP-2260): a server may ask the client for input only while processing a request, returns an
  `InputRequiredResult` with `elicitation/create`, and MUST handle decline/cancel or a client that
  cannot interact. <https://github.com/modelcontextprotocol/modelcontextprotocol>
  (`docs/specification/2026-07-28/client/elicitation.mdx`,
  `docs/docs/2026-07-28/learn/client-concepts.mdx`, `docs/seps/2322-MRTR.mdx`), retrieved 2026-11-14
  through the context7 MCP server (`/modelcontextprotocol/modelcontextprotocol`).
- Bubble Tea v2 (the TUI framework in `go.mod`): `charm.land/bubbletea/v2 v2.0.9` plus
  `charm.land/lipgloss/v2 v2.0.6` and `github.com/charmbracelet/x/term v0.2.2`; the project
  therefore already owns a terminal-input-capable dependency that the raw line editors could use.
- Internal contracts used as the judgment basis: Core `AGENTS.md` ("Work and verify":
  "Mutations follow plan -> preflight -> apply -> verify; CLI, JSON and MCP share domain semantics.
  Preserve ownership, concrete consequence/consent checks and secret protection.") and
  `docs/DEVELOPMENT_GUIDELINES.md` §6 (secrets never enter normal data paths), §8 (one lifecycle),
  §9 (CLI/JSON/MCP share one semantic core), §12 (source readability limits).

## 2. Surface inventory: routing, help, errors, exit codes

| # | Item | IST-ZUSTAND (file:line at 0e9ccb582) | Contract check | Verdict |
| --- | --- | --- | --- | --- |
| 2.1 | Command tree, no declarative flag schema | `internal/cli/cli.go:20-31` (`Command{Name,Hidden,Aliases,Summary,Usage,Long,Examples,Run,Children,HelpGroups}`); routes positionally at `internal/cli/cli.go:94-135`; every command parses its own options inside `Run`; `cmd/baha/` holds 429 non-test Go files, `cmd/baha/commands.go:28-163` builds the root tree | Core `AGENTS.md` "CLI, JSON and MCP share domain semantics"; `DEVELOPMENT_GUIDELINES.md:74-78` §9 | `trifft` for semantics (machine surface is delegated to the same CLI `Run` funcs, e.g. `cmd/baha/mcp_lifecycle_extra.go:11-13`), but there is no machine-readable option schema behind the surface: option truth lives only in prose `Usage` strings plus scattered per-file parsers. This is what makes the drift in 2.2, 4.x and 5.x possible. | Konsistenz-Risiko |
| 2.2 | Unknown-option suggestions are reconstructed from the Usage string | `internal/cli/cli.go:204-214` `knownFlags()` = fixed global list + regex `--[A-Za-z0-9][A-Za-z0-9-]*\|-[A-Za-z]` over `c.Usage`; `cli.go:171-202` `decorateUsageError` adds a suggestion only when the message contains "unknown" and `NoSuggestions` is false; `cli.go:395-435` Levenshtein cutoff (commands distance <=2, flags <=3 then <=2) | brief line 7 "no interactive dead ends"; clig.dev "Errors" (tell the user what to pass) | `trifft` in shape. Consequence: any option that is parsed but absent from the Usage string is invisible to `--help`, to the suggestion engine and to completion. Verified misses: `baha app secret set` Usage `cmd/baha/app_secret.go:31` advertises no `--json` although `app_secret.go:33` calls `parseReadOutputArgs`, which accepts `--json` (`cmd/baha/output.go:23-24`) and honours it at `app_secret.go:59`. Same shape in `baha trust uninstall` (`cmd/baha/trust.go:164`), `baha target list` (`cmd/baha/target.go:173`), `baha node list` / `node status` (`cmd/baha/node.go:147-148`). | weicht ab |
