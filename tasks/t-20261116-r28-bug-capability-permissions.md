---
id: t-20261116-r28-bug-capability-permissions
card_number: "0428-291"
card_short_title: "Scope inferred provider grants"
type: bug
areas: [security]
release: v0.4.28
version: ""
parent: v0.4.28
owner: w332-0428-288-composeids (handoff from w333-0428-291-capperms per coordinator, INCIDENTS 2026-11-26)
kanban_status: blocked
kanban_lane: blocked
kanban_summary: RabbitMQ is listed as replaceable Compose infrastructure yet Messaging Queue was not preselected; baha app init proposed…
kanban_title: 0428-291 · Scope inferred provider grants
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: "BLOCKED-BASELINE as STATE per w332 QUESTION (20:0xZ): Trusted Plan (.github#122, uncataloged cmd/baha/app_init_runtime_permission_scope_test.go) + downstream Selected Checks (UNIT_SCOPE empty) are develop-side family rows; w267 ruling 7199390854 keeps candidate product+tests only; qualify after freeze-lift #136 hop -> #1865 (+ #1867 sibling) merge. Evidence: head c945b2fcb/70c-series, runs 45868769156; see #1864 comments"
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261116-r28-bug-capability-permissions · Scope inferred provider grants #task #release/v0-4-28 #status/blocked #view/blocked #area/security #kind/bug
    <!-- generated:card -->
    **Owner:** w332-0428-288-composeids (handoff from w333-0428-291-capperms per coordinator, INCIDENTS 2026-11-26) · **Priority:** high  
    **Blocker:** BLOCKED-BASELINE as STATE per w332 QUESTION (20:0xZ): Trusted Plan (.github\#122, uncataloged cmd/baha/app\_init\_runtime\_permission\_scope\_test.go) + downstream Selected Checks (UNIT\_SCOPE empty) are develop-side family rows; w267 ruling 7199…  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w332-0428-288-composeids (handoff from w333-0428-291-capperms per coordinator, INCIDENTS 2026-11-26)  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

RabbitMQ is listed as replaceable Compose infrastructure yet Messaging Queue was not preselected; `baha app init` proposed `object-storage.s3/v1 runtime.create` for all 12 workload services despite no identified S3 capability. Distinguish a conservative optional toggle from a false detection; avoid universal runtime grants.

## Reproduction (2026-11-16 J-Commerce live test)

Init J-Commerce and inspect queue default, Runtime API operation discovery and list of services allowed to use `runtime.create` including caddy/cadvisor/prometheus.

## Acceptance

- Ensure provider suggestions and default selections are consistent with confidence and show why. Runtime operation grants are least privilege, tied to observed consumers or affirmative explicit selection. No automatic broad permission to unrelated services; negative security tests.
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
