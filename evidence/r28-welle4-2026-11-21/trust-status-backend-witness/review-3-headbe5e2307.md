# CODEX-REVIEW — PR #1702 hopped candidate

## PLAN
1. Verify PR #1702 remote head, develop base, and run 44949384417 terminal state.
2. Verify reviewed head 5761ebe6914 is an ancestor of the hop merge commit and inspect exact hop diff parity.
3. Inspect every required and executed CI cell for the exact hopped head; distinguish skipped jobs.
4. Recheck the four original review-2 findings and confirm their disposition at the hopped head.
5. Verify merge-commit authorship does not introduce a new author identity or require an exception.
6. Issue a fresh independent verdict on the exact hopped head; do not merge.
7. Render/check Planning, publish only this evidence from the lane-owned plan worktree, and verify its origin/main path.

## Planning remote
`git -C /home/marcel/dev/baseharbor-ecosystem/workers/codex-rev-1747-plan-wt remote -v`:
origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin https://github.com/mcpdev80/baseharbor-plan.git (push)

## PLAN — coordinator correction: reviewer-only
1. Complete the independent exact-head review for #1702 and publish the verdict evidence from this lane-owned Planning worktree.
2. Do not merge, close, or comment on the PR; the separate merge-role session receives any APPROVE handoff.
3. Verify remote head, run, ancestry, patch parity, and identity at review time; retain evidence for the exact candidate.
4. Update the live board and publish only this evidence file.

## Exact candidate and ancestry

Remote witnesses at review time:

```text
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1702/head refs/heads/develop
1080986fe73cb3d6e283fd9ef61c05c02b9260af refs/heads/develop
be5e23079df36a81fe17fd89068853fa022240a2 refs/pull/1702/head
```

`gh pr view 1702 --repo mcpdev80/baseharbor --json state,isDraft,mergeable,mergeStateStatus,headRefOid,baseRefName,commits` returned OPEN, non-draft, MERGEABLE, CLEAN, base `develop`, exact head `be5e23079df36a81fe17fd89068853fa022240a2`. No local product checkout was used. GitHub commit metadata for the exact head gives tree `0339f60ec5dc5cc826df253c5cfc765a3aebeef3` and parents, in order, `5761ebe6914abab0817b8f5f7a68fba64d0069b1` and `1080986fe73cb3d6e283fd9ef61c05c02b9260af`. This proves the prior reviewed candidate and the exact current develop are direct parents of the hop commit. GitHub compare `1080986...be5e230` reports merge-base `1080986`, behind_by 0, and only the five owned `cmd/baha` files in the candidate delta.

Stable patch-id parity was independently calculated from GitHub compare patches:

- Original feature delta `d1acf3f31a360cd2a5e0ebaed1c70ccdd7957cf3..5761ebe6914abab0817b8f5f7a68fba64d0069b1`: `13d2e93600eb541c3127e82874a33459fdcb29b7`.
- Hopped feature delta `1080986fe73cb3d6e283fd9ef61c05c02b9260af..be5e23079df36a81fe17fd89068853fa022240a2`: `13d2e93600eb541c3127e82874a33459fdcb29b7`.
- Both comparisons name exactly `cmd/baha/app_status_result.go`, `cmd/baha/app_status_result_seam_restored_0428_142_test.go`, `cmd/baha/app_status_result_test.go`, `cmd/baha/app_status_result_witness_boundary_0428_142_test.go`, and `cmd/baha/perses_lifecycle.go`.

## Four review-correction points rechecked

1. The earlier false-green Prometheus boundary is closed: `cmd/baha/app_status_result_witness_boundary_0428_142_test.go:131-163` fails if the Prometheus witness is missing and requires exactly `unreachable` when the resolved signal is supported but provenance is empty.
2. The empty-witness and `Verification=none` boundaries are tested as negative claims: the tests fail on any `configured` result and require a source ID for every emitted declared backend (`app_status_result_witness_boundary_0428_142_test.go:20-84`).
3. The status output carries per-backend state and source ID through the shared helper: the machine result constructs `PersesBackendWitness` in both local and remote result paths (`app_status_result.go:303-314,403-418`); the human `perses status` renderer prints backend, source ID, and state (`perses_lifecycle.go:308-319`).
4. The review-2 identity concern is resolved by the hop’s ancestry structure and exact commit metadata: the five pre-hop feature commits (`a8113ea88685`, `4a69e47f3b5b`, `68a2bded1645`, `a5ff40fbd32f`, `5761ebe6914a`) each retain author and committer `0428-142-statuswitness <0428-142@baseharbor.invalid>`. The hop commit itself is authored/committed by Marcel and introduces no new feature author. **Ein merge-commit-hop fuehrt keine autoren neu - keine ausnahme noetig.**

The original `review-2-head5761ebe6.md` file was not present in this lane worktree or Planning `origin/main` at the initial fetch. The findings above are independently rechecked against the exact candidate and source; I do not attribute additional unobserved text to that missing file. The real positive provider witness remains separately owned by 0428-143; at this candidate the public result fails closed when that provenance is absent, consistent with the Owner’s accepted boundary for this review.

## CI run 44949384417

Run URL: `https://github.com/mcpdev80/baseharbor/actions/runs/44949384417`. GitHub API reports event `pull_request`, head SHA exactly `be5e23079df36a81fe17fd89068853fa022240a2`, terminal `completed/success`. There were 36 jobs: 15 success, 21 skipped, 0 failed, 0 cancelled, 0 incomplete. Skipped cells are not treated as passes.

Executed jobs, all successful:

- `PR Selected Checks` 136985018458: terminal aggregate passed the selected native acceptance, selected Go shard coverage, and selected job result checks.
- `PR · Go unit · cli-0` 136983774399; `cli-1` 136983774394; `cli-2` 136983774352; `cli-3` 136983774356; `packages` 136983774371; `owner` 136983774411.
- `PR · Validation · go-build` 136983774332; `cli-gofmt` 136983774363; `go-vet` 136983774557.
- `PR · Native gate plan` 136983720741; `PR · Trusted Plan` 136983720782; `PR · Source format` 136983720815; `PR · Focused Python` 136983774260; `Workflow policy` 136983720558.

The exact trusted plan artifact reports `head_sha=be5e23079df36a81fe17fd89068853fa022240a2`, base and merge-base `1080986fe73cb3d6e283fd9ef61c05c02b9260af`, `coverage_status=resolved`, `broad_required=false`, `fallback_used=true`, `selected_gates=[]`, and no unresolved coverage. It selected the normal Go unit, build, format, and vet coverage for the CLI paths. The native/runtime matrices were skipped and are not passes; no local suite tests or VM tests were run. No `.github/**` or workflow action was taken by this reviewer.

The CI shard logs expose aggregate counts rather than named per-case receipts. All six CLI/package/owner Go unit shards and the terminal aggregate executed successfully. Exact named-case receipt tooling remains an owner-scope open item; it is not represented here as a per-case log receipt.

## Verdict — REVIEW role

**APPROVE** exact candidate `be5e23079df36a81fe17fd89068853fa022240a2`, run `44949384417`. The hop is an exact two-parent merge preserving the prior candidate, with identical stable patch-id content against its respective bases. The terminal selected-check aggregate and all six Go unit shards are successful at this exact head. The earlier false-green assertion is now fail-fast, the empty-provenance outputs fail closed, and the human and machine surfaces use the same per-signal witness representation. The owner-accepted upstream provenance boundary remains tracked under 0428-143. No bypass is needed.

## repo-rule compliance

- Review-only inspection used GitHub remote refs, commit/compare metadata, exact-run data, and read-only source retrieval. No product files were edited.
- No local suite tests, no `.github/**` edits, no workflow dispatch/rerun, no force push, and no subagents.
- Per the coordinator correction at 23:0xZ, this session is exclusively CODEX-REVIEW. It does not merge, close, or comment on the PR. An APPROVE is handed to the separate merge-role session.

## cleanliness

Before review finalization, `docker ps -a --no-trunc` was run by shell PID 216614 and recorded at `/home/marcel/dev/baseharbor-ecosystem/workers/codex-rev-1747-plan-wt/docker-before-1702-review.txt`. It showed eight pre-existing `bh-itest-*` containers, all exited. This reviewer started no container or compose project.

Fresh freeze check after review preparation:

```text
git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1702/head refs/heads/lane-0428-142-statuswitness refs/heads/develop
1080986fe73cb3d6e283fd9ef61c05c02b9260af refs/heads/develop
be5e23079df36a81fe17fd89068853fa022240a2 refs/heads/lane-0428-142-statuswitness
be5e23079df36a81fe17fd89068853fa022240a2 refs/pull/1702/head
```

Fresh `gh pr view` remains OPEN, non-draft, MERGEABLE, CLEAN, and at that same exact head. Trusted plan artifact `pr-plan.json` SHA-256: `b95c9337c85c994ee6ba12e920953a957bf4ce93582e8a7acb59ff6107d26b18`.

## Verdict — final review role

**APPROVE** exact head `be5e23079df36a81fe17fd89068853fa022240a2`; exact PR run `44949384417` is completed/success and the remote merge state is CLEAN. The head did not move during review. There is no request for a workflow rerun and no product write from this reviewer.

## MERGE role handoff

Coordinator correction at 23:0xZ makes this session reviewer-only. No `gh pr merge`, close, or merge-triggering comment was issued. The ordinary merge, if accepted by the separate authorized merge-role session, must preserve merge-commit history; it is not part of this review action.

## cleanliness

`docker ps -a --no-trunc` after review, shell PID 220112, is recorded at `/home/marcel/dev/baseharbor-ecosystem/workers/codex-rev-1747-plan-wt/docker-after-1702-review.txt`. It showed the same eight pre-existing `bh-itest-*` containers as the before snapshot, all exited. This reviewer started no containers or compose projects.

END codex-rev-1747 DONE — CODEX-REVIEW APPROVE, exact head `be5e23079df36a81fe17fd89068853fa022240a2`, run `44949384417`, plan SHA-256 `b95c9337c85c994ee6ba12e920953a957bf4ce93582e8a7acb59ff6107d26b18`; merge-role handoff only.

## Published path witness

Exact output of `git -C workers/codex-rev-1747-plan-wt ls-tree -r --name-only origin/main | grep evidence/r28-welle4-2026-11-21/trust-status-backend-witness/review-3-headbe5e2307.md` after fetching origin/main:

evidence/r28-welle4-2026-11-21/trust-status-backend-witness/review-3-headbe5e2307.md
