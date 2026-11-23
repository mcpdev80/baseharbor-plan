# Review mission m_rev_1620e8b

## PLAN

1. Read the mission, verify its authority, scope, acceptance contract, and required evidence location.
2. Refresh Planning ownership/task state and verify the exact GitHub remote, candidate, base, and provenance.
3. Inspect the candidate diff and exact-head hosted checks against each acceptance requirement.
4. Perform only the mission-authorized review or merge action; preserve unrelated work and record evidence.
5. Publish evidence in baseharbor-plan, verify origin/main and remote state, update the live board, and post the required handoff.

## Role and verdict

ROLE LABELS: ROLLE: REVIEW, followed by a MERGE attempt under the explicit Owner authorization from 2026-11-23 (“finish AND merge”). REVIEW: APPROVE the reviewed code and the base-neutrality finding. MERGE: BLOCKED by GitHub's active strict required-status check. No bypass or product change was made.

## Contract and authority

Task: `t-20261114-r28-cli2-wizard-platform` (0428-067), PR #1620. The task state was `blocked`; its recorded next trigger was the catalog-ingress card for `cmd/baha/app_access.go` and `cmd/baha/app_access_test.go`, followed by one hop and an exact run. The ingress card `t-20261123-catalog-ingress-app-access` is `closed` and records merge SHA `15c652136b0fce19dd0ae286b341b38cac3f7854`. The reviewed PR run uses base `e8acf740553f7218b259f4855f5b79f83f21ab6b`, which is confirmed to descend from that catalog-ingress change.

I read the Planning task note and Owner mission `/tmp/opencode/m_rev_1620e8b.md.g`. The mission authorizes review and a normal squash merge only if the candidate is neutral to the subsequent develop change. Workflow files were left untouched. I started no local product tests, workflow reruns, VM tests, or containers.

Before the first evidence commit, I verified the Planning remote. Exact `git -C baseharbor-plan remote -v` output:

```text
origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin https://github.com/mcpdev80/baseharbor-plan.git (push)
```

## Candidate and base neutrality

I identified `lane-origin` as the GitHub remote from URL `https://github.com/mcpdev80/baseharbor.git`. Fresh remote witnesses before and after the merge attempt:

```text
1b7598aef8c4cae33b77c8523872637090d0f2bf refs/heads/develop
ad5859916d54bfb218a4c04f1cd41de44df0bb62 refs/heads/w067-cli2-wizard-platform
ad5859916d54bfb218a4c04f1cd41de44df0bb62 refs/pull/1620/head
```

The PR head remains `ad5859916d54bfb218a4c04f1cd41de44df0bb62`; the current base is `1b7598aef8c4cae33b77c8523872637090d0f2bf`. GitHub Compare `e8acf...1b759` reports exactly one base commit, `1b7598aef8c4cae33b77c8523872637090d0f2bf`, “fix(0428-227): admit canonical footprint show on data-capabilities gate”, changing these five files: `cmd/baha/app_broker.go`, `cmd/baha/ci_integration_operator_enabled.go`, `cmd/baha/ci_integration_operator_enabled_test.go`, `internal/operatorauth/local_runtime.go`, and `internal/operatorauth/local_runtime_test.go`. The base-side diff contains no catalog or Trusted Plan file.

GitHub Compare `1b759...ad585` reports 10 candidate commits, one commit behind, and only two files in the PR diff: `cmd/baha/app_access.go` (+40/-0) and `cmd/baha/app_access_test.go` (+165/-1). `scripts/pr-gate-coverage.json` is not part of the candidate diff. Entries for both `app_access` paths are already present in the catalog at `e8acf` and `1b759`, with both atomic data-capabilities surfaces; the test entry has `runtime_specific: true`. The catalog delta is empty.

Neutrality: PASS. #1753 adds the `app.footprint.show` operation in `internal/operatorauth/local_runtime.go` and does not modify `app_access.go`, `app_access_test.go`, or the catalog. #1620 writes an audit event for `app.connection` after authorization succeeds and before credentials are emitted. These operations and paths have no file, gate, or catalog conflict; the base-side change does not conflict with the credential-reveal behavior. The exact PR run also uses `e8acf`, whose catalog ancestry already contains ingress for both paths from `15c652`.

## Exact-head checks and execution sample

Run `45099073208` is a pull-request run for exact head `ad5859916d54bfb218a4c04f1cd41de44df0bb62`, `completed/success`, attempt 1. Check `PR Selected Checks` (job `137452731937`, GitHub Actions integration `15368`) is `completed/success`; its terminal log line is `2026-11-23T02:38:35.5979705Z PR Selected Checks: PASS`. The log shows `trusted_base_sha` `e8acf740553f7218b259f4855f5b79f83f21ab6b` and selected runtime targets `atomic/docker/data-capabilities` and `atomic/podman/data-capabilities`.

Both required runtime jobs actually ran and succeeded: Docker job `137445999430` and Podman job `137445999443`, each `completed/success`. Each log contains `demo-data-capabilities       PASS`. Go unit job `PR · Go unit · cli-0` (`137445560998`) reports `PASS cli-0: 468 passed / 13 intentionally skipped / 481 discovered; CLI inventory total=1865`. The shard selector at the reviewed candidate assigns `TestAppCredsRevealWritesPerRevealAuditEvent` to `cli-0` (SHA-256 modulo 4); `TestAppCredsRevealFailsClosedWhenAuditWriteFails` maps to `cli-3`, whose job `137445560919` reports `PASS cli-3: 434 passed / 16 intentionally skipped / 450 discovered; CLI inventory total=1865`. The shard runner checks that every selected test ran and passed or was intentionally skipped; neither card-specific test is skipped. The native Docker/Podman execution for data-capabilities is evidenced in the two jobs above.

The PR Selected Checks selection is green, including Trusted Plan selection and both native data-capabilities runtime jobs. Other non-required or unaffected jobs in this run are `skipped`; they are not counted as passing.

## Merge attempt and required next action

Ruleset `25223521` `develop - required checks` was read live: `active`, `strict_required_status_checks_policy: true`, requires `PR Selected Checks` from integration `15368`, and has no bypass actor. Ruleset `23754541` `develop - integration branch` is `disabled`. PR #1620 remained `open`, `draft: false`, `mergeable: true`, `mergeable_state: behind`, base `e8acf...`, head `ad585...`.

I attempted a normal squash merge with expected-head guard `ad5859916d54bfb218a4c04f1cd41de44df0bb62`. GitHub rejected it with HTTP 405: `Repository rule violations found — Required status check "PR Selected Checks" is expected.` No bypass was used. The PR remains open and unmerged. The code-review verdict is approve, but merge is blocked by the active required-status check; the green old-base check does not satisfy the current strict-base condition.

Next action: hop #1620 once, monotonically, to current `develop` head `1b7598aef8c4cae33b77c8523872637090d0f2bf`, observe the PR Selected Checks run for the new exact head through terminal status, and use a normal squash merge only if the required check is green. Keep the existing candidate branch; do not edit workflow files or bypass the rule.

## Repo-rule compliance

Only this evidence file was created in the planning repository. This review session did not modify product files, `.github/**`, task metadata, or generated Planning views. No subagents, local product tests, workflow reruns, or containers were started. The only PR mutation attempted was the normal squash merge with expected-head guard; GitHub rejected it and the remote PR head and develop remained unchanged.

## cleanliness

Before review: `docker ps -a` (PID 3446891) showed only header `CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES` and no containers. After the merge attempt: `docker ps -a` (PID 3506035) showed the same header and no containers.

## END

END_BLOCKED codex-rev2-1736: REVIEW APPROVE; merge blocked by active strict PR Selected Checks status, final hop to develop `1b7598aef8c4cae33b77c8523872637090d0f2bf` required, candidate `ad5859916d54bfb218a4c04f1cd41de44df0bb62`.
