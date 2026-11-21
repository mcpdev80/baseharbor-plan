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
wait_reason: "The v0.4.27 release exists. SHA-256 checks for both published archives pass and the amd64 binary reports exact tag commit 6c40fab4; Pages run 43991826173 succeeded. Provenance remains unresolved: the cryptographically verified asset attestation binds workflow source to main c000c5db (workflow_dispatch), while the artifact binary is built from tag commit 6c40fab4. Authenticated GHCR read was attempted using the existing gh CLI session in a temporary /tmp Docker config; both `v0.4.27` and `latest` returned `manifest unknown`, and the authenticated organization package API returned 404. The temporary credential file was logged out and removed. Exact image channels are therefore absent/unverified, and tag-bound source-to-artifact provenance is still missing; do not accept."
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/43991839986", "https://github.com/mcpdev80/baseharbor/releases/tag/v0.4.27", "https://github.com/mcpdev80/baseharbor/actions/runs/43991826173", "https://github.com/mcpdev80/baseharbor/tree/v0.4.27"]
---

- [ ] t-20261017-release-0-4-27-verify · v0.4.27 · Release: verify publication, artifacts, Pages and closeout #task #release/v0-4-27 #status/wait #view/wait #area/release #kind/acceptance
    <!-- generated:card -->
    **Owner:** mission-closeout27 · **Priority:** normal  
    **Waiting:** The v0.4.27 release exists. SHA-256 checks for both published archives pass and the amd64 binary reports exact tag commit 6c40fab4; Pages run 43991826173 succeeded. Provenance remains unresolved: the cryptographically verified asset attest…  
    **Needs:** [t-20261017-release-0-4-27-publish](t-20261017-release-0-4-27-publish.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/43991839986), [proof 2](https://github.com/mcpdev80/baseharbor/releases/tag/v0.4.27), [proof 3](https://github.com/mcpdev80/baseharbor/actions/runs/43991826173), [proof 4](https://github.com/mcpdev80/baseharbor/tree/v0.4.27)  
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
- Anonymous GHCR manifest checks for `v0.4.27` and `latest` returned `denied`; the package versions API returned 404. Exact image channel/digest verification is still missing. No claim of complete release verification is made.


## Authenticated registry recheck — 2026-11-21

- Logged in to GHCR with the current GitHub CLI session using a temporary Docker config under `/tmp`; no credential was printed or retained. Both `docker manifest inspect ghcr.io/mcpdev80/baseharbor:v0.4.27` and `:latest` returned `manifest unknown`. The authenticated organization package versions endpoint also returned 404. Removed the temporary Docker config after logout. The registry channel gap is confirmed, not just an anonymous-read limitation.
