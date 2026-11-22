# Independent review: PR #1754 at exact head acd8dd95e6a7d77d59e6a602203e5891efc32cf8

## PLAN

1. Read `/var/tmp/revpub.g.md` and capture the required evidence location and scope.
2. Verify both exact-head hosted runs and the cli-3 install/test-step output.
3. Record the exact-head verdict, including whether the wrapper test ran.
4. Publish this review to Planning origin/main and send the result to the Coordinator; preserve the #1753 hold.

## Scope and refs

- Planning remote verified before commit: `origin https://github.com/mcpdev80/baseharbor-plan.git` (fetch and push).
- PR #1754, head `acd8dd95e6a7d77d59e6a602203e5891efc32cf8`; base `develop` at `6209874428f08dc3e90d6e29a42b30683ce9932a`.
- Product diff: one file, `.github/workflows/ci.yml`; one added shell-provisioning step, no unrelated workflow edits. Source review found exact parity with the existing shard install step and a cli-3-only condition.
- No product branch, workflow, PR state, or comment was changed by this reviewer.

## Exact hosted runs

- Run [44973717868](https://github.com/mcpdev80/baseharbor/actions/runs/44973717868) is for the exact head and is terminal SUCCESS, but the ready-variant Draft Go shard was SKIPPED. It did not execute the new cli-3 step.
- Run [44974482264](https://github.com/mcpdev80/baseharbor/actions/runs/44974482264) is for the exact head and is terminal SUCCESS. Draft Go cli-3 job [137061187025](https://github.com/mcpdev80/baseharbor/actions/runs/44974482264/job/137061187025) completed SUCCESS; its “Install interactive shells for the shell-wrapper path” step ran `sudo apt-get install -y zsh fish` and printed `zsh: /usr/bin/zsh` and `fish: /usr/bin/fish`.
- In the same cli-3 job, the subsequent test step ran with `BASE_SHA=6209874428f08dc3e90d6e29a42b30683ce9932a`, `HEAD_SHA=acd8dd95e6a7d77d59e6a602203e5891efc32cf8`, `SHARD=cli-3`, then logged `No changed Go packages.` Since the PR only changes the workflow, no Go package was selected. `TestEndToEndInstalledZshAndFishWrappers` was not executed on this head. The missing-shell failure text `required to run this wrapper path` has 0 hits in this job log; that absence does not prove test execution because the step selected no Go packages.
- `PR Selected Checks` job `137061189427` was SKIPPED in the Draft-triggered run; it is not a passing receipt.

## Verdict

REQUEST CHANGES. The one-step workflow change is scoped correctly and successfully provisions both shells in cli-3, but the exact-head run does not execute `TestEndToEndInstalledZshAndFishWrappers`. CI selection must be adjusted so that the real wrapper regression executes on this PR head before approval. No local tests were run.

cleanliness: nothing started

## repo-rule compliance

Read-only inspection. No code or workflow edits, no local tests, no draft/ready change, merge, close, GitHub comment, or subagents.

## END codex-rev-1747 BLOCKED

Blocked pending a CI-selected execution of `TestEndToEndInstalledZshAndFishWrappers` on exact head `acd8dd95e6a7d77d59e6a602203e5891efc32cf8`.
