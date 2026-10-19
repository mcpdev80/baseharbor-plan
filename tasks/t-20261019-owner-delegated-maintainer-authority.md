---
id: t-20261019-owner-delegated-maintainer-authority
type: maintenance
areas: [docs, ci]
release: v0.4.26
version: ""
parent: v0.4.26
owner: "Codex (Owner-authorized Maintainer policy)"
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1006]
sources: []
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1006","https://github.com/mcpdev80/baseharbor/actions/runs/39236044976","https://github.com/mcpdev80/baseharbor/commit/bb91fbc327414952b36a88271153db43970280cc"]
---

- [x] t-20261019-owner-delegated-maintainer-authority · Document Owner-delegated Maintainer merge authority #task #release/v0-4-26 #status/closed #view/closed #board/planned #area/ci #area/docs #kind/maintenance
    <!-- generated:card -->
    **Owner:** Codex (Owner-authorized Maintainer policy) · **Priority:** high  
    **PR:** [baseharbor#1006](https://github.com/mcpdev80/baseharbor/pull/1006)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1006), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/39236044976), [proof 3](https://github.com/mcpdev80/baseharbor/commit/bb91fbc327414952b36a88271153db43970280cc)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** none  
**Required by:** [t-20261017-release-0-4-26-prepare](t-20261017-release-0-4-26-prepare.md)  
**Owner:** Codex (Owner-authorized Maintainer policy)  
**Priority:** high  
**PRs:** [baseharbor#1006](https://github.com/mcpdev80/baseharbor/pull/1006)  
**Source:** 
<!-- /generated:links -->

## Goal

Marcel explicitly directed that agents acting on his instructions through @mcpdev80 inherit his repository Maintainer authority and need no additional repository review before authorized merges.

## Scope

Update the central EN/DE product development guidelines, Planning agent entry point/workflow and review-enforcement snapshot. The existing product agent entry point already links the central development process and needs no duplicate rule. Use the existing account's live PR-only review exception; do not change technical CI enforcement, product code, protected worktrees, claims or native resources.

## Acceptance

Owner authorization and delegated execution are explicit; no fake independent/self approval or repeated review-only confirmation. Record actual current live rulesets and distinguish them from the old proposal. Publish product PR and merge through actual green Required Checks; keep Planning/Obsidian current and validated.

## Required checks

Existing documentation/workflow checks selected by trusted CI; regular Planning generator/check and47tests. No runtime or full matrix.

## Dependencies and file ownership

Owned docs: product docs/DEVELOPMENT_GUIDELINES.md, docs/de/DEVELOPMENT_GUIDELINES.md, docs/internal/review-protection.md; Planning AGENTS.md, WORKFLOW.md and the delegation decision. Preserve Flash/o1's existing source/binding work.

## Handoff

### 2026-10-19 — Owner-authorized acceptance and actual regular merge completed

- PR1006 final source7ff6972651733820286b5205f840058f55d6271d: actual CI39236044976 SUCCESS, including app15368 PR Selected Checks118005658109, Trusted Plan, workflow policy, Focused Python, EN/DE strict builds, documentation audit and Pages candidate.
- Owner-authorized acceptance executed without another repository reviewer or fabricated self/independent approval. Regular Maintainer squash merge succeeded asbb91fbc327414952b36a88271153db43970280cc using the existing User22537373 PR-only review exception. Separate technical Required Checks were green; no ruleset or required-check bypass changed.
- Product guidelines EN/DE and current/historical review-protection note are published on develop. Existing product AGENTS central-process link adopts that authority; Planning AGENTS/WORKFLOW and accepted delegation decision are already published. No runtime/CI code, native tests, protected o1 files or unrelated source claims changed.
- This task is accepted/closed by the explicitly delegated Maintainer; remaining release/native work is not accepted by implication. Publish regular generated Planning/Obsidian closeout and validate the final pushed SHA.

### 2026-10-19 — Existing-linked central policy published in PR1006

- Current candidate7ff6972651733820286b5205f840058f55d6271d changes exactly three documentation files. Product agent entry point uses its existing central process link; Planning AGENTS/WORKFLOW already publish the Owner mandate.
- Earlier CI39235529033 found EN/DE literal mismatch, corrected in German guidelines. CI39235714798 then passed all selected docs checks but blocked unknown AGENTS.md impact. Removed only the redundant agent entry-point addition; no planner/CI exception, false qualification or o1 change. New exact candidate CI must pass before Owner-authorized regular merge.
- No additional repository review requested, no GitHub self-approval submitted. Existing account-level PR-only review exception is the authorized merge path; separate Required Checks remain enforced.

### 2026-10-19 — Explicit Owner assignment and claim before product changes

- Marcel's direct instruction authorizes documenting his delegated account authority without additional repository review. Existing integration ruleset23754541 already permits User22537373 PR-only review bypass; separate strict Required Check ruleset25223521 remains non-bypassable.
- Product baseline19548bf0; Planning baselinea69aef1a. No product source, CI rule, native test or protected worktree changed. Product documentation candidate follows this published claim.
