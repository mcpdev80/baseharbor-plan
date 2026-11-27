# Independent exact-head review: baseharbor-demo PR #183 r10

## PLAN

1. Refresh baseharbor-demo and Plan remotes; verify PR #183 exact head/base, card owner, r10 akte, and hosted run witnesses.
2. Inspect only the two assigned r9 findings at SHA `4e285efb6d3b50c57432fe8d878e2c402249e055`: final-drain seam/reconciliation and hook-before-captures/exactly-once/log-equivalence/AST negative-control tests.
3. Record the independent exact-head verdict and any file:line correction recipe. Merge PR #183 only if both findings and the required gates pass.
4. Since the findings remain unresolved, leave PR #183 open, publish this review through an isolated Plan PR, render/check, and report CHANGES without closing card 0428-284.

## Visible commit identity block

Exact per-card frontmatter owner fetched verbatim from Plan `origin/main` `5878bd2a010a230e08ed9cd7726ebe2a7848fc27`: `owner: w267-0428-284-pridentity`.
Git user.name: `w267-0428-284-pridentity`.
Git user.email: `w267-0428-284-pridentity@baseharbor.local`.
Literal invocation: `git -c user.name=w267-0428-284-pridentity -c user.email=w267-0428-284-pridentity@baseharbor.local commit ...`.
Pre-push author gate: `git show -s --format=%an HEAD` must equal `w267-0428-284-pridentity` exactly.

## Provenance and current witnesses

- Planning repository remote, verified before branch creation: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.
- Exact Plan branch base to cut from: `origin/main` `5878bd2a010a230e08ed9cd7726ebe2a7848fc27`, confirmed by `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main`. This base is independent of the product candidate.
- Product remote verified as `origin https://github.com/mcpdev80/baseharbor-demo.git` (fetch/push). Fresh `git ls-remote` returned `58ac70679efe5f7e95bd47d602841704fb9ffa67 refs/heads/develop` and `4e285efb6d3b50c57432fe8d878e2c402249e055 refs/pull/183/head`.
- `git merge-base --is-ancestor` succeeded for exact `develop` `58ac70679efe5f7e95bd47d602841704fb9ffa67` and PR head `4e285efb6d3b50c57432fe8d878e2c402249e055`.
- Exact `git diff develop...head --name-status`: modified `tests/guided/drive.py`; modified `tests/guided/test_consent_capture.py`. No workflow or product files are changed.
- PR #183 is OPEN, non-draft, base `develop`, branch `w366-0428-284-democonsent`, head `4e285efb6d3b50c57432fe8d878e2c402249e055`, mergeable/CLEAN. The PR status-check rollup is empty.
- Run [46034033798](https://github.com/mcpdev80/baseharbor-demo/actions/runs/46034033798) is terminal SUCCESS, event `workflow_dispatch`, exact head above; its executed job `Guided consent · production-path regressions` succeeded.
- Run [46034015065](https://github.com/mcpdev80/baseharbor-demo/actions/runs/46034015065) is terminal FAILURE, event `push`, same exact head, zero jobs; it is not a test receipt. The worker akte records why a `pull_request`-context run cannot trigger for this `develop`-base PR under the workflow filter. I did not trigger a rerun, dispatch, close/reopen, or workflow change.
- Implementer r10 akte on Plan main: `evidence/2026-11-27/0428-284/pr183-r10-w392.md`, main commit `d70ad9809`; it records the run result and the attempted pull-request-context investigation.

## Verdict: CHANGES

### Finding 1 — no demonstrated log/capture divergence or reconciliation repair

At `tests/guided/drive.py:373-388`, the main loop reads one PTY `chunk`, writes that same chunk to the log, appends its decoded content to `capture_buffer` when capture is enabled, then increments `bytes_read`. The final-drain loop follows the same invariant at `:436-463`: it writes the read chunk to the log, appends that same chunk to `capture_buffer`, and increments `bytes_read`. The reconciliation call at `:505-509` runs after these increments and asks for `log[bytes_read:]`; the code shown does not establish that any logged chunk is absent from capture or unaccounted by `bytes_read`. The hook at `:480-482` observes a chunk after the same capture append; it does not create a divergent source.

The r10 comments at `drive.py:446-458` and `:464-504` claim append-before-advance creates an independent divergence, but the statements occur sequentially for one already-read chunk: the chunk is appended to capture and then its byte count is advanced. That ordering leaves no demonstrated missing log tail for `reconcile_capture_from_log` to repair. The test proves ordinary log/transcript equivalence, not a divergent final-drain repair.

Correction recipe: remove the unsupported claim that the real PTY path yields log-only bytes, or introduce a deterministic seam at the actual capture/reconciliation boundary that creates a missing capture suffix while retaining the authoritative log; assert the reconciliation appends that suffix exactly once. Keep the test tied to `run_tty`'s real final-drain/reconciliation path, rather than only testing a synthetic helper input.

### Finding 2 — the hook is installed but its observation is not asserted

At `tests/guided/test_consent_capture.py:933-936`, the test installs `_run_tty_final_drain_hook` before the two `run_capture` calls. It then asserts digest presence/exactly-once at `:942-947`, log equivalence at `:964-974`, and an AST shape check at `:1023-1024`. However, `drained["final_drain_chunks"]` is never asserted nonempty and no captured chunk is checked for the digest. The test itself says at `:1010-1014` that it intentionally does not assert final-drain membership because the digest is in the main-loop path. Therefore the hook-order correction is present, but the hook is not evidence that the final-drain seam handled the digest.

The asserted transcript/log conditions cover the main-loop path as well: `drive.py:373-387` already captures those chunks. Consequently the negative-control explanation at `test_consent_capture.py:993-1004` is not demonstrated by these runtime assertions: dropping final-drain handling would not drop a digest already captured by the main loop. The AST assertion proves source structure only, not runtime reconciliation or exact-once behavior of a final-drain tail.

Correction recipe: either add a deterministic reachable test seam that routes a digest-bearing tail through the final-drain/reconciliation path and assert the hook observed it plus exact-once transcript/log equality, or narrow the test's stated guarantee to the main-loop transcript path and add a separate direct, meaningful test for the final-drain/reconciliation invariant. Do not describe an unused hook or AST shape check as a runtime negative control.

### Additional hygiene observation

`git diff --check develop...head` reports `tests/guided/drive.py:810: new blank line at EOF`. This is not the basis of the CHANGES verdict, but should be removed during the next candidate update.

## Gate state and disposition

The exact-head workflow-dispatch test job is green, but the PR has no `PR Selected Checks` rollup and no required aggregate receipt. The mission's recorded structural workflow-filter limitation remains a gate limitation; the successful single dispatch job does not establish a complete PR Selected Checks pass. Independently, the two assigned static-review findings are not resolved, so I did not merge PR #183 and did not close card 0428-284.

## Repo-rule compliance

- Read-only inspection of the exact remote product head and base; no product edits, tests, reruns, dispatches, close/reopen operations, or merge.
- Evidence file is isolated in a Plan clone. No shared Plan checkout was modified.
- No containers or test VMs were started.

END_BLOCKED w267-0428-284-pridentity: PR #183 head 4e285efb6 remains CHANGES; log/capture divergence and runtime final-drain observation are unproven, so no product merge or card closeout.

## Plan publication blocker

- In this isolated Plan clone, `python3 scripts/plan.py render && python3 scripts/plan.py check` completed with `784 tasks, 7 epics, 13 releases, 24 decisions; 0 errors, 10 warnings`.
- Rendering exposed pre-existing generated-view drift outside the 0428-284 review write-set: `views/overview.md:73` and `views/releases/v0.4.28.md:337` still show owner `w397-0428-307-idfallback`, while the canonical task `tasks/t-20261125-hunt42-timeout-constant-matrix.md` on current Plan main assigns `w400-0428-315-timeoutsfix`. The required Hosted Plan workflow runs `python3 scripts/plan.py check` directly (`.github/workflows/validate.yml:24-27`), so an evidence-only branch would retain stale generated files. I did not include these unrelated shared views in this review write-set.
- Scope question posted to the Coordinator: should the Coordinator reconcile those generated views, or authorize their renderer-generated correction in the same Plan PR? No evidence commit or Plan PR was pushed while this shared-file decision is unresolved.

END_BLOCKED w267-0428-284-pridentity: PR #183 head 4e285efb6 CHANGES; isolated review akte cannot be published until the unrelated generated-view drift in views/overview.md:73 and views/releases/v0.4.28.md:337 is reconciled.
