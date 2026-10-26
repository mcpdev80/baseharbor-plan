---
id: t-20261017-release-0-4-26-publish
type: acceptance
areas: [release]
release: v0.4.26
version: v0.4.26
release_stage: publish
parent: v0.4.26
owner: Codex (Owner-authorized v0.4.26 publication)
priority: normal
depends_on: [t-20261017-release-0-4-26-qualify]
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo, mcpdev80/baseharbor-console, mcpdev80/baseharbor-node-connector]
prs: [mcpdev80/baseharbor#1089]
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261017-release-0-4-26-publish · v0.4.26 · Release: promote the approved candidate and deliver exact tagging commands #task #release/v0-4-26 #status/active #view/active #area/release #kind/acceptance
    <!-- generated:card -->
    **Owner:** Codex (Owner-authorized v0.4.26 publication) · **Priority:** normal  
    **PR:** [baseharbor#1089](https://github.com/mcpdev80/baseharbor/pull/1089)  
    **Needs:** [t-20261017-release-0-4-26-qualify](t-20261017-release-0-4-26-qualify.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.26](../releases/v0.4.26.md) (v0.4.26)  
**Depends on:** [t-20261017-release-0-4-26-qualify](t-20261017-release-0-4-26-qualify.md)  
**Required by:** [t-20261017-release-0-4-26-verify](t-20261017-release-0-4-26-verify.md)  
**Owner:** Codex (Owner-authorized v0.4.26 publication)  
**Priority:** normal  
**PRs:** [baseharbor#1089](https://github.com/mcpdev80/baseharbor/pull/1089)  
**Source:** 
<!-- /generated:links -->

## Goal

Promote only approved content and provide the complete exact tagging command to the Maintainer.

## Scope and acceptance

- Require successful authenticated approval and separate Maintainer authorization for promotion/merge/publication. Verify current workflows, rulesets, exact content delta and candidate promotion constraints; no historical bypass.
- Use one reviewed release/promotion PR and the existing candidate/evidence handoff. Reconcile main-only hotfixes and ongoing develop safely. Promote the approved tree rather than accidentally including later unqualified develop work.
- Verify resulting main SHA/tree against approval using the existing release-handoff verifier and its allowed metadata policy. Preserve green evidence only under that verifier; no inferred SHA equivalence.
- Before declaring this card complete, hand the Maintainer one complete ready-to-paste command block with the ACTUAL version, full approved main SHA and verified repository/remote. Include clean-state/identity checks, fetch, local+remote tag-absence guards, annotated tag on that exact SHA and explicit push of that tag only. No placeholders or moving target in the final handoff.
- Tag only after explicit authorization (or let the Maintainer run the delivered block). Never move an existing version tag. The normal release workflow consumes immutable approval and handles images, binaries, checksums, release notes and provenance; run only genuinely supplemental publication checks.
- Record release PR/main SHA, exact delivered command, tag/ref and publish run if authorized. A prepared tagging command is not proof the tag was pushed; publication verification belongs to the next card.

## Required checks

Existing candidate/published-tree and approval verifiers, PR protection, actual immutable main/tag checks. No repeat of qualified runtime acceptance merely for publication.

## Dependencies and file ownership

- Procedure and sources: [release workflow](https://github.com/mcpdev80/baseharbor-plan/blob/main/RELEASE_WORKFLOW.md#publish). Stage dependencies are synchronized by `scripts/release_cycles.py sync`; do not weaken them manually.
- Owner updates this task, its release-specific audit/evidence and existing authorized PRs; coordinate product files through their normal owners. Planning goes directly to main.

## Handoff

### Explicit Owner-directed publication — 2026-10-26

Marcel explicitly instructed publication of all implemented v0.4.26 source now, despite failing or incomplete CI. For this release, that instruction supersedes the normal wait for complete pre-release approval. It does not turn missing or negative evidence into success, qualify the ecosystem, or authorize a false all-green statement. CI redesign remains v0.4.27 work.

- Promoted exact develop source `433a5702c9735ffbf1e9fffe7a7ae513b1c5c396`, tree `d7c63770a31b082ab7fc1c9fd254e4918efafc59`, through [PR #1089](https://github.com/mcpdev80/baseharbor/pull/1089) using the permitted squash merge. Released main is `640981588d8b9255fbe7db8ca26796db1da09eb2`; the Git tree is byte-identical to the selected develop tree. No product source was changed for publication.
- Created and independently re-fetched annotated tag `v0.4.26`, tag object `d09e1b024d1b161836b477ec37a95d017402fddc`, targeting that exact main commit. No existing version tag was moved.
- Started isolated one-time [publication run 40355992335](https://github.com/mcpdev80/baseharbor/actions/runs/40355992335) from `release-publish/v0.4.26-owner-20261026` at `a71b0b4a35e52fa80d1828845e3b8c1256e8b21b`. This branch changes only its own release workflow; neither main/develop CI nor repository rulesets were modified. The workflow binds Owner actor ID, exact source/tree and version; it creates no fabricated pre-release approval.
- Authorization/tagging job succeeded. Runtime image publication is in progress; real architecture-specific binary builds, checksum verification, provenance and GitHub Release publication follow. No product test matrix or native qualification was launched.
- A machine-readable `owner-release-decision.json` records the actual exception and explicitly sets complete pre-release approval to false. It is retained as an Actions artifact and is to be attached to the Release. Human release notes disclose the same decision briefly.
- Publication remains active until actual image/binary/release results are verified. Full pre-release qualification tasks and unresolved defects remain open; their state must not be rewritten as accepted merely because this release is Owner-directed. Existing `release/v0.4.26` and concurrent development branches were preserved.
