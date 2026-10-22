---
id: t-20261022-r27-evidence-acceptance
type: task
areas: [ci]
release: v0.4.27
version: ""
parent: v0.4.27
priority: critical
owner: ""
depends_on: [t-20261017-release-0-4-27-updates, t-20261022-r27-evidence-verifier]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
resolution: ""
evidence: []
---

- [ ] t-20261022-r27-evidence-acceptance · evidence acceptance #task #release/v0-4-27 #status/planned #view/waiting #board/planned #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** critical  
    **Waiting for prerequisites**  
    **Needs:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-evidence-verifier](t-20261022-r27-evidence-verifier.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md), [t-20261022-r27-evidence-verifier](t-20261022-r27-evidence-verifier.md)  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md), [t-20261022-r27-ci-access](t-20261022-r27-ci-access.md), [t-20261022-r27-ci-authority](t-20261022-r27-ci-authority.md), [t-20261022-r27-ci-delivery](t-20261022-r27-ci-delivery.md), [t-20261022-r27-ci-runtime](t-20261022-r27-ci-runtime.md)  
**Owner:** unassigned  
**Priority:** critical  
**PRs:** none  
**Source:** 
<!-- /generated:links -->


# Evidence acceptance: parallel contributors and recovery

## Goal
Independently demonstrate durable, trusted CI proof with Codeman workers, maintainer sessions and external contributors sharing the same claim/review protocol.

## Acceptance
- Two independent authors publish nonconflicting evidence while unrelated planning updates land; neither overwrites the other.
- Delete or expire source CI artifacts and delete a feature branch in a controlled fixture; archived proof remains resolvable and validates for the original exact candidate.
- Changed candidate, missing check, bad signature/hash and unauthorized publication fail closed.
- Document practical recovery/backup and repository-size limits, release handoff and smallest CI gates.
- Independent reviewer accepts evidence; do not automatically merge, promote or publish a release.

## Human parity acceptance
- Demonstrate an ordinary external contributor PR with no custom evidence commands: CI creates, archives, verifies and links the proof automatically.
- Demonstrate an ordinary maintainer PR and Codeman worker PR following the identical process, including concurrent planning writes.
- No manual JSON manifest, artifact download, evidence URL copy/paste or special role-specific tooling required.
