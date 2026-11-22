# PR #1754 independent read-only review — acd8dd95e6a7

## PLAN

1. Verify the real product GitHub remote, PR #1754 exact head/base and exact hosted run identity.
2. Read the full workflow diff and compare cli-3 zsh/fish provisioning with the existing owning-shard provisioning step.
3. Verify there are no unrelated workflow changes and inspect exact-run logs for executed tests, without treating skipped work as a pass.
4. Verify terminal run 44974482264 and executed cli-3 evidence for the exact SHA; finalize the exact-SHA verdict.
5. Keep #1753 held for its missing Docker data-capabilities gate; preserve the #1750 findings; no product-branch edits, local tests, merges, closes, comments, reruns or subagents.

## Exact refs

- Planning repository remote verified before evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.
- Product remote: `origin https://github.com/mcpdev80/baseharbor.git` (fetch and push).
- `git ls-remote` returned `6209874428f08dc3e90d6e29a42b30683ce9932a refs/heads/develop` and `acd8dd95e6a7d77d59e6a602203e5891efc32cf8 refs/pull/1754/head`.
- PR API: #1754 OPEN, ready for review (`isDraft=false`), base `develop`, head `acd8dd95e6a7d77d59e6a602203e5891efc32cf8`.
- GitHub compare: `ahead_by=1`, `behind_by=0`, merge-base exactly `6209874428f08dc3e90d6e29a42b30683ce9932a`.
- Full file list contains exactly `.github/workflows/ci.yml`; the exact patch is one added step (+9/−0), with no other workflow lines changed.

## Source review

The new step is at `.github/workflows/ci.yml:1681-1689` inside `pr_draft_go_shards` (job begins at line 1645). It is the same complete step as the existing shard provisioning at `:1254-1262`: same name, `if: matrix.shard == 'cli-3'`, bash shell, strict mode, `sudo apt-get update`, `sudo apt-get install -y zsh fish`, and both `command -v` echo lines. It is positioned after setup-go and before the shard test command. No unrelated workflow changes were present.

The unchanged regression at `cmd/baha/context_terminal_test.go:458-468` iterates both `zsh` and `fish`, calls `exec.LookPath` for each, and uses `t.Fatalf` at `:467` when either is absent. It does not skip or soften the missing-shell case. This PR does not modify the test.

## First hosted run — superseded by later exact-head execution

Run `44973717868` was triggered by `pull_request`, was terminal SUCCESS for exact head `acd8dd95e6a7d77d59e6a602203e5891efc32cf8`, but skipped the Draft Go shard and its selected-check aggregate. It did not witness the new step and is superseded for the specific provisioning question by run `44974482264` below. Its skipped receipts are not treated as passes.

## Final exact-head hosted run and remaining finding

Run `44974482264` was triggered by `pull_request`, completed at `2026-11-22T02:06:36Z`, and reports SUCCESS for exact head `acd8dd95e6a7d77d59e6a602203e5891efc32cf8` with base SHA `6209874428f08dc3e90d6e29a42b30683ce9932a`.

- `PR · Draft source and routing` job `137061186842`: SUCCESS.
- `PR · Draft Go · packages` job `137061186987`: SUCCESS.
- `PR · Draft Go · cli-0` job `137061187073`: SUCCESS.
- `PR · Draft Go · cli-1` job `137061187082`: SUCCESS.
- `PR · Draft Go · cli-2` job `137061187002`: SUCCESS.
- `PR · Draft Go · cli-3` job `137061187025`: SUCCESS. Its step “Install interactive shells for the shell-wrapper path” executed `sudo apt-get install -y zsh fish` and printed `zsh: /usr/bin/zsh` and `fish: /usr/bin/fish`.
- The following cli-3 step “Reuse canonical CLI shards and test selected non-CLI packages” ran with `BASE_SHA=6209874428f08dc3e90d6e29a42b30683ce9932a`, `HEAD_SHA=acd8dd95e6a7d77d59e6a602203e5891efc32cf8`, and `SHARD=cli-3`, then printed `No changed Go packages.` Because the reviewed diff changes only `.github/workflows/ci.yml`, the CLI shard script selected no Go packages. Thus this run proves the shell provisioning executes on cli-3, but does not prove `TestEndToEndInstalledZshAndFishWrappers` executed.
- `PR Selected Checks` job `137061189427`: SKIPPED. This Draft-triggered run is not a receipt for that aggregate.

The new step has exact parity with the existing ready-shard provisioning template, and the source diff remains limited to the intended workflow insertion. The remaining acceptance gap is test routing: this workflow-only change does not select `cmd/baha/context_terminal_test.go`, and the successful cli-3 job explicitly reports no changed Go packages. The exact missing receipt is an executed `TestEndToEndInstalledZshAndFishWrappers` on this SHA; it is still required before approval.

## Affected exact heads after #1754 lands on develop

The following cited candidates will be one commit behind the new develop head and need fresh exact-head runs before their affected reviews/gates can rely on current-base status: #1752 `a4adc29a584`, #1750 `4bd779b1501`, #1723 `8fe3c9bfb3c`, #1753 `71deb610a03`, and #1746 `48f0cb1e44d`.

## Verdict

REQUEST CHANGES for missing exact-head execution of the zsh/fish wrapper regression. Run `44974482264` confirms the added installation step executes successfully on cli-3 and both executables resolve, but its test step reports `No changed Go packages`; the wrapper test was not run. The source diff itself is narrowly scoped and matches the existing shard provisioning step, with no unrelated workflow changes. No product code, test, workflow, branch or PR was modified by this reviewer; no local tests, comments, merges, closes, reruns or subagents were used.

## repo-rule compliance

Read-only review of the exact GitHub head and hosted API evidence. No workflow edits or reruns were made. No test runs or containers were started locally.

## cleanliness

Before: command `docker ps -a`, shell pid 1625899. Output:

```text
CONTAINER ID   IMAGE                   COMMAND                  CREATED        STATUS                      PORTS     NAMES
268b7d8b4612   alpine:3.22             "sleep 300"              6 hours ago    Exited (0) 6 hours ago                bh-itest-1c3f4e6d-12470-edit-runtime-integration-dev-api-1
34cf9576dc2b   haproxy:3.2.23-alpine   "docker-entrypoint.s…"   10 hours ago   Exited (0) 10 hours ago               bh-itest-7daed22f-28345-shared-openbao-1
e88b00795b5c   openbao/openbao:2.7.1   "docker-entrypoint.s…"   10 hours ago   Exited (0) 10 hours ago               bh-itest-7daed22f-28345-shared-openbao-member-1-1
1451a7b5b3c6   postgres:18-alpine      "docker-entrypoint.sh"   10 hours ago   Exited (0) 10 hours ago               bh-itest-7daed22f-28345-shared-postgres-init-1
d7ba821c0e08   haproxy:3.2.23-alpine   "docker-entrypoint.s…"   10 hours ago   Exited (0) 10 hours ago               bh-itest-7daed22f-28345-shared-postgres-1
957a80e73b57   postgres:18-alpine      "/bin/sh -ec 'cp /ru…"   10 hours ago   Exited (0) 10 hours ago               bh-itest-7daed22f-28345-shared-postgres-member-1-1
45bddf32278e   postgres:18-alpine      "/bin/sh -ec 'trap :…"   10 hours ago   Exited (130) 10 hours ago             bh-itest-7daed22f-28345-shared-postgres-admin-1
9d3f1a2b1e0e   openbao/openbao:2.7.1   "/bin/sh -ec 'trap :…"   10 hours ago   Exited (143) 10 hours ago             bh-itest-7daed22f-28345-shared-openbao-admin-1
```

After: command `docker ps -a`, shell pid 1653310. Output:

```text
CONTAINER ID   IMAGE                   COMMAND                  CREATED        STATUS                      PORTS     NAMES
268b7d8b4612   alpine:3.22             "sleep 300"              7 hours ago    Exited (0) 7 hours ago                bh-itest-1c3f4e6d-12470-edit-runtime-integration-dev-api-1
34cf9576dc2b   haproxy:3.2.23-alpine   "docker-entrypoint.s…"   10 hours ago   Exited (0) 10 hours ago               bh-itest-7daed22f-28345-shared-openbao-1
e88b00795b5c   openbao/openbao:2.7.1   "docker-entrypoint.s…"   10 hours ago   Exited (0) 10 hours ago               bh-itest-7daed22f-28345-shared-openbao-member-1-1
1451a7b5b3c6   postgres:18-alpine      "docker-entrypoint.sh"   10 hours ago   Exited (0) 10 hours ago               bh-itest-7daed22f-28345-shared-postgres-init-1
d7ba821c0e08   haproxy:3.2.23-alpine   "docker-entrypoint.s…"   10 hours ago   Exited (0) 10 hours ago               bh-itest-7daed22f-28345-shared-postgres-1
957a80e73b57   postgres:18-alpine     "/bin/sh -ec 'cp /ru…"   10 hours ago   Exited (0) 10 hours ago               bh-itest-7daed22f-28345-shared-postgres-member-1-1
45bddf32278e   postgres:18-alpine     "/bin/sh -ec 'trap :…"   10 hours ago   Exited (130) 10 hours ago             bh-itest-7daed22f-28345-shared-postgres-admin-1
9d3f1a2b1e0e   openbao/openbao:2.7.1  "/bin/sh -ec 'trap :…"   10 hours ago   Exited (143) 10 hours ago             bh-itest-7daed22f-28345-shared-openbao-admin-1
```

## END codex-rev-1747 BLOCKED

Reason: run 44974482264 executed cli-3 provisioning, but selected no Go packages, so the required zsh/fish wrapper regression lacks exact-head hosted proof.

## PLAN update

1. Read `/var/tmp/rev1754b.g.md` and capture the follow-up acceptance instructions.
2. Verify the exact-head run 44974482264 and cli-3 job 137061187025 terminal result and provisioning/test evidence.
3. Update this evidence from the prior blocked state to the final verdict, without repeating the source diff review.
4. Validate and publish the evidence through the verified Planning origin/main.
5. Preserve the separate #1753 hold and report the review handoff to the Coordinator.

## Planning publication witness

Initial evidence commit published to Planning origin/main: `dbfa824c2`.

Exact output of `git ls-tree -r --name-only origin/main | grep 'evidence/r28-welle5-2026-11-22/oras-0428-229/review-1754-headacd8dd95.md'` after fetching origin/main:

```text
evidence/r28-welle5-2026-11-22/oras-0428-229/review-1754-headacd8dd95.md
```
