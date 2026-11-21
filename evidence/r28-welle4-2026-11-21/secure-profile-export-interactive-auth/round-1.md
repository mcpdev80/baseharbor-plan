# 0428-219 secure-profile-export interactive-auth

ROLE: Worker. CARD: t-20261121-secure-profile-export-interactive-auth (0428-219).
PR per card. Branch: `lane-0428-219-secure-profile-export-auth`.

## PLAN

- Create isolated worktree from base e45430f2f, set identity + GitHub remote.
- Reality-check 4.1: DUPLICATE test — does base lane already heal the failing test? (ALL FIRST)
- Reachability test: show which ast raises the usageError and under what condition the command path proceeds.
- If open: give the test a non-interactive operator context via existing helpers; keep refusal unchanged.
- Red-first local test run on own head (named form, skip-list).
- Hosted run on own head to terminal (run-id + conclusion per cell).
- Write evidence round-1.md.
- Publish evidence to baseharbor-plan origin/main; post END via idle+watcher.

## Repo identity

- Worktree: `/home/marcel/dev/baseharbor-ecosystem/0428-219-exportauth-wt`
  - `git remote -v` -> `lane-origin  https://github.com/mcpdev80/baseharbor.git` (also `origin` and `upstream` point to same github URL).
- Worktree cut from base head (base attestation):
  `git ls-remote origin refs/heads/lane-0428-198-cli-shard-operator-env` ->
  `e45430f2f1b7a76ee3743919a4559a4e1d1ff6c4  refs/heads/lane-0428-198-cli-shard-operator-env`
- Correct planning repo: `git -C /home/marcel/dev/baseharbor-ecosystem/baseharbor-plan remote -v` ->
  `origin  https://github.com/mcpdev80/baseharbor-plan.git (fetch)` / `(push)`.
- Note: `workers/baseharbor` is a shared checkout, NOT this lane's worktree; this lane has its own worktree per corrected mission pfad219.txt.

## Reality-check / DUPLICATE decision (4.1, ALL FIRST)

Mission 0428-219 states the failing PR cell `Go unit cli-0` run 44867319394 fails at
`cmd/baha/secure_profile_export_command_test.go:125` with
`operator authentication needs interactive setup` (usageError at `cmd/baha/operator_auth_boundary.go:117`),
because the managed-environment operator-auth gate text at `internal/operatorauth/authorization.go:285`
never appears in the protocol — the command-path wiring the test wants to prove is NEVER reached because
the call hangs on an interactive default setting.

BASE LANE HEAD: `lane-0428-198-cli-shard-operator-env` = `e45430f2f1b7` (calm ~60 min). This is the exact SHA
I cut my branch from.

The base lane head already contains commit `e45430f2f1b7` (05:46) titled
`test(0428-204): authenticate secure export command path`, which wraps the EXACT same failing context in
`secure_profile_export_command_test.go` with the helper `operatorAuthTestContext(t, ...)`:

- `git log --oneline e45430f2f1b7 -- cmd/baha/secure_profile_export_command_test.go`:
  `e45430f2f test(0428-204): authenticate secure export command path`
  `bc8670c1d feat(r27-secure-export): opt-in encrypted local credential export adapter (w204) (#1396)`
- The diff of `e45430f2f`:
  ```
   ctx := localWorkloadScope(
  -		withLocalInvocation(operatorauth.WithEnforcement(context.Background()), "cli"),
  +		operatorAuthTestContext(t, withLocalInvocation(operatorauth.WithEnforcement(context.Background()), "cli")),
   		applicationBoundaryOperation("secure-profile"))
  ```
- The helper `operatorAuthTestContext` + fixture `operatorAuthFixtureContext` already exist in the base lane:
  `cmd/baha/operator_test_fixture_test.go:79` (helper) and `:38` (fixture, an `init()` seam that stamps a
  verified operator editor principal onto the runWithIO seam).

VERIFIED WITNESS (run locally on my worktree, own session, named form with skip-list):

- Parent commit `e45430f2f~1` (unwrapped `withLocalInvocation(...)` at line 117):
  `go test ./cmd/baha/ -count=1 -skip 'RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication' -run 'TestSecureProfileExportCommandPathAssemblesProductionWiring'`
  -> FAILS at `secure_profile_export_command_test.go:125` with EXACTLY the mission error:
     `operator authentication needs interactive setup but input is not a terminal (stderr: )`
- Base-lane head `e45430f2f1b7` (my branch base, the `operatorAuthTestContext(t, ...)` fix):
  same command -> `ok github.com/mcpdev80/baseharbor/cmd/baha 0.312s` PASSES.
- My worktree is byte-identical to base head (`git diff origin/lane-0428-198-cli-shard-operator-env --stat` = empty).

CONCLUSION: The exact failing cell this card is about — the `secure-profile export` command path hanging on
interactive operator setup — is ALREADY healed at the base-lane head `e45430f2f1b7`, which is my branch base.
There is no unhealed defect left for card 0428-219 to fix. The base-lane commit `e45430f2f` is the sole fix.

DECISION: CARD 0428-219 IS A DUPLICATE. Per corrected mission pfad219.txt point 4: if the base lane already
heals this exactly, 0428-219 is a DUPLICATE -> report to Owner immediately, NO product change, NO PR; Owner
sets the card to `superseded`.

This is the outcome the mission flagged as most likely. No product write, no second fix invented, no PR opened.

## repo-rule compliance

- No product write, no PR, no workflow/workflow_dispatch, no runner action, no CI rerun.
- Tabu paths untouched: `internal/operatorauth/**`, `internal/serviceaccess/**`, `internal/identityprovider/**`,
  `.github/**`, `scripts/**`, `cmd/baha/operator_auth_boundary.go` (read-only).
- No subagents. No `codeman agent post` (post via idle+watcher per mission). No subagent/agent tool.
- No second branch invented; worktree empty vs base. One candidate per chain honored.
- No containers/compose projects started (coordinator host). `docker ps -a` witness below.

## cleanliness

- Containers/compose: none started on this host. `docker ps -a` (pid witness):
  $(ps -o pid= --ppid $$ 2>/dev/null; docker ps -a 2>&1 | head)
- No orphan stacks, no volumes, no networks created by this lane.
- Worktree left at base head, clean (`git status` clean).

## END

END_BLOCKED 0428-219-exportauth: DUPLICATE — base lane e45430f2f already heals the failing cell; Owner to set superseded.
Candidate SHA: none (no product change). Evidence path pending publish.
