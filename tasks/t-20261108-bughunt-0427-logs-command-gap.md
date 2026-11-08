---
id: t-20261108-bughunt-0427-logs-command-gap
card_number: "0427-131"
card_short_title: "logs top-level ohne Pfad"
type: bug
areas: [dx]
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-w131-logsgap-r2
kanban_status: closed
kanban_lane: closed
kanban_summary: "The logs entry point is coherent: either baha logs works top-level (resolving the nearest app) or the error names the correct…"
kanban_title: "0427-131 · logs top-level ohne Pfad"
priority: low
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1456]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/bughunt-logs-gap/round-2.md","https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/bughunt-logs-gap/act-1456-review-r2.md"]
---

- [x] t-20261108-bughunt-0427-logs-command-gap · Bug Hunt v0.4.27: logs top-level ohne Pfad #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/dx #kind/bug
    <!-- generated:card -->
    **Owner:** lane-w131-logsgap-r2 · **Priority:** low  
    **PR:** [baseharbor#1456](https://github.com/mcpdev80/baseharbor/pull/1456)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/bughunt-logs-gap/round-2.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/bughunt-logs-gap/act-1456-review-r2.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** lane-w131-logsgap-r2  
**Priority:** low  
**PRs:** [baseharbor#1456](https://github.com/mcpdev80/baseharbor/pull/1456)  
**Source:** 
<!-- /generated:links -->

## Outcome and acceptance

The logs entry point is coherent: either `baha logs` works top-level (resolving the nearest app) or the error names the correct command (`baha app logs`) instead of an unrelated 'login' suggestion.

## Problem (bug-hunt intake 2026-11-08, verified before carding)

BF4 docker2 hunt dossier (evidence/r27-welle5-folge-2026-11-07/vm-bughunt/docker2.md lines 57-63): `baha logs` -> unknown command with "Did you mean 'login'?"; `baha app logs` behaves correctly. TEILSTAND UX inconsistency, previously uncared.

## Acceptance

- Cobra suggestion for `baha logs` points at `baha app logs` (or working alias); regression covers the suggestion text in the existing CLI-surface CI job.

## Dependencies and file ownership

Umbrella only; write-set cmd/baha root command wiring + docs/command-index line.
