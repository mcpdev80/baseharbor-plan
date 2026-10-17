---
id: t-20261017-release-0-5-1-publish
type: acceptance
areas: [release]
release: v0.5.x
version: v0.5.1
release_stage: publish
parent: v0.5.x
owner: ""
priority: normal
depends_on: [t-20261017-release-0-5-1-qualify]
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo, mcpdev80/baseharbor-console, mcpdev80/baseharbor-node-connector]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261017-release-0-5-1-publish · v0.5.1 · Release: promote the approved candidate and deliver exact tagging commands #task #release/v0-5-x #status/planned #view/waiting #board/planned #area/release #kind/acceptance
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-5-1-qualify](t-20261017-release-0-5-1-qualify.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.5.x](../releases/v0.5.x.md) (v0.5.1)  
**Depends on:** [t-20261017-release-0-5-1-qualify](t-20261017-release-0-5-1-qualify.md)  
**Required by:** [t-20261017-release-0-5-1-verify](t-20261017-release-0-5-1-verify.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
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

Not started. Record actual source SHAs, outcomes, authorization where required, evidence and remaining blockers; do not infer acceptance from card creation.
