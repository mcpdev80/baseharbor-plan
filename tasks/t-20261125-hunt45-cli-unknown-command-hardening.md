---
id: t-20261125-hunt45-cli-unknown-command-hardening
card_number: "0428-325"
card_short_title: "unknown-command exit-2"
type: bug
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Guarantee unknown-command handling and share hint construction in the CLI layer: baha <garbage> must fail with exit 2 plus a…"
kanban_title: 0428-325 · unknown-command exit-2
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

- [ ] t-20261125-hunt45-cli-unknown-command-hardening · CLI: unknown-command exit-2 guarantee and suggestion construction under runnable parents #task #release/v0-4-28 #status/planned #view/ready #kind/bug
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

Guarantee unknown-command handling and share hint construction in the CLI layer: `baha <garbage>` must fail with exit 2 plus a suggestion even when a parent has both children and a Run func, and one helper builds the Did-you-mean/--help hints. Cluster of hunt H-V45 F6 and F9.

## Scope

- In scope: internal/cli/cli.go Execute dispatch (lines 148-165), SuggestClosest vs Command.suggest unification (cli.go:431-471), cmd/baha/ux.go unknownOptionUsage hint sharing, a cli.Execute regression test for unknown subcommands under a runnable parent, and a blank-Hint guard so a trimmed-empty UsageError hint cannot silently vanish at render (cmd/baha/main.go:276).
- Out of scope: product behavior changes beyond the dispatch guard/test; doctor prose style is a note only.

## Acceptance

- Each criterion as a plain bullet.
- A cli-package regression test asserts exit 2 + suggestion text for an unknown subcommand under a runnable parent (or a static assertion that children+Run is rejected at registration) - red if the guard is removed.
- One helper produces the "Did you mean ... / Run --help" hint at all three sites (cli.go unknown command, cli.go unknown flag path, ux.unknownOptionUsage); SuggestClosest and Command.suggest share the distance/ordering logic.
- usageError (or the Execute path) rejects blank hints so a whitespace-only Hint cannot reach the renderer silently.

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
