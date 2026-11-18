---
id: t-20261115-bughunt-d28-i18n-achtung
card_number: "0428-093"
card_short_title: "bf04 english-only hints"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: coord
kanban_status: review
kanban_lane: active
kanban_summary: "BF-04 (ux/i18n): German \"Achtung\" hint appears in English output and inside the JSON contract (15 sites). Found on develop…"
kanban_title: "0428-093 · bf04 english-only hints"
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1663, "https://github.com/mcpdev80/baseharbor/pull/1663"]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-14/vm-bughunt/h-d28.md"]
---

- [ ] t-20261115-bughunt-d28-i18n-achtung · BF-04 German 'Achtung' hint in English output and JSON contract (15 sites) #task #release/v0-4-28 #status/active #view/active #kind/task
    <!-- generated:card -->
    **Owner:** coord  
    **PR:** [baseharbor#1663](https://github.com/mcpdev80/baseharbor/pull/1663)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle1-2026-11-14/vm-bughunt/h-d28.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Required by:** [t-20261116-i18n-demo-consumer-rename](t-20261116-i18n-demo-consumer-rename.md)  
**Owner:** coord  
**Priority:** not set  
**PRs:** [baseharbor#1663](https://github.com/mcpdev80/baseharbor/pull/1663)  
**Source:** 
<!-- /generated:links -->

## Goal

BF-04 (ux/i18n): German "Achtung" hint appears in English output and inside the JSON contract (15 sites). Found on develop 0e9ccb582 during H-D28.

## Scope

- In scope:
- Out of scope:

## Acceptance

- Each criterion as a plain bullet. Do not use checkboxes here: only the card line above is a checkbox.

## Required checks

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

## Acceptance criteria (coord, 2026-11-18 nach Independent-check)
- exact-head required run on final head SUCCESS (no old-head citation)
- patch scope: the intended 15-site Achtung-to-Warning correction (code/i18n catalog surface), NO consent-logic change; distinct from docs card 0428-107 (docs keep the unified **Achtung** label, already-compliant) and from 0428-106 (consent-path fallback strings)
- evidence akte records run-ID, patch digest, and repo-rule compliance
## Handoff
- owner: coord until review; CODEX-REVIEW (Luna session) gives the verdict; GitHub self-approval not possible (same author account) — verdict lives in the akte.

kandidat 4ef41a31f (15-stelle Achtung->Warning, base-frisch auf 907f16713), exact-head run 44396406150 SUCCESS; acceptance-/handoff-felder der karte gefuellt; verdict liegt in der akte (self-approval-restriktion)

## Required checks binding + CI coverage debt (coord, 2026-11-18)
- test -> gate -> trigger -> run: public-contracts integration suite -> 'PR · Public Contracts' job -> pr_plan gate -> run 44396406150.
- DEBT (blocking for merge), reconciled 21:22 with independent check: pr-gate-plan.py at the exact head DOES select integration/static/public-contracts for the changed JSON schemas, but the ci.yml job flag public_contracts_required is fed from a step that hardcodes false (ci.yml:840) instead of from the gate-plan selection — plan and job condition are NOT wired together. Owner-scoped .github fix; lanes must not touch. (Supersedes the earlier 'structurally dead' wording.)
- Equivalent evidence path (accepted interim): a follow-up lane executes the public-contracts integration LOCALLY on exact head 4ef41a31f250b7824b57b874895790cc4435712a and appends the transcript to this card's evidence (akte follow-up-1.md); CODEX must not merge before that akte exists or the workflow fix is on develop.

CODEX-REVIEW REQUEST CHANGES 21:20Z: scope-verletzung — 51 files, docs/**-anteile gehoeren nicht zu 093 (liegen bei 107/109); korrektur-lane stellt nur die docs-dateien auf develop-stand zurueck, code/i18n-catalog-15-stelle bleibt, consent-logik unangetastet
## Witness target update (coord, 2026-11-18 21:4xZ)
- Scope-reset head: `cb3777dceb70e3b2d2957044468e2ddee5f2ebe1` (38 paths, zero docs/**). run 44404028009 pending.
- follow-up-1.md (old 4ef41a31 witness abort note) is VOID for acceptance.
- Public Contracts witness must be produced AGAINST THE FINAL SHA after terminal CI, then CODEX re-review. Merge stays blocked until all three exist for the same SHA.

scope-fix END: head d0351baf5 clean/MERGEABLE; run 44407750981 attempt2 completed SUCCESS (attempt1 war interim-Fehlerstand, upated_at 23:43Z — vom reviewer bestaetigt); pristine Public-Contracts witness-3 gleicher SHA; akten am band; Re-review geroutet
