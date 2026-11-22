---
id: t-20261122-ci-integration-operator-seams-without-gate-admission
card_number: "0428-228"
card_short_title: "Admit operator seams to a gate"
type: task
areas: [ci, cli]
release: v0.4.28
version: ""
parent: v0.4.28
owner: Owner (implementor)
kanban_status: review
kanban_lane: review
kanban_summary: A pull request that changes any cmd/baha/ciintegrationoperator.go seam selects an executed native gate in the required hosted…
kanban_title: 0428-228 · Admit operator seams to a gate
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1755]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261122-ci-integration-operator-seams-without-gate-admission · 0428-228 · Admit operator seams to a gate #task #release/v0-4-28 #status/review #view/review #area/ci #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** Owner (implementor) · **Priority:** high  
    **PR:** [baseharbor#1755](https://github.com/mcpdev80/baseharbor/pull/1755)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Required by:** [t-20261122-footprint-show-not-admitted-in-data-capabilities-gate](t-20261122-footprint-show-not-admitted-in-data-capabilities-gate.md)  
**Owner:** Owner (implementor)  
**Priority:** high  
**PRs:** [baseharbor#1755](https://github.com/mcpdev80/baseharbor/pull/1755)  
**Source:** 
<!-- /generated:links -->

## Goal

A pull request that changes any `cmd/baha/ci_integration_operator_*.go` seam selects an executed native
gate in the required hosted CI, instead of only the broad fallback checks. Today the selection is silent:
the exact PR run can be green while the operator boundary is never executed.

## Scope

- In scope: the path-to-gate mapping only.
  - `scripts/pr-gate-plan.py`: the three paths are ABSENT from every explicit file set (grep count 0, see akte).
    An unmatched `cmd/baha/*.go` falls through at `scripts/pr-gate-plan.py:1344` to area
    `cli-unresolved-runtime-impact`, which requires CODE_CHECKS and CLI_CHECKS and records an unresolved note.
  - `scripts/pre-release-runtime-impact.json`: the core map names `cmd/baha/app_machine_adapters*.go` at `:30`/`:31`
    but not the operator seams.
- In scope: the three files that carry the build tag `baseharbor_ci_operator_testonly`
  (`cmd/baha/ci_integration_operator_enabled.go`, `cmd/baha/ci_integration_operator_disabled.go`,
  `cmd/baha/ci_integration_operator_enabled_test.go`).
- Out of scope: any change to `cmd/baha/**` product code, any new workflow, any change to how gates are executed.
- Out of scope: re-litigating 0428-227; that card owns the footprint-show admission itself, this card owns the
  mapping that lets such a change be qualified at all.

## Acceptance

- `scripts/pr-gate-plan.py` maps each of the three operator seam paths to a required native gate
  (`atomic/docker/data-capabilities` and its Podman twin, or the equivalent already used for the boundary).
- `scripts/pre-release-runtime-impact.json` names the same paths in its core map.
- A PR whose only change is one of the three files shows the mapped gate as a REQUIRED check that is
  executed, not skipped, at the exact head.
- The existing fallback behaviour stays fail-closed: an unmapped `cmd/baha/*.go` path keeps its unresolved note.
- Regression evidence: the gate-plan test family that asserts path-to-gate coverage names the three paths.

## Execution notes

- Written from bug-hunt H-V32 (gate-admission-census, `w21-pr1702-0428-142-compat`), akte commit `0884c6e20`,
  which measured the three seams against both mapping files on develop `6209874428f`.
- HUNT-REF: H-V32, evidence `evidence/r28-welle5-2026-11-22/gate-admission-census/round-1.md`.
- `scripts/**` and `.github/**` are Owner-scope in this window: the mapping edit itself is applied by the Owner
  (directive 2026-11-22, CI-Aufnahmepflicht). A worker lane may verify the resulting selection in hosted CI,
  but must not edit these files.
- Related open candidates that depend on this: 0428-227 (PR #1753, footprint show in the data-capabilities gate)
  and every later operator-boundary change.

exact recipe written and published: pr-gate-plan.py entries plus pre-release-runtime-impact.json core entries for the ci_integration_operator sources, with a pairing assertion in test_pr_gate_plan.py and test_pre_release_runtime_reuse.py; 1753 acceptance waits on this merge

Erster kandidat a2f680c09 wurde am exakten head geprueft; die Nachbesserung 558265019 ergaenzt vier Zeilen in .github/workflows/ci.yml: eine direkte direkte Ausfhrung fuer die build-tagged suite, weil der vertrauenswuerdige base runner eine neue validation-id nicht kennt. Exact-head run 44985859511 ist unterwegs; review dispatcht.
