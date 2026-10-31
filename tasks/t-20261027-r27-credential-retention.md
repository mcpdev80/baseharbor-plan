---
id: t-20261027-r27-credential-retention
type: task
areas: [application]
release: v0.4.27
version: ""
parent: v0.4.27
owner: z3-lane
priority: ""
depends_on: [t-20261017-release-0-4-27-updates]
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#1077"]
sources: []
blocker: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1096"]
---

- [x] t-20261027-r27-credential-retention · Implement native credential retention + provenance (supersedes #1077 debt) #task #release/v0-4-27 #status/closed #view/closed #board/planned #area/application #kind/task
    <!-- generated:card -->
    **Owner:** z3-lane  
    **PR:** [baseharbor#1077](https://github.com/mcpdev80/baseharbor/pull/1077)  
    **Needs:** t-20261017-release-0-4-27-updates  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1096)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.27](../releases/v0.4.27.md)  
**Depends on:** t-20261017-release-0-4-27-updates  
**Required by:** [t-20261017-release-0-4-27-prepare](t-20261017-release-0-4-27-prepare.md)  
**Owner:** z3-lane  
**Priority:** not set  
**PRs:** [baseharbor#1077](https://github.com/mcpdev80/baseharbor/pull/1077)  
**Source:** 
<!-- /generated:links -->

## Goal

Native credential retention with an explicit provenance decision on the switch-back path, so the retention work that only ever existed on the retired `#1077` branch is actually implemented on develop.

## Context: cmf23 findings C1 and C2 (P1)

Source: Codex review verdict cmf23 on `baseharbor#1077` (reviewed head `a39e6bf5`), where switch-back restores backend credential values without any provenance check (C1) and the resulting credential placement transitions leave impact-consent state stale against the credentials the runtime actually uses (C2). Both findings stay unaddressed today because develop carries no retention path at all.

## Scope

- In scope: retention plus provenance in `internal/application/**`, and the regression tests named under Acceptance.
- Out of scope: new credential storage backends or secret formats, Console/UI or connector changes, CI/release work, and any path outside the owned write set.

## Acceptance

- `go test ./internal/application/ -run SwitchBack` is green for all tests in that selection, and the selection matches at least one test on develop (an empty selection that reports "no tests to run" is not acceptance).
- `ensureNativeBackendCredentialValues` runs on the switch-back path and resolves its provenance from a justified source (state or backend probe); the reasoning is stated in the handoff.
- A regression test reproduces the stale-impact-consent drift (cmf23 C2) and fails before, passes after, the fix.
- Independent review and mandatory CI are green according to the BaseHarbor repository rules.

## Required checks

- `go test ./internal/application/ -run SwitchBack`
- `go test ./internal/application/` for package regressions
- Impact-selected CI per the product repository guidelines; no release matrix unless the impact analysis requires it

## Dependencies and file ownership

- Owned files: `internal/application/**` (write set of this task).
- Depends on: no implementation prerequisite. The release-cycle intake card [t-20261017-release-0-4-27-updates](t-20261017-release-0-4-27-updates.md) is recorded as prerequisite because the validator requires it for any new v0.4.27 scope card.
- Shared files: none expected; coordinate with the owning task before touching any shared registration or golden file.

## Handoff

- 2026-10-27 (z19 planning lane, Owner mission z19): ACCEPTED + CLOSED. PR #1096 was
  MERGED into develop as squash `3431b22c94b068f15f9bd7b31b9f87e846200f0f`
  (mergedAt 2026-10-27T03:10:34Z), so the earlier review state resolves to
  accepted/closed. Evidence: root repo `evidence/board-2026-10-26/z3-credential-retention.md`
  (implementation + green local checks), `z5-reviews-1096.md` (independent CODEX-REVIEW
  of head `b7b21dad`), `z7-covmap.md` (coverage mapping landed on the PR branch) and
  `z18-pr3-plan.md` (planning note). Resolution string "merged squash 3431b22c" is
  recorded here because the schema resolution field is the enum
  accepted|superseded|dropped; `resolution: accepted` is the machine-readable state.
- 2026-10-27 (planning lane y8): card created from the cmf23 triage chain. Verified current state: develop contains no `ensureNativeBackendCredentialValues` and no `SwitchBack` test, while both exist only on the retired `#1077` branch (`internal/application/runtime_native_binding_projection.go`, `runtime_environment.go` and `runtime_placement_retention_test.go`). Diagnosis is documented in `evidence/board-2026-10-26/y4.md` with the y3 triage note in the same directory. No owner claimed, status planned.
