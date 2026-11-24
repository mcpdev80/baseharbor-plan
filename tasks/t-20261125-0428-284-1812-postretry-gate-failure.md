---
id: t-20261125-0428-284-1812-postretry-gate-failure
card_number: "0428-284"
card_short_title: "1812 post-retry gate fail"
type: bug
areas: [ci, cli]
release: v0.4.28
version: ""
parent: ""
owner: w115-0428-284-testcert
kanban_status: blocked
kanban_lane: blocked
kanban_summary: ""
kanban_title: 0428-284 · 1812 post-retry gate fail
priority: high
depends_on: []
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo]
prs: [mcpdev80/baseharbor-demo#173, mcpdev80/baseharbor#173]
sources: []
blocker: "Header half DELIVERED: demo #173 merged 87f5b28d, exact-head hosted runs 45448531969+45448729972 both green (2 run ids). Remaining half = OWNER ESCALATION per mandate: non-interactive test-certificate login needs issuer/client/certificate/Keycloak X.509 inputs (external certificate/production-prep class) - Lane-Codex may not self-authorize. #1812 policy gate stays red until this lands."
wait_reason: ""
resolution: ""
evidence:
  - https://github.com/mcpdev80/baseharbor/actions/runs/45398943139
  - https://github.com/mcpdev80/baseharbor-demo/pull/173
  - https://github.com/mcpdev80/baseharbor-demo/actions/runs/45448531969
  - https://github.com/mcpdev80/baseharbor-demo/actions/runs/45448729972
---

- [ ] t-20261125-0428-284-1812-postretry-gate-failure · #1812 post-retry gate failure #task #release/v0-4-28 #status/blocked #view/blocked #area/ci #area/cli #kind/bug
    <!-- generated:card -->
    **Owner:** w115-0428-284-testcert · **Priority:** high  
    **PR:** [baseharbor-demo#173](https://github.com/mcpdev80/baseharbor-demo/pull/173), [baseharbor#173](https://github.com/mcpdev80/baseharbor/pull/173)  
    **Blocker:** Header half DELIVERED: demo \#173 merged 87f5b28d, exact-head hosted runs 45448531969+45448729972 both green (2 run ids). Remaining half = OWNER ESCALATION per mandate: non-interactive test-certificate login needs issuer/client/certificate/…  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/45398943139), [proof 2](https://github.com/mcpdev80/baseharbor-demo/pull/173), [proof 3](https://github.com/mcpdev80/baseharbor-demo/actions/runs/45448531969), [proof 4](https://github.com/mcpdev80/baseharbor-demo/actions/runs/45448729972)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** blocked  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w115-0428-284-testcert  
**Priority:** high  
**PRs:** [baseharbor-demo#173](https://github.com/mcpdev80/baseharbor-demo/pull/173), [baseharbor#173](https://github.com/mcpdev80/baseharbor/pull/173)  
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

- **Lösung (Codex-Lane w115):** Umfang ergänzt um demo-only non-interactive Test-Zertifikat-Anmeldung (Produkt-Auth/Consent unverändert); Entscheidungsstand: Nachweis läuft, Produkt-Delta nur als Eskalation; Header-Fix bereits via #173 gemergt (2 Run-Zeugen).


- Owner question sent by session w115: provide the existing CI IdP issuer/client and cert/CA inputs, plus the Keycloak X.509 flow mapping the certificate to the test operator. Current demo source contains no such realm/client/certificate fixture. No synthetic testonly route, product-auth change, or consent edit is in scope.
- Demo PR [#173](https://github.com/mcpdev80/baseharbor-demo/pull/173) merged to develop at `87f5b28dc6a3447092389eb7d2790b76a2958bba`; source head `07a12287bf2c22717d9196d91d00217aba86cc12`. Scope is only concrete acceptance-group failure reporting (`scripts/acceptance.sh`, `scripts/report.sh`, `tests/lib.sh`, `tests/policy/run.sh`, and the reporting regression test). No product-auth, consent, or `.github/**` changes.
- PR-triggered workflow diagnosis per owner: failed run 45447956490 was on old candidate `8f706b7d2c0aad81287c0229868850e7157e2077`; first failure was the stale expected diagnostic string in `tests/test_fixture_consent.py:56` (`test_policy_gate_has_secret_safe_unexpected_error_diagnostic`). This was a test assertion mismatch caused by the new diagnostic format, not a certificate probe and not a guided-consent regression. Updated the assertion; focused regression passed.
- Exact merged head qualified by workflow runs [45448531969](https://github.com/mcpdev80/baseharbor-demo/actions/runs/45448531969) and [45448729972](https://github.com/mcpdev80/baseharbor-demo/actions/runs/45448729972), both success on `07a12287bf2c22717d9196d91d00217aba86cc12`. These were manual dispatches of the existing guided-consent workflow because its pull_request filter targets `main`, while this PR targets `develop`; no workflow policy changes were made.
- Certificate-login sub-item is `owner decision pending`: owner inputs requested are the existing IdP issuer/client, test certificate and CA material, and Keycloak X.509 flow mapping to the test operator. Do not implement a new grant/client-auth method in BaseHarbor product auth. Interactive-OIDC policy-gate failure remains open pending that owner certificate-login ruling. No cert-login implementation is included in PR #173.
