# Plan PR #213 exact-head review

## PLAN

1. Verify PR #213 full current head, exact-head Validate run, and patch file set.
2. Compare the #212 correction text and #213 additional witness lines in the akte on main and candidate; require both in the candidate.
3. If all review and hosted-check conditions pass, post verdict and merge normally; otherwise hold and report the exact discrepancy.
4. Refresh Plan main, verify merge commit and run `scripts/plan.py check` with zero errors.
5. Record final findings, update the board, verify the evidence path on main, and post Codeman END last.

Status: in progress.

## Final review and landing

- The mission-start head `8db2a1556` advanced before the first review readback to `114fddd2d56522eb9c7ce7da7cf94cb202ed1582`; its exact-head Validate run `45973982816` was completed SUCCESS.
- During the merge command, the branch advanced again to `e1de610cdcd7123a8ab2d3ef826cd97e106f3db1` by absorbing live main. The PR check result at that point was green; post-merge Actions API confirms run `45974189062` is completed SUCCESS on that exact final head. A final readback confirmed the merged patch is still only `evidence/w394-0428-249-1812diag/akte.md`.
- The final Akte on main retains #212's `origin/main presence witness` block and #213's `Coordinator follow-up 09:30Z` witness section, including the corrected delivery history and follow-up validation. Final Akte blob at merged main: `4e64cfd778c3d74b39b7ce262a8d2c8cac310d39`.
- PR #213 merged normally at `2026-11-27T09:30:52Z`; merge commit and refreshed `origin/main`: `9da6740a94b28a1aeb46afc37a38924d5d0105a0`.
- Post-merge `python3 scripts/plan.py check` on that main SHA: 784 tasks, 7 epics, 13 releases, 24 decisions; 0 errors, 10 warnings.

Verdicts: (1) YES, #212 correction and #213 witness additions are both present on final main; (2) YES, PR file set is the single Akte file; (3) YES, main `9da6740a94b28a1aeb46afc37a38924d5d0105a0`, Plan check 0 errors.

The 0428-249/#1812 release chain now has the final-witness Akte on Plan main.

END_DONE w255-0428-251-demo170codex: PR #213 merged with both witness blocks retained; Plan check green on main `9da6740a94b28a1aeb46afc37a38924d5d0105a0`.

## Evidence PR base attestation and commit identity

- Planning remote witness: `origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`; only the GitHub baseharbor-plan URL is used.
- Exact base before branch creation: `9da6740a94b28a1aeb46afc37a38924d5d0105a0` (`origin/main`).
- Card owner verbatim from that base: `owner: w362-0428-249-1812rebase` in `tasks/t-20261122-runtime-image-registry-artifact-unknown.md`; this PR is evidence-only, not card content.
- Commit user.name and user.email: `w255-0428-251-demo170codex` and `w255-0428-251-demo170codex@baseharbor.local`.
- Literal commit invocation: `git -c user.name=w255-0428-251-demo170codex -c user.email=w255-0428-251-demo170codex@baseharbor.local commit -m 'evidence: review Plan PR 213 exact head'`.
- Before-push author gate: `git show -s --format=%an HEAD` must print `w255-0428-251-demo170codex` exactly.
