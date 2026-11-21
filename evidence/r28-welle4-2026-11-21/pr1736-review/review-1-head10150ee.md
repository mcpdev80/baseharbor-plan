# CODEX-REVIEW evidence

## PLAN

1. 1. Verify the exact remote head and terminal hosted run for PR #1736; abort that candidate on head drift.
2. 2. Review PR #1736 routing fail-open behavior, selected shard preservation, bidirectional fixtures, and five named diff-base cases with job-log durations.
3. 3. Record #1736 verdict, recipe, follow-up line, required END fields, and publish its Planning evidence.
4. 4. Verify the exact remote head and terminal hosted run for PR #1702; abort that candidate on head drift.
5. 5. Review PR #1702 production witness boundary, restored seams, negative case execution, and identity.
6. 6. Record #1702 verdict, recipe, required END fields, and publish its Planning evidence.

## Candidate and run identity

Remote witness from `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1736/head refs/heads/develop`:

```text
 d1acf3f31a360cd2a5e0ebaed1c70ccdd7957cf3 refs/heads/develop
10150ee7164bbc8767136e540eb966c3baab930b refs/pull/1736/head
```

PR #1736 is OPEN, non-draft, based on develop at `d1acf3f31a360cd2a5e0ebaed1c70ccdd7957cf3`, and has one commit. Its exact candidate head is `10150ee7164bbc8767136e540eb966c3baab930b`, parented directly on that base. GitHub commit metadata reports author and committer both Marcel Pfingstgräf (`mcpdev80`), one identity. The six changed paths are `scripts/pr-gate-coverage.json`, `scripts/pr-gate-plan.py`, `scripts/pre-release-integration.py`, `scripts/test_pr_gate_coverage.py`, `scripts/test_pr_gate_plan.py`, and `scripts/test_pre_release_integration.py`.

Hosted run `44940073029` is `pull_request`, exact head `10150ee7164bbc8767136e540eb966c3baab930b`, terminal `completed/success`. Final `PR Selected Checks` job `136959286024` completed success. The trusted-plan artifact SHA-256 is `89ff7a7292043e39d0d099747ddf10148c6d0ad9ca029e378561ccbb6e138caf`; its `pr-plan.json` SHA-256 (plan-sha) is `9b4a6fe5c488513d6f7abbfe4b1d39013de4065fad69be367201b33be37a7ab3`. The plan is resolved, not broad, and selects both `integration/docker/coreless-lifecycle` and `integration/podman/coreless-lifecycle`.

## Routing and registration behavior

The PR changes only the gate coverage catalog, planner routing, executor, and tests for those changes. The planner adds the environment-destroy command, implementation, integration test, machine-coverage row, generated CLI docs, and deployment-scope files to the Docker and Podman Coreless surfaces. It keeps registration-only changes unresolved without the complete implementation/test/docs/scope set (`scripts/test_pr_gate_plan.py:test_registration_paths_alone_remain_unresolved`). A complete candidate selects both runtime gates and CLI/deployment checks (`test_complete_env_destroy_candidate_selects_both_coreless_gates`). No unrelated script behavior was changed in the reviewed diff.

`TestEnvironmentDestroyNativeLifecycle` is registered as an optional case in the `application` shard, with a 12-minute command and its acceptance environment variable. It is included only when `cmd/baha/env_destroy_integration_test.go` exists and contains the named function (`scripts/pre-release-integration.py:91-111`). If the source file is absent, the optional command is omitted, the acceptance environment variable stays unset, and existing tests remain in the shard; that is a deliberate fail-open for this optional future test, not a fail-closed test requirement. The present-source fixture verifies registration exactly once in the application shard for both runtimes (`scripts/test_pre_release_integration.py:187-213`). The absent-source/current-checkout direction verifies the acceptance variable stays unset (`:109-129`) and the partition test omits unavailable optional cases while retaining the existing set (`:153-185`). A present source without the named function raises `ValueError` (`pre-release-integration.py:105-110`). Existing selected Coreless shards are otherwise unchanged.

Run `44940073029` executed eight selected shard jobs successfully: Docker `foundation`, `identity-backend`, `application`, and `core-capability`; Podman `foundation`, `identity-backend`, `application`, and `core-capability`. Each runtime therefore ran four selected shards; both runtime aggregate jobs and final `PR Selected Checks` succeeded. This is the full selected shard set shown by the run, not a claim that skipped unrelated matrix entries passed.

## Focused regression receipts

Job `136955169619` (`PR · Focused Python`) logged the command `python3 scripts/test_pr_diff_base.py`, then `Ran 24 tests in 1.347s` and `OK`. It did not log `no tests to run`. Source at the candidate contains the five requested fail-closed cases: `test_advanced_base_must_belong_to_fetched_target_branch`, `test_expected_integration_parents_with_modified_tree_is_rejected`, `test_head_missing_from_integration_still_fails_closed`, `test_third_parent_on_integration_still_fails_closed`, and `test_unavailable_fetched_target_tip_fails_closed`. The same file also contains `test_advanced_base_requires_exact_clean_integration_tree`, so the mission's shorthand “advanced-base” does not uniquely select one of two advanced-base tests.

The job proves that all 24 test methods in that script were run successfully as a suite, but the hosted log does not list individual test names or per-case durations. The requested per-case receipt is therefore absent; no individual duration can be asserted from this log. This is an owner-scope receipt finding because the missing detail is in the test/job receipt output under `scripts/**`, which this review cannot change.

## Verdict and correction recipe

REQUEST CHANGES: the candidate’s mapping and runtime routing are coherent, the optional test's absent/present behavior is covered, and both existing Docker/Podman selected shard sets ran successfully. The required per-case hosted receipt for the five named diff-base cases is missing, so the requested evidence is incomplete despite the successful 24-test aggregate.

Recipe: in the owner-scope receipt path for `scripts/test_pr_diff_base.py` / its CI job, emit each of the five exact test method names with its individual duration and pass result; disambiguate which advanced-base method is the historical regression case. Re-run the same focused Python job and record the exact-head job log. Stop if any named case is absent, skipped, or not green. No product or workflow changes were made by this reviewer.

Required follow-up: `next-proof: #1627 braucht nach diesem mapping den exakten docker/podman-nachweis`.

## Cleanliness

`docker ps -a --no-trunc` before, shell pid 3245933: eight existing `bh-itest-*` containers, all exited. After, shell pid 3246890: the same eight container IDs and statuses, all exited. This review started no containers or compose projects.

END codex-rev-1747 DONE — REQUEST CHANGES; head `10150ee7164bbc8767136e540eb966c3baab930b`; run `44940073029`; plan-sha `9b4a6fe5c488513d6f7abbfe4b1d39013de4065fad69be367201b33be37a7ab3`; identity: autoren=[Marcel Pfingstgräf].

## Planning remote

Output of `git -C /home/marcel/dev/baseharbor-ecosystem/workers/codex-rev-1747-plan-wt remote -v | head -n 1` before this evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.
