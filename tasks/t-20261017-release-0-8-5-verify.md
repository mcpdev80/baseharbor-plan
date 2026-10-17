---
id: t-20261017-release-0-8-5-verify
type: acceptance
areas: [release]
release: v0.8.x
version: v0.8.5
release_stage: verify
parent: v0.8.x
owner: ""
priority: normal
depends_on: [t-20261017-release-0-8-5-publish]
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo, mcpdev80/baseharbor-console, mcpdev80/baseharbor-node-connector]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261017-release-0-8-5-verify · v0.8.5 · Release: verify publication, artifacts, Pages and closeout #task #release/v0-8-x #status/planned #view/waiting #board/planned #area/release #kind/acceptance
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** normal  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-8-5-publish](t-20261017-release-0-8-5-publish.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.8.x](../releases/v0.8.x.md) (v0.8.5)  
**Depends on:** [t-20261017-release-0-8-5-publish](t-20261017-release-0-8-5-publish.md)  
**Owner:** unassigned  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Prove the published release is usable and close the release cycle.

## Scope and acceptance

- Require authorized tag/publish completion, not merely a prepared command. Confirm tag immutability, main ancestry and exact release SHA; GitHub Release, archives, checksums and baha version metadata agree.
- Verify required architecture/OS artifacts, build/runtime provenance/attestations and matching GHCR version/compatible/latest channels against the current release contract; unsupported future platform artifacts are not invented.
- Verify the actual post-promotion Pages workflow and published EN/DE release notes, navigation, roadmap and changed references. A candidate build is not published-site verification. Review release-mode Demo/consumer dispatch when required.
- Reconcile audit/evidence and task acceptance, release status/evidence, roadmap/current-version messaging and next-release handoff. Tag push alone is never release completion.
- Close superseded PRs, remove incorporated temporary branches and apply evidence retention without destroying required receipts. Record actual verification results and explicit remaining blockers.

## Required checks

Canonical audit sections 10–13 and existing release-only/artifact/checksum/provenance/Pages checks. Reuse approved source/runtime evidence; no redundant full matrix.

## Dependencies and file ownership

- Procedure and sources: [release workflow](https://github.com/mcpdev80/baseharbor-plan/blob/main/RELEASE_WORKFLOW.md#verify). Stage dependencies are synchronized by `scripts/release_cycles.py sync`; do not weaken them manually.
- Owner updates this task, its release-specific audit/evidence and existing authorized PRs; coordinate product files through their normal owners. Planning goes directly to main.

## Handoff

Not started. Record actual source SHAs, outcomes, authorization where required, evidence and remaining blockers; do not infer acceptance from card creation.
