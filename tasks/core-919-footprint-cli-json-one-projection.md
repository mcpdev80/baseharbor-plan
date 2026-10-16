---
id: core-919
areas: [cli]
type: task
release: v0.4.26
version: ""
parent: v0.4.26
owner: "mcpdev80 (core-919)"
depends_on: [core-910, core-914]
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#965"]
sources: ["mcpdev80/baseharbor#919"]
source_updated: "2026-10-15T16:46:11Z"
labels: [area/dx, area/compatibility]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-919 · Footprint: serve CLI and JSON from one projection #task #release/v0-4-26 #status/review #view/review #area/cli #kind/task
    <!-- generated:card -->
    **Owner:** mcpdev80 (core-919) · **Priority:** not set  
    **PR:** [baseharbor#965](https://github.com/mcpdev80/baseharbor/pull/965)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-910](core-910-wizard-shared-read-only-editing-state.md), [core-914](core-914-preview-actual-footprint.md)  
**Required by:** [core-920](core-920-machine-adapters-capability-changes-footprint.md), [core-921](core-921-cli-mcp-register-new-interfaces.md)  
**Owner:** mcpdev80 (core-919)  
**Priority:** not set  
**PRs:** [baseharbor#965](https://github.com/mcpdev80/baseharbor/pull/965)  
**Source:** [baseharbor#919](https://github.com/mcpdev80/baseharbor/issues/919)
<!-- /generated:links -->

## Goal

`baha app footprint show` delivers the existing authoritative projection for humans and as JSON. Lane: CLI/JSON read-only.

## Scope

- In scope: dedicated footprint command/output files and tests.
- Out of scope: central command/MCP registry, footprint schema, registry golden changes.

## Acceptance

- Uses the existing footprint version/resolver and current Target/consumer/provider facts; no second footprint or state calculator.
- Reports real completeness, measured/estimated/unknown and denied/unverifiable/source_missing truthfully.
- Read-only even with missing/partial installations; safe errors/exit codes; no credential or internal path leaks.

## Required checks

- Golden/contract tests for the same facts in human/JSON output, empty/partial/wrong Target; no containers.

## Dependencies and file ownership

- Depends on core-910 and core-914. Shared v0.4.26 PR/review/runner foundation (#890–#893, #895, #896) must be qualified first.

## Autonomous execution contract — 2026-10-16

- **Owned files:** `cmd/baha/app_footprint_show.go` and `cmd/baha/app_footprint_show_test.go` only; dedicated testdata beneath `cmd/baha/testdata/app_footprint_show/` if needed.
- **Delivered interface/result:** Deliver callable human/JSON handlers consuming accepted footprint presentation and the existing authoritative footprint schema; the controller does not become a new calculation owner.
- **Task-specific proof:** `TestAppFootprintShow*`: same authoritative facts in human/JSON, empty/incomplete/wrong Target, denial and secret-free error/exit behavior.
- **Boundary:** No footprint-domain/schema changes, presenter edits, machine registry/goldens or command routing. Registration is delivered by core-921.
- **Assignment gate:** use only accepted dependencies and APIs already present on develop. Confirm that the trusted plan/executor runs these exact test families on this task's file set and checks their outcomes. A plan that reports unresolved is not execution-ready. The CI-readiness inventory is maintained by [t-20261016-wizard-task-ci-readiness](t-20261016-wizard-task-ci-readiness.md); later gaps become an explicit prerequisite before assignment, never an instruction to wait for another running session.
- **End-to-end owner:** the assigned session handles integration, implementation, focused tests, hosted CI observation, demonstrated fixes and its planning handoff. It reads other task states itself from planning main and preserves concurrent updates. No shared CI edits, dependency work-in-progress or manual message relay through Marcel. Normal independent review/Maintainer acceptance remains a boundary, not an implementation dependency.

## Handoff

- 2026-10-16 correction for [review #5547455083](https://github.com/mcpdev80/baseharbor/pull/965#pullrequestreview-5547455083): exact product head `a54388938074ad3c98554108d96494acdde92baf`, existing [PR #965](https://github.com/mcpdev80/baseharbor/pull/965). `appFootprintShowContext` human branch now calls the accepted `renderAppFootprint(view.Footprint, view.Footprint.Complete, ...)`; JSON still serializes the unchanged canonical `view.Footprint`. Wider `GuidedReadContext.Complete` is intentionally not substituted for footprint completeness. `TestAppFootprintShowFootprintCompletenessIndependentOfPlan` exercises Footprint.Complete=true with context Complete=false, asserts human complete and byte-for-byte canonical JSON equality, canonical typed evidence, and unchanged input. Only the two owned show files changed. Targeted [run 38897612963](https://github.com/mcpdev80/baseharbor/actions/runs/38897612963) selected Trusted Plan, Workflow policy, Focused Python, gofmt, contracts, vet/build and `wizard-footprint-command-tests`; all selected checks including `wizard-footprint-command-tests` and final `PR Selected Checks` **SUCCESS** (attempt 1); runtime and release paths skipped. Independent re-review required; no self-merge or acceptance.

- 2026-10-16 independent Maintainer review at source `45be574dc1c02803cfd2eefbfe27a9b795bd9297`: **changes required; not accepted or merged**. Hosted run `38896287707` and its exact integration `36508ab669b56f2ac24775a811648d1a4546819e` are confirmed green, including all six command tests. Inspection found a missing Human/JSON parity case: `Footprint.Complete=true` with `GuidedReadContext.Complete=false` makes the human presenter report incomplete while canonical JSON reports complete. This is a possible authority result because the read context also includes lifecycle-plan completeness. Keep the canonical footprint and its schema unchanged; make both command formats report the same footprint completeness, separating wider plan completeness if shown. Add a mismatched-flags regression with exact canonical JSON and input non-mutation assertions, then qualify the corrected two-file candidate using regular targeted CI. Current planning main `d5e4703` was independently verified: render unchanged, check 0 errors/0 warnings, all 38 planning unit tests pass; concurrent core-913 handoff preserved.

- 2026-10-16 core-919 completed implementation/review handoff. Product [PR #965](https://github.com/mcpdev80/baseharbor/pull/965), branch `task/core-919-footprint-show`, exact source HEAD `45be574dc1c02803cfd2eefbfe27a9b795bd9297`, trusted develop target `1d6f1a7982f69622fb1faee6f4b99040c6b6d945`, exact GitHub PR integration `36508ab669b56f2ac24775a811648d1a4546819e`. A normal two-parent develop merge `cf0ec3743770030f3707033556dafc3d9e3bdba0` preserved independently merged core-912; no force push. **Only** `cmd/baha/app_footprint_show.go` and `cmd/baha/app_footprint_show_test.go` were implemented. Callables `appFootprintShow`/`appFootprintShowContext` consume one `GuidedReadContext.Footprint`; human output calls the accepted `presentAppFootprint`, JSON serializes the canonical `application.Footprint` directly, with strict Target/footprint-version boundary, secret-free failures (including writer failures), no additional resolver or registration. `TestAppFootprintShow*` covers same authoritative provider/core/resource evidence across human/JSON, empty/partial, wrong target without output, denied/source_missing and safe error paths, and read-only non-mutation. Verified normal selected GitHub-hosted PR CI [run 38896287707](https://github.com/mcpdev80/baseharbor/actions/runs/38896287707): **SUCCESS** for Trusted Plan, Workflow policy, Focused Python, `wizard-footprint-command-tests`, `source-contracts`, `cli-gofmt`, `cli-vet`, `cli-build`, and authenticated final `PR Selected Checks`; selected runtime, HA, release, public-contracts, Demo and broad legacy validate were correctly skipped. Prior red format attempts and stale target integration are not acceptance evidence. No containers or runtime/release matrix. **Independent review pending: do not merge, accept or begin core-920/921.**


The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
