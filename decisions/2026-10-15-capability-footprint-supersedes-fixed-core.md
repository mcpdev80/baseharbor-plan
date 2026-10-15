---
id: 2026-10-15-capability-footprint-supersedes-fixed-core
status: accepted
sources: []
---

# Requested capabilities, not a fixed Core bundle, define the footprint

## Context

Older sections state "BaseHarbor Core = SQL + Secrets + Identity" and treat Identity as a mandatory Core capability: baseharbor#777 ("Core capability consistency"), #174 ("Core definition acceptance" and "Managed-provider lifecycle truth: Core SQL + Secrets + Identity"). The binding #872 correction, repeated in #155 and #427 (2026-10-11), says: no unconditional SQL/Secrets/Identity bundle; the provider footprint follows requested capabilities and genuine dependencies; a zero-capability application runs without any Core container.

## Decision

Apply the later #872 correction. Keep the still-valid part of the older text: mandatory capability does not imply mandatory shared placement, and shared and application-isolated placement use the same provider-neutral semantics. The affected notes ([core-777](../epics/core-777-developer-access-and-profiles.md), [v0.4.31](../releases/v0.4.31.md)) mark the conflict.

## Consequences

Confirmed during the migration review on 2026-10-15: apply the already binding #872 correction. Optional management services retain their actual security and dependency requirements; no unconditional SQL/Secrets/Identity bundle is reintroduced. This decision preserves existing product semantics rather than defining a new contract.
