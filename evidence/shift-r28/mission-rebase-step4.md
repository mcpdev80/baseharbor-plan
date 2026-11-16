# Mission: rebase-welle SCHRITT 4 — four dashboard followers <- new selection-head

## Context

Rebase wave (r28) step 4: fold the NEW Perses selection head into the four
dashboard follower branches. The selection head advanced via a merge-commit
(`8ce0df9` = merge of `a270725` + seam head `492b8e8f`); each follower was cut
from an earlier selection head and must receive the new content via a plain
merge (no rebase, no force). Protocol from mission-rebase-step4.md:

- working-branch from the old head
- merge the selection head (NO rebase/force)
- conflicts handled minimally, bidirectionally preserving both sides, file-by-file
- per branch: `go build` + targeted perses/metrics tests, verbatim
- normal merge-commit-push (PR heads follow; drafts stay drafts)
- deliver akte + END with all four NEW head SHAs

## Repo / provenance

- Product repo under work: `mcpdev80/baseharbor` (https://github.com/mcpdev80/baseharbor)
- Working zone (my own persistent shallow clone): `/tmp/opencode/step4-wt`
- Planning repo for evidence: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan` ONLY (NOT workers/baseharbor-plan)
- Base ref I cut from = the current remote selection head (verified via ls-remote before first push)

## Selection head (target) — VERIFIED via ls-remote

- `lane-0428-080-r28-perses-selection` = `8ce0df9148e4f388ba18386e3b731f1fc2cbd500`

## The four followers — VERIFIED via ls-remote + gh pr view

- (A) `perses-dashboard-databases-lane` (#1597) = `7f3a25a0b454adec9fba3beb5b0e3d0e2ba6b89f`
- (B) `lane-0428-077-r28-perses-dashboard-hosts` (#1602) = `ca8181c0eccbaa5a9541307171b0e64a302e30a0`
- (C) `lane-0428-079-r28-perses-messaging` (#1603, headRefName via gh pr view) = `c385abe4e451ff50df997c86d7420dcb2c4bb1aa`
- (D) `wt-0428-081` (#1604 valkey, headRefName via gh pr view) = `8221f51b60415ecf7d28adc9bd56debf798023f8`

## MERGE ANALYSIS (merge-base vs selection; disjoint file sets = clean merge)

- (A) merge-base = `a270725`; selection adds 3 files (perses.go, perses_test.go, perses_contract_test.go); lane adds 10 files (dashboards*, status_result*, cli_test*, testdata). NO overlap. Expected: clean.
- (B) merge-base = `85b4cbb`; selection adds 3 files; lane adds 10 files (hosts* dashboards, status_result*, cli_test*, testdata). NO overlap. Expected: clean.
- (C) merge-base = `0e9ccb5` (older develop); selection adds 3 files; lane adds 3 files (messaging*, testdata). NO overlap. Expected: clean.
- (D) merge-base = `a270725`; selection adds 3 files; lane adds 3 files (valkey*, testdata). NO overlap. Expected: clean.

## PLAN (numbered)

1. Re-verify all five remote SHAs via `git ls-remote` immediately before any write (as the mission requires before every merge).
2. Confirm C/D branch headRefNames via `gh pr view` (done above).
3. For each branch in order A->B->C->D (sequential):
   a. Create a local working branch from the current follower head.
   b. Merge the selection head into it (plain merge; no rebase/force).
   c. If conflicts: resolve minimally, bidirectionally preserving both sides, file-by-file; document each.
   d. Run `go build` and targeted perses/metrics tests verbatim; capture output.
   e. Commit the merge (normal merge commit) and push to the follower branch (PR head follows; draft stays draft).
4. Do NOT edit any `.github/**` file, never trigger reruns/workflow_dispatch, never force-push, never develop-merge, never ready_for_review, never add features.
5. Write the akte to `evidence/r28-welle1-2026-11-15/rebase-wave/step4-dashboards.md` with a numbered list, 8 SHAs (before/after via ls-remote), test outputs, cleanliness.
6. Verify evidence is on origin/main via `git ls-remote origin HEAD` (paste exact output) before END.
7. Post END with all four NEW head SHAs.

## repo-rule compliance

- No subagents (§4.8): every step run in this session.
- No `.github/**` edits; no force-push; no develop-merge; no ready_for_review; no feature additions.
- One integration candidate per chain: working only on the named branches.
- Reality witnesses via `git ls-remote` / fresh shallow clone in `/tmp/opencode/step4-wt` only (never the quarantined workers/baseharbor checkout).
- Evidence files live only in baseharbor-plan, never in a product repo.
- Working tree stays under /tmp/opencode/step4-wt (fixed workspace layout).

## END status

- STATUS: BLOCKED (awaiting)
