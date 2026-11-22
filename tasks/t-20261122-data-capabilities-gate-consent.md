---
id: t-20261122-data-capabilities-gate-consent
card_number: "0428-236"
card_short_title: "data-capabilities native gate"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: b90e4ba1 (lane, STOP belegt)
tags: [#task, #release/v0.4-28]
kanban_status: closed
kanban_lane: closed
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-236 · data-capabilities native gate
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor-demo]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: dropped
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/gate-admission-census/demo-consent-0428-236/round-1.md", "https://github.com/mcpdev80/baseharbor/actions/runs/44994268323"]
---

- [x] t-20261122-data-capabilities-gate-consent · demo: pass candidate consent in the data-capabilities native gate #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** b90e4ba1 (lane, STOP belegt)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle5-2026-11-22/gate-admission-census/demo-consent-0428-236/round-1.md), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44994268323)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** dropped  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** b90e4ba1 (lane, STOP belegt)  
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

## Finding (2026-11-22, first real run of the newly admitted native gate)

`PR #1753` exact head `a40b76764c3c08ec690e723def0ca167ce989c2b`, run `44994268323`: `PR · Native · native/docker/`
`data-capabilities` job `137121839425` and `PR · Selected Runtime (atomic/docker/data-capabilities)` job `137122169353`
FAILED at step 19 `Run runtime gate`; podman sibling `137122169299` still running at measurement. Log witness
(`gh api .../actions/jobs/137122169353/logs` lines 1690, 2299-2322):

```
Error: record deployment before mutation: candidate submission requires an explicit operator/automation consent
  (--confirm-candidate); refusing to record deployment
Re-run with --confirm-candidate 3b332ee5c8c1... to acknowledge this exact submission.
RuntimeError: actual native CLI JSON/MCP Footprint contracts differ
demo-data-capabilities  FAIL   RESULT FAIL
```

Cause: the deployment path in the data-capabilities gate reaches `cmd/baha/app_apply.go:194` ->
`cmd/baha/app_candidate_consent.go:154` without the consent retry that the demo harness already implements
(`baseharbor-demo/tests/fixture-consent.py:36-73` re-runs with the digest; `tests/lib.sh` and
`scripts/acceptance.sh` use it) - but `baseharbor-demo/tests/data-capabilities/run.sh` (44 lines) does not take that
path, so the first apply attempt aborts and the follow-on footprint comparison then differs.

Fix recipe: make the data-capabilities gate apply through the shared consent helper (detect `--confirm-candidate`,
parse the 64-hex digest from `Re-run with --confirm-candidate <digest>`, retry once with it) exactly as
`tests/guided/drive.py:37` does; assert the retry in the gate's own log so the evidence is machine-readable.
Scope: `baseharbor-demo` only (lane-writable); no `cmd/baha` semantics change; the consent guard stays.
Cards touched by the same guard elsewhere: 0428-061 (PR #1627) and 0428-232 (demo MCP golden list).

STOP angenommen, karte ohne defekt: der consent-retry sitzt bereits auf dem apply-pfad des gates (ueber den PTY-weg), es gibt also LUECKE, die sich im demo-scope andocken liesse, ohne den core zu aendern. Die lane hat die pruefung mit datei:zeilen belegt (gate-admission-census/demo-consent-0428-236/round-1.md, plan main e516dcfd9). Damit ist mein zweiter fund aus dem 1753-log (die 'requires an explicit operator/automation consent'-zeile) erklaert: er war sekundaer und ist kein separater arbeitsbedarf. Der blockierer bleibt ausschliesslich der broker-readiness-pfad (karte 0428-237).
