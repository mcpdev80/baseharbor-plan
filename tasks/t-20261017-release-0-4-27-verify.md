---
id: t-20261017-release-0-4-27-verify
card_number: "0427-010"
card_short_title: "verify publication, artifacts,"
type: acceptance
areas: [release]
release: v0.4.27
version: v0.4.27
release_stage: verify
parent: v0.4.27
owner: mission-closeout27
kanban_lane: wait
kanban_summary: Prove the published release is usable and close the release cycle.
kanban_status: wait
kanban_title: "0427-010 · verify publication, artifacts,"
priority: normal
depends_on: [t-20261017-release-0-4-27-publish]
repos: [mcpdev80/baseharbor, mcpdev80/baseharbor-demo]
prs: []
sources: []
blocker: ""
wait_reason: "Release artifacts, Pages and authenticated GHCR channels are verified. `ghcr.io/mcpdev80/baseharbor-runtime` tags `0.4.27`, `0.4`, `latest`, and `sha-6c40fab` share index sha256:5ea2febbab28933588bb87e7b6a0c4edb5a61375c828de0b695952eb7a9c480b; amd64 `baha version --json` reports version 0.4.27 and exact tag commit 6c40fab4. The OCI-index attestation verifies under the runtime-image workflow signer, but its signed SLSA source digest/ref are workflow-dispatch main@c000c5db / refs/heads/main, not the tag commit 6c40fab4. Resolve the signed source binding before accepting."
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/43991839986", "https://github.com/mcpdev80/baseharbor/releases/tag/v0.4.27", "https://github.com/mcpdev80/baseharbor/actions/runs/43991826173", "https://github.com/mcpdev80/baseharbor/tree/v0.4.27", "https://github.com/mcpdev80/baseharbor/actions/workflows/runtime-image.yml", "https://github.com/mcpdev80/baseharbor/pkgs/container/baseharbor-runtime"]
---

- [ ] t-20261017-release-0-4-27-verify · v0.4.27 · Release: verify publication, artifacts, Pages and closeout #task #release/v0-4-27 #status/wait #view/wait #area/release #kind/acceptance
    <!-- generated:card -->
    **Owner:** mission-closeout27 · **Priority:** normal  
    **Waiting:** Release artifacts, Pages and authenticated GHCR channels are verified. \`ghcr.io/mcpdev80/baseharbor-runtime\` tags \`0.4.27\`, \`0.4\`, \`latest\`, and \`sha-6c40fab\` share index sha256:5ea2febbab28933588bb87e7b6a0c4edb5a61375c828de0b695952eb7a9c4…  
    **Needs:** [t-20261017-release-0-4-27-publish](t-20261017-release-0-4-27-publish.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/43991839986), [proof 2](https://github.com/mcpdev80/baseharbor/releases/tag/v0.4.27), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/43991826173), [proof 4](https://github.com/mcpdev80/baseharbor/tree/v0.4.27), [proof 5](https://github.com/mcpdev80/baseharbor/actions/workflows/runtime-image.yml), [proof 6](https://github.com/mcpdev80/baseharbor/pkgs/container/baseharbor-runtime)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.27](../releases/v0.4.27.md) (v0.4.27)  
**Depends on:** [t-20261017-release-0-4-27-publish](t-20261017-release-0-4-27-publish.md)  
**Required by:** [t-20261017-release-0-4-28-cleanup](t-20261017-release-0-4-28-cleanup.md)  
**Owner:** mission-closeout27  
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
- Close superseded PRs, remove incorporated temporary branches and preserve historical records and required build artifacts. Record actual verification results and explicit remaining blockers.

## Required checks

Canonical audit sections 10–13 and existing release-only/artifact/checksum/provenance/Pages checks. Reuse approved source/runtime evidence; no redundant full matrix.

## Dependencies and file ownership

- Procedure and sources: [release workflow](https://github.com/mcpdev80/baseharbor-plan/blob/main/RELEASE_WORKFLOW.md#verify). Stage dependencies are synchronized by `scripts/release_cycles.py sync`; do not weaken them manually.
- Owner updates this task, its release-specific audit/evidence and existing authorized PRs; coordinate product files through their normal owners. Planning goes directly to main.

## Handoff

- 2026-11-14 (mission-closeout27, review-pending act): no v0.4.27 tag or GitHub Release exists (latest: v0.4.26), so publication verification is impossible and honestly unclaimed; CHANGELOG 0.4.27 section and docs/releases/v0.4.27.md already exist on develop/release branch as future witnesses. Full dossier with remote-truth witnesses: [round-1](../evidence/r27-closeout-2026-11-14/round-1.md). Review state deferred: schema requires a card PR (plan.py:417); no admissible product PR exists for this acceptance card.

## Release-state reconciliation — 2026-11-21

- The tag and GitHub Release are live, contrary to the original handoff: `v0.4.27` tag commit `6c40fab4de9a611bc8da2e834417427a83c01ca5`; release run [43991839986](https://github.com/mcpdev80/baseharbor/actions/runs/43991839986) and Pages run [43991826173](https://github.com/mcpdev80/baseharbor/actions/runs/43991826173) succeeded. Downloaded amd64/arm64 archives both passed `sha256sum -c checksums.txt`; the amd64 binary reports `version=0.4.27` and `commit=6c40fab4de9a611bc8da2e834417427a83c01ca5`.
- `gh attestation verify` successfully verifies the amd64 archive under the release workflow identity, but its SLSA statement source digest/ref are `c000c5db2560c471fe84842136e03d6e54d96779` / `refs/heads/main` (workflow dispatch), not the source commit embedded in the released binary. I will not describe this as a tag-bound provenance proof.
- Superseded initial package check: the anonymous lookup used the incorrect `ghcr.io/mcpdev80/baseharbor` name and cannot establish the status of the actual `baseharbor-runtime` package. See the authenticated, correct-name verification below.


## Correct runtime-image verification — 2026-11-21

- Audited `.github/workflows/release.yml` and `.github/workflows/runtime-image.yml` at workflow SHA `c000c5db2560c471fe84842136e03d6e54d96779`. The actual package is `ghcr.io/mcpdev80/baseharbor-runtime`; the release calls the reusable workflow with its resolved tag and version tag. The runtime-image workflow emits version, minor, latest and commit-short tags.
- Authenticated GHCR inspection found `0.4.27`, `0.4`, `latest`, and `sha-6c40fab` all at index digest `sha256:5ea2febbab28933588bb87e7b6a0c4edb5a61375c828de0b695952eb7a9c480b`. The index includes Linux amd64 manifest `sha256:a0d2fd23b365268d3848ba305376c9ded9c7ab11ca19a2e1c99feb1ce21c7021` and arm64 manifest `sha256:dd9e1c06cc1b271ecfc0335dd6a0e7df1ce531db6d6d11bf836e07c98c1d896d`.
- Pulled and ran the amd64 image by digest; `baha version --json` reports `version=0.4.27`, `commit=6c40fab4de9a611bc8da2e834417427a83c01ca5`. The temporary Docker auth config was logged out and removed; the one-shot container used `--rm`.
- `gh attestation verify` succeeds for the OCI index under signer `mcpdev80/baseharbor/.github/workflows/runtime-image.yml`; signed subject digest matches the published index. The signed SLSA statement still binds source to main `c000c5db...` / `refs/heads/main` and workflow_dispatch, not to tag commit `6c40fab4...`. The release workflow's code resolves and passes the tag to the reusable build, and the image metadata matches, but the signed provenance does not directly encode that selected source. Keep verification open until that source binding is adequately evidenced.
