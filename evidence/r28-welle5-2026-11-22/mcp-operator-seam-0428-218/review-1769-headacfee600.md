# PR 1769 independent review

## PLAN

1. Verify PR 1769 exact head, fetched develop base SHA, ancestry, and exact one-file diff.
2. Compare PR 1769 with stale-base PR 1741 for complete one-to-one port without semantic changes.
3. Verify exact-head required CI and any native matrix checks are terminal green, with no skipped required checks.
4. Verify PR 1741 remains open pending verification and merge of carrier PR 1769; write the verdict evidence.
5. Publish evidence on baseharbor-plan origin/main, verify its path, and post END.

## Exact candidate and provenance

- Role: CODEX-REVIEW, read-only and independent.
- PR #1769: https://github.com/mcpdev80/baseharbor/pull/1769; base `develop`; branch `codex/0428-218-mcp-seam-recut`; state OPEN, merge state BLOCKED.
- Exact head: `acfee600b70b8905a16ed118a071a37cdaa9e352`. Remote `refs/pull/1769/head` matched this SHA.
- `git remote -v` in the product checkout resolved `origin` and `lane-origin` to `https://github.com/mcpdev80/baseharbor.git`; no unresolved remote was used.
- Exact fetched remote develop: `64eab13e23fba8bca07a1d68c687fa36afedb64e` from `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`.
- `git merge-base --is-ancestor 64eab13e23fba8bca07a1d68c687fa36afedb64e acfee600b70b8905a16ed118a071a37cdaa9e352` exited 0. GitHub compare reported base and merge-base both equal `64eab13e23fba8bca07a1d68c687fa36afedb64e`, status ahead, ahead_by 1.
- `git diff --name-only 64eab13e23fba8bca07a1d68c687fa36afedb64e...acfee600b70b8905a16ed118a071a37cdaa9e352` output: `cmd/baha/mcp_operator_seam_test.go`.
- `git log --oneline 64eab13e23fba8bca07a1d68c687fa36afedb64e..acfee600b70b8905a16ed118a071a37cdaa9e352` output: `acfee600b test(0428-218): cover MCP operator seam on current develop`.
- The exact PR diff changes no production code, `cmd/baha/app_broker.go`, `.github/**`, or `scripts/**`.

## Port comparison

- PR #1741 is OPEN, based on `lane-0428-198-cli-shard-operator-env`, head `fb5a5deaf36ba160b527019a3ef4eea85060905d`; it has not merged or closed.
- GitHub file patches for `cmd/baha/mcp_operator_seam_test.go` in PR #1741 and PR #1769 compared byte-for-byte equal. Each patch adds the same 103-line test file; the port itself is a one-to-one textual port with no semantic change.
- The recut does not include the fixture definitions used by that test. This is material on `develop`: its exact-head CI reports both helper identifiers undefined, so the file-only port does not build against its new base.

## STATE: exact-head CI failure

- Run 45022237157 (`CI · Source & Quality`, `pull_request`) targeted exact head `acfee600b70b8905a16ed118a071a37cdaa9e352`; terminal status `completed`, conclusion `failure`, updated 2026-11-22T12:29:00Z.
- `PR · Validation · go-vet` job 137207529834 failed with log line: `vet: cmd/baha/mcp_operator_seam_test.go:44:13: undefined: operatorAuthFixtureContext`.
- `PR · Go unit · cli-1` job 137207529925 failed with log lines: `cmd/baha/mcp_operator_seam_test.go:44:13: undefined: operatorAuthFixtureContext` and `cmd/baha/mcp_operator_seam_test.go:55:15: undefined: withoutOperatorAuthTestContext`. The other Go CLI shards and owner shard also failed compilation.
- `PR Selected Checks` job 137208231452 concluded failure; its log line was `##[error]Process completed with exit code 1.`
- The native matrix job `PR · Native · ${{ matrix.id }}` job 137207518546 was skipped. Skipped is not green evidence.
- Verdict: REQUEST CHANGES. The copied test references fixture helpers absent from the develop-base candidate, and exact-head required CI failed.

## Required sequence

- PR #1741 remains OPEN and unmerged; PR #1769 is OPEN and its exact-head checks failed.
- Required order is not complete: verify and merge carrier PR #1769 first; only after that rerun and merge PR #1741. No merge, close, comment, or rerun was performed in this read-only review.

## Repo-rule compliance

- No product edits or local tests were performed. No workflow rerun or workflow_dispatch was triggered.
- Shared product checkout had pre-existing modifications and an untracked worktree on another branch; it was not changed or cleaned. The candidate was checked by exact remote SHA and GitHub records.
- Planning remote first line observed: `origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.
- `python3 scripts/plan.py check`: 683 tasks, 7 epics, 13 releases, 24 decisions; 0 errors, 10 warnings.

## cleanliness

- Before review, `docker ps -a` under shell PID 4159001 showed only the header and no containers.
- After review, `docker ps -a` under shell PID 4162357 showed only the header and no containers. No containers were started.

## Verdict

REQUEST CHANGES — the file port is textually complete, but the referenced fixtures are undefined on develop and exact-head CI failed. Keep #1741 open until #1769 is fixed, verified, and merged; then rerun #1741.

END codex-rev2-1736 DONE: REQUEST CHANGES for exact head acfee600b70b8905a16ed118a071a37cdaa9e352; #1741 remains open pending #1769 verification and merge.

## publication witness

- Exact `git ls-tree -r --name-only origin/main | grep` output after fetching origin/main: `evidence/r28-welle5-2026-11-22/mcp-operator-seam-0428-218/review-1769-headacfee600.md`
