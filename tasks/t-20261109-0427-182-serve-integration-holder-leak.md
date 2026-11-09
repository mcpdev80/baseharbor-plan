---
id: t-20261109-0427-182-serve-integration-holder-leak
card_number: "0427-182"
card_short_title: "Serve holder teardown"
type: bug
areas: []
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-0427-182-impl
kanban_status: closed
kanban_lane: closed
kanban_summary: Release and await every serve integration holder so a later cmd/baha test cannot inherit a bound listener from another test.
kanban_title: 0427-182 · Serve holder teardown
priority: ""
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1520]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1520", "https://github.com/mcpdev80/baseharbor/actions/runs/42704543118", "https://github.com/mcpdev80/baseharbor/commit/edee0ae532605fb12da3f86f2f588889f579fa7b"]
---

- [x] t-20261109-0427-182-serve-integration-holder-leak · 0427-182 · Serve integration test leaks a bound+serving holder that poisons later cmd/baha tests #task #release/v0-4-27 #status/closed #view/closed #board/planned #kind/bug
    <!-- generated:card -->
    **Owner:** lane-0427-182-impl  
    **PR:** [baseharbor#1520](https://github.com/mcpdev80/baseharbor/pull/1520)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1520), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/42704543118), [proof 3](https://github.com/mcpdev80/baseharbor/commit/edee0ae532605fb12da3f86f2f588889f579fa7b)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** lane-0427-182-impl  
**Priority:** not set  
**PRs:** [baseharbor#1520](https://github.com/mcpdev80/baseharbor/pull/1520)  
**Source:** 
<!-- /generated:links -->

## Goal

Release and await every serve integration holder so a later `cmd/baha` test cannot inherit a bound listener from another test.

## Scope

- In scope:
- Out of scope:

## Acceptance

- Each criterion as a plain bullet. Do not use checkboxes here: only the card line above is a checkbox.

## Required checks

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

## Task Note
Follow-on of 0427-181 (which isolated only the `up` side). Witness (hosted, exact): run 42678151766 on 03a4544de (PR #1512 head, base develop 8a2912c62) fails `--- FAIL: TestUpNameResumesThroughCommandEntrypoint (80.57s)` at runtime_ports_test.go:340 with `holder: root=/tmp/TestServeCommandIntegrationOwnershipOnValidRoot.../runtime` and `holder bound+serving at 127.0.0.1:43423` — a SERVE integration test's holder stays bound/serving into a later test, i.e. the same contamination family, different emitter. Required: teardown guarantee (stop + wait release) for every serve holder created in cmd/baha tests, plus a guard assertion that no listener from another test's temp root is bound when the entrypoint test starts. Must run (no SKIP) in the always-executed CI group.

## Acceptance verified — 2026-11-09

- PR [#1520](https://github.com/mcpdev80/baseharbor/pull/1520) merged into `develop` at `edee0ae532605fb12da3f86f2f588889f579fa7b`.
- Exact PR HEAD `9e9acee89ecc28072b4695a3ee00d74d116530b2` passed [CI #42704543118](https://github.com/mcpdev80/baseharbor/actions/runs/42704543118): CLI shards `cli-0`, `cli-1`, `cli-2`, native Docker and Podman, and `PR Selected Checks` all SUCCESS.
- This test-holder regression is accepted independently from full remote management E2E; the release remains unreleased.
