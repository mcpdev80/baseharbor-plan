---
id: core-752
type: bug
release: v0.4.26
version: ""
parent: v0.4.26
owner: mcpdev80
depends_on: [core-893, core-895, core-896]
repos: [mcpdev80/baseharbor]
prs: ["mcpdev80/baseharbor#935"]
sources: ["mcpdev80/baseharbor#752"]
source_updated: "2026-10-15T16:51:21Z"
labels: [kind/bug, area/dx, area/compatibility]
blocker: ""
resolution: ""
evidence: []
---

- [ ] core-752 · Inspect: reconcile default instances unambiguously #task #release/v0-4-26 #status/active

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-893](core-893-ci-enforce-selected-pr-checks.md), [core-895](core-895-reviews-require-maintainer-approval.md), [core-896](core-896-runners-isolate-parallel-pr-checks.md)  
**Owner:** mcpdev80  
**PRs:** [baseharbor#935](https://github.com/mcpdev80/baseharbor/pull/935)  
**Source:** [baseharbor#752](https://github.com/mcpdev80/baseharbor/issues/752)
<!-- /generated:links -->

## Goal

A declared canonical `default` instance reconciles with the single detected named instance of the same capability and direction, without guessing when there are several. Selected as the v0.4.26 product pilot for core-901.

## Scope

- Bug: a manifest from `baha app init --quick` can declare `database.sql:default` and `cache.key-value:default`, while repository detection names the same single provider instance after its source service (`postgres`, `valkey`). Reconciliation compares names directly and produces a false split: declared `database.sql:default` → `stale`, detected `database.sql:postgres` → `new`. Same for cache and possibly document databases.
- Root cause: `internal/repositoryinspect/reconcile.go` / `findingMatchesIntent` accepts exact names, nameless findings and the OTLP default alias, but has no rule for a canonical `default` instance when exactly one named instance of the same capability/direction is detected. Still present at develop `ba664d398f65b9aa47882556bd27f9412cc0773d` (2026-10-15 source check).
- Required behavior (fail-closed): exactly one compatible named instance → one `satisfied` item under the declared name `default`; more than one → no guessing, keep stale/new/ambiguous evidence; explicit non-default names still need exact identity; compatible nameless evidence may enrich the satisfied item but must not leave the aliased named finding as a duplicate `new`.
- Out of scope: active v0.4.25 branch; a full Docker/Podman journey only for this fix.

## Acceptance

- `database.sql:default` + one detected `postgres` → one satisfied SQL item, no SQL `new`.
- `cache.key-value:default` + one detected `valkey` → one satisfied cache item, no cache `new`.
- Document DB follows the same instance rule.
- One named instance plus nameless evidence does not duplicate reconciliation.
- Two named instances never auto-alias to `default`.
- Explicit non-default names remain exact-match only.
- Existing OTLP behavior and read-only semantics are unchanged.
- Integrated as its own v0.4.26 PR against develop and evaluated in pilot core-901 with real evidence.

## Required checks

- Focused repositoryinspect fixtures (one compatible instance, several/ambiguous, explicit names and directions) and `go vet`; affected consumers per core-888 selection.

## Dependencies and file ownership

- Small own PR after the qualified PR-CI/review/runner foundation. Final semantic acceptance: v0.4.31 (#174).
- Prior work to compare, not merge blindly: branch `fix/752-default-instance-reconcile-v0421` at `70292f0cd436fdeb170652e26e6c5e228da23c1d` (diverged from develop; neither integration nor safe deletion is proven by ancestry).

## Handoff

- Live migration review: PR #935 head `8e00e7e4a2f30c4094094e1f153cb61447f415d3`; draft/preparatory work remains unaccepted. The current PR head supersedes older SHA assertions in its body. Preserve the existing owner, branch and PR.

- 2026-10-15 (after snapshot): draft PR #935 (`task/752-reconcile-default-instances`, head `d5bd0d236e` at check time) implements the fix in `internal/repositoryinspect` with focused tests. No claim comment on the issue; owner taken from the assignee. Must not be integrated before the qualified foundation.
- 2026-10-15 hygiene check: logic still present at develop `33b7ca94b42cc45e908c0d964cfbe0cc8349f231`; no new tests run then. Historical v0.4.20/v0.4.21/v0.4.24 references in the source explain the origin, not the current target. Related: #750, #751; earlier release work #569.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
