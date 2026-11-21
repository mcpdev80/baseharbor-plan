---
id: t-20261121-static-gate-registration
card_number: "0428-208"
card_short_title: "0428-208 static gate"
type: task
areas: [ci]
release: v0.4.28
version: ""
parent: ""
owner: "Codex (Owner-directed, 2026-11-21)"
kanban_status: active
kanban_lane: active
kanban_summary: "atomic/static/ci-fast-check exists in the gate catalog AND in every consumer that validates catalog consistency, so the Workflow…"
kanban_title: 0428-208 · 0428-208 static gate
priority: high
depends_on: [t-20261120-gate-catalog-ci-fast-check]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261121-static-gate-registration · 0428-208 register the static ci-fast-check gate across planner, runner and pre-release plan #task #release/v0-4-28 #status/active #view/active #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** Codex (Owner-directed, 2026-11-21) · **Priority:** high  
    **Needs:** [t-20261120-gate-catalog-ci-fast-check](t-20261120-gate-catalog-ci-fast-check.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261120-gate-catalog-ci-fast-check](t-20261120-gate-catalog-ci-fast-check.md)  
**Owner:** Codex (Owner-directed, 2026-11-21)  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

`atomic/static/ci-fast-check` exists in the gate catalog AND in every consumer that validates catalog consistency, so the
`Workflow policy` cell on `mcpdev80/baseharbor#1665` passes without the pairing trick that 0428-205 proved impossible.

## Why

w220 measured three candidate shapes (akte
`evidence/r28-welle4-2026-11-20/gate-catalog-ci-fast-check/round-1.md`, FINDING 3, replay runs R1a-R1f): rule
`scripts/ci-workflow-policy.sh:184-187` only accepts the pairing **inside the compared diff**, so no develop-side
pairing can green the #1665 cell, and rule `scripts/ci-workflow-policy.sh:197-201` is inventory-based — any new
`.gates[].id` trips it unless the planner and the runners know the gate. A content-neutral `scripts/pr-gate-plan.py`
edit does not exist (the file carries no `atomic`/`static` literals at all). 0428-205 was therefore cut too narrow;
its lane is blocked on an Owner decision instead of expanding silently.

## Scope

Allowed write-set:

- `scripts/pr-gate-plan.py` (register the gate id, its job and its dependencies)
- `scripts/pre-release-check-plan.py` (STATIC section)
- `scripts/pr-check-runner.py` (dispatch case for the gate)
- `scripts/release-requirements.json` (`.gates[]` entry, form V2: `id`, `schema`, `required_for: []`,
  `jobs: ["static_gates"]`, `dependencies: ["core", "demo"]`)
- the tests that already cover those four files

Forbidden:

- `scripts/ci-workflow-policy.sh` (the rules are deliberately hard)
- `.github/workflows/ci.yml` — the case arm at `.github/workflows/ci.yml:1301` is **Owner scope** and is a
  prerequisite of this card, see Dependencies.

## Acceptance criteria

1. `bash scripts/ci-workflow-policy.sh` prints both `Workflow policy PASS: N approved workflow files.` and
   `Gate catalog consistency PASS` at the exact candidate head, with `BASE`/`HEAD` comparisons for develop and for
   the #1665 head `db27880c108a`.
2. `python3 scripts/test_ci_v0427_contract.py` (and the other gate-catalog suites w220 names in the akte) pass.
3. The gate is selectable in CI: the card states test -> check/gate -> trigger -> result for the new catalog entry.

## Test binding

| Attribute | Value |
| --- | --- |
| Required check(s) | `Workflow policy` cell of PR Selected Checks |
| Test identifier | `atomic/static/ci-fast-check` |
| Route | `new gate in catalog + planner + runner (this card)` |

## Dependencies

The Owner must set the case arm at `.github/workflows/ci.yml:1301` (or decide that `static_gates` needs no arm and
relax the inventory rule instead). Until that decision is recorded here, this card cannot produce a green candidate
and must not be commissioned — a red PR for a known owner-scope gap wastes the matrix (§5.4).

## Stop and report

- If the registration requires any `.github/**` line beyond the arm named above, stop and report file:line.
- If the Owner chooses route B (relax the inventory rule), this card is superseded by that decision.

## Handoff

- Candidate branch, PR, exact head SHA, terminal hosted run id, and the two `ci-workflow-policy.sh` comparison outputs.
- Evidence: `evidence/r28-welle4-2026-11-20/static-gate-registration/round-1.md`.
