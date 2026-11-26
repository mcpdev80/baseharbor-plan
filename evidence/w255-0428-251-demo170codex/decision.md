# w255-0428-251-demo170codex — demo PR-event route decision

## PLAN

1. Read the assigned mission, coordinator policy, and current Planning task frontmatter.
2. Verify demo PR heads, run events/jobs, workflow contents on `main` and `develop`, and exact changed paths.
3. Decide the smallest test-only PR-event route for #170 first and #179 alongside #1842; record a file/line prescription and exact qualification bar.
4. Publish this review akte through the requested isolated Planning PR branch; preserve the shared checkout's unrelated work.
5. Capture the post-merge `git show` witness and origin/main evidence-path witness, then post the lane END.

## Visible candidate author block

Card frontmatter `owner` verbatim from `origin/main` (`tasks/t-20261123-demo-digest-consent-adaptation.md`): `Coordinator (merge 1450) / 9b7683b5`.

`git user.name`: `Coordinator (merge 1450) / 9b7683b5`

`git user.email`: `Coordinator (merge 1450) / 9b7683b5@baseharbor.local`

Literal commit invocation: `git -c user.name='Coordinator (merge 1450) / 9b7683b5' -c user.email='Coordinator (merge 1450) / 9b7683b5@baseharbor.local' commit -m 'evidence(w255): decide demo PR-event route'`

Pre-push author gate: `git show -s --format=%an HEAD` must print exactly `Coordinator (merge 1450) / 9b7683b5`.

## Decision

Use the existing `.github/workflows/pr-config-matrix.yml` `pull_request` workflow as the only test-only route. Keep the `develop` base filter. Update its path list to cover the actual test scripts changed by #179, and explicitly include `ready_for_review` as a pull_request activity so #179 can start a run when it leaves draft. Do not treat any push-event run as PR evidence. The dispatch-failed runs below do not identify a test failure or provide a step log; the missing PR check-suite must be qualified by actual PR-event runs after the workflow is eligible.

The census statement that the path filter alone explains #170's missing PR run is not supported by the observed path data. #170 changes `tests/config-matrix/run.sh`, already matched by `tests/config-matrix/**` on the `develop` workflow. The run inventory proves no PR-event run was recorded, but not why the matching trigger did not yield one. Therefore the route prescription keeps that existing match, makes workflow event types explicit, and requires the worker to confirm an actual `pull_request` run rather than assuming a path edit fixes #170.

## Worker prescription

In `mcpdev80/baseharbor-demo`, update `.github/workflows/pr-config-matrix.yml`:

- At lines 4–7, retain `pull_request` and `branches: [develop]`; set activity types to `opened`, `synchronize`, `reopened`, and `ready_for_review`. The last type is needed for the draft #179 readiness transition. The default PR activity list already covers the first three, so spelling them out makes the qualification events inspectable.
- In the `paths` block beginning at line 7, retain `tests/config-matrix/**` (line 14 in the current develop file) for #170. Add the four exact changed-path entries already present in the current main workflow: `tests/connectivity/run.sh`, `tests/full-destroy/run.sh`, `tests/policy/operator-test-certificate.sh`, and `tests/reconciliation/run.sh`. Current main has them at lines 14–17; current develop omits them. This is the smallest path change for #179's actual diff and avoids starting the config matrix for unrelated demo paths.
- Keep the route test-only. No auth or consent behavior changes are part of this decision. The workflow change belongs in the local worker's authorized PR write-set; this review makes no demo repository edits and triggers no demo runs.

Priority and qualification:

1. **#170 first.** It is OPEN and non-draft at head `b086cf58bb2f7aafee30edf52ac4b8199daf7d0d`. Its changed path is already selected. After the trigger definition is present on the base/default workflow source, a real PR `synchronize` event on the exact candidate head must produce a successful `pull_request` run with at least one executed successful check job. Then obtain the second distinct run ID on that same exact head with the coordinator-authorized close/reopen sequence. Record both IDs, events, head SHA, job names and conclusions.
2. **#179 alongside #1842.** It is DRAFT at head `cda6aa70e80bec1a1db06d85decdd8833cb63994`; do not count its existing push run. Land the route in the assigned test-only change, coordinate the fixture work with #1842, and make the PR ready only when its owner says the fixture candidate is ready. The `ready_for_review` event must produce the first executed run after the trigger is available. Obtain a second distinct run ID on the identical head with the close/reopen sequence. Both must be `pull_request`, SUCCESS, and contain at least one actually executed successful check job.

For both PRs, skipped jobs, a workflow-level or dispatch failure, a push event, a missing run, or a run on any older/different head is unqualified. The existing failures are state only: workflow `.github/workflows/pr-config-matrix.yml`, run `45663390190` for #170 and `45688177820` for #179, each `event=push`, `conclusion=failure`, `jobs=[]`. The logs endpoint returned HTTP 404 and no jobs or steps exist, so there is no failing step log line to quote. Treat them as dispatch failures, not failed tests. This akte does not authorize any demo merge; the mission's owner-listed prerequisites remain mandatory.

## Source witnesses

Planning repo remote identity was checked before the evidence write:

```text
origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin  https://github.com/mcpdev80/baseharbor-plan.git (push)
```

Planning base was `origin/main` at `5590aaabf9deb75ec3967396cfc20c9b2d5c522f` when the isolated branch was cut. Demo branch tips at census time:

```text
5ca92a7cd2f746934890cfd7096a48068bdf218e refs/heads/develop
2618b3962330509add5bf265522995da2a9034ce refs/heads/main
```

PR views confirmed #170 OPEN/non-draft on `develop`, head `b086cf58bb2f7aafee30edf52ac4b8199daf7d0d`; #179 OPEN/draft on `develop`, head `cda6aa70e80bec1a1db06d85decdd8833cb63994`. Both review lists and reviewDecision were empty.

The census input is `evidence/verify/w253-demo170179-census.md` at `0766f05e`. It records only run `45663390190` for #170 and `45688177820` for #179; both were push events, failed immediately, and had empty jobs. `/pulls/170/runs` returned 404. The jobs endpoints returned empty arrays and logs returned 404.

The develop workflow's current path block has `tests/config-matrix/**` at line 14 and does not include the four #179 paths. The main workflow contains `tests/connectivity/run.sh` at line 14, `tests/full-destroy/run.sh` at line 15, `tests/policy/operator-test-certificate.sh` at line 16, and `tests/reconciliation/run.sh` at line 17. PR #170 changes only `tests/config-matrix/run.sh`; #179 changes the four listed scripts. See [develop workflow](https://github.com/mcpdev80/baseharbor-demo/blob/5ca92a7cd2f746934890cfd7096a48068bdf218e/.github/workflows/pr-config-matrix.yml#L4-L17) and [main workflow](https://github.com/mcpdev80/baseharbor-demo/blob/2618b3962330509add5bf265522995da2a9034ce/.github/workflows/pr-config-matrix.yml#L3-L19).

GitHub documents that `pull_request` defaults to `opened`, `synchronize`, and `reopened`; `ready_for_review` must be explicitly selected. It also documents that path and branch filters are jointly required and that a filtered workflow does not run when no changed path matches: [Events that trigger workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows) and [Triggering a workflow](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow).

## Candidate provenance and delivery

Exact fetched `origin/main` SHA for the branch cut: `5590aaabf9deb75ec3967396cfc20c9b2d5c522f`. Before commit, verify it is an ancestor of the commit. `git diff origin/main...HEAD --name-only` must show only this evidence file, and `git log --oneline origin/main..HEAD` must show only this lane's evidence commit. After pushing, record `git ls-remote` for the PR head and branch. Keep the evidence PR limited to this akte.

Post-merge witness and exact `origin/main` tree-path output will be appended here before the final END post.

## cleanliness

No Docker/Podman containers or compose projects were started. No product/demo checkout or product file was written. No local tests were run. The shared Planning checkout's unrelated modified and untracked files were left untouched.

## END

END DONE w255-0428-251-demo170codex: decision recorded and evidence PR delivered; candidate SHA pending.

### Verified candidate ancestry before publication

`git merge-base --is-ancestor 5590aaabf9deb75ec3967396cfc20c9b2d5c522f HEAD` exited 0 before the first commit. The first commit is `0116aa684` and its author gate output was exactly `Coordinator (merge 1450) / 9b7683b5`.

First-commit diff path:

```text
evidence/w255-0428-251-demo170codex/decision.md
```

First-commit log from the fetched base:

```text
0116aa684 evidence(w255): decide demo PR-event route
```

All listed branch commits are this evidence akte; no foreign candidate is included.
