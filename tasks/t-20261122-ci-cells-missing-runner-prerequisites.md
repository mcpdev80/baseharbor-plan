---
id: t-20261122-ci-cells-missing-runner-prerequisites
card_number: "0428-229"
card_short_title: "CI cells miss runner tools"
type: task
areas: [ci]
release: v0.4.28
version: ""
parent: v0.4.28
owner: ""
kanban_status: planned
kanban_lane: ready
kanban_summary: "validate and PR · Draft Go · cli- stop failing on missing runner tools, so a PR that only changes product code can reach a…"
kanban_title: 0428-229 · CI cells miss runner tools
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: []
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261122-ci-cells-missing-runner-prerequisites · 0428-229 · Provision the runner prerequisites the two PR CI cells already require #task #release/v0-4-28 #status/planned #view/ready #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** unassigned · **Priority:** high  
    **Ready to assign** · prerequisites accepted  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** ready  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** unassigned  
**Priority:** high  
**PRs:** none  
**Source:** 
<!-- /generated:links -->

## Goal

`validate` and `PR · Draft Go · cli-*` stop failing on missing runner tools, so a PR that only changes product
code can reach a terminal green exact run. No test is skipped, softened or deleted to get there.

## Scope

- In scope: `.github/workflows/ci.yml`, two added steps. Nothing else.
- Out of scope: the tests themselves (`cmd/baha/app_repository_integration_test.go`,
  `cmd/baha/context_terminal_test.go`), the `scripts/**` installers, and every product file.

## Acceptance

- The `validate` job installs ORAS before its native integration step:
  - failing step today: `.github/workflows/ci.yml:404` `Run runtime integration tests serially` (step 16 of job
    `validate`, `.github/workflows/ci.yml:300`), which calls
    `go test -p 1 ./cmd/baha ./internal/application -run '^(TestRepositoryWorkflowRealLifecycle|…)'`
    and fails with `ORAS is required before Core setup` at
    `cmd/baha/app_repository_integration_test.go:27` (further failures at `:61`, `:193`, `:350`, `:538`).
  - authorized form already used in the same workflow: `.github/workflows/ci.yml:288-289` and
    `.github/workflows/ci.yml:551-552`, `Install verified ORAS for native Core bootstrap` /
    `run: bash scripts/ci-install-oras.sh`. Add the same step before the runtime reset at
    `.github/workflows/ci.yml:400`.
- The `pr_draft_go_shards` job installs zsh and fish for the cli-3 shard:
  - failing test today: `cmd/baha/context_terminal_test.go:467`
    `zsh is required to run this wrapper path; install zsh in the owning CI cell`, job
    `PR · Draft Go · cli-3`, `github/workflows/ci.yml:1645` (steps begin at `:1672`, setup-go ends at `:1680`).
  - authorized form already used in the same workflow: `.github/workflows/ci.yml:1254-1262`
    `Install interactive shells for the shell-wrapper path` with `if: matrix.shard == 'cli-3'`
    (`sudo apt-get install -y zsh fish`). Add the same step after `.github/workflows/ci.yml:1680`.
- Witness runs after the change: an exact-head run of any draft PR shows `PR · Draft Go · cli-3` green, and a
  `validate` run shows step 16 green with the ORAS line present in the job log.
- Fail-loud behaviour stays: a missing prerequisite still fails the test rather than skipping it
  (`cmd/baha/context_terminal_test.go:467` is intentional, its comment records why a silent skip is not evidence).

## Execution notes

- Found by lane `0428-223-testctx` in hosted logs only, akte commit `efccdc0e4`
  (`evidence/r28-welle5-2026-11-22/testcontext-0428-223/round-2-ci-diagnosis.md`): develop run `44918870333`
  shows the same ORAS failure, so this is not a candidate regression.
- Same root cause blocks PR #1752 (`PR · Draft Go · cli-3` job `137051447593` at head `719242df476`) and
  PR #1750 (validate job `137044903908`, `PR · Draft Go · cli-3` job `137044885831` at head `1588ee1be72`).
- `.github/**` is Owner-scope in this window: worker lanes report file:line and do not edit (AGENTS 5.3,
  CI-Aufnahmepflicht). The Owner applies the two steps; a lane then re-runs and witnesses the exact CI.
