---
id: t-20261122-broker-diagnostics-empty
card_number: "0428-240"
card_short_title: "broker readiness failure ships"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: (offen, mission liegt bereit)
tags: [#task, #release/v0.4-28]
kanban_status: wait
kanban_lane: wait
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-240 · broker readiness failure ships
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: "kein ausfuehrender worker-sitz frei (03c7350a fuehrt missionen nicht aus, rotation braucht owner-directive)"
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/44994268323", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/runtime-broker-0428-237/round-1.md"]
---

- [ ] t-20261122-broker-diagnostics-empty · CLI: name the failing dependency in broker readiness diagnostics #task #release/v0-4-28 #status/wait #view/wait #kind/task
    <!-- generated:card -->
    **Owner:** (offen, mission liegt bereit)  
    **Waiting:** kein ausfuehrender worker-sitz frei (03c7350a fuehrt missionen nicht aus, rotation braucht owner-directive)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/44994268323), [proof 2](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/runtime-broker-0428-237/round-1.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** (offen, mission liegt bereit)  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

One or two sentences: the observable outcome.

## Scope

- In scope:
- Out of scope:

## Acceptance

- Each criterion as a plain bullet. Do not use checkboxes here: only the card line above is a checkbox.

## Required checks

- **Modified features:** Inventory and adapt all affected existing unit, contract, integration, regression, E2E and native-runtime tests; add missing cases.
- **New features/providers (e.g. Perses Provider Contract):** Implement NEW dedicated positive, negative, authorization, ownership, error-path, compatibility and lifecycle tests wherever relevant. Passing unrelated existing suites is not sufficient.
- **CI integration and mapping are part of implementation:** Register every new/changed test in its package/test inventory and update existing test-to-gate mapping, selectors, relevant `REQUIRED_CLIENT_TESTS`/package equivalent, `scripts/pr-gate-plan.py`, `scripts/release-requirements.json`, and CI workflow paths/triggers where applicable. Coordinate reserved CI files with their owner; no new CI framework.
- **Mapping selection proof:** Verify affected paths select the required tests, unrelated paths do not unnecessarily select them, and the applicable stacked-PR, ready-for-review, develop and release workflows cannot silently bypass them. Unknown coverage broadens selection instead of failing open.
- **Hard acceptance gate:** For every required test provide exact SHA -> test ID -> mapped check/native gate -> trigger -> actual run URL/outcome. Missing test, registration, mapping, selection, trigger or real passing execution BLOCKS acceptance. Docker/rootless Podman each require independent live evidence when applicable; do not rerun unaffected checks needlessly.


- **Test binding (select exactly one):**  normal (auto-discovered) ·  contract  add to `REQUIRED_CLIENT_TESTS` or the package equivalent in the same PR ·  new check  update `scripts/pr-gate-plan.py` and `scripts/release-requirements.json` in the same PR.
- Name every new or changed test (package, exact test ID, fixture/env and native runtime if applicable). Targeted checks for the changed area; broaden when impact is unknown.
- Record the existing CI validation/check or Docker/Podman native gate that actually executes each test, and which PR paths, develop integration event or release candidate selection triggers it.
- If coverage is absent, implement/register it in the owning CI lane before acceptance; prove positive selection for a relevant change and negative/non-selection for an unrelated change. Missing, skipped or failed mandatory execution is NOT PASS.
- For Docker/Podman tests, prove native Docker and rootless Podman/Quadlet separately where required; unit fakes do not replace live runtime evidence. Cross-repo tests run through existing develop/release acceptance, not a blocking independent PR gate.
- Handoff must identify exact source SHA, test -> CI gate -> trigger -> actual run/outcome, or mark explicit CI coverage debt as blocking. No new CI framework or full automatic PR matrix.

## Dependencies and file ownership

- Owned files or areas:
- Shared files: coordinate through the owning task.

## Handoff

- Current state, branch, PR and evidence links. Newest first.

## Finding (2026-11-22, measured from the attempt-3 hosted logs)

Docker native job `137133647957` and Podman native job `137133625738` (run `44994268323`, head `a40b76764c3`) print:
```
app_capability_runtime_test.go:136: [app apply --skip-memory-preflight]: Starting secure runtime broker:
  application runtime broker readiness failed: application runtime broker container health is unhealthy;
  runtime diagnostics:\n            <- NOTHING follows, the payload is empty
```
The message is built in `cmd/baha/app_broker.go:206`; the unhealthy-state strings come from
`cmd/baha/app_broker.go:348-352` and `:416`. The broker's own `/readyz` handler DOES name dependencies
(`internal/controlplaneruntime/server_run.go:166-206`, `server.go:260-274` writes `dependency` when non-empty) and logs
`runtime broker readiness failed: dependency=<name> error=...` - none of that reaches the CLI error, so the hosted log
cannot tell database vs openbao vs runtime-executor apart.

## Fix recipe (lane-allowed files only)

Make the diagnostics builder in `cmd/baha/app_broker.go` (around `:180-210`) collect what it promises: container log
tail plus the last `/readyz` body, each capped and redacted of secret values, so the failure line names the dependency.
No product semantics change, no new API, and do NOT touch `internal/observability/registry.go` or
`internal/capability/perses_selection.go`. Add/extend a test that asserts the dependency name appears in the error when
`/readyz` reports a named dependency. Evidence must be a hosted native run (docker+podman) whose output now carries the
dependency name.

mission ist zweimal zugestellt und wurde NICHT ausgefuehrt: der sitz 03c7350a ging nach der zustellung sofort wieder idle, es gibt weder branch lane-0428-240-broker-diagnostics noch eine akte. Die karte bleibt darum auf wait und behauptet keine lebende lane. Naechster trigger: der erste freie AUSFUEHRENDE worker-sitz (b90e4ba1, 0847d100, f0f6c8b4 oder ffe7611b, sobald deren laufende hops/reviews endet sind) - die mission liegt fertig unter /var/tmp/m/fix240.md.g. Wenn die rotation von 03c7350a nicht kommt, ist das ihr einziger dauerhafter ausfallender platz: fuenf von sechs arbeitsplaetzen liefern, einer replayt alten kontext (zuletzt eine END-hinweis zu karte 0428-225 und PR 1751, die um 00:26:05Z gemergt wurden).
