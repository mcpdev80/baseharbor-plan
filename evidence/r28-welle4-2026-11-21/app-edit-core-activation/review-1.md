ROLLE: REVIEW

# CODEX-REVIEW — PR #1735 / Karte 0428-207

**Verdict: REQUEST CHANGES**

## PLAN

1. Read mission, authorization files, and record numbered plan — done.
2. Verify GitHub remote, frozen PR head/base, refs, ancestry, and changed files — done.
3. Read card contract, lane evidence, w223 reproduction, and split evidence — done.
4. Inspect guard behavior and test assertions — done.
5. Verify exact-head CI status and lifecycle test coverage — done.
6. Recheck candidate and write the verdict with an actionable recipe — done.
7. Publish this file to baseharbor-plan main and verify its remote presence — done.
8. Post END_DONE to coordinator — done.

## Candidate and read-only proof

Session: Codex review session; session identifier is not exposed by this interface.
Model/backend: GPT-6 Codex API runtime; exact serving variant/backend identifier is not exposed.
Review time: 2026-11-21 01:47 UTC.

PR #1735 is open, ready for review, not merged. Candidate head: `09cf55bbaa41c921f72681ef4ee4500d9083f807`; base `develop` at `40cb28c758b02960356434b630086a341ebe1738`.

Before review, `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/heads/lane-0428-207-appedit-core-activation refs/pull/1735/head` returned:

```text
40cb28c758b02960356434b630086a341ebe1738 refs/heads/develop
09cf55bbaa41c921f72681ef4ee4500d9083f807 refs/heads/lane-0428-207-appedit-core-activation
09cf55bbaa41c921f72681ef4ee4500d9083f807 refs/pull/1735/head
```

PR API: `head=09cf55bbaa41c921f72681ef4ee4500d9083f807`, `base.sha=40cb28c758b02960356434b630086a341ebe1738`, `draft=false`, `state=open`, `merged=false`, `mergeable_state=blocked`.

In the isolated product clone, fetching the exact develop and PR refs succeeded. `git merge-base --is-ancestor origin/develop origin/pr-1735; echo $?` returned `ancestor_exit=0`. `git diff --name-status origin/develop...origin/pr-1735` returned exactly:

```text
M cmd/baha/core_network_binding.go
A cmd/baha/core_network_binding_actionability_test.go
```

`git log --oneline origin/develop..origin/pr-1735` returned only:

```text
09cf55b fix(0428-207): make Core default-network binding guard actionable
```

Candidate immutability:

```text
PR head before review = 09cf55bbaa41c921f72681ef4ee4500d9083f807
PR head after review = 09cf55bbaa41c921f72681ef4ee4500d9083f807
```

## Findings

### 1. Refusal remains fail-closed and protected-owner behavior is retained

At `cmd/baha/core_network_binding.go:52-58`, the branch still refuses to adopt an existing native network when `len(actual) != 0` and `ExistingControlPlaneRuntimeInventory(...)` cannot prove the protected owner. The comment at `:53-54` explicitly preserves that a matching native label without that owner must never be adopted. The diff changes only the returned error at `:56` to `coreDefaultNetworkBindingMissingOwnerMessage(err)`; it does not change the owner decision or the `(false, nil)` path at `:59`. Neither `app_edit_apply_test.go` nor `core_network_binding_native_test.go` is in the diff, and no `.github/**` file is changed.

### 2. Blocking defect: the missing-inventory test does not exercise the ENOENT branch

`cmd/baha/core_network_binding.go:69-74` selects the missing-inventory wording only when `errors.Is(err, os.ErrNotExist)` at `:70`. But `cmd/baha/core_network_binding_actionability_test.go:18-20` labels the case `Missing inventory (os.ErrNotExist)` and passes `errors.New("lstat ... : no such file or directory")`. A plain error whose text resembles ENOENT does not satisfy `errors.Is(..., os.ErrNotExist)`; the test actually exercises the noncanonical-shape branch at `:73`. Its assertions at `:22-36` therefore do not verify the production missing-inventory case or that branch's wording. The separate noncanonical test at `:49-50` also enters `:73`.

The `:73-80` “FailClosedNeverSilent” test invokes the message renderer directly. Since that renderer always returns a newly created error, `missingErr == nil` is not a guard-level fail-closed check.

**Recipe:** In `cmd/baha/core_network_binding_actionability_test.go:18-20`, pass `os.ErrNotExist` or a wrapped sentinel (`fmt.Errorf("…: %w", os.ErrNotExist)`) and import the needed package. Assert a phrase unique to the `:70-72` branch, such as `runtime inventory is missing`. Keep the noncanonical test on a non-ENOENT error. Stop when the two tests fail under a mutation that removes or reverses the `errors.Is(err, os.ErrNotExist)` condition and pass in the `cmd/baha` Go unit shard.

### 3. Activation-path regression remains unproven by the new tests

Production wiring is direct: `inspectCoreDefaultNetworkBinding` calls the renderer at `cmd/baha/core_network_binding.go:55-56`, and `prepareCoreDefaultNetworkBinding` calls the inspector at `:76-81`. The three new tests do not call either production function; they call `coreDefaultNetworkBindingMissingOwnerMessage` directly at `core_network_binding_actionability_test.go:20,50,74`. They pin text, but do not themselves prove that the missing-owner refusal is returned through App Edit activation.

The lane's `## WAS DAMIT NICHT BEWIESEN IST` section is candid: it says the lane did not rerun the lifecycle and that the helper test does not prove the real lifecycle. The w223 reproduction on `baha-docker` is a baseline witness, not an after-fix witness. Exact-head hosted run 44849762052 did select `TestAppEditCommandCompleteProviderEditRunsRealLifecycle` in `cli-2`: `scripts/pr-go-unit-shard.py:28-40,64-81` discovers all `cmd/baha` tests, hashes each test name to a shard, and runs those selected names; SHA-256 assignment for this lifecycle test is `cli-2`. The exact-head `cli-2` log lists failed test names and omits this lifecycle test; its body has no `t.Skip`. This indicates that it was not among the shard failures, but the overall shard failed elsewhere and publishes no individual passing-test receipt.

That hosted observation does not satisfy acceptance criterion 2: a regression test must prove the activation path reports the missing protected Core/shared-owner condition. The new tests only call the helper.

**Recipe:** Add or reshape the allowed new `cmd/baha/*0428-207*` test to exercise `inspectCoreDefaultNetworkBinding` or the real App Edit activation path with an existing native network and absent protected inventory, and assert the actionable message. Ensure auto-discovery keeps it in a `cmd/baha` CLI shard. Stop when the regression fails against the old message, passes through the corrected guard at the exact candidate, and has a successful executed CI receipt. Preserve the owner-owned files and do not trigger a workflow from this review.

### 4. “What is not proven” boundary

The lane's boundary section exists and correctly distinguishes the message unit test from a real isolated-Core lifecycle. It does not claim the worker reran that lifecycle. The exact-head CI observation above narrows the boundary: the lifecycle test was selected and absent from the failure list, but its shard failed overall and produced no per-test pass receipt. The blocker is the missing regression that exercises the activation guard and asserts the missing-owner case, not the honest disclosure itself.

### 5. Required CI status and inherited failures

Run `44849220708` was a `pull_request` run at the exact head and completed `failure`; its jobs were `PR · Draft Go · cli-0..3` failures, `PR · Draft Go · packages` success, and `PR Selected Checks` skipped. It began while the PR was still a draft, so it is not a passing required-check aggregate.

Later run `44849762052` is also `pull_request`, completed `failure`, and has the exact same head. `PR Selected Checks` failed; `PR · Go unit · cli-0`, `cli-1`, `cli-2`, `cli-3`, and `packages` failed; `owner` succeeded. The CLI failure logs include inherited operator-auth failures, for example `TestAppCreateListShowPlan` in `cli-0` reports `Managed-environment machine operations require an authenticated BaseHarbor operator.` This is the 0428-204 / #1717 class and does not mention either changed file. The packages job separately reports three Loki datasource failures, including `loki_test.go:522: ... client-cert.pem: no such file or directory` (and corresponding failures at `:586` and `:633`), outside this PR's write set. Thus the CLI red is inherited and not a content defect of 0428-207, but the aggregate is not green and is not red only because of CLI shards. No workflow rerun or dispatch was issued.

## Planning repository publication

Planning remote witness from the isolated plan clone:

```text
origin https://github.com/mcpdev80/baseharbor-plan.git (fetch) [blob:none]
origin https://github.com/mcpdev80/baseharbor-plan.git (push) [blob:none]
```

After fetching `origin main`, `git log --oneline origin/main -5` showed:

```text
8fd3f82 plan: record exact PR 1615 runtime gate fix
3b82429 kanban: t-20261121-loki-verify-probe -> active
2599561 evidence: complete PR 1734 review plan
100765a evidence: add remote path witness to PR 1734 review
5b1bf3f Merge remote-tracking branch 'origin/main'
```

I attempted `git rebase origin/main`; Git could not write `.git/rebase-merge/git-rebase-todo.backup` and returned `Disk quota exceeded`. The verdict file was therefore published as a single-file GitHub Contents commit against the current `main` after verifying the path was absent. This records the publication method exception rather than claiming a successful local rebase/push. No shared checkout, product repository, PR, workflow, or other planning file was written.

## END

END DONE codex-rev-cli2b: PR #1735 reviewed as REQUEST CHANGES at unchanged head `09cf55bbaa41c921f72681ef4ee4500d9083f807`.
