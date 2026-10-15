---
id: 2026-10-15-stable-task-ids
status: proposed
sources: []
---

# Stable task IDs without a shared counter

## Context

Concurrent sessions must be able to create tasks without colliding, so "highest number plus one" is unsafe.

## Decision

- Migrated items keep their source identity: `core-<n>`, `demo-<n>`, `console-<n>`, `nc-<n>` for baseharbor, baseharbor-demo, baseharbor-console and baseharbor-node-connector. When one source is split, the parts get a suffix (for example `core-893-interface`).
- New tasks use `t-<YYYYMMDD>-<slug>` (created with `scripts/plan.py new`); the slug makes collisions unlikely and the file name makes any remaining collision a visible Git conflict.
- File names start with the ID; the ID never changes after creation, even if the title does.
- Decisions use `<YYYY-MM-DD>-<slug>`.

## Consequences

IDs are readable on cards and in commit messages, and no coordination is needed to create one.
