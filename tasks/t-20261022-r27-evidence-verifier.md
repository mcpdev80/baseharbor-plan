---
id: t-20261022-r27-evidence-verifier
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
priority: critical
owner: w3-lane (W3 verifier package)
depends_on: [t-20261017-release-0-4-27-updates, t-20261022-r27-evidence-publisher, t-20261022-r27-evidence-resolver]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1048]
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261022-r27-evidence-verifier · evidence verifier #task #release/v0-4-27 #status/active #view/active #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** w3-lane (W3 verifier package) · **Priority:** critical  
    **PR:** [baseharbor#1048](https://github.com/mcpdev80/baseharbor/pull/1048)  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-evidence-publisher](t-20261022-r27-evidence-publisher.md), [t-20261022-r27-evidence-resolver](t-20261022-r27-evidence-resolver.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-evidence-publisher](t-20261022-r27-evidence-publisher.md), [t-20261022-r27-evidence-resolver](t-20261022-r27-evidence-resolver.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261022-r27-evidence-acceptance](t-20261022-r27-evidence-acceptance.md)  
**Owner:** w3-lane (W3 verifier package)  
**Priority:** critical  
**PRs:** [baseharbor#1048](https://github.com/mcpdev80/baseharbor/pull/1048)  
**Source:** 
<!-- /generated:links -->


# Receipt verifier: live approval, retained Git verification

## Goal
Implement scripts/receipt_verifier.py with live, approve and retained modes. No signatures and no API calls after approval.

## Scope and acceptance
- Live: authenticate successful exact run/attempt, repository, workflow/event, successful named gate job, plan and candidate/integration binding; compare exact committed receipt bytes.
- Approve: only an authenticated Owner workflow action, immediately after a new live verification, may add by/at/receipt_commit. Approval refers to the exact original receipt commit; user-controlled names are not authorization.
- Retained: verify protected Git ancestry and the unique permitted approval edit, reject subsequent edits and compare applicable plan/candidate without contacting GitHub.
- Wrong SHA, nonexistent run and edited receipt each fail closed. API unavailability is unverified, never PASS.
- Existing final-check logic consumes receipts only after skeleton acceptance and a separate cutover PR. No circular dependency on the producer workflow completing itself.

## Bootstrap
PR 1 is qualified by existing v0.4.26 legacy checks. Later changes may use only already accepted new components, never their own unaccepted successor. Keep the active legacy pipeline unchanged until the real skeleton is accepted.
