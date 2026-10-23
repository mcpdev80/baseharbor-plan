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
