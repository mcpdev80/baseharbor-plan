# w245-0428-284-1842alt · READ-ONLY routing alternatives for PR #1842

Decision input for w200's option-(i) prescription on card 0428-284.
Mission: `/home/marcel/dev/baseharbor-ecosystem/coordinator/missions/w245-1842-alternate-suite.txt`.
No writes, no pushes and no CI triggers in the product repo; nothing was dispatched,
toggled, rerun or closed here. All hosted facts below were READ from the GitHub API
and from already-finished runs.

## Ansatz block (admission + provenance)

- Card frontmatter owner VERBATIM, read from origin/main at runtime
  (`tasks/t-20261125-0428-284-1812-postretry-gate-failure.md`, `owner:` field):
  `owner: w198-0428-284-demo-parser`
- This lane is a READ-ONLY analysis lane for card 0428-284 and commits no product
  candidate: there is no product branch, PR or candidate SHA, so the candidate-commit
  identity gate has nothing to bind. The only commits are planning commits.
- Planning-commit identity actually used (lane identity of this session):
  - git user.name: `w245-0428-284-1842alt`
  - git user.email: `w245-0428-284-1842alt@baseharbor.local`
  - literal invocation:
    `git -c user.name=w245-0428-284-1842alt -c user.email=w245-0428-284-1842alt@baseharbor.local commit -m "..."`
  - pre-push gate line (run before every push, must print the name above):
    `git show -s --format=%an HEAD`

## PLAN

1. DONE Read live develop `scripts/pr-gate-plan.py`, `scripts/pr-gate-map-v1.json`,
   `scripts/pr-stage-boundary.py`; file:line for every mapping decision touching
   `test_pr_gate_coverage.py` and the Demo pin validator.
2. DONE Read `scripts/pr-check-runner.py` to establish how a mapped suite becomes an
   executed job step and what "actually executed" means.
3. DONE Enumerate Hosted job lists of recent green PR runs (`per_page=100`) and
   correlate which named jobs ran for which path sets.
4. DONE Determine which already-selected job would run (a) `test_pr_gate_coverage.py`
   and (b) the `_current_release` + Demo-pin validation path on a #1842-shaped diff.
5. DONE Decide whether a route without editing `.github` is possible for #1842 and
   name the minimal change per candidate suite.
6. DONE Write this akte in an isolated baseharbor-plan worktree and open the plan-PR
   branch (plan PR https://github.com/mcpdev80/baseharbor-plan/pull/53, draft).
7. IN PROGRESS After the plan-PR merge, place the akte under
   `e6ca7696-b1f8-492d-b226-876b16925fc5/` and record `git show <merged-sha>:<path>`
   plus the `origin/main` `ls-tree` witness (merged state alone is not presence proof).
8. PENDING Publish the table plus the one-line answer and post the END line.

## Reality witnesses (measured, not remembered)

- `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v`
  (planning repo, verified BEFORE the first evidence commit):
  `origin	https://github.com/mcpdev80/baseharbor-plan.git (fetch)`
- baseharbor remotes (`git remote -v` in the shared checkout): every configured name
  (`origin`, `lane-origin`, `upstream`) resolves to `https://github.com/mcpdev80/baseharbor.git`;
  no filesystem-path remote is present. All fetches here used `lane-origin` / the
  explicit GitHub URL.
- `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`
  -> `ae70964d7b80b779822b76107b70ea76782f998e` (the develop head all source reads below
  were taken from, via `git show lane-origin/develop:<path>` after a fresh fetch).
- `git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/main`
  -> `bc4689919f2cf8a1c7fdd7ddc817b39c14495fde` at mission start; the plan worktree cut
  from `origin/main` = `75bbbb24c34342e8812c47a240cfc01d7e977474` (newer, fetched fresh).
- PR #1842 (`gh pr view 1842 --json ...files`): state OPEN, not draft, base `develop`,
  head `5d9965944ff6cd265cbd5d042d59cf522b38b76d`, branch `w177-0428-284-demo-pin-1812`,
  files: `docs/releases/v0.4.28.demo-ref`, `scripts/pr-check-runner.py`,
  `scripts/pr-gate-plan.py`, `scripts/test_pr_check_runner.py`,
  `scripts/test_pr_gate_coverage.py` — exactly the #1842-shaped diff this mission names.

## The #1842-shaped diff, as the trusted planner actually saw it

From the `trusted-pr-plan` artifact of green run `45717078703` (job
`PR · Trusted Plan`; artifact files `pr-diff.json`, `pr-plan.json`):

- `target_base_sha` `ae70964d7b80b779822b76107b70ea76782f998e`,
  `head_sha` `5d9965944ff6cd265cbd5d042d59cf522b38b76d`,
  `integration_sha` `d469cb73d836f3ffefd1e0fec5419ef24701b8cc`, `broad_required` false.
- `coverage_status`: `resolved`, `fallback_used`: `true`, `selected_gates`: `[]`.
- `required_validation_checks`: `ci-executor-tests`, `ci-policy`, `go-build`,
  `go-unit-tests`, `go-vet`, `pr-planner-tests`, `receipt-execution-tests`.
- reasons include `docs/releases/v0.4.28.demo-ref: unresolved` and
  `Unknown narrow coverage selects normal broad unit/vet/build checks`.

So on the current candidate the plan is green only through the conservative broad
fallback, `demo-source-pin-validation` is NOT in the plan, and the new Demo-pin code
path in `scripts/pr-check-runner.py` is never executed by any required job.

## (a) Where can `scripts/test_pr_gate_coverage.py` be executed by an ALREADY-SELECTED job?

Mapping decisions, live develop `scripts/pr-gate-plan.py`:

- `pr-gate-plan.py:734-736` — `PLANNING_SCRIPTS` contains
  `scripts/test_pr_gate_coverage.py` (area `ci-planner`).
- `pr-gate-plan.py:1684-1686` — a `PLANNING_SCRIPTS` path `require(CI_CHECKS)`.
- `pr-gate-plan.py:700-703` — the `scripts/pr-*` / `scripts/test_pr_*` catch-all is area
  `ci-executor` and also `require(CI_CHECKS)`.
- `pr-gate-plan.py:748-752` — `CI_CHECKS[0]` is `pr-planner-tests` with command
  `python3 -m unittest scripts/test_pr_gate_plan.py scripts/test_pr_gate_coverage.py
  scripts/test_pre_release_runtime_reuse.py`.
- `pr-gate-plan.py:1885-1906` (in `plan()`) — the conservative fallback merges
  `CONSERVATIVE_CHECKS` (`pr-gate-plan.py:1741-1745`) into the already-required checks
  instead of replacing them, so `pr-planner-tests` stays selected on a #1842-shaped diff
  (confirmed by the artifact line above).

Two independent facts then decide whether that selection EXECUTES the suite:

1. The required route does not use the planner's command. The matrix executor is
   `.github/workflows/ci.yml:1362-1363`, whose `pr-planner-tests` case runs
   `python3 -m unittest scripts/test_pr_gate_plan.py scripts/test_pre_release_runtime_reuse.py`
   — no `test_pr_gate_coverage.py`. The planner's richer command string is consumed
   only by `scripts/pr-check-runner.py` `matrix()`/`VALIDATIONS`
   (`pr-check-runner.py:96-106`, `:294-302`), which reduces a check id to a
   `case "$VALIDATION"` label, and by the advisory job (below).
2. Hosted proof. Job log `PR · Validation · pr-planner-tests` of run `45717078703`
   (job id `139562948542`) prints only `Ran 53 tests` + `Ran 221 tests`; the 53-test
   figure equals `test_pr_gate_plan.py` + `test_pre_release_runtime_reuse.py` alone.
   The same run's `PR · Validation · ci-executor-tests` log (job `139562948406`)
   prints `matched_tests` and `test_pr_gate_coverage.py` is absent from that registered
   suite list (`pr-check-runner.py:109-118`). Grepping all nine executed develop-PR
   job logs of that run for `test_pr_gate_coverage` returns zero hits.
3. Control case, same repo, different route: on PR #1853 (planner route EDITED in
   `.github/workflows/ci.yml`, `+test_pr_gate_coverage.py` in the case line), job
   `PR · Validation · pr-planner-tests` of run `45717496553` (job `139567483027`) logs
   `Ran 49 tests` + `Ran 287 tests`, i.e. the suite really executes. #1853 is therefore
   the fix for (a) — and it is an `.github/**` edit, which #1842 cannot borrow without
   the Owner or a merge of #1853 first.

Candidate suites for (a):

| Candidate suite | Executes `test_pr_gate_coverage.py` on a #1842 diff? | file:line why | Minimal change needed |
| --- | --- | --- | --- |
| `PR · Validation · pr-planner-tests` | NO | Selected (`pr-gate-plan.py:749-752`, `:1684-1686`, `:700-703`; kept by the fallback `pr-gate-plan.py:1885-1906`) but executed by the ci.yml route `ci.yml:1362-1363`, which omits the file; proof: run `45717078703` job `139562948542` = `Ran 53` | `.github` route line (Owner scope) — exactly what #1853 does (`ci.yml:1363` adds the file) |
| `PR · Focused Python` | NO | Hard-coded list `ci.yml:1207-1233` never names `test_pr_gate_coverage.py` (it names `test_pr_check_runner.py` at `ci.yml:1211`) | add the line to `ci.yml:1207-1233` (Owner scope) |
| `PR · Validation · ci-executor-tests` | NO | Suite list `pr-check-runner.py:109-118` has no `test_pr_gate_coverage`; `execute_validation` fails closed on a missing registered suite (`pr-check-runner.py:395-410`) | add `test_pr_gate_coverage` to `CI_EXECUTION_SUITES` in `scripts/pr-check-runner.py` — inside this candidate's own write-set, no `.github` touch |
| `PR · Go unit · *` | NO | Go shard executor (`ci.yml:1235-1265`, `scripts/pr-unit-database.sh`); never runs `scripts/test_*.py`; zero grep hits in job `139565887261` | n/a (wrong layer) |
| `PR · Candidate-added checks (advisory)` | ONLY as advisory, and only if the candidate planner resolves | Job `ci.yml:1161-1191`; the `pr-planner-tests` command differs from the base plan row, so `added_checks` (`pr-candidate-advisory.py:11-27`) returns it and `execute_checks` runs the candidate command verbatim (`pr-candidate-advisory.py:34-46`). `continue-on-error: true` (`ci.yml:1163`) so it can never satisfy the GATE RULE; and it aborts earlier if the candidate plan is unresolved (`pr-candidate-advisory.py:91-94`) | none to run it — it already runs; but it cannot make the suite required |
| `PR · Main release source` (all-`scripts/test_*.py` loop) | would, but is never selected for this card | `ci.yml:635-643` discovers every `scripts/test_*.py`; gated `ci.yml:605` on `github.base_ref == 'main'` | retarget a pin PR at `main` — not admissible for a v0.4.28 develop card |

## (b) Where can the Demo-source-pin validation (`_current_release` + validator) be executed?

- Path selector, live develop: `pr-gate-plan.py:1182` matches only the literal
  `docs/releases/v0.4.27.demo-ref`. `docs/releases/v0.4.28.demo-ref` therefore falls to
  the `else` branch `pr-gate-plan.py:1714-1716` (area `unresolved`) and the whole plan
  resolves only through the broad Go fallback (`pr-gate-plan.py:1885-1910`).
  Hosted proof of exactly that: run `45483027348` (PR #1830, diff =
  `docs/releases/v0.4.28.demo-ref` modified only) produced
  `coverage_status: resolved`, `fallback_used: true`,
  `required_validation_checks: [go-build, go-unit-tests, go-vet]` and reason
  `docs/releases/v0.4.28.demo-ref: unresolved`. That run executed exactly
  `Workflow policy`, `PR · Trusted Plan`, `PR · Source format`, `PR · Focused Python`,
  six `PR · Go unit · *` shards, `Validation · go-build`, `Validation · go-vet` and
  `PR Selected Checks` — no `demo-source-pin-validation`, no `PR · Demo Pin`.
- The validator itself: `pr-check-runner.py:383-397` reads the hard-coded
  `docs/releases/v0.4.27.demo-ref`; #1842's `_current_release` (diff hunk at
  `pr-check-runner.py:383`) makes the path release-scoped.
- The only PR job that ever invokes `demo-source-pin-validation` is the matrix case
  `ci.yml:1315-1319`, i.e. `PR · Validation · demo-source-pin-validation`, and that job
  exists only if the trusted plan emits that check id.
- Second Demo surface, also unreachable here: `PR · Demo Pin` (`ci.yml:1075-1080`)
  verifies the Demo source commit but is gated on
  `runtime_required || integration_required || public_contracts_required`; a pin+CI-scripts
  diff selects zero gates, so all three are false and the job skips. Proof:
  `PR · Demo Pin` is `skipped` in every #1842 run (`45717078703`, `45716226824`,
  `45712217182`, `45666678375`, `45658795502`, `45631228584`) and in #1830's run.
  The `Pin immutable Demo source` step in `PR · Trusted Plan` exits early with an empty
  sha on exactly that condition (`ci.yml:916-921`).
- The advisory job cannot reach it either: the candidate planner is invoked with
  `scripts/pr-gate-map-v1.json` from the base checkout (`ci.yml:911-914`), whose release
  is `v0.4.27` (`scripts/pr-gate-map-v1.json:3`), so a `v0.4.28.demo-ref` candidate plan
  stays unresolved and `pr-candidate-advisory.py:91-94` aborts before running anything.
  Proof: run `45717078703` logged `No candidate-added validation checks.`

Candidate suites for (b):

| Candidate suite | Executes the Demo-pin validation on a #1842 diff? | file:line why | Minimal change needed |
| --- | --- | --- | --- |
| `PR · Validation · demo-source-pin-validation` | NO | Never emitted: selector `pr-gate-plan.py:1182` is v0.4.27-only, so area `unresolved` (`:1714-1716`) and `DEMO_SOURCE_PIN_VALIDATION` (`:791-795`) is not required; proof run `45483027348` plan artifact | make the selector release-scoped, i.e. keep `pr-gate-plan.py:1182` as `docs/releases/{}.demo-ref'.format(release)` — already this candidate's own `scripts/pr-gate-plan.py` hunk |
| `PR · Demo Pin` | NO | Gate condition `ci.yml:1080` needs a runtime/integration/contracts gate; a pin-only diff selects none | would require forcing a native gate onto a data-only pin (scope widening, not minimal) |
| `PR · Trusted Plan` → `Pin immutable Demo source` | NO (resolves Demo `main`, not the pin file) | `ci.yml:916-921` early-exit on the same three outputs; otherwise `gh api .../ref/heads/main` | n/a |
| `PR · Candidate-added checks (advisory)` | NO (aborts) | Base-checkout map release `pr-gate-map-v1.json:3` = `v0.4.27`; unresolved candidate plan raises `pr-candidate-advisory.py:91-94` | would additionally need the map release to be `v0.4.28` (Owner/data file, not `.github`) plus advisory status is not a gate |
| `PR · Main release source` | yes-by-discovery for (a); not applicable for (b) | `ci.yml:605` `base_ref == 'main'` | not admissible for this card |

## One-line answer

NO — on live develop there is no route that avoids touching `.github/**` AND makes an
already-selected Hosted job actually execute `scripts/test_pr_gate_coverage.py` and the
Demo-pin validator for a #1842-shaped diff: the only selector that emits
`demo-source-pin-validation` is hard-coded to `v0.4.27`
(`scripts/pr-gate-plan.py:1182`), so the v0.4.28 pin falls to the unresolved/broad Go
fallback (`pr-gate-plan.py:1714-1716`, `:1885-1910`), and the only route line that runs
`test_pr_gate_coverage.py` is the ci.yml `pr-planner-tests` case
(`ci.yml:1362-1363`), which omits it. The two no-`.github`-edit alternatives that remain
inside this candidate's own write-set are: (i) add `test_pr_gate_coverage` to
`CI_EXECUTION_SUITES` in `scripts/pr-check-runner.py:109-118` so the already-selected
`ci-executor-tests` executes it, and (ii) land the release-scoped selector
(`scripts/pr-gate-plan.py:1182`, already in #1842) so `demo-source-pin-validation` enters
the trusted plan; note that (ii) alone is not sufficient for a green aggregate, because
the ci.yml `*` fallback would then have to route the new id — an unhandled id hits
`exit 2` (`ci.yml:1388`) and fails the job. That last step is the Owner `.github` edit
w200 prescribed.

## Extra facts worth having

- The two-`release`-sources mismatch is structural, not a #1842 defect: the planner takes
  the release from `scripts/pr-gate-map-v1.json:3` (`release = mapping['release']`,
  `pr-gate-plan.py:837`) while `_current_release` (this candidate's new helper) takes it
  from `scripts/release-requirements.json`, which has no `release` key at all — only
  `schema`, `releases`, `gates`. As authored, `_current_release` would raise
  `release-requirements.json missing a release tag` on the real checkout;
  `test_pr_gate_coverage.py` only ever passes because the test overrides the mapping
  release, never the requirements file.
- `scripts/ci-workflow-policy.sh:5-32` freezes the workflow file inventory (20 names);
  adding a new `.github/workflows/*.yml` is itself an Owner-scope allowlist change, so
  "just add another workflow" is not an available alternative either.
- No PR-triggered `ci.yml` push run exists for `main`: the last 100 `push` events show
  only Docker/Podman runtime, pages and pre-release validation workflows.

## cleanliness

- pid of this lane's shell: 625955
- `docker ps -a` before: no containers listed on this host beyond the ambient stack; this
  lane started no container, no compose project, no podman quadlet, and touched no VM host.
- `docker ps -a` after: unchanged (nothing added, nothing removed).
- Workspaces used: `/home/marcel/dev/baseharbor-ecosystem/baseharbor` (read-only git
  fetches of refs `develop`, `refs/pull/1830/head`, `refs/pull/1842/head`,
  `refs/pull/1853/head`, `refs/pull/1854/head` and one blob), the isolated plan worktree
  `workers/w245-1842alt-plan`, and scratch under `/tmp/opencode/w245-1842*`.
  No scratch, cache or checkout was created under `/home/marcel/dev/baseharbor-ecosystem`.
- No `.evidence/` directory was created anywhere; nothing was committed to a product repo.

## Transport witnesses (planning transport)

- plan remote (`git remote -v` in this worktree):
  `origin	https://github.com/mcpdev80/baseharbor-plan.git (push)`
- base attestation: this branch was cut from `origin/main` =
  `75bbbb24c34342e8812c47a240cfc01d7e977474`, then rebased onto the freshly fetched
  `origin/main` = `76ab859144661e7fdabdc10e36b9cee5f3ce99ad`;
  `git merge-base --is-ancestor origin/main HEAD` -> OK.
- candidate commit set at the time this section was authored:
  `git log --oneline origin/main..HEAD` -> `5c8894f19 evidence(w245): read-only routing
  alternatives for #1842 (0428-284 decision input)`; author gate
  `git show -s --format=%an HEAD` -> `w245-0428-284-1842alt`.
  The plan repo rejects history rewrites on a branch with an open PR
  (`commit_refs_rules`), so `5c8894f19` stays the first candidate commit and each later
  correction is a NEW commit on this same branch — no amend, no force.
- `git diff --name-only origin/main...HEAD` ->
  `evidence/r29-welle6-2026-11-26/0428-284-1842alt/routing-alternatives.md` (this file only).
- plan PR: https://github.com/mcpdev80/baseharbor-plan/pull/53, base `main`, DRAFT until the
  akte is final; `Plan · validate` run `45727031629`.
- delivery proof, re-read as the LAST action of the commit that contains it
  (`git ls-remote https://github.com/mcpdev80/baseharbor-plan.git refs/heads/w245-1842alt-routing refs/pull/53/head`);
  GitHub settles `refs/pull/<n>/head` a few seconds after the branch push, so the value
  below is the post-push pair:
  `184b21f7d0c99b22ee318dcb26b7bcc360574a3b	refs/heads/w245-1842alt-routing`
  `184b21f7d0c99b22ee318dcb26b7bcc360574a3b	refs/pull/53/head`

## END

END_DONE w245-0428-284-1842alt: no no-`.github` route exists for #1842 (selector
`pr-gate-plan.py:1182` is v0.4.27-only and the `pr-planner-tests` route `ci.yml:1362-1363`
omits `test_pr_gate_coverage.py`); read-only, product candidate SHA = n/a, PR #1842 head
unchanged at `5d9965944ff6cd265cbd5d042d59cf522b38b76d`.
