---
id: t-20261124-r28-perses-backend-status-real-probe
card_number: "0428-263"
card_short_title: "status probe not the verifier"
type: bug
areas: [metrics, observability, cli]
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "One definition of the \"real HTTP probe\" behind the Perses three-state status. Witnessed on develop 3ebfb90d:"
kanban_title: 0428-263 · status probe not the verifier
priority: ""
depends_on: [t-20261120-r28-perses-status-never-verified]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261124-r28-perses-backend-status-real-probe · PersesBackendAnswersStatusNow runs the dashboard build while the app-status comment names VerifyPersesInfraDashboard as the real probe. #task #release/v0-4-28 #status/planned #view/ready #area/cli #area/metrics #area/observability #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261120-r28-perses-status-never-verified](t-20261120-r28-perses-status-never-verified.md)  
**Required by:** [t-20261124-r28-perses-state-spelling-drift](t-20261124-r28-perses-state-spelling-drift.md), [t-20261124-r28-perses-two-status-faces-disagree](t-20261124-r28-perses-two-status-faces-disagree.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

Source: bughunt-hv25 F1 dossier adc07163d (akte `evidence/r28-welle6-2026-11-24/bughunt-hv25-status-obs-desk/round-1.md`, develop 3ebfb90d)

## Goal

One definition of the "real HTTP probe" behind the Perses three-state status. Witnessed on develop 3ebfb90d:

- `internal/metrics/perses_backend_status.go:49-60` documents "the established per-target instrument: the production path runs real HTTP round trips" and then calls `BuildPersesInfraDashboardWithProbe` (line 81) with `httpClientSeriesProbe`.
- `cmd/baha/app_status_result.go:306-307` states the opposite contract for the same surface: "only the real per-target health probe (metrics VerifyPersesInfraDashboard) can" promote to verified — and `PersesInfraDashboardAvailability` uses `VerifyPersesInfraDashboard` (`internal/metrics/perses_infra_dashboards.go:208`).

The three-state `perses.status` must be derived from exactly the one documented verifier path (or the doc/comment is corrected to one named path). Two coexisting "real probe" definitions for the same surface are the defect.

## Acceptance

1. One probe definition: either `PersesBackendAnswersStatusNow` routes through `VerifyPersesInfraDashboard` semantics (per-panel live verification, fail-closed on missing datasource/endpoint/authorization) or the comments in `internal/metrics/perses_backend_status.go` and `cmd/baha/app_status_result.go` name the single build-with-probe path as authoritative. No third definition stays in the codebase.
2. One executable regression in the package that owns the status entry point (wired into the CI group that covers `internal/metrics` — "PR · Go unit"): with a scripted probe whose endpoint/datasource is denied, `PersesBackendAnswersStatusNow` fails closed to `configured_unverified`, never `verified`; with an answering backend it reports `verified`.
3. Evidence names the CI job and trigger that run the test (AGENTS 5.3).

## Boundaries

`internal/metrics/perses_backend_status.go`, the comment sites in `internal/metrics/perses_infra_dashboards.go` / `cmd/baha/app_status_result.go`, and their tests. No changes to the verified-only predicate in `internal/capability/perses_selection.go` (owner-closed per 0428-186).

## Related

- F1 verified real on develop 3ebfb90d (see goal).
- F8 (stale symbol name `metrics.PersesBackendAnswers` in docs, dossier's 0428-186 ref): verified real on develop 3ebfb90d; the complete fix list (three comment sites) and the card that owns it are in card 0428-267 acceptance item 2 — one comment-only sweep, not a second card.
- F2 (same probe family, two faces disagreeing) is card [0428-264](t-20261124-r28-perses-two-status-faces-disagree.md), a sequel that depends on this card.
