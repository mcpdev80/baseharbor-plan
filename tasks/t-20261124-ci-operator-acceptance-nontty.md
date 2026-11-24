---
id: t-20261124-ci-operator-acceptance-nontty
card_number: "0428-285"
card_short_title: "CI operator Accept"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: w116-0428-285-takeover
kanban_status: closed
kanban_lane: closed
kanban_summary: "Loesung: Core test-only up fixture regression accepted; entschieden von Codex-Lane w116 under the Owner mandate of 2026-11-24.…"
kanban_title: 0428-285 · CI operator Accept
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1827]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence:
  - https://github.com/mcpdev80/baseharbor/pull/1827
  - https://github.com/mcpdev80/baseharbor/actions/runs/45455276409
  - https://github.com/mcpdev80/baseharbor/actions/runs/45460654225
  - https://github.com/mcpdev80/baseharbor/commit/adf43709b8b37cd2b18a6bf4710019d7343d54b4
---

- [x] t-20261124-ci-operator-acceptance-nontty · CI operator acceptance non-interactive in CI #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** w116-0428-285-takeover  
    **PR:** [baseharbor#1827](https://github.com/mcpdev80/baseharbor/pull/1827)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1827), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/45455276409), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/45460654225), [proof 4](https://github.com/mcpdev80/baseharbor/commit/adf43709b8b37cd2b18a6bf4710019d7343d54b4)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w116-0428-285-takeover  
**Priority:** not set  
**PRs:** [baseharbor#1827](https://github.com/mcpdev80/baseharbor/pull/1827)  
**Source:** 
<!-- /generated:links -->

## Goal

Loesung: Core test-only `up` fixture regression accepted; entschieden von Codex-Lane w116 under the Owner mandate of 2026-11-24. Demo login and acceptance-group behavior remains with 0428-284; #1812 runtime requalification remains downstream.

## Scope

- In scope:
  - BaseHarbor's test-only CI fixture regression for root `up --yes` and `up --yes --confirm-candidate <digest>` on policy and connectivity gates, proving the existing managed-local apply admission contract.
- Out of scope:
  - Demo `scripts/acceptance.sh` login and acceptance-group behavior; tracked separately by 0428-284.
  - baseharbor `.github/**` workflow files (owner-scope; #1825 already added the build tag/binary).
  - The frozen chain PRs #1812/#1819/#1820/#1818 — do NOT touch them.
  - #1826 / 0428-279 / 0428-283 static/mcp operator gap (separate owner decision, runtime=static excluded from this fallback).

## Acceptance

- The changed `up` fixture cases for policy and connectivity run in `ci-integration-operator-seam-tests` on the exact PR head, with both Docker and rootless Podman selected native data-capabilities checks green on that same head.
- The two exact-head Hosted PR runs and merge commit are linked in this card's evidence; the separate Demo acceptance behavior remains tracked by 0428-284.
- #1812's 14 Light runtime gates remain a separate requalification after this merge; they are not claimed as completed by this card.

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

- **Leg-A/Befund (Codex-Lane w113b, #170-Demo-Route):** kein Input-Schema-Mismatch; Workflow-Blob zum letzten funktionierenden Lauf identisch (bbcff8dc6); startup_failure VOR Job-Scheduling (resolve ohne Condition, null Jobs/Logs) = Plattform-Klasse. Leg-B-Supersession streng gated auf Merge von Core #1830 (demo_ref weggelassen=Pin); #170 bleibt open.


- **Lösung (Codex-Lane w116, Übernahme von Worker w111):** Umfang = Core-test-only allow-list beider up-Formen + Seam-Regression; entschieden von w116 nach Mandat; Seam-Test am Diagnosedhead grün, finale Qualifikation nach Hop auf develop inkl. #1828.


- Current state, branch, PR and evidence links. Newest first.

### Takeover closeout (2026-11-24)

- Loesung: Core test-only `up` fixture regression accepted after merge and two exact-head green CI runs; entschieden von Codex-Lane w116 under the Owner mandate of 2026-11-24.
- **Decision:** Core fixture half is complete and handed to review. BaseHarbor PR [#1827](https://github.com/mcpdev80/baseharbor/pull/1827) merged at `adf43709b8b37cd2b18a6bf4710019d7343d54b4`; source head `83d7c7afc84740b565ff654562a178361c3522c8`, based on develop `08274e67dfd61d65834f5c4bdb4bf6640fa11576`.
- The final diff is only seven added cases/comments in `cmd/baha/ci_integration_operator_enabled_test.go`, covering `up --yes` and `up --yes --confirm-candidate <digest>` on policy and connectivity fixtures. Existing regression `TestCIIntegrationOperatorAdmitsFiveCoreFixtureFormsOnlyOnConsumerGate` ran in `ci-integration-operator-seam-tests`; PR CI selected Docker and rootless Podman `data-capabilities` gates as well.
- Exact-head Hosted PR CI runs [45455276409](https://github.com/mcpdev80/baseharbor/actions/runs/45455276409) and [45460654225](https://github.com/mcpdev80/baseharbor/actions/runs/45460654225) both completed successfully on `83d7c7afc84740b565ff654562a178361c3522c8`, with all 35 jobs terminal and zero failures. `PR Selected Checks` succeeded from GitHub Actions integration 15368 in both runs; Docker and Podman selected runtime jobs succeeded.
- Independent review: Codex CLI `gpt-6-luna`, session `01a20ec8-9b1e-7e73-a9c2-cf52c0535e23`, approved the complete diff at `83d7c7af` against base `08274e67`; review artifact was `/tmp/w116-0428-285-review-83d7c7af.md`. Horde task: none; the review was performed in a separate Codex CLI session.
- Scope trim: removed the original production allow-list policy-check admission and kept only the test-only regression cases. No product-auth semantics, workflow files, or Demo files changed. The diagnosed seam-test failure on the earlier `27f60e22` candidate was an incorrect connectivity-fixture expectation and was corrected in the final test-only diff.
- Void witnesses: `45445355381` (`19ce34ef`, superseded head) was cancelled and is void; `45450521570` (`8c580f96`, stale base `f14fb87c`) is void after the owner-directed hop; `45460647858` was the cancelled draft-transition workflow; `45461209724` was an unsuccessful Pre-Release dispatch whose source planner rejected the mismatched Demo input before any gate executed. None count toward acceptance. Earlier candidate runs `45447834402` and `45455276409` were not substitutes for the final two-run pair; final qualifying IDs are only `45455276409` and `45460654225`.
- Post-merge boundary: Demo login and acceptance-group work remains independently owned by card 0428-284. #1812 must refresh/requalify after this merge; owner assigned that develop-merge requalification to w112. The shared test file also appears in #1826, which must refresh against the new develop tip.
