# REVIEW / MERGE record: PR #1765 exact head

## PLAN

1. Read the mission, coordinator authorization, and task contract; record the authorized review and merge scope.
2. Verify the real GitHub remotes, exact PR head and base, ancestry, and changed-file set.
3. Review the candidate diff against card 0428-209 and inspect the exact hosted run and gate logs.
4. Record the verdict, merge result, any acceptance evidence gap, and cleanliness witnesses.
5. Publish this record to baseharbor-plan origin/main, verify its remote presence, and post the handoff.

## Mission and authorization

Mission: `/tmp/opencode/m_rev_1765.md.g`. Task: `t-20261121-native-cell-operator-seam`, card 0428-209. Mission role was REVIEW, followed by MERGE only for an approved exact candidate with the required checks green. The mission's specific binding criterion required evidence that the changed tests execute in the native data-capability gates. The workspace policy files COST_CONTROL.md and GITHUB_AUTHORITY.md were read before the merge action in the prior review pass.

## Provenance and candidate

Product remote resolved to `https://github.com/mcpdev80/baseharbor.git`. The planning repository is `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`; its verified remote was `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and the corresponding push URL is the same.

Base before merge: `c6a7138ce2bf7de88f45f2a68e5168c835601a16` (`develop`). Candidate head: `c8bbb0f5232b9725d750a1eca9efac238a9e221a` (PR #1765). The pre-merge remote witness showed those exact values for `refs/heads/develop` and `refs/pull/1765/head`. GitHub compare reported the candidate based directly on the stated develop SHA, with seven commits ahead and zero behind; merge-base was the base SHA. This was a develop-based candidate, not a stacked foreign PR head.

The exact candidate diff contained only:

- `cmd/baha/control_plane_single_native_ci_test.go` (+7 lines)
- `cmd/baha/runtime_integration_test_support_test.go` (+43/-22 lines)

No production implementation, catalog file, or `.github/**` file changed in the PR. The source test path was cataloged on the base at `scripts/pr-gate-coverage.json:1855-1862`, with runtime-specific coverage for Docker and Podman data-capability surfaces. The catalog entry was already present at the base and byte-identical in the candidate; no catalog edit was needed in this PR.

## Review findings

The focused test change registers the bootstrap Target before selection. In the test helper, `target create` is invoked through the existing `runWithIOAsTestOperator` seam, and `BASEHARBOR_TARGET` is set only after successful creation. The control-plane native CI test sets the target and checks the effective target name and provider. The diff stayed within the task's allowed test-only write set and did not alter production enforcement.

The task card was `review` before the merge and required `TestControlPlaneSingleDefaultNativeRuntimeInCI` to pass in the native Keycloak/Core cell. The exact test was observed passing in `PR · Native Keycloak/Core · podman`, job `137408210664`, in run `45087109688`. The test output showed the named test executing and passing.

Acceptance evidence gap: the mission additionally required the changed tests to be shown executing in the native data-capability gates. Docker and Podman data-capability jobs `137408195963` and `137408195996` both completed successfully, but the inspected logs showed `TestApplicationCapabilityLifecycleExistingCore`, not the new test identifiers `TestControlPlaneSingleDefaultNativeRuntimeInCI` or `TestRuntimeIntegrationBootstrapTargetSelectsAfterCreate`. Therefore these logs do not prove that the changed tests themselves ran in those data-capability cells. The exact named control-plane test did run in the Native Keycloak/Core Podman cell, which satisfies the task card's stated test binding, but it does not satisfy the mission's stronger data-capability binding requirement. This is a material qualification; the green aggregate alone does not close it.

Other hosted evidence in the exact run: `PR Selected Checks` run `45087109688` completed SUCCESS for head `c8bbb0f5232b9725d750a1eca9efac238a9e221a`. The terminal aggregate was check-run `137416707967`. The six selected native matrix jobs (Docker and Podman coreless, data-capabilities, and guided) succeeded. Policy, planner, source-contract, Go unit shards, and build/static jobs also succeeded. Targeted HA Docker and Podman jobs were skipped, as were unrelated release jobs; skipped jobs are not counted as passes. No required check was bypassed.

Active ruleset `25223521` required `PR Selected Checks` from GitHub Actions integration `15368`; bypass was `never`. No review approval was submitted. The v0.4.27 tag predated the merge, satisfying the release ordering rule.

## Merge and remote witnesses

The prior review action merged PR #1765 with the mission-authorized squash method and expected head `c8bbb0f5232b9725d750a1eca9efac238a9e221a`. GitHub returned `merged: true` and merge SHA `b9e69b14a7c8c7e1ccf9176b0762bacecdecee5e`.

Fresh remote witness after merge:

```text
b9e69b14a7c8c7e1ccf9176b0762bacecdecee5e refs/heads/develop
c8bbb0f5232b9725d750a1eca9efac238a9e221a refs/pull/1765/head
```

The PR was closed and merged. No force push or protection bypass occurred.

## Verdict and follow-up

The merge is complete and the task-card test binding passed in the named Native Keycloak/Core Podman cell. However, the mission's stronger requirement to prove execution of the changed tests in both native data-capability cells is not demonstrated by the inspected job logs. Record this as a CI binding finding: make the changed tests reachable from the Docker and Podman data-capability gates, or amend the binding contract if the intended route is the Native Keycloak/Core cell, then capture named test output from an exact-head run. This record does not claim that the data-capability jobs executed those two changed tests.

Verdict for the mission's strict data-capability proof criterion: BLOCKED / qualification required after merge. The requested merge action was already performed before this qualification was identified; it cannot be represented as an unconditional approval against that criterion. Candidate merge SHA: `b9e69b14a7c8c7e1ccf9176b0762bacecdecee5`.

## Repo-rule compliance

Evidence is stored only in baseharbor-plan. Product files and `.github/**` were not edited by this review. No local product tests were run. The reviewer did not modify the candidate or submit a self-approval. Changes to planning state follow the repository's card-status workflow. No markdown checkbox lines are used in this evidence file.

## cleanliness

`docker ps -a` before and after review showed only the table header and no containers. This session started no containers or compose projects. Planning worktree status before writing this file had only unrelated untracked evidence files; those files were left untouched.

## END

END_BLOCKED codex-rev2-1736: PR #1765 is merged at `b9e69b14a7c8c7e1ccf9176b0762bacecdecee5`, but mission-required proof that the changed tests ran in the native data-capability cells is missing from their inspected logs.
## Origin main evidence-path witness

Exact output of `git ls-tree -r --name-only origin/main | grep <evidence-path>` after fetch:

```text
evidence/r28-welle5-2026-11-22/testctx-0428-223/review-merge-1765-c8bbb0f52.md
```
