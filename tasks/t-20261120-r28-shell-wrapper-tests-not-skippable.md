---
id: t-20261120-r28-shell-wrapper-tests-not-skippable
card_number: "0428-179"
card_short_title: "shell wrapper cells must run"
type: bug
areas: []
release: v0.4.28
version: ""
parent: ""
owner: "Owner (marcel, direkt)"
kanban_status: closed
kanban_lane: closed
kanban_summary: ""
kanban_title: 0428-179 · shell wrapper cells must run
priority: ""
depends_on: [t-20261114-r28-cli2-identity-secrets]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1731]
sources: []
blocker: ""
wait_reason: ""
resolution: accepted
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1731", "https://github.com/mcpdev80/baseharbor/actions/runs/44886665489", "https://github.com/mcpdev80/baseharbor/commit/c2c94ad115ffa33e91efcd1be1fae6fc2bba7046", "https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-21/shell-wrapper/round-3.md"]
---

- [x] t-20261120-r28-shell-wrapper-tests-not-skippable · CI intake: zsh/fish wrapper tests skip silently when the shell is not installed #task #release/v0-4-28 #status/closed #view/closed #board/planned #kind/bug
    <!-- generated:card -->
    **Owner:** Owner (marcel, direkt)  
    **PR:** [baseharbor#1731](https://github.com/mcpdev80/baseharbor/pull/1731)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1731), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44886665489), [proof 3](https://github.com/mcpdev80/baseharbor/commit/c2c94ad115ffa33e91efcd1be1fae6fc2bba7046), [proof 4](https://github.com/mcpdev80/baseharbor-plan/blob/main/evidence/r28-welle4-2026-11-21/shell-wrapper/round-3.md)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** accepted  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-identity-secrets](t-20261114-r28-cli2-identity-secrets.md)  
**Owner:** Owner (marcel, direkt)  
**Priority:** not set  
**PRs:** [baseharbor#1731](https://github.com/mcpdev80/baseharbor/pull/1731)  
**Source:** 
<!-- /generated:links -->

## Acceptance closure — 2026-11-21

At source SHA `db3f6927fee1a1831de9820a51f5e0264e59f184`, test `TestEndToEndInstalledZshAndFishWrappers` maps deterministically to `cli-3` (SHA-256 first eight bytes modulo four = 3). Exact run [44886665489](https://github.com/mcpdev80/baseharbor/actions/runs/44886665489) executed and passed `PR · Go unit · cli-3` (job `136793350734`); that workflow installs both `/usr/bin/zsh` and `/usr/bin/fish` before the Go suite. The full required PR matrix and `PR Selected Checks` passed. PR #1731 merged normally as `c2c94ad115ffa33e91efcd1be1fae6fc2bba7046`. The SHA -> test -> gate -> run proof is in [round-3](../evidence/r28-welle4-2026-11-21/shell-wrapper/round-3.md).

## Why this card exists (finding -> card duty, AGENTS 3.3.5 / 5.3)

Same CODEX post-merge review (post-merge-068-166-develop-96f2ae11.md, B2): TestEndToEndInstalledZshAndFishWrappers
(cmd/baha/context_terminal_test.go:434-439 and :491-505) drives zsh/fish ONLY if the binary is present and continues
otherwise. On a runner without those shells the gate reports success without executing either path, which is not durable
evidence for the fish recursion guard (completion_setup.go:64-67, :78-80).

## Acceptance

1. The test must fail loudly (or be reported as skipped by the CI aggregate, not as passed) when the shell under test is
   absent, so the gap is visible.
2. Either install the shells in the cell that owns this path, or split a dedicated cell with a name that shows it runs.
   Where this needs a change in .github/workflows/ci.yml or its trigger rule, the card owner reports the needed change to
   the coordinator with file:line (Owner scope, AGENTS 5.3) instead of editing it.
3. Evidence: one hosted run id at the exact head showing the cells as executed (not skipped) or failing loudly.

## Boundaries

Test code plus the guard that detects a missing shell. No silent taint of unrelated cells, no gate deletion.


ARBEITET JETZT, kante gegen session gemessen (name w179-0428-179-shells, ornith-kanal, worktree aus develop 3653369a4d83): der stille erfolg der zsh/fish-pfade in cmd/baha/context_terminal_test.go:434-439 und :491-505 wird zu fail-loud oder sichtbarem skip, und die gate-route kommt in DENSELBEN PR (owner-anweisung 51d95b99). konfliktfrei geworden, weil 0428-178 soeben #1718 abgeliefert hat (nur test-datei, keine funktionsaenderung).

Initial handoff: patch `0eeda344` was locally verified but had no PR because the available OAuth CLI token lacked `workflow` scope.

## Owner takeover (2026-11-20)

The connected GitHub Maintainer integration has repository push permission. PR [#1731](https://github.com/mcpdev80/baseharbor/pull/1731) is open from `codex/0428-179-shell-wrapper` at exact head `f90b3f448caf6441acfb3007deb2338308b400d9`. It makes missing zsh/fish fail loudly and installs both in the CLI-3 shard and the develop validation cell. Local `bash scripts/ci-workflow-policy.sh`, `gofmt -d cmd/baha/context_terminal_test.go`, and diff checks pass. Exact hosted run [44812248904](https://github.com/mcpdev80/baseharbor/actions/runs/44812248904) is pending on this head; keep the card active until the shell test executes and the exact PR checks pass.
