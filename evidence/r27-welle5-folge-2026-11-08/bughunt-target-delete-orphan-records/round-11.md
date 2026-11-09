# 0427-165 r11 — landing-refresh rebase on PR #1500

- Card/mission: mission-165-refresh.md (0427-165 landing-refresh, on PR #1500 head)
- Session: `089b8a60-a030-45f2-8ff3-8596d8bcdc11` — worker lane `0427-165-refresh` (confirmed identity; the 594fd2f5 in the note is the END RECEIVER, not this session)
- Base refresh of prior rounds 1–10: linear rebase of PR #1500 head onto develop 8a2912c62.

## PLAN
- Claim task on planning card, confirm active + session identity 089b8a60 as worker lane.
- Base PR #1500 head on develop 8a2912c62; keep regression split (lock-fall without orphans / refusal) UNCHANGED.
- Push rebased head to branch 0427-165-target-delete-orphanrec (single-commit log on top of develop).
- Exact-head local run; capture raw `--- PASS: TestUpNameResumesThroughCommandEntrypoint` line.
- Write round-11.md evidence with SOP raw lines (ls-remote refs/pull/1500/head, own run-id, PASS line).
- Exact-head CI terminal-green witness.
- Post END line to coordinator 594fd2f5.

## STEP 1 — claim + identity (DONE)
- Session `089b8a60` confirmed as worker lane `0427-165-refresh` via `codeman agent list --json`.
- Card `t-20261108-bughunt-target-delete-orphan-records` state `active`, owner `lane-0427-165-refresh`, `superseded_by` field was a stale rest (removed by Owner commit 62737527); chain runs 10+ rounds on PR #1500, NOT superseded.
- planning `origin/main` at `62737527` (Owner cleaned superseded rest); round-11 evidence commit `ebc1397b` already on origin/main.

## STEP 2 — linear rebase onto develop 8a2912c62 (DONE)
- PR #1500 head (pre): `f5883e1e9897869686d9879675489bc1496c3156`.
- Branch base (merge-base) = `fea92f37` (Merge PR #1507 0427-176 lockfairness).
- develop = `8a2912c62869cc89adc35bd6680b18724c5eac8d`.
- 4 NEW develop commits since branch base:
  - `d9bf3d94` (#1516) isolate TestUpNameResumesThroughCommandEntrypoint from shared-docker contamination — card-181 fix, GELANDET.
  - `13fca4f9` (#1515) enforce lifecycle flock cross-process via validity probe (adds internal/stableid/lock_probe.go).
  - `230221700` (#1499) detect damaged deployment before generic budget check (BF-03) — touches internal/deployment/deployment_list.go.
  - `8a2912c6` (#1511) truthful owner-failure classification in batched app-list.
- Rebase `git rebase --onto origin/develop fea92f37 0427-165-target-delete-orphanrec` → applied cleanly, 0 conflicts (analysis: branch's new CollectableOrphans reads deployments/<id>/deployment.json directly and already does the exact blank/mismatched DeploymentID==folder + Target==detached-target guard the 230221700 ValidateDeploymentID/DamagedDirectoryState gate protects; listDeploymentRecords gate and the new CollectableOrphans function are independent additions, no line overlap).
- Resulting HEAD = `bf3f92a55d4d8da9c43fce36380d31771de08280`.
- Provenance: 3 own commits on top of develop (`ca112965` refuse orphan attach, `39d910d7` production target-detach regression r7, `bf3f92a5` regression split r9); merge-base == develop 8a2912c62 (is-ancestor confirmed). Nothing changed by the rebase: same 5 files, same 1206 insertions as the pre-rebase branch.
- Regression split UNCHANGED: last commit `bf3f92a5 test(cmd/baha): split lock regression from orphan refusal (0427-165 r9)`.
- Files: cmd/baha/target_definition_change_plan.go, cmd/baha/target_definition_orphan_refusal_test.go, internal/deployment/collectable_orphans_test.go, internal/deployment/deployment_list.go, internal/deployment/deployment_orphan_refusal.go.
- `go build ./...` exit 0 on exact head.

## STEP 3 — push to branch (DONE)
- Remote head was still `f5883e1e` (non-fast-forward); force-push `--force-with-lease` replaced tip.
- New remote head = `bf3f92a55d4d8da9c43fce36380d31771de08280`.
- PR #1500 now points at `bf3f92a5`, state open, mergeable, 1206+/0-, base develop.

## STEP 4 — exact-head local run (DONE, PASS witness)
- `go build -o /tmp/baha-165 ./cmd/baha` exit 0.
- `go test ./cmd/baha -run 'TestUpNameResumesThroughCommandEntrypoint' -v`:
  raw line: `--- PASS: TestUpNameResumesThroughCommandEntrypoint (0.71s)`  (witness for card-181 effect on this head).
- Full cmd/baha suite: 1451/1452 tests PASS on exact head `ef1851dc`; the ONLY failing test is `TestAppEditCommandCompleteProviderEditRunsRealLifecycle`, an infrastructure-gated Core test that requires a running, initialized OpenBao/Postgres ("existing native network lacks a protected Core or shared backend owner", app_edit_apply_test.go:957). This failure is environmental (no verified runtime on this host) and unrelated to the 0427-165 orphan-refusal change.

## STEP 5 — r11 fix: orphan-refusal test on new develop (DONE, per Owner 2026-11-09)
- CI run 42668673003 (head bf3f92a5) failed at TestTargetDeleteRefusalIgnoresUuidFolderMismatch (0.01s) in PR · Validation · go-unit-tests. Owner (FUND-HILFE) confirmed this is a REAL develop interaction, not a base regression to ignore.
- Root cause: my seedMismatchedUuidOrphan used folder name "orphan-folder" (NOT a valid UUIDv4). On develop 8a2912c62 the listDeploymentRecords gate (230221700 / BF-03 "damaged before budget", deployment_list.go:78) skips any directory whose name is not a valid UUID (ValidateDeploymentID -> stableid.ValidateUUIDv4 -> false). So the mismatched record was DISCARDED BY THE GATE BEFORE the embedded-DeploymentID mismatch could surface; the owner-missing guard never fired and the ownerless detach was accepted (test line 241).
- Fix (path a, Owner's guidance): rebuilt the fixture to use a VALID UUIDv4 folder name `77777777-7777-4777-8777-777777777777`. The record still carries a PRESENT deployment.json (so DamagedDirectoryState returns false — NOT damaged state, which only fires when deployment.json is missing AND protected runtime state exists, damaged_state.go:185-196), and the ONLY differing detail is the embedded DeploymentID "22222222-..." != folder name — a genuine tolerance case, never a damaged signature. On new develop the record is now LISTED by listDeploymentRecords, the mismatch guard excludes it from CollectableOrphans (F2 holds), and the owner-missing guard still refuses the detach (fail-closed).
- Commit ef1851dc (single commit on top of bf3f92a5); pushed to 0427-165-target-delete-orphanrec; PR #1500 now at ef1851dc, mergeable. No .github/** touched, regression split r9 unchanged, PR orphan-refusal goal unchanged.
- Verified locally post-fix: TestTargetDeleteRefusalIgnoresUuidFolderMismatch PASS; TestTargetDeleteRefusalIgnoresBlankIdentity PASS; TestTargetDeleteRefusesWhileCollectableOrphansAttached PASS; TestTargetDeleteRefusalIsJSONFriendly PASS. Full cmd/baha (minus the infra-gated Core test) ok (354.8s).

## STEP 6 — CI exact-head terminal-green (STATE: CI not auto-dispatching; Owner decision needed)
- Exact-head CI = pr_selected_final / "PR Selected Checks" in .github/workflows/ci.yml (816). Provenance guards: linear integration commit (EXPECTED_INTEGRATION == github.sha), exact parents (parents[2]==head OR integration==head), event==pull_request AND base_ref==develop, pinned pr-plan.json.
- Branch push to 0427-165-target-delete-orphanrec did NOT auto-dispatch CI: 0 PR#1500 runs observed across 5 polls (75s) post-push (rate limit healthy, core remaining 54). PR #1500 already had prior runs; the pull_request trigger is not re-firing on this branch this shift.
- This worker lane CANNOT trigger the hosted run (workflow_dispatch / rerun = Owner scope, AGENTS 3.8/4.6; mission forbids .github/**, reruns, workflow_dispatch). No .github/** edited, no rerun, no ruleset change.
- Local exact-head witness is complete (go build ok; TestUpNameResumesThroughCommandEntrypoint PASS; 1451/1452 cmd/baha tests pass; r11 fix verified). The exact-head CI terminal-green witness is the ONE unverified item pending an Owner-hosted run.

## SOP raw lines
- ls-remote refs/pull/1500/head: `git ls-remote origin refs/pull/1500/head` -> `f5883e1e9897869686d9879675489bc1496c3156` (pre-rebase); branch remote head now `ef1851dc707cf386ccab73b6d1041a673b9f826b`.
- Own run-id: not yet obtainable — no CI run has dispatched for ef1851dc this shift (see STEP 6).
- PASS raw line: `--- PASS: TestUpNameResumesThroughCommandEntrypoint (0.69s)` (local exact-run witness on ef1851dc); `--- PASS: TestTargetDeleteRefusalIgnoresUuidFolderMismatch (0.01s)` (r11 fix).

## END
BLOCKED 0427-165-refresh: rebase + r11 fix complete and pushed (HEAD ef1851dc, 4 own commits on develop 8a2912c62, regression split r9 intact, go build ./... ok, TestUpNameResumesThroughCommandEntrypoint PASS on exact head, r11 orphan-refusal fix verified locally). Root cause of CI 42668673003: my seedMismatchedUuidOrphan used a non-UUID folder "orphan-folder" that develop's ValidateDeploymentID gate silently discards, so the owner-missing guard never fired — rebuilt fixture with a valid UUIDv4 folder so the mismatch surfaces and fail-closed refusal holds. The ONE unverified item is the exact-head CI terminal-green (pr_selected_final, ci.yml:816): the branch push did NOT auto-dispatch CI (0 PR#1500 runs post-push) and this worker lane cannot trigger it (workflow_dispatch/rerun = Owner scope, .github/** prohibition). Awaiting Owner to dispatch the hosted ef1851dc run (run-id recorded once fired) OR to confirm the local exact-head witness suffices for this refresh. No .github/** edited, no rerun, no subagent.
