---
id: t-20261114-r28-cli-command-semantics
card_number: "0428-043"
card_short_title: "harmonize human CLI semantics"
type: task
areas: [cli, architecture, documentation]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Make BaseHarbor's human CLI predictable for Linux developers before WSL2 and macOS work relies on that interface. Commands must…"
kanban_title: "0428-043 · harmonize human CLI semantics"
priority: high
depends_on: [t-20261017-release-0-4-28-updates, t-20261114-r28-cli2-final-acceptance]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261114-r28-cli-command-semantics · v0.4.28 · CLI: harmonize command semantics before platform adapters #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/architecture #area/cli #area/documentation #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261114-r28-cli2-final-acceptance](t-20261114-r28-cli2-final-acceptance.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261017-release-0-4-28-updates](t-20261017-release-0-4-28-updates.md), [t-20261114-r28-cli2-final-acceptance](t-20261114-r28-cli2-final-acceptance.md)  
**Required by:** [core-821](core-821-wsl2-host-behavior-windows-boundaries.md), [core-822](core-822-macos-darwin-adapters.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Make BaseHarbor's human CLI predictable for Linux developers before WSL2 and macOS work relies on that interface. Commands must state clearly what resource they act on, which Target they select, and what a destructive action removes.

## Split implementation coordination

The owner requested five parallel workers, one coordinator and Codex/Owner-delegated Maintainer acceptance. The bounded `t-20261114-r28-cli2-*` cards hold the audit, contract, implementation and final acceptance chain. This umbrella cannot be accepted until `t-20261114-r28-cli2-final-acceptance` has actually completed; release startup remains mandatory. Owner decisions and still-proposed names are recorded in [the working brief](../evidence/cli-redesign-20261114/brief.md). Existing platform dependents continue to depend on this umbrella.

## Scope and acceptance

- Inventory every shipped `baha` command and subcommand from parser/registration source; record resource, scope, Target/environment defaults, mutability, consent and next-step guidance.
- Define one understandable command grammar for application, Target, user, workstation and installation lifecycle. Resolve inconsistencies around implicit `dev`, selected Targets, `app init`/`up`, `stop`/`destroy`, and local versus remote cleanup.
- Preserve explicit Target selection, active-Target display and shell completion, native local Docker/Podman support, JSON/MCP semantics, ownership, authorization, impact consent and no-local-fallback behavior.
- Implement the agreed changes in small PRs; retain compatibility aliases where safe and document removals/migrations explicitly. Do not change provider contracts or add macOS/WSL runtime behavior in this task.
- Update EN/DE help, CLI references, completions and human workflows from the actual parser. Add positive invocation/help checks and safety-relevant negative coverage for each changed command.
- Complete this command contract before `core-821` WSL2 and `core-822` macOS behavior begins; both platform tasks depend on this card.

## Required checks

Parser/help golden coverage, generated shell-completion tests, CLI/JSON/MCP semantic parity, exact local and remote lifecycle regressions for changed commands, source/readability audit, strict EN/DE docs and documentation audit. Route each changed test through existing focused CI selection; use native runtime tests only where command behavior changes runtime execution.

## Dependencies and file ownership

Follows v0.4.28 dependency intake. Owns the CLI inventory/spec, parser/help/completion and matching EN/DE CLI docs. Coordinate shared parser or generated-doc changes with the current owner; retain existing interfaces until migration is explicit.

## Handoff

Scheduled by Maintainer direction on 2026-11-14. Implementation has not started. Console and Node Connector are archived/paused and outside this task.
