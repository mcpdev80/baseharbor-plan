---
id: t-20261122-runtime-broker-health-unhealthy
card_number: "0428-237"
card_short_title: "data-capabilities native gate"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: 0847d100 (rerun + diagnose)
tags: [#task, #release/v0.4-28]
kanban_status: active
kanban_lane: active
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-237 · data-capabilities native gate
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/44994268323"]
---

- [ ] t-20261122-runtime-broker-health-unhealthy · CI: data-capabilities native gate fails on secure runtime broker readiness #task #release/v0-4-28 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** 0847d100 (rerun + diagnose)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/44994268323)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** 0847d100 (rerun + diagnose)  
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

## Finding (2026-11-22, exact-head run of PR #1753)

Run `44994268323` at head `a40b76764c3c08ec690e723def0ca167ce989c2b` (base `52a3c5446f4`) FAILED both engines on the
same test: `PR · Native · native/docker/data-capabilities` job `137121839425`, `PR · Native · native/podman/`
`data-capabilities` job `137121839379`, and their `PR · Selected Runtime` siblings `137122169353` (docker) /
`137122169299` (podman); aggregate `PR Selected Checks` `137124048433` failure. Both fail inside
`TestApplicationCapabilityLifecycleExistingCore/secrets` while *starting the secure runtime broker*: the broker
container reports unhealthy and its readiness endpoint answers `503 not_ready`; timeouts ~2m (docker) / ~5m (podman).
The mTLS identity check immediately before it passes, so this is broker readiness/fixture behaviour - NOT a footprint
CLI assertion and NOT candidate-introduced content (the hop diff is develop-only).

Steps: (1) rerun the failed jobs at the exact same head to classify transient vs deterministic; (2) read the broker
start path and the fixture's readiness wait, cite file:line; (3) decide fix owner: `internal/observability/registry.go`
and `internal/capability/perses_selection.go` are lane-banned, so a readiness/fixture change needs a named owner.
History: `t-20261102-broker-ready3-widen-readiness-grace` was closed as dropped, `0427-118` (ORAS edge readiness) was
accepted - neither covers a `503 not_ready` broker health failure in this suite.
Evidence: run `https://github.com/mcpdev80/baseharbor/actions/runs/44994268323`.

triage ist aktiv auf sitz 03c7350a: rerun der fehlgeschlagenen jobs am exakten head 44994268323 (transient oder deterministisch), danach datei:zeilen-kette fuer den broker-start und die readiness-warte-schleife. Schreibsperren beachten: internal/observability/registry.go und internal/capability/perses_selection.go sind Lane-gesperrt.

RERUN AM EXAKTEN head a40b76764c3 ist GELAUFPEN (attempt 3 von run 44994268323) und zeigt dieselbe signatur: docker selected-runtime job 137133627704 FAILED, podman selected-runtime job 137133627980 FAILED, docker native job 137133647957 FAILED, podman native 137133625738 bei meiner messung noch aktiv. URAECHIERNUNG: DER FEHLER IST DETERMINISTISCH, NICHT TRANSIENT. Rueckstand: PR 1753 ist hinter develop acc34323968 zurueck (1627 ist gemergt), jeder weitere beweis braucht also erst einen frischen hop. Die diagnosis-akte der lane (rerun-tabelle + datei:zeilen-kette) steht noch aus; der naechste schritt ist die ursaechen-kette im broker-start/pfad der readiness-warte-schleife - wenn sie in internal/observability/registry.go oder internal/capability/perses_selection.go landet, entscheidet der Owner ueber den fix-besitzer, weil beide pfade Lane-gesperrt sind.
