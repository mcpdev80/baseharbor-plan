---
id: t-20261124-r28-perses-state-spelling-drift
card_number: "0428-267"
card_short_title: "three spellings one state"
type: bug
areas: [metrics, observability, cli, docs]
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "One canonical spelling per state across every Perses status field. Witnessed on develop 3ebfb90d, all in the same JSON output…"
kanban_title: 0428-267 · three spellings one state
priority: ""
depends_on: [t-20261124-r28-perses-witness-producer-cli, t-20261124-r28-perses-backend-status-real-probe]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261124-r28-perses-state-spelling-drift · The Perses three-state values appear as not_configured, not configured and not-configured in one JSON output family, and unreachable is a value no contract names. #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/cli #area/docs #area/metrics #area/observability #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned  
    **Waiting for prerequisites**  
    **Needs:** [t-20261124-r28-perses-witness-producer-cli](t-20261124-r28-perses-witness-producer-cli.md), [t-20261124-r28-perses-backend-status-real-probe](t-20261124-r28-perses-backend-status-real-probe.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261124-r28-perses-witness-producer-cli](t-20261124-r28-perses-witness-producer-cli.md), [t-20261124-r28-perses-backend-status-real-probe](t-20261124-r28-perses-backend-status-real-probe.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

Source: bughunt-hv25 F9 dossier adc07163d (akte `evidence/r28-welle6-2026-11-24/bughunt-hv25-status-obs-desk/round-1.md`, develop 3ebfb90d)

## Goal

One canonical spelling per state across every Perses status field. Witnessed on develop 3ebfb90d, all in the same JSON output family (`Perses.State`, `Perses.AlertEvaluator.State`, `PersesBackendWitness[].State`):

- `internal/application/perses_lifecycle.go:166-171` via `capability.PersesStatusNow` (`internal/capability/perses.go:265-283`): `not_configured` / `configured_unverified` (underscore) — the shape `docs/spec/management-access-v1.md` names normatively.
- `cmd/baha/perses_lifecycle.go:234-235`: `not configured` (SPACE) and `unavailable (owner-gated evaluator contract)`.
- `cmd/baha/app_status_result.go:76-80`: `not-configured` (HYPHEN) / `configured` / `unreachable` — `unreachable` appears in no spec.

A consumer parsing `baha app status --json` or `baha app perses status --json` must match three spellings for the same concept; the mission contract names fewer values than the code emits.

## Acceptance

1. One canonical vocabulary for the three states across all Perses status fields (the underscore form the spec already pins, `not_configured` / `configured_unverified` / `verified`), or each distinct field's vocabulary is defined normatively in `docs/spec/management-access-v1.md` (EN and DE) with its exact values. No silent divergence between code and spec either way.
2. The stale symbol name `metrics.PersesBackendAnswers` is corrected to `metrics.PersesBackendAnswersStatusNow` at EVERY reference site (bughunt-hv25 F8; comment-only). Complete list witnessed on develop 3ebfb90d: `internal/capability/perses.go:213` and `:252`, `internal/application/perses_lifecycle.go:162`. Re-grep at card start (`grep -rn 'PersesBackendAnswers' --include='*.go' | grep -v StatusNow`) and fix all hits outside test identifiers.
3. One executable regression that renders both status surfaces and asserts every emitted state string is a member of the documented vocabulary.
4. The test runs in the CI group covering `cmd/baha` ("PR · Go unit"); evidence names job and trigger (AGENTS 5.3).

## Boundaries

String constants in `cmd/baha/perses_lifecycle.go` / `cmd/baha/app_status_result.go`, the comment sites of acceptance item 2 (`internal/application/perses_lifecycle.go`, `internal/capability/perses.go`), the `docs/spec/management-access-v1.md` vocabulary section (EN + DE), and tests. If a public JSON contract test pins an old spelling, update it in the same PR and note it in the release notes.

## Related

- F9 is this card; F8 (stale symbol name, comment-only) is intake here as acceptance item 2 — same status surfaces, one sweep. The dossier's F8 site list is INCOMPLETE: measured on develop 3ebfb90d, `grep -rn 'PersesBackendAnswers' | grep -v StatusNow` outside test files hits EXACTLY the three cited comments (`internal/capability/perses.go:213` and `:252`, `internal/application/perses_lifecycle.go:162`) and nothing else — the dossier's "4 references" counts the definition-site note in `internal/metrics/perses_backend_status.go:18`, which names no symbol and needs no fix.
- Start after the probe/witness wiring of 0428-263 and 0428-265 so the vocabulary sweep covers the final call sites, not intermediate shapes.
