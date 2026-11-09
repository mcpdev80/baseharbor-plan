---
id: t-20261109-r31-cli-manpage-after-consolidation
card_number: "0431-008"
card_short_title: "CLI man page after consolidation"
type: task
areas: [cli, docs]
release: v0.4.31
version: ""
parent: v0.4.31
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Once the v0.4.31 CLI consolidation and final command ordering/hierarchy are complete and approved, deliver an installable,…"
kanban_title: 0431-008 · CLI man page after consolidation
priority: normal
depends_on: [t-20261017-release-0-4-31-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261109-r31-cli-manpage-after-consolidation · CLI: provide a man page after the final command organization #task #release/v0-4-31 #status/planned #view/waiting #board/planned #area/cli #area/docs #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-31-updates](t-20261017-release-0-4-31-updates.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.31](../releases/v0.4.31.md)  
**Depends on:** [t-20261017-release-0-4-31-updates](t-20261017-release-0-4-31-updates.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** [baseharbor#603](https://github.com/mcpdev80/baseharbor/issues/603), [baseharbor#846](https://github.com/mcpdev80/baseharbor/issues/846)
<!-- /generated:links -->

## Goal

Once the v0.4.31 CLI consolidation and final command ordering/hierarchy are complete and approved, deliver an installable, maintained `man baha` manual for the **shipped** CLI. Do not document a provisional command layout or prematurely freeze aliases.

## Sequencing

- **Start only after the final human CLI surface is accepted**, including the consolidated command names/groups, help output and task-oriented wizard routes (source scope core #603 / #846 and the v0.4.31 semantic acceptance).
- This card is `planned`, not `wait`: no work has started and no active worker is assigned.
- Finish before v0.4.31 release qualification/publication; coordinate documentation and packaging with the release owner.

## Scope

- POSIX man page for `baha(1)` with NAME, SYNOPSIS, DESCRIPTION, COMMANDS (hierarchical command groups and all shipped subcommands), OPTIONS, configuration/environment, examples, exit/error behavior, security/authorization notes and SEE ALSO as relevant.
- Consistent command order/names between `baha --help`, subcommand `--help`, official CLI docs and the man page.
- Source-controlled documentation and reproducible build (prefer generation from the same canonical CLI command metadata/help definitions to prevent drift; no duplicate manually maintained command registry).
- Package/install `baha.1` into the appropriate `man1` directory for supported Linux distributions/package channels; usable via `man baha` without relying on network access.
- Explicitly identify applicable platforms: man is a Unix/Linux documentation format; WSL2/macOS integration follows supported packaging and availability.

## Acceptance

1. Command names, hierarchy, examples and flags match the **final approved** v0.4.31 CLI (no legacy pre-freeze aliases introduced for documentation convenience).
2. `man baha` renders correctly and is installed by the supported package/distribution path; source and generated artifact are versioned/reproducible.
3. Automated CI checks generate/validate the man page and detect command/flag/help drift, including newly added/removed command groups; `mandoc`/equivalent lint when available.
4. Smoke proof for installed package or release candidate: `man baha`, command inventory parity and at least one documented task-oriented path validated against the CLI.
5. Security-sensitive and destructive flags are accurately documented (no hint suggesting bypass of approval, identity, or confirmation gates).
6. Evidence records the exact source commit, packaging mode, test output and relevant installation proof; mark accepted only after verified checks.

## Ownership boundaries

CLI command taxonomy and its tests belong to the CLI consolidation scope. This task documents and packages its final output, avoiding parallel command renames or `.github/**` edits without CI-owner coordination.
