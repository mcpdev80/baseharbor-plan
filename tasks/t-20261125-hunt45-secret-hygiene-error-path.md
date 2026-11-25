---
id: t-20261125-hunt45-secret-hygiene-error-path
card_number: "0428-324"
card_short_title: "scrub external runtime stderr"
type: bug
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Secret hygiene on the CLI error path: scrub external runtime stderr before it becomes a user-facing error message, and zero the…"
kanban_title: 0428-324 · scrub external runtime stderr
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

- [ ] t-20261125-hunt45-secret-hygiene-error-path · CLI: scrub external runtime stderr and zero dev credential buffers #task #release/v0-4-28 #status/planned #view/ready #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
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

Secret hygiene on the CLI error path: scrub external runtime stderr before it becomes a user-facing error message, and zero the dev credentials buffer after rendering, matching the export path's hygiene. Hunt H-V45 F5.

## Scope

- In scope: internal/runtime/compose_command.go (the three stderr-embed sites: lines ~20-24, ~60-66, ~90-96), cmd/baha/dev_access.go credentials handling (zero after render, JSON branch at :203), a shared scrub helper in internal/cli or internal/apierror, leak-detection test with a poisoned secret value on failing compose and the reveal path.
- Out of scope: changing the deliberate reveal seams themselves (app connect PASSWORD/URI masking, dev credentials stdout reveal by design - F5 positive controls stay); .github/** triggers.

## Acceptance

- Each criterion as a plain bullet.
- A failing `docker/podman compose` invocation whose stderr contains a poisoned secret value renders without that value in the user-facing error (test asserts absence), while the command/args context is kept.
- cmd/baha/dev_access.go zeroes the password buffer after rendering on all paths including --json (defer zeroBytes on the []byte form).
- The scrub helper is used by every compose stderr-capture site (grep witness: no remaining raw `fmt.Errorf("compose %s: %s"` with unsanitized message).

## Required checks

- **Modified features:** Inventory and adapt all affected existing unit, contract, integration, regression, E2E and native-runtime tests; add missing cases.
- **New features/providers (e.g. Perses Provider Contract):** Implement NEW dedicated positive, negative, authorization, ownership, error-path, compatibility and lifecycle tests wherever relevant. Passing unrelated existing suites is not sufficient.
- **CI integration and mapping are part of implementation:** Register every new/changed test in its package/test inventory and update existing test-to-gate mapping, selectors, relevant `REQUIRED_CLIENT_TESTS`/package equivalent, `scripts/pr-gate-plan.py`, `scripts/release-requirements.json`, and CI workflow paths/triggers where applicable. Coordinate reserved CI files with their owner; no new CI framework.
- **Mapping selection proof:** Verify affected paths select the required tests, unrelated paths do not unnecessarily select them, and the applicable stacked-PR, ready-for-review, develop and release workflows cannot silently bypass them. Unknown coverage broadens selection instead of failing open.
- **Hard acceptance gate:** For every required test provide exact SHA -> test ID -> mapped check/native gate -> trigger -> actual run URL/outcome. Missing test, registration, mapping, selection, trigger or real passing execution BLOCKS acceptance. Docker/rootless Podman each require independent live evidence when applicable; do not rerun unaffected checks needlessly.


- **Test binding:** normal (auto-discovered) Go unit tests in internal/runtime and cmd/baha packages.
- Name every new or changed test (package, exact test ID, fixture/env and native runtime if applicable). Targeted checks for the changed area; broaden when impact is unknown.
- Record the existing CI validation/check or Docker/Podman native gate that actually executes each test, and which PR paths, develop integration event or release candidate selection triggers it.
- If coverage is absent, implement/register it in the owning CI lane before acceptance; prove positive selection for a relevant change and negative/non-selection for an unrelated change. Missing, skipped or failed mandatory execution is NOT PASS.
- For Docker/Podman tests, prove native Docker and rootless Podman/Quadlet separately where required; unit fakes do not replace live runtime evidence. Cross-repo tests run through existing develop/release acceptance, not a blocking independent PR gate.
- Handoff must identify exact source SHA, test -> CI gate -> trigger -> actual run/outcome, or mark explicit CI coverage debt as blocking. No new CI framework or full automatic PR matrix.


Hunt note: no container or compose project runs on the coordinator host; the leak-detection test uses a fake runtime command (or the named baha-docker/baha-podman hosts via existing native gates) and must be selected by the ordinary PR Go-unit path.

## Dependencies and file ownership

- Owned files or areas: as listed in Scope.
- Shared files: docs/reference/cli.md and docs/reference/errors.md are shared with the sibling H-V45 cards (0428-321/322/323) - coordinate to avoid overlapping rewrites.

## Handoff

- Cast from bug hunt H-V45 (Funde->Karte-Pflicht), intake akte evidence/r28-welle6-2026-11-27/bughunt-hv45-cli-errors/intake-1.md, anchor develop 2a141387dbbaf24f52501a0f66f1abf61cf8fcda (verified live at intake). Unassigned; no branch or PR yet.
