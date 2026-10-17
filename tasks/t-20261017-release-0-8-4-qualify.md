---
id: t-20261017-release-0-8-4-qualify
type: acceptance
areas: [release]
release: v0.8.x
version: v0.8.4
release_stage: qualify
parent: v0.8.x
owner: ""
priority: normal
depends_on: [t-20261017-release-0-8-4-prepare]
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo, mcpdev80/baseharbor-console, mcpdev80/baseharbor-node-connector]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261017-release-0-8-4-qualify · v0.8.4 · Pre-release: obtain complete authenticated approval #task #release/v0-8-x #status/planned #view/waiting #board/planned #area/release #kind/acceptance
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-8-4-prepare](t-20261017-release-0-8-4-prepare.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.8.x](../releases/v0.8.x.md) (v0.8.4)  
**Depends on:** [t-20261017-release-0-8-4-prepare](t-20261017-release-0-8-4-prepare.md)  
**Required by:** [t-20261017-release-0-8-4-publish](t-20261017-release-0-8-4-publish.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Obtain complete authenticated release-boundary approval for the frozen candidate.

## Scope and acceptance

- Require accepted preparation and explicit Maintainer authorization for the complete pre-release. Record that authorization and exact candidate/ecosystem matrix before dispatch.
- Use the existing pre-release workflow, canonical release requirements, resume verifier and original gate owners. Inspect queued/running equivalent runs first; do not create a duplicate full run or a new proof system.
- An overall red workflow does not invalidate every green gate: preserve authenticated successful individual receipts. Fix demonstrated failures; rerun only failed/affected/missing gates. Evidence reuse requires verifier-confirmed unchanged/compatible inputs, original run/attempt/artifact/digest and no newer relevant negative result.
- Targeted/selected runs cannot approve a release. The final complete approval must cover every required unique gate and current ecosystem inputs, with valid release-approved.json and coverage provenance from the canonical verifier.
- Deliver exact approval origin, candidate/consumer SHAs, complete coverage, accepted exceptions if any and remaining failures. Do not claim release-ready with required coverage missing. No promotion or tagging under this card.

## Required checks

Existing final approval and resume/check-approval verifiers; actual required Docker/rootless Podman/consumer evidence. Not-required is justified, never synthetic PASS; no repeat whole matrix merely because one gate failed.

## Dependencies and file ownership

- Procedure and sources: [release workflow](https://github.com/mcpdev80/baseharbor-plan/blob/main/RELEASE_WORKFLOW.md#qualify). Stage dependencies are synchronized by `scripts/release_cycles.py sync`; do not weaken them manually.
- Owner updates this task, its release-specific audit/evidence and existing authorized PRs; coordinate product files through their normal owners. Planning goes directly to main.

## Handoff

Not started. Record actual source SHAs, outcomes, authorization where required, evidence and remaining blockers; do not infer acceptance from card creation.
