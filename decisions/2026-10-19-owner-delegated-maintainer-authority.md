---
id: 2026-10-19-owner-delegated-maintainer-authority
status: accepted
sources: []
---

# Owner-delegated Maintainer authority

## Decision and authority

On2026-10-19 Marcel explicitly directed that his authorized agents operating through @mcpdev80 may exercise his repository Maintainer authority, including acceptance and merge, without another repository reviewer or repeated confirmation. This standing delegation applies within the actual Owner-assigned scope, including an authorized agent's own implementation. It supersedes earlier repository review-only handoff/stop requirements for those delegated actions. Ordinary contributors and workers without delegated Maintainer authority retain their normal review handoff.

## Execution

Use the existing regular PR merge and account-level review exception. Record the actual Owner mandate, exact candidate, executed checks and merge result. Owner acceptance is valid repository authorization; it must not be mislabeled an independent technical review or fabricated GitHub self-approval. The grant does not transfer unrelated protected claims or authorize unrequested releases, credential disclosure or unrelated destructive work.

Live GET ruleset23754541 permits User22537373 pull_request bypass for the integration/review rules. Separate ruleset25223521 enforces strict PR Selected Checks from integration15368 without bypass. These live technical rules were not changed by this decision. This repository policy does not claim to override separate tool/platform permissions or replace missing execution evidence.

## Implementation

[Assigned policy task](../tasks/t-20261019-owner-delegated-maintainer-authority.md) updates product development guidelines and agent entry point plus the historical/current enforcement distinction, then uses actual selected documentation CI and regular merge. Planning entry points adopt the delegation immediately from this explicit Owner instruction. Product branch/worktree ownership, source fixes and mandatory runtime proofs remain unchanged.

After every actual acceptance/merge, publish canonical status/evidence and regular generated Planning/Obsidian views; do not leave a completed task open or represent an unexecuted native test as successful.
