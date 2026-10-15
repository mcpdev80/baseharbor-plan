---
id: 2026-10-15-planning-authority
status: proposed
sources: []
---

# Planning lives in baseharbor-plan after an approved cutover

## Context

Planning was spread over GitHub issues in four repositories (roadmaps, release umbrellas, epics, tasks) plus a GitHub Project. Local and cloud agents need one planning source that works without Obsidian or an MCP server.

## Decision

- After the Maintainer approves the cutover ([checklist](../migration/cutover-checklist.md)), human-readable Markdown in this repository is the planning authority for roadmaps, releases, epics, tasks, priorities, ownership, dependencies, decisions and handoffs. Obsidian is an optional interface.
- Code, PRs, reviews, CI, test artifacts, release evidence, tags and published releases stay in their product repositories.
- Migrated GitHub issue bodies and GitHub Projects stop being competing planning authorities; their discussions stay reachable through the `sources` links in each note.
- **Until the cutover is approved, the existing GitHub issues remain authoritative** and this repository is a migration candidate.

## Consequences

- Each task note keeps repository-qualified source links (`mcpdev80/<repo>#<n>`) and a lossless [source snapshot](../migration/source-snapshot/inventory.json).
- Product repositories link to this repository from their contributor/agent entry points (not from the product README).
- External bug/feature reports keep arriving as GitHub issues and are triaged into tasks here ([WORKFLOW.md](../WORKFLOW.md#intake-of-external-bugs-and-feature-requests)).
