# PR #1842 Demo Pin selection Befund (w177)

- Card: t-20261125-0428-284-1812-postretry-gate-failure, lane w177-0428-284-demo-pin-1812
- PR: https://github.com/mcpdev80/baseharbor/pull/1842, head 8b172f7c5312267cfa79417f620613410468a2e2
- Run 45611830424 (run 7729) on 8b172f7c5: top-level SUCCESS, but `PR · Demo Pin` = skipped.

## Proof: selection fix WORKS (demo-ref validator now fires when selected)
- Exact head 8b172f7c5 diff vs develop 2a141387 = 3 files:
  docs/releases/v0.4.28.demo-ref (pin bump), scripts/pr-gate-plan.py, scripts/test_pr_gate_coverage.py
- Running the trusted planner on the exact head:
  required_validation_checks = [ci-executor-tests, ci-policy, demo-source-pin-validation, pr-planner-tests, receipt-execution-tests]
  -> `demo-source-pin-validation` IS selected. broad_required=True (data-only Go fallback).
- Red-first regression test (test_pr_gate_coverage.ReleaseDemoPinSelectionTests) FAILS on the old
  v0.4.27-only match, PASSES after the regex fix (v0.4.2[78]). 47/47 coverage tests green.

## Why `PR · Demo Pin` gate is still SKIPPED (ci.yml:1080 boolean chain)
The gate's `if` (ci.yml:1080) is:
  runtime_required=='true' || integration_required=='true' || public_contracts_required=='true'
For THIS diff all three are false:
  - public_contracts_required = "false" (ci.yml:904, hardcoded for PR path)
  - runtime_required  = true iff pr-runtime-matrix.json["required"] (ci.yml:902)
  - pr-selected-runtime-matrix.py:35 -> "required": bool(supported)
    where supported = atomic/docker + atomic/podman gates in selected_gates.
  - 8b172f7c5 selected_gates = [] (data-only) -> required=false -> runtime_required=false
  - integration_required likewise false (bool(integration_included), same empty matrix)
So the gate correctly does NOT fire: a data-only demo-ref pin + scripts change sets NO
runtime/integration/contract requirement. This is BY DESIGN, not a selection defect.

## Owner-Befund (workflow-scope; NOT edited by lane)
Firing the Demo Pin gate for a pure data-only pin would require a .github/workflows/ci.yml change
(ci.yml:1080, ci.yml:902, pr-selected-runtime-matrix.py:35) to add a pin-only trigger, e.g. an
`|| needs.pr_plan.outputs.demo_pin_required=='true'` clause. This is OUTSIDE the worker write-set.
Delivered here as Befund. The selection fix itself (scripts/pr-gate-plan.py) is in and proven;
the remaining gate-firing is an owner workflow decision.
