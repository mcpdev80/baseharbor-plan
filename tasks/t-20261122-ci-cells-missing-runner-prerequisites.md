---
id: t-20261122-ci-cells-missing-runner-prerequisites
card_number: "0428-229"
card_short_title: "CI cells miss runner tools"
type: task
areas: [ci]
release: v0.4.28
version: ""
parent: v0.4.28
owner: w21-pr1702-0428-142-compat
kanban_status: active
kanban_lane: active
kanban_summary: "validate and PR · Draft Go · cli- stop failing on missing runner tools, so a PR that only changes product code can reach a…"
kanban_title: 0428-229 · CI cells miss runner tools
priority: high
depends_on: []
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1754]
sources: []
blocker: ""
wait_reason: ""
resolution: ""
evidence: []
---

- [ ] t-20261122-ci-cells-missing-runner-prerequisites · 0428-229 · Provision the runner prerequisites the two PR CI cells already require #task #release/v0-4-28 #status/active #view/active #area/ci #kind/task
    <!-- generated:card -->
    **Owner:** w21-pr1702-0428-142-compat · **Priority:** high  
    **PR:** [baseharbor#1754](https://github.com/mcpdev80/baseharbor/pull/1754)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** active  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** none  
**Owner:** w21-pr1702-0428-142-compat  
**Priority:** high  
**PRs:** [baseharbor#1754](https://github.com/mcpdev80/baseharbor/pull/1754)  
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

Owner ordered the central zsh provisioning; mission b34f567c3cf2 adds the existing authorized step 'Install interactive shells for the shell-wrapper path' (template ci.yml:1254-1262) into pr_draft_go_shards (ci.yml:1645) on branch lane-0428-229-ci-draft-cell-shells; ORAS half of the card is solved differently by 0428-223 test-side and is under review

lane delivered PR #1754 (branch lane-0428-229-ci-draft-cell-shells, head acd8dd95e6a): adds the existing authorized step 'Install interactive shells for the shell-wrapper path' into pr_draft_go_shards; ORAS half stays with 0428-223's test-side route under review. exact-head CI and independent review pending

Owner ordered exact-head read-only review by codex-rev-1747 (verdict only after terminal CI); run 44973717868 in_progress on acd8dd95e6a. After merge of #1754 every affected candidate PR must hop onto the new develop and re-run its exact hosted CI; coordinator books those hops

proof closed: run 44974482264 (draft variant) completed/success with PR Draft Go cli-3 job 137061187025 EXECUTED; job log shows 'sudo apt-get install -y zsh fish', 'zsh: /usr/bin/zsh', 'fish: /usr/bin/fish' and zero occurrences of the fail message from context_terminal_test.go:467. earlier run 44973717868 skipped that cell and stays as an incomplete witness. Owner restores ready and merges after the verdict

RETRACTION of my own earlier claim: the install-only proof does NOT close the wrapper-test proof. verdict review-1754-headacd8dd95.md (plan dbfa824c2..e113d401b) says REQUEST CHANGES / END BLOCKED: shells install fine in cli-3 (job 137061187025, 'sudo apt-get install -y zsh fish', 'zsh: /usr/bin/zsh', 'fish: /usr/bin/fish') but the test step printed 'No changed Go packages.' (ci.yml:1706-1707) because #1754 changes only .github/**, so scripts/pr-draft-go-packages.py:8 selects no ./cmd/baha package and TestEndToEndInstalledZshAndFishWrappers never ran. needed: a test-inclusion route (map .github/workflows/ci.yml to ./cmd/baha in the planner, or force the cli-3 shard when the cell's own definition changed) - Owner-scope decision
