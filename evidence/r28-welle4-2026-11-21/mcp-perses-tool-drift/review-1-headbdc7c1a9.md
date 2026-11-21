# CODEX-REVIEW — PR #1751 MCP contract/static gate

## PLAN
1. Verify live #1751 head and develop refs before source inspection; stop if the PR head differs from the mission SHA.
2. Read card 0428-225 and the exact authorized workflow path from card 0428-208; verify identity and inspect the candidate diff.
3. Determine whether the candidate removes the named Static mcp contract mismatch or whether the golden/contract file must change.
4. If authorized by the task contract, dispatch the single approved release-suite workflow at the exact PR head and watch the Static mcp cell to terminal.
5. Issue an independent exact-head verdict; remain review-only and do not merge, close, or comment.
6. Publish this evidence from the lane-owned Planning worktree and verify its origin/main path.

## Candidate inspection

- Live PR: #1751 is OPEN, base `develop`, head `bdc7c1a9e6e6b1de29afb916d28712eba95dff56`, branch `w26-pr1588-0428-225-mcpcontract-wt`; `refs/pull/1751/head` and the branch resolve to that SHA. Develop was `513488eeb6d788f0e5eec054be89807505f05e08` (candidate is one commit behind by the mission's measurement).
- Commit author and committer both identify as `w26-pr1588-0428-225-mcpcontract <w26-pr1588-0428-225@baseharbor.local>`.
- Candidate parent: `1080986fe73cb3d6e283fd9ef61c05c02b9260af`.
- Changed paths: only `cmd/baha/agent_mcp_test.go` (+25, -0). The new regression assertion requires the four Perses MCP names in the server's discovered tools. It does not change the server surface, release gate's expected list, contract, or golden fixture; therefore it cannot remove the reported runtime mismatch by itself.
- The existing contract declares all four names at `internal/machine/contract.go:205-208`. The checked-in candidate golden also contains all four at `contracts/machine/v1/control.golden.json:391-424`; changing that golden to delete them would contradict the contract. No golden change is indicated by this head. The needed alignment is on the release gate's expected contract/catalog side, which is outside this task's writable scope (`scripts/**` and release registration; see `tasks/t-20261121-mcp-release-gate-perses-tool-drift.md`, Scope and Dependencies).

## Authorized release workflow observation

- The task-authorized path is `.github/workflows/pre-release.yml`, workflow `Release · Pre-Release Validation` (workflow ID `362658451`). The mission authorized one dispatch for the exact candidate head; no workflow file was edited.
- Dispatch command: `gh workflow run 362658451 --repo mcpdev80/baseharbor --ref w26-pr1588-0428-225-mcpcontract-wt -f tag=v0.4.28 -f ref=bdc7c1a9e6e6b1de29afb916d28712eba95dff56 -f demo_ref=f23b6e09be34601ba542a3087e19b80764a4165d -f only_gates=atomic/static/mcp`.
- Run `44952645994`, URL `https://github.com/mcpdev80/baseharbor/actions/runs/44952645994`, event `workflow_dispatch`, exact `headSha=bdc7c1a9e6e6b1de29afb916d28712eba95dff56`; terminal state `completed/failure`.
- Source job `136993749322` (`Source · Candidate and Gate Plan`) failed in `Resolve release candidate`; hosted log line: `REJECT: pre-release candidate does not contain develop tip 513488eeb6d788f0e5eec054be89807505f05e08 (drift).` The same log also reports `fatal: couldn't find remote ref refs/heads/release/v0.4.28`.
- `Static · ${{ matrix.gate }}` job `136993835355` completed `skipped`. There was no executed `Static · mcp` cell, so it has no terminal pass/fail result and the requested acceptance cell remains unproven. Per-job logs command for the skipped static job: `curl -sL https://api.github.com/repos/mcpdev80/baseharbor/actions/jobs/136993835355/logs`; byte count: 190. Source job log command: `curl -sL https://api.github.com/repos/mcpdev80/baseharbor/actions/jobs/136993749322/logs`; byte count: 190. `gh run view 44952645994 --repo mcpdev80/baseharbor --job 136993749322 --log-failed` showed the failing `Resolve release candidate` step and the rejection line above.
- Workflow source has the strict develop ancestry rejection at `.github/workflows/pre-release.yml:157`; release registration has no v0.4.28 entry in `scripts/release-requirements.json:3-10`, and `scripts/pre-release-check-plan.py:21-22` fails closed for an unregistered release. The workflow also attempted to fetch the absent `release/v0.4.28` ref. These are Owner-scope prerequisites, not changes this review may make.
- Verdict: BLOCKED. The candidate's regression assertion is directionally consistent with the contract, but acceptance cannot be approved without an actually executed green `Static mcp` at this SHA. Current run is a setup/source rejection, not a passing or failing Static mcp test. Owner-scope registration and an exact-head run after the candidate contains the required develop tip are required. No PR comment, merge, or close was performed.

## Cleanliness

- `docker ps -a` before, shell PID 443126: listed only pre-existing exited `bh-itest-*` containers; this review started no containers or compose projects.
- `docker ps -a` after, shell PID 443126: same eight pre-existing exited `bh-itest-*` containers; this review started no containers or compose projects.

## Repo-rule compliance

- Review-only against the mission's exact head. No product files or `.github/**` were changed; no tests were run locally; no PR comment, merge, close, product-branch push, or workflow edit was performed. The single authorized workflow dispatch was observed through terminal state.
- Evidence is in the lane-owned Planning worktree. Planning remote was verified before any evidence commit as `origin https://github.com/mcpdev80/baseharbor-plan.git` for fetch and push.
- `python3 scripts/plan.py render && python3 scripts/plan.py check`: completed with 0 errors and 11 pre-existing dependency-state warnings across 663 tasks, 7 epics, 13 releases, and 24 decisions. Evidence checkbox scan found no checkbox lines.

## END

END_BLOCKED codex-rev-1747: #1751 head bdc7c1a9e6e is blocked; run 44952645994 failed before Static mcp (job 136993835355 skipped); receipt: owner-scope open item; Planning SHA 95235073456c5d68582f199c5c1b6e441c871498.

## Evidence publication

- Initial evidence commit `5e7c0c5514205fc25f741360f0671e826f4891b0` was pushed to Planning `origin/main`; `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main` returned `5e7c0c5514205fc25f741360f0671e826f4891b0 refs/heads/main`.

## Planning main path witness

Exact output of `git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep evidence/r28-welle4-2026-11-21/mcp-perses-tool-drift/review-1-headbdc7c1a9.md` before final evidence push:

```text
From https://github.com/mcpdev80/baseharbor-plan
 * branch                main       -> FETCH_HEAD
evidence/r28-welle4-2026-11-21/mcp-perses-tool-drift/review-1-headbdc7c1a9.md
```

## Planning remote
`git -C /home/marcel/dev/baseharbor-ecosystem/workers/codex-rev-1747-plan-wt remote -v`:
```text
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```
