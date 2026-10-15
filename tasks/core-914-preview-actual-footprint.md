---
id: core-914
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: ""
depends_on: [core-910]
repos: [mcpdev80/baseharbor]
prs: []
sources: ["mcpdev80/baseharbor#914"]
source_updated: "2026-10-15T16:46:40Z"
labels: [area/dx]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-914 · Preview: present the actual footprint concisely #task #release/v0-4-26 #status/planned

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-910](core-910-wizard-shared-read-only-editing-state.md)  
**Required by:** [core-916](core-916-wizard-back-cancel-eof-no-side-effects.md), [core-919](core-919-footprint-cli-json-one-projection.md)  
**Owner:** unassigned  
**PRs:** none  
**Source:** [baseharbor#914](https://github.com/mcpdev80/baseharbor/issues/914)
<!-- /generated:links -->

## Goal

The New/Edit preview explains required services and incremental resource needs in a few lines. Lane: read-only presentation.

## Scope

- In scope: separate footprint presenter files and tests in the existing presentation area.
- Out of scope: resolver changes; `internal/application/footprint.go` is consumed only.

## Acceptance

- Shows new/reused/stopped/unverified realizations correctly; running/additional containers are not guessed from capability names.
- RAM/container values distinguish measured, estimated and unknown; no invented zeros or seemingly exact sums.
- Explains zero-core and genuine dependencies, details optional; output is secret-free.

## Required checks

- Fixtures for empty, reuse/new, unknown capacity, real transitive dependencies and incomplete facts; no runtime.

## Dependencies and file ownership

- Depends on core-910. Shared v0.4.26 PR/review/runner foundation (#890–#893, #895, #896) must be qualified first.

## Handoff

- Not started.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
