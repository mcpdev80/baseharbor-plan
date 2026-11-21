---
id: t-20261122-impact-consent-after-preview-contract
card_number: "0428-226"
card_short_title: "impact consent validated after"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: w21-pr1702-0428-142-compat
kanban_status: active
kanban_lane: active
kanban_summary: Define and enforce one consent contract for env destroy so that an impact consent produced by a preview is still authoritative…
kanban_title: 0428-226 · impact consent validated after
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261122-impact-consent-after-preview-contract · Env destroy: impact consent validated after preview is structurally stale (five fixture rounds) #task #release/v0-4-28 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** w21-pr1702-0428-142-compat  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w21-pr1702-0428-142-compat  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Define and enforce one consent contract for `env destroy` so that an impact consent produced by a preview is still
authoritative when the destroy applies it, on both Docker and rootless Podman. Today the equality test between the
preview consent and the destroy-time authorization fails, and the native test
`TestEnvironmentDestroyNativeLifecycle` reports `stale impact consent after preview` in hosted CI.

## Scope

- In scope: the consent issuance/validation path that the destroy authorization checks (preview object identity,
  resolved deployment UUID, stop-plan/stop-mode binding and the runtime retirement binding), plus the native test
  fixture that has to present exactly the production shape.
- Out of scope: weakening or removing the stale-consent protection; any change that lets a destroy run without a
  freshly authorised plan.

## Acceptance

- A single documented contract states which fields bind a preview consent to its destroy apply, and where each field is
  re-resolved at apply time.
- `TestEnvironmentDestroyNativeLifecycle` executes (not skips) and passes on the exact candidate SHA in hosted CI for
  both the Docker and the rootless Podman coreless-lifecycle shards.
- One deterministic assertion proves the consent is rejected when the resolved target changes after preview, so the
  protection is regression-tested, not just satisfied.
- The five-round fixture-patch sequence on PR #1627 is replaced by at most one further change round whose diff names
  the contract line it satisfies.

## Required checks

- **Modified features:** Inventory and adapt all affected existing unit, contract, integration, regression, E2E and native-runtime tests; add missing cases.
- **New features/providers (e.g. Perses Provider Contract):** Implement NEW dedicated positive, negative, authorization, ownership, error-path, compatibility and lifecycle tests wherever relevant. Passing unrelated existing suites is not sufficient.
- **CI integration and mapping are part of implementation:** Register every new/changed test in its package/test inventory and update existing test-to-gate mapping, selectors, relevant `REQUIRED_CLIENT_TESTS`/package equivalent, `scripts/pr-gate-plan.py`, `scripts/release-requirements.json`, and CI workflow paths/triggers where applicable. Coordinate reserved CI files with their owner; no new CI framework.
- **Mapping selection proof:** Verify affected paths select the required tests, unrelated paths do not unnecessarily select them, and the applicable stacked-PR, ready-for-review, develop and release workflows cannot silently bypass them. Unknown coverage broadens selection instead of failing open.
- **Hard acceptance gate:** For every required test provide exact SHA -> test ID -> mapped check/native gate -> trigger -> actual run URL/outcome. Missing test, registration, mapping, selection, trigger or real passing execution BLOCKS acceptance. Docker/rootless Podman each require independent live evidence when applicable; do not rerun unaffected checks needlessly.

- **Test binding (select exactly one):** ☐ normal (auto-discovered) · ☐ contract → add to `REQUIRED_CLIENT_TESTS` or the package equivalent in the same PR · ☐ new check → update `scripts/pr-gate-plan.py` and `scripts/release-requirements.json` in the same PR.
- Name every new or changed test (package, exact test ID, fixture/env and native runtime if applicable). Targeted checks for the changed area; broaden when impact is unknown.
- Record the existing CI validation/check or Docker/Podman native gate that actually executes each test, and which PR paths, develop integration event or release candidate selection triggers it.
- If coverage is absent, implement/register it in the owning CI lane before acceptance; prove positive selection for a relevant change and negative/non-selection for an unrelated change. Missing, skipped or failed mandatory execution is NOT PASS.
- For Docker/Podman tests, prove native Docker and rootless Podman/Quadlet separately where required; unit fakes do not replace live runtime evidence. Cross-repo tests run through existing develop/release acceptance, not a blocking independent PR gate.
- Handoff must identify exact source SHA, test -> CI gate -> trigger -> actual run/outcome, or mark explicit CI coverage debt as blocking. No new CI framework or full automatic PR matrix.

## Dependencies and file ownership

- Owned files or areas: the consent issuance/validation path in the destroy authorization, and the native destroy test
  fixture. The `env destroy` branch `cli2-env-delete` (PR #1627) stays Owner-owned; this card does not take it over.
- Shared files: coordinate through the owning task.

## Handoff

- Origin of this card: five consecutive failed attempts on one assertion in
  `cmd/baha/env_destroy_integration_test.go:128` (`stale impact consent after preview`) across heads `8de37f58caa`,
  `62dd38f9b6d`, `ac05cc4efbc`, `38be89aa4a0` and `b3b0c2c9efc`. Both required engine shards failed on the exact run
  `44961334018`: Docker job `137020935578` and Podman job `137020935792`, log lines 1178-1192 resolving
  `prod/docker-dev` and the target deployment.
- Current state: PR #1627 (`0428-055`) is held from review and merge; a read-only diagnosis of the preview-to-apply
  consent path is dispatched and its artefact will be linked here.

STELLE BESATZT, coordinator-auftrag 02:5xZ. grund fuer den namen: die FRISCHE Lane w226-pr1627-0428-226-consent konnte nicht gestartet werden, weil 'worker-cleanup.sh w21-pr1702-…' mit PARTIAL 'session/OpenCode release incomplete' endete (tooling issue #6) und spawn-lane.sh deshalb ADMISSION-HOLD 'POOL-UNKNOWN: live worker without pool reservation' meldet. der sitz 0847d100 (w21) fuehrt diese karte daher in derselben session weiter - AGENTS 3.6 erlaubt das ausdruecklich als explizite uebergabe, und dieselbe session hat die diagnose bereits geliefert. PR-FELD bleibt leer, bis die lane ihren eigenen branch/PR eroffnet; integration in #1627 erfolgt erst, wenn der fix mit dem dann exakten develop 7d4351c6d64 bereit ist.
