---
id: t-20261017-release-0-4-27-qualify
card_number: "0427-008"
card_short_title: "complete required candidate"
type: acceptance
areas: [release]
release: v0.4.27
version: v0.4.27
release_stage: qualify
parent: v0.4.27
owner: mission-closeout27
kanban_lane: wait
kanban_summary: Obtain complete release-boundary validation for the frozen candidate.
kanban_status: wait
kanban_title: "0427-008 · complete required candidate"
priority: normal
depends_on: [t-20261017-release-0-4-27-prepare]
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo]
prs: []
sources: []
blocker: ""
wait_reason: "v0.4.27 was in fact published: release run 43991839986 succeeded and the tag binary reports source 6c40fab4. The release-stage validator still finds 0427-189 active and 0427-191 planned in the v0.4.27 scope; reconcile those outstanding cards before marking qualification accepted."
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/43991839986", "https://github.com/mcpdev80/baseharbor/releases/tag/v0.4.27", "https://github.com/mcpdev80/baseharbor/actions/runs/43971466986"]
---

- [ ] t-20261017-release-0-4-27-qualify · v0.4.27 · Pre-release: complete required candidate checks #task #release/v0-4-27 #status/wait #view/wait #area/release #kind/acceptance
    <!-- generated:card -->
    **Owner:** mission-closeout27 · **Priority:** normal  
    **Waiting:** v0.4.27 was in fact published: release run 43991839986 succeeded and the tag binary reports source 6c40fab4. The release-stage validator still finds 0427-189 active and 0427-191 planned in the v0.4.27 scope; reconcile those outstanding car…  
    **Needs:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/43991839986), [proof 2](https://github.com/mcpdev80/baseharbor/releases/tag/v0.4.27), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/43971466986)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.27](../releases/v0.4.27.md) (v0.4.27)  
**Depends on:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md)  
**Required by:** [t-20261017-release-0-4-27-publish](t-20261017-release-0-4-27-publish.md)  
**Owner:** mission-closeout27  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Obtain complete release-boundary validation for the frozen candidate.

## Scope and acceptance

- Require accepted preparation and explicit Maintainer authorization for the complete pre-release. Record that authorization and exact candidate/ecosystem matrix before dispatch.
- Use the existing pre-release workflow, canonical release requirements and original test owners. Inspect queued/running equivalent runs first; do not create a duplicate full run or a new proof system.
- Fix demonstrated failures and rerun only the failed or affected checks during diagnosis. Normal job results determine success; no manifests, evidence reuse or completed-run/job re-verification.
- Targeted/selected runs cover only their chosen scope. Complete validation executes every required test on the frozen ecosystem sources through normal workflow dependencies. No release-approved.json or other approval payload is required.
- Deliver exact approval origin, candidate/consumer SHAs, complete coverage, accepted exceptions if any and remaining failures. Do not claim release-ready with required coverage missing. No promotion or tagging under this card.

## Required checks

Normal required-job result checks and actual Docker/rootless Podman/consumer test execution. Not-required is justified, never synthetic PASS; no repeat whole matrix merely because one gate failed.

## Dependencies and file ownership

- Procedure and sources: [release workflow](https://github.com/mcpdev80/baseharbor-plan/blob/main/RELEASE_WORKFLOW.md#qualify). Stage dependencies are synchronized by `scripts/release_cycles.py sync`; do not weaken them manually.
- Owner updates this task, its release-specific audit/evidence and existing authorized PRs; coordinate product files through their normal owners. Planning goes directly to main.

## Handoff

- 2026-11-14 (mission-closeout27, review-pending act): no complete pre-release run exists on any 0.4.27 candidate head; targeted run 43633496362 failed at fe018b97 and current head 385b0410 has no checks reported. Candidate not frozen (pinned Demo SHA 2494b05a only on open PR #160), pre-release source gate broken on main (PR #1576, .github/ routing = Owner), no Maintainer run authorization recorded. Full dossier: [round-1](../evidence/r27-closeout-2026-11-14/round-1.md). Review state deferred: schema requires a card PR (plan.py:417); no admissible product PR exists for this acceptance card.

## Release-state reconciliation — 2026-11-21

- The prior wait note described an unpublished candidate and is stale. GitHub now has tag `v0.4.27` at commit `6c40fab4de9a611bc8da2e834417427a83c01ca5`; the release workflow [43991839986](https://github.com/mcpdev80/baseharbor/actions/runs/43991839986) completed successfully and the published `baha version --json` reports version `0.4.27` and that exact commit.
- The planner still requires the outstanding v0.4.27-scope cards 0427-189 (active) and 0427-191 (planned) to be accepted before it allows qualification closeout. The release event does not erase those live scope records. No acceptance is claimed until their status is reconciled.
