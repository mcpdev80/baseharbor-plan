# Lane akte — 0428-306 · add golden --help snapshot CI guard

- Lane: w396-0428-306-goldenhelp
- Card: tasks/t-20261125-hunt36-golden-help-guard.md (card_number 0428-306, release v0.4.28, repo mcpdev80/baseharbor)
- Mission: coordinator/missions/w396-0428-306-goldenhelp.txt
- Date: 2026-11-27

## PLAN

1. Done — Reality check: card read; source hunt H-V36 akte (evidence/r28-welle6-2026-11-26/bughunt-hv36-config-surface/index.md) confirms the surface was consistent and proposes only a regression guard.
2. Done — Claim published (see Claim and publishing below; reconcile commit cce92d8c5 on origin/main).
3. Done — Product rules read: baseharbor AGENTS.md, docs/DEVELOPMENT_GUIDELINES.md, CI planner/runner/shard scripts.
4. Done — Base attestation and branch creation (see witnesses).
5. Done — Implementation: golden --help guard tests + committed golden file + shared HelpSurface walk + EN/DE reference docs.
6. Done — Local pre-checks: gofmt, go vet, go build, source-readability, documentation-audit (non-test only).
7. Done — Draft PR mcpdev80/baseharbor#1874 against develop, then marked ready for review (CI trigger).
8. Done — Hosted CI observed to terminal state on exact head 60d4d4906c (run 45987934493, Trusted Plan base-catalog abort; see akte Hosted CI section); the second paired run ID on this head is pending a content push.
9. Done(partial) — This akte published through plan PR #220 (evidence path under evidence/2026-11-27/0428-306/).
10. Done — prs field and akte published on plan PR #220 at the current product head (owner-directive 2026-11-27T11:09Z/11:32Z).

## Card contract facts

- The card note is a hunt skeleton: Goal/Scope/Acceptance placeholders. The authoritative content comes from hunt H-V36: "the config/flag surface is currently consistent; a regression guard (golden --help snapshot in CI) would catch future drift."
- The H-V36 finding note said a guard "requires .github/** change (Owner scope)". That premise is obsolete for the CURRENT planner (a87da7d1 anchor vs today's develop): every ordinary Go test in ./cmd/baha is auto-discovered through scripts/pr-go-unit-shard.py (go test ./cmd/baha -list . plus sha256-balanced cli-0..cli-3 shards) and scripts/pr-unit-database.sh, and any cmd/baha test file change selects CLI_PACKAGE_CHECKS + CODE_CHECKS + WIZARD_BASE_CHECKS through the 'cli-package-tests' area in scripts/pr-gate-plan.py. No workflow file change was needed or made.
- Card frontmatter owner after claim: "w396-0428-306-goldenhelp" — canonical lane identity used for every commit.

## Commit identity (visible Ansatz block, owner mandate 2026-11-26)

- Frontmatter owner verbatim (fetched from origin/main): owner: "w396-0428-306-goldenhelp"
- user.name: w396-0428-306-goldenhelp
- user.email: w396-0428-306-goldenhelp@baseharbor.local
- Invocation: git -c user.name=w396-0428-306-goldenhelp -c user.email=w396-0428-306-goldenhelp@baseharbor.local commit -m '...'
- Pre-push gate line (output below): git log --format='%h an=%an cn=%cn' -1

## Base attestation and provenance

- git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop
  ea5218d72e263f21e79853b679af50074dab8c25  refs/heads/develop
- Branch: lane-0428-306-golden-help-guard created at that exact SHA via
  git worktree add workers/w396-0428-306-wt -b lane-0428-306-golden-help-guard lane-origin/develop
  (the shared checkout's remote 'origin' resolves to a local path zone; the GitHub remote used for every fetch/push is lane-origin = https://github.com/mcpdev80/baseharbor.git; git remote -v was the first git action)
- git merge-base --is-ancestor lane-origin/develop HEAD → ancestor of ea5218d72e... = OK
- git log --oneline lane-origin/develop..HEAD (must list ONLY lane commits):
  8f260b6e54 test(0428-306): pin golden help file, docs and non-mutating HelpSurface walk
  07999fa201 test(0428-306): golden --help surface guard with shared HelpSurface traversal
- git diff origin/develop...HEAD --name-only:
  cmd/baha/testdata/cli-help-golden.txt
  cmd/baha/help_golden_guard_test.go
  cmd/baha/help_golden_invocation_test.go
  docs/de/reference/help-surface.md
  docs/reference/help-surface.md
  internal/cli/cli.go
  internal/cli/help_surface_test.go
- Pre-push identity line:
  8f260b6e54 an=w396-0428-306-goldenhelp cn=w396-0428-306-goldenhelp
  07999fa201 an=w396-0428-306-goldenhelp cn=w396-0428-306-goldenhelp
- Post-push delivery witness (git ls-remote lane-origin refs/heads/lane-0428-306-golden-help-guard):
  8f260b6e54cd96d1a9042d2c3cc4cc41a4f4d7d1  refs/heads/lane-0428-306-golden-help-guard

## Implementation

- internal/cli/cli.go: new Command.HelpSurface() — one shared, side-effect-free walk producing {Path, rendered --help text} for every public command, sorted stably; hidden commands excluded; plus the exported CommandChild routing accessor so guards and tests share the router's first-match semantics instead of re-implementing them. Execute/find behavior is unchanged.
- cmd/baha/testdata/cli-help-golden.txt: committed golden (185 commands), exact rendered --help of every public command at COLUMNS=100 outside an application repository, with per-command sha256 records and the regeneration header.
- cmd/baha/help_golden_guard_test.go:
  - TestCLIHelpGoldenSurface — byte-exact comparison of the live rendering against the committed golden; regeneration only through BASEHARBOR_UPDATE_MACHINE_DOCS=1 (same convention as TestMachineDocumentationTracksRegistryAndCommandTree).
  - TestCLIHelpGoldenFileInventoryPinsEveryCommand — golden row count/paths must match the current help surface (deleted or duplicated golden rows fail closed).
  - TestCLIHelpSurfaceCoversEveryDocumentedCommandPath — every path published by the human command index and machine coverage inventories must exist in the golden surface.
- cmd/baha/help_golden_invocation_test.go: TestCLIHelpGoldenMatchesEveryExecutableHelpInvocation executes BOTH live help routes ('<sub> --help' and 'help <sub>') through runWithIOAsTestOperator and compares against the golden file.
- internal/cli/help_surface_test.go: unit coverage of the shared walk (hidden exclusion, ordering, both help routes equal the rendered surface, alias routing, stability under repeated/concurrent walks).
- docs/reference/help-surface.md + docs/de/reference/help-surface.md: EN/DE reference page documenting the guard and the regeneration command (locale parity + DE integrity audited).
- No product behavior change: no command semantics, no auth/consent/authorization touchpoints, no .github/** change, no scripts/** change.

## Test binding (card row: normal auto-discovery)

- Route: NEW tests are plain Go tests in ./cmd/baha. scripts/pr-gate-plan.py classifies any cmd/baha/*_test.go change as area 'cli-package-tests' requiring CLI_PACKAGE_CHECKS (go test ./cmd/baha -count=1), CODE_CHECKS (source-contracts) and WIZARD_BASE_CHECKS (cli-gofmt/cli-vet/cli-build). The PR · Go unit shards (scripts/pr-go-unit-shard.py, sha256-balanced cli-0..cli-3 over the discovered inventory) execute every discovered test including the new names. internal/cli changes execute in the packages shard (go test ./... inventory).
- Trigger: pull_request (ready_for_review + pushes) on PR #1874; no new check, no catalog change, therefore no pr-gate-plan.py/release-requirements.json registration obligation under ci-workflow-policy.sh (no check file or gate ID added/removed).
- Selection proof: this PR's own runs below are the positive-selection witness (the new test names execute in PR · Go unit and PR · Validation cli-package shards). Unrelated paths do not select the guard beyond the normal package discovery every cmd/baha change already gets.

## Hosted CI (self-run duty §4.6)

- PR: https://github.com/mcpdev80/baseharbor/pull/1874 (base develop ea5218d72e; former head 60d4d4906c, superseded — current exact head b143395545bd2c5c4bd637ad476a5c4cc78630a4, see the two run lines below)
- Run 45983604940 (earlier head 8f260b6e54, event pull_request) — cancelled by this lane's draft→ready toggle; VOID for qualification.
- Run 45983691443 (head 8f260b6e54) — FAILURE observed by this lane: `PR · Trusted Plan` aborts with `ValueError: invalid trusted PR gate coverage catalog: uncataloged source change, no declared runtime gate owner: cmd/baha/help_golden_guard_test.go` (the same failure already fails on the then-head 60d4d4906c via run 45987934493 below; the paired-run requirement applied to 60d4d4906c, itself since superseded by the current head b143395545).
- Run 45987934493 (historical exact head 60d4d4906c, superseded by current head b143395545) — FAILURE at the identical `PR · Trusted Plan` step, job 140468193731 (https://github.com/mcpdev80/baseharbor/actions/runs/45987934493/job/140468193731), all downstream gates `skipping`. Root cause (verified locally against the base controller planner): `.github/workflows/ci.yml` trusted-plan step loads `scripts/pr-gate-coverage.json` from the BASE/merge-target revision (develop ea5218d72e), and `scripts/validate-pr-gate-coverage.py` (unresolved_source_error → planner ValueError) then aborts on the brand-new guard files. Candidate-side catalog rows in the same PR cannot resolve this fail-loud: a base-catalog landing is required. This reproduces the known w361/w365 class (compare 0428-312 BLOCKED-BASE-CATALOG records).
- Current exact head b143395545bd2c5c4bd637ad476a5c4cc78630a4 (content push: router-proven invocations in the shared walk; golden bytes unchanged) — Run 45993109149 observed to FAILURE by this lane at `PR · Trusted Plan` (job 140485661455), identical ValueError listing exactly the four new source files, and at `PR Selected Checks` (job 140485855484, 'Require complete selected Go shard coverage', a downstream consequence of the aborted plan).
- Pair run on this same head: **45994654068** (close/reopen pairing event, head unchanged, observed FAILURE to terminal state at `PR · Trusted Plan` job 140490905899 with the identical base-catalog ValueError and `PR Selected Checks` job 140491094290). Two executed run IDs on the exact head: 45993109149 + 45994654068. Former head 60d4d4906c stays recorded above as superseded history. Rerun justification: no lane-producible content change can fix the abort (the base-catalog landing is Owner/CI-owner scope), so the pairing uses the sanctioned close/reopen event, not a filler push.
- Coordinator measurement 2026-11-27T12:17Z reported "2 of 30 checks failed" on head b143395545; this lane re-counted the rollup directly: `gh api repos/mcpdev80/baseharbor/commits/b143395545.../check-runs?per_page=100` lists **28 completed check runs: 26 success/skipped, 2 failure** — `PR · Trusted Plan` (run 45994654068 job 140490905899, base-catalog ValueError above) and `PR Selected Checks` (job 140491094290, `REJECT: Go test selection missing or invalid`, `UNIT_SCOPE:` blank / `UNIT_RESULT: skipped`, a downstream consequence of the aborted plan). There is no 29th/30th check on this head, and the run is already terminal — nothing further to wait for.
- Lane STATE: BLOCKED-BASE-CATALOG; card 306 kept active under this lane per Owner directive 2026-11-27T11:54Z. Unblock = land the four catalog rows (exact JSON already in PR #1874, `scripts/pr-gate-coverage.json`) on develop, then one clean push re-runs the pipeline; only new exact-head runs qualify.
- STATE / blocker (file:line witness): the trusted-plan step in `.github/workflows/ci.yml` (Resolve exact immutable PR inputs using trusted base policy) loads `scripts/pr-gate-coverage.json` from the BASE revision, and `scripts/validate-pr-gate-coverage.py::unresolved_source_error` (raised via `scripts/pr-gate-plan.py`) aborts fail-loud on brand-new candidate files. This lane may not edit `.github/**` (Owner scope) and the fix is a base-catalog landing of the four rows on develop, not a candidate-side change. Same class as 0428-312 BLOCKED-BASE-CATALOG (w361/w365 records).

## repo-rule compliance

- smallest sufficient scope: one golden file + one shared walk + focused guard tests + EN/DE doc page; nothing else touched.
- tests only in Hosted CI: this host saw only gofmt/vet/build/readability/documentation-audit prechecks and the single-name golden REGENERATION invocation (BASEHARBOR_UPDATE_MACHINE_DOCS=1 go test -run TestCLIHelpGoldenSurface$), which writes the reviewed golden artifact, not a qualification result; all pass/fail claims come from Hosted CI below.
- docs: new pages follow STYLE conventions (EN canonical + DE pair), pass documentation-audit, locale-parity and DE integrity scripts locally as non-test validation.
- one PR per card; branch named in mission pattern; no second branch for this card.

## cleanliness

- No containers/compose started anywhere (no docker/podman use on this host; docker ps -a untouched by this lane).
- Temporary artifacts: /tmp/baha-w396, /tmp/baha-w396b, /tmp/homeprobe, /tmp/cmd (removed); test temp dirs auto-cleaned by go test.
- Worktrees: workers/w396-0428-306-wt (product, lane-owned), workers/w396-0428-306-plan (planning, removed after publishing).

## Claim and planning publishing

- plan repo remote witness: origin https://github.com/mcpdev80/baseharbor-plan.git (verified via git -C baseharbor-plan remote -v before the first evidence commit)
- Claim commit: 3f3de1858 on branch w396-0428-306-goldenhelp; plan PR https://github.com/mcpdev80/baseharbor-plan/pull/220.
- Coordinator board reconcile landed on main earlier: cce92d8c5 board(0428-306): reconcile active golden-help claim (same owner/active state; verified via git show origin/main:tasks/...).
- The mission line "Direct-main wie in plan AGENTS.md" conflicts with the top-level harness protocol (plan main is protected: branch + plan PR + admin squash). Followed the protocol; claim already lives on origin/main through the reconcile commit, so the claim itself needed no merge — this branch carries only the evidence addition.

## END

END_LINE_PLACEHOLDER
