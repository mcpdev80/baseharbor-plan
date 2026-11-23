# PR #1793 review and merge record

## PLAN — PR #1793

- 319. Read the #1793 review/merge contract and create this numbered plan in the live board and Planning evidence.
- 320. Verify GitHub remotes, exact PR/base/head, merge-base ancestry, merge state, and exact changed files.
- 321. Validate release requirements carry-forward while source release fields remain unchanged.
- 322. Verify shell-ux and ci-fast-check gate ownership/routing plus MCP release-only deferral and correct workflow/suite citation.
- 323. Inspect regression tests a, b, and c and confirm exact-head hosted execution.
- 324. Check consent/fail-closed behavior is unchanged and review the candidate against the three intake points.
- 325. Merge normally only if every contract and exact-head CI check passes; otherwise document repair and stop.
- 326. Verify merged/develop refs, record cleanliness, validate and publish evidence, update board, and post END.

## REVIEW — PR #1793

- Role: CODEX-REVIEW. The PR had already been merged before this independent review began; no merge action was performed in this session.
- Reviewer identity: codex-rev-1747, independent review session. Model family: GPT-6. Backend/session UUID was not exposed in the shell.
- Review time: 2026-11-23 06:26 UTC.
- Product remote was resolved first: `origin`, `lane-origin`, and `upstream` all resolve to `https://github.com/mcpdev80/baseharbor.git`; this GitHub URL/API supplied remote truth.
- Planning remote verified before the evidence commit: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`.
- `python3 baseharbor-plan/scripts/plan.py show t-20261121-static-gate-registration` reports `state: blocked` (dependency `t-20261122-gate-catalog-missing-app-broker-component` accepted). The mission supplies the current review criteria; this review leaves the task blocked because one explicit focused-gate routing criterion is absent in the merged tree.

### Remote PR and merge state

- Mission candidate: PR #1793 head `6d39cc8aafc2512ffdc1420e42e315eb89a4fb8a`, base `fcccf7a2059fa862f921ed58fda3f8248932c60d`.
- GitHub compare `fcccf7a2059fa862f921ed58fda3f8248932c60d...6d39cc8aafc2512ffdc1420e42e315eb89a4fb8a` reports merge base equal to the exact base, ahead 6, behind 0, and only the five contract files below.
- At review time, GitHub already reported PR #1793 closed/merged at `2026-11-23T06:12:46Z`, merge commit `fc3eecbf4b65330bf0643dcde4136ca6d9620665`, head unchanged at `6d39cc8aafc2512ffdc1420e42e315eb89a4fb8a`.
- Remote refs at the later verification point: `refs/heads/develop` was `f50b118f2dfc670ac040185a0a766370f8d992a2`; `refs/pull/1793/head` remained `6d39cc8aafc2512ffdc1420e42e315eb89a4fb8a`. The merged branch ref `ingress-0428-208-static-gate` was no longer present. GitHub compare from merge commit `fc3eecbf4b65330bf0643dcde4136ca6d9620665` to current develop `f50b118f2dfc670ac040185a0a766370f8d992a2` shows one later commit changing only `scripts/pr-gate-coverage.json`; it does not repair the routing gap below.
- The merge commit has parent `fcccf7a2059fa862f921ed58fda3f8248932c60d`, confirming the expected base ancestry. No branch rewrite or merge was performed by this reviewer.

### Scope and release catalog checks

- Exact PR file list and numstat:
  - `scripts/pr-required-final.py`: 10 additions, 1 deletion.
  - `scripts/pr-stage-boundary.py`: 24 additions, 6 deletions.
  - `scripts/release-requirements.json`: 4 additions, 2 deletions.
  - `scripts/test_pr_required_final.py`: 31 additions, 0 deletions.
  - `scripts/test_pr_stage_boundary.py`: 27 additions, 8 deletions.
- No `.github/**`, product content, or `go.mod` file changed.
- Deep JSON comparison of `scripts/release-requirements.json` at base and candidate confirms top-level `releases` gains `v0.4.28`; only `atomic/static/mcp.required_for` gains `v0.4.28`; every other gate object and every other field remains unchanged. The gate catalog has no separate root `release` value; the existing gate requirements remain through `v0.4.27` except the explicitly carried MCP gate.
- The candidate’s patch contains zero occurrences of the incorrect `docker-runtime-acceptance.yml:630` citation. It contains the correct release executor chain: `.github/workflows/pre-release.yml:663-681` invokes the static-gates matrix and `.github/workflows/pre-release-runtime-suite.yml:264-270` dispatches `GATE=mcp` to `tests/mcp/run.sh`. `scripts/pr-stage-boundary.py` cites this chain in both release-only MCP boundary comments.

### Routing finding — acceptance gap

The candidate correctly keeps `atomic/static/mcp` release-only: `scripts/pr-stage-boundary.py:26` defines `ATOMIC_STATIC_DEFERRED_RELEASE_ONLY`, lines 74-82 defer MCP and keep unrelated gates selected; `scripts/pr-required-final.py:54-63` allows only the declared release-only deferral and preserves rejection of unknown deferred gates. The regression in `scripts/test_pr_required_final.py` also proves a failing PR validation still blocks.

However, the requested shell-ux/ci-fast-check focused mapping is absent from the final merged policy:

- `scripts/pr-stage-boundary.py:33-36` includes `atomic/static/shell-ux` and `atomic/static/ci-fast-check` in `ATOMIC_STATIC_PR_EXECUTED_GATES`, so the stage boundary keeps them selected.
- `scripts/pr-required-final.py` contains no `ATOMIC_STATIC_FOCUSED_GATES` constant. Its selected-gate routing at lines 69-78 handles Docker/Podman runtime gates, public contracts, and coreless lifecycle; any selected static shell-ux or ci-fast-check gate reaches line 78 and adds `selected gate has no workflow executor`.
- `scripts/test_pr_required_final.py` has no regression proving either focused static gate maps to the real `pr_focused` executor. Its new tests cover MCP deferral and rejecting invented deferred gates. `scripts/test_pr_stage_boundary.py` proves stage classification only, not final-verifier routing.
- The PR commit history records an initial focused mapping, then the MCP deferral correction explicitly says it “drop[s] the ATOMIC_STATIC_FOCUSED_GATES pr_focused mapping.” The final tree has the intended MCP deferral but also lost the required shell-ux/ci-fast-check mapping. Thus a green exact-head run does not establish this acceptance point.

Review verdict: REQUEST CHANGES / BLOCKED (post-merge finding). PR #1793 is already merged; this session did not approve or merge it. Keep 0428-208 unaccepted until the policy gap is repaired and hosted evidence passes.

Repair recipe for a new owner-authorized correction:
- In `scripts/pr-required-final.py`, restore an explicit `ATOMIC_STATIC_FOCUSED_GATES` allowlist containing exactly `atomic/static/shell-ux` and `atomic/static/ci-fast-check`, and route those selected gates to the existing PR-focused executor. Keep `atomic/static/mcp` out of this set and in the release-only deferred allowlist.
- Add `scripts/test_pr_required_final.py` cases proving each focused gate is accepted through the PR executor, while an unrecognized `atomic/static/*` gate still fails. Retain the existing MCP deferral, failing-PR-job, and unsupported-deferral regressions.
- Run the focused Python suite and `PR Selected Checks` on the corrected exact head. The hosted evidence must show the test modules execute and the selected-check plan recognizes both focused static gates; skipped/queued evidence is not a pass.
- Stop if MCP is routed as PR-executed, an unknown static gate is accepted, or either required focused gate still yields `selected gate has no workflow executor`.

### Exact-head hosted checks and regression execution

- Run `45122245021` completed `success` on exact PR head `6d39cc8aafc2512ffdc1420e42e315eb89a4fb8a`, event `pull_request`.
- The exact-head `PR Selected Checks` check run succeeded with GitHub Actions integration id `15368`. `PR · Trusted Plan`, `PR · Native gate plan`, `Workflow policy`, `PR · Source format`, `PR · Focused Python`, and candidate-added advisory checks succeeded. The complete job census was 32 terminal jobs: 11 success and 21 skipped; skipped jobs are not counted as passes.
- Owning test job: `PR · Focused Python`, job id `137518493055`. Its log explicitly ran `python3 scripts/test_pr_required_final.py` and `python3 scripts/test_pr_stage_boundary.py`; the corresponding suites reported 24 tests / `OK` and 13 tests / `OK`. These modules contain the MCP deferral cases (a), the still-failing PR-validation case (b), the unsupported-deferred-gate rejection (c), and the stage-boundary cases. The log reports module-level execution and suite totals rather than individual unittest method names.
- The focused Python test execution is durable through the existing `pull_request` job. It does not cover the missing final-verifier mapping for shell-ux/ci-fast-check, because no such test exists in the final candidate.
- No product tests were run locally. No workflow rerun or dispatch was triggered.

## repo-rule compliance

- The review used GitHub refs, API compare, PR files, and hosted logs as remote evidence; it did not rely on the shared product checkout or edit product files.
- The current task card remains `blocked`; no Planning acceptance status was changed.
- No workflow files were edited. No containers or compose projects were started.

## cleanliness

- Before evidence publication, PID 4093377 ran `docker ps -a --no-trunc`; output was only `CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES`.
- A post-publication Docker inventory will be recorded before END.

## END codex-rev-1747 BLOCKED

PR #1793 is already merged as `fc3eecbf4b65330bf0643dcde4136ca6d9620665`, but independent post-merge review found the required shell-ux/ci-fast-check final-verifier routing missing at candidate `6d39cc8aafc2512ffdc1420e42e315eb89a4fb8a`. Keep 0428-208 blocked pending the repair recipe and exact-head hosted evidence above.
