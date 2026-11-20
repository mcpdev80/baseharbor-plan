---
id: t-20261120-r28-identity-dashboard-catalog-consumer
card_number: "0428-181"
card_short_title: "identity catalog consumer"
type: bug
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "The identity dashboard catalog added by 0428-078 has no production consumer; wire it to the real Perses export path or do not ship it."
kanban_title: 0428-181 · identity catalog consumer
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: [evidence/r28-welle4-2026-11-20/hunt-signals-103/round-1.md]
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261120-r28-identity-dashboard-catalog-consumer · Identity dashboard catalog has zero production consumers (P4 of review 1650) #task #release/v0-4-28 #status/planned
    <!-- generated:card -->
    **Owner:** unassigned  
    <!-- /generated:card -->

## Found by bug hunt H-103 (funded from card t-20261117-hunt-signals-103, AGENTS 3.3.5 finding-to-card duty)

CODEX-REVIEW of PR #1650 (evidence/r28-welle4-2026-11-20/codex-review-wave/1650-0428-078-r7.md, P4) found that git grep at the candidate head shows no production call site for PersesIdentityDashboardAvailability / identityDashboardCatalog - every use is inside the new tests. The reviewer states plainly: a test-only golden is not a release proof. 0428-078 asked whether to widen her write-set into internal/capability/perses_selection.go or internal/application/perses_runtime.go; the coordinator refused both (perses_selection.go is closed by owner ruling, and #1684 is live in perses_runtime.go), and shrank her PR to the predicate-only write-set the owner already ruled.

## Acceptance

1. Wire the catalog into the Perses provision/export path that actually runs, so a dashboard is emitted only for a verified current signal.
2. Byte/hash-stability proof against the pinned Perses schema or a real export (not a hand-written fixture).
3. If the catalog stays unwired for this release: remove it from the tree in a follow-up commit, and record that decision here so no dead 500-line package ships.

## Boundaries

internal/metrics/** plus the one call site in internal/application/perses_runtime.go or internal/capability/perses_selection.go needed to attach it. SEQUENCING: wait until 0428-083 (#1684) is merged, because it writes the same file; if it is still open, this card stays blocked - owner ruling 2026-11-20.
