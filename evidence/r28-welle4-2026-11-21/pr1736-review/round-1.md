ROLE: CODEX-REVIEW
PR #1736: `codex/env-destroy-gate-routing`
Candidate: `a595472b77fb3620fac1dd457448211a86e3be24`
Base: `develop` at `e6c199e7b7dd7d076a776d11c3ba16f25e59c254`

## PLAN

1. Read the review mission, cost-control policy, and task contract. Done.
2. Verify remote PR heads, exact base ancestry, diff, commit authors, and dependent PR #1627. Done.
3. Trace trusted coverage mapping, lifecycle gate selection and shards, fallback, and CI test routing. Done.
4. Observe the exact-head hosted run to terminal, count per-job log bytes, and decide verdict. Done.
5. Publish only this evidence file, verify origin/main tree presence, and post END. Done.

## Candidate and dependency witnesses

Product remote resolution first: `lane-origin https://github.com/mcpdev80/baseharbor.git (fetch)`. The listed `origin` and `upstream` URLs also resolve to the same GitHub repository.

`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/codex/env-destroy-gate-routing refs/pull/1736/head refs/heads/develop refs/pull/1627/head`:

```text
a595472b77fb3620fac1dd457448211a86e3be24 refs/heads/codex/env-destroy-gate-routing
e6c199e7b7dd7d076a776d11c3ba16f25e59c254 refs/heads/develop
e24bd481e0d08d0c9780834c211b3891343ede0d refs/pull/1627/head
a595472b77fb3620fac1dd457448211a86e3be24 refs/pull/1736/head
```

PR #1736 is OPEN, non-draft, mergeable, authored by `mcpdev80`; review decision is empty and there are no review requests or reviews. PR #1627 is OPEN, draft, mergeable, head `e24bd481e0d08d0c9780834c211b3891343ede0d`, base `develop`.

The exact develop head is an ancestor of #1736 (`git merge-base --is-ancestor refs/remotes/lane-origin/develop a595472b77fb3620fac1dd457448211a86e3be24` succeeded). `git rev-list --count candidate..develop` is `0`; `develop..candidate` is `2`. The candidate diff is exactly:

```text
M scripts/pr-gate-coverage.json
M scripts/pr-gate-plan.py
M scripts/test_pr_gate_coverage.py
M scripts/test_pr_gate_plan.py
```

`git log --format='%h %an' develop..candidate` contains only:

```text
a595472b7 Marcel Pfingstgräf
8f11a34da Marcel Pfingstgräf
```

The first commit parent is exact develop `e6c199e7b7dd7d076a776d11c3ba16f25e59c254`; the top commit parent is `8f11a34da52f7a7f81a48eaf8df75da6f0fc3f12`, the preceding candidate commit. Thus the candidate is current with develop and has no foreign commits. `git log -1 --format=%P` is the preceding candidate commit, not develop, because the branch has two commits.

The planning repository remote verified before evidence commit is:
`origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`

## Findings

### Trusted mapping and forward reference

At candidate `scripts/pr-gate-coverage.json:1467-1476`, `cmd/baha/env_destroy_integration_test.go` is marked `runtime_specific: true`, covered by both `integration/docker/coreless-lifecycle` and `integration/podman/coreless-lifecycle`, with required test name `TestEnvironmentDestroyNativeLifecycle`.

Develop `e6c199e7b7dd7d076a776d11c3ba16f25e59c254` contains zero matches for that test name under `cmd/baha` and `internal` (`git grep -c ...` produced no match; exit 1). The test body exists only in PR #1627's current head: `cmd/baha/env_destroy_integration_test.go:23`. `scripts/validate-pr-gate-coverage.py:179-184` validates `required_test_names` syntax and uniqueness, not that the source or test exists in the target base. Therefore, if #1736 lands before #1627, the mapping can be accepted while pointing at a path/test absent from develop. It does not fail closed at catalog validation time; the path is dormant until a later diff changes it.

The coverage resolver does select both gate IDs for the declared runtime-specific source: `scripts/validate-pr-gate-coverage.py:17-63` preserves both runtime variants when `runtime_specific` is true. Candidate test `scripts/test_pr_gate_coverage.py:192-202` asserts both gate IDs and the exact test-name metadata. Candidate planner test `scripts/test_pr_gate_plan.py:3131-3154` asserts that the complete env-destroy diff selects both gates.

However, the real coreless executor does not consume this `required_test_names` field. At the candidate's inherited `scripts/pre-release-integration.py:55-58`, `CORELESS_TEST_ANCHORS` contains only `TestSelectiveBackendCleanupPreservesRuntimeBaseline`; `CORELESS_SHARD_TESTS` at lines 62-81 lists the existing four shards and omits `TestEnvironmentDestroyNativeLifecycle`. `coreless_shard_checks` at lines 117-128 selects names only from `CORELESS_SHARD_TESTS`. The new test is also absent from the candidate's `scripts/pre-release-integration.py` (`git grep` confirms no occurrence). The remote #1627 head has the test body but no runner/shard registration. Thus the mapping-level unit tests prove selection of two gate IDs, but neither proves that the new test is executed in each runtime nor assigns it to exactly one shard.

### Required merge dependency and pre-merge condition

The safe ordering is: **keep PR #1736 draft until PR #1627 has landed with the new test registered in the coreless executor and exactly one shard**. Current PR #1736 is non-draft and PR #1627 is still draft, so this condition is not yet met. Before considering the condition satisfied, the #1627 candidate must register the test source in `CORELESS_TEST_ANCHORS` and include its exact name once in `CORELESS_SHARD_TESTS`, then show the named test selected and executed on both Docker and Podman coreless gates. The current `44928428184` run does not provide that evidence. Because #1736 modifies the planner, rerun the relevant exact-head checks after any base movement before merge.

### Conservative selection and fallback

For a valid but unowned source, `scripts/pr-gate-plan.py:1784-1812` marks missing declared ownership unresolved and broad-required when legacy logic had selected runtime gates. With `conservative_fallback=True`, valid verified diffs can add the broad unit/vet/build checks at lines 1813-1858; runtime gates are retained only when already declared and are never guessed for an unknown source. Invalid or untrusted diffs return unresolved without converting into the narrow plan. Candidate test `scripts/test_pr_gate_plan.py:3156-3160` confirms registration-only paths remain unresolved. This behavior is conservative for source checks and does not infer a runtime gate from an unknown path.

### CI routing and exact-head checks

Candidate `scripts/pr-gate-plan.py:712-716` places both `scripts/test_pr_gate_plan.py` and `scripts/test_pr_gate_coverage.py` in the `pr-planner-tests` command. On run `44928428184`, exact head `a595472b77fb3620fac1dd457448211a86e3be24`, event `pull_request`, `PR · Validation · pr-planner-tests` job `136919606391` completed success. The separate Focused Python job `136919606322` also completed success. The run reached terminal `completed/success`; exact commit check-runs show 9 success and 21 skipped, with no failed conclusions. `PR Selected Checks` job `136920102974` completed success.

The two runtime checks needed to prove this new test were skipped: `Targeted HA · docker` job `136919544603` and `Targeted HA · podman` job `136919590974`. Their per-job log commands each returned 0 bytes. Skipped is not a pass, and neither lifecycle execution is established by this run.

Per-job log byte counts (49152 bytes is the truncation threshold):

- `gh run view 44928428184 --repo mcpdev80/baseharbor --job 136919543415 --log`: 70051 bytes (oversized; not used for detailed content claims).
- `gh run view 44928428184 --repo mcpdev80/baseharbor --job 136919606391 --log`: 62789 bytes (oversized; job terminal state and source-declared command recorded separately).
- `gh run view 44928428184 --repo mcpdev80/baseharbor --job 136919606322 --log`: 59407 bytes (oversized).
- `gh run view 44928428184 --repo mcpdev80/baseharbor --job 136920102974 --log`: 103606 bytes (oversized).
- `gh run view 44928428184 --repo mcpdev80/baseharbor --job 136919544603 --log`: 0 bytes; targeted Docker job was skipped.
- `gh run view 44928428184 --repo mcpdev80/baseharbor --job 136919590974 --log`: 0 bytes; targeted Podman job was skipped.

### Verdict

**APPROVE CONTENT with a pre-merge condition; not merge-ready yet.** The trusted mapping correctly resolves the exact source to both gate IDs, and the candidate adds the mapping assertions to the pull-request planner test group. The absent runtime execution evidence is a dependency on PR #1627, not a reason to reject the mapping content. Keep #1736 draft until #1627 lands with the named test in exactly one shard and actual Docker plus Podman coreless execution; then refresh the base and rerun exact-head checks. Do not merge #1736 before that condition is met.

## repo-rule compliance

Read-only review. No product code, workflow, PR state, review request, task card, or branch was changed. No merge, push to product, test execution, or subagent was used. Owner-scope `scripts/**` was inspected only. The product checkout already contained an unrelated untracked directory `0428-211-hopdevelop-wt/`; it was left untouched.

## cleanliness

No test, container, or compose project was started. Initial Docker witness, PID `1484891`, showed the shared `bh-itest-13cfc16d-71420-shared-*` group running and `bh-itest-7daed22f-28345-shared-*` containers exited. They were not touched. Final Docker witness, PID `1509503`, showed only the seven exited `bh-itest-7daed22f-28345-shared-*` containers; the other lane's group disappeared independently. No containers were created by this review.

## END

END_DONE codex-rev-1747: APPROVE CONTENT with pre-merge condition; keep #1736 draft until #1627 lands with lifecycle test registration and both runtime executions; candidate a595472b77fb3620fac1dd457448211a86e3be24. Initial evidence publication SHA: 4966913b4.

Planning validation in the clean planning worktree: `python3 scripts/plan.py render && python3 scripts/plan.py check` completed with 0 errors and 11 existing dependency warnings. `git diff --check` passed and no checkbox syntax is present in this evidence. This planning-only publication uses the plan repository's validator; product `scripts/ci-fast-check.sh` is not part of this evidence-only change.

Required origin/main tree witness, exact command output after fetch:

```text
evidence/r28-welle4-2026-11-21/pr1736-review/round-1.md
```
