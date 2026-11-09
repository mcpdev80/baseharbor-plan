---
id: t-20261109-0427-182-serve-integration-holder-leak
card_number: "0427-182"
card_short_title: "0427-182 · Serve Integr test"
type: bug
areas: []
release: v0.4.27
version: ""
parent: v0.4.27
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0427-182 · 0427-182 · Serve Integr test
priority: ""
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261109-0427-182-serve-integration-holder-leak · 0427-182 · Serve integration test leaks a bound+serving holder that poisons later cmd/baha tests #task #release/v0-4-27 #status/planned #view/ready #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** unassigned  
**Priority:** not set  
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
