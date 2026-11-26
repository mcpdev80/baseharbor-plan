# w200-cancelgroup-befund

## PLAN

1. Inspect the three cited findings and their source evidence, checking exact run states, cleanup details, and workflow scope from primary records.
2. Decide for each finding whether to extend an existing card, create no card, or recommend a new card; do not create coordinator cards.
3. Write the exact one-line Owner ask for each finding that needs an Owner-owned workflow change.
4. Publish the findings table and asks in an evidence akte on baseharbor-plan origin/main and report END_DONE.

## Visible owner and commit ansatz

Existing card selected for finding 1: `core-893-ci-enforce-selected-pr-checks.md`, exact frontmatter owner from origin/main at runtime: `owner: mcpdev80 (session 1)`.

Evidence commit identity: `w200-cancelgroup-befund`; email: `w200-cancelgroup-befund@baseharbor.local`.
Literal commit form: `git -c user.name=w200-cancelgroup-befund -c user.email=w200-cancelgroup-befund@baseharbor.local commit -m 'evidence(w200-cancelgroup-befund): disposition CI cancellation findings'`.
Pre-push author gate: `test "$(git show -s --format=%an HEAD)" = w200-cancelgroup-befund`.

## Scope and base

Planning repository remote verified before evidence work: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.
Evidence worktree cut from `origin/main` at `b1ac80ed040cc00ac25d35b65207b2a7f02f80f9`. No product branch or product file was changed. No workflow was edited or dispatched.

## Findings and dispositions

| Finding | Evidence and decision | Card disposition | Owner ask |
| --- | --- | --- | --- |
| Core PR run cancellation, stale run 45680881740 | w210 akte `evidence/2026-11-shift/0428-263/w210-0428-263-pr1846-hop.md` records the stale same-ref run remaining queued/in progress until manual cancellation of job 139441794922, while the exact-head attempt had zero jobs. GitHub run 45680881740 is now terminal `cancelled`; the job completed successfully at 19:20:25Z, and the run ended 19:20:36Z. This supports the operational finding that `cancel-in-progress` did not release the stale run in time. | Extend/reopen existing `core-893` (`owner: mcpdev80 (session 1)`), which owns PR capture/orchestration and the required final check. Do not create a new card. `core-896` explicitly excludes #893 orchestration files. | “Please investigate and correct the `ci-github.ref` concurrency behavior so a superseded same-ref run is cancelled and releases the group before the exact-head PR run is queued, while preserving the required `PR Selected Checks` result.” |
| #1842 run 45674221284, alleged eight-minute cleanup-cap kill | Run was `workflow_dispatch` on develop SHA `3a2ae6b1139570c98b8924e3b19975c56a289400`, completed failure. Docker policy job 139422945142 and Podman policy job 139422944976 each ran about nine minutes and ended `failure`, not `cancelled` or timed out. Both jobs show `Run runtime gate` failed; diagnostics, assertion-display, and cleanup steps succeeded. The accessible aggregate failure log reports both runtime results as failure and `Require both runtime matrices`; it does not establish that cleanup terminated either runtime process. | No new card or card extension on this evidence. Record as a failed runtime-gate state; the specific causal claim “cleanup cap killed two policy jobs” is unproven and should not be converted into implementation scope without a log identifying termination. | “Please verify from the complete run/job logs whether the eight-minute cleanup cap terminated either #1842 runtime job; if confirmed, identify the responsible workflow step and correct the cap/ordering.” |
| Demo `pr-guided-consent.yml` base-branch gap | w136 `w136-179-gate-disposition.txt` reports #179 at `cda6aa70e`; `pr-guided-consent.yml` accepts pull requests targeting `main` only. The same source says draft `pr-config-matrix.yml` path filters match none of the four fixture files and push run 45688177820 is a workflow-file artifact, not qualifying validation. Existing task `t-20261104-r27-demo-guided-consent` is closed, targets demo PR #128 and implements product harness behavior, so it does not own this workflow routing gap. | No matching active demo-CI card found in the origin/main task inventory; no new coordinator card. Keep #179 unqualified for merge until an executable exact-head PR check exists. | “Please add `develop` to the `pull_request.branches` filter in baseharbor-demo `.github/workflows/pr-guided-consent.yml`; this resolves the base-branch gap, while #179 still needs a workflow whose path filter actually matches its four fixture files.” |

## Exact source notes

Run 45674221284 aggregate failure excerpt: `Require both runtime matrices`; `DOCKER_RESULT: failure`; `PODMAN_RESULT: failure`; `Process completed with exit code 1`. The failed jobs were not reported as cancelled by the GitHub job API, and their cleanup steps completed successfully.

The referenced `.github/**` changes remain Owner-owned. This lane made no such change and did not trigger a rerun or dispatch.

## END w200-cancelgroup-befund DONE

Evidence publication path: `evidence/2026-11-shift/cancelgroup/w200-cancelgroup-befund.md`.
