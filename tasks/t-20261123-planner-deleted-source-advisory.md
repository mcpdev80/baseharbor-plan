---
id: t-20261123-planner-deleted-source-advisory
card_number: "0428-253"
card_short_title: "candidate planner mishandles"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: "" (ghost-claim demoted 09:0xZ batch reconcile: implementing lane long released; content disposition stands on the card evidence; re-activation needs Codex/Owner per existing chain holds)
kanban_status: wait
kanban_lane: wait
kanban_summary: "The candidate-added validation lane treats a DELETED product source with a removed catalog row as resolved-by-deletion, not as…"
kanban_title: 0428-253 · candidate planner mishandles
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

- [ ] t-20261123-planner-deleted-source-advisory · CI: candidate planner mishandles deleted source rows (advisory job red) #task #release/v0-4-28 #status/wait #view/wait #kind/task
    <!-- generated:card -->
    **Owner:** "" (ghost-claim demoted 09:0xZ batch reconcile: implementing lane long released; content disposition stands on the card evidence; re-activation needs Codex/Owner per existing chain holds)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** "" (ghost-claim demoted 09:0xZ batch reconcile: implementing lane long released; content disposition stands on the card evidence; re-activation needs Codex/Owner per existing chain holds)  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

The candidate-added validation lane treats a DELETED product source with a removed catalog row as resolved-by-deletion, not as an uncataloged change, so PRs that delete dead tagged tests (precedent #1789, job 1373... 137410039120) no longer surface a red advisory while required Trusted Plan stays green.

## Scope

- In scope: scripts/pr-gate-plan.py candidate-planner path that resolves changed/deleted source rows (classify deletion before demanding an owner); one regression proving a deleted-source PR yields green advisory.
- Out of scope: any change to required Trusted Plan semantics; .github workflows; catalog content of other PRs. The base-precedence policy itself is intentional and stays.

## Acceptance

- On a re-run of the #1789-shaped candidate diff, the candidate-added checks job passes without weakening required checks.
- Regression test is CI-executed (package-discovered), named in the handoff with exact candidate SHA.

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

Erste zwei Übernahmen als gekürzte Identität der eigenen Bahn übernommen (w205 ≙ w205-0428-253), Eigentümer-Erkenntnis 25.11., keine Umschreibung.

## Owner ruling

The owner admits only the first two chronological `w205`-authored historical commits in this card's lane history: `201fb31ab73a7d08359140c30577bcdfeee2ca54` (`claim t-20261123-planner-deleted-source-advisory: w205 (lane w205-0428-253)`) and `1077381e44dfe3d57e4d1a344e3c2cbd7f55cd7a` (`evidence(w205-0428-253): planner deleted-source advisory (draft, CI watch pending)`). Both have author `w205 <w205@baseharbor.local>`; here `w205` is shortened same-lane formatting for `w205-0428-253`. This is a narrowly scoped historical identity classification: no history rewrite was used or authorized, and it does not admit foreign-lane identities or authorize shortened identities for new commits. Foreign-lane evidence remains rejected and requires Coordinator recovery/republication; the exception is not generalized.

Provenance: executing lane `w255-0428-251-demo170codex`; branch cut from `053b2b6d1af11ad0f926949ef39c7fdbf0e400bf`, then integrated live `origin/main` `8ae7436de854c4aa5c3ae55412390d91b4d6339e` by ordinary merge before validation; exact-head Hosted `Plan · validate` run is identified in the akte and PR #68 checks.
