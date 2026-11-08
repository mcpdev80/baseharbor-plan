# 0427-136 app init Owner-Naht — native-hosted gate round-4 (RESUMED, trigger now met)

- Task: t-20261108-bughunt-0427-appinit-owner-seam (karte 0427-136)
- Lane: mission-136-r4 (session 594fd2f5-4e80-43b6-9841-92879146a85e)
- Trigger (owner): PR #1464 MUST be in develop. Check `git fetch origin develop && git log origin/develop --oneline | grep 1464`.
- Branch / PR: PR #1458 vs develop, head branch `fix/0427-136-appinit-owner-seam`. Candidate merge commit **6670ca4a6c8828a44cd858c8c3c0bf2c83cac902**.
- Host: this shared codeman host (coordinator server) — NO container/compose runs here.
- Evidence dir: `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan/evidence/r27-welle5-folge-2026-11-08/bughunt-appinit-owner-seam/round-4.md`

## PLAN

- Verify trigger: PR #1464 present on origin/develop.
- Confirm PR #1458 state and reachability of #1458/#1464 on develop.
- Drift-merge develop-head (incl #1464) into candidate: ancestry-clean merge commit, document the one conflict resolution.
- Push merge to candidate branch; confirm PR #1458 head == merge commit.
- `gh pr ready 1458` (already ready-for-review).
- Watch hosted native Docker + Podman cells on exact head to terminal; record run-ids, job names, PASS lines.
- Confirm full Source & Quality run terminal/green.
- ls-remote witness + publish evidence to origin/main + END.

## Candidate and remote witnesses

All remote truth measured fresh this shift via the canonical checkout
`/home/marcel/dev/baseharbor-ecosystem/baseharbor` and `git ls-remote` / GitHub
API. **The quarantined `workers/baseharbor` checkout was NOT used** (mission
warning w282 phantom-chain misread). The planning repo is `/home/marcel/dev/baseharbor-ecosystem/baseharbor-plan`
ONLY; `workers/baseharbor-plan` is a bookkeeping subdir and never committed.

- origin/develop ls-remote (witness): `201735b03145ce036407a0272882ec184943cd6a` refs/heads/develop
- origin/develop HEAD: `201735b03` `fix(cmd/baha): use/activate verifies Keycloak-bound core issuer (0427-133 r2) (#1460)`
- PR #1464 grep on origin/develop: PRESENT — `cd494610c test(ci): verify ready-PR native destroy impact and hosted proof (#1464)`
- PR #1464 state (GitHub API, this shift): MERGED, mergeCommit `cd494610c`, mergedAt `2026-11-08T11:13:50Z`.
- PR #1458 (this shift): state OPEN, isDraft false (ready-for-review), base develop, head branch `fix/0427-136-appinit-owner-seam`, head `6670ca4a6c`.
- Candidate merge commit: **6670ca4a6c8828a44cd858c8c3c0bf2c83cac902**
  - parent 1 (candidate line): `5c5e24a7c` (0427-136 r2 drift-merge, "owner HOLD - no state change")
  - parent 2 (develop head): `201735b03` (develop, incl #1464)
  - merge-base: `48d6f10ac` `ci(r27): require pinned workload and bootstrap cleanup in native runtime proof (#1462)`

## Base attestation (owner directive)

- Base ref cut from: `origin/develop` head `201735b03145ce036407a0272882ec184943cd6a` (ls-remote witness above).
- `git merge-base --is-ancestor 201735b03 6670ca4a6` => YES (develop is a merge parent).
- `git merge-base --is-ancestor cd494610c 6670ca4a6` => YES (#1464 carried in candidate).
- `git merge-base --is-ancestor 7536878d4 6670ca4a6` => YES (1458 bootstrap commit carried in candidate).
- `git rev-list --parents -n1 6670ca4a6` => `6670ca4a6 5c5e24a7... 201735b03...` (exactly two parents).
- `git log 6670ca4a6` lists ONLY this lane's commits plus the two merge parents — no foreign candidate on top.

## Trigger check (now satisfied)

- `git fetch origin develop` then `git log origin/develop --oneline | grep 1464` => PRESENT (`cd494610c ... (#1464)`).
- This differs from the prior round-4 (mission-136-r4, END_BLOCKED 2026-11-08 10:49 CET) where #1464 was still an open PR (head `3b272ff0`). #1464 has since merged (11:13:50Z) and develop has drifted to `201735b03` (incl #1460).

## Drift-merge onto current develop (owner HOLD preserved)

Worktree: `/tmp/opencode/mission-136-r4-wt` (detached at `5c5e24a7c`, my own zone under /tmp).

- `git merge --no-edit origin/develop` produced ONE conflict, in the only file PR #1458 touches:
  `cmd/baha/installation_destroy_native_test.go` (the bootstrap block added by 7536878d4).
- Conflict: candidate used an inline `runWithIO(ctx, ["up","--control-plane-only","--yes"]); ... t.Fatal(err)` while
  develop's canonical path (from drift-merge PR #1453 onto develop, gated by #1463) uses the
  `installCore(...)` helper with `runtimeUpOptions{Yes, ControlPlaneOnly, MachineRole: Development, RecoveryFile}`
  and a readiness assertion.
- Resolution (in favor of develop's canonical helper): kept the develop `installCore` block and added a
  comment noting the owner enforcement (#1347 / card 0427-056) is untouched — only its precondition changed.
  No other content touched. Verified with `git diff 201735b03 HEAD` => ONLY
  `cmd/baha/installation_destroy_native_test.go` (5 insertions, 1 deletion).
- Build/vet/compile: `go build ./...`, `go vet ./cmd/baha/`, and `go test -run xxx ./cmd/baha/` (test compile)
  all EXIT 0 on the merge commit (Go 1.26.8; go.mod pins 1.25.0).
- Commit: `6670ca4a6 Merge remote-tracking branch 'origin/develop' into HEAD` (owner HOLD wording preserved;
  no product-code state change beyond the drift-merge and the one-line conflict resolution).
- Push: `git push origin 6670ca4a6:fix/0427-136-appinit-owner-seam` => `5c5e24a7c..6670ca4a6`.
  `git ls-remote origin fix/0427-136-appinit-owner-seam` => `6670ca4a6c8828a44cd858c8c3c0bf2c83cac902`.
- PR #1458 head == `6670ca4a6c`; `gh pr ready 1458` => already ready-for-review (not a draft).

## Hosted native Docker + Podman cells — round 4 (terminal, all PASS on exact head)

Run 5207 (GitHub Actions), head `6670ca4a6c`, workflow "CI · Source & Quality".
Watched to terminal this shift. Both native destroy-retry cells ran the exact test the
1458 bootstrap targets, `TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry`
(includes the `up --control-plane-only` / `installCore` bootstrap before the owner seam).

- PR · Native destroy retry · docker — run 42476195799 / job 128718024910
  - status COMPLETED, conclusion SUCCESS, completed_at 2026-11-08T11:37:24Z
  - log line: `--- PASS: TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry (181.65s)`
  - log line: `PASS` then `ok  	github.com/mcpdev80/baseharbor/cmd/baha	181.654s`
  - log line: `PASS: native installation destroy current-scope, partial failure, retry and foreign preservation`
- PR · Native destroy retry · podman — run 42476195799 / job 128718024935
  - status COMPLETED, conclusion SUCCESS, completed_at 2026-11-08T11:37:37Z
  - log line: `--- PASS: TestInstallationDestroyCurrentChildrenInterruptedVolumeAndRetry (209.68s)`
  - log line: `PASS` then `ok  	github.com/mcpdev80/baseharbor/cmd/baha	209.693s`
- PR · Validation · cli-package-tests (all Go package tests incl. cmd/baha): SUCCESS
- Full run 5207 tally: 13 SUCCESS, 11 SKIPPED, 0 FAILURE, 0 RUNNING.
  Run terminal: `conclusion=success`, `status=completed`, `completed_at` set, `run_number=5207`, `head_sha=6670ca4a6c`.
- Job detail endpoints: `repos/mcpdev80/baseharbor/actions/runs/42476195799/jobs`
  (job 128718024910 docker, 128718024935 podman); logs: `repos/mcpdev80/baseharbor/actions/jobs/{128718024910,128718024935}/logs`.

## repo-rule compliance

- No product-code state change authored by this lane beyond the drift-merge: the only hand-written diff vs
  develop head is the one comment on the 1458 bootstrap block; the rest of the merge is develop's own drift.
- No `.github/**` workflow file edited (Owner scope). The merge auto-merged develop's ci.yml changes into the
  candidate as part of the drift — those are develop's own commits (#1460/#1464/#1463 lineage), not a lane edit.
- No rerun / workflow_dispatch issued. No runner infrastructure touched (GitHub-hosted shared runners only).
- No subagents / sub-processes used to write, push, merge, close, or check (owner directive 4.8).
- Exactly one candidate per chain: worked only on `fix/0427-136-appinit-owner-seam`; no second branch invented.
- No container/compose project started (this host is the coordinator server; none run here).

## Next trigger

No further action required for this mission. If develop drifts again after this merge, re-drift onto the new
develop head in the same candidate branch.

## END

END_DONE mission-136-r4.md — PR #1458 drifted onto develop-head (merge 6670ca4a6, #1464 + #1460 carried in),
ready-for-review, and both hosted native Docker + Podman cells PASSED to terminal on the exact head.
