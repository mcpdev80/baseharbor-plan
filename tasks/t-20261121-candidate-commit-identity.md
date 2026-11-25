---
id: t-20261121-candidate-commit-identity
card_number: "0428-224"
card_short_title: "candidate commits carry"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: w119b-0428-224-step4
kanban_status: active
kanban_lane: active
kanban_summary: "Sweeps show that most open candidates carry commits whose user.name belongs to a different lane, because lanes share…"
kanban_title: 0428-224 · candidate commits carry
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence:
  - "https://github.com/mcpdev80/baseharbor-plan/commit/3b85964a0"
---

- [ ] t-20261121-candidate-commit-identity · Coordination: candidate commits carry another lane's git identity (14 of 22 open PRs) #task #release/v0-4-28 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** w119b-0428-224-step4  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/commit/3b85964a0)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w119b-0428-224-step4  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Sweeps show that most open candidates carry commits whose `user.name` belongs to a different lane, because lanes share checkout/store state and the last writer wins. After this card, a candidate's commit authorship is provably the lane that owns the card, and the coordinator can verify it mechanically before requesting a verdict.

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

- **Lösung (Codex-Lane w119):** ESCALATION - durchsetzbarer Punkt ist nur scripts/dispatch-lane.sh (geteilte Checkout-Identität, last-writer-wins); Doku allein verhindert den Fehler nicht. Entscheidung beim Owner: scripts/**-Änderung freigeben oder Karte neu klassifizieren.


- 2026-11-24 · w119 · QUESTION / blocked. Claim published in planning commit `3b85964a0` (https://github.com/mcpdev80/baseharbor-plan/commit/3b85964a0). No product candidate or Hosted CI run was created. A shared checkout's repository-local `user.name` cannot be lane-deterministic when concurrent lanes overwrite it. The dispatch prompt has the canonical lane at `coordinator/scripts/dispatch-lane.sh:19` and is assembled at `:41`; minimal proposed change: append a requirement to create each candidate commit with `git -c user.name="$lane" -c user.email="$lane@baseharbor.local" commit ...`, and verify `git show -s --format=%an HEAD` equals `$lane` before push. This is a scripts-only coordinator fix, and the mission explicitly requires STOP + QUESTION. Owner: authorize this exact `scripts/dispatch-lane.sh` prompt change or direct another solution. No CI run IDs exist because no candidate was made; the planning claim commit is the only published witness.

- 2026-11-26 · w155 · DONE (owner direction 2026-11-26, implement + audit). AUDIT: live board has 26 open-status cards (active/claimed/review/waiting/blocked; `scripts/plan.py check` = 0 errors), not the 22 in the older wording. GitHub current open PRs = 8 (`gh pr list --repo mcpdev80/baseharbor --state open`). 11 of 26 open cards carry a PR link in frontmatter; 6 of those map to an OPEN PR (#1650, #1818, #1833, #1835, #1819, #1820; plus #1832 still open but blocked), the rest merged/closed. Identity signal = `.commit.author.name` of each PR head (top-level `.author`/GitHub login ignored; null on unsigned commits is not a finding). MISMATCH (author lane != owning lane) on #1650, #1818, #1819, #1812, #1837, #1817, #1820, #1826, #1834, #1833, #1832, #1753, #1761, #1780, #1783, #1773, #1809, #1714. OK on #1835 (author w105 == owning lane w105) and on the documented PR #1596 exception (author Marcel Pfingstgräf, 3-owner Owner-side hop, no content finding). Full per-PR table in evidence/r28-welle6-2026-11-26/candidate-commit-identity/audit.md. SYMPTOM CONFIRMED: candidate commit authorship is not lane-deterministic across lanes sharing the checkout (last-writer-wins) — the exact 0428-224 symptom. NO product code change, NO head rewrite, NO merge.

- 2026-11-26 · w155 · ADMISSION RULE implemented (scripts-only, Owner scope scripts/**). Added a CANDIDATE COMMIT IDENTITY ADMISSION RULE block to `coordinator/scripts/dispatch-lane.sh:45` (after the CI POLICY block at line 44): every candidate commit must be created with `git -c user.name=<lane> -c user.email=<lane>@baseharbor.local commit ...` and BEFORE any push the lane must mechanically verify `git show -s --format=%an HEAD` equals the lane name; on mismatch: STOP + report (no silent amend). No behavior change elsewhere; same verification one-liner requirement text. Diff SHA to be recorded in evidence. Codex reviews the scripts change (max 2 lanes), per mission.

## Recorded exception (coordinator, 2026-11-21)

One documented exception exists so far: PR #1596 candidate
`c27158567c0ebc370fc6c97390a561846305738f` (three authors from Owner-side hops, no content finding, exact run `44945468909`
success). Witness and scope: `evidence/r28-welle4-2026-11-21/org-env-reconciliation/owner-exception-identity-1596.md`.
The rule itself is unchanged: any other candidate with more than one author, or any candidate with a content finding,
still needs history normalization plus a fresh exact-head run.
