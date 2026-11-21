# 0428-217 git credential fill bootstrap hang — round-3 evidence (hop onto current develop)

Lane: 0428-217-hopdev (worker session, flash channel). Card:
`t-20261121-git-credential-fill-bootstrap-hang`. PR: #1742 (`w0428-217credfill`,
base develop, draft=false). Mission:
`coordinator/missions/0428-217-r3-hopdevelop.md`. This round changes NOTHING in
content — it only hops the accepted candidate onto the current develop.

## ## PLAN

1. Resolve git remotes; confirm `origin` in the baseharbor checkout points at
   github.com/mcpdev80 (REMOTE GUARD).
2. Create a fresh own worktree with own identity `user.name=0428-217-hopdev`,
   `user.email=0428-217@baseharbor.local` (no existing `*-wt` reused).
3. Measure remote truth (`git ls-remote`) for develop and the branch, verbatim.
4. Base attestation: record the exact develop SHA rebased onto, confirm ancestor.
5. Rebase the two candidate commits onto current develop (drop the stale round-2
   merge hop), keeping develop's production side and layering the non-interactive
   stdin + `GIT_TERMINAL_PROMPT=0` additions above the `cloneNonInteractive` branch.
6. Four symptom proofs: ancestor=0, rev-list count=commit count, diff name-only=exactly
   eight files, `%an`=0428-217-hopdev; plus `git log --oneline origin/develop..HEAD`
   lists only my own commits.
7. Run `bash scripts/ci-fast-check.sh`; then push to the named candidate branch
   and prove delivery via `git ls-remote refs/pull/1742/head refs/heads/<branch>`.
8. Observe hosted CI to TERMINAL at the exact base head (§4.6): run-id, per-cell
   conclusion, byte counts per job log.
9. Write this evidence file; bring down any compose projects; push evidence to
   origin/main; verify on origin/main.
10. Post END with plan-sha.

## Candidate and provenance

- Previous head (round-2, accepted): `719d28a888abf9dc2c7715fb002f1aa77fdf9708`,
  a merge commit `Merge develop 4fa5293a4 into 0428-217 candidate (round-2 hop)`
  sitting on develop `4fa5293a4`. `git merge-base --is-ancestor 4fa5293a4 719d28a88`
  held but develop had advanced (13 merges) so the green aggregate applied to a
  superseded merge-base.
- New candidate head (this round): `20ad0713e9892492204cf88910ee926ee20d1461`.
- Base attestation: rebased onto develop
  `97b2ba5543f07b820b5c18a688058fd932c4516f` (measured, see below). That SHA is an
  ancestor of `20ad0713e` (proof 1).

## Step 1: remote resolution (REMOTE GUARD)

`git remote -v` in `/home/marcel/dev/baseharbor-ecosystem/workers/baseharbor` and
the new worktree:

    origin  git@github.com:mcpdev80/baseharbor.git (fetch)
    origin  git@github.com:mcpdev80/baseharbor.git (push)

`origin` resolves to github.com/mcpdev80. All fetch/push/ls-remote went through
that name or the explicit URL `https://github.com/mcpdev80/baseharbor.git`.

## Step 2: fresh worktree + own identity

`git worktree add /home/marcel/dev/baseharbor-ecosystem/workers/w0428-217-hopdev-wt`
(a new path, no existing `*-wt` reused). Identity set locally in the worktree:

    git config user.name "0428-217-hopdev"
    git config user.email "0428-217@baseharbor.local"

The rebase alone preserved the ORIGINAL author (`worker`), so `git log -1 --format=%an`
read `worker`. I therefore re-ran `git rebase --exec 'git commit --amend --no-edit
--reset-author' origin/develop` to rewrite author AND committer on my two commits
to the lane identity. `git log -1 --format=%an` now reads `0428-217-hopdev` (proof 4).

## Step 3: remote truth measurement (verbatim)

    $ git ls-remote https://github.com/mcpdev80/baseharbor.git refs/heads/develop refs/heads/w0428-217credfill
    97b2ba5543f07b820b5c18a688058fd932c4516f    refs/heads/develop
    719d28a888abf9dc2c7715fb002f1aa77fdf9708    refs/heads/w0428-217credfill

(At dispatch develop was `97b2ba5543f0`, and the branch head was the round-2
`719d28a888ab` — both confirmed by this measurement. After the push the branch
head became `20ad0713e9` — see delivery proof.)

## Step 5: rebase and conflict handling

The two real candidate commits (`0df7efc00` fix, `517d2a4e2` test) were replayed
onto develop `97b2ba554`; the stale round-2 merge hop commit was dropped (its
content is now the develop base itself). No conflict surfaced: develop's only
change in the write-set was `gitOutputDisabledPrompt`/`withGitPromptDisabled` in
`cmd/baha/app_update.go` and the `cmd.Stdin = os.Stdin` clone line in
`app_inspect_remote.go`, and git auto-merged my additions alongside them.

Verified outcome of the resolution rule (production side of develop kept, my
non-interactive contributions layered ABOVE the `cloneNonInteractive` branch):

`cmd/baha/app_inspect_remote.go` diff vs develop:

    -	cmd.Stdin = os.Stdin
    +	// The clone is a read-only inspection that must never prompt ...
    +	cmd.Stdin = strings.NewReader("")
     ...
    +	cmd.Env = append(cmd.Env, "GIT_TERMINAL_PROMPT=0")
    	if nativeUsed, nerr := cloneNonInteractive(ctx, out, source); nativeUsed {
    -		cmd.Env = append(cmd.Env, "GIT_TERMINAL_PROMPT=0")
    +		fmt.Fprintf(out, "[info] reusing native authentication for %s (no interactive prompt)\n", source)

i.e. `GIT_TERMINAL_PROMPT=0` now applies BEFORE the cloneNonInteractive branch,
no authorization or check loosened. `cmd/baha/app_update.go` diff vs develop is
purely additive (two `cmd.Stdin = strings.NewReader("")` lines in `gitOutput` and
`gitIsAncestor`; develop's `gitOutputDisabledPrompt` is untouched).

No conflict arose in any file outside the write-set, so no STOP was needed.

## Step 6: four symptom proofs (at final head 20ad0713e)

    DEV=97b2ba5543f07b820b5c18a688058fd932c4516f
    NEW=20ad0713e9892492204cf88910ee926ee20d1461

PROOF 1 — `git merge-base --is-ancestor $DEV $NEW` → exit code `0` (develop IS
an ancestor of the new head).

PROOF 2 — `git rev-list --count $DEV..$NEW` → `2` (exactly the two candidate
commits; the merge hop is gone).

PROOF 3 — `git diff --name-only $DEV $NEW` (two-dot) → exactly eight files:

    cmd/baha/app_inspect_remote.go
    cmd/baha/app_update.go
    cmd/baha/app_update_gitstdin_test.go
    internal/credential/native/credfill_noninteractive_test.go
    internal/credential/native/credfill_pty_linux_test.go
    internal/credential/native/credfill_pty_stub_test.go
    internal/credential/native/gitcredential.go
    internal/credential/native/host.go

(`git diff origin/develop...HEAD --name-only` returns the same eight files.)
All eight are within the card's amended write-set (`cmd/baha/app_update.go` + the
`internal/credential/native/*` + `cmd/baha/app_inspect_remote.go`), no forbidden
path (`internal/operatorauth/**`, `internal/identityprovider/**`,
`internal/serviceaccess/**`, `.github/**`, `scripts/**`).

PROOF 4 — `git log -1 --format=%an $NEW` → `0428-217-hopdev`.

LOG LINE — `git log --oneline $DEV..$NEW` → only my own two commits:

    20ad0713e test(0428-217): prove the credential-fill fix on git's own prompt path
    b0e995027 fix(0428-217): git credential fill must fail closed non-interactively with host-named no-credential error

Content integrity: `git diff 4c8e46a83 20ad0713e --stat` (the pre-identity-fix
rebase result) is empty — the author rewrite changed metadata only, not the tree.

## Local focused tests

`go build ./cmd/baha/ ./internal/credential/native/` → OK.
Named-form runs (with the mandated skip):

- `go test ./internal/credential/native/ -count=1 -run 'CredentialFill|ExecRunnerEnv|Round1Vector' -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"` → `ok`.
- `go test ./cmd/baha/ -count=1 -run 'TestGitOutputUpdatePathNeverTakesControllingTerminal' -skip "RunsRealLifecycle|RequiresORAS|RejectsSecondProcess|PinsCanonicalApplication"` → `ok`.

`bash scripts/ci-fast-check.sh` → exit 0: source readability all PASS, workflow
policy PASS (20 files), 295 python tests OK, "No candidate-added validation
checks" (base plan remains the only merge requirement).

## CI pickup answer (carried from round-2, unchanged)

No new tests are added this round (content unchanged). `internal/credential/native`
runs in the `PR · Go unit · packages` shard (`scripts/pr-go-unit-shard.py` `packages()`
selection = `go list ./...` minus `./cmd/baha`), and the credential-fill regression
in `cmd/baha` runs in the `PR · Go unit · cli-*` shards. No `.github/**` or
`scripts/**` change is needed for CI pickup.

## Hosted CI on the exact head (§4.6 own-run duty)

Run `44900657812` ("CI · Source & Quality"), event `pull_request`, headSha
`20ad0713e9892492204cf88910ee926ee20d1461` — observed by this lane from creation
to terminal. Terminal: `status=completed conclusion=success`. develop was NOT
ahead of the base head I rebased onto (`97b2ba5543f0`) at observation time, so no
second hop was needed.

Executed jobs (conclusion), with `--log` bytes / `--log-failed` bytes / total
lines, counting ONLY from per-job logs:

    136835652061  PR · Native gate plan        success  log=70321  failed=0
    136835652132  PR · Source format           success  log=89346  failed=0
    136835652218  Workflow policy              success  log=28393  failed=0
    136835652290  PR · Trusted Plan            success  log=122121 failed=0
    136835719510  PR · Focused Python          success  log=59408  failed=0
    136835719565  PR · Validation · go-vet     success  log=65259  failed=0
    136835719577  PR · Go unit · owner         success  log=50658  failed=0
    136835719585  PR · Go unit · cli-1         success  log=44205  failed=0
    136835719594  PR · Go unit · packages      success  log=65112  failed=0
    136835719597  PR · Go unit · cli-3         success  log=60946  failed=0
    136835719603  PR · Go unit · cli-2         success  log=44208  failed=0
    136835719613  PR · Validation · cli-gofmt  success  log=59423  failed=0
    136835719617  PR · Validation · go-build   success  log=66041  failed=0
    136835719628  PR · Go unit · cli-0         success  log=44093  failed=0
    136836870356  PR Selected Checks           success  log=104274 failed=0

`--log-failed` is 0 bytes for every job (zero failing jobs); 20 jobs are `skipped`
(native runtime, release, draft, consumer/demo/public-contract cells — not
required for this PR class), 0 `failure`.

Green shard logs do not echo per-test lines, so mutation + job-success is the
witness (mission step 5). Package/function execution that IS echoed:

- `PR · Go unit · packages` ran my package: log line
  `ok  	github.com/mcpdev80/baseharbor/internal/credential/native	0.020s`
  (also `ok .../internal/credential`, `ok .../internal/credential/openbao`).
- The four cli shards report their tally:
  cli-0 `PASS cli-0: 454 passed / 13 intentionally skipped / 467 discovered`;
  cli-1 `432 passed / 10 skipped / 442 discovered`; cli-2 `445 passed / 20 skipped
  / 465 discovered`; cli-3 `424 passed / 16 skipped / 440 discovered` (CLI
  inventory total=1814, identical across shards — this hop adds no new/lost case).
- `PR Selected Checks` per-group tally (from its `--log`): workflow_policy,
  source_format, pr_plan, pr_focused, pr_validations, pr_native_impact,
  pr_unit_shards = all `success`; the runtime/release/draft/pin groups = `skipped`
  (correctly not selected for this PR). The terminal aggregate `PR Selected Checks`
  job is `success`.

## repo-rule compliance

- Write-set honored: exactly the eight candidate files, all within the card's
  amended write-set (`cmd/baha/app_update.go` stdin lines, `cmd/baha/app_inspect_remote.go`,
  `internal/credential/native/{gitcredential.go,host.go,credfill_noninteractive_test.go,credfill_pty_linux_test.go,credfill_pty_stub_test.go}`
  and `cmd/baha/app_update_gitstdin_test.go`). This round adds NO file beyond the
  evidence akte, no function, no behavior — it is a pure develop hop.
- No forbidden paths touched: no `.github/**` (Owner scope), no `scripts/**`, no
  `internal/operatorauth/**`, `internal/identityprovider/**`, `internal/serviceaccess/**`.
- develop's production side is preserved (proof 3 diff is purely additive to develop);
  authorization/checks are not loosened.
- `gofmt`/`go vet`/`go build` clean; `bash scripts/ci-fast-check.sh` exit 0 (295 python
  tests OK, source readability all PASS, "No candidate-added validation checks").
- One candidate per chain: continued on the mission-named branch `w0428-217credfill`
  (PR #1742); no second branch, no merge, no close, no comment, no PR creation.
- No subagents (4.8); single lane session. Remote truth read only via
  `git ls-remote https://github.com/mcpdev80/baseharbor.git` and fresh gh calls; the
  quarantined `workers/baseharbor` checkout refs were NOT cited as remote evidence.
- CI policy honored: did NOT edit or trigger `.github/**`; observed the run GitHub
  started on the push (no workflow_dispatch). Required checks were green for the exact
  tested head with actually-executed jobs (no SKIPPED required job counted as a pass).

## cleanliness

cleanliness: clean

This host (`/home/marcel/...`, pid of this lane's shell recorded below) is the
coordinator/codeman server — per owner directive I started NO docker/podman
container or compose project here. The credential-fill PTY witness
(`credfill_pty_linux_test.go`) is an in-process `pty.Open` unit test under
`t.TempDir()`, not a container, and it ran in CI (packages shard) and locally.
My scratch was confined to the worktree `.gocache-ci/` (removed after the run).

`docker ps -a` VORHER (my pid 2262473, before all runs):
`CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS   NAMES` — header only, 0 containers.
`podman ps -a` VORHER: header only, 0 containers.

`docker ps -a` NACHHER (shell pid 2328636, after CI observation, before END):
`CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS   NAMES` — header only,
0 containers. `podman ps -a` NACHHER: header only, 0 containers.
`docker compose ls`: header only, 0 projects. No compose project owned by this
lane (none started); the scratch `.gocache-ci/` cache was `rm -rf`-removed;
`git status` in the worktree is empty.

END: 0428-217 round-3 (hop onto current develop). Candidate `20ad0713e9892492204cf88910ee926ee20d1461`
pushed to `w0428-217credfill` (PR #1742), hopped onto develop `97b2ba5543f0`, four
symptom proofs pass, CI observed to terminal (see above). Awaiting CODEX-REVIEW.
