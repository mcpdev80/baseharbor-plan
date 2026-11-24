---
id: t-20261116-r28-bug-metrics-discovery
card_number: "0428-290"
card_short_title: "Validate metrics source mappin"
type: bug
areas: [observability]
release: v0.4.28
version: ""
parent: v0.4.28
owner: Codex (ChatGPT lane w122)
kanban_status: active
kanban_lane: active
kanban_summary: "Wizard found /metrics from a Bruno file and defaulted to caddy; generated source caddy:8080/metrics is not supported by Compose…"
kanban_title: 0428-290 · Validate metrics source mappin
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261116-r28-bug-metrics-discovery · Validate metrics source mapping #task #release/v0-4-28 #status/active #view/active #area/observability #kind/bug
    <!-- generated:card -->
    **Owner:** Codex (ChatGPT lane w122) · **Priority:** high  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** Codex (ChatGPT lane w122)  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Wizard found `/metrics` from a Bruno file and defaulted to `caddy`; generated source `caddy:8080/metrics` is not supported by Compose evidence (`caddy` ports 80/443). J-Commerce contains Quarkus Micrometer and Spring Boot Micrometer services.

## Reproduction (2026-11-16 J-Commerce live test)

Init original J-Commerce, accept default metrics service and port 8080; inspect generated metrics source `service: caddy`, `path: /metrics`. Compare Quarkus `/q/metrics` and Spring `/actuator/prometheus` configured routes.

## Acceptance

- Metrics discovery binds proven service, internal port and path together; reject or clearly mark unverified endpoints before apply. Support Quarkus/Spring Actuator paths and conventional `/metrics` based on evidence; do not confuse Prometheus backend with application exporter.
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

- Active implementation on product branch `lane-0428-290-metrics-discovery`, PR [#1832](https://github.com/mcpdev80/baseharbor/pull/1832). The current remote head is red-first test-only `a442738cb5600975662aed5440755a942b4bee3b`; do not merge it. Corrected mapping and tests are being prepared in the isolated product worktree. After the baseline run reaches terminal, integrate `145b4a20f35179a0ac6bc0a66666a846c1ae35c0` from `develop`, then push and verify the resulting exact head. Acceptance, independent review and merge remain open.

Source reproduction: 2026-11-16 J-Commerce guided-init/apply/destroy/reset transcript supplied by Owner.

## Baseline CI classification (2026-11-24)

- Red-first test-only head `a442738cb5600975662aed5440755a942b4bee3b`, run [45478910054](https://github.com/mcpdev80/baseharbor/actions/runs/45478910054), base `d0a6f370bdab87386819b61c0a85ae64e7814caf`. This is intentionally intermediate and is not merge evidence. `PR · Validation · cli-guided-tests` job `138750850316` executed `go test ./cmd/baha -run '^TestGuided'` and failed.
- `TestGuidedQuickInitDoesNotTreatBrunoRequestAsMetricsSource` and `TestGuidedQuickInitBindsQuarkusMetricsServicePortAndPath` both stopped before their assertions: `mustWriteWizardTestFile` uses `os.WriteFile` without creating parent directories. The helper behavior predates this card on develop; the new nested fixtures exposed the setup gap. Classification: test-fixture setup defects, not product mapping regressions. Fix the helper to create parent directories.
- `TestGuidedAdoptionSummaryFullyPopulated` changes the old green `TestAdoptionSummaryFullyPopulated` expectation from generic `/metrics` wording to the discovered source tuple. The develop witness only asserted generic wording, so its green result did not prove source mapping (too-weak assertion). The Owner also flagged the test input as an unproven mapping fixture; although the current diff calls `WithMetricsSource`, add an explicit precondition asserting the service, port and path before checking rendered output. The test-only head lacks the implementation that prints the tuple, so this failure is expected red-first evidence once that precondition is explicit.
- Baseline witness: these Bruno and Quarkus regressions do not exist at develop `d0a6f370`; `mustWriteWizardTestFile` exists there with the same plain `os.WriteFile` behavior; `TestAdoptionSummaryFullyPopulated` exists there with only the generic metrics assertion. Candidate implementation must land with the corrected fixture and regressions together.
- Before the candidate push, merge the current `origin/develop` tip `145b4a20f35179a0ac6bc0a66666a846c1ae35c0` normally. Collect two exact-head hosted CI run IDs for the integrated candidate; preserve independent Docker and rootless Podman evidence.
