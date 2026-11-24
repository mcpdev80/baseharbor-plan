---
id: t-20261125-0428-283-static-mcp-gate-operator-gap
card_number: "0428-283"
card_short_title: "static-mcp operator gap"
type: bug
areas: [ci]
release: v0.4.28
version: ""
parent: ""
owner: Lane-Codex (w112)
kanban_status: active
kanban_lane: active
kanban_summary: ""
kanban_title: 0428-283 · static-mcp operator gap
priority: high
depends_on: []
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence:
  - https://github.com/mcpdev80/baseharbor/actions/runs/45413604588
  - https://github.com/mcpdev80/baseharbor/blob/develop/cmd/baha/ci_integration_operator_enabled.go
---

- [ ] t-20261125-0428-283-static-mcp-gate-operator-gap · static-mcp operator gap #task #release/v0-4-28 #status/active #view/active #area/ci #kind/bug
    <!-- generated:card -->
    **Owner:** Lane-Codex (w112) · **Priority:** high  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/45413604588), [proof 2](https://github.com/mcpdev80/baseharbor/blob/develop/cmd/baha/ci_integration_operator_enabled.go)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** Lane-Codex (w112)  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Problem

- Where: v0.4.28 static/mcp gate. Confirmed READ-ONLY by w80 with run 45413604588 log lines 580-594 + these files:
  - baseharbor-demo tests/mcp/new-edit-static.py:75-86 sets BASEHARBOR_TEST_RUNTIME=static, GATE=mcp, BASEHARBOR_TARGET=mcp-static, no operator env, then runs 'baha target create mcp-static --provider docker --access local-docker --reference local --scope default --default' with check=True -> 'requires an authenticated BaseHarbor operator'.
  - baseharbor .github/workflows/pre-release-runtime-suite.yml: the static/mcp path builds a PLAIN binary (go build -trimpath -o .../baha ./cmd/baha, ~:276) WITHOUT -tags; the runtime path sets GOFLAGS=-tags=baseharbor_ci_operator_testonly (~:304). The synthetic operator cmd/baha/ci_integration_operator_enabled.go is //go:build baseharbor_ci_operator_testonly, so it is absent from the plain static/mcp binary.
  - cmd/baha/ci_integration_operator_enabled.go:100-103: even if tagged, the managed-local-gate operator requires BASEHARBOR_DEMO_OPERATOR_GATE set AND runtime in {docker,podman} AND target == 'atomic-<runtime>-<gate>'; the static/mcp gate (runtime=static, gate=mcp, target=mcp-static) satisfies none -> operator path not engaged.
- Preexisting: tests/mcp/new-edit-static.py exists on demo since c23bd9a (PR #169); the gap reproduces at demo df4867c independent of #1826. NOT a #1826 regression, NOT a product defect per se — a gate-provisioning design gap.
- Expected vs Actual: expected the static/mcp gate's baha to carry the synthetic CI integration operator (as the runtime gates do) or the harness to satisfy its env contract; actual: plain binary + no operator env -> managed op fails auth.

## Regression

- After the owner-authorised provisioning change, the v0.4.28 static/mcp gate reaches the annotation/parity assertions AND the new-edit-static bootstrap on the exact candidate head without the auth error; a check/test asserts the static/mcp binary is built WITH the operator tag (or the harness sets the operator contract), so the gap cannot silently regress.

## Acceptance

- OWNER-SOPE decision first (see blocker). Worker implements only after the owner names the mechanism (A tag the static/mcp build, and/or B operator env/target contract, touching .github and possibly demo + the product env gate). No merge of #1826's static/mcp qualification until this antecedent is resolved; #1826's own code (contract set + #171 destructiveHint annotation) is correct.
