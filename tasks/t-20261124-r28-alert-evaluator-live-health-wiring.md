---
id: t-20261124-r28-alert-evaluator-live-health-wiring
card_number: "0428-268"
card_short_title: "evaluator health wired"
type: bug
areas: [cli, observability]
release: v0.4.28
version: ""
parent: ""
owner: Codex (w120)
kanban_status: closed
kanban_lane: closed
kanban_summary: Both Perses status faces now report live evaluator health only after confirming the runtime stamp matches the resolved…
kanban_title: 0428-268 · evaluator health wired
priority: ""
depends_on: [t-20261119-r28-perses-alert-verifier-caller-wiring]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1831]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1831", "https://github.com/mcpdev80/baseharbor/actions/runs/45468539868", "https://github.com/mcpdev80/baseharbor/actions/runs/45469392236", "https://github.com/mcpdev80/baseharbor/commit/d0a6f370bdab87386819b61c0a85ae64e7814caf"]
---

- [x] t-20261124-r28-alert-evaluator-live-health-wiring · VerifyPersesAlertEvaluatorHealth has no CLI/MCP caller and the applied alert face derives from the manifest alone, so applied-but-failing reads as configured_unverified. #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/cli #area/observability #kind/bug
    <!-- generated:card -->
    **Owner:** Codex (w120)  
    **PR:** [baseharbor#1831](https://github.com/mcpdev80/baseharbor/pull/1831)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1831), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/45468539868), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/45469392236), [proof 4](https://github.com/mcpdev80/baseharbor/commit/d0a6f370bdab87386819b61c0a85ae64e7814caf)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261119-r28-perses-alert-verifier-caller-wiring](t-20261119-r28-perses-alert-verifier-caller-wiring.md)  
**Owner:** Codex (w120)  
**Priority:** not set  
**PRs:** [baseharbor#1831](https://github.com/mcpdev80/baseharbor/pull/1831)  
**Source:** 
<!-- /generated:links -->

Source: bughunt-hv25 F6+F7 dossier adc07163d (akte `evidence/r28-welle6-2026-11-24/bughunt-hv25-status-obs-desk/round-1.md`, develop 3ebfb90d)

## Goal

Both Perses status faces now report live evaluator health only after confirming the runtime stamp matches the resolved deployment identity. Witnessed on develop 3ebfb90d:

- F7: `VerifyPersesAlertEvaluatorHealth` (`internal/metrics/perses_prometheus_alerts.go:90-115`) — the per-panel rule-health probe — has NO caller outside its own file and its test (`grep -r` on develop). The consumer that landed with 0428-152/#1816 calls only `BuildPersesAlertEvaluator`, which returns always `configured_unverified` (`perses_prometheus_alerts.go:83`). So a broken live evaluator (Prometheus loaded, rule health != ok) is reported as `configured_unverified`: the 3-way observation the 0428-152 mission promised is 2-way in code.
- F6: `deploymentApplied` (`cmd/baha/perses_lifecycle.go:343-346`) is existence-only (`ExistingRuntimeFiles(...) == nil`); the applied branch of `persesAlertEvaluatorObservationWithApplication` (`cmd/baha/perses_lifecycle.go:230-250`) then derives the verdict from the manifest alone, so a stale runtime tree (prior deployment's files) yields the current manifest's applied verdict, contradicting the fail-closed doc at `perses_lifecycle.go:340-342`.

## Acceptance

1. On the applied branch (runtime confirmed for THIS deployment identity), the consumer calls `VerifyPersesAlertEvaluatorHealth` and maps its outcome to the documented third state (rule health ok / failing → distinct state), fail-closed to `configured_unverified` when the probe cannot run. No second parallel logic in the CLI.
2. `deploymentApplied` cross-checks the found runtime against the resolved deployment identity (the stamp the other status faces use); a mismatch or unreadable tree fails closed to the not-applied face with a concrete reason. No new state holders.
3. One executable regression in `cmd/baha` (wired into the CI group covering `cmd/baha` — "PR · Go unit"): (a) a scripted evaluator with failing rule health on an applied deployment is NOT reported `configured_unverified`-identical to the silent case; (b) runtime files from a different deployment identity do not yield the current manifest's applied verdict.
4. Evidence names the CI job and trigger that run the test (AGENTS 5.3).

**Test binding:** Normal Go package auto-discovery in `cmd/baha`; Hosted `PR · Go unit` CLI shards select the package tests on the `pull_request` trigger.

## Boundaries

`cmd/baha/perses_lifecycle.go`, `cmd/baha/app_status_collect.go` (shared consumer), and `cmd/baha` tests; `internal/metrics/perses_prometheus_alerts.go` only if the health probe needs a small injectable seam — no contract change there. Owner-gate: if the live rule-health contract requires an Owner decision on the probe's authorization, stop and report.

## Related

- F6 and F7 verified real on develop 3ebfb90d (see goal).
- Consumer wiring is 0428-152 (accepted, #1816): its acceptance demanded the verifier's result decide the state; the verifier function that could distinguish it (`VerifyPersesAlertEvaluatorHealth`) never got wired — this card closes that gap plus the applied-face staleness.

## Handoff

Test -> check/gate -> trigger -> result: `TestPersesAlertEvaluatorObservationReflectsLiveHealth`, `TestPersesAlertEvaluatorObservationFailsClosedOnLiveProbeError`, `TestDeploymentAppliedRejectsRuntimeStampedForDifferentDeployment`, and CLI status-face tests -> Hosted `PR · Go unit` CLI shards -> `pull_request` -> success on exact candidate `fa1608b69f0bce7f305b6e90ac4b3691ff5061cc`. Runs `45468539868` and `45469392236` both completed top-level success. In run `45469392236`, `PR Selected Checks` succeeded from GitHub Actions integration 15368, all four CLI shards succeeded, and the targeted Core-less Docker lifecycle jobs plus Docker data-capabilities runtime gate succeeded. Skipped jobs were reviewed by the owner.

Independent Codex review covered the full five-file diff at that exact candidate against base `adf43709b8b37cd2b18a6bf4710019d7343d54b4`; no correctness or security blockers were found. Review note: [PR #1831 review comment](https://github.com/mcpdev80/baseharbor/pull/1831#issuecomment-7142616196).

Merged by owner-authorized squash through PR [#1831](https://github.com/mcpdev80/baseharbor/pull/1831). Merge SHA: `d0a6f370bdab87386819b61c0a85ae64e7814caf`; remote `develop` was witnessed at that SHA with `git ls-remote` after merge.

Loesung: Die Live-Regelgesundheit ist an beide Perses-Statusfaces angeschlossen und wird nur fuer die passende angewandte Deployment-Identitaet behauptet. Entschieden von Codex-Lane w120.
