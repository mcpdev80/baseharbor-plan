# REVIEW verdict — PR #1725 / 0428-201

## PLAN

1. Read the mission and required coordinator/repository policies; capture role, contract, and evidence path.
2. Refresh task ownership and verify the exact remote PR head/base, diff scope, and ancestry.
3. Review the exact candidate against each acceptance criterion and inspect required hosted checks.
4. Write the verdict and supporting evidence in baseharbor-plan, preserving unrelated work.
5. Publish evidence, verify remote witnesses, update the live board, and post the required handoff.

## ROLE: REVIEW

Session/model/backend: Codex review session; GPT-6.2; backend identity is not exposed by this interface.
Review time: 2026-11-23 02:19 UTC.
Task: 0428-201, `t-20261120-shared-backend-state-version-message`.
Evidence path: `evidence/r28-welle5-2026-11-22/shared-backend-0428-201/review-merge-1725-3d32bc489.md`.

## Candidate and provenance

PR #1725 is open, ready for review, and reports mergeable. The exact PR head is `3d32bc489646023b9e3a7460bbd9b62e96163e48`; the requested base is `develop` at `e8acf740553f7218b259f4855f5b79f83f21ab6b`.

Remote witness from `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/pull/1725/head`:

```text
e8acf740553f7218b259f4855f5b79f83f21ab6b refs/heads/develop
3d32bc489646023b9e3a7460bbd9b62e96163e48 refs/pull/1725/head
```

The GitHub compare for base `develop` and head `3d32bc489646023b9e3a7460bbd9b62e96163e48` reports merge base `e8acf740553f7218b259f4855f5b79f83f21ab6b`, `ahead_by=29`, `behind_by=0`. Thus the exact requested base is an ancestor of the candidate.

Changed paths and numstat from the exact PR compare:

```text
internal/application/shared_backends.go             +32
internal/application/shared_backends_state.go        +1/-1
internal/application/shared_backends_test.go         +100
```

Three changed files, 133 additions and 1 deletion. No catalog or workflow file is changed; no separate new test file appears in the PR diff. The catalog delta is empty by the compare's changed-file list.

## Content review

The failure now returns `SharedBackendStateVersionMismatch{Found, Expected}` and the error text names the found and supported versions, describes the upgrade-from-outside condition, and directs the operator to upgrade the shared-backend provider. The version check still returns an error before any write. The test `TestSharedBackendStateLoadReportsVersionReason` writes v2 JSON, calls `loadSharedBackendState`, checks the typed version reason, and compares the file bytes before and after. The other moved tests are `TestSharedBackendStateVersionMismatchNamesVersions`, `TestSharedBackendStateVersionMismatchIsDistinguishableFromCorruption`, and `TestSharedBackendStateCorrectVersionStillLoads`.

Content sample passes the requested message, distinct-error, and fail-closed checks. However, the load regression calls the internal loader directly; it does not exercise the real command surface specified in acceptance criterion 3.

## Hosted checks

Exact workflow run: `45096961182`, completed, conclusion success, associated with candidate artifact `3d32bc489646023b9e3a7460bbd9b62e96163e48` and trusted base `e8acf740553f7218b259f4855f5b79f83f21ab6b`.

The `PR Selected Checks` aggregate job `137444792357` ended with `PR Selected Checks: PASS`. Its own log reports `UNIT_SCOPE: none` and `UNIT_RESULT: skipped`. The corresponding completion assertions accept this as a skip because the unit scope is none. The successful selected runtime job `137439201438` executed the Podman `data-capabilities` runtime gate, but that journey does not execute the moved Go unit tests. Therefore the required owning shard did not execute this regression on the exact head. Per policy, skipped is not a pass.

## Verdict

**BLOCKED — DO NOT MERGE.** The explicit hosted test requirement is unmet: the owning Go unit shard is skipped (`UNIT_SCOPE: none`, `UNIT_RESULT: skipped` in run 45096961182), and the current regression does not meet acceptance criterion 3's real command-surface requirement. The green Podman runtime check and aggregate do not substitute for either condition. No merge action was taken.

## Implementer recipe

- In the same PR, make the regression exercise the real command surface that loads the v2 state and assert the specific version mismatch reaches the user while the state bytes remain unchanged.
- Ensure the test is selected and actually executed by its owning hosted check for changes to `internal/application/shared_backends_test.go`; do not rely on the Podman journey or a skipped Go shard.
- Run the resulting exact-head hosted checks and hand off only when the owning shard actually executes the test with zero failures. Stop if satisfying this requires a shared base planner/required-plan change outside this card's write set; report that exact owner-owned file and line.

## repo-rule compliance

Review was read-only against the product repository. No product files, workflows, branch refs, or PR metadata were changed. No product test command was run. No containers or compose projects were started on this host. The planning repository remote was verified before evidence publication:

```text
origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin https://github.com/mcpdev80/baseharbor-plan.git (push)
```

## cleanliness

Before review, `docker ps -a` ran with shell PID 3292479 and returned only the header, with no containers. No containers were started; no compose project was created. After review, the same command returned only the header, with no containers.

## Evidence delivery

Planning repo current HEAD before this evidence edit was `8ad6b4443d885f4d12392c3a212ab96ea0d69f62`; `origin/main` resolved to the same SHA before publication. This mission's evidence is confined to the planning repository.

END_BLOCKED codex-rev2-1736: PR #1725 cannot merge until the owning hosted Go shard executes the regression and the regression uses the real command surface; candidate `3d32bc489646023b9e3a7460bbd9b62e96163e48`.

After-review cleanliness witness: shell PID 3298290; `docker ps -a` returned the header only (no containers). Planning validation: `python3 scripts/plan.py render && python3 scripts/plan.py check` completed with 0 errors and 11 existing warnings; `git diff --check` passed; evidence checkbox scan was clean.
