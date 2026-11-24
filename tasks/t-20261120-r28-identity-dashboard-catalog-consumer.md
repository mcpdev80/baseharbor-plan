---
id: t-20261120-r28-identity-dashboard-catalog-consumer
card_number: "0428-181"
card_short_title: "identity catalog consumer"
type: bug
areas: []
release: v0.4.28
version: ""
parent: ""
owner: w54-0428-181-export
kanban_status: blocked
kanban_lane: blocked
kanban_summary: ""
kanban_title: 0428-181 · identity catalog consumer
priority: ""
depends_on: [t-20261114-r28-perses-datasources]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1819]
sources: []
blocker: "EXACT-DIFF REVIEW finding (w54): perses_dashboard_provision.go:353 queries identity_selection_confirmed WITHOUT target/application/environment selectors; the exact series appears only at that line across develop/#1818/#1819 with NO producer in those trees; the positive test calls writePersesDashboardProjection DIRECTLY, bypassing the production eligibility filter + witness. So current #1819 is NOT secure-by-design / not target-bound. Secure+functional acceptance requires: (a) a REAL target-bound signal/query at :353, (b) an end-to-end test through persesDashboardProvisionForLifecycle (not a direct-projection bypass). Plus OWNER RULING on target binding. #1819 stays DRAFT; run 45313892257 ran Draft Go shards only, required+selected checks skipped. No scope change / no ready-for-review until owner direction + actual source/target evidence. Coordinator recommendation: rule TARGET-BOUND (fail-closed design; otherwise identity dashboard shows regardless of target eligibility = forgeable, matches H-V25 F4/F5 witness gap)."
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/codex-review-wave/1650-0428-078-r7.md", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-24/w54-0428-181-export/0428-181-evidence.md"]
---

- [ ] t-20261120-r28-identity-dashboard-catalog-consumer · Identity dashboard catalog has zero production consumers (P4 of review 1650) #task #release/v0-4-28 #status/blocked #view/blocked #kind/bug
    <!-- generated:card -->
    **Owner:** w54-0428-181-export  
    **PR:** [baseharbor#1819](https://github.com/mcpdev80/baseharbor/pull/1819)  
    **Blocker:** EXACT-DIFF REVIEW finding (w54): perses\_dashboard\_provision.go:353 queries identity\_selection\_confirmed WITHOUT target/application/environment selectors; the exact series appears only at that line across develop/\#1818/\#1819 with NO produce…  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-20/codex-review-wave/1650-0428-078-r7.md), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-24/w54-0428-181-export/0428-181-evidence.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-perses-datasources](t-20261114-r28-perses-datasources.md)  
**Owner:** w54-0428-181-export  
**Priority:** not set  
**PRs:** [baseharbor#1819](https://github.com/mcpdev80/baseharbor/pull/1819)  
**Source:** 
<!-- /generated:links -->

## Found by bug hunt H-103 (funded from card t-20261117-hunt-signals-103, AGENTS 3.3.5 finding-to-card duty)

CODEX-REVIEW of PR #1650 (evidence/r28-welle4-2026-11-20/codex-review-wave/1650-0428-078-r7.md, P4) found that git grep at the candidate head shows no production call site for PersesIdentityDashboardAvailability / identityDashboardCatalog - every use is inside the new tests. The reviewer states plainly: a test-only golden is not a release proof. 0428-078 asked whether to widen her write-set into internal/capability/perses_selection.go or internal/application/perses_runtime.go; the coordinator refused both (perses_selection.go is closed by owner ruling, and #1684 is live in perses_runtime.go), and shrank her PR to the predicate-only write-set the owner already ruled.

## Acceptance

1. Wire the catalog into the Perses provision/export path that actually runs, so a dashboard is emitted only for a verified current signal.
2. Byte/hash-stability proof against the pinned Perses schema or a real export (not a hand-written fixture).
3. If the catalog stays unwired for this release: remove it from the tree in a follow-up commit, and record that decision here so no dead 500-line package ships.

## Boundaries

internal/metrics/** plus the one call site in internal/application/perses_runtime.go or internal/capability/perses_selection.go needed to attach it. SEQUENCING: wait until 0428-083 (#1684) is merged, because it writes the same file; if it is still open, this card stays blocked - owner ruling 2026-11-20.

## Premise corrected by the coordinator (2026-11-20, measured, status unchanged)

The card text says the catalog "exists but is unwired". Measured on develop `f5ce95afce1c` both files are ABSENT:

```
git cat-file -e refs/heads/tmp-dev3:internal/metrics/perses_identity_dashboards.go  -> FEHLT
git cat-file -e refs/heads/tmp-dev3:internal/metrics/perses_identity_witness.go      -> FEHLT
```

They are absent because the owner's 0428-078 takeover removed the zero-consumer catalog from PR #1650 (the witness stayed,
with its consumer at `cmd/baha/app_status_result.go:343`), and #1650 is not merged. Acceptance item 3 ("remove it from the
tree") is therefore already satisfied and is NOT the work. The work is item 1 in its full form: add the catalog AND its
consumer in one card, so the tree never again carries a dashboard file that nothing calls.

Declared dependency `t-20261114-r28-perses-datasources` (#1684): that PR is open and its lane is writing
`internal/application/perses_runtime.go` - the file this card's call-site work would also touch. Start here only after #1684
lands, or report the conflict instead of editing the same file twice (AGENTS 4.3).

Dep-free now (#1810 probe merged 951014e9; 0428-083 on develop). w54 dispatched: wire PersesDashboardCatalog/identity selection witness into production provision/export path in internal/application/perses_runtime.go + regression proving keycloak identity dashboard reaches Perses. Write-set CONSTRAINED to perses_runtime.go; MUST NOT edit internal/metrics/perses_dashboards* / app_status_result.go (#1650/w078 owns them) — post QUESTION if needed there. This is the Option-A full-delivery consumer #1650 depends on. no merge; no Codex.

Design decision made (contract silent on export target): Option 1 — provisioning/dashboards/ under providers/management-ui/perses (mirrors globaldatasource/), registered via config.yaml file provider so Perses LOADS them; gated by #1810 PersesBackendAnswersStatusNow + identity witness. Option 2 rejected (Owner Option-A = real delivery, not status-only). Write-set constrained vs #1650/w078. Documented in evidence for Owner/CODEX review. exact-head Hosted; no merge; no Codex.

Owner keeps PR open; coordinator books accepted/closed only on owner exact-diff accept+merge. Target-bound ruling is the linchpin for #1819 + #1818.
