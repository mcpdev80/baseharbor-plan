---
id: t-20261024-r27-candidate-trigger-prototype
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
priority: high
owner: "ChatGPT (isolated v0.4.27 prototype)"
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1055]
sources: []
early: false
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261024-r27-candidate-trigger-prototype · CI: explicit candidate trigger prototype #task #release/v0-4-27 #status/active #view/active #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** ChatGPT (isolated v0.4.27 prototype) · **Priority:** high  
    **PR:** [baseharbor#1055](https://github.com/mcpdev80/baseharbor/pull/1055)  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** ChatGPT (isolated v0.4.27 prototype)  
**Priority:** high  
**PRs:** [baseharbor#1055](https://github.com/mcpdev80/baseharbor/pull/1055)  
**Source:** 
<!-- /generated:links -->

# CI: explicit candidate trigger prototype

## Goal
Prepare explicit candidate-ready PR trigger with no per-commit PR CI, without activating it during v0.4.26.

## Scope
- Isolated design, review and regression preparation only on the existing draft PR.
- No merge to develop, no Ruleset or production workflow changes, no v0.4.26 interference.
- Do not treat prototype output as accepted trusted evidence.

## Acceptance
- Mock event and token paths, draft/stale guards, workflow-policy and actionlint; independent E2E qualification after v0.4.26.
- Final independent check and Owner-authorized rollout must follow v0.4.26 completion.

## Dependencies and file ownership
The v0.4.27 release-start updates remain unaccepted; this active status documents isolated work only, not production readiness. Existing PR #1055 remains draft. No ownership of other tasks or PRs is implied.

## Handoff
- 2026-10-24: isolated preparation in [PR #1055](https://github.com/mcpdev80/baseharbor/pull/1055); current status active, not qualified or mergeable by this card.
- Draft-label event security fix: all twelve candidate guards in `ci.yml` now require a non-draft PR for `labeled` events; the separate artifact-GC test guard also rejects draft label events. Static regression checks cover both workflow surfaces. Candidate source head: `a77371a20e6a1959c7fc0e9e0adc4ce3689c7c1b`.
- Missing: executable workflow-policy/Actionlint/selected checks on exact head; authenticated GitHub App/PAT event E2E and base-SHA/stale-head verification. Keep on draft feature branch; v0.4.26 release freeze is binding.

- 2026-10-24: label-delete HTTP 404 is no longer ignored by the candidate submitter: it now fails closed before POST rather than reporting a spurious dispatch. Regression added for GET/DELETE-only on failure. Draft PR #1055 current head `1089a169061fec0fdc49ecb2140dc0b1001cdd3c` (unqualified until targeted checks run).

- 2026-10-24: tightened re-label race guard: after DELETE, the second GET must show `ci:validate` absent; otherwise fail with an actionable error and perform no POST. Added a mocked GET/DELETE/GET negative regression. Candidate head `24934756677fd261580f2f37b11ad61197f4444d`, draft/unqualified. This protects against silently claiming CI dispatch when GitHub has not actually removed the label.

- Current draft PR #1055 head: `4a89d8115ee146675599ca31bd8a1ac8486a91a9`. Submission text distinguishes a label request from proven CI completion. Independent checks remain outstanding.

- Latest prototype head `13e6a649200b70330e1179cd882bcdcb4e355522`: candidate submitter now rechecks exact target base SHA after label preparation and fails closed on a changed base before POST; mocked regression and all relevant fixture shapes updated. Static source review only; independent tests and actual event delivery not yet qualified.
