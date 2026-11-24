---
id: t-20261124-r28-alert-evaluator-live-health-wiring
card_number: "0428-268"
card_short_title: "evaluator health never probed"
type: bug
areas: [cli, observability]
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "The alert-evaluator face must distinguish applied-but-failing from configured-unverified, from the real runtime, not from the…"
kanban_title: 0428-268 · evaluator health never probed
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

- [ ] t-20261124-r28-alert-evaluator-live-health-wiring · VerifyPersesAlertEvaluatorHealth has no CLI/MCP caller and the applied alert face derives from the manifest alone, so applied-but-failing reads as configured_unverified. #task #release/v0-4-28 #status/planned #view/ready #area/cli #area/observability #kind/bug
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

Source: bughunt-hv25 F6+F7 dossier adc07163d (akte `evidence/r28-welle6-2026-11-24/bughunt-hv25-status-obs-desk/round-1.md`, develop 3ebfb90d)

## Goal

The alert-evaluator face must distinguish applied-but-failing from configured-unverified, from the real runtime, not from the manifest alone. Witnessed on develop 3ebfb90d:

- F7: `VerifyPersesAlertEvaluatorHealth` (`internal/metrics/perses_prometheus_alerts.go:90-115`) — the per-panel rule-health probe — has NO caller outside its own file and its test (`grep -r` on develop). The consumer that landed with 0428-152/#1816 calls only `BuildPersesAlertEvaluator`, which returns always `configured_unverified` (`perses_prometheus_alerts.go:83`). So a broken live evaluator (Prometheus loaded, rule health != ok) is reported as `configured_unverified`: the 3-way observation the 0428-152 mission promised is 2-way in code.
- F6: `deploymentApplied` (`cmd/baha/perses_lifecycle.go:343-346`) is existence-only (`ExistingRuntimeFiles(...) == nil`); the applied branch of `persesAlertEvaluatorObservationWithApplication` (`cmd/baha/perses_lifecycle.go:230-250`) then derives the verdict from the manifest alone, so a stale runtime tree (prior deployment's files) yields the current manifest's applied verdict, contradicting the fail-closed doc at `perses_lifecycle.go:340-342`.

## Acceptance

1. On the applied branch (runtime confirmed for THIS deployment identity), the consumer calls `VerifyPersesAlertEvaluatorHealth` and maps its outcome to the documented third state (rule health ok / failing → distinct state), fail-closed to `configured_unverified` when the probe cannot run. No second parallel logic in the CLI.
2. `deploymentApplied` cross-checks the found runtime against the resolved deployment identity (the stamp the other status faces use); a mismatch or unreadable tree fails closed to the not-applied face with a concrete reason. No new state holders.
3. One executable regression in `cmd/baha` (wired into the CI group covering `cmd/baha` — "PR · Go unit"): (a) a scripted evaluator with failing rule health on an applied deployment is NOT reported `configured_unverified`-identical to the silent case; (b) runtime files from a different deployment identity do not yield the current manifest's applied verdict.
4. Evidence names the CI job and trigger that run the test (AGENTS 5.3).

## Boundaries

`cmd/baha/perses_lifecycle.go`, `cmd/baha/app_status_collect.go` (shared consumer), and `cmd/baha` tests; `internal/metrics/perses_prometheus_alerts.go` only if the health probe needs a small injectable seam — no contract change there. Owner-gate: if the live rule-health contract requires an Owner decision on the probe's authorization, stop and report.

## Related

- F6 and F7 verified real on develop 3ebfb90d (see goal).
- Consumer wiring is 0428-152 (accepted, #1816): its acceptance demanded the verifier's result decide the state; the verifier function that could distinguish it (`VerifyPersesAlertEvaluatorHealth`) never got wired — this card closes that gap plus the applied-face staleness.
