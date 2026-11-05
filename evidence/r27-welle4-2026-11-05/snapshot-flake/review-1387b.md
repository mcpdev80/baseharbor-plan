# CODEX-REVIEW — PR #1387, review 1387b

Review role: CODEX-REVIEW (read-only; no merge or PR action). Review pane: `codex-luna-ch`, session `ab08e19f-3b8b-41dc-b817-41f3d8879948` (Codeman metadata reports GPT-6-Luna). Review re-run attempted on 2026-11-05.

## PLAN

1. Check whether review-1387b already exists and refresh PR #1387's head, branch ref, changed paths, and run status.
2. Re-run the named race tests and the fail-fast mutant at the mission SHA if the local environment permits.
3. Record only witnessed results; stop acceptance if the mission SHA is stale, a required current check is red, or local test execution cannot start.

## Candidate and remote witness

- The mission names PR #1387 at `d5ff9bc7b5996a74b7ecc942d6deee65d9976d67`; the prior round-2 hosted run `42026851319` is terminal SUCCESS at that exact SHA, including `PR Selected Checks`.
- Before this review rerun, PR #1387 had advanced. The current branch ref and PR head are `929584714a75d2ec82cd004d6e35d314502bd985`, base `42bfcb1cb481c9e37ecd6ce30580e27829284113`.
- GitHub compare from mission SHA `d5ff9bc7` to current head `92958471` shows one additional commit changing only `.evidence/snapshot-flake/round-2.md`. The product source/test tree is unchanged from the mission SHA, but the candidate SHA is no longer the mission SHA.
- The latest hosted run, `42028356564`, is terminal FAILURE at current head `929584714a75d2ec82cd004d6e35d314502bd985`: `PR · Validation · go-unit-tests` and `PR Selected Checks` failed. `gh run view --log-failed` could not retrieve the failure log because the configured local GitHub CLI cache is read-only. The failure status and exact head were independently visible from GitHub's run metadata and PR checks.
- GitHub branch-ref API confirms the remote head. SSH `ls-remote` could not be used because the local system SSH configuration permissions check failed.

## Focused review results

- **Two named tests under `-race -count=50`: NOT RUN.** I attempted the focused command with an overlay containing the exact mission-SHA test and production files. Compilation stopped before test execution with `disk quota exceeded` while writing Go build output. This is an environment failure, not a test failure.
- **Quiet companion `-race -count=20`: NOT RUN** in this rebind session for the same build limitation.
- **Hook-disabled mutant fail-fast with named assertion: NOT RUN** in this rebind session. Existing `round-2.md` and `scripts/mutant-proof-r2.txt` preserve the earlier claimed single-run output (`source_snapshot_test.go:252: expected change-during-read guard to abort the capture`, failure at 0.007s), but that historical proof is not a new 1387b execution.
- **Capture behavior / blobs:** the prior round-2 record says production `source_snapshot.go` was restored byte-identically after its mutant run. The current-head diff from the mission SHA contains only the evidence file, so no additional product path was added after `d5ff9bc7`.
- **Hosted run 42026851319:** terminal SUCCESS on the mission SHA, including the selected-checks job. This does not satisfy the current-head check because run `42028356564` on current PR head is red.

## Verdict: BLOCKED

The mission candidate is stale, the current PR head has a required selected-check failure, and this rebind session could not execute the focused Go tests because the local filesystem quota stopped compilation before test start. The historical round-2 evidence is preserved as historical evidence only; it cannot replace a review of the current candidate or the failed current-head gate.

## Actionable recipe

- **Owner:** PR #1387's implementation owner, on current head `929584714a75d2ec82cd004d6e35d314502bd985`.
- **Action:** inspect the failed `PR · Validation · go-unit-tests` job from run `42028356564`, correct any reproduced failure, and publish a new exact-head run with `PR Selected Checks` successful. Keep the source/test diff limited to a necessary correction.
- **Review requirement:** after a green current-head run, recheck the branch SHA, rerun both named tests with `-race -count=50`, the quiet companion with `-race -count=20`, and the hook-disabled mutant once; retain the named fail-fast assertion and recheck capture behavior.
- **Stop criterion:** do not accept while the current selected checks are red/pending, until the local run completes, or if the mutant's only red result is a generic timeout rather than the named assertion.

## repo-rule compliance

- Read-only review; no product files, PR metadata, branch, or review state was changed.
- No subagents, rerun trigger, merge, or force operation.
- The new evidence file is the only file staged for the Planning commit; unrelated untracked Planning evidence remains untouched.
