# 0428-082 Perses Infra dashboards — r1 evidence (worker w208)

## Task

t-20261114-r28-perses-dashboards (card 0428-082). PR #1665, draft, base `refs/heads/w083-perses-datasources`.
Goal: native Perses infrastructure dashboards with verified Prometheus metrics and explicit missing-signal behavior.

## Scope write-set (my card)

Own: `internal/metrics/prometheus.go`, `internal/metrics/prometheus_render.go`, `internal/metrics/prometheus_verify.go` (+ `prometheus_files.go`, `prometheus_shared.go`), the `internal/metrics/*_test.go`, and `internal/metrics/testdata/perses-infra-dashboard/`.
Touch (product wiring, permitted): `cmd/baha/app_status_result.go` + perses CLI tests, `internal/capability/perses_selection.go`, `docs/spec/*.md`.
Do NOT touch: `internal/serviceaccess/**` (owner rail #1594/0428-053), `internal/observability/registry.go`, `internal/capability/perses_selection` runtime, `internal/identityprovider/**`, `internal/logs/**` (that is 0428-202, lane w207), `.github/**`, `internal/metrics/perses_dashboards*.go`, `internal/metrics/testdata/perses-dashboard-*/`, `internal/metrics/perses_prometheus_datasource*` (076 lane, #1597), `go.mod`/`go.sum` without proof.

## Reality witnesses

Planning repo remote (verified before first evidence commit):
`git remote -v` on `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`:
`origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` / `(push)`

Real remote heads via `git ls-remote https://github.com/mcpdev80/baseharbor.git`:
`e580d32414565442376f23ace9a4a2dd7ed03838  refs/pull/1665/head`  (my 082 PR head)
`b71c6da27e8bbf180d26762eb9bfb101ec5a7bbe  refs/pull/1684/head`  (base lane 0428-083, moved)
`408b18d2dc7b0abe299749bb3a506c8cbd089098  refs/pull/1724/head`  (grandparent 0428-177)
`ed55d893374b593a7a6032f0de496ca9920ad08d  refs/heads/w083-perses-datasources`  (082 PR base)

Base attestation SHA I rebase from: the new base head `b71c6da27e8bbf180d26762eb9bfb101ec5a7bbe`
(measured at refs/pull/1684/head, confirmed by ls-remote). This is the current content of the 083 base lane;
177 -> 083 -> 082 stacks correctly (wait on CONTENT, not merges, 3.3.8).

## PLAN (numbered)

1. Rebase the 082 candidate branch onto the new base head b71c6da27e8b so the candidate carries only 082 content on top of current 083.
2. Prove ancestry: `git merge-base --is-ancestor b71c6da27e8b <new head>` == YES, paste output.
3. Scope check: `git diff --name-only b71c6da27e8b <new head>` must list only the write-set above. Foreign files are left untouched and reported file:line, not merged in.
4. Undraft the PR via `gh api -X POST repos/mcpdev80/baseharbor/pulls/1665/mark_ready` (PATCH draft=false is inert).
5. Verify live: `gh pr view 1665 --json isDraft,baseRefName,headRefOid` — isDraft MUST be false; paste all three values.
6. Run one hosted run on the exact new head, watched to terminal (4.6). Prove with smallest matching gate: `go test ./internal/metrics/ -count=1` and `go build ./...`.
7. If the CLI cells stay red: that is field-gate 0428-198 (`internal/operatorauth/authorization.go:285`); record exact line + `GATE-FAIL 0428-198`, do not chase. If the packages cell stays red: field-gate 0428-202, missing client-cert.pem in `internal/logs/loki_test.go` (another lane); name it, do not fix.
8. Keep PR DRAFT until implementation AND gate are complete; move to review only at handoff.
9. Commit evidence to baseharbor-plan (never a product repo), push to origin/main, verify path present on origin/main, post END.

## Work plan (board file)

Board file `/home/marcel/dev/baseharbor-ecosystem/workers/todos/w208-0428-082-dashboards.json` kept in sync with these steps.

## Container/composition hygiene (3.3.5)

No docker/podman compose project started this round. pre/post list: none. `cleanliness: OK`.

## REPRODUCTION COMMAND (for CI run)

`go test ./internal/metrics/ -count=1` and `go build ./...` in repo `mcpdev80/baseharbor` at candidate head.

## repo-rule compliance

- No subagents (4.8): every step ran in this session.
- Evidence only in baseharbor-plan, never in a product repo. No `.evidence/` dir, no main-branch writes in product.
- No `.github/**` edits (Owner scope); no reruns/workflow_dispatch.
- One candidate branch per chain: the 082 branch named in mission.
