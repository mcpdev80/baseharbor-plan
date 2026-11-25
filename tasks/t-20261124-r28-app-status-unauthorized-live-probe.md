---
id: t-20261124-r28-app-status-unauthorized-live-probe
card_number: "0428-266"
card_short_title: "status probes without operator"
type: bug
areas: [cli, observability]
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "Align the baha app status --json Perses probe with the operator-context contract. Witnessed on develop 3ebfb90d:"
kanban_title: 0428-266 · status probes without operator
priority: ""
depends_on: [t-20261120-r28-perses-status-never-verified, t-20261124-r28-perses-witness-producer-cli]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261124-r28-app-status-unauthorized-live-probe · baha app status --json runs the live Perses HTTP probe with no operator authorization while perses status gates it. #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/cli #area/observability #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned  
    **Waiting for prerequisites**  
    **Needs:** [t-20261124-r28-perses-witness-producer-cli](t-20261124-r28-perses-witness-producer-cli.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261120-r28-perses-status-never-verified](t-20261120-r28-perses-status-never-verified.md), [t-20261124-r28-perses-witness-producer-cli](t-20261124-r28-perses-witness-producer-cli.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

Source: bughunt-hv25 F3 dossier adc07163d (akte `evidence/r28-welle6-2026-11-24/bughunt-hv25-status-obs-desk/round-1.md`, develop 3ebfb90d)

## Goal

Align the `baha app status --json` Perses probe with the operator-context contract. Witnessed on develop 3ebfb90d:

- `cmd/baha/app_status_result.go:294-317`: the status render calls `metricsprovider.PersesBackendAnswersStatusNow` (line 314), which performs real HTTP (`internal/metrics/perses_backend_status.go:52-60`).
- `collectApplicationStatus` (`cmd/baha/app_observe.go:32`) and the render path issue no `authorizeApplicationOperation` / operatorauth gate; by contrast `reportPersesSurfaceStatus` (`cmd/baha/perses_lifecycle.go:351-358`, `baha app perses status`) DOES call `authorizeApplicationOperation` before any observation.
- The contract at `internal/capability/perses.go:213-214` says `verified` requires an authenticated operator context; the machine-JSON path has no such gate, so the surface discloses live-backend reachability (and can report `verified`) in a context the contract says cannot produce it.

## Acceptance

1. Either the `app status` Perses probe runs only behind the same authorization seam `reportPersesSurfaceStatus` uses (unauthorized callers get the fail-closed `configured_unverified`, no live HTTP), or the contract documents an explicit allow-anonymous-read ruling in `docs/spec/management-access-v1.md` (EN + DE). No undocumented divergence between the two surfaces.
2. One executable regression in `cmd/baha` (wired into the CI group covering `cmd/baha` — "PR · Go unit"): in an unauthorized context the probe seam is not invoked (or the verdict is the documented fail-closed one) — asserting the chosen contract, fail-closed.
3. Evidence names the CI job and trigger that run the test (AGENTS 5.3).


## Owner decision — 2026-11-25

The live Perses probe requires an authenticated, authorized operator. An unauthorized `baha app status --json` call must return the documented fail-closed `configured_unverified` result without issuing the live HTTP probe. Do not add an anonymous-probe exception.

## Boundaries

`cmd/baha/app_status_result.go` probe call site, `cmd/baha/app_observe.go`, `internal/capability/perses.go` comments or the spec doc. No change to the authorization implementation itself (owned by the operator-auth cards).

## Related

- F3 verified real on develop 3ebfb90d (see goal).
- Same surface family under repair: [0428-263](t-20261124-r28-perses-backend-status-real-probe.md) (probe definition), [0428-265](t-20261124-r28-perses-witness-producer-cli.md) (witness producer). This card gates WHO may run the probe, not WHAT it probes; start after 0428-263/265 so the authorization seam wraps the final probe wiring.
