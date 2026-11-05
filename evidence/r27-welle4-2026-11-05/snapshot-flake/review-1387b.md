# CODEX-REVIEW — PR #1387, review 1387b

Review role: CODEX-REVIEW (read-only; no merge or PR action). Review pane: `codex-luna-ch`, session `ab08e19f-3b8b-41dc-b817-41f3d8879948` (Codeman metadata reports GPT-6-Luna). Review run rechecked on 2026-11-05 against the corrected candidate head.

## PLAN

1. Refresh PR #1387 and its branch ref; confirm the corrected candidate and closed duplicate #1389.
2. Check the automatic hosted run at the corrected exact SHA through its terminal state.
3. Re-run the named focused tests and mutant if local compilation permits; record the verdict and any remaining gate.

## Candidate and remote witness

- The original mission named `d5ff9bc7b5996a74b7ecc942d6deee65d9976d67`. The corrected PR #1387 head is now `27cf86c3396b3886bbbb9b0a4b23be57ce82fd93`, base `42bfcb1cb481c9e37ecd6ce30580e27829284113`.
- GitHub branch-ref API and PR #1387 both report `work/r27-snapshot-flake` at the exact `27cf86c3` SHA.
- PR #1389 is CLOSED and points at the same head; the current review target remains PR #1387.
- GitHub compare `d5ff9bc7...27cf86c3` is two commits ahead with an empty final-tree file diff. The mistaken `.evidence/...` addition was removed by the cleanup/revert history; the product and test tree is byte-for-byte the same tree as `d5ff9bc7`.
- The earlier run `42028356564` at intermediate head `929584714a75d2ec82cd004d6e35d314502bd985` was terminal FAILURE. It is superseded as a head witness by the newer run below.

## Focused review results

- **Two named tests under `-race -count=50`:** the rebind-session replay could not compile to test start; the temporary Go build failed with `disk quota exceeded`. The prior round-2 evidence records both named tests passing at `d5ff9bc7`. Because GitHub compare confirms the corrected `27cf86c3` has the identical final tree, that prior source-level result is applicable to the unchanged code, but it was not a new local execution in this review session.
- **Quiet companion `-race -count=20`:** prior round-2 evidence records green; not newly executed in this review session for the same local build limitation.
- **Hook-disabled mutant:** prior `round-2.md` and `scripts/mutant-proof-r2.txt` record a single-run fail-fast result at 0.007s with the named assertion `source_snapshot_test.go:252: expected change-during-read guard to abort the capture`. This review session could not rerun it locally.
- **Capture behavior / blobs:** round-2 evidence records that production `source_snapshot.go` was restored byte-identically after the mutant run. GitHub compare confirms no final-tree changes between `d5ff9bc7` and `27cf86c3`.
- **Automatic hosted run 42050483534 — terminal FAILURE** at exact head `27cf86c3396b3886bbbb9b0a4b23be57ce82fd93` (event `pull_request`). `PR · Validation · go-unit-tests` failed and `PR Selected Checks` failed. `Workflow policy`, `PR · Trusted Plan`, `PR · Source format`, `go-build`, `go-vet`, and `Focused Python` succeeded; unrelated checks were skipped by workflow selection. Run URL: https://github.com/mcpdev80/baseharbor/actions/runs/42050483534.
- The failed job log was not retrievable through `gh run view --log-failed` because the configured local GitHub CLI cache is read-only. The terminal run/job statuses and exact head were read from GitHub metadata. SSH `ls-remote` was unavailable because the local system SSH configuration permissions check failed; the GitHub branch-ref API supplied the exact remote-ref witness.

## Verdict: BLOCKED

The corrected head is verified and its automatic gate run is terminal, but the required Go unit-test job and `PR Selected Checks` are red. The local focused replay also could not start. The prior `d5ff9bc7` test evidence still describes the unchanged code tree, but it cannot replace a green current-head gate.

## Actionable recipe

- **Owner:** PR #1387's implementation owner, on current head `27cf86c3396b3886bbbb9b0a4b23be57ce82fd93`.
- **Action:** inspect the failed `PR · Validation · go-unit-tests` result in run `42050483534`, reproduce and correct any test failure, then publish a new run with `PR Selected Checks` successful on the new exact head. Keep the candidate source diff limited to the proven correction.
- **Review requirement:** after the current-head gate is green, recheck the remote head, run both named tests under `-race -count=50`, the quiet companion under `-race -count=20`, and run the hook-disabled mutant once; retain the named fail-fast assertion and capture-behavior check.
- **Stop criterion:** do not accept while current `PR Selected Checks` are red/pending, until the focused local run completes, or if the mutant's only red result is a generic timeout rather than the named assertion.

## repo-rule compliance

- Read-only review; no product files, PR metadata, branch, or review state was changed.
- No subagents, rerun trigger, merge, or force operation.
- Only this evidence file changed in the follow-up Planning commit; concurrent mutation-lock and connection-client worktree changes remain untouched.
