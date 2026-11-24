---
id: t-20261124-r28-perses-witness-producer-cli
card_number: "0428-265"
card_short_title: "backend witness never proven"
type: bug
areas: [metrics, observability, cli]
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: Make the configured verdict of PersesBackendWitness reachable through real observation instead of a hard-coded empty witness.…
kanban_title: 0428-265 · backend witness never proven
priority: ""
depends_on: [t-20261119-r28-perses-status-backend-witness]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261124-r28-perses-witness-producer-cli · PersesBackendSignalWitness is passed as a zero-value literal at every CLI call site, so the configured verdict is unreachable on every status surface. #task #release/v0-4-28 #status/planned #view/ready #area/cli #area/metrics #area/observability #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261119-r28-perses-status-backend-witness](t-20261119-r28-perses-status-backend-witness.md)  
**Required by:** [t-20261124-r28-app-status-unauthorized-live-probe](t-20261124-r28-app-status-unauthorized-live-probe.md), [t-20261124-r28-perses-state-spelling-drift](t-20261124-r28-perses-state-spelling-drift.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

Source: bughunt-hv25 F4+F5 dossier adc07163d (akte `evidence/r28-welle6-2026-11-24/bughunt-hv25-status-obs-desk/round-1.md`, develop 3ebfb90d)

## Goal

Make the `configured` verdict of `PersesBackendWitness` reachable through real observation instead of a hard-coded empty witness. Witnessed on develop 3ebfb90d:

- `cmd/baha/perses_lifecycle.go:366` (`baha app perses status`) passes the literal `metricsprovider.PersesBackendSignalWitness{}`.
- `cmd/baha/app_status_result.go:328` (remote face) and `:436` (local face) pass the same literal; `internal/metrics/perses_dashboards_hosts.go:338` and `:612` use the same zero-value internally.
- With all three `Proven` fields false (`internal/metrics/perses_dashboards_hosts.go:546-555`), `persesBackendSignalWitnessFromManifest` (`cmd/baha/app_status_result.go:117`) can never answer `configured`: every declared backend shows `unreachable` even on a fully working stack (False-Red on both the human and the machine surface).
- Grep on develop: no production call site anywhere constructs a witness with a `Proven` field set — the producer the surfaces claim to consume does not exist.
- The comment at `cmd/baha/app_status_result.go:112-116` defers the probe to "card 0428-143"; that card closed as #1729 with a different scope (Verification=none semantics), so the deferral is stale — this card is the missing wiring.

## Acceptance

1. One witness producer derives `PrometheusProven` / `LokiProven` / `TempoProven` from real backend answers (the per-signal probe paths already in `internal/metrics`), not from manifest declaration alone; every CLI call site (`perses_lifecycle.go:366`, `app_status_result.go:328`, `:436`) passes it instead of the literal.
2. One executable regression in `cmd/baha` (wired into the CI group covering `cmd/baha` — "PR · Go unit"): with a scripted answering backend the JSON shows `configured` for that backend; with a silent backend it shows `unreachable`. Fail-closed in both directions, never an inferred `configured`.
3. The stale "card 0428-143" comment is replaced by a reference to this card's wiring.
4. Evidence names the CI job and trigger that run the test (AGENTS 5.3).

## Boundaries

`cmd/baha/app_status_result.go`, `cmd/baha/perses_lifecycle.go`, a witness producer in `internal/metrics` (the `perses_dashboards_hosts.go` family) and their tests. No new manifest fields, no new state holders. The human and machine faces must keep sharing the one witness (0428-142 rule).

## Related

- F4 and F5 verified real on develop 3ebfb90d (see goal); the zero-value literal is the only witness any call site passes.
- Sequel to 0428-142 (`perses status` backend witness, accepted): the shape landed there, this card lands the producer. The 0428-143 comment the dossier called stale is NOT this card's scope (that card closed accepted as #1729, Verification=none semantics); its witness deferral is resolved here.
- Probe unification is card [0428-263](t-20261124-r28-perses-backend-status-real-probe.md); use whichever probe path it fixes.
