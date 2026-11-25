# w232-0428-284-1842hop — PR-HOP #1842 onto develop fcd449117 (card 0428-284)

Mission: `coordinator/missions/w232-1842-hop.txt`. Scope: develop hop ONLY so the candidate stops drifting; the 14-LIGHT-GATE qualification stays parked at the demo-CI owner gap. Owner correction 2026-11-25 (in-lane): NO workflow_dispatch, NO only_gates, NO pre-release trigger from this lane — #1842 = Core demo-ref pin update + hop + exact-head Hosted PR-event CI + END. No merges, no cards, no `.github/**` edits.

## PLAN

1. Resolve real github remotes (`git remote -v`) + ls-remote triple-witness for refs/heads/develop, refs/heads/main, refs/pull/1842/head — done
2. Checkout `refs/pull/1842/head` (48bac372f…) first, never detached develop — done
3. Read card 0428-284 frontmatter owner VERBATIM from planning origin/main; record identity + `git -c` invocation in the visible ANSATZ block — done
4. `git merge origin/develop` (fcd449117) with canonical identity via `git -c`; print gates (merge-base ancestry, log --oneline, diff --name-only) — done
5. Payload proof: develop...HEAD = card write-set, non-empty, no stale catalog rows added (#1852 lesson) — done
6. NORMAL push to the existing PR #1842 branch; ls-remote delivery witness — done
7. Watch the fresh pull_request run to terminal; executed check census; run IDs — done
8. Evidence akte in baseharbor-plan (isolated worktree), prove on origin/main, END post — done

## ANSATZ — candidate commit identity (visible block)

- Card frontmatter owner VERBATIM (fetched at runtime from origin/main, `tasks/t-20261125-0428-284-1812-postretry-gate-failure.md`): `owner: w198-0428-284-demo-parser`. No `(lane X)` marker present, so the full owner value is the canonical string. The card's ownership-transfer record (coordinator, owner ledger 2026-11-28) confirms `w198-0428-284-demo-parser` is the EXACT identity for every new 0428-284 commit; historical w177 commits stay under original authorship (fix-forward, no rewrite).
- git user.name: `w198-0428-284-demo-parser` · git user.email: `w198-0428-284-demo-parser@baseharbor.local`
- Literal invocation used: `git -c user.name=w198-0428-284-demo-parser -c user.email=w198-0428-284-demo-parser@baseharbor.local merge --no-ff --no-edit lane-origin/develop`
- Pre-push gate line (run before push, output below): `git show -s --format=%an HEAD` → `w198-0428-284-demo-parser` (exact match — PASS)

## Remote resolution (REMOTE GUARD)

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor remote -v` (first git action):

```
lane-origin  https://github.com/mcpdev80/baseharbor.git (fetch) [blob:none]
lane-origin  https://github.com/mcpdev80/baseharbor.git (push)
origin       https://github.com/mcpdev80/baseharbor.git (fetch) [blob:none]
origin       https://github.com/mcpdev80/baseharbor.git (push)
upstream     https://github.com/mcpdev80/baseharbor.git (fetch)
upstream     https://github.com/mcpdev80/baseharbor.git (push)
```

All names resolve to the real GitHub URL; fetch/push used `lane-origin` and explicit `https://github.com/mcpdev80/baseharbor.git` for ls-remote witnesses.

Planning-repo check (wrong-zone rule): `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` →

```
origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin  https://github.com/mcpdev80/baseharbor-plan.git (push)
upstream2       https://github.com/mcpdev80/baseharbor-plan.git (fetch)
upstream2       https://github.com/mcpdev80/baseharbor-plan.git (push)
```

## Base attestation and ls-remote triple-witness (before hop)

```
fcd449117e189c555c7530b9527cd22d3f6f25ff       refs/heads/develop
cddc81b34fe13d8befdde4c487b365a0309ba428       refs/heads/main
48bac372f9f006c964309fab958e569a7ce076a0       refs/pull/1842/head
```

Taken three times (URL ×2, resolved remote name `lane-origin` ×1); all three identical. `refs/pull/1842/head` == branch head == mission-stated checkout `48bac372f…` (verified via `gh pr view 1842` headRefOid). PR: base `develop`, branch `w177-0428-284-demo-pin-1812`, state OPEN, not draft.

Worktree: `/home/marcel/dev/baseharbor-ecosystem/workers/w232-1842-hop-wt`, checked out from `refs/pull/1842/head` FIRST (detached at 48bac372f), then branch `w177-0428-284-demo-pin-1812` reset to it — never detached develop.

Pre-hop state: merge-base(develop, HEAD) = `3a2ae6b11`; develop NOT an ancestor (16 commits behind) → hop required. `48bac372f` IS ancestor of HEAD.

## The hop

- Merge: `git -c user.name=w198-0428-284-demo-parser -c user.email=w198-0428-284-demo-parser@baseharbor.local merge --no-ff --no-edit lane-origin/develop` — clean 'ort' merge, zero conflicts.
- New exact head: `996fe5ffa0afd81ffcd864ba23e6e4da4c5f5e52`
- Develop took in: `cmd/baha/app_status_result.go`, `internal/applicationbackup/identity_regression_test.go`, `internal/metrics/perses_backend_status.go`, `scripts/pr-gate-coverage.json` (+36 lines, #1852 catalog rows).

Gates printed before push:

```
git show -s --format=%an HEAD            → w198-0428-284-demo-parser        (identity gate PASS)
git merge-base --is-ancestor fcd449117 HEAD → PASS (exact fetched develop head is ancestor)
git merge-base --is-ancestor 48bac372f HEAD → PASS (prior candidate head preserved)
```

`git log --oneline lane-origin/develop..HEAD` (only own-chain commits, no foreign candidate):

```
996fe5ffa Merge remote-tracking branch 'lane-origin/develop' into w177-0428-284-demo-pin-1812
48bac372f chore(release): advance v0.4.28 demo pin to 5ca92a7 (w136 pin disposition)
0dbcee642 Merge remote-tracking branch 'origin/develop' into HEAD
1eac9ff3e fix(pr-gate): release-scoped demo-ref selector + release-scoped validator
50c6d84e6 chore(pr-gate): make demo-ref pin selection release-aware (v0.4.28)
28b82c00b chore(release): bump demo_ref pin to merged develop tip 1a3c055 (post #175 consent retry)
```

## Payload proof (develop...HEAD)

`git diff origin/develop...HEAD --name-only`:

```
docs/releases/v0.4.28.demo-ref
scripts/pr-check-runner.py
scripts/pr-gate-plan.py
scripts/test_pr_check_runner.py
scripts/test_pr_gate_coverage.py
```

Non-empty; all five are this card's write-set (demo-ref pin + release-scoped pr-gate selector/validator + their tests). `docs/releases/v0.4.28.demo-ref` = `5ca92a7cd2f746934890cfd7096a48068bdf218e` (unchanged by the hop; develop never touched the pin file since merge-base: 0 develop commits on it).

Stale-catalog check (#1852 lesson): `git diff origin/develop...HEAD --name-only -- scripts/pr-gate-coverage.json` → EMPTY. The hop carries develop's catalog exactly; this PR adds/removes no catalog rows. Structural check of the merged catalog: 301 components, zero duplicate ids, zero duplicate paths. Eight rows reference files absent from BOTH develop and this head (`cmd/baha/installation_reset_preservation_test.go`, `cmd/baha/w128_failed_apply_destroy_test.go`, `cmd/baha/w287_destroy_after_failed_apply_test.go`, `internal/application/runtime_identity_workload_fallback_test.go`, `internal/metrics/identity_dashboard_witness.go`, `internal/metrics/perses_dashboard_provision.go`, `internal/metrics/perses_dashboard_provision_test.go`, `internal/metrics/perses_dashboards_keycloak.go`) — all inherited from develop byte-identically (present in develop's catalog, files missing there too), NOT introduced or preservable-away by this hop; recorded as a FINDING for the catalog owner, not a lane fix.

## Push and delivery witness

`git push lane-origin HEAD:refs/heads/w177-0428-284-demo-pin-1812` → `48bac372f..996fe5ffa` (normal push, no force, no second branch).

`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/pull/1842/head refs/heads/w177-0428-284-demo-pin-1812 refs/heads/develop`:

```
fcd449117e189c555c7530b9527cd22d3f6f25ff       refs/heads/develop
996fe5ffa0afd81ffcd864ba23e6e4da4c5f5e52       refs/heads/w177-0428-284-demo-pin-1812
996fe5ffa0afd81ffcd864ba23e6e4da4c5f5e52       refs/pull/1842/head
```

## Hosted CI (self-run duty, §4.6) — PR-event runs only

- Run `45712217182` — `CI · Source & Quality`, event `pull_request`, head `996fe5ffa0afd81ffcd864ba23e6e4da4c5f5e52` (exact tested head), watched from queued to terminal: `completed` / `success`. Aggregate `PR Selected Checks` = success. THIS lane's own terminal exact-head run.
- Run `45666678375` — pull_request, head `48bac372f…` (pre-hop head), completed success (aggregate success). Historical chain witness only.
- The SECOND pull_request run on the exact head `996fe5ffa` is w234's zero-write close/reopen duty (in flight, boundary 2026-11-25); this lane does NOT trigger close/reopen or reruns (collision guard). Its run ID is relayed by the coordinator and cited in the END line.
- No workflow_dispatch, no gate dispatches, no pre-release triggers from this lane (mission + owner correction).

Executed census, run 45712217182 (39 jobs): EXECUTED and passed (19): Workflow policy, PR · Source format, PR · Trusted Plan, PR · Native gate plan, PR · Go unit · cli-0/1/2/3, PR · Go unit · owner, PR · Go unit · packages, PR · Focused Python, PR · Validation · ci-executor-tests, PR · Validation · ci-policy, PR · Validation · go-build, PR · Validation · go-vet, PR · Validation · pr-planner-tests, PR · Validation · receipt-execution-tests, PR · Candidate-added checks (advisory), PR Selected Checks (aggregate). Skipped-by-planner (20, correct for a scripts/docs-only diff): PR · Demo Pin, PR · Consumer Pins, PR · Public Contracts, PR · Runner Interface, PR · Exact Candidate, PR · Exact full Pre-Release, PR · Selected Runtime, PR · Selected Core-less · matrix, PR · Native · matrix, PR · Native Keycloak/Core · matrix, Targeted HA · docker, Targeted HA · podman, Targeted · Workstation onboarding · matrix, PR · Draft path jobs (4), PR · Main release jobs (3), validate, Release Source Preflight. Zero failures. Runtime gates skipped by the trusted incremental planner — expected: the diff touches `scripts/**` + the pin file, no runtime source paths.

## Cleanliness

- Host: this session's host ran NO containers from this lane. `docker ps -a` before/after (shell PID 4116514): header-only list, `count=0`. No compose projects started; nothing to bring down.
- local ci-fast-check PID 4056632 executed ~9 min, interrupted, NON-QUALIFYING, output discarded (disclosure per owner guard; superseded instruction "bash scripts/ci-fast-check.sh before push" not executed to completion — static witnesses + Hosted CI only thereafter).
- Worktree `/home/marcel/dev/baseharbor-ecosystem/workers/w232-1842-hop-wt` preserved exactly at `996fe5ffa` (git status clean); plan worktree `workers/w232-0428-284-plan` removed after this commit is pushed.

## Findings / notes

- Card frontmatter (`owner: w198-0428-284-demo-parser`) and the PR branch name (`w177-0428-284-demo-pin-1812`) diverge; per the card's recovery-transfer record the w198 string is canonical for new commits — applied here.
- The eight develop-inherited catalog rows pointing at nonexistent files (see payload proof) are a catalog-owner maintenance item; `PR · Trusted Plan` passed, so they are not currently gate-blocking.

## Evidence delivery proof (origin/main)

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep <path>` output:

```
evidence/r28-welle6-2026-11-25/0428-284-1842-hop/round-1.md
```

Committed via isolated worktree `workers/w232-0428-284-plan` (author `w198-0428-284-demo-parser`), pushed `d9d168063..d3f717bc7` to main.

END_DONE w232-0428-284-1842hop: hop head 996fe5ffa (merge of origin/develop fcd449117 into w177-0428-284-demo-pin-1812), pushed normally, PR #1842 head updated (ls-remote witness above); pull_request run 45712217182 on the EXACT head terminal success with executed census above; second exact-head PR-event run is w234's close/reopen duty (coordinator relays its run ID; not triggered by this lane per collision guard); no gate dispatches, no merges, no .github changes.
