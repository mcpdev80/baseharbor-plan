---
id: core-896
areas: [ci]
type: task
release: v0.4.26
version: ""
parent: core-888
owner: mcpdev80 (session 1)
depends_on: [core-893-interface]
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#932"]
sources: ["mcpdev80/baseharbor#896"]
source_updated: "2026-10-15T20:35:26Z"
labels: [area/evidence]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-896 · Runners: isolate parallel PR checks safely #task #release/v0-4-26 #status/review #view/review #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (session 1) · **Priority:** not set  
    **PR:** [baseharbor#932](https://github.com/mcpdev80/baseharbor/pull/932)  
    **Needs:** [core-893-interface](core-893-interface-agree-planning-execution-interface.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Parent:** [core-888](../epics/core-888-development-and-ci.md)  
**Depends on:** [core-893-interface](core-893-interface-agree-planning-execution-interface.md)  
**Required by:** [core-390](core-390-architecture-service-contracts-provider-catalog.md), [core-750](core-750-inspect-source-neutral-findings.md), [core-751](core-751-inspect-no-false-positives-comments-text.md), [core-752](core-752-inspect-reconcile-default-instances.md), [core-754](core-754-mcp-classify-expected-preconditions.md), [core-766](core-766-cleanup-orphaned-owned-runtime-resources.md), [core-815](core-815-tests-greenfield-stacks-native-runtimes.md), [core-893](core-893-ci-enforce-selected-pr-checks.md), [core-901](core-901-pilot-verify-parallel-task-prs-ci-costs.md), [core-910](core-910-wizard-shared-read-only-editing-state.md)  
**Owner:** mcpdev80 (session 1)  
**Priority:** not set  
**PRs:** [baseharbor#932](https://github.com/mcpdev80/baseharbor/pull/932)  
**Source:** [baseharbor#896](https://github.com/mcpdev80/baseharbor/issues/896)
<!-- /generated:links -->

## Goal

Independent PR lanes share neither mutable runtime state nor permissions.

## Scope

- In scope: dedicated runner-isolation helpers and tests: per-run Target/volume/port/state isolation, trust boundaries, cleanup and capacity.
- Out of scope: #893 orchestration files, privileged untrusted execution, merges, releases, other sessions' files. Do not copy #930 wholesale.

## Acceptance

- Docker/Podman run in parallel within actual slots; no foreign PR or candidate is cancelled.
- Own Targets/volumes/ports and reliable cleanup; no shared provider/secret/recovery state.
- Forks get neither secrets nor privileged self-hosted runners; the necessary trusted acceptance stays visibly open.
- Caches only for matching immutable build inputs; cache is never evidence.

## Required checks

- Configuration and security/isolation fixtures; the two necessary small isolated pilot lanes including cleanup instead of an extra full matrix.

## Dependencies and file ownership

- Depends on #892 (closed) and the agreed interface (core-893-interface). **Full #893 completion or merge is not a start prerequisite.** Order fixed by the [2026-10-15 dependency correction](../epics/core-888-development-and-ci.md#binding-dependency-correction--2026-10-15).
- Separate small PR against develop; integrate, then core-893 consumes it.

## Handoff

- Live migration review: PR #932 head `174dc6d56b40dea85f2708b95e71b3a7b3638c4c`; draft/preparatory work remains unaccepted. The current PR head supersedes older SHA assertions in its body. Preserve the existing owner, branch and PR.

- 2026-10-15T20:35Z (issue comment): implementation reviewable in PR #932, head `fa1be26dc4373a288bb130d6ecdf92f2c1a8571f`, marked ready (not draft), not merged. Docker and Podman isolation pilots with success, injected failure and SIGTERM cleanup passed in runs 38800255264 and 38801650732; concurrent capacity, authenticated run/PR/repo identity, peer preservation and cleanup security fixtures passed; workflow-policy/fixture run 38802577817 PASS; costly pilots made manual-only after the evidence. Trusted code only in disposable hosted contexts. PR #932 is one commit behind develop (`bf69ad0a…`, unrelated #900 GC commit). Awaiting Maintainer review; acceptance not yet granted.
- 2026-10-15: session 1 owns #896 "for the explicitly authorized sequential assignment", confined to runner isolation helpers and focused fixtures, consuming #930 interface commit `ca2653cbf5d86216d87d4cdddb4e21eb5d6d2e06`. Draft PR #932 ("establish isolated PR lane leases"), head `d5f355a66a` at snapshot time.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
