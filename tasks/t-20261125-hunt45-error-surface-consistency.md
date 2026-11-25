---
id: t-20261125-hunt45-error-surface-consistency
card_number: "0428-323"
card_short_title: "centralize error"
type: bug
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Consistent, actionable machine error surface: every machine ErrorCode has one canonical remediation vocabulary (starting with…"
kanban_title: 0428-323 · centralize error
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

- [ ] t-20261125-hunt45-error-surface-consistency · CLI: centralize error classification, canonical auth hints and Next/Remediation discipline #task #release/v0-4-28 #status/planned #view/ready #kind/bug
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

Consistent, actionable machine error surface: every machine ErrorCode has one canonical remediation vocabulary (starting with authentication_failed naming the concrete command), every partial-completion/ownership conflict error carries a non-empty Next, and the Remediation class enum is declared. Cluster of hunt H-V45 F2, F4, F7, F8.

## Scope

- In scope: internal/machine/contract.go (Classify registry / registration seam for internal sentinels), cmd/baha/main.go classifyMachineCLIError, cmd/baha/mcp.go:331-334, cmd/baha/node_owner_context.go:26, cmd/baha/node_disconnect_client.go:29,216, cmd/baha/node.go:414, internal/operatorauth/authorization.go:204-206, the nine Next-less machine.Error literals listed in the akte F7 table, docs/reference/errors.md (remediation enum declaration).
- Out of scope: auth/consent SEMANTICS (no guard is weakened; hints only), exit-code documentation (0428-321), app exec envelope (0428-322).

## Acceptance

- Each criterion as a plain bullet.
- One canonical Next string per authentication-denial site for the same error class, naming `baha login` with its Target/environment argument; the akte F2 variant list is resolved to it.
- All nine F7 machine.Error literals (plus CauseCode at cmd/baha/node_disconnect_client.go:216) carry a concrete Next.
- A test asserts every exported internal sentinel reachable from the CLI JSON surface classifies to a non-internal_error code, or a central registration table maps it (F4).
- Remediation values are restricted to the declared enum in docs/reference/errors.md; snake_case `operator_review` and the three free-sentence sites are normalized, their sentences moved to Next (F8).

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
