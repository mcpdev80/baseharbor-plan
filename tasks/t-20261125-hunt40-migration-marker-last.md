---
id: t-20261125-hunt40-migration-marker-last
card_number: "0428-310"
card_short_title: "migration marker retry"
type: task
areas: []
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "Make the one-time migration from a world-writable legacy organization-selection file fail closed across failures and retries,…"
kanban_title: 0428-310 · migration marker retry
priority: ""
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261125-hunt40-migration-marker-last · 0428 hunt H-V40: migration marker failure can permit legacy re-adoption #task #release/v0-4-28 #status/planned #view/ready #kind/task
    <!-- generated:card -->
    **Owner:** unassigned  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** not set  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Make the one-time migration from a world-writable legacy organization-selection file fail closed across failures and retries, without writing the migration marker before the canonical selection is safely stored.

## Scope

- In scope: `internal/orgconfig/store.go` and focused tests in the `internal/orgconfig` Go package.
- Keep the safe ordering: atomically write the canonical selection first, then record the durable once-only marker. Do not implement the old marker-first suggestion; that can strand a marker without the migrated selection.
- Out of scope: general organization-config redesign, filesystem-wide migration framework, and unrelated target/identity changes.

## Acceptance

- Preserve canonical-file-before-marker ordering so a crash cannot leave a marker that falsely claims the selection was adopted when no canonical selection exists.
- Handle marker-creation failure after the canonical rename so a later load/save cannot silently re-adopt the stale legacy selection if the canonical file is subsequently absent.
- Add a deterministic package regression for the marker-write failure/retry window, using an injectable filesystem seam or equivalent controlled fault; assert fail-closed behavior and preserve the successfully migrated selection.
- Keep the existing successful migration guarantees: the canonical value loads, the durable marker is written, and later deletion of canonical state does not revive the legacy value.
- Bind the regression to normal Go package test discovery for `internal/orgconfig`; do not create a per-test catalog row or a new CI gate.
- Record the exact candidate SHA, test command, selected existing check and actual run result in the implementation handoff.

## Dependencies and file ownership

- Owned files: `internal/orgconfig/store.go` and the package's migration tests.
- No dependency on the real-version Core provider migration qualification card; these are separate migrations with separate runtime and risk boundaries.

## Audit disposition — REWRITE

Rechecked BaseHarbor `develop` at `3a2ae6b1139570c98b8924e3b19975c56a289400`. The finding's proposed marker-first fix is unsafe and is rejected: the code deliberately writes the canonical file before the marker. The actual narrow gap is that a marker-write error is returned after canonical state has landed, while the loader only checks the marker when canonical state is absent; a later loss of that canonical file can therefore permit legacy re-adoption. The existing tests cover successful marker creation and later state deletion, but not controlled marker-write failure and retry. This card stays open with that corrected scope; no product fix is claimed here.

Evidence: [current migration implementation](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/orgconfig/store.go), [current orgconfig migration tests](https://github.com/mcpdev80/baseharbor/blob/3a2ae6b1139570c98b8924e3b19975c56a289400/internal/orgconfig/orgconfig_test.go), [H-V40 source dossier](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/w173/hunt-v40-upgrade-migration.md).
