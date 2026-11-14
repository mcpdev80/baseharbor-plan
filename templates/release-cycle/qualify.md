---
id: {{id}}
type: acceptance
areas: [release]
release: {{release}}
version: {{version}}
release_stage: qualify
parent: {{release}}
owner: ""
priority: normal
depends_on: []
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] {{id}} · {{version}} · {{title}} #task #{{release_tag}} #status/planned

## Goal

Obtain complete release-boundary validation for the frozen candidate.

## Scope and acceptance

- Require accepted preparation, acceptance of every scoped implementation/CI/docs/consumer task (including later-added scope), and explicit Maintainer authorization for the complete pre-release. Record that authorization and exact candidate/ecosystem matrix before dispatch.
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

Not started. Record actual source SHAs, outcomes, authorization where required, evidence and remaining blockers; do not infer acceptance from card creation.
