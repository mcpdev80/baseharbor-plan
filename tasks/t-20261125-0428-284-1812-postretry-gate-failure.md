---
id: t-20261125-0428-284-1812-postretry-gate-failure
card_number: "0428-284"
card_short_title: "1812 post-retry gate fail"
type: bug
areas: [ci, cli]
release: v0.4.28
version: ""
parent: ""
owner: 
kanban_status: blocked
kanban_lane: blocked
kanban_summary: ""
kanban_title: 0428-284 · 1812 post-retry gate fail
priority: high
depends_on: []
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo]
prs: []
sources: []
blocker: "Consent Demo-PR authorization is MOOT (the nested-refusal/digest-retry fix already exists in merged demo #169 + the demo ref #1812 uses -> an empty PR must NOT be created). Authoritative root cause (w97 eeda96c91): consented up reaches READY, then acceptance FAILS at INTERACTIVE OIDC operator authentication (baseharbor-demo scripts/acceptance.sh policy-acceptance step). This demo/operator-harness scope is NOT covered by the earlier narrow consent authorization -> FRESH OWNER DECISION required before any implementation. No lane dispatched. Preserve #1812->#1819->#1820."
wait_reason: ""
resolution: ""
evidence:
  - https://github.com/mcpdev80/baseharbor/actions/runs/45398943139
---

- [ ] t-20261125-0428-284-1812-postretry-gate-failure · #1812 post-retry gate failure #task #release/v0-4-28 #status/blocked #view/blocked #area/ci #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Blocker:** Consent Demo-PR authorization is MOOT (the nested-refusal/digest-retry fix already exists in merged demo \#169 + the demo ref \#1812 uses -\> an empty PR must NOT be created). Authoritative root cause (w97 eeda96c91): consented up reaches REA…  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/45398943139)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
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
