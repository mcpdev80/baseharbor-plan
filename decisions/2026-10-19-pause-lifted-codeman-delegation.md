---
id: 2026-10-19-pause-lifted-codeman-delegation
status: accepted
sources: []
---

# Maintainer pause lifted; operation moves to Codeman/Ornith/Codex

## Context

Marcel explicitly lifted the temporary handover pause recorded in
[2026-10-18-horde-codex-handover-pause](2026-10-18-horde-codex-handover-pause.md)
on 2026-10-19 and issued an autonomous development assignment for the approved
v0.4.26 backlog until verifiable pre-release readiness.

## Decision

- Development, merges and native tests are resumed under the standing rules of
  the affected repositories. The 2026-10-18 pause notice is ended by this
  coordinated resumption, as that decision itself required.
- Operational delegation moves from the Horde test setup to the Codeman
  coordinator model documented in the ecosystem-root `AGENTS.md`:
  Flash coordinates, at most three Ornith workers (`agentgateway/ornith15`)
  implement and test in isolated task branches, an independent Ornith worker
  performs the local review, and Codex 6.1 holds the final independent
  acceptance and then the regular maintainer closeout (merge plus planning
  publication) on explicit `ACCEPTED` with actual green mandatory CI.
- Existing claims, PRs, reviews and handoffs from the paused period are
  preserved and remain protected. Sessions previously named in claims
  (core-921 Session 1, #995 correction Session 2, Qwen native testing) retain
  their ownership; no silent takeover. An existing PR is continued by a new
  worker only with an explicit ownership release for that task.
- Correction budgets apply per stable root cause: after two failed correction
  attempts the task is documented, set back to blocked and the coordinator
  continues with independent executable work.
- The uncommitted Horde working-tree additions found in this repository on
  2026-10-19 (an `AGENTS.md` delegation block and the untracked `.agents/` and
  `.codex/` directories) were never part of `main`. They were preserved outside
  the vault as transition evidence and are not published; planning delegation
  rules remain those of this repository plus the ecosystem `AGENTS.md`.

## Consequences

- Ready-queue maintenance, handoffs and acceptance publishing continue per
  [WORKFLOW.md](../WORKFLOW.md). Planning authority is unchanged.
- No release, pre-release, tag or deployment follows from this decision alone;
  those remain separately authorized maintainer actions.
