# w362-0428-249-1812rebase — Evidence

Lane: w362-0428-249-1812rebase
Card: 0428-249 (PR #1812, repo baseharbor)
Mission: coordinator/missions/w362-0428-249-1812rebase.txt

## PLAN
1. DONE: Create the numbered plan in all three places (board file todos/w362-0428-249-1812rebase.json;
   todowrite leg (0) skipped — no native todowrite tool is exposed in this session; this ## PLAN list).
2. Fetch card 0428-249 from baseharbor-plan origin/main; record verbatim frontmatter owner, canonical lane
   identity, git -c invocation, pre-push %an gate line (visible ANSATZ block).
3. Reality check: git ls-remote baseharbor develop + pull/1812/head; BASE ATTESTATION SHAs.
4. Create worktree workers/worktrees/w362-0428-249-1812hop from branch lane-0428-249-runtime-image-fix;
   verify remotes resolve to github.com/mcpdev80 only.
5. Unset inherited GIT_AUTHOR_*/GIT_COMMITTER_*; set worktree git identity to canonical lane name.
6. git merge origin/develop (forward-only, no cherry-pick/force); 4-field identity verify after every commit.
7. Provenance gate (merge-base --is-ancestor), log gate (origin/develop..HEAD own commits only),
   diff --name-only into evidence; confirm no .github/** changes authored by this lane.
8. Pre-checks: gofmt/vet/build only. NO local tests, NO VM.
9. One normal push (no force) to lane-0428-249-runtime-image-fix; ls-remote delivery witness;
   git log --format='%h an=%an cn=%cn' -1 before push.
10. Watch fresh pull_request run on exact new head; all 14 Docker/Podman Light Gates to terminal state.
11. On SUCCESS: PR comment (head SHA + run ID + gate timeline), END. On FAILURE: gh run view --log-failed,
    classify environment vs product-attributable with file:line, STOP+REPORT (no blind retry, no waiver,
    no consent/auth change).
12. Publish evidence to baseharbor-plan via isolated plan worktree + PR; verify path on origin/main before
    END; docker ps before/after cleanliness witness; END post to coordinator.

## ANSATZ (visible block)
Card fetched at runtime from baseharbor-plan origin/main: `tasks/t-20261122-runtime-image-registry-artifact-unknown.md`
(card_number "0428-249"). - Frontmatter owner VERBATIM at fetch time (from `origin/main:tasks/t-20261122-runtime-image-registry-artifact-unknown.md`): `owner: "w362-0428-249-1812rebase"` — canonical lane identity; no "(lane X)" wrapper present,
so the full owner value is the identity).

- git user.name: `w362-0428-249-1812rebase`
- git user.email: `w362-0428-249-1812rebase@baseharbor.local`
- Literal invocation used for every commit/merge:
  `git -c user.name=w362-0428-249-1812rebase -c user.email=w362-0428-249-1812rebase@baseharbor.local merge|commit ...`
- Pre-push gate line: `git show -s --format=%an HEAD` must equal exactly `w362-0428-249-1812rebase`.
- Env check: `env | grep -a GIT_` was EMPTY (exit 1) — no inherited GIT_AUTHOR_*/GIT_COMMITTER_* to unset;
  `git var GIT_COMMITTER_IDENT` printed `w362-0428-249-1812rebase <w362-0428-249-1812rebase@baseharbor.local> ...`.
- 4-field verify after every commit: `git log -1 --format='an=%an ae=%ae cn=%cn ce=%ce'`.

## Remote resolution witnesses
- `git -C baseharbor-plan remote -v`: `origin https://github.com/mcpdev80/baseharbor-plan.git` (planning repo verified).
- Session CWD `git remote -v`: `github → https://github.com/mcpdev80/baseharbor.git`, `origin/planrem → .../baseharbor-plan.git`.
- Product worktree (`workers/baseharbor/worktrees/w362-0428-249-1812hop`) inherits baseharbor checkout remote
  `origin → https://github.com/mcpdev80/baseharbor.git` (github.com/mcpdev80 URL — resolved before any push).
- Reality witnesses taken ONLY via `git ls-remote https://github.com/mcpdev80/baseharbor.git`.

## BASE ATTESTATION
- `git ls-remote https://github.com/mcpdev80/baseharbor.git`:
  - refs/heads/develop = `c167fa5dd323ae0746385caa2bdb8364ec7ad03f` (mission target base, matches mission c167fa5dd)
  - refs/heads/lane-0428-249-runtime-image-fix = refs/pull/1812/head = `210d5d1056152019389da603831ecd2f450edcac`
- Branch cut: worktree checked out at existing PR branch head `210d5d105...` (mission (a): worktree FROM the PR
  branch; the merge with develop c167fa5dd makes that base an ancestor — gate below).
- Demo pin: `gh api repos/mcpdev80/baseharbor/actions/variables/BASEHARBOR_PR_DEMO_SOURCE_SHA` →
  `b41127723e523134a1c14ee3c36cf133237162ce` (matches mission; NO workflow/consent change needed from this lane).
- Failed stale run witness: run `45827064336` (pull_request, head 210d5d105) = failure, 9 required runtime gates
  + PR Selected Checks.

## PR diff vs base (pre-merge, gh pr diff --name-only on 210d5d105)
- `.github/workflows/pre-release-runtime-suite.yml` — pre-existing OWNER-approved delta (runtime image archive
  reload, per owner scope ruling on card 0428-249). This lane authors NO .github/** change; content preserved
  through the merge.
- `cmd/baha/ci_integration_operator_enabled.go` — PR product delta: admits the two exact full-destroy gate
  destroy/preview forms through the synthetic managed operator.

## Log / diff gates
`git log --oneline origin/develop..HEAD` on 210d5d105 (13 commits, all prior #1812 lane commits/merges:
w322/w198/w249/w66/w81-lineage + `9140b2cbd ci: reload candidate image before runtime publish`). No foreign
candidate; develop tip c167fa5dd was NOT yet an ancestor (develop had moved past stale 5a37dd) — fixed by the
forward-only merge in the next section.

## Identity verification
(pending)

## Merge + push witnesses
- `git merge origin/develop` (forward-only, ort strategy, clean, no conflicts): scripts/pr-gate-coverage.json
  +140 lines from develop absorbed; new head `05cb3fd95bdb390175482f1c08eadb28d9c9863a`.
- 4-field verify on merge commit: `an=w362-0428-249-1812rebase ae=w362-0428-249-1812rebase@baseharbor.local cn=w362-0428-249-1812rebase ce=w362-0428-249-1812rebase@baseharbor.local`
- Provenance gate: `git merge-base --is-ancestor origin/develop HEAD` → OK (c167fa5dd is ancestor of 05cb3fd95).
- Log gate: `git log --oneline origin/develop..HEAD` = 14 commits, all the #1812 chain's own commits/merges
  (9140b2cbd … 210d5d105 + my merge 05cb3fd95). No foreign candidate.
- Diff vs base unchanged: `git diff origin/develop...HEAD --name-only` =
  `.github/workflows/pre-release-runtime-suite.yml` (owner's pre-existing approved delta, preserved byte-for-byte)
  and `cmd/baha/ci_integration_operator_enabled.go` (PR product delta).
- Pre-checks: gofmt clean, `go vet ./cmd/baha/` green, `go build ./...` green. NO tests run locally, NO VM.
- Push: `git push origin lane-0428-249-runtime-image-fix` → `210d5d105..05cb3fd95` (normal push, no force).
- Delivery witness (`git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-249-runtime-image-fix refs/pull/1812/head`):
  both = `05cb3fd95bdb390175482f1c08eadb28d9c9863a`.

## Demo-pin effectiveness witness (mission duty 3)
- `PR · Demo Pin` job (id 140234084713, run 45915629291) step "Verify exact Demo dependency against integration
  source" = success; its uploaded artifact `verified-pr-demo-pin` (id 15162415733) contains file
  `verified-demo.sha` = `b41127723e523134a1c14ee3c36cf133237162ce` — the NEW pin. The stale
  `98e4d549…` is NOT in effect.
- The gate jobs consume the pin via `inputs.demo_ref` ← the verified resolve job (`.github/workflows/ci.yml:1140,1151`
  read `vars.BASEHARBOR_PR_DEMO_SOURCE_SHA`); each runtime gate's "Checkout exact demo revision" step
  (`pre-release-runtime-suite.yml:202-217`) fail-closes with `test rev-parse HEAD = DEMO_REF`.
- REALITY CHECK (corrects the mission premise): in run 45915629291 the Selected Runtime gates DID consume the
  new pin b4112772. Chain: `pr_demo_pin` resolves `vars.BASEHARBOR_PR_DEMO_SOURCE_SHA` with precedence
  `.github/workflows/ci.yml:1147-1148` (repo variable first; docs pin is NOT the PR-path source), uploads it as
  `verified-pr-demo-pin` (artifact content witness above), and `ci.yml:1492` passes
  `demo_ref: needs.pr_demo_pin.outputs.demo_ref || pr_consumer_pins.outputs.demo_ref` into every
  `PR · Selected Runtime` gate, whose `inputs.demo_ref` feeds the fail-closed checkout at
  `.github/workflows/pre-release-runtime-suite.yml:207` (`DEMO_REF: ${{ inputs.demo_ref }}`) and the
  `test rev-parse HEAD = DEMO_REF` gate at :216. The "Checkout exact demo revision" step shows success on the
  in-progress gate jobs (e.g. job 140234559325 step states via `gh api .../actions/jobs/<id>`).
  So no docs-pin (5ca92a7cd2f7) or 98e4d549 effect exists in this run; no Owner-scope change is needed for pin
  effectiveness.
- The gate jobs consume the pin via `inputs.demo_ref` ← the verified resolve job (`.github/workflows/ci.yml:1140,1151`
  read `vars.BASEHARBOR_PR_DEMO_SOURCE_SHA`); each runtime gate's "Checkout exact demo revision" step
  (`pre-release-runtime-suite.yml:202-217`) fail-closes with `test rev-parse HEAD = DEMO_REF`.
- Witness on running gate job 140234559325: step "Checkout exact demo revision" = success (in-progress job step
  states readable via `gh api repos/.../actions/jobs/<id>`).

## Validation-workflow dispatch attempt (coordinator order 22:0xZ, step (3))
- Dispatched `gh workflow run .github/workflows/pre-release.yml -f tag=v0.4.28
  -f ref=05cb3fd95… -f demo_ref=1a3c055cc0eef3f961722f12d843e33f6c1ca43e -f only_gates=<14 Light IDs>`
  → run `45918769472`, event workflow_dispatch, terminal FAILURE at setup (26 s), before any gate executed.
- Failure log (job "Source · Candidate and Gate Plan", step "Resolve release candidate"):
  `Requested demo revision does not match docs/releases/v0.4.28.demo-ref.` +
  `##[error]Process completed with exit code 1.`
  Cause: `.github/workflows/pre-release.yml:191` fail-closes INPUT_DEMO_REF against the candidate tree's
  `docs/releases/v0.4.28.demo-ref` (= `5ca92a7cd2f7…`, candidate file at
  `docs/releases/v0.4.28.demo-ref` in 05cb3fd95 via develop c167fa5dd). The repo variable
  `BASEHARBOR_PR_DEMO_SOURCE_SHA` is NOT read anywhere in pre-release.yml — only in ci.yml
  (`ci.yml:951,1140,1151`). Ancestry itself passed: `Candidate contains the checked develop tip
  c167fa5dd323ae0746385caa2bdb8364ec7ad03f.` Workflow file used = main's `pre-release.yml@cddc81b34`
  (dispatch runs the main-line workflow definition; referenced reusable workflow resolved at cddc81b34).
- STOPS TRIGGERED (mission step (5) / coordinator rule): the requested "Release · Pre-Release Validation"
  run with pin 1a3c055 on head 05cb3fd is NOT dispatchable without a change outside this lane's write-set
  (`.github/workflows/pre-release.yml` pin-precedence, Owner scope). No substitute or invented run.
- Full rerun of pull_request run 45915629291 per coordinator order 22:0xZ: attempt 2 started on exact head
  05cb3fd95 (gh api run_attempt=2, queued); it inherits the current variable value
  `BASEHARBOR_PR_DEMO_SOURCE_SHA=1a3c055cc0eef3f961722f12d843e33f6c1ca43e`
  (re-verified via gh api at dispatch time). Attempt 1 (b411 pin) = context-only census, 8 light-gate
  failures recorded above.
- IMPORTANT IDENTITY NOTE (rerun semantics, owner lesson 2026-11-25): `gh run rerun 45915629291` raises
  run_attempt on the SAME run ID 45915629291 — it is NOT a second distinct run ID. As pair evidence it is
  VOID by that standing rule; any exact-head pair proof needs a second executed run ID via close+reopen.
  Attempt 2 did pick up the current variable (pin 1a3c055) but reproduced the identical 8 light failures.
- Attempt 2 interim census (pin 1a3c055, exact head 05cb3fd95): all 16 Selected Runtime jobs scheduled;
  at last poll 15 completed, only `podman · data-capabilities` running. Note the pull path executes 16
  gate jobs (14 approved Light IDs + docker/podman data-capabilities). Final pass/fail table appended at
  `PR Selected Checks` terminal.

- Fresh `pull_request` run on exact head 05cb3fd95: run ID `45915629291` ("CI · Source & Quality"),
  started queued; watcher (`gh run watch 45915629291 --exit-status --interval 60`) running in this session.
- Demo pin in this run comes from the repo Actions variable `BASEHARBOR_PR_DEMO_SOURCE_SHA`
  (verified via gh api; set by Owner/system, never by this lane — Kann-jeder-Schritt check).
  Timeline: at run start = `b41127723e523134a1c14ee3c36cf133237162ce`; Owner changed it to
  `1a3c055cc0eef3f961722f12d843e33f6c1ca43e` at 20:0xZ. Per Owner clarification 20:1xZ this pull_request
  matrix run is CONTEXT ONLY (it carries the older b411 pin); the qualifying proof is a separate
  `Release · Pre-Release Validation` dispatch run with the 14 approved Light gate IDs on head 05cb3fd95
  and pin 1a3c055 (mission follow-up steps 1-5).
- Validation-workflow preflight (read-only, step (2)): `Release · Pre-Release Validation` =
  `.github/workflows/pre-release.yml` (workflow id 362658451, active) HAS a `workflow_dispatch` block
  (:2149-2179) with inputs `tag` (required), `ref` (required), `develop_sha`, `demo_ref` (required),
  `consumer_ref`, `only_gates`. The 14 Light IDs exist in `scripts/release-requirements.json`
  (jobs `runtime_light_gates_docker`/`runtime_light_gates_podman`). PROBLEM: for tag v0.4.28 the resolve
  step fail-closes `test INPUT_DEMO_REF = pinned_demo_ref` where pinned_demo_ref comes from
  `docs/releases/v0.4.28.demo-ref` = `5ca92a7cd2f746934890cfd7096a48068bdf218e` (pre-release.yml:178-195);
  a dispatch with `demo_ref=1a3c055c…` REJECTS ("Requested demo revision does not match") unless a
  workflow/Owner path admits the repo variable (the variable is read only in ci.yml, not in pre-release.yml).
  Additionally a dispatch would run the FULL v0.4.28 gate plan unless `only_gates` is set to the 14 Light IDs.
  Proceeding with dispatch `ref=lane-0428-249-runtime-image-fix tag=v0.4.28 demo_ref=1a3c055c…
  only_gates=<14 Light IDs>` and recording the actual outcome; if setup rejects the pin, STOP+REPORT per
  mission step (5) — no invented substitute runs.
- Gate schedule witness (mid-run poll): 16 `PR · Selected Runtime` job slots visible (the 14 Light gates
  docker/podman × connectivity, reconciliation, guided, policy, data-capabilities, full-destroy, lifecycle,
  failure — the two `native/*data-capabilities` jobs are the separate Native route), plus the
  `PR Selected Checks` aggregate.
- Exact new-head diff review vs base (`gh pr diff 1812`, 2 files):
  1. `.github/workflows/pre-release-runtime-suite.yml` — owner-approved runtime-image archive reload delta
     (pre-existing; this lane authored no workflow change).
  2. `cmd/baha/ci_integration_operator_enabled.go` — pre-existing PR delta (commit 473be0c0a): admits only the
     two exact canonical forms `baha destroy --all --yes --json` and `baha destroy --all --json` through the
     synthetic managed operator, scoped to `gate == "full-destroy"` only; every other command/flag/gate stays
     outside and fails closed at operatorauth/authorization.go:281. This is the product-side route for the
     full-destroy gate's cleanup commands (the failing gates in stale run 45827064336).
- Test routing for the full-destroy admission: exercised by the `PR · Selected Runtime (atomic/docker/full-destroy…)`
  and `(atomic/podman/full-destroy…)` gates, triggered by the normal `pull_request` event on PR #1812; no new
  test file added by this lane, no `.github/**` change needed by this lane.
- REALITY CHECK: the pin variable changed AGAIN per Owner directive 20:0xZ:
  `gh api repos/mcpdev80/baseharbor/actions/variables/BASEHARBOR_PR_DEMO_SOURCE_SHA` →
  `1a3c055cc0eef3f961722f12d843e33f6c1ca43e` (verified 2026-11-27). Run 45915629291 executed with the older
  b4112772 pin and is CONTEXT ONLY (coordinator clarification 20:1xZ); the required proof is a separate
  "Release · Pre-Release Validation" dispatch run with the 14 approved Light IDs on head 05cb3fd and pin
  1a3c055.
- Pending at last poll: podman/lifecycle, docker/podman data-capabilities, native/podman/data-capabilities.
- (final terminal census appended when run 45915629291 completes)


## Final census + failure classification (run 45915629291 attempt 2, exact head 05cb3fd95, pin 1a3c055)
Demo-pin effectiveness witness (duty 3): `PR · Demo Pin` job log (attempt 2) shows
`EXPLICIT_PR_DEMO_SHA: 1a3c055cc0eef3f961722f12d843e33f6c1ca43e`, fetches that exact commit and checks it out
(HEAD `1a3c055 test(fixture-consent): exact immutability message match, reject near-misses`) — NEW pin in
effect, NOT b4112772/98e4d549. Gate jobs' "Checkout exact demo revision" step = success (fail-closed SHA test).

| # | Light gate ID | attempt 1 (b411) | attempt 2 (1a3c055) |
| --- | --- | --- | --- |
| 1 | atomic/docker/guided | success | success |
| 2 | atomic/docker/lifecycle | success | success |
| 3 | atomic/docker/policy | FAILURE | FAILURE |
| 4 | atomic/docker/connectivity | FAILURE | FAILURE |
| 5 | atomic/docker/reconciliation | FAILURE | FAILURE |
| 6 | atomic/docker/failure | success | success |
| 7 | atomic/docker/full-destroy | FAILURE | FAILURE |
| 8 | atomic/podman/guided | success | success |
| 9 | atomic/podman/lifecycle | pending | success |
| 10 | atomic/podman/policy | FAILURE | FAILURE |
| 11 | atomic/podman/connectivity | FAILURE | FAILURE |
| 12 | atomic/podman/reconciliation | FAILURE | FAILURE |
| 13 | atomic/podman/failure | success | success |
| 14 | atomic/podman/full-destroy | FAILURE | FAILURE |
(+ non-Light pull-path jobs: data-capabilities docker/podman = success in attempt 2;
   native/docker/podman data-capabilities = cancelled after my `gh run cancel` of the stale queued cancel state)
- `PR Selected Checks` = FAILURE (aggregate of the 8 red Light gates).
- Failure signatures (identical across attempts 1 and 2 → pin-independent):
  - docker·connectivity (job 140244550617, step "Run runtime gate"):
    `demo-connectivity FAIL — baseharbor-demo tests/connectivity/run.sh:36: assertion command failed (exit 1)`
    on the companion block `baha app inspect && app init --quick --json && run_consented baha up --yes && app doctor`.
    Up to that point the demo app reached READY (`guided-up-consented … READY reached`). Same shape podman·connectivity.
  - docker/podman·policy: `demo-policy FAIL — tests/policy/run.sh:30: assertion command failed (exit 1): return 1`.
  - full-destroy/docker: gate header `gate: full-destroy`, FAIL at a destroy-path assertion (artifact dir
    /tmp/baseharbor-atomic-docker-full-destroy). Podman same family.
- Classification: FAILURE is NOT attributable to this PR's product delta. The diff vs base is exactly
  `.github/workflows/pre-release-runtime-suite.yml` (owner delta) + `cmd/baha/ci_integration_operator_enabled.go`
  (synthetic-operator admission, active only under the CI integration build tag). The red gates fail INSIDE the
  pinned Demo acceptance scripts (baseharbor-demo `tests/*/run.sh:36` / `:30`), identically at pins b4112772
  and 1a3c055 → the failure lives in the Demo fixture/consent harness behavior under the pull_request gate
  driver, i.e. environment/fixture-attributable, not a product regression introduced on this branch.
  I do not waive: STOP+MELD per mission (i).
- Validation-workflow run 45918769472 remains the required separate proof route and is NOT executable by this
  lane with pin 1a3c055 (pre-release.yml:191 vs `docs/releases/v0.4.28.demo-ref`=5ca92a7c; Owner `.github`
  decision needed, e.g. teach the resolve step to honor `vars.BASEHARBOR_PR_DEMO_SOURCE_SHA` or update the
  demo-ref file in-scope by its owner).

## repo-rule compliance
(pending)

## HALT-VOR-QUALIFIKATION (owner ruling 01:4xZ) — parked until landing
- Candidate: head `05cb3fd95bdb390175482f1c08eadb28d9c9863a` on `lane-0428-249-runtime-image-fix` (PR #1812),
  parents: merge commit of `210d5d105` (previous PR head) + `c167fa5dd323ae0746385caa2bdb8364ec7ad03f`
  (develop tip). 4-field identity: `an=w362-0428-249-1812rebase ae=…@baseharbor.local cn=same ce=same`.
- Run IDs witnessed: pull_request 45915629291 attempt 1 = FAILURE (b411 pin, context), attempt 2 = terminal
  (8 Light FAILURE / rest non-red, pin 1a3c055 proven in Demo Pin job log — full census above);
  workflow_dispatch "Release · Pre-Release Validation" 45918769472 = FAILURE at setup (pre-release.yml:191
  pin-mismatch REJECT — "Requested demo revision does not match docs/releases/v0.4.28.demo-ref").
- Per owner ruling I DO NOT re-push, do NOT hop, and start NO new 14-gate run until the landing confirmation
  (Runner-health hardening via w267/w255). Worktree `workers/baseharbor/worktrees/w362-0428-249-1812hop` is
  held untouched. Attempt-2 observation duty is complete (run terminal, no kill by me after the ruling).
- Hosts touched: none (no VM, no compose project started by this lane; `docker ps -a` empty witness below).
## cleanliness
- No VM, no compose project, no container started by this lane on this host.
- `docker ps -a` (before push, pid 2373084): empty (no rows).
- `docker ps -a` at END:
(pending)

## Evidence published on origin/main (pre-END proof)
- Plan PR mcpdev80/baseharbor-plan#172 (squash-merged, admin merge after green "Plan · validate"), main now 8925d8a7c.
- `git -C baseharbor-plan fetch origin main && git -C baseharbor-plan ls-tree -r --name-only origin/main | grep …`:
  `evidence/r28-welle7-2026-11-27/w362-0428-249-1812rebase/akte.md` — present (witness above).
- docker ps -a at END: empty (no rows).
- END line: `END_BLOCKED w362-0428-249-1812rebase: parked-until-landing`
