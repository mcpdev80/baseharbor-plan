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

## Scope boundary

This is a base-only refresh. Preserve the existing task changes and add the current develop ancestry. Do not change implementation or tests, `.github`, runtime/VM state, or create another PR. Use no subagents. Build caches and temporary output, if needed, stay under `/tmp/opencode/w248*`.

## repo-rule compliance

The work is limited to integrating current develop into the assigned existing branch and recording evidence. The claim is published on the Planning card before product-branch mutation. The native Todo tool is unavailable in this session; this numbered evidence checklist is the persistent plan.
