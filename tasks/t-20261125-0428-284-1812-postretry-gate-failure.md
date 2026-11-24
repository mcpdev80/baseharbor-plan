---
id: t-20261125-0428-284-1812-postretry-gate-failure
card_number: "0428-284"
card_short_title: "1812 post-retry gate fail"
type: bug
areas: [ci, cli]
release: v0.4.28
version: ""
parent: ""
owner: Codex (w115-0428-284-testcert)
kanban_status: active
kanban_lane: active
kanban_summary: ""
kanban_title: 0428-284 · 1812 post-retry gate fail
priority: high
depends_on: []
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence:
  - https://github.com/mcpdev80/baseharbor/actions/runs/45398943139
---

- [ ] t-20261125-0428-284-1812-postretry-gate-failure · #1812 post-retry gate failure #task #release/v0-4-28 #status/active #view/active #area/ci #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** Codex (w115-0428-284-testcert) · **Priority:** high  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/45398943139)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** Codex (w115-0428-284-testcert)  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Problem

- Context: 0428-282 (consent fixture) DISPROVED/DROPPED — the consent retry works. Owner-verified all 4 failed jobs in run 45398943139 log the nested refusal, the emitted digest, then the [ci-operator-testonly] decision RETRY ACCEPTED, and the execution failure happens LATER than the retry.
- So #1812's Docker Light gates still fail for a reason downstream of consent. The exact post-retry failure point (which command/step after the consented re-run errors, and with what message) is NOT yet captured. This card exists to triage THAT, not to change consent.

## Triage (read-only first; no edits until root cause proven)

- Pull the FULL per-job logs for run 45398943139 jobs policy/connectivity/reconciliation/full-destroy; after the consent-retry-accepted line, capture the FIRST error (file/step/command + exit) that fails the gate. Determine whether it is (a) a product runtime defect, (b) a demo Light-gate harness setup issue, or (c) an operator-provisioning issue (same family as 0428-283 static/mcp) — with file:line + run-log witnesses.
- Reconcile against w93 (operator-auth commonality in Light harness) + w94 (prerequisite map). The outcome decides what must change before #1812 can go green on its exact head.

## Acceptance

- A named, evidenced root cause for the post-retry #1812 Light-gate failure + the minimal fix scoped to the correct repo/file (owner-authorized separately if it touches .github/product contract or the Light harness). #1812 stays blocked until this is proven and its Docker then Podman Light gates run green on the exact head.

## Handoff

- Owner question sent by session w115: provide the existing CI IdP issuer/client and cert/CA inputs, plus the Keycloak X.509 flow mapping the certificate to the test operator. Current demo source contains no such realm/client/certificate fixture. No synthetic testonly route, product-auth change, or consent edit is in scope.
- Demo checkout branch `lane-0428-284-testcert` is based on origin/develop `7d9eb21af4b0a3c3db2dbc4dcaf8db22bef03d1c`; no product files changed. The independent acceptance-group reporting fix remains pending under the same mission.
- No PR, product verification, or CI run exists for this lane.
