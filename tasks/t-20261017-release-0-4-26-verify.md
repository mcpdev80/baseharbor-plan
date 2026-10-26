---
id: t-20261017-release-0-4-26-verify
type: acceptance
areas: [release]
release: v0.4.26
version: v0.4.26
release_stage: verify
parent: v0.4.26
owner: "Codex (Owner-authorized publication verification)"
priority: normal
depends_on: [t-20261017-release-0-4-26-publish]
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo, mcpdev80/baseharbor-console, mcpdev80/baseharbor-node-connector]
prs: [mcpdev80/baseharbor#1089]
sources: []
blocker: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/releases/tag/v0.4.26", "https://github.com/mcpdev80/baseharbor/actions/runs/40355992335", "https://github.com/mcpdev80/baseharbor/pull/1089"]
---

- [ ] t-20261017-release-0-4-26-verify · v0.4.26 · Release: verify publication, artifacts, Pages and closeout #task #release/v0-4-26 #status/review #view/review #area/release #kind/acceptance
    <!-- generated:card -->
    **Owner:** Codex (Owner-authorized publication verification) · **Priority:** normal  
    **PR:** [baseharbor#1089](https://github.com/mcpdev80/baseharbor/pull/1089)  
    **Needs:** [t-20261017-release-0-4-26-publish](t-20261017-release-0-4-26-publish.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/releases/tag/v0.4.26), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/40355992335), [proof 3](https://github.com/mcpdev80/baseharbor/pull/1089)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.26](../releases/v0.4.26.md) (v0.4.26)  
**Depends on:** [t-20261017-release-0-4-26-publish](t-20261017-release-0-4-26-publish.md)  
**Required by:** [t-20261017-release-0-4-27-cleanup](t-20261017-release-0-4-27-cleanup.md)  
**Owner:** Codex (Owner-authorized publication verification)  
**Priority:** normal  
**PRs:** [baseharbor#1089](https://github.com/mcpdev80/baseharbor/pull/1089)  
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

### Owner-directed release verification — 2026-10-26

- Marcel expressly authorized release of implemented v0.4.26 regardless of incomplete/failing CI. Publication verification below does not certify a successful complete pre-release or reopen native test matrices.
- Public stable Release: https://github.com/mcpdev80/baseharbor/releases/tag/v0.4.26. Published at `2026-10-26T16:17:03Z`; not draft or prerelease.
- Annotated tag `d09e1b024d1b161836b477ec37a95d017402fddc` targets `640981588d8b9255fbe7db8ca26796db1da09eb2`. Exact tree `d7c63770a31b082ab7fc1c9fd254e4918efafc59` equals selected develop `433a5702c9735ffbf1e9fffe7a7ae513b1c5c396`.
- Actual successful publisher run `40355992335`/attempt 1 contains successful authorization, runtime and archives jobs. Both archive checksum checks report OK. GitHub archive provenance attestation: https://github.com/mcpdev80/baseharbor/attestations/59997514; checksum attestation: https://github.com/mcpdev80/baseharbor/attestations/59997592.
- Linux AMD64 archive: 13,670,930 bytes, SHA-256 `31dcef96b86d96c2bbdfc7bb0ac1092063d22b1f7bc250fc9d849eaef8b95fa7`. Linux ARM64 archive: 12,504,459 bytes, SHA-256 `81bd22c412a4f7bff92b6eb3390954cc6ac454117c4adaa059f02f5ab8c79e97`.
- Checksum manifest: 192 bytes, SHA-256 `6946abbd4c46f33c5116f4b97e3989cf0af9736384c48b0fe44bfeae52a1ebf8`. The public `owner-release-decision.json` attachment records the exception without claiming pre-release success.
- Runtime AMD64/ARM64 image and provenance publication succeeded; version/compatible/latest channels use manifest digest `sha256:b2167acb13b9966ef7e3814869de628d9726bd63be83108234dadf0efce5148f`. Build arguments bind COMMIT to promoted main. The existing reusable workflow OCI revision label follows the isolated publisher context (`a71b0b4a`), rather than the explicitly checked-out build source; retain that distinction when interpreting provenance.
- Post-promotion Pages run `40355591107` succeeded on promoted main. No additional platform support, consumer qualification or native usability proof is inferred from this publication.
- Publication and its observable artifacts verified under delegated Owner mandate; normal gated-stage acceptance, source/native qualification and unresolved defects remain independently open. Preserve the release tag and final publication/exception evidence. CI redesign/recovery remains v0.4.27 work; its completion is not implied.
