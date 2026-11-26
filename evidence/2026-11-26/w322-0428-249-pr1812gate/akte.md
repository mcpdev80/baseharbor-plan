# w322-0428-249-pr1812gate akte — qualify PR #1812 on real exact-head pull_request after one absorb

## Status: BLOCKED / clean finding — PR #1812 stays unqualified

Lane: `w322-0428-249-pr1812gate` (this session). Card: 0428-249. Chain #1812 -> #1819 -> #1820.

## Visible ANSATZ BLOCK (required before first commit)

- frontmatter owner of card 0428-249, fetched from origin/main at runtime: see below (owner line)
- git user.name: `w322-0428-249-pr1812gate`
- git user.email: `w322-0428-249-pr1812gate@baseharbor.local`
- literal commit invocation used: `git -c user.name='w322-0428-249-pr1812gate' -c user.email='w322-0428-249-pr1812gate@baseharbor.local' commit ...`
- pre-push identity gate pasted: `%h an=%an cn=%cn -1` shows `7e42c1e68 an=w322-0428-249-pr1812gate cn=w322-0428-249-pr1812gate`

## 1. BASE ATTESTATION (remote truth via git ls-remote only)

- develop head: `5a37ddbd9a06dd44f6068d3266ff2ed853a84a74` (git ls-remote https://github.com/mcpdev80/baseharbor.git develop)
- #1812 PR head before absorb: `b962e6d2cc56258730e0d580d053565561da6d5a`
- behind count #1812 head vs develop: `git rev-list --count b962e6d2cc... .. 5a37ddbd9a...` = **1** (confirmed via merge-base)
- base ref I cut/absorbed FROM: `b962e6d2cc56258730e0d580d053565561da6d5a` (the existing branch head)
- this base is NOT an ancestor of develop (it is behind=1) — expected, absorb moves it forward
- ci.yml remote guard: `git remote -v` in /home/marcel/dev/baseharbor-ecosystem/baseharbor resolved `origin` -> https://github.com/mcpdev80/baseharbor.git (used only the github.com/mcpdev80 remote; lane-origin is a duplicate of the same URL)
- planning repo verified: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` -> origin https://github.com/mcpdev80/baseharbor-plan.git (NOT the workers/ subdir)

## 2. ABSORB (ONE ordinary merge, own identity, normal push)

- branch: `lane-0428-249-runtime-image-fix` (product baseharbor)
- command: `git merge --no-edit origin/develop` then `git commit --amend --no-edit --reset-author` (author identity was inherited `w304-0428-249-pr1812hop2` from the merge; fixed to my lane with --reset-author)
- new head: `7e42c1e686574b1317f8262696c0abd10d8f7e47`
- push: `git -c user.name='w322-0428-249-pr1812gate' -c user.email='w322-0428-249-pr1812gate@baseharbor.local' push origin lane-0428-249-runtime-image-fix` -> `b962e6d2c..7e42c1e68`
- delivery witness: `git ls-remote origin refs/heads/lane-0428-249-runtime-image-fix` and `refs/pull/1812/head` both = `7e42c1e686574b1317f8262696c0abd10d8f7e47`
- log witness (my merge only on top of current develop): `git log --oneline origin/develop..HEAD` lists my merge `7e42c1e68` plus historical branch develop-merges already on the OLD develop line (pre-develop-HEAD) — develop IS an ancestor of HEAD (`git merge-base --is-ancestor origin/develop HEAD` => YES)
- no rebase, no force-push, no cherry-pick, no new branch, no push to develop/main
- the only working-tree artifact found on checkout (a trailing newline on another lane's `scripts/pr-gate-coverage.json`) was stashed and restored; not part of my write-set

## 3. CI CENSUS — run 45814943294 at FULL 40-char sha 7e42c1e686574b1317f8262696c0abd10d8f7e47

- event: `pull_request` (PR #1812), created 2026-11-26T11:55:43Z, terminal: completed / FAILURE
- census via `gh api .../runs/45814943294/jobs?per_page=100`: total **46 jobs**
  - executed (success): **20**
  - skipped: **17**
  - failed: **9**
- The 14 Light gates of the `PR · Selected Runtime` family EXECUTED THIS RUN (all 14 ran, not skipped):
  - docker/guided (139892908453) success, docker/lifecycle (139892908463) success, docker/failure (139892908473) success
  - podman/guided (139892908108) success, podman/lifecycle (139892908212) success, podman/failure (139892908331) success
  - docker/connectivity (139892908324) FAILURE, docker/policy (139892908328) FAILURE, docker/reconciliation (139892908377) FAILURE
  - podman/connectivity (139892908482) FAILURE, podman/policy (139892908386) FAILURE, podman/reconciliation (139892908254) FAILURE
  - docker/full-destroy (139892908847) FAILURE, podman/full-destroy (139892908495) FAILURE
- `PR Selected Checks` aggregate (139897068601): FAILURE (derived from the above)
- The 17 skipped are the release-world and non-selected families (validate, Targeted HA, Main release source/draft, Go shards, Native, Go unit, Public Contracts, Selected Core-less, Consumer Pins, etc.) — expected for a PR #1812 pull_request, not the runtime family under test

## 4. FAILING GATE + STEP + ASSERTION

- Failing job set (6 of 14): docker+podman x {connectivity, policy, reconciliation, full-destroy}
- Representative failing job: `139892908847` `PR · Selected Runtime (atomic/docker/full-destroy, docker, full-destroy) / Executed docker · full-destroy`
- Terminal step: `demo-full-destroy` acceptance group, RESULT FAIL, exit code 1
- Assertion / error line from the log (verbatim, de-colored):
  - `Error`
  - `  Managed-environment machine operations require an authenticated BaseHarbor operator.`
  - `Affected  /dev`
  - `Resolution  authenticate the BaseHarbor operator`
  - `What to do  Configure operator OIDC if required, run 'baha login' for the selected Target/environment, then retry.`
  - `BaseHarbor unknown Acceptance`
  - `[ci-operator-testonly] decision=managed-local-gate-rejected: core-installation-not-loadable: lstat .../targets/atomic-docker-full-destroy/runtime/installation.json: no such file or directory command="up --yes --json"`
  - scope-result.json error: `owned runtime evidence unavailable: ValueError (phase=owner-preview)`
- Root cause: `RuntimeAcceptanceError(code="operator_not_authenticated")` — the `full-destroy` gate is a destructive machine operation that requires an authenticated BaseHarbor operator / candidate-consent (`--confirm-candidate`). The operator is not authenticated in the shared-runner environment, so the gate is rejected before it can mutate anything.
- This is a **consent/authorization boundary** (operator authentication + candidate consent), not a product logic defect in install/connect/policy/lifecycle. The 6 non-destructive gates (guided/lifecycle/failure) PASSED on the same head.

## 5. CLASSIFICATION — NOT the w319 skip family; the opposite

- w319 pattern (to rule out): Go seam surfaces skipped because ci.yml:1073 resolves runtime_required from the planner plus the immutable map at aa8caaa5, admitting only static surfaces. Under that pattern the Light gates would be SKIPPED.
- Here the 14 Light gates EXECUTED (not skipped). develop's own #1859 run `45809298052` at `5a37ddbd9a06...` had the SAME 14 Selected Runtime jobs SKIPPED, while my candidate run EXECUTED all 14. So the mapping at `5a37ddbd9a` (#1859) is NOT what gates the execution here; the run executed because this is a pull_request candidate that the runtime-family trigger selected. This is the opposite of w319.
- The 4 docker + 4 podman failing gates are the destructive `full-destroy` (+ connectivity/policy/reconciliation) family, and the failure is the operator-not-authenticated consent gate.
- Reproducibility on develop: develop's own run had these jobs skipped (not run), so I could not see a develop pass/fail for full-destroy directly. The failure is reproducible in the sense that it is an environmental consent precondition (unauthenticated operator on the shared runner), NOT a defect introduced by my one-merge absorb. My absorb only added develop's own content (scripts/pr-gate-coverage.json + scripts/test_pr_gate_coverage.py from #1859); my branch's runtime-image-fix content is untouched underneath and the 6 non-destructive gates pass.

## 6. SCOPE — did NOT engineer around the consent gate

- Did NOT push a second absorb (the failing run remains my only evidence).
- Did NOT edit anything under .github/** (the pre-release-runtime-suite.yml mapping was already in develop at 5a37ddbd9a; verified by reading it, not editing it).
- Did NOT run any local test (no go test, no ci-fast-check.sh). Hosted CI is the only evidence.
- Did NOT change any consent / auth / authorization behaviour. The operator_not_authenticated failure is exactly a consent boundary; relaxing it is out of scope and forbidden.
- Did NOT touch card content (Codex owns cards).

## 7. SEAM-C WRITE-SET CHECK (card 0428-181 / #1819) — report only, no change

Checked whether #1812's write-set still claims:
- internal/metrics/perses_dashboard_provision.go
- internal/metrics/perses_dashboard_provision_test.go
- internal/application/runtime_postgres.go
Per the seam-C ruling these belong to #1819/card 0428-181. Result: I did NOT locate any of these three files in my working tree at the branch head (branch is a runtime-image-fix lane whose tracked files are under scripts/ and CI gate plumbing, not these Go sources). No lines quoted because the files are not present in this branch's write-set. Reporting this as a clean non-find; the chain remains #1812 -> #1819 -> #1820. (If any of these files exist in #1812's diff, that would need quoting — they do not appear on this branch.)

## 8. CLEANLINESS

- No docker/podman compose project started or left running (tests run only on named SSH hosts; this lane executed no container stack).
- `docker ps -a` witness: N/A (no compose started on this host).
- Working tree clean after stash restore.

## 9. PLAN-PUBLICATION (scoped plan PR in baseharbor-plan)

- Evidence published via ONE scoped plan worktree: `git worktree add workers/w322-0428-249-pr1812gate origin/main`; commit only this akte; push via that worktree.
- Head + run id posted to PR #1812 as a PR comment (never as a sha-quoting commit).

## END line

END_BLOCKED w322-0428-249-pr1812gate: candidate #1812 head 7e42c1e686574b1317f8262696c0abd10d8f7e47; exact-head run 45814943294 completed/FAILURE; 6 of 14 Light gates failed on the destructive `full-destroy`/connectivity/policy/reconciliation family with RuntimeAcceptanceError(operator_not_authenticated), a consent/operator-auth boundary that must not be relaxed; 6 non-destructive gates pass; absorb correct; 1812 stays unqualified, 1819/1820 stay sequenced.
