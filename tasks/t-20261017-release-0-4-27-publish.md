---
id: t-20261017-release-0-4-27-publish
card_number: "0427-007"
card_short_title: "promote the validated"
type: acceptance
areas: [release]
release: v0.4.27
version: v0.4.27
release_stage: publish
parent: v0.4.27
owner: mission-closeout27
kanban_lane: wait
kanban_summary: Promote only approved content and provide the complete exact tagging command to the Maintainer.
kanban_status: wait
kanban_title: "0427-007 · promote the validated"
priority: normal
depends_on: [t-20261017-release-0-4-27-qualify]
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo]
prs: []
sources: []
blocker: ""
wait_reason: "The release was actually published at tag v0.4.27 on 6c40fab4 (run 43991839986 succeeded); the old #1574-conflict note is stale. Keep this stage in Wait because 0427-008 cannot yet be accepted: the validator sees outstanding v0.4.27-scope cards 0427-189 and 0427-191."
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/43991839986", "https://github.com/mcpdev80/baseharbor/releases/tag/v0.4.27", "https://github.com/mcpdev80/baseharbor/tree/v0.4.27"]
---

- [ ] t-20261017-release-0-4-27-publish · v0.4.27 · Release: promote the validated candidate and deliver exact tagging commands #task #release/v0-4-27 #status/wait #view/wait #area/release #kind/acceptance
    <!-- generated:card -->
    **Owner:** mission-closeout27 · **Priority:** normal  
    **Waiting:** The release was actually published at tag v0.4.27 on 6c40fab4 (run 43991839986 succeeded); the old \#1574-conflict note is stale. Keep this stage in Wait because 0427-008 cannot yet be accepted: the validator sees outstanding v0.4.27-scope…  
    **Needs:** [t-20261017-release-0-4-27-qualify](t-20261017-release-0-4-27-qualify.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/43991839986), [proof 2](https://github.com/mcpdev80/baseharbor/releases/tag/v0.4.27), [proof 3](https://github.com/mcpdev80/baseharbor/tree/v0.4.27)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.27](../releases/v0.4.27.md) (v0.4.27)  
**Depends on:** [t-20261017-release-0-4-27-qualify](t-20261017-release-0-4-27-qualify.md)  
**Required by:** [t-20261017-release-0-4-27-verify](t-20261017-release-0-4-27-verify.md)  
**Owner:** mission-closeout27  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Promote only approved content and provide the complete exact tagging command to the Maintainer.

## Scope and acceptance

- Require successful complete validation and separate Maintainer authorization for promotion/merge/publication. Verify current workflows, rulesets, exact content delta and candidate promotion constraints; no historical bypass.
- Use one reviewed release/promotion PR and the reviewed immutable candidate handoff. Reconcile main-only hotfixes and ongoing develop safely. Promote the approved tree rather than accidentally including later unqualified develop work.
- Verify the resulting main SHA/tree against the intended candidate directly using Git. No CI evidence verifier or inferred SHA equivalence.
- Before declaring this card complete, hand the Maintainer one complete ready-to-paste command block with the ACTUAL version, full approved main SHA and verified repository/remote. Include clean-state/identity checks, fetch, local+remote tag-absence guards, annotated tag on that exact SHA and explicit push of that tag only. No placeholders or moving target in the final handoff.
- Tag only after explicit authorization (or let the Maintainer run the delivered block). Never move an existing version tag. The normal release workflow executes the required reusable pre-release jobs on the exact tag, then handles images, binaries, checksums, release notes and provenance.
- Record release PR/main SHA, exact delivered command, tag/ref and publish run if authorized. A prepared tagging command is not proof the tag was pushed; publication verification belongs to the next card.

## Required checks

Direct Git candidate/published-tree checks, normal required jobs and immutable main/tag checks. No manifest or run-history re-verification.

## Dependencies and file ownership

- Procedure and sources: [release workflow](https://github.com/mcpdev80/baseharbor-plan/blob/main/RELEASE_WORKFLOW.md#publish). Stage dependencies are synchronized by `scripts/release_cycles.py sync`; do not weaken them manually.
- Owner updates this task, its release-specific audit/evidence and existing authorized PRs; coordinate product files through their normal owners. Planning goes directly to main.

## Handoff

- 2026-11-14 (mission-closeout27, review-pending act): promotion not authorized and prerequisites unmet — PR #1574 is CONFLICTING against main (478 conflicted paths, all .github/** = Owner scope), validation missing, pinned Demo SHA unreachable. No tag/Release/publication executed (frozen scope). Ready-to-paste guards and the post-merge block recipe are in the dossier; the final actual-SHA block needs the authorized promotion merge first. Full dossier: [round-1](../evidence/r27-closeout-2026-11-14/round-1.md). Review state deferred: schema requires a card PR (plan.py:417); no admissible product PR exists for this acceptance card.

## Release-state reconciliation — 2026-11-21

- Published tag `v0.4.27` resolves to commit `6c40fab4de9a611bc8da2e834417427a83c01ca5`; Release workflow [43991839986](https://github.com/mcpdev80/baseharbor/actions/runs/43991839986) succeeded and the GitHub Release is live. Thus the prior “prepared only / #1574 conflicting” wait note is stale.
- This card remains in Wait until the release-cycle validator accepts its qualification predecessor. It currently reports 0427-189 active and 0427-191 planned as unfinished tasks in the release scope.
