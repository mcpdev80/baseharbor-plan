---
id: t-20261124-r28-perses-two-status-faces-disagree
card_number: "0428-264"
card_short_title: "two status faces disagree"
type: bug
areas: [metrics, observability, cli]
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Self-consistency of the two Perses faces in the same baha app status --json render. Witnessed on develop 3ebfb90d:"
kanban_title: 0428-264 · two status faces disagree
priority: ""
depends_on: [t-20261124-r28-perses-backend-status-real-probe]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261124-r28-perses-two-status-faces-disagree · perses.status and infrastructure_dashboards can report verified vs all-unavailable for one manifest because the two faces derive from different probe paths. #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/cli #area/metrics #area/observability #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned  
    **Waiting for prerequisites**  
    **Needs:** [t-20261124-r28-perses-backend-status-real-probe](t-20261124-r28-perses-backend-status-real-probe.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261124-r28-perses-backend-status-real-probe](t-20261124-r28-perses-backend-status-real-probe.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

Source: bughunt-hv25 F2 dossier adc07163d (akte `evidence/r28-welle6-2026-11-24/bughunt-hv25-status-obs-desk/round-1.md`, develop 3ebfb90d)

## Goal

Self-consistency of the two Perses faces in the same `baha app status --json` render. Witnessed on develop 3ebfb90d:

- `internal/metrics/perses_backend_status.go:81` (status face) calls `BuildPersesInfraDashboardWithProbe` directly; all-missing panels map to `configured_unverified` (`perses_backend_status.go:85-87`).
- `internal/metrics/perses_infra_dashboards.go:208` (availability face) calls `VerifyPersesInfraDashboard`, which ERRORS when no panel answered (`perses_infra_dashboards.go:145-147`) → every panel becomes an explicit unavailable entry.
- Both are computed in the same render at `cmd/baha/app_status_result.go:314` and `:317`, so one manifest can show `perses.status` from one probe semantics and `infrastructure_dashboards` from the other; partial-panel gaps diverge per-panel.

After 0428-263 fixes the probe definition, the two faces must derive from the SAME probe result in one render pass, so they cannot disagree.

## Acceptance

1. A regression in `cmd/baha` (wired into the CI group covering `cmd/baha` — "PR · Go unit") drives one manifest through a scripted probe with a partial panel gap and asserts the two faces agree: a panel the status face counts as answered is `available` in `infrastructure_dashboards`, a missing panel is `unavailable`; `verified` status never coincides with an all-unavailable availability face for the same manifest.
2. One probe execution per status render (no second HTTP round-trip path that can drift between the two fields); the derivation shares the probe result.
3. Evidence names the CI job and trigger that run the test (AGENTS 5.3).

## Boundaries

The render path in `cmd/baha/app_status_result.go` and the two entry points' shared probe plumbing. Depends on 0428-263 (the single probe definition) — do not start before that lands.

## Related

- F2 verified real on develop 3ebfb90d (see goal).
- F1 (probe definition) is card [0428-263](t-20261124-r28-perses-backend-status-real-probe.md); this card is its self-consistency sequel.
