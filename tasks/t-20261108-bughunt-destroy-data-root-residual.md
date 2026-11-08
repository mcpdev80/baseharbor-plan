---
id: t-20261108-bughunt-destroy-data-root-residual
card_number: "0427-152"
card_short_title: "Destroy finds own core"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: "chatgpt-r27-destroy-owner"
kanban_status: review
kanban_lane: review
kanban_summary: "Destroy resolves owned core targets from the data root (never discards foreign targets, fail-closed per the card-127 doctrine);…"
kanban_title: 0427-152 · Destroy finds own core
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1483]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/bughunt-ca-pkce/act-1455-fate.md", "https://github.com/mcpdev80/baseharbor/actions/runs/42487539941"]
---
- [ ] t-20261108-bughunt-destroy-data-root-residual · Bug Hunt v0.4.27: Destroy finds own core #task #release/v0-4-27 #status/review #view/review #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** chatgpt-r27-destroy-owner · **Priority:** normal  
    **PR:** [baseharbor#1483](https://github.com/mcpdev80/baseharbor/pull/1483)  
    **Waiting:** Produkt-PR \#1483 gemergt; Bearbeitung pausiert bis zur gesonderten exakten Native-Docker/Podman-Abnahme des Datenwurzel-/Core-Discovery-Vertrags. Kein neuer Produkt-PR ohne Befund.  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/bughunt-ca-pkce/act-1455-fate.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** chatgpt-r27-destroy-owner  
**Priority:** normal  
**PRs:** [baseharbor#1483](https://github.com/mcpdev80/baseharbor/pull/1483)  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
Destroy resolves owned core targets from the data root (never discards foreign targets, fail-closed per the card-127 doctrine); use the two commits as a base or deliberately re-slice with rationale; regression destroy+core in the lifecycle field.

## Problem (source evidence in the dossier)
The destroy change from PR #1455 (resolve owned core targets from the data root) landed in NO ancestry of develop or #1457 - the review confirms residual commits a2761413 + 9a963000. PR #1455 is closed; this card is its contract. Source: act-1455-fate.md.

## Acceptance
Destroy resolves owned core targets from the data root (never discards foreign targets, fail-closed per the card-127 doctrine); use the two commits as a base or deliberately re-slice with rationale; regression destroy+core in the lifecycle field.

## Dependencies and file ownership
None. Write-set: internal destroy + data-root resolution.

## Audit note (Karten-Audit 2026-11-08)
Audit 2026-11-08 (mapping): related to #122 destroy inventory but a distinct data-root recovery contract. [Dossier](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r27-welle5-folge-2026-11-08/karten-audit-2026-11-08.md)


## Source/CI ownership — 2026-11-08

- Owner `chatgpt-r27-destroy-owner`, [PR #1483](https://github.com/mcpdev80/baseharbor/pull/1483). Re-sliced the old unmerged #1455 data-root Core discovery using validated `coreinstallation.Load` rather than trusting arbitrary JSON. Foreign/ambiguous Core owners fail closed without guessed runtime.
- Regression: real temporary owned Core-only state is discoverable; foreign state remains unverifiable with no inferred runtime. Native Docker/Podman exact-head CI required before merge; card remains Active, no claim of actual destruction.

## Kanban-Pause 2026-11-08

- Produkt-PR #1483 gemergt; Bearbeitung pausiert bis zur gesonderten exakten Native-Docker/Podman-Abnahme des Datenwurzel-/Core-Discovery-Vertrags. Kein neuer Produkt-PR ohne Befund.
- Status `wait` als Ressourcen-/Abnahme-Pause, **nicht** als technischer Blocker. Owner bleibt bestehen; Reaktivierung nach konkreter Uebergabe bzw. Acceptance.

## Exact native CI audit – 2026-11-08

- [PR #1483](https://github.com/mcpdev80/baseharbor/pull/1483) was merged into develop (`cf9351e766f6dbcd654a9af1701c2da2d592ee9b`). Exact PR run [#42487539941](https://github.com/mcpdev80/baseharbor/actions/runs/42487539941) completed SUCCESS; required native Docker job `128752757865` and Podman job `128752757922` both SUCCESS.
- Both raw job logs include **one real PASS** for `TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry`, with actual partial native deletion, retry, foreign-holder preservation and selected owner/resource removal. Not a green-by-SKIP.
- The PR also adds `TestFullDestroyDiscoversProtectedCoreOnlyTarget` covering verified data-root Core-only discovery and fail-closed foreign ownership with temporary state. **This specific regression is not a native runtime test**; do not conflate the generic native destroy-retry PASS with a full positive unregistered-Core data-root cleanup E2E.
- **Review decision:** Code implementation is merged and native destroy/retry proof exists, so unqualified `wait` is no longer accurate. Move to `review` for the precise criterion: whether the already-tested identity/owner state regression plus native destroy retry jointly satisfy the card, or whether a dedicated native missing-target-configuration Core-only case is mandated. Do not claim card accepted or start redundant product code.
