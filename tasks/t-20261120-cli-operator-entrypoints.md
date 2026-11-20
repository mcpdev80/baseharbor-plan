---
id: t-20261120-cli-operator-entrypoints
card_number: "0428-204"
card_short_title: "CLI operator entry points"
type: bug
areas: [cli, security]
release: v0.4.28
version: ""
parent: ""
owner: ""
kanban_status: planned
kanban_lane: planned
kanban_summary: "One or two sentences: the observable outcome."
kanban_title: 0428-204 · CLI operator entry points
priority: high
depends_on: [t-20261120-r28-cli-shard-operator-env]
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261120-cli-operator-entrypoints · 0428-204 · CLI operator seam: MCP handlers and direct Run entry points #task #release/v0-4-28 #status/planned #view/waiting #board/planned #area/cli #area/security #kind/bug
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Waiting for prerequisites**  
    **Needs:** [t-20261120-r28-cli-shard-operator-env](t-20261120-r28-cli-shard-operator-env.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** waiting  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261120-r28-cli-shard-operator-env](t-20261120-r28-cli-shard-operator-env.md)  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

One or two sentences: the observable outcome.

## Scope

- In scope:
- Out of scope:

## Acceptance

- Each criterion as a plain bullet. Do not use checkboxes here: only the card line above is a checkbox.

## Required checks

- **Modified features:** Inventory and adapt all affected existing unit, contract, integration, regression, E2E and native-runtime tests; add missing cases.
- **New features/providers (e.g. Perses Provider Contract):** Implement NEW dedicated positive, negative, authorization, ownership, error-path, compatibility and lifecycle tests wherever relevant. Passing unrelated existing suites is not sufficient.
- **CI integration and mapping are part of implementation:** Register every new/changed test in its package/test inventory and update existing test-to-gate mapping, selectors, relevant `REQUIRED_CLIENT_TESTS`/package equivalent, `scripts/pr-gate-plan.py`, `scripts/release-requirements.json`, and CI workflow paths/triggers where applicable. Coordinate reserved CI files with their owner; no new CI framework.
- **Mapping selection proof:** Verify affected paths select the required tests, unrelated paths do not unnecessarily select them, and the applicable stacked-PR, ready-for-review, develop and release workflows cannot silently bypass them. Unknown coverage broadens selection instead of failing open.
- **Hard acceptance gate:** For every required test provide exact SHA -> test ID -> mapped check/native gate -> trigger -> actual run URL/outcome. Missing test, registration, mapping, selection, trigger or real passing execution BLOCKS acceptance. Docker/rootless Podman each require independent live evidence when applicable; do not rerun unaffected checks needlessly.


- **Test binding (select exactly one):** ☐ normal (auto-discovered) · ☐ contract → add to `REQUIRED_CLIENT_TESTS` or the package equivalent in the same PR · ☐ new check → update `scripts/pr-gate-plan.py` and `scripts/release-requirements.json` in the same PR.
- Name every new or changed test (package, exact test ID, fixture/env and native runtime if applicable). Targeted checks for the changed area; broaden when impact is unknown.
- Record the existing CI validation/check or Docker/Podman native gate that actually executes each test, and which PR paths, develop integration event or release candidate selection triggers it.
- If coverage is absent, implement/register it in the owning CI lane before acceptance; prove positive selection for a relevant change and negative/non-selection for an unrelated change. Missing, skipped or failed mandatory execution is NOT PASS.
- For Docker/Podman tests, prove native Docker and rootless Podman/Quadlet separately where required; unit fakes do not replace live runtime evidence. Cross-repo tests run through existing develop/release acceptance, not a blocking independent PR gate.
- Handoff must identify exact source SHA, test -> CI gate -> trigger -> actual run/outcome, or mark explicit CI coverage debt as blocking. No new CI framework or full automatic PR matrix.

## Dependencies and file ownership

- Owned files or areas:
- Shared files: coordinate through the owning task.

## Handoff

- Current state, branch, PR and evidence links. Newest first.

## Why

0428-198 delivered an in-test operator identity seam (head 7546b1806aac, 8 files) and proved it fires on the
`runWithIO` path. The lane's round-3 dossier (`evidence/r28-welle4-2026-11-20/cli-shard-operator-env/round-3.md`)
records that this does not reach every way a test enters the product: MCP tool handlers connect through
`server.Connect`/`client.Connect` and `CallTool` with their own contexts, and several tests call the command
object directly (`rootCommand().Execute(ctx)` / `.Run(ctx)`) instead of through `runWithIO`. Those call sites
never receive `operatorauth.WithEnforcement`, so they keep failing with the managed-environment operator
message in `PR · Go unit · cli-0..3`.

## What

1. Enumerate the entry-point classes that reach enforcement-relevant production code from `cmd/baha` tests,
   using the gate map (`cli-shard-operator-env/gate-map-1.md`) as the starting list and `git grep` to refresh it.
2. Make the seam apply for each class, in one place per class, keeping the required order
   (`WithEnforcement` -> `WithVerifiedPrincipal` -> `WithMembershipProvider`) exactly as 0428-198 established it.
3. Keep production behaviour unchanged: the seam stays nil outside tests, asserted by one test.

## Acceptance

- `PR · Go unit · cli-0`, `cli-1`, `cli-2`, `cli-3` pass at the exact head with no operator message in their logs.
- `internal/operatorauth/**` decision logic untouched (no `policy.go`, no `authorization.go` edits).
- One evidence table line per entry-point class: class, file:line, before (failing test), after (passing test).
