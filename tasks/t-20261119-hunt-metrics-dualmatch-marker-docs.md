---
id: t-20261119-hunt-metrics-dualmatch-marker-docs
card_number: "0428-126"
card_short_title: "ein CLI-Stadium druckt kein"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: 0428-126 (codeman 5f65f620)
kanban_status: closed
kanban_lane: closed
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-126 · ein CLI-Stadium druckt kein
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1696]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/dualmatch-docs/fix-1.md", "https://github.com/mcpdev80/baseharbor/pull/1696", "https://github.com/mcpdev80/baseharbor/actions/runs/44471319498", "https://github.com/mcpdev80/baseharbor/commit/da76c5cf9"]
---

- [x] t-20261119-hunt-metrics-dualmatch-marker-docs · Warning/Achtung dual-match: ein CLI-Stadium druckt kein Warning + EN-Normdoku hinter rename zurueck #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** 0428-126 (codeman 5f65f620)  
    **PR:** [baseharbor#1696](https://github.com/mcpdev80/baseharbor/pull/1696)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/dualmatch-docs/fix-1.md), [proof 2](https://github.com/mcpdev80/baseharbor/pull/1696), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/44471319498), [proof 4](https://github.com/mcpdev80/baseharbor/commit/da76c5cf9)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** 0428-126 (codeman 5f65f620)  
**Priority:** not set  
**PRs:** [baseharbor#1696](https://github.com/mcpdev80/baseharbor/pull/1696)  
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
## Befund (intake aus hunt-918)
Befund 5 (LOW) + 4-sub: Zwei doku-/marker-fragmente aus der i18n-rename-kette: dual-match verhaelt sich korrekt auf machine-EOs, aber ein CLI-Stadium druckt kein Warning (readProviderImpactAcknowledgement-EOF); EN normdoku blieb hinter dem rename zurueck. Akzeptanz: marker in jedem acknowledging Stadium + EN/DE doku gleichstandig. Befund 4 ist hier NICHT cardwuertig (already carded 105/112/073)
Erlaubtes write-set (vorschlag, lane prueft): docs + CLI marker stage. Evidence-Quelle: https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-19/hunt-metrics/befund-1.md (17 probes, base 97a840e54).

126 abgegeben: Warning-marker wird in jedem annerkennenden CLI-stadium gedruckt (nur repraesentation, gate-semantik unveraendert) + EN-normdoku auf den i18n-rename gezogen. kandidat 864fdcd3a auf lane-0428-126-dualmatch-docs, PR #1696, run 44471319498 (alle selected checks pass), akte dualmatch-docs/fix-1.md origin/main daceecb5. folgearbeit gemeldet: demo drive.py matcher-pattern (eigene karte im demo-repo)

CODEX-REVIEW: ACCEPT at exact head 864fdcd3a71c83d1fd2a5ae9a3304b23a5cefd6c. The marker is present at acknowledgement stages and consent semantics are unchanged; EN normdocs align to Warning. Exact-head run 44471319498 SUCCESS (34.13 summed hosted runner-minutes); PR Selected Checks app 15368. CODEX-MERGE: squash merge da76c5cf9c963207038d5599bd130b89ecb1e8a4 verified as develop head. Follow-up card 0428-129 covers the demo drive.py matcher; current origin/main card still shows unassigned, so confirm its claim/status.

126 gemergt: PR #1696 (head 864fdcd3a) ist als da76c5cf9 auf develop (Warning-marker in jedem annerkennenden stadium, gate-semantik unveraendert + EN-doku). follow-karte 0428-129 (demo drive.py matcher) laeuft bereits auf dieser grundlage
