---
id: t-20261017-concise-code-comments
type: task
areas: [docs]
release: v0.4.26
version: ""
parent: v0.4.26
owner: "Codex (comment-guideline session)"
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#981"]
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261017-concise-code-comments · Docs: require clear and concise code comments #task #release/v0-4-26 #status/review #view/review #area/docs #kind/task
    <!-- generated:card -->
    **Owner:** Codex (comment-guideline session)  
    **PR:** [baseharbor#981](https://github.com/mcpdev80/baseharbor/pull/981)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** none  
**Required by:** [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md)  
**Owner:** Codex (comment-guideline session)  
**Priority:** not set  
**PRs:** [baseharbor#981](https://github.com/mcpdev80/baseharbor/pull/981)  
**Source:** 
<!-- /generated:links -->

## Goal

Make code comments clear, concise and useful through the canonical development guidelines.

## Scope

Only product `docs/DEVELOPMENT_GUIDELINES.md`: add a short normative subsection under source readability. Preserve required API/safety contracts; no rigid line cap, task history or narration of implementation. No production-code, CI or other task edits.

## Acceptance

- Public declarations follow Go doc-comment conventions; internal comments add non-obvious information.
- Comments use direct, precise language without filler, task/PR history, caller counts or paraphrased code.
- Normally one to three short sentences; document necessary safety, locking, errors and side effects. Longer architectural rationale belongs in existing architecture/ADR docs.
- Small product PR against develop, relevant documentation checks and exact-source planning handoff.

## Required checks

Existing documentation audit and trusted documentation CI, no runtime matrix.

## Dependencies and file ownership

Own only `docs/DEVELOPMENT_GUIDELINES.md`. Read current product and planning AGENTS; preserve other sessions' source and planning work.

## Handoff

- PR [#981](https://github.com/mcpdev80/baseharbor/pull/981), source `c5581feb8ba313122f0022a16ad005a056a60804`, based on develop `4bc21c4d7a55c253db70b5329ec4c5326b90e6a3`. Only `docs/DEVELOPMENT_GUIDELINES.md` changes (10 lines).
- Added a concise code-comment subsection: normally one to three short sentences; clear purpose/contract/reason; no filler, task/PR history, caller counts or implementation narration. Required safety/locking/error/side-effect guarantees remain; Go declaration comments and useful inline rationale stay permitted. No arbitrary hard line limit.
- Existing documentation audit PASS: 156 paired EN/DE pages; technical integrity, navigation, structure, size, governance, runtime and branding checks. `git diff --check` PASS. Trusted [CI run 39026276819](https://github.com/mcpdev80/baseharbor/actions/runs/39026276819) PASS: documentation audit, EN/DE strict builds, Pages candidate, focused policy checks and executed PR Selected Checks. PR #981 merged into develop at `d54ac358fb6a6b256164ac2689a33e981c013baa`. No runtime matrix launched; planning render/check and 47 planning tests PASS. Implementation complete; retained review state pending Maintainer task acceptance.
