---
id: core-752
areas: [inspect]
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

- [ ] core-752 · Inspect: reconcile default instances unambiguously #task #release/v0-4-26 #status/review #view/review #area/inspect #kind/bug
    <!-- generated:card -->
    **Owner:** mcpdev80 · **Priority:** not set  
    **PR:** [baseharbor#935](https://github.com/mcpdev80/baseharbor/pull/935)  
    **Needs:** [core-895](core-895-reviews-require-maintainer-approval.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** review  
**Release:** [v0.4.26](../releases/v0.4.26.md)  
**Depends on:** [core-893](core-893-ci-enforce-selected-pr-checks.md), [core-895](core-895-reviews-require-maintainer-approval.md), [core-896](core-896-runners-isolate-parallel-pr-checks.md)  
**Owner:** mcpdev80  
**Priority:** not set  
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

- 2026-10-16 cleanup: temporary diagnostic PR #940 was closed WITHOUT merge after preserving its exact-source Actions evidence in this task and the closed pilot body. The product PR remains open; closing a pilot does not accept the product implementation.

- 2026-10-16 Maintainer-authorized closeout: PR #935 remains unmerged and unaccepted. Exact-source focused GitHub-hosted checks were rechecked in [Actions 38815960883](https://github.com/mcpdev80/baseharbor/actions/runs/38815960883). A local Git merge-tree check found no conflicts against develop after #930. core-893 and core-896 are accepted; the remaining foundation prerequisite is core-895 live protection activation and qualification. Merging the #933 proposal alone does not satisfy it. Preserve this task in review; do not check its card as done.

- 2026-10-15T22:24Z (session 3): **focused GitHub-hosted verification obtained autonomously** on exact tested SHA `4804cb1d53a1caaa44da6f384b0a18c170cae431` via a temporary ref-gated pilot lane modeled on the #936 pattern but narrowed to this task: branch `runtime-validation/ci/935-exact-reconcile` (ci.yml gained one ref-gated job `Core752 · Exact Reconcile Verification` plus one exclusion term so the legacy broad `validate` job would not run; not merged, branch deleted after recording). Run 38815960883 https://github.com/mcpdev80/baseharbor/actions/runs/38815960883: job **SUCCESS** (pinned-SHA assertion, gofmt of both changed files, `go test ./internal/repositoryinspect/ -count=1`, `go test ./cmd/baha -run 'Inspect|Reconcile' -count=1`, `go vet ./internal/repositoryinspect/`, CLI build; all gated by a Require step); Workflow policy PASS; legacy validate and every runtime/HA/preflight job **skipped**. No release matrix, no Hugging Face. Implementation is verified; **integration prerequisites remain**: core-893 selected-check enforcement qualified and core-895 review protection accepted (core-896 merged via #932). Permanent exact-SHA lane placement proposed to Session 1 in PR #935 comments. Evidence recorded in PR #935 body (comments carry run/job links). Earlier note: PR #935 head `4804cb1d` (this entry supersedes the request-only status of the 21:58Z entry below).

- 2026-10-15T21:58Z (session 3, this note's claim held under owner `mcpdev80`; claim already `active`, not re-claimed): implementation complete in draft PR baseharbor#935, tested source SHA `4804cb1d53a1caaa44da6f384b0a18c170cae431` (head of `task/752-reconcile-default-instances`; supersedes `8e00e7e4` and `d5bd0d23`). Sole-candidate membership correction confirmed and covered by an exact-evidence-attribution regression for both declaration orders. Local results green: `go test -count=1 ./internal/repositoryinspect/` (all default-instance, duplicate-evidence, direction-boundary, OTLP, QuickInit and sole-unclaimed-candidate tests), `go vet`, `gofmt`, `go test ./cmd/baha -run 'Inspect|Reconcile'`, CLI build. Focused **GitHub-hosted** verification requested from Session 1 (CI ownership) in baseharbor#752 (comment) and PR #935 (comment), because develop currently exposes no dispatchable hosted Go-source lane without the broad legacy runtime-validation job; runner isolation (core-896) is merged through #932. Remaining prerequisites: core-893 selected-check enforcement qualified and core-895 review protection accepted; PR stays draft until then. Not accepted; Maintainer decision pending.
- Live migration review: PR #935 head `8e00e7e4a2f30c4094094e1f153cb61447f415d3`; draft/preparatory work remains unaccepted. The current PR head supersedes older SHA assertions in its body. Preserve the existing owner, branch and PR.

- 2026-10-15 (after snapshot): draft PR #935 (`task/752-reconcile-default-instances`, head `d5bd0d236e` at check time) implements the fix in `internal/repositoryinspect` with focused tests. No claim comment on the issue; owner taken from the assignee. Must not be integrated before the qualified foundation.
- 2026-10-15 hygiene check: logic still present at develop `33b7ca94b42cc45e908c0d964cfbe0cc8349f231`; no new tests run then. Historical v0.4.20/v0.4.21/v0.4.24 references in the source explain the origin, not the current target. Related: #750, #751; earlier release work #569.

The [standard v0.4.26 task rules](../releases/v0.4.26.md#standard-rules-for-v0426-tasks) apply.
