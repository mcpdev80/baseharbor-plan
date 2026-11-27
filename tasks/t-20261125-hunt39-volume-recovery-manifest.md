---
id: t-20261125-hunt39-volume-recovery-manifest
card_number: "0428-312"
card_short_title: "assert recovery-manifest"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: Marcel (Owner) 2026-11-27; w365 executing
kanban_status: blocked
kanban_lane: blocked
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-312 · assert recovery-manifest
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: ["1860"]
sources: []
blocker: "PR Trusted Plan fails ValueError uncataloged source change internal/applicationbackup/recovery_manifest_workload_test.go read at resolved effective base 5a37ddbd (predates this PR catalog fix). Merge-commit re-hop shape (f3dc7b6) trips pr-diff-base.py:186 integration_sha_mismatch 'integration merge must include PR head as one of exactly two parents'. No commit shape passes; same base/lineage + catalog-read-at-base class as w361 (0428-299/#1863). Outside worker write-set; requires Codex/Owner resolver fix. Candidate 6deab9ff68d15060525cc3078e828027e65e9955."
wait_reason: ""
resolution: ""
evidence: ["evidence/board-2026-11-27/0428-312/w365-0428-312-1860hop/akte.md"]
---

- [ ] t-20261125-hunt39-volume-recovery-manifest · 0428 hunt H-V39: assert recovery-manifest coverage for workload volumes #task #release/v0-4-28 #status/blocked #view/blocked #kind/task
    <!-- generated:card -->
    **Owner:** Marcel (Owner) 2026-11-27; w365 executing  
    **PR:** [baseharbor#1860](https://github.com/mcpdev80/baseharbor/pull/1860)  
    **Blocker:** PR Trusted Plan fails uncataloged source change internal/applicationbackup/recovery\_manifest\_workload\_test.go (ValueError) read at resolved base 5a37ddbd which predates this PR catalog fix; merge-commit shape fails pr-diff-base.py 186 inte…  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** Marcel (Owner) 2026-11-27; w365 executing  
**Priority:** not set  
**PRs:** [baseharbor#1860](https://github.com/mcpdev80/baseharbor/pull/1860)  
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

w365 Re-Hop + Qualifikation on existing card 0428-312 PR 1860 branch w333-0428-312-volrecovery. Candidate 6deab9ff. Verified resolver reads coverage catalog at effective base 5a37ddbd where introducing source is not cataloged; re-hop forward-merge produces merge commit f3dc7b6 that trips line 186. END_BLOCKED no blind retry. Evidence evidence/board-2026-11-27/0428-312/w365-0428-312-1860hop/akte.md
