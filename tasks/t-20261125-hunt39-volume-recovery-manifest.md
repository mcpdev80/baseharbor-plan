---
id: t-20261125-hunt39-volume-recovery-manifest
card_number: "0428-312"
card_short_title: "manifest volume coverage"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Pin existing recovery behavior with tests: selected application-owned workload volumes must appear in the archive manifest and…"
kanban_title: 0428-312 · manifest volume coverage
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/cmd/baha/app_recovery_selection.go#L48-L58","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/cmd/baha/app_recovery_selection.go#L148-L240","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/cmd/baha/app_backup_restore_data.go#L110-L120","https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/cmd/baha/app_backup_restore_data.go#L197-L254","https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-26/bughunt-hv39-backup-restore/akte.md"]
---

- [ ] t-20261125-hunt39-volume-recovery-manifest · 0428 hunt H-V39: assert recovery-manifest coverage for workload volumes #task #release/v0-4-28 #status/planned #view/ready #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/cmd/baha/app_recovery_selection.go#L48-L58), [proof 2](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/cmd/baha/app_recovery_selection.go#L148-L240), [proof 3](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/cmd/baha/app_backup_restore_data.go#L110-L120), [proof 4](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/cmd/baha/app_backup_restore_data.go#L197-L254), [proof 5](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-26/bughunt-hv39-backup-restore/akte.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Pin existing recovery behavior with tests: selected application-owned workload volumes must appear in the archive manifest and payload, while external or bind-mounted data remains explicitly excluded. A manifest/payload mismatch must fail before restore mutation.

## Scope

- In scope: tests for workload-volume discovery, manifest encoding, and manifest-to-payload validation using existing unit or CLI test seams.
- Out of scope: changing which storage is owned or selected by default, altering destroy semantics, or adding a new native CI pipeline.

## Acceptance

- A declared, materialized application-owned workload volume is represented as a selected supported contributor and its logical resource is included in the recovery payload.
- Bind mounts and external named volumes remain explicit excluded/external contributors and are not treated as application-owned backup data.
- Missing or unexpected workload-storage payload entries relative to the selected manifest are rejected before mutation.
- Bind the focused tests to their existing package/gate and record the exact source SHA and execution evidence in handoff.

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

## Task

Cast from hunt H-V39 (akte origin/main ac6b10bfa, evidence/r28-welle6-2026-11-2[67]/bughunt-hv39* - exact path in commit): F4 - workload-volume recovery-manifest assertion missing; add test asserting every workload volume appears in the recovery manifest (fail-closed on omission).
