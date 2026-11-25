---
id: t-20261116-r28-bug-installation-reset-recovery
card_number: "0428-287"
card_short_title: "Unblock full installation rese"
type: bug
areas: [lifecycle]
release: v0.4.28
version: ""
parent: v0.4.28
owner: w157-0428-287-pr1835-preservation
kanban_status: active
kanban_lane: active
kanban_summary: "baha destroy --yes selects all owned resources, asks for two current-plan confirmations plus deletion consent, but aborts…"
kanban_title: 0428-287 · Unblock full installation rese
priority: critical
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1835]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261116-r28-bug-installation-reset-recovery · Unblock full installation reset #task #release/v0-4-28 #status/active #view/active #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** w157-0428-287-pr1835-preservation · **Priority:** critical  
    **PR:** [baseharbor#1835](https://github.com/mcpdev80/baseharbor/pull/1835)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w157-0428-287-pr1835-preservation  
**Priority:** critical  
**PRs:** [baseharbor#1835](https://github.com/mcpdev80/baseharbor/pull/1835)  
**Source:** 
<!-- /generated:links -->

## Goal

`baha destroy --yes` selects all owned resources, asks for two current-plan confirmations plus deletion consent, but aborts because application destroy preflight fails on retained provider ownership. Global XDG state and Core resources remain; user had to manually delete Docker resources and BaseHarbor directories.

## Reproduction (2026-11-16 J-Commerce live test)

Start Core; create the same failed J-Commerce app registration; run `baha destroy --yes`; consent three times. Inspect cleanup report: app FAILED, target-runtime SKIPPED, xdg-data/config SKIPPED.

## Acceptance

- An explicitly authorized installation destroy handles unmaterialized/broken app records without bypassing authorization or deleting ambiguous/foreign resources. Clearly enumerate preserved items, finish verifiable owned Core/provider/registry cleanup and rerun idempotently. Native Docker and rootless Podman coverage; no broad docker prune.
- Preserve existing BaseHarbor safety, immutable candidate consent, source ownership and shared-provider isolation. Never bypass preflight or delete foreign resources.
- Include positive/negative regressions and classify baseline-red vs candidate-green.

## Required checks and CI mapping

- Discover all affected existing tests; implement smallest causal regression and register it in existing package tests / PR-gate selection. Prove touched paths select the test and unrelated paths do not trigger unnecessary full native gates.
- Capture exact SHA, test ID, actual CI check/trigger and passing run URL. Where behavior is common to Docker and rootless Podman, produce independent native evidence in existing appropriate integration/release qualification gates. No separate CI framework.
- Reproduction is local user evidence; its observations must be verified in code before declaring a product fix.

## Mandatory regression and existing-green-test audit

- **Investigate the green-test gap before implementing the fix:** identify all existing unit, contract, integration, native Docker, native rootless Podman and release/guided journey tests that *claim or should claim* this behavior; record exact test IDs, assertions, fixtures, mocks, skipped paths, CI selectors, job names and actual run evidence. Do not infer coverage from a green check.
- Prove whether the existing green test path actually executed the failing behavior and rejected it (including Compose detection -> generated manifest -> apply/preflight -> interrupted deployment -> app destroy -> installation destroy where relevant). Classify each gap: missing test, too-weak assertions, fixture mismatch, skipped/conditional path, wrong CI mapping, or actual product regression.
- **Red-first proof is mandatory:** add a deterministic reproduction that fails against the affected current baseline with the exact J-Commerce failure mode, then passes on the candidate. A test that remains green on the broken baseline cannot close the bug.
- Validate the changed test is discovered and executed in the *real* appropriate hosted CI check with a positive path-selection proof; show that unrelated changes do not relaunch costly native suites. Capture exact commit SHA, test ID, check name, selector/trigger, run URL and assertion result. Never count a skipped, mocked-only or non-executed assertion as native PASS.
- Where lifecycle behavior is supported for both engines, provide independent native Docker and rootless Podman verification, using existing acceptance/release qualification runs rather than adding duplicate heavyweight PR gates. Do not change gate/permission/security semantics merely to turn tests green.

## Dependencies and file ownership

- Coordinate shared CLI, wizard, lifecycle and provider files with existing v0.4.28 CLI redesign owners; no competing writes or blanket permissions.

## Handoff

- Planned only. No implementation, PR, merge or acceptance claimed. Source: 2026-11-16 J-Commerce guided-init/apply/destroy/reset transcript supplied by Owner.
