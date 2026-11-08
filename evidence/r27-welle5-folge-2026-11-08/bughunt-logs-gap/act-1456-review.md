# CODEX-REVIEW 0427-131 — PR #1456

## PLAN

1. Verify the live PR head, current develop, mergeability, commit list, and run `42460379046`.
2. Read the full hosted job and step results, including the exact runtime failure lines.
3. Evaluate whether the claimed clean-develop comparison reproduces those same tests with the same runtime gate and configuration.
4. Review the CLI routing regression and the German documentation commits for relevance and scope.
5. Publish a SHA-specific verdict, correction recipe, tests, and stop criterion in the Planning Vault.

## Verdict

**ROLE: REVIEW**  
**VERDICT: KORREKTUR (REQUEST-CHANGES)**  
**PR #1456:** OPEN; GitHub reports `mergeable=CONFLICTING`, `mergeStateStatus=DIRTY`  
**Candidate head:** `27ef90449be7ad53a4d6011ad90ff83b6c6f0ae5`  
**Current develop:** `07ae6c3e91b081a189266ca4b162ba705d4aa78f`  
**Run:** `42460379046`, terminal failure, event `workflow_dispatch`

The CLI shorthand implementation and bilingual documentation are in scope and the unit/docs validation step passed. The run as a whole is not green: the `validate` job failed in runtime integration, and the evidence does not establish that those exact failures are pre-existing. The candidate is also based on an older develop commit and conflicts with current develop.

### 1. Exact hosted result: `validate` is the red job

`gh run view 42460379046` reports `headSha=27ef90449be7ad53a4d6011ad90ff83b6c6f0ae5`, `status=completed`, `conclusion=failure`, `event=workflow_dispatch`. The only failed workflow job is `validate`; `Workflow policy` passed. The `validate` job's step results are:

- `Validate documentation`: success.
- `Check formatting`: success.
- `Validate source readability`: success.
- `Run unit and package tests`: success.
- `Run runtime integration tests serially`: failure.
- Later `Run Go vet`, Compose validation, and CLI build steps: skipped after the failure.

The runtime step ran the selected five-test command. Four tests failed with the same explicit-consent error:

- `TestRepositoryWorkflowRealLifecycle` — `cmd/baha/app_repository_integration_test.go:55`: `record deployment before mutation: candidate submission requires an explicit operator/automation consent (--confirm-candidate); refusing to record deployment state`.
- `TestRepositoryComposeWorkloadUsesBaseHarborBackendsInCI` — `cmd/baha/app_workload_integration_test.go:99`: same consent error.
- `TestRepositoryComposeWorkloadOnlyLifecycleInCI` — `cmd/baha/app_workload_integration_test.go:233`: same consent error.
- `TestRepositoryBuildWorkloadRebuildsSourceChangesInCI` — `cmd/baha/app_workload_integration_test.go:387`: same consent error.

`TestMultiInstanceComposeLifecycleInCI` passed. `PR Selected Checks` and the PR matrix jobs were skipped for this workflow-dispatch run; `gh pr checks 1456` reports no checks on the branch. Thus “unit and docs green” accurately describes two successful steps, but neither the `validate` job nor the candidate's required PR checks are green.

### 2. The clean-develop comparison does not establish that these failures are pre-existing

The `round-1.md` comparison says `TestRepositoryComposeWorkloadOnlyLifecycleInCI` passed locally on the candidate with `BASEHARBOR_TEST_RUNTIME=docker` and was “identical to clean develop.” It does not include the exact command output or a clean-develop run ID/log for the hosted failures. More importantly, the test itself checks `BASEHARBOR_CI_RUNTIME_INTEGRATION` and calls `t.Skip` unless it equals `1` (`cmd/baha/app_workload_integration_test.go:182-184`). The reported local command does not set that gate. Its reported 0.007s “pass” therefore does not prove that the test body ran. The hosted command sets the runtime integration gate and failed; the evidence does not compare all four failing test bodies under that same gate and runtime/consent configuration against clean develop.

The consent error is consistent with a missing test-fixture consent input and the PR's CLI/docs diff does not touch deployment-consent code. That makes an environmental or baseline explanation plausible, but plausibility is not proof. Under the §5.4 same-test/same-configuration evidence standard, the current comparison cannot waive a red required integration result. The lane did observe its dispatched run to terminal, satisfying the observation portion of §4.6, but the dispatch run is not a PR-triggered required-check result. The evidence is internally inconsistent on execution provenance: its CI section says it explicitly triggered `workflow_dispatch`, while its repo-rule-compliance section says no workflow dispatch occurred. GitHub run metadata confirms `event=workflow_dispatch`; correct the conflicting evidence statement.

**Fix recipe:** Reproduce the exact failing integration selection on the candidate and clean develop with `BASEHARBOR_CI_RUNTIME_INTEGRATION=1`, the same runtime provider, runner class, persistent-state reset, and consent settings. Capture the exact command, commit SHA, run environment, per-test outcomes, and failure lines for each side. If clean develop fails identically under those same conditions, document the paired baseline evidence and identify the owner/environmental consent prerequisite; otherwise fix the fixture/candidate cause. After updating the existing candidate onto current develop, obtain and observe a genuine PR-triggered run on its exact new SHA. Do not count a skipped test or a local invocation without the runtime gate as a passing comparison.

### 3. The candidate is not based on current develop and GitHub reports conflicts

Remote refs show develop `07ae6c3e91b081a189266ca4b162ba705d4aa78f` and PR head `27ef90449be7ad53a4d6011ad90ff83b6c6f0ae5`. `git merge-base --is-ancestor 07ae6c3e91b081a189266ca4b162ba705d4aa78f refs/remotes/origin/pr-1456` returned exit 1. The merge base is `8bda98c1cd34a984810a0a0ee2d9fe4085b3933a`; the candidate has three task commits while current develop has 237 commits not in the candidate. GitHub reports `CONFLICTING` / `DIRTY`.

**Fix recipe:** Update the existing named candidate branch onto the fetched current `develop`, resolve the actual conflicts, and verify the final diff and ancestry. Run the required PR checks against that final SHA; do not treat run `42460379046` on the old base as final-candidate evidence.

### 4. The German coverage commits are relevant and appropriately scoped

The functional commit `8e93b08b` adds the top-level `baha logs` shorthand and a canonical CLI regression. `cd0d7e3e` adds the corresponding German human command-index and machine-coverage entries; the English machine-coverage entry is in the functional change. `27ef9044` removes one trailing-whitespace difference from the German command index. These changes preserve English/German command and machine-coverage parity, and the hosted documentation step reports success, including `DE technical integrity: PASS (163 paired pages)`. The two German documentation commits are narrow, related to the new command, and belong in this PR; they are not the reason `validate` failed.

## Evidence and exact candidate witnesses

- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1456/head` returned `07ae6c3e91b081a189266ca4b162ba705d4aa78f refs/heads/develop` and `27ef90449be7ad53a4d6011ad90ff83b6c6f0ae5 refs/pull/1456/head`.
- `gh pr view 1456` reports base `develop`, branch `work/w131-logs-command-gap`, OPEN, and mergeable `CONFLICTING`.
- The three task commits in the PR are `8e93b08bdcbe2b22b98baaf6d01cddf2898cc874` (CLI shorthand), `cd0d7e3efa5e83675f7896d3efe55bc2fba9a7d2` (German command/machine-coverage rows), and `27ef90449be7ad53a4d6011ad90ff83b6c6f0ae5` (German command-index normalization).
- PR diff is limited to `cmd/baha/commands.go`, `cmd/baha/human_cli_canonical_contract_test.go`, `cmd/baha/machine_coverage.go`, and four English/German command-index or machine-coverage documentation files.
- `gh run view 42460379046` reports `headSha=27ef90449be7ad53a4d6011ad90ff83b6c6f0ae5`, `event=workflow_dispatch`, completed failure. The red job was `validate`; its unit/docs steps succeeded and its runtime integration step failed as itemized above. PR Selected Checks and PR-triggered matrix jobs were skipped.
- Review-only: no product files changed, no tests or runtime jobs were run by this review, no workflow was edited or dispatched, and no VM/runtime resources were touched.

## Stop criterion

Do not approve until the existing candidate is conflict-free and ancestry-clean against current develop; the consent failures are either fixed or proven pre-existing by paired same-test, same-runtime-gate, same-configuration baseline evidence; and the final candidate has a terminal successful PR-triggered required-check result. Retain the relevant German coverage changes. A green docs/unit step does not override the failed `validate` job.

## END

END_BLOCKED 0427-131-review — KORREKTUR required; PR #1456 head `27ef90449be7ad53a4d6011ad90ff83b6c6f0ae5`, run `42460379046` failed in runtime integration.
