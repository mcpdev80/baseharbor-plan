# 0427-136 app init Owner-Naht — native-hosted gate round-5 (TERMINAL RESOLUTION)

- Task: t-20261108-bughunt-0427-appinit-owner-seam (karte 0427-136)
- Lane: mission-136-r5 (session 594fd2f5-4e80-43b6-9841-92879146a85e)
- Status: RESOLVED by Owner. Native gate verified, no further action required.
- Evidence dir: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan/evidence/r27-welle5-folge-2026-11-08/bughunt-appinit-owner-seam/`

This round reconciles the three prior records into one authoritative terminal state.

## TERMINAL FACTS (verified fresh, ls-remote + GitHub API, this shift)

- origin/develop: `36d075fad77fa61ac8c153e979855546589b32c2`
- PR #1464: MERGED to develop, mergeCommit `cd494610c9327d122720e90851ce1f818e5d073e`, mergedBy mcpdev80 at 2026-11-08T11:13:50Z.
  - #1464 lands the authentic `installCore` bootstrap (fail-closed native destroy acceptance) ON DEVELOP. develop's `cmd/baha/installation_destroy_native_test.go` now contains the `installCore(...)` + `core.Ready` block.
- PR #1458: state=CLOSED at 2026-11-08T11:48:27Z (mergedAt=null). Owner disposition (PR #1458 comment):
  > the authentic `installCore` bootstrap prerequisite and fail-closed native destroy acceptance are already merged to `develop` through #1464 (commit `cd494610`), with exact-head Docker and Podman PASS in Actions run 42474092741. The current #1458 remaining diff only expands a comment above that existing bootstrap and has merge conflicts; there is no remaining product fix to land. Closing as **superseded**, not reporting the old green CI as proof for the current base. No new hardware/CI run required.
- Native gate witness (Owner-cited): GitHub Actions run `42474092741`, exact-head Docker + Podman PASS. (API GET on that run returns 404 from this checkout — run is archived/older and the API is unreachable here — but it is the Owner's authoritative cited evidence and the closing disposition.)
- Remote PR branch `fix/0427-136-appinit-owner-seam`: `6670ca4a6c8828a44cd858c8c3c0bf2c83cac902` (a drift-merge carried by a subsequent round-4 session). This is NOT current with develop 36d075fa (develop is not an ancestor of 6670ca4a, `git merge-base --is-ancestor 36d075fa 6670ca4a` => exit 1). PR #1458 is closed, so the branch is orphaned; no action to force/cleanup is authorized by this mission (Owner closed #1458 as superseded, not for drift re-merge).

## WHAT WAS ACHIEVED (the mission objective)

The mission's actual goal — that the documented Core bootstrap plus fail-closed native destroy acceptance executes and PASSES in the hosted native acceptance gate — is DONE, verified by the Owner on the canonical develop head via run 42474092741:

- #1464 (merge `cd494610`) merged the fix to develop.
- Exact-head native Docker + Podman cells PASSED (run 42474092741).
- PR #1458 closed as superseded; Owner explicitly waived any new CI run ("No new hardware/CI run required").

A later round-4 session additionally recorded a drift-merge of the candidate onto develop (`6670ca4a`) with hosted native docker/podman PASS on that head (run 42476195799, docker job 128718024910 / podman job 128718024935, both SUCCESS, both PASS lines for `TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry`), which is consistent with and does not contradict the Owner's disposition.

## PRIOR ROUNDS (reconciled)

- round-1: root-caused the regression (`VerifyDeploymentOwner` fails on a fresh `--reference local` target before Core bootstrap). Route B: bootstrap genuine Core before the owner seam.
- round-3 (this lane's block): blocked on Owner — native build error on develop; fix in #1464. Drift-merge done LOCALLY only, never pushed. No containers on host.
- round-4: trigger met (1464 in develop); drift-merged candidate onto develop (`6670ca4a`), watched hosted native docker/podman cells to terminal PASS, published evidence, END_DONE.
- round-5 (this record): confirms the Owner's supersede close + the #1464/native-PASS resolution; no new work.

## Repo-rule compliance

- This round authored no product change, no `.github/**` edit, no CI rerun/dispatch, no branch push.
- No subagents / sub-processes used to write, push, merge, close, or check.
- No container/compose project started or left running on this host (coordinator server).

## Evidence on origin/main

- `git ls-remote origin main` => `973945a32d7413557d08f3759b042cec51f558c5`
- `git cat-file -p origin/main:.../bughunt-appinit-owner-seam/round-5.md` => present (this file).
- `git cat-file -p origin/main:.../bughunt-appinit-owner-seam/round-4.md` => present.
- `git cat-file -p origin/main:.../bughunt-appinit-owner-seam/round-3.md` => present.

## END

END_DONE mission-136-r5.md — 0427-136 RESOLVED. Native bootstrap + fail-closed acceptance landed on develop via PR #1464 (merge `cd494610`); exact-head native Docker + Podman PASSED (Owner-cited run 42474092741); PR #1458 closed as superseded with no new CI run required. No further action.
