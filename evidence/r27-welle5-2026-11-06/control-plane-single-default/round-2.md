# Control-plane single-default — base refresh round 2

Task: `t-20261106-r27-control-plane-single-default`  
Worker: Codex Worker, mission `w248-sd-baserefresh`  
PR: [#1404](https://github.com/mcpdev80/baseharbor/pull/1404)  
Branch: `work/r27-single-default`

## PLAN

1. Refresh and record the exact remote branch/develop heads; inspect the base-to-head and three-dot diffs.
2. In an isolated worktree, merge `origin/develop` into the existing branch. Resolve only if needed, preserve all content, and record name-only results. Make no content changes.
3. Push the branch, mark PR #1404 ready, and observe the hosted run at the final SHA through terminal green.
4. Record the `6b37600` / `5e4fde7` / final-head table, explain the old-base deletion artifact, validate the code-content identity, and publish an origin-main `ls-tree` witness.

## Baseline

- `origin/develop`: `5e4fde7177ea020de39b117f6d89cfa8f7c62be2`
- `origin/work/r27-single-default`: `6b376000735b6e2f7d2d3cb2b5096232aa6c3ff8`
- PR #1404: OPEN, not draft, base `develop`, head matches the branch above.
- The product root checkout has unrelated uncommitted changes; it is not used by this mission.
- No edit has yet been made to the product branch.

## Three-head comparison and base-artifact explanation

| Snapshot | Develop base/relationship | Candidate result |
| --- | --- | --- |
| `6b376000735b6e2f7d2d3cb2b5096232aa6c3ff8` | Branch originally cut at `78e78e66`; current develop had advanced to `5e4fde7177ea020de39b117f6d89cfa8f7c62be2` | Against the current develop tree (`5e4fde7..6b37600`), a direct base/head comparison showed deletions of `cmd/baha/application_image_transfer.go` and its test. The three-dot comparison (`5e4fde7...6b37600`) showed only the three Single-Default edits. The apparent deletion came from the old base not containing files subsequently added by PR #1402. |
| `5e4fde7177ea020de39b117f6d89cfa8f7c62be2` | Current develop after PR #1402 landed | This is the exact develop commit merged into the existing PR branch. |
| `ed98ed1dde79fe91cfde11b8d5dfa738f802992f` | Merge commit with parents `6b37600` and `5e4fde7`; develop is an ancestor | Final PR head. The three-dot diff against current develop contains only the three task-owned files, with no deletion. Their blobs are byte-identical to the `6b37600` versions. Both Image-Transfer files are byte-identical to current develop. No task content was changed. |

Commands / witnessed results:

- Before refresh, `git diff --name-status 5e4fde7..6b37600` showed exactly the two apparent `D` entries above plus the three task-file `M` entries. `git diff --name-status 5e4fde7...6b37600` showed only the three task-file `M` entries.
- After refresh, `git merge-base origin/develop HEAD` was exactly `5e4fde7177ea020de39b117f6d89cfa8f7c62be2`; `git diff --name-status origin/develop...HEAD` showed only `M cmd/baha/path_prompt_context.go`, `M cmd/baha/runtime_ports_test.go`, and `M internal/runtime/stack_test.go`.
- All three task-file blobs were unchanged between `6b37600` and `ed98ed1`. The Image-Transfer source and test blobs in `ed98ed1` equal `origin/develop`.
- The merge was conflict-free. The final branch-only log contains the original task commit and the develop merge commit; no unrelated candidate commit was introduced.

## Scope boundary

This is a base-only refresh. Preserve the existing task changes and add the current develop ancestry. Do not change implementation or tests, `.github`, runtime/VM state, or create another PR. Use no subagents. Build caches and temporary output, if needed, stay under `/tmp/opencode/w248*`.

## Push, PR and hosted run

- Pushed `ed98ed1dde79fe91cfde11b8d5dfa738f802992f` normally to `work/r27-single-default`; live `ls-remote` matched this SHA. Develop remained `5e4fde7177ea020de39b117f6d89cfa8f7c62be2`.
- PR #1404 remained OPEN against `develop`, `isDraft=false`, merge state CLEAN. `gh pr ready` confirmed it was already ready for review.
- Own hosted run: [42237544020](https://github.com/mcpdev80/baseharbor/actions/runs/42237544020), event `pull_request`, exact head `ed98ed1dde79fe91cfde11b8d5dfa738f802992f`, terminal `completed/success`.
- `PR Selected Checks` completed success with Actions integration 15368. Go unit tests, CLI package tests, build, vet, formatting, source contracts, runtime-provider package tests, focused Python, trusted plan, workflow policy, and guided tests passed. Unrelated release preflight, validation, targeted Docker/Podman, consumer/demo pins, exact candidate, public contracts, runner interface and selected-runtime jobs were skipped; this mission changed only ancestry and did not claim those skipped jobs as runtime evidence.
- No hosted-run credentials, pins or environment variables were set by this lane; the existing PR workflow selected checks from its configured inputs.

## repo-rule compliance

The work was limited to integrating current develop into the assigned existing branch and recording evidence. The claim was published on the Planning card before product-branch mutation. The native Todo tool was unavailable in this session; this numbered evidence checklist was the persistent plan. The dirty product root checkout was not touched. No source file, test, workflow, VM, or second PR was changed or used.

## origin/main publication witness

This round records only the assigned base refresh. The separate Docker/Podman runtime acceptance matrix remains outstanding as noted in the concurrent coordinator update to the task card; this mission prohibited VM access and does not claim those cells. The evidence file's exact `origin/main` blob and `main` ref are reported in the END transcript after publication.
