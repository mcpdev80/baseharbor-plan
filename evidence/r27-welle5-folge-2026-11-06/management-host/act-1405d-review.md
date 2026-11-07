# CODEX-REVIEW 0427-036 / PR #1405 rereview

## PLAN

1. Verify the real planning repository and read the 0427-036 task and prior review evidence.
2. Fetch authoritative develop and PR #1405 refs; prove ancestry and inspect commits.
3. Compare product code with previously accepted 5b8d0f5745 and recheck findings.
4. Verify terminal CI for the exact candidate and record the verdict in planning evidence.
5. Publish evidence on origin/main, verify it is present, and post END to coordinator.


## Planning task and prior review evidence

- Planning repo: `git -C baseharbor-plan rev-parse --show-toplevel` returned exactly `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`.
- `git remote -v` returned `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)` and `origin https://github.com/mcpdev80/baseharbor-plan.git (push)`. Authenticated GitHub user: `mcpdev80`.
- Planning `origin/main` fetched at `a898223dacb2b0e8280a604dec95df995c67bbda`. The current card is `t-20261018-r27-management-host` / 0427-036, state review, with all listed predecessors accepted.
- Read the prior review and round-9 record directly from the fetched `origin/main`: `evidence/r27-welle5-folge-2026-11-06/management-host/act-1405c-review.md` and `round-9-baserefresh.md`. The earlier accepted findings remain: `serve.go` initializes and passes non-nil startup context through both paths, and `TestServeStartUpPathNeverReceivesNilStartupContext` has the behavioral RED-without-fix / GREEN-with-fix witness in round-8 evidence. Round 9 records a mechanical merge of current develop and no change to the accepted `serve.go` or regression test.

## Candidate and provenance

Fresh `git ls-remote` for the product candidate:

```text
934be499b9d2d894f80889fc23cd811884c8aec4	refs/heads/develop
6014a8fcd2697f34ab0c52353d328dd55cc9a1a5	refs/pull/1405/head
```

PR #1405 is OPEN, non-draft, targets `develop`, is MERGEABLE, and its live head matches `6014a8fcd2697f34ab0c52353d328dd55cc9a1a5`. `git merge-base --is-ancestor 934be499b9d2d894f80889fc23cd811884c8aec4 6014a8fcd2697f34ab0c52353d328dd55cc9a1a5` returned rc=0.

The required `git log --oneline origin/develop..6014a8fcd2697f34ab0c52353d328dd55cc9a1a5` output is:

```text
6014a8fc Merge origin/develop 934be499b into work/r27-management-host (base refresh, no product logic change)
5b8d0f57 fix(cmd/baha): never pass nil startup context on per-application broker serve path
0f08b877 Merge develop dddf0d7823f into work/r27-management-host (basis-auffischung r5)
5b8c5422 test(r27 management-host r4): real serveCommand two-process ownership integration regression
3a80ed04 fix(r27 management-host r4): one ownership primitive across bootstrap through server lifetime
64d93e94 fix(r27 management-host r3): serve retains bootstrap ownership through bind and surfaces resolution errors
a87f8377 feat(r27 management-host): durable minimal authority on the selected host
```

Every candidate-only commit in this chain is part of card 0427-036; no foreign PR candidate is carried. Head `6014...` is a two-parent merge whose first parent is the previously reviewed `5b8d0f5745c55fd8be89d5dc53edb4e9b145eede` and second parent is exact develop `934be499b9d2d894f80889fc23cd811884c8aec4`.

## Accepted code comparison

`git diff 5b8d0f5745c55fd8be89d5dc53edb4e9b145eede 6014a8fcd2697f34ab0c52353d328dd55cc9a1a5 -- cmd/baha/serve.go cmd/baha/serve_test.go` is empty. The blobs are identical at both heads: `serve.go` `a4d9a5a2e022e89d4cfeda2ffa99a577048827f6`; `serve_test.go` `d20b5cb5f4a55545386edd6114d4dcf38c93f61a`.

The broader `cmd/baha/` diff from 5b8d0f57 consists of the develop merge's `control_plane_single_native_ci_test.go` addition and `target_remote_boundary_test.go` test addition. Both candidate blobs equal their `origin/develop` blobs exactly. There is no new `serve.go` edit or candidate-authored logic change beyond the previously reviewed fix. Thus the act-1405c code and regression findings remain unchanged at this candidate.

## Exact-head CI

Workflow run `42338548731` (`CI · Source & Quality`) is terminal `completed / success` for `pull_request` head `6014a8fcd2697f34ab0c52353d328dd55cc9a1a5`. `PR Selected Checks` succeeded from Actions integration `15368`; `PR · Source format`, `PR · Trusted Plan`, `PR · Focused Python`, `authority-package-tests`, `cli-gofmt`, `go-unit-tests`, `go-build`, and `go-vet` also succeeded. `Targeted HA · docker`, `Targeted HA · podman`, and `PR · Selected Runtime` were skipped by the existing designated-ref owner gate; no check failed. No rerun or workflow_dispatch was performed.

## Verdict

**verdict=ACCEPT.** The sole act-1405c rejection reason, missing current-base ancestry, is fixed. The current base is an ancestor, the only candidate-side chain is card 0427-036 plus its base-refresh merge, accepted serve behavior and regression blobs are unchanged, and exact-head CI is terminal with required checks green; skipped runtime cells are explained by the owner gate and are not a new code finding for this rereview.

No product writes, local tests, workflow actions, merge, VM/container work, or subagents were used.

## Turn-start operational flags

`basics-check.py` reported two queued watcher messages, missing `workers/todos/codex-rev-1419.json`, five existing `bh-*` containers on the dev host, and an owner report due after eight watcher events. `wake-drain.sh` drained two messages and `events-check.py --ack` acknowledged the watcher records. The mission-specific board is `workers/todos/codex-1405-rereview-d.json`; unrelated lane TODO state and pre-existing host containers were left untouched. These coordinator-level flags are reported to the coordinator, not handled as product-review work.

## Planning publication witness

Exact pre-push output of `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main`:

```text
a898223dacb2b0e8280a604dec95df995c67bbda	refs/heads/main
```

## END

END_DONE codex-1405-rereview-d: verdict=ACCEPT head=6014a8fcd2697f34ab0c52353d328dd55cc9a1a5 ancestry=rc0 code_unchanged=ok ci=42338548731 TERMINAL SUCCESS; runtime owner-gated skips; evidence=<this file>
