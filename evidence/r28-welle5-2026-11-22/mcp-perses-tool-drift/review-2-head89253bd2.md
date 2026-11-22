# PR #1751 review — exact head 89253bd23d6a4c5f9006d624c3d78910c2eea68b

## PLAN

1. Record the owner-directed exact-head scope, without inspecting other PRs.
2. Preserve the fresh product remote witness, exact merge parents, and PR diff summary.
3. Record the executed `cli-0` test job and terminal exact-head run.
4. Issue the exact-head APPROVE and publish this evidence to Planning origin/main.
5. Update the live board and post one END with the Planning commit SHA; do not merge or close.

## Exact candidate witnesses

Product remote verified as `origin https://github.com/mcpdev80/baseharbor.git` (fetch and push). Fresh `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1751/head refs/heads/develop` returned:

```text
7d4351c6d645353b6b96c8d320b4c832d55f9047 refs/heads/develop
89253bd23d6a4c5f9006d624c3d78910c2eea68b refs/pull/1751/head
```

The exact PR head `89253bd23d6a4c5f9006d624c3d78910c2eea68b` is a merge commit with parents `bdc7c1a9e6e6b1de29afb916d28712eba95dff56` and `7d4351c6d645353b6b96c8d320b4c832d55f9047`. The hop commit author and committer are both `mcpdev80`. The PR diff against current develop is only `cmd/baha/agent_mcp_test.go`, 25 added lines. The feature commit is retained. The merge commit tree matches the deterministic merge of those two parents; no merge or close was performed by this review.

## Test coverage and hosted execution

The added test requires the four Perses MCP tools on the live MCP surface at `cmd/baha/agent_mcp_test.go:145-160`; the contract declares the same names at `internal/machine/contract.go:205-208`. The enclosing test derives the expected operation set from `machine.Operations()`, compares it to the live MCP list, and checks safety annotations at `cmd/baha/agent_mcp_test.go:102-128`. The regression covers the Perses tool-list/contract drift by requiring the names and rejecting missing or unexpected surface entries.

Run `44965123423` (`CI · Source & Quality`, `pull_request`) completed `success` on the exact head `89253bd23d6a4c5f9006d624c3d78910c2eea68b`. The deterministic CLI sharder assigns `TestMCPGenericClientDiscoversCompleteSemanticSurfaceAndExercisesReadOnlyTools` to shard `cli-0`. Job `PR · Go unit · cli-0`, job ID `137032347806`, executed `bash scripts/pr-unit-database.sh "cli-0"` and completed success. Its terminal log reports `PASS cli-0: 460 passed / 13 intentionally skipped / 473 discovered; CLI inventory total=1843`. The sharder requires each selected test to emit a run event and pass or skip; this test contains no skip, so it executed and passed, not skipped.

The terminal `PR Selected Checks` aggregate, job `137033435161`, completed success. Selected source format, trusted plan, native gate plan, CLI build, CLI gofmt, CLI vet, source-contracts, and all four CLI unit shard jobs completed success. Other unselected jobs were skipped and are not counted as passed evidence.

## Verdict

APPROVE — exact PR head `89253bd23d6a4c5f9006d624c3d78910c2eea68b`. The test pins the required Perses tool surface, is selected and executed by the hosted `cli-0` job, and the exact-head run reached terminal success. The terminal-green exact-run acceptance condition is satisfied by run `44965123423` (the analogous #1749 condition was satisfied by run `44961731917`). No change recipe is needed. Handoff to the merge role; this review did not merge or close the PR.

## repo-rule compliance

Review only. No product edits, local tests, workflow edits, CI reruns, PR comments, merges, or closes. Evidence is stored only in the Planning repository.

## cleanliness

Shell PID `1299905`: `docker ps -a` before and after showed the same eight pre-existing exited containers (IDs `268b7d8b4612`, `34cf9576dc2b`, `e88b00795b5c`, `1451a7b5b3c6`, `d7ba821c0e08`, `957a80e73b57`, `45bddf32278e`, `9d3f1a2b1e0e`). No container or compose project was started or changed.

END_DONE codex-rev-1747: APPROVE #1751 exact head 89253bd23d6a4c5f9006d624c3d78910c2eea68b; run 44965123423 and cli-0 job 137032347806 passed; Evidence path verified on Planning origin/main before END.

## Planning remote witness

Verified before the evidence commit with `git -C baseharbor-plan remote -v`:

```text
origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin https://github.com/mcpdev80/baseharbor-plan.git (push)
```


## Final pre-END origin/main path witness

After `git -C baseharbor-plan fetch origin main`, `git -C baseharbor-plan ls-tree -r --name-only origin/main | grep 'evidence/r28-welle5-2026-11-22/mcp-perses-tool-drift/review-2-head89253bd2.md'` returned exactly:

`evidence/r28-welle5-2026-11-22/mcp-perses-tool-drift/review-2-head89253bd2.md`
