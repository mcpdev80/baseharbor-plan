---
id: t-20261125-0428-283-static-mcp-gate-operator-gap
card_number: "0428-283"
card_short_title: "static-mcp operator gap"
type: bug
areas: [ci]
release: v0.4.28
version: ""
parent: ""
owner: w112-0428-283-staticmcp
kanban_status: closed
kanban_lane: closed
kanban_summary: ""
kanban_title: 0428-283 · static-mcp operator gap
priority: high
depends_on: []
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo]
prs: [mcpdev80/baseharbor#1826]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence:
  - https://github.com/mcpdev80/baseharbor/actions/runs/45474619605
  - https://github.com/mcpdev80/baseharbor/actions/runs/45480707229
  - https://github.com/mcpdev80/baseharbor/actions/runs/45480707229/job/138756755764
  - https://github.com/mcpdev80/baseharbor/actions/runs/45482875408
  - https://github.com/mcpdev80/baseharbor/actions/runs/45482875373
  - https://github.com/mcpdev80/baseharbor/commit/145b4a20f35179a0ac6bc0a66666a846c1ae35c0
  - https://github.com/mcpdev80/baseharbor/pull/1826#issuecomment-7143836376
---

- [x] t-20261125-0428-283-static-mcp-gate-operator-gap · static-mcp operator gap #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/ci #kind/bug
    <!-- generated:card -->
    **Owner:** w112-0428-283-staticmcp · **Priority:** high  
    **PR:** [baseharbor#1826](https://github.com/mcpdev80/baseharbor/pull/1826)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/45474619605), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/45480707229), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/45480707229/job/138756755764), [proof 4](https://github.com/mcpdev80/baseharbor/actions/runs/45482875408), [proof 5](https://github.com/mcpdev80/baseharbor/actions/runs/45482875373), [proof 6](https://github.com/mcpdev80/baseharbor/commit/145b4a20f35179a0ac6bc0a66666a846c1ae35c0), [proof 7](https://github.com/mcpdev80/baseharbor/pull/1826#issuecomment-7143836376)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w112-0428-283-staticmcp  
**Priority:** high  
**PRs:** [baseharbor#1826](https://github.com/mcpdev80/baseharbor/pull/1826)  
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

- RESOLVED by owner grants 2026-11-24 (19:0xZ scope note + 23:5xZ restatement): the previously open scope decision is made — mechanism (A): operator build-tag on the static/mcp path in .github/workflows/pre-release-runtime-suite.yml ONLY (the single authorized file; ci.yml and the normal CI path untouched; no third provisioning kind), plus minimal demo configuration; the affected sources are catalogued in the same step. Lane-Codex (w112) implements/verifies/merges within this grant; merge requires two exact-host green run IDs per the standing evidence rule. #1826's own code (contract set + #171 destructiveHint annotation) was already assessed correct.


## Handoff

- **Decision (Owner mandate 2026-11-24): ACCEPTED and MERGED.** PR [#1826](https://github.com/mcpdev80/baseharbor/pull/1826) merged to `develop` as `145b4a20f35179a0ac6bc0a66666a846c1ae35c0`.
- **Pre-merge exact-head pair:** PR CI [45474619605](https://github.com/mcpdev80/baseharbor/actions/runs/45474619605) and Hosted qualification [45480707229](https://github.com/mcpdev80/baseharbor/actions/runs/45480707229) both succeeded on Core head `0b391f01a77d55ff5fd1e767c729d51f5ce3748c`. The Hosted planner log records `static_execute_count: 1`, `reuse_from: ""`; executed job [138756755764](https://github.com/mcpdev80/baseharbor/actions/runs/45480707229/job/138756755764) checked out that exact SHA and passed `Static · mcp`.
- **Post-merge witnesses:** Docker [45482875408](https://github.com/mcpdev80/baseharbor/actions/runs/45482875408) and Podman [45482875373](https://github.com/mcpdev80/baseharbor/actions/runs/45482875373) both succeeded on merge SHA `145b4a20f35179a0ac6bc0a66666a846c1ae35c0`, which matches remote `develop`.
- **Scope decision:** use the existing test-only operator build/tag and minimal Demo MCP environment; no third provisioning kind, no production authorization/consent changes, `.github/workflows/ci.yml` untouched. The only changed `.github` file is `.github/workflows/pre-release-runtime-suite.yml`; all four changed Core files and related Demo harness/contract/catalog sources were catalogued in the PR evidence. Independent scope review passed: [PR review note](https://github.com/mcpdev80/baseharbor/pull/1826#issuecomment-7143836376).
