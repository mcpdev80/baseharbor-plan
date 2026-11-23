# PR-SWEEP #1614 — HOP-WELLE r2 (stand 1458 directive): cd9cc hop + draft->ready

Lane: w076-0428-076-1789rest (sitz: erster frei), mission /tmp/opencode/m_1614b.md.g.
Branch `lane-0428-062-cli2-app-status` (sole candidate), worktree
`/home/marcel/dev/baseharbor-ecosystem/workers/sweep-1614-hop-wt` (unchanged zone from r1).

## PLAN

1. Resolve remotes; ls-remote attest develop tip and refs/pull/1614/head (3ddf61e4).
2. `git fetch origin develop`; `git merge --no-ff origin/develop` (no force; union expected on app_* cli2 family).
3. Check: catalog byte-identical to develop; `.github` untouched; ancestry + log-line proof.
4. Push + `ls-remote refs/pull/1614/head` witness; no merge.
5. Watch exact hosted CI run to terminal; record head + run-id + gates.
6. Extra directive (stand 1458): after green cd9cc-run, `gh pr ready 1614` (DRAFT -> READY).
7. Evidence (this akte) on plan origin/main with witness; END post.

## Remote resolution (REMOTE GUARD)

`git remote -v` (first git action):

```
origin	https://github.com/mcpdev80/baseharbor.git (fetch)
origin	https://github.com/mcpdev80/baseharbor.git (push)
```

## BASE ATTESTATION

Pre-merge `git ls-remote origin refs/heads/lane-0428-062-cli2-app-status refs/pull/1614/head` → both
`3ddf61e4423d7e8f81a5e96b452984c43c323576`. `git fetch origin develop; git rev-parse origin/develop` →

```
cd9cc4836a69815a6cdcf7079902bafe5be1e000
```

Mission said "e8acf74055 oder jünger": cd9cc (current tip, includes #1792) chosen — head 3ddf61e4
on base e8acf740 was two stages old, exactly the hop target the directive names.

## Merge

`git merge --no-ff --no-edit origin/develop` → auto-merged (ort), NO conflicts this round
(#1787 broker/operatorauth + 62 #1792 catalog lines came in cleanly):

```
098d4554ed223a16f607801c61d95b1ebbb76b39 (parents: 3ddf61e4 cd9cc4836a)
```

Ancestry: `git merge-base --is-ancestor origin/develop HEAD` → exit 0.

## Konfliktliste (END requirement)

This r2 hop: KEINE konflikte (0 files). r1 union resolution (11 files) stays documented in the
same akte section below and in r28-welle5-2026-11-23/sweep-1614 (this file supersedes r1 akte;
r1 conflict table repeated here for completeness):

| File | Kind | Resolution |
| --- | --- | --- |
| cmd/baha/app_status_result.go | content | union: develop Perses/dashboard fields + our Versions fields, both setter paths |
| cmd/baha/app_workspace_source_model.go | content | take develop (per-operation authorizeWorkspaceSourceModel supersedes HEAD central auth) |
| cmd/baha/app_workspace_source_model_test.go | add/add | develop helpers/tests + our call-site adaptation (runWithIOAsTestOperator) |
| cmd/baha/machine_coverage.go | content | take develop presentation rows |
| cmd/baha/app_version_unified_test.go | call-site adaptation | runWithIOAsTestOperator (hosted-required fix after hop) |
| docs/cli/command-index.md + de twin | content | develop + regenerated via BASEHARBOR_UPDATE_MACHINE_DOCS |
| docs/{de/}reference/cli-machine-coverage.md | content | take develop; regenerated == committed |
| internal/development/source.go | content | take develop ResolveWorkspace (symlink-hardened superset) |
| internal/development/source_model_test.go | add/add | union (both sides' new tests) |
| internal/development/source_mutation.go | add/add | take develop (rollback superset; HEAD-only funcs: none) |

## Checks (step 3)

- `git diff origin/develop HEAD -- scripts/pr-gate-coverage.json` → 0 lines; `--quiet` exit 0 → byte-identical.
- `.github/**`: 0 files in branch-vs-develop diff → untouched.
- TP expectation: app_access rows (`cmd/baha/app_access.go`, `app_access_test.go`) live in trusted base (merged ingress cards), confirmed byte-identical catalog inherits them.
- uid-app/env/target lane branches no longer exist on origin (squash-merged) → content in base, as the mission predicted.
- `git log --oneline origin/develop..HEAD` → only this chain's own commits (098d4554 merge + r1 history: 3ddf61e4, 4bfc775d, 80d4df52, 6377f1b2, 03e28080, 818d572b, 63468454, 0963d08d, 98877cc1, eda0cd61).
- `git diff origin/develop...HEAD --name-only` → 24 files (the PR's own 55-file footprint minus base-consolidated files), no `.github`.

## Push + delivery witness (step 4)

`git push origin HEAD:refs/heads/lane-0428-062-cli2-app-status` → `3ddf61e4..098d4554`.
`git ls-remote origin refs/pull/1614/head refs/heads/lane-0428-062-cli2-app-status`:

```
098d4554ed223a16f607801c61d95b1ebbb76b39	refs/heads/lane-0428-062-cli2-app-status
098d4554ed223a16f607801c61d95b1ebbb76b39	refs/pull/1614/head
```

No merge performed by this lane.

## Hosted CI on exact head (step 5, Eigenes-Run-Pflicht)

- Run (DRAFT path): **45111533811**, pull_request, headSha 098d4554,
  url https://github.com/mcpdev80/baseharbor/actions/runs/45111533811
  — watched to terminal: `completed / success` (04:23:12Z → ~04:26Z).
  Executed: PR · Draft source and routing + PR · Draft Go · cli-0/cli-1/cli-2/cli-3/packages — all success.
- `bash scripts/ci-fast-check.sh` before push → exit 0 (344 python tests OK; no candidate-added checks).

## Draft -> ready + STATE of the ready-path run (step 6)

`gh pr ready 1614` → `✓ Pull request mcpdev80/baseharbor#1614 is marked as "ready for review"`;
`gh pr view` → `isDraft:false state:OPEN headRefOid:098d4554`.
The ready transition re-triggered full PR CI on the SAME head:
- Run **45112021896** — `completed / failure`. Failing checks as STATE (per scope-split rule, no reruns by lane):
  - `PR · Trusted Plan` — failed (aggregate `PR Selected Checks` → failure).
  - Cause observed via reality witness: develop tip has ALREADY moved to `7880a8f6bcfaabd8fd254ef987522abc1770c52e`
    during this window and 098d4554 is not contained in it — the classic base-moved race: the
    trusted-plan/diff base is re-resolved against a newer develop. This is exactly the condition the
    mission warned about ("fallt der tipp schon auf den dann aktuellen").
  - This is NOT a code regression from this hop: catalog byte-identical, .github untouched, same
    product diff that passed the draft path.

Disposition: per mission END ("gruener cd9cc-run" = run 45111533811 success, achieved; ready done),
this lane does NOT chase a newer-base run (CI policy: no endless hopping; a fresh develop hop is a
coordinator decision, and rulesets are disabled). Reporting as STATE: one further cd9cc/newer-tip
hop + exact run, OR a merge onto 098d4554 while the plan still admits the diff, is 1450/coordinator's
call after review->merge.

## cleanliness

- git-only hop + gh-pr-ready: no containers, compose projects, networks, volumes or VM work started.
- `docker ps -a` on this host (pid 3710689): zero containers before and after; ambient untouched.
- No files created outside the worktree and this plan-repo evidence directory.

## Evidence-on-origin/main verification (second-to-last actions)

```
<output appended after push>
```

Planning repo remote verified before first evidence commit:
`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` →
`origin https://github.com/mcpdev80/baseharbor-plan.git (fetch)`.

END_DONE w076-0428-076-1789rest: #1614 hop-wave r2 — cd9cc4836a merged --no-ff onto 3ddf61e4, new head 098d4554 (zero conflicts), catalog byte-identical, .github untouched, run 45111533811 (draft path) completed/success on exact head, PR set READY per directive; STATE: re-triggered full run 45112021896 failed PR · Trusted Plan after develop moved to 7880a8f6 (base race, not a regression) — coordinator/1450 decides newer-tip hop vs merge.
