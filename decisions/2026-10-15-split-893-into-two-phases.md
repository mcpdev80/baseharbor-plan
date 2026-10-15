---
id: 2026-10-15-split-893-into-two-phases
status: proposed
sources: []
---

# Represent baseharbor#893 as two phases

## Context

The binding 2026-10-15 correction in baseharbor#888/#893/#896 orders the work as #892 → #893 planning/execution interface → #896 isolated runners → #893 final runtime/evidence acceptance. A single #893 entry would either create a #893 ↔ #896 cycle or treat the partial interface (PR #930, not merged or qualified) as a completed prerequisite.

## Decision

Two entries share the source: [core-893-interface](../tasks/core-893-interface-agree-planning-execution-interface.md) (the agreed interface at an exact PR #930 commit) and [core-893](../tasks/core-893-ci-enforce-selected-pr-checks.md) (final integration and acceptance). core-896 depends on core-893-interface only; core-893 depends on core-896; core-895 depends on core-893.

## Consequences

core-893-interface is accepted only when the agreed interface SHA is recorded with evidence; an open draft PR does not count. The manifest records #893 with disposition `split`.
