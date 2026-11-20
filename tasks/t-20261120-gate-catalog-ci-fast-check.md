---
id: t-20261120-gate-catalog-ci-fast-check
card_number: "0428-205"
card_short_title: "Gate catalog for ci-fast-check"
type: bug
areas: [ci]
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-205 · Gate catalog for ci-fast-check
priority: normal
depends_on: [t-20261120-r28-cli-shard-operator-env]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261120-gate-catalog-ci-fast-check · 0428-205 · Wire scripts/ci-fast-check.sh into the gate catalog #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/ci #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Waiting for prerequisites**  
    **Needs:** [t-20261120-r28-cli-shard-operator-env](t-20261120-r28-cli-shard-operator-env.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261120-r28-cli-shard-operator-env](t-20261120-r28-cli-shard-operator-env.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
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

## Why

Round-2 of `evidence/r28-welle4-2026-11-20/aggregate-vs-base/round-1.md` (sitz w215) measured: `Workflow policy` is SUCCESS at
PR #1731 head `f90b3f44` (job 136551503837, "Workflow policy PASS: 20 approved workflow files." + "Gate catalog consistency
PASS"), while PR #1665 shows the same cell as FAILURE. The enforcing rule is `scripts/ci-workflow-policy.sh:34-40` (workflow
file inventory + gate catalog), invoked from `.github/workflows/ci.yml:31-32`. The coordinator verified on develop
`40cb28c758b0`: `scripts/ci-fast-check.sh` exists there, and the string `ci-fast-check` appears only in
`scripts/pr-candidate-advisory.py`, NOT in `release-requirements.json`. So the new check surface is not wired into the
catalog that the policy gate compares against.

## What

Add the missing catalog pairing for `scripts/ci-fast-check.sh` in `release-requirements.json` (or wire it into the existing
PR selection surface the policy script reads), so a PR whose base comparison sees the new file does not fail
`Workflow policy`. No workflow file may be added or removed; the policy script itself stays untouched.

## Acceptance

- `scripts/ci-workflow-policy.sh` run locally at the exact head prints "Workflow policy PASS" and "Gate catalog consistency
  PASS" with the same two strings the hosted job uses.
- The failing cell on a stacked/older-base PR (evidence: PR #1665) is explained by this pairing alone, verified by re-running
  the policy script on that head in a scratch worktree - not by any `.github/**` change.
- One PR, base develop, non-draft from the start; hosted `Workflow policy` + `PR Selected Checks` observed at the exact head.
