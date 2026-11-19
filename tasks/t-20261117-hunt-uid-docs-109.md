---
id: t-20261117-hunt-uid-docs-109
release: v0.4.28
repos: [mcpdev80/baseharbor]
card_number: "0428-109"
title: "v0.4.28 lacks release notes page and populated CHANGELOG"
kanban_status: closed
kanban_lane: closed
kanban_title: 0428-109 · v0.4.28 lacks release notes
kanban_summary: "Document the merged v0.4.28 configuration-error behavior from #1666 and Keycloak native metrics registration from #1660 in the…"
sources: []
source_note: "hunt hunt-uid-docs (akte: evidence/r28-welle3-2026-11-16/hunt-uid-docs/befund-1.md)"
depends_on: []
owner: Codex (Codeman lane)
blocker: ""
wait_reason: ""
resolution: accepted
superseded_by: ""
prs: [mcpdev80/baseharbor#1681]
evidence: ["https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/hunt-uid-docs/befund-1.md", "https://github.com/mcpdev80/baseharbor/commit/b548828d33856e70a8f206a5150824ed9f8fe520", "https://github.com/mcpdev80/baseharbor/pull/1681", "https://github.com/mcpdev80/baseharbor/actions/runs/44060670144", "https://github.com/mcpdev80/baseharbor/commit/907f16713cbf38693d30c9dadaad7fe299759219"]
card_short_title: v0.4.28 lacks release notes
---

- [x] t-20261117-hunt-uid-docs-109 · v0.4.28 lacks release notes page and populated CHANGELOG #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/task
    <!-- generated:card -->
    **Owner:** Codex (Codeman lane)  
    **PR:** [baseharbor#1681](https://github.com/mcpdev80/baseharbor/pull/1681)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle3-2026-11-16/hunt-uid-docs/befund-1.md), [proof 2](https://github.com/mcpdev80/baseharbor/commit/b548828d33856e70a8f206a5150824ed9f8fe520), [proof 3](https://github.com/mcpdev80/baseharbor/pull/1681), [proof 4](https://github.com/mcpdev80/baseharbor/actions/runs/44060670144), [proof 5](https://github.com/mcpdev80/baseharbor/commit/907f16713cbf38693d30c9dadaad7fe299759219)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** v0.4.28  
**Depends on:** none  
**Owner:** Codex (Codeman lane)  
**Priority:** not set  
**PRs:** [baseharbor#1681](https://github.com/mcpdev80/baseharbor/pull/1681)  
**Source:** 
<!-- /generated:links -->


## Goal

Document the merged v0.4.28 configuration-error behavior from #1666 and Keycloak native metrics registration from #1660 in the release page and Keep a Changelog Unreleased section. Preserve the existing optional Perses entry.

## Scope

- In scope: CHANGELOG.md and docs/releases/v0.4.28.md.
- Out of scope: product behavior, published release or tag state, unrelated release history.

## Acceptance

- The v0.4.28 release page describes the user-visible configuration failure behavior and Keycloak metrics fix accurately.
- CHANGELOG Unreleased contains these two fixes with Keep a Changelog categories; existing Perses content remains under Added.
- The v0.4.28 page remains indexed and documentation locale/style audits pass.

## Test binding

- Test binding: normal documentation validation.
- Local route: bash scripts/documentation-audit.sh; python3 scripts/check_docs_locale_parity.py; git diff --check. All passed on exact commit b548828d33856e70a8f206a5150824ed9f8fe520.
- CI route: ready PR paths select mkdocs-en-strict, mkdocs-de-strict, pages-candidate-build, documentation-audit, Source format and Trusted Plan. Exact PR run: 44060670144 passed.

## Handoff

PR #1681 merged to develop as 907f16713cbf38693d30c9dadaad7fe299759219 from head b548828d33856e70a8f206a5150824ed9f8fe520. Local documentation audit and EN/DE parity checks passed; exact-head CI run 44060670144 passed.
