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
kanban_status: wait
kanban_lane: wait
kanban_summary: ""
kanban_title: 0428-179 · shell wrapper cells must run
priority: ""
depends_on: [t-20261114-r28-cli2-identity-secrets]
repos: [mcpdev80/baseharbor]
prs: [mcpdev80/baseharbor#1731]
sources: []
blocker: ""
wait_reason: "PR #1731 run 44812248904 fails cli-0..3 on managed-operator test-context failures addressed by prerequisite 0428-057 / PR #1615. Its cli-3 job installed zsh and fish. Latest #1615 head 5d5cfdf1b3edefabfdcafb154d711d61dad74ed8 is running exact CI 44828743735 after exact cleanup-preview and guided wizard test-gate fixes. Wait for it to pass and #1615 to merge; then hop #1731 onto current develop and rerun exact CI, verifying the wrapper test executes."
resolution: ""
evidence: ["https://github.com/mcpdev80/baseharbor/pull/1731", "https://github.com/mcpdev80/baseharbor/actions/runs/44812248904"]
---

- [ ] t-20261120-r28-shell-wrapper-tests-not-skippable · CI intake: zsh/fish wrapper tests skip silently when the shell is not installed #task #release/v0-4-28 #status/wait #view/wait #kind/bug
    <!-- generated:card -->
    **Owner:** Owner (marcel, direkt)  
    **PR:** [baseharbor#1731](https://github.com/mcpdev80/baseharbor/pull/1731)  
    **Waiting:** PR \#1731 run 44812248904 fails cli-0..3 on managed-operator test-context failures addressed by prerequisite 0428-057 / PR \#1615. Its cli-3 job installed zsh and fish. Latest \#1615 head 5d5cfdf1b3edefabfdcafb154d711d61dad74ed8 is running ex…  
    **Needs:** [t-20261114-r28-cli2-identity-secrets](t-20261114-r28-cli2-identity-secrets.md)  
    **Evidence:** [proof 1](https://github.com/mcpdev80/baseharbor/pull/1731), [proof 2](https://github.com/mcpdev80/baseharbor/actions/runs/44812248904)  
    <!-- /generated:card -->

<!-- generated:links -->
**State:** wait  
**Release:** [v0.4.28](../releases/v0.4.28.md)  
**Depends on:** [t-20261114-r28-cli2-identity-secrets](t-20261114-r28-cli2-identity-secrets.md)  
**Owner:** Owner (marcel, direkt)  
**Priority:** not set  
**PRs:** [baseharbor#1731](https://github.com/mcpdev80/baseharbor/pull/1731)  
**Source:** 
<!-- /generated:links -->

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
