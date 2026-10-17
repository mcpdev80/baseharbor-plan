---
id: {{id}}
type: acceptance
areas: [release]
release: {{release}}
version: {{version}}
release_stage: verify
parent: {{release}}
owner: ""
priority: normal
depends_on: []
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo, mcpdev80/baseharbor-console, mcpdev80/baseharbor-node-connector]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] {{id}} · {{version}} · {{title}} #task #{{release_tag}} #status/planned

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
