---
id: t-20261125-hunt45-app-exec-exit-collision
card_number: "0428-322"
card_short_title: "decide app exec exit-status"
type: bug
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Decide and enforce the baha app exec exit-status passthrough contract so a child process exit code is not confusable with baha's…"
kanban_title: 0428-322 · decide app exec exit-status
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

- [ ] t-20261125-hunt45-app-exec-exit-collision · CLI: decide app exec exit-status passthrough collision with reserved codes #task #release/v0-4-28 #status/planned #view/ready #kind/bug
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

Decide and enforce the `baha app exec` exit-status passthrough contract so a child process exit code is not confusable with baha's reserved exit codes 1 and 2 from the process status alone. Hunt H-V45 F3.

## Scope

- In scope: cmd/baha/app_exec.go (preserveWorkloadExitStatus, cli.WithExitCode site), internal/cli/cli.go ExitCode interaction, docs/reference/cli.md app exec section (owned jointly with 0428-321 - coordinate the same docs file, 0428-321 adds the taxonomy section this card extends), a regression case for a child exiting 2.
- Out of scope: weakening the Presented double-render guard (F10 positive control holds); changing machine contract membership for app exec (docs/reference/cli-machine-coverage.md:27 keeps it excluded unless the decision says otherwise).

## Acceptance

- `baha app exec` passes through the child process exit code unchanged, including 1 and 2; CLI invocation failures remain separately described by their command context and diagnostics.
- Document this contract in `docs/reference/cli.md` and correct the comment that claims the child can never return a reserved usage code.
- Add a regression for a child returning exit code 2 and assert the exact passthrough result.
- Use the existing CLI Go test check; no new CI pipeline.


## Owner decision — 2026-11-25

The child process exit code is passed through unchanged. Exit values 1 and 2 may therefore also originate from the child; document that fact and keep BaseHarbor invocation failures distinguishable by their diagnostic/context rather than changing the child status.

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
