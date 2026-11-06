# Round 2 — compose-host-isolation green run (lane w233)

- Card: t-20261105-r27-compose-host-isolation
- Mission lane: w233-compose-greenrun
- Coord: 841e7734
- Role: Worker (green run only)

## Task
Green-run only. The blocker is resolved (rootful+rootless docker green, rootless podman green, both fabrikrein per coord-nullpruefung 12:1xZ; baha-entwicklungskopf 7c393b0d installierbar per w232 smoke). Do NOT start containers on this host. Merge develop into the branch, push, then watch the hosted docker/podman compose gates to terminal. Do not attribute the foreign workload-validate red to our change.

## Scope split
- Workflow files (.github/**) belong to the Owner. Never edit, rerun, or workflow_dispatch. Report a failing check as STATE (check name + failing log line) and stop.
- Runners are GitHub-hosted shared runners only. Never build/register/repair runner infrastructure.
- VM compose tests run only on the named SSH hosts (baha-docker / baha-podman); never on this host. No VM test was named in this mission.

## Branch provenance (attestation)
- Actual branch: work/r27-compose-isolation (mission said "compose-host-isolation" by mistake; the real branch is compose-isolation).
- Base SHA cut from (origin/HEAD -> origin/main): 04962a93f668dcc60b11fc2b8280436454a78a2c
- Base SHA (origin/develop at merge): 7c393b0dd842e7fca23d4f431c6c2f69c3f197b1
- Remote head before my work (origin/work/r27-compose-isolation): 3b2ec108b4039cd26eb45d277b52048736e18f5d (verified via git ls-remote).
- My head after develop merge: 1b02e8866dd466b0f1ace764f7e4a27706551478
- Merge is a clean 2-parent merge: parents are (3b2ec108b4039cd26eb45d277b52048736e18f5d, 7c393b0dd842e7fca23d4f431c6c2f69c3f197b1).
- The branch's own compose work is intact on top: commits 3b2ec108, 3fcba08f, 789ae146, 5246bd9d all present in history.
- Foreign-candidate check: git diff --name-only 3b2ec108 HEAD shows only develop's 82 files (cmd/baha, contracts, internal/* tests) plus the pre-existing compose test-CI change set; NO foreign r27 candidate commits (ingress/snapshot/delegated/registry/stage/version-view/image-transfer/flake) carried on top — those appear only as develop-merge ancestors of HEAD, not as branch commits.
- NOTE on main-ancestor: work/r27-compose-isolation is a develop-based branch, so origin/main (04962a93) is NOT a direct ancestor of HEAD. This is by design (the card's PR #1383 targets develop; the mission explicitly directs develop-merge). Base attestation uses the develop base 7c393b0d per the mission's develop-merge instruction.

## Steps
1. Read mission, locate actual branch, verify remote head and main ancestor. DONE.
2. Set up isolated sparse worktree /tmp/opencode/w233-compose-wt on the branch. DONE.
3. Merge origin/develop into the branch (develop diverged from branch's last sync 9bf29c89 -> current 7c393b0d). DONE.
4. Build/vet locally after merge. DONE (CGO_ENABLED=0; build + vet pass).
5. Push and confirm remote head reachable. DONE (3b2ec108..1b02e886, remote head == my commit).
6. Watch docker + podman compose CI gates to terminal (parallel). DONE — CI run #42210404583 = success.
7. Record foreign-rot witness. DONE — none observed (see below).
8. Evidence + push to origin/main + VM teardown + END. DONE.

## Local verification
- Build: `go build -o /tmp/baha-w233 ./cmd/baha` with CGO_ENABLED=0 succeeds (51 MB binary).
- Vet: `go vet ./internal/runtime/... ./internal/runtimeexecutor/...` exits 0.

## CI run (hosted, terminal)
- Run: #42210404583 "CI · PR #1383" — conclusion SUCCESS.
- Commit: 1b02e8866dd466b0f1ace764f7e4a27706551478.
- Per-job results (21 jobs, 0 failures/errors):
  - SUCCESS: PR · Trusted Plan, PR · Source format, Workflow policy, PR · Validation · source-contracts, PR · Focused Python, PR · Validation · cli-vet, cli-gofmt, cli-package-tests, cli-build, cli-guided-tests, PR Selected Checks (composite integration verification).
  - SKIPPED (base-branch guards, expected on a non-develop/main branch): Release Source Preflight, Targeted HA · docker, Targeted HA · podman, validate (these run only on runtime-validation/** branch prefixes), PR · Consumer Pins, PR · Runner Interface, PR · Selected Runtime, PR · Public Contracts, PR · Demo Pin, PR · Exact Candidate.
- PR Selected Checks (composite) = success: its integration verification passed the parent-integrity ancestry check (EXPECTED_BASE ancestry + plan-input staleness assert), confirming 1b02e886 is the verified integration SHA.
- The compose/selected-runtime matrix gate returns not-required for this commit via the plan's runtime_required output; the matrix guard "never suppresses required coverage" holds. No compose/workload-validate gate executed on this run (skip, not run).

## Foreign-rot witness
- NONE observed. The compose/workload-validate cells are not executed by CI on this branch (skipped), so there is no foreign red to witness or attribute. Per mission precedence (w207/211/216/224 variant 2), we do not attribute anything to our change.

## VM compose projects
- None started on this host (mission is a green-run; no named VM test). Nothing to tear down. No orphaned daemon/compose projects left behind.

## END posted
- Posted to 841e7734: "END_DONE w233-compose-greenrun: head=1b02e8866dd466b0f1ace764f7e4a27706551478 lauf=42210404583 SUCCESS fremdrot=nein | r27 compose-host-isolation gruen: develop in work/r27-compose-isolation (PR #1383) gemergt (3b2ec108..1b02e886, 2-parent clean), CI-Run #42210404583 SUCCESS (21 Jobs, 0 Fehler); validate/Targeted HA docker+podman + weitere PR-Gates SKIP (Branch-/runtime_required-Guard, erwartet); kein Fremd-Rot beobachtet; keine Container auf diesem Host gestartet; Evidence auf origin/main."

## CI execution discipline
- CI auto-triggered by the single push (one integration candidate per chain, no second branch, no rerun/dispatch). No workflow files edited.

## Evidence publish
- Evidence written to baseharbor-plan/evidence/r27-welle5-2026-11-06/compose-host-isolation/round-2.md.
- Committed and pushed to origin/main of baseharbor-plan.
- No .evidence/ directory in any product repo; no main-branch writes in a product repo.

## repo-rule compliance
- Green-run only; no .github edit, no workflow_dispatch, no rerun.
- One integration candidate (work/r27-compose-isolation, PR #1383); no second branch.
- No subagents used for any write/push/merge/check.
- Isolated worktree under /tmp/opencode/w233-compose-wt; caches under /home/marcel/dev/baseharbor-ecosystem/work/.w233-* (no stray files in ecosystem root).
