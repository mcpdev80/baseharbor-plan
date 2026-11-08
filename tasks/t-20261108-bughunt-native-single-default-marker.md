---
id: t-20261108-bughunt-native-single-default-marker
card_number: "0427-156"
card_short_title: "Native marker missing"
type: bug
areas: [lifecycle, compose]
release: v0.4.27
version: ""
parent: v0.4.27
owner: lane-w156-diag
kanban_status: active
kanban_lane: active
kanban_summary: "Root cause identified with file:line and either (a) the marker is produced again on the productive path (product fix +…"
kanban_title: 0427-156 · Native marker missing
priority: normal
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/actions/runs/42485190712","https://github.com/mcpdev80/baseharbor/actions/runs/42485190770"]
superseded_by: t-20261108-bughunt-0427-test-bootstrap-leak
---
- [ ] t-20261108-bughunt-native-single-default-marker · Develop red 0.4.27: native single-default marker #task #release/v0-4-27 #status/active #view/active #area/compose #area/lifecycle #kind/bug
    <!-- generated:card -->
    **Owner:** lane-w156-diag · **Priority:** normal  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/actions/runs/42485190712), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/42485190770)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md)  
**Owner:** lane-w156-diag  
**Priority:** normal  
**PRs:** none  
**Source:** 
<!-- /generated:links -->
<!-- generated:card -->

<!-- /generated:card -->
## Outcome and acceptance
Root cause identified with file:line and either (a) the marker is produced again on the productive path (product fix + regression in the native single-default group) or (b) the assertion is corrected to the new intended bootstrap semantics (test fix + rationale), then a push-triggered Docker+Podman native single-default pair is terminal green on the exact develop head; no permanent skips, no rerun spam.

## Problem (observed on hosted runs, 2026-11-08)
Post-merge develop native cells (Docker run 42485190712, Podman run 42485190770) fail in TestControlPlaneSingleDefaultNativeRuntimeInCI: the bootstrap leftover marker is missing, so the single-default SQL/Secrets verification step fails on the current develop head 8ecd1ea5d. First develop-red after the #1464 stabilization; cause not yet attributed (test construction vs. remote-up pivot 223042bc0 vs. #1474-only-test change which is unrelated by content).

## Acceptance
Root cause identified with file:line and either (a) the marker is produced again on the productive path (product fix + regression in the native single-default group) or (b) the assertion is corrected to the new intended bootstrap semantics (test fix + rationale), then a push-triggered Docker+Podman native single-default pair is terminal green on the exact develop head; no permanent skips, no rerun spam.

## Watch status (2026-11-08)
Fix-vs-masking unresolved: red at 8ecd1ea5d, silently skipped on b95f913ff + cdb4350a6 after #1482. The next commit touching installation_destroy_native_test.go must show a TERMINAL GREEN Native single-default pair, otherwise this bug returns to active.

## Dependencies and file ownership
None. Write-set: cmd/baha/installation_destroy_native_test.go + internal bootstrap marker paths (exact files per root-cause decision).
