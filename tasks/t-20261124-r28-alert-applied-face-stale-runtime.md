---
id: t-20261124-r28-alert-applied-face-stale-runtime
card_number: "0428-358"
card_short_title: "applied face ignores runtime"
type: bug
areas: [cli, observability]
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Make the applied alert-evaluator face reflect the CURRENT runtime, not just the presence of files. Witnessed on develop 3ebfb90d:"
kanban_title: 0428-358 · applied face ignores runtime
priority: ""
depends_on: [t-20261119-r28-perses-alert-verifier-caller-wiring]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261124-r28-alert-applied-face-stale-runtime · deploymentApplied only asks whether runtime files exist; the applied-branch alert verdict then comes from the manifest alone, so stale runtime files make the alert-evaluator face claim another deployment's state. #task #release/v0-4-28 #status/planned #view/ready #area/cli #area/observability #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261119-r28-perses-alert-verifier-caller-wiring](t-20261119-r28-perses-alert-verifier-caller-wiring.md)  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

Source: bughunt-hv25 F6 dossier adc07163d (akte `evidence/r28-welle6-2026-11-24/bughunt-hv25-status-obs-desk/round-1.md`, develop 3ebfb90d)

## Goal

Make the applied alert-evaluator face reflect the CURRENT runtime, not just the presence of files. Witnessed on develop 3ebfb90d:

- `cmd/baha/perses_lifecycle.go:343-346`: `deploymentApplied` returns true iff `application.ExistingRuntimeFiles(...) == nil` — existence only, no identity or version check.
- `persesAlertEvaluatorObservationWithApplication` (`cmd/baha/perses_lifecycle.go:230-250, 313-316`) then derives the applied verdict from `BuildPersesAlertEvaluator(m)` — manifest-only, no runtime read.
- Consequence: if `ExistingRuntimeFiles` succeeds but returns a prior deployment's files (store not locked, replacement apply interrupted), the face reports the manifest's verdict as applied truth, contradicting the fail-closed doc at `perses_lifecycle.go:340-342` ("only materialized, applied runtime may claim a wired evaluator").

## Acceptance

1. The applied branch cross-checks the runtime it found against the resolved deployment identity (the same identity stamp the other status faces use, e.g. `resolved.DeploymentIdentity`); a mismatch or unreadable tree fails closed to the not-applied/unavailable face with a concrete reason. No new state holders.
2. One executable regression in `cmd/baha` (wired into the CI group covering `cmd/baha` — "PR · Go unit"): with runtime files from a different deployment identity present, the alert-evaluator observation does NOT report the current manifest's applied verdict.
3. Evidence names the CI job and trigger that run the test (AGENTS 5.3).

## Boundaries

`cmd/baha/perses_lifecycle.go` (`deploymentApplied`, `persesAlertEvaluatorObservationWithApplication`) and `cmd/baha` tests. Reuse the existing deployment-identity plumbing; no changes in `internal/metrics`.

## Related

- Severity low/medium in the dossier (edge case, needs a stale-tree window).
- Verified real on develop 3ebfb90d (see goal). Consumer wiring is 0428-152 (accepted, #1816); this card closes the applied-face staleness its dossier left open.
