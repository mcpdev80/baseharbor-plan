ROLLE: REVIEW
Zeitstempel: 2026-11-21 12:24 UTC
Backend/Modell: OpenAI Codex / GPT-6.2

Verdict: REQUEST CHANGES

Karte: t-20261114-r28-perses-dashboard-databases (0428-076)
PR: #1597
Exakt geprüfter Head: 12a6e7a46e85cc5ab3b3464fe24dddf08e1807e7
Gemessene develop-Basis: 97b2ba5543f07b820b5c18a688058fd932c4516f

## PLAN

1. Read binding coordinator policies, current task contract, prior reviews, and owner-stop state. Done.
2. Verify GitHub remotes, develop and PR refs, exact ancestry, changed paths, and commit count. Done.
3. Review card acceptance criteria against source and tests; inspect exact-head required check logs. Done.
4. Write exact-SHA review verdict and actionable recipes if any in review-1.md. Done.
5. Publish only review-1.md and verify its presence on planning origin/main. In progress.

## Scope and exact-head witnesses

- Product remote verified by `git remote -v`: lane-origin, origin, and upstream resolve to `https://github.com/mcpdev80/baseharbor.git`.
- Planning remote verified before publishing: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch/push)`.
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1597/head`:
  `97b2ba5543f07b820b5c18a688058fd932c4516f refs/heads/develop`
  `12a6e7a46e85cc5ab3b3464fe24dddf08e1807e7 refs/pull/1597/head`
- `gh pr view 1597 --repo mcpdev80/baseharbor --json state,isDraft,mergeable,mergeStateStatus,headRefOid,baseRefName,headRefName,updatedAt`: state OPEN, isDraft false, mergeable MERGEABLE, mergeStateStatus CLEAN, base develop, head `12a6e7a46e85cc5ab3b3464fe24dddf08e1807e7`.
- `git merge-base --is-ancestor 97b2ba5543f07b820b5c18a688058fd932c4516f 12a6e7a46e85cc5ab3b3464fe24dddf08e1807e7`: exit 0.
- GitHub compare of those exact SHAs: status ahead, ahead_by 1, behind_by 0, merge base `97b2ba5543f07b820b5c18a688058fd932c4516f`.
- `git rev-list --count 97b2ba5543f07b820b5c18a688058fd932c4516f..12a6e7a46e85cc5ab3b3464fe24dddf08e1807e7`: 1.
- `git log --oneline 97b2ba5543f07b820b5c18a688058fd932c4516f..12a6e7a46e85cc5ab3b3464fe24dddf08e1807e7`: `12a6e7a46 hop(0428-076): rebase perses dashboard work onto develop`.
- Exact diff contains 13 paths: `cmd/baha/app_perses_cli_test.go`, `cmd/baha/app_status_result.go`, `go.mod`, `go.sum`, `internal/metrics/perses_dashboards.go`, `internal/metrics/perses_dashboards_helpers.go`, `internal/metrics/perses_dashboards_promql_test.go`, `internal/metrics/perses_dashboards_test.go`, and five `internal/metrics/testdata/perses-dashboards/*.json` goldens. These are within the card write-set. None of the prohibited `.github/**`, `scripts/**`, `internal/observability/registry.go`, `internal/capability/perses_selection.go`, or `internal/operatorauth/**` paths is changed.
- No task-specific STOP was present. The binding authority's Maintainer pause remains in force; this review performs no merge. The dependency `t-20261114-r28-perses-dashboard-selection` is accepted.

## Required checks

Run `44900492916` was completed with conclusion success on exact head `12a6e7a46e85cc5ab3b3464fe24dddf08e1807e7`, event `pull_request`. `gh pr checks 1597 --repo mcpdev80/baseharbor` reports these applicable checks passing: `PR Selected Checks`, `PR · Trusted Plan`, `Workflow policy`, `PR · Source format`, `PR · Validation · cli-gofmt`, `PR · Validation · go-build`, `PR · Validation · go-vet`, `PR · Focused Python`, CLI shards 0–3, owner, and packages. The package job 136835212018 completed success; its executed Go test step also completed success. Runtime, Docker, Podman, and other unrelated gates are skipped and are not counted as passes. The PR changes generated static dashboard resources and status metadata; no new lifecycle/runtime stack was started.

## Acceptance review

The CLI status additions expose database dashboard availability. PostgreSQL and MongoDB are explicitly unavailable with reasons and no fabricated dashboard; Prometheus, Loki, and Tempo have separate catalog entries. The candidate does not claim Perses alert evaluator or notification-routing parity. Those aspects are consistent with the card.

The native-format acceptance is not met. The candidate’s tests marshal the candidate-defined structs and unmarshal the result back into those same permissive structs; the golden files only pin those bytes. Neither mechanism validates against Perses v0.55.1.

## Finding 1 — emitted resources do not match Perses v0.55.1 native shape

Witnesses in the candidate at `internal/metrics/perses_dashboards.go`:
- Lines 96–106 marshal each query as `spec.kind`, `spec.spec`, and `spec.datasource` directly under the query wrapper. Perses v0.55.1’s query model has `spec.plugin.kind` and `spec.plugin.spec` (`github.com/perses/spec` v0.3.0, `go/dashboard/dashboard.go:52-60`).
- Lines 163–168 and 275/290/305 marshal dashboard-local datasources as `kind/name/default`. The pinned Perses spec defines a local datasource as `default` plus `plugin.kind/spec` (`github.com/perses/spec` v0.3.0, `go/datasource/datasource.go:26-32`).
- Lines 140–151 also model only name/version in dashboard metadata; the pinned Perses API’s dashboard resource uses project metadata. If the intended import path supplies project outside the resource, document and validate that exact path.

The exact pinned Perses release v0.55.1 depends on `github.com/perses/spec v0.3.0` (Perses `go.mod`); its example dashboard at `perses/perses/dev/data/9-dashboard.json` has the nested query plugin and datasource plugin forms. The official API docs likewise describe a Dashboard as a project resource and query plugin nested under `spec.plugin`: https://perses.dev/docs/perses/latest/api/dashboard/

Correction recipe:
- File: `internal/metrics/perses_dashboards.go` and its tests/goldens.
- Change: marshal real dashboard, query, and datasource resources using the pinned Perses v0.55.1/v0.3.0 shape; give the dashboard an explicit project context or prove the supported project-path import contract. Keep each backend bound to its actual datasource and retain the unavailable PG/Mongo entries.
- Test requirement: replace/augment the self-round-trip test with validation by the pinned Perses schema/model or the version-matched Perses validator. Validate all three generated dashboards, query plugin nesting, datasource plugin definitions, references, and the explicit unsupported cases. Include a malformed-shape negative case that the native validator rejects.
- Stop criterion: do not approve until the generated resources pass the pinned Perses validator and the test proves malformed native structure fails.

## Finding 2 — tagged real PromQL parser test is not executed by PR CI

The new `internal/metrics/perses_dashboards_promql_test.go` has build constraint `//go:build promqlparser`. The exact-head `PR · Go unit · packages` job (136835212018) completed successfully, but the current base’s route at `.github/workflows/ci.yml:922-980,1196-1226` calls the selected unit shards. The packages route uses `scripts/pr-go-unit-shard.py:118-132`, which runs `go test -count=1` with no `-tags promqlparser`. A normal package success therefore does not execute the tagged test. The default heuristic tests do execute, but they do not substitute for the tagged parser test required by the candidate’s own comments and prior review finding.

Correction recipe:
- File: owner-owned `.github/workflows/ci.yml` at the Go-unit routing step beginning line 922 and package job beginning line 1224. No workflow file was edited in this review.
- Change: have the CI package route execute the metrics parser test with `-tags promqlparser` on pull_request for develop, retaining an explicit test receipt so a skipped or unmatched test cannot pass silently. The related executor is under the card’s forbidden `scripts/**` scope, so the workflow owner/coordinator must choose the permitted route.
- Test requirement: show `TestPersesPrometheusParserRejectsMalformedSelectors` as passed in a completed GitHub PR run on the corrected exact head, and show the malformed selector mutation makes that test fail.
- Stop criterion: do not approve based only on `PR · Go unit · packages` or the aggregate while the parser-tagged case remains absent/skipped.

## Handoff

Verdict is REQUEST CHANGES; no merge instruction. The two findings are independently blocking. The required CI-route change is owner-owned workflow scope and must be coordinated; this review did not edit product files, workflow files, task metadata, or the PR.

## Cleanliness

Reviewer PIDs: 2489482 (before) and 2494611 (after).
`docker ps -a` before and after each showed only the column header and no containers. No container was started by this review. Existing untracked `0428-211-hopdevelop-wt/` in the product checkout was observed and left untouched.

## Evidence publication

This file is the only file to publish for this review. After push, record the exact `origin/main` tree witness here.

END REVIEW DONE — REQUEST CHANGES for 12a6e7a46e85cc5ab3b3464fe24dddf08e1807e7.
