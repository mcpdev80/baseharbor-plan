# Demo PR gate availability disposition — #179 and #170

## PLAN

1. Verify Demo default branch, workflow presence on main/develop, the two PR heads, their changed paths, and the prior failed run event/job census.
2. Choose the smallest test-only workflow change that makes the existing PR gate available on the default branch and selects the changed Demo acceptance gates for the two PRs.
3. Record the card owner, product commit identity, literal commit command and pre-push author gate before creating the product branch.
4. Add the workflow to Demo main with exact fixture paths and changed-path-to-gate selection; do not change product auth or consent behavior.
5. Open a PR to Demo main, wait for its real Hosted pull_request checks, and merge normally if the checks and review pass.
6. After main contains the workflow, trigger pull_request events for #179 and #170 and record exact run IDs, job execution and outcomes.

## Scope decision

The test-only workflow availability and routing change belongs in the existing 0428-284 demo fixture-gate context. No new card is needed. The current owner instruction explicitly delegates test-only workflow provisioning in-context; this scope excludes product authentication, authorization and consent semantics.

The minimal implementation is one file, `.github/workflows/pr-config-matrix.yml`, on Demo's default branch `main`. Preserve the current `pull_request.branches: [develop]` trigger and existing path filters. Add the four exact #179 paths:

- `tests/connectivity/run.sh` -> `connectivity`
- `tests/full-destroy/run.sh` -> `full-destroy`
- `tests/policy/operator-test-certificate.sh` -> `policy`
- `tests/reconciliation/run.sh` -> `reconciliation`

The existing `tests/config-matrix/**` path already selects #170's `tests/config-matrix/run.sh` -> `config-matrix`. In the workflow job, compute changed paths from the PR base/head SHAs and pass only the corresponding named gate(s) to the existing `scripts/acceptance.sh`; preserve `config-matrix` as the fallback for the workflow's existing non-gate-specific trigger paths. This makes #179's fixture scripts actually execute instead of merely starting an unrelated config-matrix run.

## Fresh source witnesses

- Planning remote: `origin https://github.com/mcpdev80/baseharbor-plan.git` (fetch and push).
- Plan branch base: `75bbbb24c34342e8812c47a240cfc01d7e977474` (origin/main at evidence creation).
- Demo remote: `https://github.com/mcpdev80/baseharbor-demo.git`.
- `git ls-remote` returned Demo `refs/heads/main=6381a67f58e067358ef54dce7f4cff2106f8a623` and `refs/heads/develop=5ca92a7cd2f746934890cfd7096a48068bdf218e`.
- Demo default branch API: `main`.
- `.github/workflows/pr-config-matrix.yml` on `develop`: blob `7108cf69e4f53164f83faa8dc13ae51ec25e291d1`; on `main`: HTTP 404.
- #179: base `develop`, draft, head `cda6aa70e80bec1a1db06d85decdd8833cb63994`; changed files are the four paths listed above.
- #170: base `develop`, ready, head `b086cf58bb2f7aafee30edf52ac4b8199daf7d0d`; changed file `tests/config-matrix/run.sh`.
- Prior runs `45688177820` on #179 and `45663390190` on #170 were event `push`, conclusion `failure`, and each had zero jobs; neither is PR-event evidence.
- Existing workflow executes `bash scripts/acceptance.sh config-matrix`; the acceptance script supports multiple positional gate IDs and `DEMO_ATOMIC_GATE=1`. The new exact path mapping will call the corresponding named acceptance gates for #179 and retain `config-matrix` for #170.

## Ownership and commit identity block

- Card owner VERBATIM from plan `origin/main`: `w198-0428-284-demo-parser`.
- Product candidate commit identity under the owner admission rule: `user.name=w198-0428-284-demo-parser`; `user.email=w198-0428-284-demo-parser@baseharbor.local`.
- Literal product commit invocation: `git -c user.name='w198-0428-284-demo-parser' -c user.email='w198-0428-284-demo-parser@baseharbor.local' commit -m 'ci(demo): route fixture gates on pull requests'`.
- Product pre-push gate: `git show -s --format=%an HEAD` must print exactly `w198-0428-284-demo-parser`.
- Planning evidence author: `user.name=w136-pr1836-rowsreview`; `user.email=w136-pr1836-rowsreview@baseharbor.local`.
- Literal evidence commit invocation: `git -c user.name='w136-pr1836-rowsreview' -c user.email='w136-pr1836-rowsreview@baseharbor.local' commit -m 'docs(evidence): record Demo PR gate availability plan'`.
- Evidence pre-push gate: `git show -s --format=%an HEAD` must print exactly `w136-pr1836-rowsreview`.

## Planned verification and acceptance

The bootstrap PR targets `main`; the existing default-branch `pr-guided-consent.yml` workflow is the Hosted PR-event check for that PR. After the workflow lands on `main`, reopen #179 and #170 to emit actual `pull_request` events without changing either PR head. Accept evidence only for exact current heads and event `pull_request`; record whether the `Config Matrix · full config-matrix acceptance` job actually executed the corresponding gate(s), its final conclusion, and any skipped/unavailable job. Do not count prior push failures as evidence.

No product files, consent semantics or auth behavior are in the planned write set. No local runtime test is planned; Hosted GitHub Actions is the durable CI evidence.
