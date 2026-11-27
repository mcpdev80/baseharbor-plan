# w402 · card 0428-315 · PR #1882 — compile-time constant correction (akte)

Mission: coordinator/missions/w402-pr1882-tempo-const.txt. Repo `mcpdev80/baseharbor`,
branch `lane-0428-315-timeouts`, PR #1882 (base develop). Correction round from the
independent Codex re-review verdict
`evidence/2026-11-27/0428-315/verdict-recheck-w267.md` (plan main, reviewed plan head
`2f40ca1630f5919ec7c129a038ff6e2185130966`).

## PLAN (numbered; mirrors workers/todos/w402-0428-315-constfix.json)

1. Reality check: resolve the github.com/mcpdev80 remote, verify branch head d51763d0d. — DONE
2. Read the Codex verdict from plan origin/main; record card owner + commit identity block. — DONE
3. Create the isolated worktree from the existing candidate branch (one candidate per chain). — DONE
4. Fix the finding: restore the compile-time invariant + static drift check (runtime test kept). — DONE
5. Commit under the canonical lane identity; pre-push author gate. — DONE
6. Transport: merge origin/develop, gofmt/vet/build prechecks, normal push to the SAME branch. — DONE
7. Watch own pull_request runs to terminal; both run IDs + job results; pair per exact head. — DONE (pair at 78ab390579)
8. Publish akte on plan origin/main; ls-tree witness before END. — see Publishing below
9. END post with candidate SHA. — DONE (END_BLOCKED: class-A catalog freeze)

## Visible ANSATZ BLOCK (before first commit)

- Card frontmatter `owner:` VERBATIM, fetched from plan origin/main at runtime
  (`git show origin/main:tasks/t-20261125-hunt42-timeout-constant-matrix.md`, line 9):
  `owner: w400-0428-315-timeoutsfix`
  No `(lane X)` marker is present in the frontmatter, so the canonical lane string is the
  full owner value: `w400-0428-315-timeoutsfix`.
- Deviation (recorded, not silent): my dispatch mission registers this session as
  `w402-0428-315-constfix` and assigns the correction round to this lane. I therefore used
  MY OWN lane's canonical name for every commit (author AND committer), per the commit
  identity mandate ("EVERY commit you create ... must carry YOUR OWN lane's FULL canonical
  name"):
  - `user.name = w402-0428-315-constfix`
  - `user.email = w402-0428-315-constfix@baseharbor.local`
  - Literal invocation used for every commit:
    `git -c user.name=w402-0428-315-constfix -c user.email=w402-0428-315-constfix@baseharbor.local commit ...`
  - Pre-push gate printed before every push (must equal the lane name exactly):
    `git show -s --format=%an HEAD | grep -qx "w402-0428-315-constfix" && echo AUTHOR-GATE-OK`
  The prior commits on this branch carry `w397-0428-307-idfallback` (a162aced, be410aea) and
  `w400-0428-315-timeoutsfix` (d51763d0); they are foreign work preserved, never rewritten.
  If the Coordinator intends the card-owner identity to author this correction round instead,
  say so and I will re-commit under `w400-0428-315-timeoutsfix` via a normal follow-up commit.

## Remote guard + base attestation (reality witnesses)

- FIRST git action in the shared baseharbor checkout, `git -C .../baseharbor remote -v` (head lines):
  `origin  https://github.com/mcpdev80/baseharbor.git` and
  `lane-origin  https://github.com/mcpdev80/baseharbor.git` — both resolve to github.com/mcpdev80;
  every fetch/push/ls-remote in this lane used the explicit URL `https://github.com/mcpdev80/baseharbor.git`.
- Planning repo verified BEFORE any evidence commit (`git -C .../baseharbor-plan remote -v` head line):
  `origin  https://github.com/mcpdev80/baseharbor-plan.git`.
  (The WRONG-ZONE path `workers/baseharbor-plan` was NOT used; see the finding under Cleanliness.)
- Base attestation: `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop`
  = `6944e8761af6f07b801f55e39bb9a5409226c10b` — this exact SHA is an ancestor of my first commit:
  `git merge-base --is-ancestor 6944e8761a... HEAD` → YES (printed at each candidate).
- Starting point (given mission head): `git ls-remote ... refs/heads/lane-0428-315-timeouts`
  = `d51763d0dcb881e49279cd270c3265c00282b5b5`; my first commit is a DIRECT CHILD of it
  (no merge, no rewrite). Transport `git merge origin/develop` answered "Already up to date"
  (develop was already an ancestor) — so no merge commit was created, none needed.
- `git log --oneline origin/develop..HEAD` on the final head lists: a162aced, be410aea,
  d51763d0 (pre-existing card-owner/lane work on the named branch, preserved) + my seven
  commits acc9a93e, 21802311, b5eb6201, 59170996, 0f4ec59f, 6b0fd46a, 78ab3905.
- `git diff origin/develop...HEAD --name-only` (final head):
  cmd/baha/app_observe.go, internal/application/timeouts.go, internal/application/timeouts_test.go,
  internal/metrics/perses_contract_test.go, internal/metrics/perses_tempo_datasource.go,
  internal/objectstorage/runtime_resources_test.go, internal/objectstorage/seaweedfs.go,
  scripts/pr-gate-coverage.json (eight paths: the card's existing PR set, no unrelated scope).

## Implementation of the finding (verbatim target: perses_tempo_datasource.go:64-71)

- `var tempoTraceQueryTimeout = application.FastServiceTimeout` →
  `const tempoTraceQueryTimeout = application.FastServiceTimeout` (the recipe's preferred
  form: the const aliases the matrix constant directly; the matrix group is itself a typed
  time.Duration constant, so the literal 10s lives in exactly one place, and no package code
  can mutate the alias at runtime again).
- Static drift guards (so the alias cannot drift silently; drift fails the build):
  - `type tempoTraceQueryTimeoutMatrixAlias [tempoTraceQueryTimeout - application.FastServiceTimeout]struct{}`
    — array length must be a NON-NEGATIVE CONSTANT: mutation to a var (non-constant) and
    downward drift (negative) both break `go build`.
  - `type tempoTraceQueryTimeoutMatrixAliasExact [application.FastServiceTimeout - tempoTraceQueryTimeout]struct{}`
    — the same difference the other way round: upward drift breaks the build.
  - `func assertTempoAliasMatrixEquality()` returns both guard types; the new test
    `TestTempoTraceQueryTimeoutIsCompileTimeConstant` (internal/metrics/perses_contract_test.go)
    takes their `reflect` types, forcing the compiler to evaluate both guards.
- Runtime tests kept: `TestTempoTraceQueryTimeoutReadsFastServiceMatrix` (matrix equality AND
  literal 10s) untouched; behavior of both probe call sites (perses_tempo_datasource.go:433,
  perses_tempo_verify.go:98) unchanged (they read the same constant).
- Negative pilots run against the EXACT candidate trees (temporary edits, reverted, never
  committed): var-mutation fails the build ("array length ... must be constant"); ±1s drift
  fails the build ("invalid array length ... constant -1000000000" / "-1"); +0.5s sub-second
  upward drift fails the build (nanosecond-domain difference). Pilot records are in this file's
  transcript trail; the b61e3ab tree additionally showed a pilot artifact (the `time` import
  was not referenced by the literal-pilot form at that tree), which is why the final head keeps
  the alias declared as the matrix constant directly — the pilots above then pass on HEAD.

## Test → check/gate → trigger route

- New/changed tests: `TestTempoTraceQueryTimeoutIsCompileTimeConstant` +
  `TestTempoTraceQueryTimeoutReadsFastServiceMatrix` in package `internal/metrics`
  (perses_contract_test.go), plus the unchanged matrix tests in
  `internal/application` and `internal/objectstorage`.
- Route: ordinary Go package discovery (`go list ./...` doctrine — no per-test list) via the
  package-shard `PR · Go unit · shard` checks, which the gate plan selects from the catalog
  rows for the changed paths. Those catalog rows exist on this branch (candidate side); the
  trusted BASE side must contain them for the plan to run the shards — see the STATE finding.
- Gate registration in THIS PR: scripts/pr-gate-coverage.json rows for all six timeout-matrix
  paths (the four consolidation files + the two pre-existing matrix files), committed at
  78ab3905 on my candidate. No `.github/**` file touched, no rerun/workflow_dispatch triggered.

## Hosted run witnesses (Eigenes-Run-Pflicht; pair = two DISTINCT executed run IDs on the same exact head)

Candidate heads and their pull_request runs (all executed by MY pushes / the authorized close+reopen):

- head `acc9a93e2892e508cbc12df82633e285c890800f`
  - run `46052660694` — pull_request — terminal FAILURE. Non-skipped jobs:
    Workflow policy SUCCESS, PR · Source format SUCCESS, PR · Native gate plan SUCCESS,
    PR · Trusted Plan FAILURE, PR Selected Checks FAILURE (all others SKIPPED).
    Failing log line: `ValueError: invalid trusted PR gate coverage catalog: uncataloged
    source change, no declared runtime gate owner: internal/application/timeouts.go ...` (six paths).
    Diagnosis: Trusted Plan plans with the trusted BASE catalog; my catalog rows were missing at that head.
- head `b5eb62015a894866ad151d2b808fc107e89a952c`
  - run `46053037805` — pull_request — terminal FAILURE; same Trusted Plan uncataloged-source line.
    Diagnosis: catalog rows present, but the base planner consumes the candidate catalog only
    when its `release` matches the planned release (scripts/pr-gate-plan.py:1905); the base
    catalog carries release `v0.4.27`. Also this push cancelled my in-flight pair run on the
    previous head (process defect noted; avoided afterwards by batching).
- head `21802311486bcde53329ae7ac6f7b81b9f090db8`
  - run `46053397934` — pull_request — terminal FAILURE; same Trusted Plan line. The seconds-truncated
    upward guard was insufficient; final guards now use the typed difference (see Implementation).
- head `591709960ccadc561ddf8dd832a5143c0ff694e5`
  - run `46054034098` — pull_request — terminal FAILURE; same Trusted Plan line (rows present; base-planner
    release guard still ignores the candidate catalog).
- head `0f4ec59f29fdd84d71fc02ec1a0fe775b87590de`
  - run `46054436788` — pull_request — terminal FAILURE; same Trusted Plan line.
- head `6b0fd46a29b5ba447d38b09b5e3bb0620472ad6a`
  - run `46054726423` — pull_request — terminal FAILURE; same Trusted Plan line. (One terminal witness;
    superseded by the final head's executed pair — a rerun would raise run_attempt on the SAME ID and is
    VOID as pair evidence, so no rerun was requested.)
- FINAL head `78ab390579afeb483fb1c181ad9eb11e0e317ea3` — PAIR complete:
  - run `46055456117` — pull_request (push trigger) — terminal FAILURE. Non-skipped jobs:
    Workflow policy SUCCESS, PR · Source format SUCCESS, PR · Native gate plan SUCCESS,
    PR · Trusted Plan FAILURE, PR Selected Checks FAILURE.
  - run `46055569861` — pull_request (second distinct trigger via authorized
    `gh pr close 1882 --comment 'second exact-head hosted run trigger (coordinator-authorized)' && gh pr reopen 1882`;
    no content change; PR left open, draft=false verified) — terminal FAILURE. Same job pattern:
    Trusted Plan FAILURE, PR Selected Checks FAILURE (cascade), everything else green or skipped.
  - Both runs executed on the EXACT head 78ab390579 (run list headSha fields above).
  - Trusted Plan failing log line (verbatim fragment):
    `ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared runtime gate owner: internal/application/timeouts.go (id source.internal_application_timeouts_go): ... internal/objectstorage/seaweedfs.go (id source.internal_objectstorage_seaweedfs_go): ...`

## STATE finding (class-A catalog freeze; coordinator/Owner action, NOT bypassed here)

- The `PR · Trusted Plan` job runs the planner + catalog from the TRUSTED BASE/controller
  (`ci.yml` step 'Resolve exact immutable PR inputs using trusted base policy' copies
  `pr-gate-plan.py`, `validate-pr-gate-coverage.py`, `pr-gate-coverage.json` from the controller
  blob; planner guard at `scripts/pr-gate-plan.py:1905`: candidate catalog content is consulted
  only when `coverage.get('release') == result['release']`, and the base blob at
  develop `6944e8761a` `scripts/pr-gate-coverage.json` carries `release: v0.4.27`).
- Consequence: the six timeout-source rows on my candidate branch cannot make the gate green.
  The base-side registration of these exact rows (paths + surfaces as in this PR's catalog diff,
  i.e. the merged catalog-only precedent family #1865/#1857/#1852/#1849/#1872 for the
  0428-359/#136 lineage) is the coordinator/Owner action. My candidate keeps the rows so the
  gate passes the moment they land on the base.
- The failing check is therefore the same class-A freeze the card's own wait_reason already
  records for this chain ("Same Owner-scope shared scripts/pr-gate-coverage.json gate as lanes
  307/310/312/316"); the content finding of the Codex re-review is fully fixed on head 78ab390579.

## repo-rule compliance

- No `.github/**` file edited; no rerun/workflow_dispatch; no force-push; no cherry-pick; no second
  branch (all work on `lane-0428-315-timeouts`, single candidate per chain); PR #1882 NOT merged by me.
- Transport was `git merge origin/develop` + normal push; push delivery proved with
  `git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/lane-0428-315-timeouts refs/pull/1882/head`
  (output above; refs/pull/1882/head == refs/heads/lane-0428-315-timeouts at every final witness).
- Local prechecks before every push: gofmt (clean), `go vet` on the touched packages (clean),
  `go build ./...` (clean), `go test -c` compile-only (clean). NO tests were executed locally;
  test execution happens only in Hosted CI (its shards are gated behind the frozen Trusted Plan
  route, see STATE finding). `python3 scripts/validate-pr-gate-coverage.py` is a schema validator,
  not a test suite.
- Catalog JSON regenerated from the BASE catalog shape at 7738c151/59170996 to normalize
  serialization (one observed churn: whole-file rewrite, content = base + six rows; recorded here).
- No subagents; every step executed in this session.

## cleanliness

- `docker ps -a` before first action and at END: BOTH CHECKS EXECUTED, BOTH RETURNED EMPTY
  (no containers exist on this host at all — the coordinator/server host runs no ambient stack;
  the `bh-docker-dev-shared-*` stack the runner rule mentions is absent here, consistent with
  the -run skip mandate). This lane started and removed NO container or compose project.
- Scratch lives under /tmp/opencode and this lane's worktree
  `workers/w402-0428-315-constfix-wt` (isolated, mine). Nothing created in the ecosystem root.
- Foreign paths observed (reported, untouched, per instruction): `workers/baseharbor-plan`
  (the wrong-zone dir the WARNING names; I verified and did NOT use or extend it),
  `/tmp/w402-tr`, `/tmp/w402-head`, `/tmp/w402-hdrtree`, `/tmp/w402-ctr` (my own scratch).
- Process note (self-reported): one early `git reset --hard 2180231148` discarded only MY OWN
  uncommitted edits (remote was unchanged at 2180231148, proved by ls-remote before/after); the
  incident is why the final candidate tree was re-verified blob-for-blob (worktree == HEAD, and
  `git show HEAD:internal/metrics/perses_tempo_datasource.go | sha256sum` recorded).

## Publishing

- This akte lives at `evidence-staging/2026-11-27/w402-pr1882-fix.md` in the workers bookkeeping
  area, per the mission's evidence path. baseharbor-plan main is PROTECTED and the shared plan
  checkout holds foreign uncommitted work (PLAN REPO IS A SHARED CHECKOUT), so I did not write to
  the plan repo from this lane; the Coordinator folds this akte into
  `evidence/2026-11-27/0428-315/` via the usual isolated-worktree + plan-PR route.

END_BLOCKED w402-0428-315-constfix: content finding fixed at candidate head 78ab390579 (pair runs 46055456117 + 46055569861, terminal; only PR · Trusted Plan red = class-A base-catalog freeze; base-side rows for the six timeout paths are the coordinator action); akte: workers/evidence-staging/2026-11-27/w402-pr1882-fix.md
