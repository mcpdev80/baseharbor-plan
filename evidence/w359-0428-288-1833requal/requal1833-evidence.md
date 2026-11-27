# w359 — Consumer requalifications #1833 (card 0428-288) and #1855 (card 0428-078)

Lane session: w359-0428-288-1833requal (part 1) / w359-0428-078-1855requal (part 2, owner-ordered follow-up task in same session)

# Part 2 — w359-0428-078-1855requal: Consumer requalification PR #1855 (card 0428-078)

Baseline #1867 landed → BLOCKED-BASELINE blocker lifted. Transport + CI only, NO merge.

## PLAN (part 2)

- gh pr view 1855 → headRefName/headRefOid; fetch origin develop + branch w279-0428-078-pr1650-reissue
- Create worktree baseharbor/workers/worktrees/w359-0428-078-1855requal on origin/<branch>
- Canonical lane identity w359-0428-078-1855requal, env GIT_* unset, 4-field verify BEFORE merge commit
- Base attestation: exact develop SHA, ancestor state, diff --name-only, log base..HEAD
- git merge origin/develop forward-only under lane identity
- Prechecks format/vet/build ONLY
- Push HEAD:<branch> no force; ls-remote delivery witness
- Watch fresh pull_request run to terminal (Trusted Plan must use landed catalog rows)
- PR comment head FULL40 + run id
- Evidence to baseharbor-plan via isolated plan worktree + PR
- Cleanliness; END with pair history (70c005e8/alt + neu/neu)

## Identity block (part 2)

- Mission identity: `w359-0428-078-1855requal` / `w359-0428-078-1855requal@users.noreply.github.com`
- Gate witness (git var, GIT_* env unset, before merge):

```
author: w359-0428-078-1855requal <w359-0428-078-1855requal@users.noreply.github.com> 1795735884 +0100
committer: w359-0428-078-1855requal <w359-0428-078-1855requal@users.noreply.github.com> 1795735884 +0100
```

## PR state at start (part 2)

```
baseRefName: develop
headRefName: w279-0428-078-pr1650-reissue
headRefOid:  70c005e8bc48b6186da1095a183905a42ee6c493
isDraft: false  state: OPEN
title: fix(0428-078): reissue Perses identity-keycloak (reviewed content, single-lane)
```

## Base attestation (part 2)

`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop` → `c167fa5dd323ae0746385caa2bdb8364ec7ad03f`

Before merge, `git merge-base --is-ancestor origin/develop HEAD` → NEEDS MERGE (head 70c005e8b behind, as mission stated).

`git log --oneline origin/develop..HEAD` after merge: 18 commits, all in the card 0428-078 chain (70c005e8b/fe940dc31/d5545573a/879655f07/18ccd8ea8/f13d37d4c/77bd785cb/8635ba07f/81a49dff6/d0b0f0b70/eb45c655b/adb7cfd10 + earlier chain commits + this lane's merge commit d18e4b367). No foreign candidate commits.

`git diff origin/develop...HEAD --name-only` (card content vs develop):

```
cmd/baha/app_identity_dashboard_status_test.go
cmd/baha/app_perses_cli_test.go
cmd/baha/app_status_result.go
internal/identityprovider/keycloak_realization.go
internal/identityprovider/keycloak_signal_attribution_test.go
internal/metrics/identity_dashboard_witness.go
internal/metrics/identity_dashboard_witness_test.go
internal/metrics/perses_dashboards.go
internal/metrics/testdata/perses-dashboards/keycloak-identity.json
internal/runtime/project_names.go
scripts/pr-gate-coverage.json
```

Merge: `git merge --no-edit origin/develop` (ort, no conflicts), absorbed only scripts/pr-gate-coverage.json (+140 develop rows). Merge commit d18e4b367940ad5ee36862dbda1eea2d7a605db0 with 4-field identity `an=ae=cn=ce=w359-0428-078-1855requal <...@users.noreply.github.com>` (GIT_* env unset at invocation). Ancestor test after merge: PASS develop c167fa5dd is ancestor of candidate.

Prechecks: gofmt clean on all changed Go files; `go vet ./cmd/baha/ ./internal/identityprovider/ ./internal/metrics/ ./internal/runtime/` clean; `go build ./...` clean; pr-gate-coverage.json parses. No local test runs.

Push: `git push origin HEAD:w279-0428-078-pr1650-reissue` → `70c005e8b..d18e4b367` (fast-forward, no force). ls-remote witness: refs/heads/w279-0428-078-pr1650-reissue = d18e4b367940ad5ee36862dbda1eea2d7a605db0 (refs/pull/1855/head refreshes with GitHub-side delay).

## Hosted CI run (part 2)

Run `45911769054`, event `pull_request`, head `d18e4b367940ad5ee36862dbda1eea2d7a605db0` (attempt 1, dispatched by the push). Watched by this lane to terminal: status `completed`, conclusion `failure` — `PR Selected Checks` FAILURE.

Failed checks (2) with failing log lines:

```
--- FAIL: TestKeycloakSignalRegistrationTargetProductionAttribution (0.00s)   [identity-provider-package-tests + Go unit · packages]
    keycloak_signal_attribution_test.go:74: attribution root = "docker-dev", want the producer's state root "/tmp/TestKeycloakSignalRegistrationTargetProductionAttribution3197917589/001/targets/docker-dev"
--- FAIL: TestIdentityDashboardWitnessPositiveMatchesConcreteTarget (0.00s)    [Go unit · packages]
    identity_dashboard_witness_test.go:144: the witness must be non-forgeably available for the concrete matching Target, got {SelectionConfirmed:true MetricPresent:false MetricCurrent:false TargetAuthorized:true Available:false}
--- FAIL: TestIdentityDashboardWitnessTwoValidTargetsIsolation (0.00s)
--- FAIL: TestIdentityDashboardWitnessTwoValidDottedTargetsIsolation (0.01s)
--- FAIL: TestIdentityDashboardWitnessForeignTargetFailsClosed (0.00s)
--- FAIL: TestIdentityDashboardWitnessRootAttributionResolvers (0.00s)
```

All Native runtime gates executed SUCCESS (no runner problem) — Trusted Plan used the landed catalog rows; gate durations confirm real execution:

```
23:36:17 -> 23:41:55  success  docker · identity
23:36:17 -> 23:43:39  success  docker · observability
23:36:17 -> 23:43:52  success  podman · observability
23:36:17 -> 23:56:43  success  docker · data-capabilities (~20 min)
23:36:17 -> 23:58:04  success  podman · data-capabilities (~22 min)
23:34:51 -> 23:35:01  success  PR · Trusted Plan
23:35:03 -> 23:35:09  success  PR · Demo Pin
23:35:03 -> 23:36:15  success  PR · Exact Candidate
```

Pin note (coordinator disposition): run started 2026-11-26T23:34:49Z, BEFORE the Demo-Pin update to b411277 landed on develop; the run's Demo Pin check validated the then-current pin, unrelated to the failures.

Pair history: 70c005e8bc48b6186da1095a183905a42ee6c493 (old head, run 45872372065 failure) + d18e4b367940ad5ee36862dbda1eea2d7a605db0 (new head, run 45911769054 failure). Both real test failures, consistent with the missing #1819 producer seam. Per owner disposition: NO retry, NO new head until the #1812→#1819→#1820 chain lands serially.

## Cleanliness (part 2)

- Worktree baseharbor/workers/worktrees/w359-0428-078-1855requal (branch w359-requal-1855, pushed ONLY to PR head branch w279-0428-078-pr1650-reissue — one candidate per chain).
- No docker/podman/compose projects started on this host or SSH hosts; `docker ps -a` on coordinator host empty (witness in part 1 section). Lane now PARKED per owner disposition — nothing new started.
- PR comment posted: https://github.com/mcpdev80/baseharbor/pull/1855#issuecomment-7205681900

## END (part 2)

END_BLOCKED w359-0428-078-1855requal: #1855 head d18e4b367940ad5ee36862dbda1eea2d7a605db0 run 45911769054 FAILURE (Go packages + identity-provider attribution tests; all Native runtime gates SUCCESS); parked pending #1812→#1819→#1820 serial landing — owner disposition 18:0xZ, no retry, no new head.

# Part 1 — w359-0428-288-1833requal — Consumer requalification PR #1833 (card 0428-288)

Lane: w359-0428-288-1833requal (session e6ca7696-b1f8-492d-b226-876b16925fc5)
Mission: coordinator/missions/w359-0428-288-1833requal.txt
Date: 2026-11-26/27. Transport + CI only, NO merge.

## PLAN

- Read mission file; establish work plan in board file (workers/todos/w359-0428-288-1833requal.json), this akte, todo tool if native
- Verify git remotes resolve to github.com/mcpdev80; read card 0428-288 frontmatter owner identity verbatim from origin/main
- gh pr view 1833 → headRefName + headRefOid; fetch origin develop and that branch
- Create worktree baseharbor/workers/worktrees/w359-0428-288-1833requal on origin/<branch> as branch w359-requal-1833
- Set worktree git identity BEFORE any commit; paste git var author/committer gate
- Record base attestation: exact origin/develop SHA, ancestor state, diff --name-only, log base..HEAD
- git merge origin/develop forward-only under lane identity
- Prechecks format/vet/build ONLY (no local tests on this host)
- Push HEAD:lane-0428-288-compose-ids (no force); prove delivery via git ls-remote
- Watch fresh pull_request run to terminal; record every required check conclusion
- Post PR comment with new head FULL40 + run id
- Publish this evidence via plan PR
- Cleanliness witnesses; END line

## Identity block

Card: tasks/t-20261116-r28-bug-compose-service-ids.md (card_number 0428-288) frontmatter `owner:` verbatim (from origin/main b9688a54d): `w147-0428-288-pr1833-fix`. No `(lane X)` marker present. The mission file for this requalification lane explicitly orders the lane identity used for the merge commit:

- git user.name: `w359-0428-288-1833requal`
- git user.email: `w359-0428-288-1833requal@users.noreply.github.com`
- Invocation: `git -c user.name=w359-0428-288-1833requal -c user.email=w359-0428-288-1833requal@users.noreply.github.com merge --no-edit origin/develop`
- Gate witness (git var, before merge commit):

```
author: w359-0428-288-1833requal <w359-0428-288-1833requal@users.noreply.github.com> 1795734017 +0100
committer: w359-0428-288-1833requal <w359-0428-288-1833requal@users.noreply.github.com> 1795734017 +0100
```

- Pre-push identity line (`git show -s --format='%h an=%an cn=%cn' HEAD`):

```
d88ebc934 an=w359-0428-288-1833requal cn=w359-0428-288-1833requal
```

## Remote resolution witness

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` (planning repo verified before evidence work):

```
origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)
origin	https://github.com/mcpdev80/baseharbor-plan.git (push)
```

`git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor remote -v`:

```
lane-origin	https://github.com/mcpdev80/baseharbor.git (fetch) [blob:none]
lane-origin	https://github.com/mcpdev80/baseharbor.git (push)
origin	https://github.com/mcpdev80/baseharbor.git (fetch) [blob:none]
origin	https://github.com/mcpdev80/baseharbor.git (push)
upstream	https://github.com/mcpdev80/baseharbor.git (fetch)
upstream	https://github.com/mcpdev80/baseharbor.git (push)
```

All remotes resolve to github.com/mcpdev80; pushes used `origin` after this resolution.

## PR state at start

`gh pr view 1833` (before push):

```
baseRefName: develop
headRefName: lane-0428-288-compose-ids
headRefOid:  0898ab4108ebda24b46a468849a57f83d4eb3a1b
isDraft: false  state: OPEN
```

## Base attestation

`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/heads/lane-0428-288-compose-ids`:

```
c167fa5dd323ae0746385caa2bdb8364ec7ad03f	refs/heads/develop
0898ab4108ebda24b46a468849a57f83d4eb3a1b	refs/heads/lane-0428-288-compose-ids
```

Baseline note: mission names chain baseline develop dff8c9e3 (#1870 merged, runtime_specific rows live); current develop tip at fetch was c167fa5dd (#1872 merged after). Branch cut from `origin/lane-0428-288-compose-ids` @ 0898ab410 (the PR head itself — this is the transport of the existing card candidate, per mission).

`git merge-base --is-ancestor origin/develop HEAD` before merge: FAILED (develop not yet ancestor → merge required, forward-only).

After merge, `git log --oneline origin/develop..HEAD` (own commits first, all are this card's chain + this lane's merge):

```
d88ebc934 Merge remote-tracking branch 'origin/develop' into w359-requal-1833
0898ab410 Merge remote-tracking branch 'origin/develop' into absorb-develop
a7b0a4804 Merge remote-tracking branch 'origin/develop' into lane-0428-288-compose-ids
b9d312bce 0428-288: drop redundant pr-gate-coverage rows ... (this card's prior rounds)
9e6b2957f Merge remote-tracking branch 'origin/develop' into lane-0428-288-compose-ids
392649532 docs(coverage): catalogue workload service-ID fix sources in trusted gate catalog
92d3267eb refactor: move canonicalComposeServiceID to manifest_validation.go ...
4064a6317 fix(application): match manifest workload component IDs ...
```

`git diff origin/develop...HEAD --name-only` (card content vs develop):

```
internal/application/manifest_validation.go
internal/application/workload.go
internal/application/workload_test.go
```

## Merge

`git merge --no-edit origin/develop` (lane identity), ort strategy, no conflicts:

```
Merge made by the 'ort' strategy.
 scripts/pr-gate-coverage.json | 140 ++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 140 insertions(+)
```

Merge commit d88ebc934 carries lane author=committer (see identity block). Candidate final head FULL40: `d88ebc9348a1cd0c6f3859c5d3a7e7d52277ed3d`.

## Prechecks (non-test only)

- gofmt -l on the three changed Go files: clean (exit 0)
- go vet ./internal/application/: clean (exit 0)
- go build ./...: clean (exit 0)
- scripts/pr-gate-coverage.json parses: json-ok
- No local test runs on this host (CI policy 2026-11-26).

## Push + delivery witness

`git push origin HEAD:lane-0428-288-compose-ids` → `0898ab410..d88ebc934` (fast-forward, no force).

`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-288-compose-ids refs/pull/1833/head`:

```
d88ebc9348a1cd0c6f3859c5d3a7e7d52277ed3d	refs/heads/lane-0428-288-compose-ids
0898ab4108ebda24b46a468849a57f83d4eb3a1b	refs/pull/1833/head
```

(PR refs/pull/1833/head refreshes on GitHub's side with a short delay; branch head is authoritative for the PR head.)

## Hosted CI run

Run `45908378759`, event `pull_request`, head `d88ebc9348a1cd0c6f3859c5d3a7e7d52277ed3d` (attempt 1, first run of this head — dispatched by the push, no rerun, no close/reopen needed). Watched by this lane to terminal: `gh run watch 45908378759` exited 0, run status `completed`, conclusion `success`.

Requalification signal confirmed: with the runtime_specific:true rows now on develop (via merged #1870), the targeted runtime selection executed — both Selected Runtime jobs ran (not skipped):

- PR · Selected Runtime (atomic/docker/data-capabilities, docker, data-capabilities) / Executed docker · data-capabilities — SUCCESS
- PR · Selected Runtime (atomic/podman/data-capabilities, podman, data-capabilities) / Executed podman · data-capabilities — SUCCESS

Full check matrix (all executed jobs SUCCESS; the `PR Selected Checks` aggregate is SUCCESS; skipped jobs are not selected by this head's paths, per Trusted Plan):

```
SUCCESS  Workflow policy
SUCCESS  PR · Trusted Plan
SUCCESS  PR · Native gate plan
SUCCESS  PR · Source format
SUCCESS  PR · Runner Interface
SUCCESS  PR · Demo Pin
SUCCESS  PR · Validation · go-vet
SUCCESS  PR · Validation · go-build
SUCCESS  PR · Exact Candidate
SUCCESS  PR · Focused Python
SUCCESS  PR · Go unit · packages
SUCCESS  PR · Go unit · owner
SUCCESS  PR · Go unit · cli-0 / cli-1 / cli-2 / cli-3
SUCCESS  PR · Selected Runtime (atomic/docker/data-capabilities, docker, data-capabilities) / Executed docker · data-capabilities
SUCCESS  PR · Selected Runtime (atomic/podman/data-capabilities, podman, data-capabilities) / Executed podman · data-capabilities
SUCCESS  PR Selected Checks  (aggregate)
SKIPPED  validate, Release Source Preflight, Targeted HA · docker/podman, Targeted · Workstation onboarding,
         PR · Draft source and routing, PR · Draft Go, PR · Main release source/Go/checks,
         PR · Exact full Pre-Release, PR · Native · matrix, PR · Native Keycloak/Core, PR · Public Contracts,
         PR · Selected Core-less, PR · Consumer Pins, PR · Candidate-added checks (advisory)
```

PR state at terminal: `isDraft:false`, `state:OPEN`, `headRefOid d88ebc9348a1cd0c6f3859c5d3a7e7d52277ed3d`. PR comment posted: https://github.com/mcpdev80/baseharbor/pull/1833#issuecomment-7205211566

Pair note: this mission orders ONE fresh run on the new merged head (the prior pair evidence lived on the old heads; the new candidate is d88ebc934). Run 45881654916 (success) belonged to the pre-merge head 0898ab410 and is recorded only as historical.

## Cleanliness

- Plan PR note: my first PR · validate run failed on PRE-EXISTING main drift (evidence/w350-0428-359-batchhop2/akte.md checkboxes, lines 21-25, landed via 8a0dcac2a, foreign lane) — not my file. My branch was rebased onto current main and re-committed as one clean commit 2ee92fad8 with lane identity (an=cn=w359-0428-288-1833requal); the red foreign-author rebase artifact e777f1ca0 was discarded by force-update of my own branch ref only.
- Plan PR #166 STATE: `Plan · validate` FAIL, run 45910939028, failing lines: `error: evidence/w350-0428-359-batchhop2/akte.md: checkbox outside tasks/ would become a CardBoard card (lines 21-25)` (5 errors, all in that foreign file, already on main). My diff touches only evidence/w359-0428-288-1833requal/requal1833-evidence.md (checkbox-free, verified by scan). Fixing the foreign file is outside my write-set: reporting to coordinator instead of editing.

- No docker/podman/compose projects were started on this host or any SSH test host (mission names none).
- Worktree: baseharbor/workers/worktrees/w359-0428-288-1833requal (kept until Maintainer disposition; branch w359-requal-1833 pushed only to the PR head branch — exactly one candidate branch per chain).
- `docker ps -a` witness on this host: no containers (empty output, no compose project started or left by this lane; no SSH test host used — mission names none).
- Delivery re-witness before END: `git ls-remote` shows refs/heads/lane-0428-288-compose-ids AND refs/pull/1833/head both at d88ebc9348a1cd0c6f3859c5d3a7e7d52277ed3d; candidate 4-field identity `an=w359-0428-288-1833requal ae=w359-0428-288-1833requal@users.noreply.github.com cn=... ce=...`; PR isDraft=false; run 45908378759 event=pull_request head=d88ebc934... conclusion=success.

## Handoff

- PR: https://github.com/mcpdev80/baseharbor/pull/1833 (OPEN, not draft)
- New head: d88ebc9348a1cd0c6f3859c5d3a7e7d52277ed3d
- Run: 45908378759 (state recorded above when terminal)
- NO merge performed (mission).

- Next task in same session: #1855 requalification uses its own canonical identity w359-0428-078-1855requal (Part 2 of this akte).

## END (part 1)

END_DONE w359-0428-288-1833requal: #1833 hopped onto develop c167fa5dd, candidate d88ebc9348a1cd0c6f3859c5d3a7e7d52277ed3d, run 45908378759 pull_request SUCCESS incl. both Selected Runtime (docker+podman) gates; identity lane w359-0428-288-1833requal an=cn verified; no merge.
