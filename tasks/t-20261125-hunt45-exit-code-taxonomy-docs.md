---
id: t-20261125-hunt45-exit-code-taxonomy-docs
card_number: "0428-321"
card_short_title: "document baha exit-code"
type: bug
areas: []
release: v0.4.28
version: ""
parent: ""
owner: "w364-0428-321-1866rerun"
kanban_status: active
kanban_lane: active
kanban_summary: "Document the baha process exit-code taxonomy at the user-facing surface: 0 success, 1 runtime failure, 2 usage error, 130…"
kanban_title: 0428-321 · document baha exit-code
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1866"]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261125-hunt45-exit-code-taxonomy-docs · CLI: document baha exit-code taxonomy and machine coverage check #task #release/v0-4-28 #status/active #view/active #kind/bug
    <!-- generated:card -->
    **Owner:** w364-0428-321-1866rerun  
    **PR:** [baseharbor#1866](https://github.com/mcpdev80/baseharbor/pull/1866)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w364-0428-321-1866rerun  
**Priority:** not set  
**PRs:** [baseharbor#1866](https://github.com/mcpdev80/baseharbor/pull/1866)  
**Source:** 
<!-- /generated:links -->

## Goal

Document the baha process exit-code taxonomy at the user-facing surface: 0 success, 1 runtime failure, 2 usage error, 130 SIGINT, 143 SIGTERM, plus the `baha app exec` child-status passthrough (1-255), and keep the documentation honest with a machine-coverage check. Hunt H-V45 F1 (see intake mapping).

## Scope

- In scope: docs/reference/cli.md (new exit-code section), docs/reference/errors.md (cross-link from outcome classes to process exit codes), scripts/ documentation-audit or CLI contract test asserting the documented set matches cli.ExitCode behavior.
- Out of scope: changing any exit-code behavior itself (card 0428-322 owns the app exec collision decision).

## Acceptance

- Each criterion as a plain bullet.
- docs/reference/cli.md states each code, where it originates (file:line anchors: internal/cli/cli.go:113-127, cmd/baha/main.go:61-63,83-86) and that `baha app exec` passes the child status through; docs/reference/errors.md links the outcome classes to these codes.
- A check (test or scripts/documentation-audit.sh row) fails if cli.ExitCode produces a code outside the documented set or the docs document a code the implementation cannot produce.
- Hunt akte: https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-27/bughunt-hv45-cli-errors/hunt-1.md (finding F1).

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

- Owned files or areas: as listed in Scope.
- Shared files: docs/reference/cli.md and docs/reference/errors.md are shared with the sibling H-V45 cards (0428-321/322/323) - coordinate to avoid overlapping rewrites.

## Handoff

- Cast from bug hunt H-V45 (Funde->Karte-Pflicht), intake akte evidence/r28-welle6-2026-11-27/bughunt-hv45-cli-errors/intake-1.md, anchor develop 2a141387dbbaf24f52501a0f66f1abf61cf8fcda (verified live at intake). Unassigned; no branch or PR yet.
