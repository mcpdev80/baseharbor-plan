---
id: t-20261116-keycloak-metrics-signal-unregistered
card_number: "0428-097"
card_short_title: "register keycloak-metrics"
type: task
areas: [runtime, capability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: coord
kanban_status: closed
kanban_lane: planned
kanban_summary: "Make the declared keycloak-metrics native signal actually resolvable at runtime so the identity fan-in gate can ever be true."
kanban_title: 0428-097 · Register keycloak-metrics signal
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1660]
sources: [evidence/r28-welle2-2026-11-16/perses-dashboard-identity/on-resolver-round-2.md]
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1660"]
---

- [ ] t-20261116-keycloak-metrics-signal-unregistered · Runtime: register keycloak-metrics native signal in observability registry #task #release/v0-4-28 #status/planned

## Goal

The keycloak-metrics ProviderObservabilitySignal declared in internal/capability/reference.go (Keycloak provider descriptor, ~line 160) is never registered in the observability registry the runtime fan-in reads, so perses_identity_witness matching (perses_identity_witness.go:16/117) can never hit a registered source and identity_dashboard_eligible (cmd/baha/app_status_result.go:161) is permanently false. Register the signal on the real registry path (or wire the provider into it) with a regression proving an eligible positive once signal+target-auth exist, without weakening fail-closed elsewhere.

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


- **Test binding (select exactly one):** ☐ normal (auto-discovered) · ☐ contract → add to `REQUIRED_CLIENT_TESTS` or the package equivalent in the same PR · ☐ new check → update `scripts/pr-gate-plan.py` and `scripts/release-requirements.json` in the same PR.
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

merged 2026-11-17T03:30:15Z als 1df7c343 (Luna CODEX-MERGE welle1c, identity-check sauber)
