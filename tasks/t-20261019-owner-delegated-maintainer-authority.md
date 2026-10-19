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
resolution: ""
evidence: []
---

- [ ] t-20261019-owner-delegated-maintainer-authority · Document Owner-delegated Maintainer merge authority #task #release/v0-4-26 #status/active

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

### 2026-10-19 — Existing-linked central policy published in PR1006

- Current candidate7ff6972651733820286b5205f840058f55d6271d changes exactly three documentation files. Product agent entry point uses its existing central process link; Planning AGENTS/WORKFLOW already publish the Owner mandate.
- Earlier CI39235529033 found EN/DE literal mismatch, corrected in German guidelines. CI39235714798 then passed all selected docs checks but blocked unknown AGENTS.md impact. Removed only the redundant agent entry-point addition; no planner/CI exception, false qualification or o1 change. New exact candidate CI must pass before Owner-authorized regular merge.
- No additional repository review requested, no GitHub self-approval submitted. Existing account-level PR-only review exception is the authorized merge path; separate Required Checks remain enforced.

### 2026-10-19 — Explicit Owner assignment and claim before product changes

- Marcel's direct instruction authorizes documenting his delegated account authority without additional repository review. Existing integration ruleset23754541 already permits User22537373 PR-only review bypass; separate strict Required Check ruleset25223521 remains non-bypassable.
- Product baseline19548bf0; Planning baselinea69aef1a. No product source, CI rule, native test or protected worktree changed. Product documentation candidate follows this published claim.
