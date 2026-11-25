---
id: t-20261120-redact-invalid-org-environment-key
card_number: "0428-162"
card_short_title: "Redact env key errors"
type: task
areas: [architecture, security]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: closed
kanban_lane: closed
priority: high
depends_on: [t-20261114-r28-cli2-org-env, t-20261119-orgconfig-error-redaction]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: superseded
superseded_by: t-20261119-orgconfig-error-redaction
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1596", "https://github.com/mcpdev80/baseharbor/actions/runs/44945468909", "https://github.com/mcpdev80/baseharbor/commit/1080986fe73cb3d6e283fd9ef61c05c02b9260af"]
kanban_title: 0428-162 · Redact env key errors
---

- [x] t-20261120-redact-invalid-org-environment-key · Redact secret-like invalid environment keys #task #release/v0-4-28 #status/closed #view/closed #board/planned #area/architecture #area/security #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1596), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44945468909), [proof 3](https://github.com/mcpdev80/baseharbor/commit/1080986fe73cb3d6e283fd9ef61c05c02b9260af)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** superseded  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-org-env](t-20261114-r28-cli2-org-env.md), [t-20261119-orgconfig-error-redaction](t-20261119-orgconfig-error-redaction.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

Ensure `Config.Validate` never copies secret-like environment map keys into error text when the key is invalid, while keeping ordinary invalid-name diagnostics useful.

## Scope

- In scope: change the invalid-name error path in `internal/orgconfig/model.go` and add a sentinel regression in `internal/orgconfig/orgconfig_test.go`.
- Out of scope: changing secret-detection rules or authorization policy, editing `security.go`, changing CI/workflow code, or editing a shared branch before its current owner releases the files.

## Acceptance

- `TestSecretLikeEnvironmentMapKeyIsRedactedFromValidationError` fails at the current predecessor candidate and passes after the fix.
- The error for a secret-like invalid environment name is actionable and contains neither the supplied key nor the sentinel; ordinary invalid non-secret names retain their existing detailed diagnostic.
- The focused test and `go test ./internal/orgconfig -count=1` pass on the exact candidate SHA.
- The change is integrated only after both declared dependencies are accepted and the parent owner coordinates a single-writer handoff.

## Required checks

- **Test binding (select exactly one):** ☒ normal (auto-discovered) · ☐ contract → `REQUIRED_CLIENT_TESTS` · ☐ new check/catalog.
- Test: package `internal/orgconfig`; exact ID `TestSecretLikeEnvironmentMapKeyIsRedactedFromValidationError`; fixture is an invalid environment name containing `token=environment-map-key-sentinel-7f3a`; no native runtime is required.
- Route: ordinary Go package discovery via the existing `PR · Draft Go · packages` shard for a Draft stacked PR, and the normal Go unit package shard in the applicable ready-for-review PR workflow. Trigger: the PR diff changes only `internal/orgconfig/` Go files. Verify execution on the exact candidate SHA; a skipped job is not a pass.
- Required local checks: focused regression and `go test ./internal/orgconfig -count=1`; run `go vet ./internal/orgconfig` when verifying the change. Record exact SHA, test ID, CI check, trigger, run URL and outcome in the handoff.
- No CI catalog/workflow edit is planned because the test is an ordinary package-discovered Go unit test; confirm that mapping on the current workflow before acceptance.

## Dependencies and file ownership

- Owned files: `internal/orgconfig/model.go` and the dedicated regression in `internal/orgconfig/orgconfig_test.go`.
- Dependencies: 0428-056 (#1596), which introduces the environment validation surface, and 0428-149, which owns the first error-redaction fix in that same stack.
- Do not modify `security.go`, `.github/**`, or another worker's branch. The task stays unassigned/planned until dependencies are accepted and the shared write path is explicitly released.

## Handoff

- Superseded 2026-11-25 by 0428-149. The merged #1596 diff includes `TestSecretLikeEnvironmentMapKeyIsRedactedFromValidationError` and the corresponding safe diagnostic; exact-head run [44945468909](https://github.com/mcpdev80/baseharbor/actions/runs/44945468909) passed the Go package and selected-check jobs. No second implementation is needed.

- ZWEIFEL, observed at PR #1596 exact head `c90c3b89007e87a4bf277c8c9015fab3ac65728e`: `Config.Validate` formats an invalid environment key with `%q` (`internal/orgconfig/model.go`, lines 171–174 at that SHA), which can echo secret-like input. Evidence: [exact source](https://github.com/mcpdev80/baseharbor/blob/c90c3b89007e87a4bf277c8c9015fab3ac65728e/internal/orgconfig/model.go#L171-L174). A local red-green fix exists on isolated branch `codex/0428-149-map-key-redact` at `f113baf57aef9e24de5083740decdf84b361f8d8`, based on #1596 head; it has not been pushed or integrated. This card records the issue and preserves that candidate for coordinated handoff. Do not interpret it as accepted or CI-qualified.
- Current state: planned/unassigned with dependencies on 0428-056 and 0428-149. Start only after both are accepted and the current owner releases the shared files; then verify the exact candidate through the mapped Go package job and record its run.
