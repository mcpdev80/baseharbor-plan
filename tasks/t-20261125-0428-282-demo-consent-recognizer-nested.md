---
id: t-20261125-0428-282-demo-consent-recognizer-nested
card_number: "0428-282"
card_short_title: "demo consent recognizer"
type: bug
areas: [cli]
release: v0.4.28
version: ""
parent: ""
owner: w92-0428-282-democonsent
kanban_status: closed
kanban_lane: closed
kanban_summary: ""
kanban_title: 0428-282 · demo consent recognizer
priority: high
depends_on: []
repos: [mcpdev80/baseharbor-demo]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: dropped
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-25/0428-281-consent/diagnosis.md", "https://github.com/mcpdev80/baseharbor/actions/runs/45398943139"]
  - https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-25/0428-281-consent/diagnosis.md
  - https://github.com/mcpdev80/baseharbor/actions/runs/45398943139
---

- [x] t-20261125-0428-282-demo-consent-recognizer-nested · demo consent recognizer nested #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** w92-0428-282-democonsent · **Priority:** high  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-25/0428-281-consent/diagnosis.md), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/45398943139), [proof 3](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle6-2026-11-25/0428-281-consent/diagnosis.md), [proof 4](https://github.com/mcpdev80/baseharbor/actions/runs/45398943139)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** dropped  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w92-0428-282-democonsent  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Problem

- Where: baseharbor-demo tests/fixture-consent.py:45 (the recognizer) invoked as run_consented via tests/lib.sh:182-183. It accepts ONLY three exact message strings: direct_message ("<prefix>; refusing to record deployment state"), wrapped_message ("record deployment before mutation: " + direct_message), nested_wrapped_message (wrapped_message + ": " + direct_message).
- The refusal baha up actually surfaces is DOUBLY nested differently: app_apply.go:204 wraps ("record deployment before mutation: %w") an inner error whose message already embeds "; refusing to record deployment state" from deployment_record.go:369-371, producing a string outside the accepted set. The recognizer therefore raises and never extracts the 64-hex digest from error['next'], so run_consented never re-invokes with --confirm-candidate -> the gate fails closed.
- The baseharbor PRODUCT path is correct: #1807 (merged 7b45db92, ancestor of develop 46d3dccc) threads --confirm-candidate through app_input_resolver.go:536 / runtime_repository_up.go / app_apply.go; the digest survives to recordDeploymentBeforeMutation and is re-validated fail-closed. So NO baseharbor change is warranted (that would be an empty/wrong diff). This is why 0428-281 is superseded.

## Regression

- Extend the baseharbor-demo tests/fixture-consent.py recognizer to ALSO match the actual doubly-nested refusal form produced by app_apply.go:204 wrapping deployment_record.go:369-371, extract the exact 64-hex digest from the nested error['next'], and re-run with --confirm-candidate. Preserve the fail-closed guarantee: only the exact candidate-consent refusal (with a single exact source digest) may trigger a retry; arbitrary messages containing the phrase must still be rejected.

## Acceptance

- The v0.4.28 Docker Light gates policy + connectivity + reconciliation + full-destroy go GREEN against a demo_ref that contains this demo fix (previously failing only because the consent wrapper did not recognize the nested refusal).
- baseharbor-demo tests exercise run_consented on the nested refusal and assert a digest retry + fail-closed-when-no-consent.
- OWNER AUTHORIZATION REQUIRED before any edit: this is a baseharbor-demo repo/write-set change, OUT OF SCOPE of the prior baseharbor-product consent authorization. Do not implement until the owner grants the repo/write-set change.

Owner-AUTHORIZED separate baseharbor-demo consent PR. w92 dispatching. Scope tests/fixture-consent.py + regression; pull ci-operator.log from run 45398943139 first; merge by lane after green CI + required checks; then #1812 qualified, then serial #1819->#1820. #1812 stays workflow-only/blocked.

DISPOSITION A (owner): consent recognizer + regression ALREADY PRESENT in demo_ref f23b6e09 (PR #169 nested_wrapped_message + test_fixture_consent nested/stale-rejection). A demo PR would be empty. Full logs of all 4 failed jobs in run 45398943139: nested refusal -> emitted digest -> [ci-operator-testonly] decision log RETRY ACCEPTED -> failure occurs AFTER the retry. Consent is NOT the cause. Causal record corrected; post-retry gate failure triaged separately (card 0428-284).
