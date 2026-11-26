---
id: t-20261124-r28-runtime-authority-gate-routing
card_number: "0428-272"
card_short_title: "authority seam no runtime gate"
type: task
areas: [ci, testing, security]
release: v0.4.28
version: ""
parent: v0.4.28
owner: w327-0428-272-gaterouting
kanban_status: active
kanban_lane: active
kanban_summary: A PR that changes the local-runtime / trusted-authority seam is qualified by at least one native runtime gate (Docker and…
kanban_title: 0428-272 · authority seam no runtime gate
priority: normal
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: "Awaiting routing answer (w267 dispositions a/b): release-requirements.json gates[] base rows (0428-275 re-point vs 0428-359 fold-in) and #1860 held-catalog overlap. Next trigger: coordinator routing post, then rebase + dispatch."
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261124-r28-runtime-authority-gate-routing · PR-Gate-Plan routes the runtime-authority seam to package checks only, so a fail-open regression there is never qualified by a native runtime gate. #task #release/v0-4-28 #status/active #view/active #area/ci #area/security #area/testing #kind/task
    <!-- generated:card -->
    **Owner:** w327-0428-272-gaterouting · **Priority:** normal  
    **Blocker:** Awaiting routing answer (w267 dispositions a/b): release-requirements.json gates\[\] base rows (0428-275 re-point vs 0428-359 fold-in) and \#1860 held-catalog overlap. Next trigger: coordinator routing post, then rebase + dispatch.  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w327-0428-272-gaterouting  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

A PR that changes the local-runtime / trusted-authority seam is qualified by at least one native runtime gate (Docker and rootless Podman) in addition to its package checks. Witnessed on develop 3ebfb90d (bughunt-hv26 F5):

- `scripts/pr-gate-plan.py:1643-1647`: any path in `OPERATORAUTH_POLICY_FILES` (declared at `scripts/pr-gate-plan.py:85-92`, which includes `internal/operatorauth/config.go`, `internal/operatorauth/local_runtime.go` and their tests) resolves to `area = 'operatorauth-explicit-policy'` and calls `require(AUTHORITY_PACKAGE_CHECKS + CODE_CHECKS)` only.
- Consequence: no `atomic/{docker,podman}/<gate>` is added, so `scripts/pr-selected-runtime-matrix.py` reports `runtime_required=false` and the `pr_candidate` job that builds `baha-ci-operator-testonly` (`ci.yml:1141-1153`) is never dispatched for such a PR.
- The engine-owner plus grant boundary the seam depends on lives in `cmd/baha/local_workload_authority.go:49-157`; a fail-open regression there passes CI on unit coverage alone with no native acceptance.

## Scope

- In scope: the routing decision in `scripts/pr-gate-plan.py` (extend the operatorauth branch so it also requires a bounded native runtime gate, or move `internal/operatorauth/local_runtime.go` into the rule that already escalates), plus the registration that keeps the gate map self-consistent.
- Out of scope: changing product code, inventing a new gate, adding a CI framework, or editing `.github/workflows/**` beyond what the existing PR-gate jobs already consume.

## Acceptance

1. A PR touching `internal/operatorauth/local_runtime.go` (or `authorization.go`) selects at least one native runtime gate for Docker and one for rootless Podman, visible in the plan artifact of the exact-head run.
2. A PR touching an unrelated path (for example `internal/metrics/**`) still does NOT select that runtime gate, so the escalation stays precise instead of broadening every PR.
3. The existing planner tests cover both directions in the same PR, registered in the CI group that executes the `scripts/pr-gate-plan.py` tests; the evidence names the job, trigger and run URL for both selections (AGENTS 5.3).

## Dependencies and file ownership

- Owned files or areas: `scripts/pr-gate-plan.py`, its planner tests, and the gate registration data it reads if the route needs it.
- Shared files: `.github/workflows/ci.yml` only if a dispatch wiring change is unavoidable — that file is Owner scope and must be reported as a finding with file:line, not edited by a lane.

## Handoff

- OWNER SCOPE: `scripts/pr-gate-plan.py` is the trusted gate planner (Owner-adjacent per the H-V26 dossier note, and a `scripts/**` routing change binds later PRs under CI policy). The Owner implements; this card documents the need with file:line.
- Pairs with [0428-270](t-20261124-r28-trusted-local-failopen-seam-dead.md), which fixes the seam itself: neither card substitutes for the other, and 0428-270's regression is only as strong as the gate that actually executes it.
- Source: bughunt-hv26 F5 dossier `evidence/r28-welle6-2026-11-24/bughunt-hv26-candidate-consent-gate/round-1.md` (develop 3ebfb90d).

## Handoff

- BLOCKED (exact, w327-0428-272-gaterouting, 2026-11-27): STOP acknowledged and disposition routed by the coordinator (08:4xZ). Two write-set clashes on `scripts/pr-gate-coverage.json` / planner files, no safe lane route:
  1. The 0428-272 route needs the `release-requirements.json` `gates[]` base rows (missing since the #1859 drift) so declared catalog gates resolve against the trusted release catalog; baseline-family rows belong to Codex disposition — w267 answers (a) whether 0428-275 (w65 ghost-held) is re-pointed to this card or the rows fold into the accepted 0428-359 baseline family, and (b) how #1860's held catalog edits avoid clashing with this card's candidate delta.
  2. Open PR #1860 (lane `w333-0428-312-volrecovery`) edits `scripts/pr-gate-coverage.json` in its delta — same-file overlap with this card's write-set (merge-frost rule).
- Reproduced on develop 5a37ddbd with the production planner: `internal/operatorauth/local_runtime.go` + `local_runtime_test.go` ALREADY select `atomic/docker/data-capabilities` + `atomic/podman/data-capabilities` via catalog rows (runtime_specific=True), so the seam half of acceptance item 1 holds on current develop; `authorization.go`/`context.go` remain unresolved ('unknown impact') and `config.go` selects only the Docker representative. The bughunt-hv26 F5 witness predates those rows (#1859 era).
- Candidate planner/test delta prepared in lane worktree /var/tmp/w327-0428-272-gaterouting (uncommitted, NOTHING pushed, product code untouched): comment-corrected operatorauth branch (catalog is the gate authority) + catalog-authority regression `test_operatorauth_runtime_seam_selects_both_data_gates`. Rebase and dispatch after the routing answer and the #1860/0428-275/0428-359 dispositions land.
